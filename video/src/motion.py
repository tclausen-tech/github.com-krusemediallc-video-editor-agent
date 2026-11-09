"""Renderizador "motion clean" — Uso: python3 motion.py [--frames 10,20 [--guides]] [--workers 4] [--out arquivo.mp4]

LAYOUT (1080x1920) — tudo o que importa fica dentro da ÁREA SEGURA:
  * grade do perfil do Instagram (recorte 4:5 central: y 285–1635; recorte 3:4: y 240–1680)
  * interface do Reels/TikTok: nada abaixo de y=1500 (legenda/usuário), nada acima de y=250, nada à direita de x=950 na metade de baixo (botões)
  -> área segura usada: x 60–940, y 300–1490.
Coluna de conteúdo (cartões, títulos): x 60–640. Personagem: fixa à direita (centro x=800, pés em y=1470, 1,65 m = 900 px).
Proporção: a personagem tem sempre o mesmo tamanho; o celular na mão está em escala real (7,5 cm); as empresas do
cartão "portes" usam uma escala única entre si; telas e cartões nunca são esticados (só escala uniforme).
"""
import sys, os, json, math, subprocess, argparse
from functools import lru_cache
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
sys.path.insert(0, os.path.dirname(__file__))
from engine import *
from timeline import SCENES

AUDIO = A('in', 'narr.mp3'); WORDS = json.load(open(A('words.json')))
DUR = 122.52; NF = int(DUR * FPS)
MOUTH, LEVEL = mouth_track(AUDIO, WORDS, NF)
BLINKS = set(); _rng = np.random.default_rng(7); _t = 1.2
while _t < DUR:
    f0 = int(_t * FPS); BLINKS.update([f0, f0 + 1, f0 + 2]); _t += _rng.uniform(2.4, 4.2)

SAFE = (60, 300, 940, 1490)
COLX, COLY, COLW = 60, 410, 580            # coluna de conteúdo
LABEL_Y = 300; CAP_Y = 1385
RED = PAL['red']; NV = PAL['navy']; YL = PAL['yellow']
F_BLACK, F_XB, F_SB = A('fonts', 'Poppins-Black.ttf'), A('fonts', 'Poppins-ExtraBold.ttf'), A('fonts', 'Poppins-SemiBold.ttf')

# ---------------- personagem ----------------
CM = json.load(open(A('assets', 'char', 'meta.json'))); PIV = CM['pivot']; ARM_LEN = CM['arm_len']; PHONE_U = CM['phone']
CH_CX, CH_FEET, CH_H = 800, 1470, 900
K = CH_H / 1000                                    # px por unidade do desenho (1000 u = 1,65 m)
CH_LEFT = CH_CX - 500 * K; CH_TOP = CH_FEET - 1020 * K
PVX, PVY = CH_LEFT + PIV[0] * K, CH_TOP + PIV[1] * K

@lru_cache(32)
def body_img(m, b, pose):
    src = Image.open(A('assets', 'char', f'body_m{m}_b{b}_{pose}.png'))
    return src.resize((int(src.width * K / 2), int(src.height * K / 2)), Image.LANCZOS)

@lru_cache(400)
def arm_img(ang):
    a = Image.open(A('assets', 'char', 'arm.png')); a = a.resize((int(a.width * K / 2), int(a.height * K / 2)), Image.LANCZOS)
    return a.rotate(ang, center=(a.width / 2, a.height / 2), resample=Image.BICUBIC)

# ---------------- fundo ----------------
@lru_cache(1)
def background():
    y = np.linspace(0, 1, H)[:, None]
    top, bot = np.array([246, 248, 252]), np.array([229, 234, 242])
    g = (top * (1 - y) + bot * y)[:, None, :].repeat(W, 1).reshape(H, W, 3)
    im = Image.fromarray(g.astype(np.uint8)).convert('RGBA'); d = ImageDraw.Draw(im)
    for x in range(30, W, 60):                         # grade de pontos sutil
        for yy in range(30, H, 60): d.ellipse((x - 2, yy - 2, x + 2, yy + 2), fill=(0, 29, 82, 14))
    return im

def blobs(t):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for cx, cy, r, col, ph in [(930, 430, 330, NV + (12,), 0), (60, 1560, 260, YL + (26,), 1.7), (1010, 1700, 180, NV + (10,), 3.1)]:
        x = cx + 22 * math.sin(t * .35 + ph); yy = cy + 16 * math.cos(t * .3 + ph)
        d.ellipse((x - r, yy - r, x + r, yy + r), fill=col)
    return lay.filter(ImageFilter.GaussianBlur(30))

