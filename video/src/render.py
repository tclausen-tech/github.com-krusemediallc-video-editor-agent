"""Renderiza o vídeo. Uso: python3 render.py [--frames 10,200,...] [--workers 4] [--out arquivo.mp4]"""
import sys, os, json, math, subprocess, argparse
from functools import lru_cache
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from engine import *
from timeline import SCENES

AUDIO = A('in', 'narr.mp3')
WORDS = json.load(open(A('words.json')))
DUR = 122.52
NF = int(DUR * FPS)
COL = dict(red=PAL['red'], blue=PAL['blue'], green=PAL['green'], black=PAL['black'])
CAPS = caption_chunks(WORDS)
MOUTH, LEVEL = mouth_track(AUDIO, WORDS, NF)
BLINKS = set()
_rng = np.random.default_rng(7); _t = 1.2
while _t < DUR:
    f0 = int(_t * FPS); BLINKS.update([f0, f0 + 1, f0 + 2]); _t += _rng.uniform(2.4, 4.2)

def scene_at(t):
    for i, s in enumerate(SCENES):
        if s['t0'] <= t < s['t1']: return i, s
    return len(SCENES) - 1, SCENES[-1]

# ---------- geometria de telas ----------
SCR = (36, 316, 1008, 680)                     # área da tela do monitor no mundo (bg_desk)
PH_W = 470; PH_S = PH_W / 600; PH_H = int(1260 * PH_S); PH_X, PH_Y = 70, 430

def phone_xy(s, t):
    k = ease_out((t - s['t0']) / .35)
    return PH_X + (1 - k) * -600, PH_Y + (1 - k) * 40

def target_rect(s, tgt, t):
    """retângulo-alvo no espaço do MUNDO"""
    if isinstance(tgt, tuple) and tgt[0] == 'rect': return tgt[1:]
    x, y, w, h = BOX[s['screen']][tgt]
    if s['kind'] == 'desk':
        k = SCR[2] / 1512; return SCR[0] + x * k, SCR[1] + y * k, w * k, h * k
    px, py = phone_xy(s, t)
    return px + x * PH_S, py + y * PH_S, w * PH_S, h * PH_S

@lru_cache(8)
def phone_img(name):
    scr = img(name).resize((PH_W, PH_H), Image.LANCZOS)
    b = 16; im = Image.new('RGBA', (PH_W + 2 * b, PH_H + 2 * b), (0, 0, 0, 0))
    sh = Image.new('RGBA', (im.width + 60, im.height + 60), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((30, 46, 30 + im.width, 46 + im.height), 70, fill=(0, 0, 0, 90))
    from PIL import ImageFilter
    sh = sh.filter(ImageFilter.GaussianBlur(16))
    d = ImageDraw.Draw(im); d.rounded_rectangle((0, 0, im.width - 1, im.height - 1), 66, fill=(20, 20, 22))
    m = Image.new('L', scr.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, PH_W - 1, PH_H - 1), 52, fill=255)
    im.paste(scr, (b, b), m)
    d.rounded_rectangle((im.width / 2 - 70, b + 10, im.width / 2 + 70, b + 44), 17, fill=(10, 10, 10))
    sh.alpha_composite(im, (30, 30)); return sh

@lru_cache(4)
def base_world(i):
    s = SCENES[i]; k = s['kind']
    bg = img({'room': 'bg_room', 'desk': 'bg_desk', 'board': 'bg_board', 'phone': 'bg_sala', 'building': 'bg_building'}[k]).copy()
    if k == 'desk':
        bg.paste(img(s['screen']).resize(SCR[2:], Image.LANCZOS), SCR[:2])
    return bg

