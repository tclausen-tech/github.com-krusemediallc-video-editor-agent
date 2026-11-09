"""Renderiza o vídeo 1080x1920 @30 fps a partir de roteiro.py.

uso:
  python3 render.py                       # vídeo completo -> ../../output/<nome>.mp4
  python3 render.py --frames 1.0,23.5     # só quadros PNG para conferência
  python3 render.py --frames 1.0 --guides # quadros com guias da área segura
"""
import argparse, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

from roteiro import SCENES, END, WORDS, ROOT

W, H, FPS = 1080, 1920, 30
# Identidade jamap.com.br (variáveis globais do Elementor do site)
NAVY = (0, 29, 82)        # --e-global-color-secondary #001D52
YEL = (254, 191, 0)       # --e-global-color-primary   #FEBF00
RED = (239, 68, 68)       # --e-global-color-2d3477f   #EF4444
GRAY = (96, 96, 96)       # --e-global-color-text      #606060
WHITE = (255, 255, 255)
INK = {"navy": NAVY, "red": RED, "gray": GRAY}

A = lambda *p: os.path.join(ROOT, "assets", *p)
FONTS = {}


def font(name, size):
    k = (name, size)
    if k not in FONTS:
        FONTS[k] = ImageFont.truetype(A("fonts", name + ".ttf"), size)
    return FONTS[k]


def ease_out(p):
    p = min(max(p, 0.0), 1.0)
    return 1 - (1 - p) ** 3


def clamp(x, a=0.0, b=1.0):
    return min(max(x, a), b)


# ---------------------------------------------------------------- fundos
def cover(img, w, h, focus=(0.5, 0.5)):
    s = max(w / img.width, h / img.height)
    im = img.resize((math.ceil(img.width * s), math.ceil(img.height * s)), Image.LANCZOS)
    x = int((im.width - w) * focus[0]); y = int((im.height - h) * focus[1])
    return im.crop((x, y, x + w, y + h))


PHOTO = {}


def photo(name):
    if name not in PHOTO:
        PHOTO[name] = Image.open(A("photos", name + ".jpg")).convert("RGB")
    return PHOTO[name]


K = 1.3  # margem do fundo para o zoom


class PhotoBG:
    """Foto real em tela cheia: push-in de 1,0 -> 1,12x em 0,7 s (ease-out) + drift lento."""

    def __init__(self, sc):
        self.base = cover(photo(sc["img"]), int(W * K), int(H * K), sc.get("focus", (0.5, 0.5)))
        self.z0 = sc.get("zoom0", 1.0)

    def frame(self, lt):
        z = self.z0 + 0.12 * ease_out(lt / 0.7) + 0.012 * max(lt - 0.7, 0)
        # a base tem K vezes o tamanho do quadro: a janela visível encolhe com o zoom
        cw, ch = self.base.width / z, self.base.height / z
        cx, cy = self.base.width / 2, self.base.height / 2
        box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
        return self.base.transform((W, H), Image.EXTENT, box, Image.BILINEAR)


# Quadro branco real (foto) sobre a parede do escritório desfocada
BOARD_BOX = (40, 300, 1040, 910)       # posição do quadro no frame
BOARD_TEXT = (92, 352, 1000, 860)      # área útil de escrita


def board_bg():
    wall = cover(photo("escritorio"), W, H, (0.42, 0.35)).filter(ImageFilter.GaussianBlur(16))
    wall = ImageEnhance.Brightness(wall).enhance(1.08)
    wall = Image.blend(wall, Image.new("RGB", (W, H), (236, 238, 242)), 0.35)
    bd = photo("quadro")
    bw = BOARD_BOX[2] - BOARD_BOX[0]; bh = BOARD_BOX[3] - BOARD_BOX[1]
    bd = bd.resize((bw, bh), Image.LANCZOS)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
    d.rectangle((BOARD_BOX[0] + 10, BOARD_BOX[1] + 18, BOARD_BOX[2] + 10, BOARD_BOX[3] + 22), fill=(0, 20, 50, 110))
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    out = wall.convert("RGBA"); out.alpha_composite(sh); out.paste(bd, BOARD_BOX[:2])
    return out.convert("RGB")


# ---------------------------------------------------------------- personagem
CH_H = 1064
CHAR_POS = (428, 858)   # canto superior esquerdo; a base sai do quadro como na referência