BLOB_CACHE = {}
def blob_layer(f):
    key = f // 3                                         # atualiza a cada 3 quadros (movimento lento)
    if key not in BLOB_CACHE:
        if len(BLOB_CACHE) > 4: BLOB_CACHE.clear()
        BLOB_CACHE[key] = blobs(key * 3 / FPS)
    return BLOB_CACHE[key]

# ---------------- cartões ----------------
def shadowed(card, r=40):
    sh = Image.new('RGBA', (card.width + 80, card.height + 80), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((40, 54, 40 + card.width, 54 + card.height), r, fill=(0, 29, 82, 46))
    sh = sh.filter(ImageFilter.GaussianBlur(20)); sh.alpha_composite(card, (40, 40)); return sh

def white_card(w, h, r=40):
    c = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(c).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=(255, 255, 255, 255)); return c

@lru_cache(8)
def ui_card(name):
    src = img(name).convert('RGB'); a = np.asarray(src).min(axis=2) < 245
    rows = np.where(a.any(axis=1))[0]; hcrop = min(src.height, rows.max() + 56)
    src = src.crop((0, 0, src.width, hcrop)); s = COLW / src.width
    inner = src.resize((COLW, int(hcrop * s)), Image.LANCZOS).convert('RGBA')
    m = Image.new('L', inner.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, inner.width - 1, inner.height - 1), 40, fill=255)
    c = Image.new('RGBA', inner.size, (0, 0, 0, 0)); c.paste(inner, (0, 0), m)
    return shadowed(c), s

@lru_cache(8)
def panel(name):                                        # painel de zoom da tela do celular
    pw = 400; s = pw / 600; scr = img(name).resize((pw, int(1260 * s)), Image.LANCZOS)
    b = 12; im = Image.new('RGBA', (pw + 2 * b, scr.height + 2 * b), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, im.width - 1, im.height - 1), 46, fill=NV)
    m = Image.new('L', scr.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, scr.width - 1, scr.height - 1), 36, fill=255)
    im.paste(scr, (b, b), m); cx, cy = im.width - 40, 40
    d.ellipse((cx - 30, cy - 30, cx + 30, cy + 30), fill=YL, outline=(255, 255, 255), width=5)
    d.ellipse((cx - 14, cy - 16, cx + 8, cy + 6), outline=NV, width=5); d.line((cx + 5, cy + 3, cx + 16, cy + 14), fill=NV, width=6)
    return shadowed(im, 46), s, b

