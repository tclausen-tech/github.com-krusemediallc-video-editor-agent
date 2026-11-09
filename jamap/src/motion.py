"""Cenas de motion graphics ("pow") na identidade Jamap.

Fundo azul-marinho (ou amarelo) animado, tipografia cinética palavra a palavra com
overshoot, marca-texto, risco, carimbo, barras que crescem, flash e tremida nos impactos.
"""
import math
from PIL import Image, ImageDraw, ImageFilter

W, H = 1080, 1920
NAVY = (0, 29, 82); YEL = (254, 191, 0); RED = (239, 68, 68); WHITE = (255, 255, 255)
AREA = (330, 880)          # faixa vertical do texto (acima da personagem)
X0, X1 = 70, 1010


def clamp(x, a=0.0, b=1.0):
    return min(max(x, a), b)


def ease_out(p):
    p = clamp(p); return 1 - (1 - p) ** 3


def ease_back(p, s=2.2):
    p = clamp(p) - 1; return 1 + (s + 1) * p ** 3 + s * p ** 2


# ---------------------------------------------------------------- fundos
def _gradient(c_in, c_out):
    g = Image.radial_gradient("L").resize((W * 2, H * 2)).crop((W // 2, H // 2 - 200, W // 2 + W, H // 2 - 200 + H))
    a = Image.new("RGB", (W, H), c_in); b = Image.new("RGB", (W, H), c_out)
    return Image.composite(b, a, g)


BG = {}


def _static(style):
    if style not in BG:
        if style == "yellow":
            base = _gradient((255, 208, 40), (240, 168, 0))
            dot = (0, 29, 82, 34)
        else:
            base = _gradient((12, 52, 128), (0, 14, 44))
            dot = (255, 255, 255, 26)
        tile = Image.new("RGBA", (W + 120, H + 120), (0, 0, 0, 0)); d = ImageDraw.Draw(tile)
        for y in range(0, H + 120, 60):
            for x in range(0, W + 120, 60):
                d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=dot)
        BG[style] = (base.convert("RGBA"), tile)
    return BG[style]


def background(style, lt):
    base, tile = _static(style)
    fr = base.copy()
    off = int(lt * 40) % 60
    fr.alpha_composite(tile.crop((off, off, off + W, off + H)))
    d = ImageDraw.Draw(fr)
    acc = NAVY if style == "yellow" else YEL
    # anéis girando
    for k, (cx, cy, r, w_, sp) in enumerate([(930, 420, 260, 26, 40), (120, 1500, 340, 34, -28)]):
        a0 = lt * sp + k * 90
        d.arc((cx - r, cy - r, cx + r, cy + r), a0, a0 + 250, fill=acc + (70,), width=w_)
    # faixa diagonal que atravessa a tela devagar
    x = -600 + (lt * 120) % 2400
    d.polygon([(x, 0), (x + 120, 0), (x - 900, H), (x - 1020, H)], fill=acc + (22,))
    return fr


# ---------------------------------------------------------------- textos
def _font(fontf, name, size):
    return fontf(name, size)


class Motion:
    def __init__(self, sc, fontf):
        self.sc = sc; self.font = fontf
        self.style = sc.get("bg", "navy")
        on_y = self.style == "yellow"
        self.col = {"navy": NAVY if on_y else WHITE, "gray": (90, 70, 20) if on_y else (170, 186, 222),
                    "red": RED, "yel": NAVY if on_y else YEL}
        items = sc["items"]
        self.lines = []
        for it in items:
            if it[0] == "write":
                _, t, text, col, size = it
                self.lines.append(dict(t=t, text=text.upper(), col=self.col[col], size=int(size * 1.15), subs=[]))
        for it in items:
            if it[0] == "sub":
                self.lines[it[2]]["subs"].append(dict(t=it[1], text=it[3].upper()))
        area = sc.get("area", AREA)
        avail = area[1] - area[0]; ss = 46
        total = sum(l["size"] * 1.12 + len(l["subs"]) * ss * 1.25 for l in self.lines)
        if total > avail:
            k = avail / total
            for l in self.lines:
                l["size"] = int(l["size"] * k)
            ss = int(ss * k); total = avail
        y = area[0] + (avail - total) / 2
        for l in self.lines:
            self._words(l, l["size"], "Poppins-Black")
            l["y"] = y; y += l["size"] * 1.12
            for s in l["subs"]:
                s["col"] = self.col["gray"]; self._words(s, ss, "Poppins-ExtraBold")
                s["y"] = y; y += ss * 1.25
        self.strikes = [(i[1], i[2]) for i in items if i[0] == "strike"]
        self.hls = [(i[1], i[2]) for i in items if i[0] == "hl"]
        self.stamps = [(i[1], i[2]) for i in items if i[0] == "stamp"]
        self.bars = [i for i in items if i[0] == "bars"]
        self.pills = [i for i in items if i[0] == "pill"]
        self.impacts = sorted([l["t"] for l in self.lines if l["size"] >= 100] + [s[0] for s in self.strikes]
                              + [s[0] for s in self.stamps] + [p[1] for p in self.pills])

    def _words(self, l, size, fname):
        """Quebra a linha em palavras (cada uma entra com seu próprio pop)."""
        while True:
            f = self.font(fname, size)
            if f.getlength(l["text"]) <= X1 - X0 or size <= 30:
                break
            size -= 3
        l["size"] = size; l["f"] = f
        sp = f.getlength(" "); x = 0; ws = []
        for wd in l["text"].split(" "):
            ws.append((wd, x)); x += f.getlength(wd) + sp
        l["width"] = x - sp; l["words"] = ws

    def _word_img(self, wd, f, col):
        b = f.getbbox(wd)
        im = Image.new("RGBA", (b[2] + 24, int(f.size * 1.45)), (0, 0, 0, 0))
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((6, int(f.size * 0.12) + 6), wd, font=f, fill=(0, 0, 0, 90))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)))
        ImageDraw.Draw(im).text((0, int(f.size * 0.12)), wd, font=f, fill=col + (255,))
        return im

    def shake(self, t):
        dx = dy = 0.0
        for ti in self.impacts:
            q = t - ti
            if 0 <= q < 0.3:
                a = 14 * (1 - q / 0.3)
                dx += a * math.sin(q * 90); dy += a * math.cos(q * 70)
        return int(dx), int(dy)

    def flash(self, t):
        a = 0.0
        for ti in self.impacts:
            q = t - ti
            if 0 <= q < 0.12:
                a = max(a, 0.35 * (1 - q / 0.12))
        return a

    def draw(self, frame, t):
        lt = t - self.sc["t0"]
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        hl_on = {}
        for th, idx in self.hls:
            if t >= th:
                hl_on[idx] = th
        # marca-texto (caixa que cresce do centro)
        for idx, th in hl_on.items():
            l = self.lines[idx]; p = ease_out((t - th) / 0.25)
            cx = W / 2; hw = (l["width"] / 2 + 26) * p
            box = WHITE if self.style == "yellow" else YEL
            d.rounded_rectangle((cx - hw, l["y"] + l["size"] * 0.05, cx + hw, l["y"] + l["size"] * 1.2), 16, fill=box + (255,))
        for i, l in enumerate(self.lines):
            col = NAVY if i in hl_on and t >= hl_on[i] + 0.1 else l["col"]   # texto sobre o marca-texto
            self._draw_line(lay, l, t, col)
            for s in l["subs"]:
                self._draw_line(lay, s, t, s["col"])
        for th, idx in self.strikes:
            if t < th:
                continue
            l = self.lines[idx]; p = ease_out((t - th) / 0.2)
            x0 = W / 2 - l["width"] / 2 - 20; x1 = x0 + (l["width"] + 40) * p
            y = l["y"] + l["size"] * 0.68
            d.line((x0, y + 8, x1, y - 8 * p), fill=RED + (255,), width=max(10, l["size"] // 7))
        for b in self.bars:
            self._bars(lay, b, t)
        for p in self.pills:
            self._pill(lay, p, t)
        for th, txt in self.stamps:
            if t >= th:
                self._stamp(lay, txt, t - th)
        dx, dy = self.shake(t)
        frame.alpha_composite(lay, (dx, dy)) if (dx or dy) else frame.alpha_composite(lay)
        fa = self.flash(t)
        if fa > 0:
            frame.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(255 * fa))))

    def _draw_line(self, lay, l, t, col):
        if t < l["t"]:
            return
        key = ("img", col)
        imgs = l.setdefault("_imgs", {})
        if key not in imgs:
            imgs[key] = [self._word_img(wd, l["f"], col) for wd, _ in l["words"]]
        left = W / 2 - l["width"] / 2
        for k, ((wd, x), im) in enumerate(zip(l["words"], imgs[key])):
            q = (t - l["t"] - k * 0.07) / 0.3
            if q <= 0:
                continue
            s = 0.35 + 0.65 * ease_back(q)
            a = clamp(q * 3)
            yo = (1 - ease_out(q)) * 50
            w2 = im
            if abs(s - 1) > 0.01:
                w2 = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR)
            if a < 1:
                w2 = w2.copy(); w2.putalpha(w2.getchannel("A").point(lambda v: int(v * a)))
            cx = left + x + im.width / 2 - 12; cy = l["y"] + im.height / 2 + yo
            lay.alpha_composite(w2, (int(cx - w2.width / 2), int(cy - w2.height / 2)))

    def _bars(self, lay, b, t):
        _, t0, labels, base = b
        d = ImageDraw.Draw(lay); n = len(labels)
        bw, gap = 130, 50; tot = n * bw + (n - 1) * gap; x = W / 2 - tot / 2
        on_y = self.style == "yellow"
        f = self.font("Poppins-ExtraBold", 33)
        for k, lab in enumerate(labels):
            q = ease_back((t - t0 - k * 0.18) / 0.4, 1.6)
            if t - t0 - k * 0.18 <= 0:
                x += bw + gap; continue
            hmax = 50 + 150 * (k / (n - 1)) ** 1.2
            h = hmax * max(q, 0)
            body = NAVY if on_y else WHITE
            d.rounded_rectangle((x, base - h, x + bw, base), 14, fill=body + (255,))
            d.rounded_rectangle((x, base - h, x + bw, base - h + min(h, 22)), 10, fill=(RED if on_y else YEL) + (255,))
            tw = f.getlength(lab)
            d.text((x + bw / 2 - tw / 2, base + 12), lab, font=f, fill=(NAVY if on_y else WHITE) + (255,))
            x += bw + gap

    def _pill(self, lay, p, t):
        _, t0, text, y = p
        q = (t - t0) / 0.3
        if q <= 0:
            return
        f = self.font("Poppins-Black", 64)
        tw = f.getlength(text)
        im = Image.new("RGBA", (int(tw + 90), 120), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        on_y = self.style == "yellow"
        d.rounded_rectangle((0, 0, im.width - 1, 119), 60, fill=(NAVY if on_y else YEL) + (255,))
        d.text((45, 18), text, font=f, fill=(YEL if on_y else NAVY) + (255,))
        s = 0.3 + 0.7 * ease_back(q, 2.6)
        im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR)
        lay.alpha_composite(im, (int(W / 2 - im.width / 2), int(y + 60 - im.height / 2)))

    def _stamp(self, lay, txt, q):
        p = ease_out(q / 0.16)
        sc = 2.2 - 1.2 * p
        f = self.font("Poppins-Black", 150)
        b = f.getbbox(txt)
        im = Image.new("RGBA", (b[2] + 90, b[3] + 70), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((8, 8, im.width - 8, im.height - 8), 22, fill=WHITE + (235,), outline=RED + (255,), width=14)
        d.text((45 - b[0], 35 - b[1]), txt, font=f, fill=RED + (255,))
        im = im.rotate(10, expand=True, resample=Image.BICUBIC)
        im = im.resize((int(im.width * sc), int(im.height * sc)), Image.BILINEAR)
        im.putalpha(im.getchannel("A").point(lambda v: int(v * p)))
        lay.alpha_composite(im, (int(W / 2 - im.width / 2), int(640 - im.height / 2)))
