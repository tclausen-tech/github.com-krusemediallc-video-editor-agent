"""Motor de composição: utilidades de texto, paleta, áudio e legendas (segue modelo.md)."""
import json, math, os, subprocess, numpy as np
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
A = lambda *p: os.path.join(ROOT, *p)
W, H, FPS = 1080, 1920, 30

# ---------------- PALETA — cores de jamap.com.br ----------------
NAVY, YELLOW, GRAY, TEXT = (0, 29, 82), (254, 191, 0), (221, 224, 223), (51, 51, 51)
PAL = dict(
    label_bg=NAVY, label_fg=(255, 255, 255), label_accent=YELLOW,
    cta_bg=YELLOW, cta_fg=NAVY,
    navy=NAVY, yellow=YELLOW, red=(208, 49, 45), text=TEXT,
    hl=YELLOW, hl_edge=NAVY, marker=YELLOW, caption=(255, 255, 255), stroke=NAVY,
)
F_CAP = A('fonts', 'Poppins-Black.ttf')
F_LAB = A('fonts', 'Poppins-ExtraBold.ttf')
F_BRD = A('fonts', 'Bangers.ttf')

@lru_cache(None)
def font(path, size): return ImageFont.truetype(path, size)

def ease_out(x): x = min(max(x, 0), 1); return 1 - (1 - x) ** 3
def ease_io(x): x = min(max(x, 0), 1); return x * x * (3 - 2 * x)

BOX = json.load(open(A('assets', 'boxes.json')))
@lru_cache(None)
def img(name): return Image.open(A('assets', name + '.png')).convert('RGBA')

def wrap(text, f, maxw):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if f.getlength(t) <= maxw or not cur: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines

@lru_cache(None)
def caption_img(text):
    f = font(F_CAP, 62); sw = 8
    lines = wrap(text, f, 900); lh = 80
    wmax = int(max(f.getlength(l) for l in lines)) + 2 * sw + 10
    im = Image.new('RGBA', (wmax, lh * len(lines) + 2 * sw + 14), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    for i, l in enumerate(lines):
        x = (wmax - f.getlength(l)) / 2; y = sw + i * lh - 6
        sd.text((x + 3, y + 5), l, font=f, fill=(0, 0, 0, 120), stroke_width=sw, stroke_fill=(0, 0, 0, 120))
        d.text((x, y), l, font=f, fill=PAL['caption'], stroke_width=sw, stroke_fill=PAL['stroke'])
    sh = sh.filter(ImageFilter.GaussianBlur(4)); sh.alpha_composite(im); return sh

@lru_cache(None)
def label_img(text, big=False, maxw=900, style='navy'):
    f = font(F_LAB, 62 if big else 44); pad = (30, 14) if big else (24, 10)
    bg, fg = (PAL['cta_bg'], PAL['cta_fg']) if style == 'yellow' else (PAL['label_bg'], PAL['label_fg'])
    lines = wrap(text, f, maxw); lh = int(f.size * 1.25)
    wmax = int(max(f.getlength(l) for l in lines))
    bar = 0 if style == 'yellow' else 8
    im = Image.new('RGBA', (wmax + 2 * pad[0], lh * len(lines) + 2 * pad[1] + bar), bg + (255,))
    d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        d.text(((im.width - f.getlength(l)) / 2, pad[1] + i * lh - int(f.size * .02)), l, font=f, fill=fg)
    if bar: d.rectangle((0, im.height - bar, im.width, im.height), fill=PAL['label_accent'])
    sh = Image.new('RGBA', (im.width + 30, im.height + 30), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((15, 21, 15 + im.width, 21 + im.height), fill=(0, 0, 0, 80))
    sh = sh.filter(ImageFilter.GaussianBlur(6)); sh.alpha_composite(im, (15, 15)); return sh

@lru_cache(None)
def board_text(text, size, color):
    f = font(F_BRD, size); bb = f.getbbox(text)
    im = Image.new('RGBA', (bb[2] + 10, bb[3] + 14), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((4, 4), text, font=f, fill=color + (255,)); return im

@lru_cache(None)
def prop(name):
    if name == 'warn':
        im = Image.new('RGBA', (220, 200), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.polygon([(110, 8), (212, 192), (8, 192)], fill=YELLOW, outline=NAVY, width=10)
        d.text((110, 128), '!', font=font(F_CAP, 120), fill=NAVY, anchor='mm'); return im
    if name == 'question':
        im = Image.new('RGBA', (170, 170), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.ellipse((0, 0, 168, 168), fill=YELLOW, outline=(255, 255, 255), width=8)
        d.text((84, 90), '?', font=font(F_CAP, 110), fill=NAVY, anchor='mm'); return im
    if name == 'cta_btn':
        f = font(F_LAB, 44); t = 'DÊ O PRIMEIRO PASSO'; tw = f.getlength(t) + 60
        im = Image.new('RGBA', (int(tw) + 90, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((4, 8, im.width - 4, 106), 50, fill=(0, 0, 0, 70))
        d.rounded_rectangle((0, 0, im.width - 8, 96), 48, fill=YELLOW)
        d.text(((im.width - 8) / 2 - 30, 48), t, font=f, fill=NAVY, anchor='mm')
        ax = (im.width - 8) / 2 + tw / 2 - 40; d.polygon([(ax, 30), (ax + 26, 48), (ax, 66)], fill=NAVY); return im
    raise KeyError(name)

def mouth_track(audio, words, n):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', audio, '-ac', '1', '-ar', '24000', '-f', 's16le', '-'], capture_output=True).stdout
    a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    hop = 24000 // FPS; rms = np.array([np.sqrt(np.mean(a[i * hop:(i + 1) * hop] ** 2) + 1e-9) for i in range(n)])
    speak = np.zeros(n, bool)
    for _, s, e in words: speak[int(s * FPS):int(e * FPS) + 1] = True
    ref = np.percentile(rms[speak], 90) if speak.any() else 1
    lv = np.clip(rms / ref, 0, 1.2); m = np.zeros(n, int)
    m[lv > .18] = 1; m[lv > .45] = 2; m[lv > .75] = 3; m[~speak] = 0
    for i in range(1, n - 1):
        if m[i - 1] == m[i + 1] != m[i]: m[i] = m[i - 1]
    return m, lv

def caption_chunks(words, max_words=3, max_chars=18):
    chunks, cur = [], []
    for wd in words:
        cur.append(wd)
        if wd[0][-1] in '.,?!:' or len(cur) >= max_words or len(' '.join(x[0] for x in cur)) >= max_chars:
            chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    out = []
    for i, c in enumerate(chunks):
        t0 = c[0][1]; t1 = chunks[i + 1][0][1] if i + 1 < len(chunks) else c[-1][2] + .3
        out.append((t0, min(t1, c[-1][2] + .45), ' '.join(x[0] for x in c).upper().rstrip('.,')))
    return out