@lru_cache(64)
def text_img(text, path, size, color, maxw=None):
    f = font(path, size)
    if maxw:
        while f.getlength(text) > maxw and size > 30: size -= 2; f = font(path, size)
    bb = f.getbbox(text); im = Image.new('RGBA', (int(f.getlength(text)) + 8, bb[3] + 12), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((2, 0), text, font=f, fill=color); return im

@lru_cache(32)
def icon(name, size): return img(name).resize((size, size), Image.LANCZOS)

def fade(im, a):
    if a >= .999: return im
    im = im.copy(); im.putalpha(im.split()[3].point(lambda v: int(v * max(0, a)))); return im

# ---------------- geometria dos cartões gerados ----------------
def list_geom(s):
    items = [e for e in s['ev'] if e[0] == 'item']; h = 150 + len(items) * 170 + 30
    if any(e[0] == 'stamp' for e in s['ev']): h += 120
    return items, h
def item_rect(i): return (COLX + 24, COLY + 40 + 130 + i * 170 - 14, COLW - 48, 150)
def calc_rect(i): return [(COLX + 24, COLY + 110, COLW - 48, 140), (COLX + 24, COLY + 270, COLW - 48, 140), (COLX + 24, COLY + 470, COLW - 48, 170)][i]
GROUND = COLY + 690; PX_M = 22                           # cartão "portes": 22 px por metro para TODAS as empresas
BIZ = {'tower': (COLX + 330, 8, 24), 'store': (COLX + 140, 7, 6), 'kiosk': (COLX + 36, 3.6, 3.2)}   # x, largura m, altura m
def biz_rect(n): x, wm, hm = BIZ[n]; return (x, GROUND - hm * PX_M, wm * PX_M, hm * PX_M)
PHONE_PANEL = (COLX, COLY)

def target_rect(s, tgt):
    k = s['kind']
    if isinstance(tgt, tuple):
        if tgt[0] == 'item': return item_rect(tgt[1])
        if tgt[0] == 'row': return calc_rect(tgt[1])
    if k == 'portes': return biz_rect(tgt)
    if k == 'title' and tgt == 'button': return BUTTON_RECT
    if k == 'ui':
        _, sc = ui_card(s['card']); x, y, w, h = BOX[s['card']][tgt]; return COLX + x * sc, COLY + y * sc, w * sc, h * sc
    if k == 'phone':
        _, sc, b = panel(s['screen']); x, y, w, h = BOX[s['screen']][tgt]
        return PHONE_PANEL[0] + b + x * sc, PHONE_PANEL[1] + b + y * sc, w * sc, h * sc
    raise KeyError(tgt)

def scene_at(t):
    for i, s in enumerate(SCENES):
        if s['t0'] <= t < s['t1']: return i, s
    return len(SCENES) - 1, SCENES[-1]

def enter_exit(s, t, delay=0.0):
    lt = t - s['t0'] - delay; a_in = ease_out(lt / .45); a_out = 1 - ease_io((t - (s['t1'] - .2)) / .2) if s is not SCENES[-1] else 1
    return a_in * a_out, (1 - a_in) * -70 + (1 - a_out) * -40

# ---------------- braço (pré-cálculo sequencial) ----------------
def precompute_arm():
    out = np.zeros((NF, 2)); ang, ext = -8.0, 0.0; last = -1
    for f in range(NF):
        t = f / FPS; i, s = scene_at(t)
        if i != last: last = i
        tgt = None
        for e in s['ev']:
            if e[0] == 'point' and e[1] <= t < e[2]:
                x, y, w, h = target_rect(s, e[3]); tgt = (x + w + 4, y + h * .5)
        if tgt:
            want = 90 - math.degrees(math.atan2(tgt[1] - PVY, tgt[0] - PVX))
            while want > 20: want -= 360
            while want < -340: want += 360
            want = min(max(want, -215), 0); ang += (want - ang) * .3; ext += (1 - ext) * .3
        else: ang += (-8 - ang) * .2; ext += (0 - ext) * .4
        out[f] = (ang, ext)
    return out
ARM = precompute_arm()

# ---------------- legendas com palavra ativa ----------------
def chunks():
    out, cur = [], []
    for wd in WORDS:
        cur.append(wd)
        if wd[0][-1] in '.,?!:' or len(cur) >= 3 or len(' '.join(x[0] for x in cur)) >= 16: out.append(cur); cur = []
    if cur: out.append(cur)
    res = []
    for i, c in enumerate(out):
        t1 = out[i + 1][0][1] if i + 1 < len(out) else c[-1][2] + .3
        res.append((c[0][1], min(t1, c[-1][2] + .45), [(w[0].upper().rstrip('.,'), w[1]) for w in c]))
    return res
CAPS = chunks()

@lru_cache(512)
def caption(words, active):
    f = font(F_BLACK, 60); sw = 8; gap = f.getlength(' ')
    ws = [f.getlength(w) for w in words]; tw = sum(ws) + gap * (len(words) - 1)
    im = Image.new('RGBA', (int(tw) + 2 * sw + 20, 100), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh); x = sw + 10
    for i, w in enumerate(words):
        sd.text((x + 2, 16), w, font=f, fill=(0, 0, 0, 110), stroke_width=sw, stroke_fill=(0, 0, 0, 110))
        d.text((x, 10), w, font=f, fill=YL if i == active else (255, 255, 255), stroke_width=sw, stroke_fill=NV)
        x += ws[i] + gap
    sh = sh.filter(ImageFilter.GaussianBlur(4)); sh.alpha_composite(im); return sh

BUTTON_RECT = (COLX, 0, 0, 0)   # preenchido ao desenhar


class Ov:
    """Camada transparente para desenhar com alfa e compor por cima (ImageDraw em RGBA não mistura)."""
    def __init__(self, fr): self.fr = fr; self.l = Image.new('RGBA', fr.size, (0, 0, 0, 0)); self.d = ImageDraw.Draw(self.l)
    def __getattr__(self, n): return getattr(self.d, n)
    def flush(self): self.fr.alpha_composite(self.l); self.l = Image.new('RGBA', self.fr.size, (0, 0, 0, 0)); self.d = ImageDraw.Draw(self.l)

# ---------------- desenho de destaques ----------------
def draw_hl(d, r, t0, t, pad=10):
    x, y, w, h = r; k = ease_out((t - t0) / .18); e = (1 - k) * 14; a = int(255 * k)
    box = (x - pad - e, y - pad - e, x + w + pad + e, y + h + pad + e)
    d.rounded_rectangle(box, 22, outline=NV + (a,), width=12); d.rounded_rectangle(box, 22, outline=YL + (a,), width=6)

def draw_tap(d, r, t0, t):
    x, y, w, h = r; k = (t - t0) / .45
    if not 0 <= k < 1: return
    rr = 18 + 60 * ease_out(k); cx, cy = x + w / 2, y + h / 2
    d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=(255, 255, 255, int(255 * (1 - k))), width=9)
    d.ellipse((cx - rr + 6, cy - rr + 6, cx + rr - 6, cy + rr - 6), outline=NV + (int(220 * (1 - k)),), width=5)