class Character:
    def __init__(self, rms):
        src = Image.open(A("personagem", "personagem.webp")).convert("RGBA")
        self.s = CH_H / src.height
        self.img = src.resize((round(src.width * self.s), CH_H), Image.LANCZOS)
        sh = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        sh.putalpha(self.img.getchannel("A").point(lambda a: a * 0.35))
        self.shadow = sh.filter(ImageFilter.GaussianBlur(14))
        self.rms = rms
        # boca (coordenadas da imagem original): sorriso de x 502–737, y 686–727
        self.mouth = (620 * self.s, 700 * self.s, 236 * self.s)

    def mouth_patch(self, o):
        cx, cy, mw = self.mouth
        S = 4
        pw, ph = int(mw * 1.2 * S), int(mw * 0.8 * S)
        p = Image.new("RGBA", (pw, ph), (0, 0, 0, 0)); d = ImageDraw.Draw(p)
        half = mw * (0.36 + 0.06 * o) * S
        depth = mw * (0.08 + 0.30 * o) * S
        x0, x1 = pw / 2 - half, pw / 2 + half; top = ph * 0.18
        pts = [(x0, top)]
        for k in range(1, 20):
            a = k / 20
            pts.append((x0 + (x1 - x0) * a, top - 0.05 * depth * math.sin(math.pi * a)))
        pts.append((x1, top))
        for k in range(20, -1, -1):
            a = k / 20
            pts.append((x0 + (x1 - x0) * a, top + depth * math.sin(math.pi * a) ** 0.8))
        d.polygon(pts, fill=(112, 26, 38, 255))
        # língua
        tw = (x1 - x0) * 0.42
        d.ellipse((pw / 2 - tw / 2, top + depth * 0.55, pw / 2 + tw / 2, top + depth * 1.25), fill=(214, 96, 104, 255))
        d.polygon(pts, outline=(150, 20, 30, 255))
        m = Image.new("L", p.size, 0); ImageDraw.Draw(m).polygon(pts, fill=255)
        p.putalpha(Image.fromarray(np.minimum(np.array(p.getchannel("A")), np.array(m))))
        p = p.resize((pw // S, ph // S), Image.LANCZOS)
        return p, (int(cx - pw / S / 2), int(cy - ph / S * 0.18 - 2))

    def draw(self, frame, t, hop):
        f = int(t * FPS)
        o = self.rms[f] if f < len(self.rms) else 0.0
        im = self.img
        if o > 0.12:
            im = im.copy(); p, pos = self.mouth_patch(o); im.alpha_composite(p, pos)
        breath = 1 + 0.006 * math.sin(2 * math.pi * t / 3.4)
        nh = round(CH_H * breath)
        if nh != CH_H:
            im = im.resize((im.width, nh), Image.BILINEAR)
        x = CHAR_POS[0] + round(3 * math.sin(2 * math.pi * t / 5.1))
        y = CHAR_POS[1] + (CH_H - nh) - round(hop)
        frame.alpha_composite(self.shadow, (x + 14, CHAR_POS[1] + 16))
        frame.alpha_composite(im, (x, y))


def audio_rms(path):
    """Volume da voz por quadro (0..1) para abrir a boca."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "24000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    hop = 24000 // FPS
    n = len(a) // hop
    r = np.sqrt(np.mean(a[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-9)
    db = 20 * np.log10(r)
    o = np.clip((db + 42) / 24, 0, 1)
    o = np.convolve(o, [0.25, 0.5, 0.25], mode="same")   # suaviza
    # só abre a boca dentro de palavras
    on = np.zeros(n, bool)
    for wd in WORDS:
        on[int(wd["s"] * FPS): int(wd["e"] * FPS) + 1] = True
    return np.where(on[:n], o, 0.0)


# ---------------------------------------------------------------- etiquetas
LABEL_TOP = 492   # ~26% da altura, como na referência (y 328/1280)
ROW = 116


def label_img(text, style):
    big = style == "y"
    f = font("Poppins-Bold", {"y": 66, "hook": 62}.get(style, 54))
    lines = text.split("\n")
    bg, fg = {"n": (NAVY, WHITE), "r": (RED, WHITE), "y": (YEL, NAVY), "hook": (NAVY, WHITE)}[style]
    px, py, gap = 30, 14, 6
    sizes = []
    for ln in lines:
        b = f.getbbox(ln.replace("*", ""))
        sizes.append((b[2] - b[0], b[3] - b[1], b))
    lh = f.size * 1.12
    bw = max(s[0] for s in sizes) + 2 * px
    bh = int(lh * len(lines) + 2 * py + (gap if len(lines) > 1 else 0))
    im = Image.new("RGBA", (int(bw), bh + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, bw, bh), fill=bg + (255,))
    if style in ("n", "hook"):
        d.rectangle((0, bh, bw, bh + 8), fill=YEL + (255,))   # faixa amarela da marca
    y = py - 4
    for ln, (lw, _, b) in zip(lines, sizes):
        col = fg
        if ln.startswith("*"):
            col = YEL; ln = ln.strip("*")
        d.text(((bw - lw) / 2 - b[0], y + (lh - f.size) / 2 + 2), ln, font=f, fill=col)
        y += lh
    return im


LCACHE = {}


def draw_label(frame, text, style, row, a, sc, y0=None):
    k = (text, style)
    if k not in LCACHE:
        LCACHE[k] = label_img(text, style)
    im = LCACHE[k]
    if style == "hook":
        y0 = 360
    y = (y0 if y0 is not None else LABEL_TOP) + row * ROW
    if sc != 1.0:
        im = im.resize((max(1, round(im.width * sc)), max(1, round(im.height * sc))), Image.BILINEAR)
    if a < 1.0:
        im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
    frame.alpha_composite(im, (round(W / 2 - im.width / 2), round(y + (1 - sc) * im.height / 2)))


def label_state(t, t_in, t_out):
    """Fade de 3 quadros com leve scale-up (0,96 -> 1,0), saída em 3 quadros."""
    fin, fout = 3 / FPS, 3 / FPS
    if t < t_in or t >= t_out:
        return None
    p = (t - t_in) / fin
    a = clamp(p) ; sc = 0.96 + 0.04 * clamp(p)
    if t_in == 0.0:
        a, sc = 1.0, 1.0
    q = (t_out - t) / fout
    if q < 1:
        a = min(a, clamp(q))
    return a, sc


# ---------------------------------------------------------------- legenda
def caption_chunks():
    out, cur = [], []
    for i, wd in enumerate(WORDS):
        cur.append(wd)
        txt = " ".join(x["w"] for x in cur)
        nxt = WORDS[i + 1] if i + 1 < len(WORDS) else None
        brk = (wd["w"][-1] in ",.?!" or len(cur) >= 3 or len(txt) >= 15 or nxt is None
               or (nxt and nxt["s"] - wd["e"] > 0.35))
        if nxt and not brk and len(txt + " " + nxt["w"]) > 19:
            brk = True
        if brk:
            out.append([cur[0]["s"], cur[-1]["e"], txt]); cur = []
    for k in range(len(out)):
        nxt_s = out[k + 1][0] if k + 1 < len(out) else END
        out[k][1] = nxt_s if nxt_s - out[k][1] < 0.6 else out[k][1] + 0.25
    return out


CAP_Y = 1470
CCACHE = {}


def caption_img(txt):
    if txt in CCACHE:
        return CCACHE[txt]
    t = txt.upper().strip(",.")
    size = 62
    while True:
        f = font("Poppins-Black", size)
        b = f.getbbox(t, stroke_width=7)
        if b[2] - b[0] <= 940 or size <= 40:
            break
        size -= 2
    im = Image.new("RGBA", (b[2] - b[0] + 30, b[3] - b[1] + 30), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((15 - b[0] + 3, 15 - b[1] + 5), t, font=f, fill=(0, 0, 0, 150), stroke_width=7, stroke_fill=(0, 0, 0, 150))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)))
    ImageDraw.Draw(im).text((15 - b[0], 15 - b[1]), t, font=f, fill=WHITE, stroke_width=7, stroke_fill=(10, 14, 30))
    CCACHE[txt] = im
    return im


# ---------------------------------------------------------------- quadro branco (write-on)
def marker_img():
    S = 3
    im = Image.new("RGBA", (60 * S, 230 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((14 * S, 40 * S, 46 * S, 200 * S), 12 * S, fill=NAVY + (255,))
    d.rounded_rectangle((12 * S, 150 * S, 48 * S, 228 * S), 12 * S, fill=YEL + (255,))
    d.polygon([(18 * S, 40 * S), (42 * S, 40 * S), (34 * S, 14 * S), (26 * S, 14 * S)], fill=(30, 30, 30, 255))
    d.rectangle((27 * S, 2 * S, 33 * S, 16 * S), fill=(20, 20, 20, 255))
    im = im.resize((60, 230), Image.LANCZOS).rotate(-28, expand=True, resample=Image.BICUBIC)
    return im


MARKER = None


class Board:
    def __init__(self, sc):
        self.items = sc["items"]
        self.lines = []   # dict(text,color,size,t,dur,y,img,subs=[])
        for it in self.items:
            if it[0] == "write":
                _, t, text, col, size = it
                size = int(size * 1.3)   # escala única do texto do quadro
                self.lines.append(dict(t=t, text=text, col=INK[col], size=size, subs=[]))
        for it in self.items:
            if it[0] == "sub":
                self.lines[it[2]]["subs"].append(dict(t=it[1], text=it[3]))
        # layout vertical
        avail = BOARD_TEXT[3] - BOARD_TEXT[1]
        ss = 56   # tamanho das sublinhas
        total = sum(ln["size"] * 1.18 + len(ln["subs"]) * ss * 1.2 for ln in self.lines)
        if total > avail:   # encolhe tudo por igual para caber no quadro
            k = avail / total
            for ln in self.lines:
                ln["size"] = int(ln["size"] * k)
            ss = int(ss * k)
        total = 0
        for ln in self.lines:
            ln["h"] = ln["size"] * 1.18 + len(ln["subs"]) * ss * 1.2
            total += ln["h"]
        y = BOARD_TEXT[1] + max(0, (BOARD_TEXT[3] - BOARD_TEXT[1] - total) / 2 - 10)
        for ln in self.lines:
            ln["img"], ln["bb"] = self.text_img(ln["text"], ln["size"], ln["col"])
            ln["y"] = y; ln["x"] = BOARD_TEXT[0]
            ln["dur"] = clamp(0.045 * len(ln["text"]), 0.35, 1.1)
            sy = y + ln["size"] * 1.18
            for s in ln["subs"]:
                s["img"], s["bb"] = self.text_img(s["text"], ss, GRAY)
                s["y"] = sy; s["x"] = BOARD_TEXT[0] + 40; s["dur"] = clamp(0.04 * len(s["text"]), 0.35, 0.9)
                sy += ss * 1.2
            y += ln["h"]
        self.strikes = [(it[1], it[2]) for it in self.items if it[0] == "strike"]
        self.hls = [(it[1], it[2]) for it in self.items if it[0] == "hl"]
        self.stamps = [(it[1], it[2]) for it in self.items if it[0] == "stamp"]

    @staticmethod
    def text_img(text, size, col):
        f = font("PermanentMarker-Regular", size)
        while f.getbbox(text)[2] > BOARD_TEXT[2] - BOARD_TEXT[0] and size > 30:
            size -= 4; f = font("PermanentMarker-Regular", size)
        b = f.getbbox(text)
        im = Image.new("RGBA", (b[2] + 10, int(size * 1.4)), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((0, int(size * 0.1)), text, font=f, fill=col + (255,))
        bb = im.getbbox()
        return im, bb

    def writers(self):
        for ln in self.lines:
            yield ln
            yield from ln["subs"]

    def draw(self, frame, t):
        global MARKER
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        # marca-texto amarelo (atrás do texto)
        for th, idx in self.hls:
            if t < th:
                continue
            ln = self.lines[idx]; bb = ln["bb"]
            p = ease_out((t - th) / 0.35)
            x0 = ln["x"] + bb[0] - 10; x1 = x0 + (bb[2] - bb[0] + 20) * p
            yc = ln["y"] + (bb[1] + bb[3]) / 2 + ln["size"] * 0.08
            d.rectangle((x0, yc - ln["size"] * 0.34, x1, yc + ln["size"] * 0.34), fill=YEL + (150,))
        tip = None
        for ln in self.writers():
            if t < ln["t"]:
                continue
            p = clamp((t - ln["t"]) / ln["dur"])
            im = ln["img"]; bb = ln["bb"]
            xr = bb[0] + (bb[2] - bb[0]) * p
            if p < 1:
                im = im.crop((0, 0, max(1, int(xr)), im.height))
                tip = (ln["x"] + xr, ln["y"] + (bb[1] + bb[3]) / 2)
            lay.alpha_composite(im, (int(ln["x"]), int(ln["y"])))
        for th, idx in self.strikes:
            if t < th:
                continue
            ln = self.lines[idx]; bb = ln["bb"]
            p = ease_out((t - th) / 0.3)
            y = ln["y"] + (bb[1] + bb[3]) / 2 + 4
            x0 = ln["x"] + bb[0] - 12; x1 = x0 + (bb[2] - bb[0] + 24) * p
            d.line((x0, y + 6, x1, y - 6 * p), fill=RED + (255,), width=12)
            if p < 1:
                tip = (x1, y)
        for th, txt in self.stamps:
            if t < th:
                continue
            p = ease_out((t - th) / 0.18)
            lay.alpha_composite(self.stamp(txt, 1.8 - 0.8 * p, p), (0, 0))
        frame.alpha_composite(lay)
        if tip:
            MARKER = MARKER or marker_img()
            frame.alpha_composite(MARKER, (int(tip[0] - 8), int(tip[1] - MARKER.height + 30)))

    SCACHE = {}

    def stamp(self, txt, sc, a):
        f = font("Poppins-Black", 120)
        b = f.getbbox(txt)
        im = Image.new("RGBA", (b[2] + 80, b[3] + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((6, 6, im.width - 6, im.height - 6), 18, outline=RED + (255,), width=12)
        d.text((40 - b[0], 30 - b[1]), txt, font=f, fill=RED + (255,))
        im = im.rotate(12, expand=True, resample=Image.BICUBIC)
        im = im.resize((int(im.width * sc), int(im.height * sc)), Image.BILINEAR)
        im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
        out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        out.alpha_composite(im, (int(600 - im.width / 2), int(700 - im.height / 2)))
        return out


# ---------------------------------------------------------------- CTA (cartão + URL digitando)
def cta_card(t, sc):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if t < sc["card"]:
        return lay
    p = ease_out((t - sc["card"]) / 0.3)
    cw, chh = 820, 300
    card = Image.new("RGBA", (cw, chh), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
    d.rounded_rectangle((0, 0, cw - 1, chh - 1), 36, fill=WHITE + (255,))
    icon = Image.open(A("brand", "icon_jamap_azul.e.amarelo.png")).convert("RGBA")
    icon = icon.resize((round(icon.width * 170 / icon.height), 170), Image.LANCZOS)
    card.alpha_composite(icon, (40, 30))
    logo = Image.open(A("brand", "logo-jamap-1-ok.png")).convert("RGBA")
    logo = logo.resize((round(logo.width * 100 / logo.height), 100), Image.LANCZOS)
    card.alpha_composite(logo, (230, 40))
    # barra de endereço com digitação
    d.rounded_rectangle((230, 170, cw - 40, 250), 40, fill=(240, 242, 246, 255), outline=(221, 224, 223, 255), width=3)
    t0, t1 = sc["url"]
    n = int(len(sc["url_text"]) * clamp((t - t0) / (t1 - t0))) if t >= t0 else 0
    f = font("Poppins-SemiBold", 44)
    d.text((262, 182), sc["url_text"][:n], font=f, fill=NAVY + (255,))
    if (int(t * 2) % 2 == 0) or (t0 <= t <= t1):
        cx = 262 + f.getlength(sc["url_text"][:n]) + 4
        d.rectangle((cx, 186, cx + 4, 236), fill=NAVY + (255,))
    # sombra
    sh = Image.new("RGBA", (cw + 80, chh + 80), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((40, 50, cw + 40, chh + 50), 36, fill=(0, 20, 50, 90))
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    s = 0.78 + 0.12 * p
    x = W / 2 - cw * s / 2; y = 610 + (1 - p) * 40
    sh2 = sh.resize((int(sh.width * s), int(sh.height * s)))
    lay.alpha_composite(sh2, (int(x - 40 * s), int(y - 40 * s)))
    c2 = card.resize((int(cw * s), int(chh * s)), Image.BILINEAR)
    c2.putalpha(c2.getchannel("A").point(lambda v: int(v * p)))
    lay.alpha_composite(c2, (int(x), int(y)))
    # anel de clique no fim da digitação (como o cursor da referência)
    if t1 <= t < t1 + 0.35:
        q = (t - t1) / 0.35; r = 20 + 50 * q
        cx = x + (262 + f.getlength(sc["url_text"]) + 30) * s; cy = y + 210 * s
        ImageDraw.Draw(lay).ellipse((cx - r, cy - r, cx + r, cy + r), outline=YEL + (int(255 * (1 - q)),), width=8)
    return lay


# ---------------------------------------------------------------- montagem
def scene_at(t):
    k = 0
    for i, sc in enumerate(SCENES):
        if sc["t0"] <= t:
            k = i
    return k


def label_windows(sc, end):
    labs = sc.get("labels", [])
    out = []
    for i, (ti, to, txt, st, row) in enumerate(labs):
        if to is None:
            # sai quando entra a próxima da mesma linha, ou no corte
            nx = [l[0] for l in labs[i + 1:] if l[4] == row]
            to = nx[0] if nx else end
        out.append((ti, min(to, end), txt, st, row))
    return out


def guides(frame):
    d = ImageDraw.Draw(frame)
    d.rectangle((60, 300, 940, 1490), outline=(255, 0, 255, 255), width=3)
    d.rectangle((950, 960, 1080, 1700), outline=(255, 0, 0, 255), width=3)
    d.line((0, 285, W, 285), fill=(0, 255, 255, 255), width=2); d.line((0, 1635, W, 1635), fill=(0, 255, 255, 255), width=2)


class Renderer:
    def __init__(self):
        self.audio = os.path.join(ROOT, "in", "narracao.mp3")
        self.char = Character(audio_rms(self.audio))
        self.caps = caption_chunks()
        self.bgs = {}
        self.board_bg = None
        self.ends = [SCENES[i + 1]["t0"] if i + 1 < len(SCENES) else END for i in range(len(SCENES))]
        self.hops = sorted(l[0] for sc in SCENES for l in sc.get("labels", []) if l[0] > 0)

    def bg(self, i, lt):
        sc = SCENES[i]
        if sc["kind"] == "board":
            if self.board_bg is None:
                self.board_bg = board_bg()
            return self.board_bg.copy()
        if i not in self.bgs:
            self.bgs = {i: PhotoBG(sc)}   # só a cena atual em memória
        return self.bgs[i].frame(lt)

    def frame(self, t, show_guides=False):
        i = scene_at(t); sc = SCENES[i]; end = self.ends[i]; lt = t - sc["t0"]
        fr = self.bg(i, lt).convert("RGBA")
        if sc["kind"] == "board":
            if sc.get("_b") is None:
                sc["_b"] = Board(sc)
            sc["_b"].draw(fr, t)
        if sc["kind"] == "cta":
            fr.alpha_composite(cta_card(t, sc))
        # personagem (pulinho quando entra uma etiqueta)
        hop = 0.0
        for h in self.hops:
            if 0 <= t - h < 0.3:
                hop = 16 * math.sin(math.pi * (t - h) / 0.3)
        self.char.draw(fr, t, hop)
        for ti, to, txt, st, row in label_windows(sc, end):
            s = label_state(t, ti, to)
            if s:
                draw_label(fr, txt, st, row, s[0], s[1])
        for c0, c1, txt in self.caps:
            if c0 <= t < c1:
                im = caption_img(txt)
                fr.alpha_composite(im, (round(W / 2 - im.width / 2), round(CAP_Y - im.height / 2)))
                break
        if show_guides:
            guides(fr)
        return fr.convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", help="tempos em s separados por vírgula")
    ap.add_argument("--guides", action="store_true")
    ap.add_argument("--out", default=os.path.join(ROOT, "..", "output", "vale-a-pena-vender-para-o-governo.mp4"))
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=END)
    a = ap.parse_args()
    r = Renderer()
    if a.frames:
        od = os.path.join(ROOT, "previews"); os.makedirs(od, exist_ok=True)
        for ts in a.frames.split(","):
            t = float(ts); fn = os.path.join(od, f"f_{t:07.2f}.png")
            r.frame(t, a.guides).save(fn); print(fn)
        return
    n0, n1 = int(round(a.start * FPS)), int(math.ceil(a.end * FPS))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-ss", f"{a.start}", "-t", f"{a.end - a.start}", "-i", r.audio,
           "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", a.out]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for n in range(n0, n1):
        ff.stdin.write(r.frame(n / FPS).tobytes())
        if n % 300 == 0:
            print(f"{n / FPS:6.1f}s", flush=True)
    ff.stdin.close(); ff.wait()
    print("ok", a.out)


if __name__ == "__main__":
    main()