# ---------- câmera (pré-calculada, sequencial) ----------
def compute_camera():
    cam = np.zeros((NF, 3)); state = None; last = -1
    for f in range(NF):
        t = f / FPS; i, s = scene_at(t)
        if i != last: state = None; last = i
        k = s['kind']; lt = t - s['t0']
        if k == 'desk':
            push = ease_out(lt / .8)
            sc = 1.0 + .07 * push; cx, cy = 540, 960 + (842 - 960) * push
            foc = [e for e in s['ev'] if e[0] == 'hl' and e[1] <= t < e[2]]
            if foc and lt > .8:
                x, y, w, h = target_rect(s, foc[-1][3], t); tx, ty, ts = x + w / 2, y + h / 2, s.get('zoom', 1.13)
            else: tx, ty, ts = 540, 842, 1.07
            if state is None or lt <= .8: state = [cx, cy, sc]
            else:
                a = .07; state = [state[0] + (tx - state[0]) * a, state[1] + (ty - state[1]) * a, state[2] + (ts - state[2]) * a]
            sc = state[2]; half_w, half_h = W / 2 / sc, H / 2 / sc
            cx = min(max(state[0], half_w), W - half_w); cy = min(max(state[1], half_h), H - half_h)
            cam[f] = (cx, cy, sc)
        elif k in ('room', 'building'):
            sc = 1.0 + .05 * ease_io(lt / (s['t1'] - s['t0'])); cam[f] = (540, 960, sc)
        else:
            cam[f] = (540, 960, 1.0)
    return cam
CAM = compute_camera()

def w2f(p, c):
    cx, cy, sc = c; return ((p[0] - cx) * sc + W / 2, (p[1] - cy) * sc + H / 2)

# ---------- desenho ----------
def draw_hl(d, r, t0, t, color=None, width=7, pad=10):
    x, y, w, h = r; k = ease_out((t - t0) / .15); e = (1 - k) * 18
    d.rounded_rectangle((x - pad - e, y - pad - e, x + w + pad + e, y + h + pad + e), 12, outline=(color or PAL['hl']) + (int(255 * k),), width=width)

def board_pen(s, t):
    for e in s['ev']:
        if e[0] == 'write' and e[1] <= t < e[1] + e[2] + .15:
            _, t0, dur, txt, x, y, size, col = e
            im = board_text(txt, size, COL[col]); k = min(1, (t - t0) / dur)
            return (x + im.width * k, y + im.height * .75)
        if e[0] == 'strike' and e[1] <= t < e[1] + e[2] + .1:
            _, t0, dur, x0, y, x1, col = e; k = min(1, (t - t0) / dur); return (x0 + (x1 - x0) * k, y)
    return None