# ---------------- conteúdo por tipo de cena ----------------
def draw_title(fr, s, t):
    """Frase grande na coluna de conteúdo. 'clear' encerra um grupo de linhas (some em 0,2 s) e o próximo recomeça no topo."""
    global BUTTON_RECT
    a_sc, dx = enter_exit(s, t)
    clears = [e[1] for e in s['ev'] if e[0] == 'clear']
    groups = [[]]
    for e in s['ev']:
        if e[0] == 'clear': groups.append([]); continue
        if e[0] in ('line', 'icon', 'button'): groups[-1].append(e)
    for gi, g in enumerate(groups):
        g_start = clears[gi - 1] if gi > 0 else -1
        g_end = clears[gi] if gi < len(clears) else 1e9
        if t < g_start: continue
        ga = 1 - ease_io((t - g_end) / .2)
        if ga <= 0: continue
        y = COLY + 20; A_ = a_sc * ga
        for e in g:
            if e[0] == 'icon':
                if t >= e[1]:
                    k = ease_out((t - e[1]) / .35); z = .6 + .4 * k + .1 * math.sin(min(1, (t - e[1]) / .5) * math.pi)
                    ic = icon(e[2], int(130 * z)); fr.alpha_composite(fade(ic, k * A_), (int(COLX + 65 - ic.width / 2 + dx), int(y + 65 - ic.height / 2)))
                y += 170
            elif e[0] == 'line':
                style = e[3]
                im = text_img(e[2].upper(), F_SB, 40, PAL['text'], COLW) if style == 'small' else text_img(e[2], F_BLACK, 84, NV, COLW - (40 if style == 'yellow' else 0))
                if t >= e[1]:
                    k = ease_out((t - e[1]) / .35); yy = y + (1 - k) * 30
                    if style == 'yellow':
                        bw = int((im.width + 40) * ease_out((t - e[1]) / .3)) + 1
                        bx = Image.new('RGBA', (bw, im.height + 6), (0, 0, 0, 0)); ImageDraw.Draw(bx).rounded_rectangle((0, 0, bw - 1, im.height + 5), 18, fill=YL)
                        fr.alpha_composite(fade(bx, A_), (int(COLX + dx), int(yy + 4)))
                        fr.alpha_composite(fade(im, k * A_), (int(COLX + 20 + dx), int(yy)))
                    else: fr.alpha_composite(fade(im, k * A_), (int(COLX + dx), int(yy)))
                y += im.height + (18 if style != 'small' else 8)
            elif e[0] == 'button':
                f = font(F_XB, 40); tw = f.getlength(e[2]); bw, bh = int(tw + 120), 96; by = y + 30
                BUTTON_RECT = (COLX, by, bw, bh)
                if t >= e[1]:
                    k = ease_out((t - e[1]) / .35)
                    bt = Image.new('RGBA', (bw + 10, bh + 14), (0, 0, 0, 0)); d = ImageDraw.Draw(bt)
                    d.rounded_rectangle((4, 10, bw + 4, bh + 10), 48, fill=(0, 29, 82, 60)); d.rounded_rectangle((0, 0, bw, bh), 48, fill=NV)
                    d.text((44, bh / 2), e[2], font=f, fill=(255, 255, 255), anchor='lm'); ax = bw - 56
                    d.polygon([(ax, bh / 2 - 16), (ax + 24, bh / 2), (ax, bh / 2 + 16)], fill=YL)
                    z = .85 + .15 * k; bt2 = bt.resize((int(bt.width * z), int(bt.height * z)))
                    fr.alpha_composite(fade(bt2, k * A_), (int(COLX + dx), int(by)))
                y = by + bh + 30

