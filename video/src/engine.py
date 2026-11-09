"""Motor de composição: cenas -> frames 1080x1920 @30fps (segue modelo.md)."""
import json, math, os, subprocess, numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
A = lambda *p: os.path.join(ROOT, *p)
W, H, FPS = 1080, 1920, 30

# ---------------- PALETA (trocar aqui quando a paleta oficial chegar) ----------------
PAL = dict(
    label_bg=(30, 102, 48), label_fg=(255, 255, 255),
    green=(45, 179, 74), red=(208, 40, 48), blue=(32, 88, 200), black=(17, 17, 17),
    hl=(214, 40, 52), marker=(255, 232, 77), caption=(255, 255, 255), stroke=(0, 0, 0),
)
F_CAP = A('fonts', 'Montserrat-Black.ttf')
F_LAB = A('fonts', 'Montserrat-ExtraBold.ttf')
F_BRD = A('fonts', 'Bangers.ttf')

@lru_cache(None)
def font(path, size): return ImageFont.truetype(path, size)

def ease_out(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def ease_io(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)

# ---------------- assets ----------------
BOX = json.load(open(A('assets', 'boxes.json')))
@lru_cache(None)
def img(name): return Image.open(A('assets', name + '.png')).convert('RGBA')

# ---------------- personagem ----------------
CH_SIZE = 660
@lru_cache(None)
def char(b, m):
    return Image.open(A(f'char_b{b}_m{m}.png')).resize((CH_SIZE, CH_SIZE), Image.LANCZOS)

# ---------------- texto ----------------
def wrap(text, f, maxw):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if f.getlength(t) <= maxw or not cur: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines

@lru_cache(None)
def caption_img(text):
    f = font(F_CAP, 64); sw = 8
    lines = wrap(text, f, 900)
    lh = 76; wmax = int(max(f.getlength(l) for l in lines)) + 2 * sw + 10
    im = Image.new('RGBA', (wmax, lh * len(lines) + 2 * sw + 10), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    for i, l in enumerate(lines):
        x = (wmax - f.getlength(l)) / 2; y = sw + i * lh
        sd.text((x + 3, y + 5), l, font=f, fill=(0, 0, 0, 140), stroke_width=sw, stroke_fill=(0, 0, 0, 140))
        d.text((x, y), l, font=f, fill=PAL['caption'], stroke_width=sw, stroke_fill=PAL['stroke'])
    sh = sh.filter(ImageFilter.GaussianBlur(4)); sh.alpha_composite(im); return sh

@lru_cache(None)
def label_img(text, big=False, maxw=900):
    f = font(F_LAB, 64 if big else 46); pad = (30, 16) if big else (24, 12)
    lines = wrap(text, f, maxw); lh = int(f.size * 1.18)
    wmax = int(max(f.getlength(l) for l in lines))
    im = Image.new('RGBA', (wmax + 2 * pad[0], lh * len(lines) + 2 * pad[1] - int(f.size * .12)), PAL['label_bg'] + (255,))
    d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        d.text(((im.width - f.getlength(l)) / 2, pad[1] + i * lh - int(f.size * .06)), l, font=f, fill=PAL['label_fg'])
    sh = Image.new('RGBA', (im.width + 30, im.height + 30), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((15, 21, 15 + im.width, 21 + im.height), fill=(0, 0, 0, 90))
    sh = sh.filter(ImageFilter.GaussianBlur(6)); sh.alpha_composite(im, (15, 15)); return sh

@lru_cache(None)
def board_text(text, size, color):
    f = font(F_BRD, size); bb = f.getbbox(text)
    im = Image.new('RGBA', (bb[2] + 10, bb[3] + 14), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((4, 4), text, font=f, fill=color + (255,)); return im

# ---------------- props desenhados ----------------
@lru_cache(None)
def prop(name):
    if name == 'warn':
        im = Image.new('RGBA', (260, 240), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, 1, 1), 1)
        d.polygon([(130, 8), (252, 228), (8, 228)], fill=(255, 196, 0), outline=(30, 30, 30), width=10)
        f = font(F_CAP, 150); d.text((130, 150), '!', font=f, fill=(30, 30, 30), anchor='mm'); return im
    if name == 'question':
        im = Image.new('RGBA', (200, 220), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.ellipse((0, 0, 200, 200), fill=PAL['label_bg'] + (255,), outline=(255, 255, 255), width=8)
        d.text((100, 104), '?', font=font(F_CAP, 140), fill=(255, 255, 255), anchor='mm'); return im
    if name in ('shop_s', 'shop_m', 'shop_l'):
        if name == 'shop_l':
            im = Image.new('RGBA', (220, 380), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            d.rectangle((10, 10, 210, 380), fill=(70, 110, 160), outline=(40, 60, 90), width=6)
            for r in range(7):
                for c in range(3): d.rectangle((30 + c * 60, 30 + r * 46, 70 + c * 60, 60 + r * 46), fill=(180, 220, 250))
            d.rectangle((85, 330, 135, 380), fill=(40, 60, 90)); tag = 'GRANDE'
        elif name == 'shop_m':
            im = Image.new('RGBA', (220, 280), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            d.rectangle((10, 60, 210, 280), fill=(245, 236, 220), outline=(120, 90, 60), width=6)
            for i in range(5): d.rectangle((10 + i * 40, 40, 50 + i * 40, 90), fill=(32, 88, 200) if i % 2 == 0 else (255, 255, 255))
            d.rectangle((30, 120, 110, 200), fill=(180, 220, 250), outline=(120, 90, 60), width=4)
            d.rectangle((135, 150, 190, 280), fill=(120, 90, 60)); tag = 'MÉDIA'
        else:
            im = Image.new('RGBA', (190, 230), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            d.rectangle((10, 70, 180, 230), fill=(255, 248, 230), outline=(150, 70, 50), width=6)
            for i in range(5): d.rectangle((5 + i * 36, 40, 41 + i * 36, 95), fill=(208, 40, 48) if i % 2 == 0 else (255, 255, 255))
            d.rectangle((40, 130, 150, 230), fill=(180, 220, 250), outline=(150, 70, 50), width=4); tag = 'PEQUENA'
        f = font(F_LAB, 26); tw = f.getlength(tag)
        out = Image.new('RGBA', (im.width, im.height + 50), (0, 0, 0, 0)); out.alpha_composite(im)
        d = ImageDraw.Draw(out); d.rounded_rectangle(((im.width - tw) / 2 - 12, im.height + 6, (im.width + tw) / 2 + 12, im.height + 46), 8, fill=PAL['label_bg'])
        d.text((im.width / 2, im.height + 26), tag, font=f, fill=(255, 255, 255), anchor='mm'); return out
    if name == 'cta_btn':
        f = font(F_LAB, 44); t = 'DÊ O PRIMEIRO PASSO'; tw = f.getlength(t) + 60
        im = Image.new('RGBA', (int(tw) + 90, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((4, 8, im.width - 4, 106), 50, fill=(0, 0, 0, 70))
        d.rounded_rectangle((0, 0, im.width - 8, 96), 48, fill=(255, 255, 255), outline=PAL['label_bg'], width=6)
        d.text(((im.width - 8) / 2 - 30, 48), t, font=f, fill=PAL['label_bg'], anchor='mm'); ax = (im.width - 8) / 2 + tw / 2 - 40
        d.polygon([(ax, 30), (ax + 26, 48), (ax, 66)], fill=PAL['label_bg']); return im
    raise KeyError(name)

# ---------------- áudio -> boca ----------------
def mouth_track(audio, words, n):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', audio, '-ac', '1', '-ar', '24000', '-f', 's16le', '-'], capture_output=True).stdout
    a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    hop = 24000 // FPS; rms = np.array([np.sqrt(np.mean(a[i * hop:(i + 1) * hop] ** 2) + 1e-9) for i in range(n)])
    speak = np.zeros(n, bool)
    for _, s, e in words: speak[int(s * FPS):int(e * FPS) + 1] = True
    ref = np.percentile(rms[speak], 90) if speak.any() else 1
    lv = np.clip(rms / ref, 0, 1.2); m = np.zeros(n, int)
    m[lv > .18] = 1; m[lv > .45] = 2; m[lv > .75] = 3; m[~speak] = 0
    # suaviza: evita alternância frame a frame
    for i in range(1, n - 1):
        if m[i - 1] == m[i + 1] != m[i]: m[i] = m[i - 1]
    return m, lv

# ---------------- legendas ----------------
def caption_chunks(words, max_words=3, max_chars=18):
    chunks, cur = [], []
    for wd in words:
        cur.append(wd)
        txt = ' '.join(x[0] for x in cur)
        if wd[0][-1] in '.,?!:' or len(cur) >= max_words or len(txt) >= max_chars:
            chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        t0 = c[0][1]; t1 = chunks[i + 1][0][1] if i + 1 < len(chunks) else c[-1][2] + .3
        t1 = min(t1, c[-1][2] + .45)
        txt = ' '.join(x[0] for x in c).upper().rstrip('.,')
        out.append((t0, t1, txt))
    return out