def render_frame(f):
    t = f / FPS; i, s = scene_at(t); kind = s['kind']; c = CAM[f]
    world = base_world(i).copy(); d = ImageDraw.Draw(world, 'RGBA')
    pointers = []
    if kind == 'phone':
        px, py = phone_xy(s, t); ph = phone_img(s['screen']); world.alpha_composite(ph, (int(px) - 30, int(py) - 30))
    for e in s['ev']:
        typ = e[0]
        if typ == 'hl' and e[1] <= t < e[2]: draw_hl(d, target_rect(s, e[3], t), e[1], t)
        elif typ == 'mark' and e[1] <= t < e[2]:
            x, y, w, h = target_rect(s, e[3], t); k = ease_out((t - e[1]) / .3)
            lay = Image.new('RGBA', world.size, (0, 0, 0, 0))
            ImageDraw.Draw(lay).rectangle((x - 6, y - 4, x - 6 + (w + 12) * k, y + h + 4), fill=PAL['marker'] + (110,))
            world.alpha_composite(lay)
        elif typ == 'tap' and e[1] <= t < e[1] + .45:
            x, y, w, h = target_rect(s, e[2], t); k = (t - e[1]) / .45; r = 20 + 70 * ease_out(k)
            d.ellipse((x + w / 2 - r, y + h / 2 - r, x + w / 2 + r, y + h / 2 + r), outline=(255, 255, 255, int(255 * (1 - k))), width=10)
            d.ellipse((x + w / 2 - r + 6, y + h / 2 - r + 6, x + w / 2 + r - 6, y + h / 2 + r - 6), outline=PAL['blue'] + (int(230 * (1 - k)),), width=6)
        elif typ == 'point' and e[1] <= t < e[2]:
            x, y, w, h = target_rect(s, e[3], t)
            k = ease_out((t - e[1]) / .2) * (1 - ease_out((t - (e[2] - .15)) / .15))
            pointers.append(((x + w * .5, y + h * .5), k))
        elif typ == 'write' and t >= e[1]:
            _, t0, dur, txt, x, y, size, col = e; im = board_text(txt, size, COL[col])
            k = min(1, (t - t0) / dur); cw = int(im.width * k)
            if cw > 0: world.alpha_composite(im.crop((0, 0, cw, im.height)), (int(x), int(y)))
        elif typ == 'strike' and t >= e[1]:
            _, t0, dur, x0, y, x1, col = e; k = min(1, (t - t0) / dur)
            d.line((x0, y, x0 + (x1 - x0) * k, y + 4 * k), fill=COL[col] + (255,), width=12)
        elif typ == 'stamp' and t >= e[1]:
            _, t0, txt, cx, cy, size, col = e; k = ease_out((t - t0) / .22)
            im = board_text(txt, size, COL[col]); fr = Image.new('RGBA', (im.width + 60, im.height + 30), (0, 0, 0, 0))
            ImageDraw.Draw(fr).rounded_rectangle((4, 4, fr.width - 4, fr.height - 4), 18, outline=COL[col] + (255,), width=12)
            fr.alpha_composite(im, (30, 12)); sc = 1.8 - .8 * k
            fr = fr.resize((int(fr.width * sc), int(fr.height * sc))).rotate(8, expand=True, resample=Image.BICUBIC)
            fr.putalpha(fr.split()[3].point(lambda v: int(v * min(1, k * 1.5))))
            world.alpha_composite(fr, (int(cx - fr.width / 2), int(cy - fr.height / 2)))
        elif typ == 'prop' and e[1] <= t < e[2] and e[6] != 'popc':
            _, t0, t1, name, x, y, anim = e; im = prop(name); k = ease_out((t - t0) / .3)
            if anim == 'pop':
                sc = .3 + .7 * k + .12 * math.sin(min(1, (t - t0) / .45) * math.pi)
                im2 = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))))
                world.alpha_composite(im2, (int(x + (im.width - im2.width) / 2), int(y + (im.height - im2.height) / 2)))
            elif anim == 'up':
                world.alpha_composite(im, (int(x), int(y + (1 - k) * 500)))
    if kind == 'board':
        pen = board_pen(s, t)
        if pen: pointers.append((pen, 1.0))
    # câmera
    cx, cy, sc = c
    if abs(sc - 1) < 1e-3 and cx == 540 and cy == 960: frame = world
    else:
        frame = world.transform((W, H), Image.AFFINE, (1 / sc, 0, cx - W / 2 / sc, 0, 1 / sc, cy - H / 2 / sc), resample=Image.BILINEAR)
    fd = ImageDraw.Draw(frame, 'RGBA')
    # personagem
    lt = t - s['t0']
    chx = {'R': 470, 'C': 230, 'L': -40}[s['side']]
    bob = math.sin(t * 2 * math.pi * .45) * 6
    pop = 0.0
    for e in s['ev']:
        if e[0] == 'label' and 0 <= t - e[1] < .3: pop = max(pop, math.sin((t - e[1]) / .3 * math.pi) * .035)
    enter = ease_out(lt / .25) if s['t0'] > 0 else 1
    m = MOUTH[min(f, NF - 1)]; b = 1 if f in BLINKS else 0
    ch = char(b, m)
    sc_ch = 1 + pop + .012 * LEVEL[min(f, NF - 1)] * (m > 0)
    if abs(sc_ch - 1) > 1e-3: ch = ch.resize((int(CH_SIZE * sc_ch), int(CH_SIZE * sc_ch)), Image.BILINEAR)
    chy = H - ch.height + 40 + bob + (1 - enter) * 40
    # vareta (atrás do personagem)
    for (p, k) in pointers:
        if k <= 0.01: continue
        fx, fy = w2f(p, c) if kind != 'room' else p
        ox, oy = chx + CH_SIZE * .22, H - 120
        ex, ey = ox + (fx - ox) * k, oy + (fy - oy) * k
        fd.line((ox, oy, ex, ey), fill=(255, 255, 255, 255), width=16)
        fd.line((ox, oy, ex, ey), fill=(20, 20, 20, 255), width=8)
        fd.ellipse((ex - 15, ey - 15, ex + 15, ey + 15), fill=(255, 255, 255), outline=(20, 20, 20), width=6)
    frame.alpha_composite(ch, (int(chx - (ch.width - CH_SIZE) / 2), int(chy)))
    # props de tela (CTA)
    for e in s['ev']:
        if e[0] == 'prop' and e[6] == 'popc' and e[1] <= t < e[2]:
            im = prop(e[3]); k = ease_out((t - e[1]) / .3); sc2 = .4 + .6 * k + .08 * math.sin(min(1, (t - e[1]) / .5) * math.pi)
            im2 = im.resize((int(im.width * sc2), int(im.height * sc2))); frame.alpha_composite(im2, (int(e[4] - im2.width / 2), int(e[5] - im2.height / 2 + 30)))
        if e[0] == 'tap' and kind == 'room' and e[1] <= t < e[1] + .45:
            x, y, w, h = e[2][1:]; k = (t - e[1]) / .45; r = 20 + 70 * ease_out(k)
            fd.ellipse((x + w / 2 - r, y + h / 2 - r, x + w / 2 + r, y + h / 2 + r), outline=PAL['label_bg'] + (int(255 * (1 - k)),), width=10)
    # etiquetas (fade 0,15 s)
    stack = []
    for e in s['ev']:
        if e[0] == 'label' and e[1] <= t < e[2]:
            opt = e[4] if len(e) > 4 else {}
            im = label_img(e[3], opt.get('big', False), opt.get('maxw', 900))
            a = min(1, (t - e[1]) / .15, (e[2] - t) / .15 if e[2] < s['t1'] - .05 else 1)
            y = opt.get('y', 175)
            if a < 1: im = im.copy(); im.putalpha(im.split()[3].point(lambda v: int(v * a)))
            frame.alpha_composite(im, (int((W - im.width) / 2), int(y)))
    # legenda
    for (t0, t1, txt) in CAPS:
        if t0 <= t < t1:
            im = caption_img(txt); frame.alpha_composite(im, (int((W - im.width) / 2), int(1238 - im.height / 2)))
            break
    return frame.convert('RGB')

def worker(args):
    a, b, path = args
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
    for f in range(a, b): p.stdin.write(render_frame(f).tobytes())
    p.stdin.close(); p.wait(); return path

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--frames'); ap.add_argument('--workers', type=int, default=4); ap.add_argument('--out', default=A('out', 'video.mp4'))
    ap.add_argument('--range')
    a = ap.parse_args(); os.makedirs(A('out'), exist_ok=True)
    if a.frames:
        for t in a.frames.split(','):
            f = int(float(t) * FPS); render_frame(f).save(A('out', f'f_{float(t):06.2f}.png'))
        sys.exit()
    r0, r1 = (0, NF) if not a.range else [int(float(x) * FPS) for x in a.range.split(':')]
    n = a.workers; step = math.ceil((r1 - r0) / n)
    parts = [(r0 + k * step, min(r1, r0 + (k + 1) * step), A('out', f'part{k}.mp4')) for k in range(n)]
    with Pool(n) as pool: paths = pool.map(worker, parts)
    with open(A('out', 'parts.txt'), 'w') as fh: fh.writelines(f"file '{p}'\n" for p in paths)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', A('out', 'parts.txt'), '-ss', str(r0 / FPS), '-i', AUDIO,
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', a.out], check=True)
    print('ok', a.out)