def draw_list(fr, s, t):
    items, h = list_geom(s); a_sc, dx = enter_exit(s, t)
    card = shadowed(white_card(COLW, h)); fr.alpha_composite(fade(card, a_sc), (int(COLX - 40 + dx), COLY - 40))
    d = Ov(fr)
    for e in s['ev']:
        if e[0] == 'head' and t >= e[1]:
            k = ease_out((t - e[1]) / .3); im = text_img(e[2], F_XB, 46, NV, COLW - 60)
            fr.alpha_composite(fade(im, k * a_sc), (int(COLX + 34 + dx), int(COLY + 40 + (1 - k) * 20)))
            d.rounded_rectangle((COLX + 34 + dx, COLY + 112, COLX + 34 + dx + 110 * k, COLY + 118), 3, fill=YL + (int(255 * a_sc),))
    strikes = {e[2]: e[1] for e in s['ev'] if e[0] == 'strike'}
    for i, e in enumerate(items):
        if t < e[1]: continue
        k = ease_out((t - e[1]) / .35); x, y, w, hh = item_rect(i); x += dx + (1 - k) * -40
        st = strikes.get(i); dim = 1 - .55 * ease_io((t - st) / .3) if st is not None and t >= st else 1
        ic = icon(e[2], 96); fr.alpha_composite(fade(ic, k * a_sc * (1 if dim == 1 else .7)), (int(x + 10), int(y + 14)))
        tt = text_img(e[3], F_XB, 46, NV if e[2] != 'ic_x' else (35, 35, 45), w - 140)
        fr.alpha_composite(fade(tt, k * a_sc * dim), (int(x + 130), int(y + (18 if e[4] else 38))))
        if e[4]:
            sb = text_img(e[4], F_SB, 32, (107, 114, 128), w - 140); fr.alpha_composite(fade(sb, k * a_sc * dim), (int(x + 130), int(y + 84)))
        if st is not None and t >= st:
            kk = ease_out((t - st) / .25); ly = y + (18 if e[4] else 38) + tt.height * .5
            d.line((x + 124, ly, x + 124 + (tt.width + 12) * kk, ly), fill=RED + (int(255 * a_sc),), width=9)
    for e in s['ev']:
        if e[0] == 'stamp' and t >= e[1]:
            k = ease_out((t - e[1]) / .25); f = font(F_BLACK, 76); tw = f.getlength(e[2])
            st = Image.new('RGBA', (int(tw + 80), 130), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
            sd.rounded_rectangle((0, 0, st.width - 1, 129), 30, fill=YL, outline=NV, width=8); sd.text((st.width / 2, 66), e[2], font=f, fill=NV, anchor='mm')
            z = 1.5 - .5 * k; st = st.resize((int(st.width * z), int(st.height * z))).rotate(-6, expand=True, resample=Image.BICUBIC)
            fr.alpha_composite(fade(st, min(1, k * 1.6) * a_sc), (int(COLX + COLW / 2 - st.width / 2 + dx), int(COLY + h - 100 - st.height / 2)))
    d.flush()

def brl(v): s = f'{abs(int(v)):,}'.replace(',', '.'); return ('-R$ ' if v < 0 else 'R$ ') + s

def draw_calc(fr, s, t):
    a_sc, dx = enter_exit(s, t); h = 680
    fr.alpha_composite(fade(shadowed(white_card(COLW, h)), a_sc), (int(COLX - 40 + dx), COLY - 40)); d = Ov(fr)
    rows = [e for e in s['ev'] if e[0] in ('row', 'result')]
    for e in s['ev']:
        if e[0] == 'tag' and t >= e[1]:
            k = ease_out((t - e[1]) / .3); f = font(F_XB, 30); tw = f.getlength(e[2])
            d.rounded_rectangle((COLX + 34 + dx, COLY + 36, COLX + 34 + dx + tw + 40, COLY + 86), 25, fill=YL + (int(255 * k * a_sc),))
            d.text((COLX + 54 + dx, COLY + 61), e[2], font=f, fill=NV + (int(255 * k * a_sc),), anchor='lm')
        if e[0] == 'divider' and t >= e[1]:
            k = ease_out((t - e[1]) / .35); y = COLY + 440
            d.line((COLX + 34 + dx, y, COLX + 34 + dx + (COLW - 68) * k, y), fill=NV + (int(255 * a_sc),), width=5)
    for i, e in enumerate(rows):
        if t < e[1]: continue
        k = ease_out((t - e[1]) / .35); cnt = ease_out((t - e[1]) / .9); x, y, w, hh = calc_rect(i); x += dx
        col = RED if e[4] == 'red' else NV
        lab = text_img(e[2], F_SB, 32, (107, 114, 128)); fr.alpha_composite(fade(lab, k * a_sc), (int(x + 10), int(y + 4)))
        val = text_img(brl(e[3] * cnt), F_BLACK, 84 if e[0] == 'result' else 64, col)
        fr.alpha_composite(fade(val, k * a_sc), (int(x + 10), int(y + 48 + (1 - k) * 16)))
        if e[0] == 'result' and cnt > .95:
            kk = ease_out((t - e[1] - .9) / .3); f = font(F_XB, 30); tx = x + 10; ty = y + 48 + val.height + 6
            d.rounded_rectangle((tx, ty, tx + 190, ty + 50), 25, fill=RED + (int(255 * kk * a_sc),))
            d.text((tx + 95, ty + 25), 'PREJUÍZO', font=f, fill=(255, 255, 255, int(255 * kk * a_sc)), anchor='mm')
    d.flush()

def draw_biz(d, n, k, dx, a):
    x, y, w, h = biz_rect(n); x += dx; yy = GROUND - h * k        # cresce a partir do chão
    al = int(255 * a)
    if n == 'tower':
        d.rectangle((x, yy, x + w, GROUND), fill=(61, 90, 133, al))
        for r in range(int(h * k / 22)):
            for c in range(4):
                wy = GROUND - 26 - r * 22
                if wy > yy + 8: d.rectangle((x + 14 + c * 40, wy, x + 36 + c * 40, wy + 12), fill=(191, 221, 245, al))
    elif n == 'store':
        d.rectangle((x, yy, x + w, GROUND), fill=(242, 231, 213, al)); d.rectangle((x, yy, x + w, yy + 24 * k), fill=YL + (al,))
        if k > .6: d.rectangle((x + 16, GROUND - 70, x + 76, GROUND - 26), fill=(191, 221, 245, al)); d.rectangle((x + 96, GROUND - 64, x + 136, GROUND), fill=(122, 90, 58, al))
    else:
        d.rectangle((x, yy, x + w, GROUND), fill=(255, 248, 230, al))
        for i in range(4): d.rectangle((x - 2 + i * 21, yy - 6, x + 19 + i * 21, yy + 12), fill=(NV if i % 2 == 0 else (255, 255, 255)) + (al,))
        if k > .6: d.rectangle((x + 46, GROUND - 40, x + 70, GROUND), fill=(138, 106, 58, al))

def draw_portes(fr, s, t):
    a_sc, dx = enter_exit(s, t); h = 840
    fr.alpha_composite(fade(shadowed(white_card(COLW, h)), a_sc), (int(COLX - 40 + dx), COLY - 40)); d = Ov(fr)
    badge = [e for e in s['ev'] if e[0] == 'badge' and t >= e[1]]
    if badge:
        e = badge[0]; k = ease_out((t - e[1]) / .35)
        fr.alpha_composite(fade(icon(e[2], 90), k * a_sc), (int(COLX + 34 + dx), COLY + 34))
        for j, ln in enumerate(['Benefícios previstos', 'em lei para pequenos']):
            fr.alpha_composite(fade(text_img(ln, F_XB, 38, NV), k * a_sc), (int(COLX + 140 + dx), COLY + 36 + j * 48))
    else:
        fr.alpha_composite(fade(text_img('Todos os portes', F_XB, 46, NV), a_sc), (int(COLX + 34 + dx), COLY + 40))
        fr.alpha_composite(fade(text_img('mesma escala: 1 m = 22 px', F_SB, 28, (107, 114, 128)), a_sc), (int(COLX + 34 + dx), COLY + 104))
    d.rectangle((COLX + 20 + dx, GROUND, COLX + COLW - 20 + dx, GROUND + 6), fill=(160, 168, 178, int(255 * a_sc)))
    for e in s['ev']:
        if e[0] == 'biz' and t >= e[1]:
            k = ease_out((t - e[1]) / .45); draw_biz(d, e[2], k, dx, a_sc)
            x, y, w, hh = biz_rect(e[2]); lab = {'tower': 'GRANDE', 'store': 'MÉDIA', 'kiosk': 'PEQUENA'}[e[2]]
            f = font(F_XB, 24); tw = f.getlength(lab); cx = x + w / 2 + dx
            d.rounded_rectangle((cx - tw / 2 - 14, GROUND + 20, cx + tw / 2 + 14, GROUND + 58), 19, fill=NV + (int(255 * k * a_sc),))
            d.text((cx, GROUND + 39), lab, font=f, fill=(255, 255, 255, int(255 * k * a_sc)), anchor='mm')
    d.flush()

# ---------------- quadro ----------------
def render_frame(f, guides=False):
    t = f / FPS; i, s = scene_at(t); kind = s['kind']; lt = t - s['t0']
    fr = background().copy(); fr.alpha_composite(blob_layer(f))
    d = Ov(fr)
    # sombra no chão
    d.ellipse((CH_CX - 170, CH_FEET - 22, CH_CX + 170, CH_FEET + 22), fill=(0, 29, 82, 30)); d.flush()
    # conteúdo
    if kind == 'ui':
        card, sc = ui_card(s['card']); a, dx = enter_exit(s, t)
        fr.alpha_composite(fade(card, a), (int(COLX - 40 + dx), COLY - 40))
    elif kind == 'list': draw_list(fr, s, t)
    elif kind == 'calc': draw_calc(fr, s, t)
    elif kind == 'portes': draw_portes(fr, s, t)
    elif kind == 'title': draw_title(fr, s, t)
    d = Ov(fr)
    for e in s['ev']:
        if e[0] == 'mark' and e[1] <= t < e[2]:
            x, y, w, h = target_rect(s, e[3]); k = ease_out((t - e[1]) / .3)
            d.rounded_rectangle((x - 6, y - 4, x - 6 + (w + 12) * k, y + h + 4), 8, fill=YL + (90,))
        if e[0] == 'hl' and e[1] <= t < e[2] and kind != 'phone': draw_hl(d, target_rect(s, e[3]), e[1], t)
        if e[0] == 'tap' and kind != 'phone' and e[1] <= t < e[1] + .45: draw_tap(d, target_rect(s, e[2]), e[1], t)
    d.flush()
    # personagem
    bob = math.sin(t * 2 * math.pi * .45) * 3; hop = 0.0
    for e in s['ev']:
        if e[0] in ('label', 'item', 'line') and 0 <= t - e[1] < .3: hop = max(hop, math.sin((t - e[1]) / .3 * math.pi) * 8)
    dy = bob - hop; m = MOUTH[min(f, NF - 1)]; b = 1 if f in BLINKS else 0; pose = 'phone' if kind == 'phone' else 'down'
    ang, ext = ARM[f]; pvy = PVY + dy
    dirx, diry = math.sin(math.radians(ang)), math.cos(math.radians(ang))
    hx, hy = PVX + dirx * (ARM_LEN - 10) * K, pvy + diry * (ARM_LEN - 10) * K
    tgt = None
    for e in s['ev']:
        if e[0] == 'point' and e[1] <= t < e[2]: x, y, w, h = target_rect(s, e[3]); tgt = (x + w + 4, y + h * .5)
    if kind == 'phone':      # faixa de zoom: atrás da personagem
        pim, sc, bdr = panel(s['screen']); kk = ease_out(lt / .4) * (1 - ease_io((t - (s['t1'] - .2)) / .2))
        px, py, pw, ph = (CH_LEFT + PHONE_U[0] * K, CH_TOP + PHONE_U[1] * K + dy, PHONE_U[2] * K, PHONE_U[3] * K)
        ax = PHONE_PANEL[0] + pim.width - 80; ay = PHONE_PANEL[1]
        poly = [(ax, ay + 60), (ax, ay + pim.height - 140), (px, py + ph), (px, py)]
        d.polygon(poly, fill=YL + (int(60 * kk),))
    if ext > .02 and tgt is not None:
        dist = max(0, math.hypot(tgt[0] - hx, tgt[1] - hy) - 4) * ext; ex, ey = hx + dirx * dist, hy + diry * dist
        d.line((hx, hy, ex, ey), fill=(255, 255, 255, 255), width=12); d.line((hx, hy, ex, ey), fill=NV + (255,), width=6)
        d.ellipse((ex - 11, ey - 11, ex + 11, ey + 11), fill=YL, outline=NV, width=4)
    d.flush()
    ai = arm_img(int(round(ang))); fr.alpha_composite(ai, (int(PVX - ai.width / 2), int(pvy - ai.height / 2)))
    fr.alpha_composite(body_img(m, b, pose), (int(CH_LEFT), int(CH_TOP + dy)))
    d = Ov(fr)
    if kind == 'phone':
        d.rounded_rectangle((px - 5, py - 5, px + pw + 5, py + ph + 5), 8, outline=YL + (int(255 * kk),), width=4); d.flush()
        fr.alpha_composite(fade(pim, kk), (int(PHONE_PANEL[0] - 40 + (1 - kk) * -50), PHONE_PANEL[1] - 40))
        d = Ov(fr)
        for e in s['ev']:
            if e[0] == 'hl' and e[1] <= t < e[2]: draw_hl(d, target_rect(s, e[3]), e[1], t, pad=6)
            if e[0] == 'tap' and e[1] <= t < e[1] + .45: draw_tap(d, target_rect(s, e[2]), e[1], t)
        if ext > .02 and tgt is not None:     # vareta por cima do painel
            d.line((hx, hy, ex, ey), fill=(255, 255, 255, 255), width=12); d.line((hx, hy, ex, ey), fill=NV + (255,), width=6)
            d.ellipse((ex - 11, ey - 11, ex + 11, ey + 11), fill=YL, outline=NV, width=4)
        d.flush()
    # etiqueta (entra subindo + fade)
    for e in s['ev']:
        if e[0] == 'label' and e[1] <= t < e[2]:
            im = label_img(e[3]); k = ease_out((t - e[1]) / .25)
            a = min(k, (e[2] - t) / .15 if e[2] < s['t1'] - .05 else 1)
            fr.alpha_composite(fade(im, a), (int((W - im.width) / 2), int(LABEL_Y - 15 + (1 - k) * 24)))
    # legenda com palavra ativa
    for (t0, t1, ws) in CAPS:
        if t0 <= t < t1:
            act = max(j for j, w in enumerate(ws) if w[1] <= t + .02)
            im = caption(tuple(w[0] for w in ws), act); fr.alpha_composite(im, (int((W - im.width) / 2), int(CAP_Y - im.height / 2))); break
    if guides:
        g = Ov(fr)
        g.rectangle((0, 285, W - 1, 1635), outline=(255, 0, 0, 200), width=4)      # grade 4:5
        g.rectangle(SAFE, outline=(0, 160, 0, 220), width=4)                        # área segura
        g.rectangle((950, 960, W, 1700), fill=(255, 0, 0, 40)); g.rectangle((0, 1500, W, H), fill=(255, 0, 0, 40)); g.rectangle((0, 0, W, 250), fill=(255, 0, 0, 40)); g.flush()
    return fr.convert('RGB')

def worker(args):
    a, b, path = args
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
    for f in range(a, b): p.stdin.write(render_frame(f).tobytes())
    p.stdin.close(); p.wait(); return path

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--frames'); ap.add_argument('--guides', action='store_true')
    ap.add_argument('--workers', type=int, default=4); ap.add_argument('--out', default=A('out', 'video.mp4'))
    a = ap.parse_args(); os.makedirs(A('out'), exist_ok=True)
    if a.frames:
        for t in a.frames.split(','): render_frame(int(float(t) * FPS), a.guides).save(A('out', f'f_{float(t):06.2f}.png'))
        sys.exit()
    n = a.workers; step = math.ceil(NF / n)
    parts = [(k * step, min(NF, (k + 1) * step), A('out', f'part{k}.mp4')) for k in range(n)]
    with Pool(n) as pool: paths = pool.map(worker, parts)
    with open(A('out', 'parts.txt'), 'w') as fh: fh.writelines(f"file '{p}'\n" for p in paths)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', A('out', 'parts.txt'), '-i', AUDIO,
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', a.out], check=True)
    print('ok', a.out)
