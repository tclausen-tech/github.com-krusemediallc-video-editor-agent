"""Renderiza o vídeo. Uso: python3 render.py [--frames 10,20] [--workers 4] [--out arquivo.mp4]

Regra de proporção: cada cena tem uma escala em pixels por metro (PPM). A personagem (1,65 m), o
celular (7,5 x 15 cm), o monitor, o quadro e as lojas usam a escala da cena — nada é esticado nem
aumentado fora de escala. Quando a tela do celular precisa ser lida, ela aparece num PAINEL DE ZOOM
(lupa) ligado ao aparelho, em vez de aumentar o celular.
"""
import sys, os, json, math, subprocess, argparse
from functools import lru_cache
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from engine import *
from timeline import SCENES

AUDIO = A('in', 'narr.mp3')
WORDS = json.load(open(A('words.json')))
DUR = 122.52; NF = int(DUR * FPS)
COL = dict(red=PAL['red'], navy=PAL['navy'], navy_mk=PAL['navy'], text=PAL['text'])
CAPS = caption_chunks(WORDS)
MOUTH, LEVEL = mouth_track(AUDIO, WORDS, NF)
BLINKS = set(); _rng = np.random.default_rng(7); _t = 1.2
while _t < DUR:
    f0 = int(_t * FPS); BLINKS.update([f0, f0 + 1, f0 + 2]); _t += _rng.uniform(2.4, 4.2)

# ---------- personagem ----------
CM = json.load(open(A('assets', 'char', 'meta.json')))
PIV = CM['pivot']; ARM_LEN = CM['arm_len']; PHONE_U = CM['phone']
FIG_U = 1000            # unidades do desenho = 1,65 m
# escala e posição por tipo de cena: ppm = pixels por metro no plano da personagem
CHAR = {
    'room':   dict(ppm=760,  x=650, top=None, feet=1885),   # mesa 0,75 m; iMac 0,6 m
    'board':  dict(ppm=547,  x=930, top=None, feet=1840),   # quadro 1,8 m de largura
    'desk':   dict(ppm=1677, x=790, top=1240, feet=None),   # monitor 0,62 m de largura -> close
    'phone':  dict(ppm=1000, x=790, top=760,  feet=None),   # plano médio segurando o celular
    'street': dict(ppm=700,  x=880, top=None, feet=1895),   # primeiro plano na calçada
}
def char_geom(kind):
    c = CHAR[kind]; k = c['ppm'] * 1.65 / FIG_U          # px por unidade
    top = c['top'] if c['top'] is not None else c['feet'] - FIG_U * k
    left = c['x'] - 500 * k; ctop = top - 20 * k        # canto do canvas (cabelo começa em y=20u)
    return k, left, ctop

@lru_cache(64)
def body_img(m, b, pose, kind):
    k, left, ctop = char_geom(kind)
    src = Image.open(A('assets', 'char', f'body_m{m}_b{b}_{pose}.png'))      # 2 px por unidade
    vis_u = min(1040, (H - ctop) / k + 2)                                       # só a parte visível
    src = src.crop((0, 0, 2000, int(vis_u * 2)))
    return src.resize((max(1, int(2000 * k / 2)), max(1, int(src.height * k / 2))), Image.LANCZOS)

@lru_cache(512)
def arm_img(kind, ang):
    k = char_geom(kind)[0]; a = Image.open(A('assets', 'char', 'arm.png'))
    s = k / 2; a = a.resize((int(1440 * s), int(1440 * s)), Image.LANCZOS)
    return a.rotate(ang, center=(a.width / 2, a.height / 2), resample=Image.BICUBIC)

def pivot_px(kind):
    k, left, ctop = char_geom(kind); return left + PIV[0] * k, ctop + PIV[1] * k

# ---------- cenas ----------
def scene_at(t):
    for i, s in enumerate(SCENES):
        if s['t0'] <= t < s['t1']: return i, s
    return len(SCENES) - 1, SCENES[-1]

SCR = (36, 316, 1008, 680)                       # tela do monitor no mundo (bg_desk)
PANEL = (40, 300, 470)                           # painel de zoom do celular (x, y, largura)
PANEL_S = PANEL[2] / 600; PANEL_H = int(1260 * PANEL_S)

def phone_rect_px():
    k, left, ctop = char_geom('phone'); x, y, w, h = PHONE_U
    return left + x * k, ctop + y * k, w * k, h * k

def target_rect(s, tgt, t):
    if isinstance(tgt, tuple) and tgt[0] == 'rect': return tgt[1:]
    x, y, w, h = BOX[s['screen']][tgt]
    if s['kind'] == 'desk':
        k = SCR[2] / 1512; return SCR[0] + x * k, SCR[1] + y * k, w * k, h * k
    return PANEL[0] + x * PANEL_S, PANEL[1] + y * PANEL_S, w * PANEL_S, h * PANEL_S

@lru_cache(8)
def panel_img(name):
    scr = img(name).resize((PANEL[2], PANEL_H), Image.LANCZOS)
    b = 12; im = Image.new('RGBA', (PANEL[2] + 2 * b, PANEL_H + 2 * b), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, im.width - 1, im.height - 1), 46, fill=PAL['navy'])
    m = Image.new('L', scr.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, scr.width - 1, scr.height - 1), 36, fill=255)
    im.paste(scr, (b, b), m)
    # selo de lupa
    cx, cy = im.width - 44, 44
    d.ellipse((cx - 34, cy - 34, cx + 34, cy + 34), fill=PAL['yellow'], outline=(255, 255, 255), width=5)
    d.ellipse((cx - 16, cy - 18, cx + 10, cy + 8), outline=PAL['navy'], width=6); d.line((cx + 6, cy + 4, cx + 18, cy + 16), fill=PAL['navy'], width=7)
    sh = Image.new('RGBA', (im.width + 60, im.height + 60), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((30, 44, 30 + im.width, 44 + im.height), 46, fill=(0, 0, 0, 80))
    sh = sh.filter(ImageFilter.GaussianBlur(14)); sh.alpha_composite(im, (30, 30)); return sh

@lru_cache(4)
def base_world(i):
    s = SCENES[i]; k = s['kind']
    bg = img({'room': 'bg_room', 'desk': 'bg_desk', 'board': 'bg_board', 'phone': 'bg_sala', 'street': 'bg_street'}[k]).copy()
    if k == 'desk': bg.paste(img(s['screen']).resize(SCR[2:], Image.LANCZOS), SCR[:2])
    return bg

def board_pen(s, t):
    for e in s['ev']:
        if e[0] == 'write' and e[1] <= t < e[1] + e[2] + .15:
            _, t0, dur, txt, x, y, size, col = e; im = board_text(txt, size, COL[col]); k = min(1, (t - t0) / dur)
            return (x + im.width * k, y + im.height * .75)
        if e[0] == 'strike' and e[1] <= t < e[1] + e[2] + .1:
            _, t0, dur, x0, y, x1, col = e; k = min(1, (t - t0) / dur); return (x0 + (x1 - x0) * k, y)
    return None

# ---------- câmera + braço (pré-calculados em sequência) ----------
def precompute():
    cam = np.zeros((NF, 3)); arm = np.zeros((NF, 2))      # (ângulo, extensão da vareta 0..1)
    state = None; last = -1; ang = -8.0; ext = 0.0
    for f in range(NF):
        t = f / FPS; i, s = scene_at(t); kind = s['kind']; lt = t - s['t0']
        if i != last: state = None; last = i; ang = -8.0; ext = 0.0
        if kind == 'desk':
            push = ease_out(lt / .8); foc = [e for e in s['ev'] if e[0] == 'hl' and e[1] <= t < e[2]]
            if foc and lt > .8:
                x, y, w, h = target_rect(s, foc[-1][3], t); tx, ty, ts = x + w / 2, y + h / 2, s.get('zoom', 1.13)
            else: tx, ty, ts = 540, 842, 1.07
            if state is None or lt <= .8: state = [540, 960 + (842 - 960) * push, 1 + .07 * push]
            else: state = [state[j] + ((tx, ty, ts)[j] - state[j]) * .07 for j in range(3)]
            sc = state[2]; hw, hh = W / 2 / sc, H / 2 / sc
            cam[f] = (min(max(state[0], hw), W - hw), min(max(state[1], hh), H - hh), sc)
        elif kind in ('room', 'street'): cam[f] = (540, 960, 1.0 + .04 * ease_io(lt / (s['t1'] - s['t0'])))
        else: cam[f] = (540, 960, 1.0)
        # alvo do braço (em coordenadas do quadro final)
        tgt = None
        for e in s['ev']:
            if e[0] == 'point' and e[1] <= t < e[2]:
                x, y, w, h = target_rect(s, e[3], t); tgt = (x + w / 2, y + h / 2)
        if kind == 'board':
            p = board_pen(s, t); tgt = p or tgt
        if tgt is not None:
            if kind in ('desk', 'room', 'street'):
                cx, cy, sc = cam[f]; tgt = ((tgt[0] - cx) * sc + W / 2, (tgt[1] - cy) * sc + H / 2)
            px, py = pivot_px(kind); phi = math.degrees(math.atan2(tgt[1] - py, tgt[0] - px))
            want = 90 - phi
            while want > 20: want -= 360
            while want < -340: want += 360
            want = min(max(want, -215), 0); ang += (want - ang) * .35; ext += (1 - ext) * .35
        else:
            ang += (-8 - ang) * .25; ext += (0 - ext) * .45
        arm[f] = (ang, ext)
    return cam, arm
CAM, ARM = precompute()

def draw_hl(d, r, t0, t, pad=10):
    x, y, w, h = r; k = ease_out((t - t0) / .15); e = (1 - k) * 18; a = int(255 * k)
    box = (x - pad - e, y - pad - e, x + w + pad + e, y + h + pad + e)
    d.rounded_rectangle(box, 14, outline=PAL['hl_edge'] + (a,), width=13)
    d.rounded_rectangle(box, 14, outline=PAL['hl'] + (a,), width=7)

def render_frame(f):
    t = f / FPS; i, s = scene_at(t); kind = s['kind']; cx, cy, sc = CAM[f]
    world = base_world(i).copy(); d = ImageDraw.Draw(world, 'RGBA')
    screen_layer = []                      # coisas desenhadas no quadro final (fora da câmera)
    for e in s['ev']:
        typ = e[0]; on_panel = kind == 'phone' and not (isinstance(e[-1], tuple) and e[-1][0] == 'rect')
        if typ == 'hl' and e[1] <= t < e[2]:
            if kind == 'phone': screen_layer.append(e)
            else: draw_hl(d, target_rect(s, e[3], t), e[1], t)
        elif typ == 'mark' and e[1] <= t < e[2]:
            if kind == 'phone': screen_layer.append(e); continue
            x, y, w, h = target_rect(s, e[3], t); k = ease_out((t - e[1]) / .3)
            lay = Image.new('RGBA', world.size, (0, 0, 0, 0))
            ImageDraw.Draw(lay).rectangle((x - 6, y - 4, x - 6 + (w + 12) * k, y + h + 4), fill=PAL['marker'] + (105,))
            world.alpha_composite(lay)
        elif typ == 'tap' and e[1] <= t < e[1] + .45: screen_layer.append(e)
        elif typ == 'write' and t >= e[1]:
            _, t0, dur, txt, x, y, size, col = e; im = board_text(txt, size, COL[col])
            k = min(1, (t - t0) / dur); cw = int(im.width * k)
            if col == 'navy_mk' and cw > 0:
                d.rectangle((x - 6, y + im.height * .45, x + cw + 6, y + im.height * .95), fill=PAL['marker'] + (200,))
            if cw > 0: world.alpha_composite(im.crop((0, 0, cw, im.height)), (int(x), int(y)))
        elif typ == 'strike' and t >= e[1]:
            _, t0, dur, x0, y, x1, col = e; k = min(1, (t - t0) / dur)
            d.line((x0, y, x0 + (x1 - x0) * k, y + 4 * k), fill=COL[col] + (255,), width=12)
        elif typ == 'stamp' and t >= e[1]:
            _, t0, txt, scx, scy, size, col = e; k = ease_out((t - t0) / .22)
            im = board_text(txt, size, PAL['navy']); fr = Image.new('RGBA', (im.width + 60, im.height + 30), (0, 0, 0, 0))
            ImageDraw.Draw(fr).rounded_rectangle((4, 4, fr.width - 4, fr.height - 4), 18, fill=PAL['yellow'] + (255,), outline=PAL['navy'] + (255,), width=12)
            fr.alpha_composite(im, (30, 12)); z = 1.8 - .8 * k
            fr = fr.resize((int(fr.width * z), int(fr.height * z))).rotate(8, expand=True, resample=Image.BICUBIC)
            fr.putalpha(fr.split()[3].point(lambda v: int(v * min(1, k * 1.5))))
            world.alpha_composite(fr, (int(scx - fr.width / 2), int(scy - fr.height / 2)))
    # câmera
    if abs(sc - 1) < 1e-3 and cx == 540 and cy == 960: frame = world
    else: frame = world.transform((W, H), Image.AFFINE, (1 / sc, 0, cx - W / 2 / sc, 0, 1 / sc, cy - H / 2 / sc), resample=Image.BILINEAR)
    fd = ImageDraw.Draw(frame, 'RGBA')
    # personagem
    lt = t - s['t0']; k, left, ctop = char_geom(kind)
    bob = math.sin(t * 2 * math.pi * .45) * 3 * k / 1.25
    hop = 0.0
    for e in s['ev']:
        if e[0] == 'label' and 0 <= t - e[1] < .3: hop = max(hop, math.sin((t - e[1]) / .3 * math.pi) * 10 * k / 1.25)
    dy = bob - hop
    m = MOUTH[min(f, NF - 1)]; b = 1 if f in BLINKS else 0
    pose = 'phone' if kind == 'phone' else 'down'
    ang, ext = ARM[f]; pvx, pvy = pivot_px(kind); pvy += dy
    # vareta (atrás do braço), saindo da mão na direção do braço
    # direção do braço: rotacionar (0,1) pelo ângulo visual anti-horário 'ang'
    dirx, diry = math.sin(math.radians(ang)), math.cos(math.radians(ang))
    hx, hy = pvx + dirx * (ARM_LEN - 10) * k, pvy + diry * (ARM_LEN - 10) * k
    tgt = None
    for e in s['ev']:
        if e[0] == 'point' and e[1] <= t < e[2]:
            x, y, w, h = target_rect(s, e[3], t); tgt = (x + w / 2, y + h / 2)
    if kind == 'board': tgt = board_pen(s, t) or tgt
    if tgt is not None and kind in ('desk', 'room', 'street'): tgt = ((tgt[0] - cx) * sc + W / 2, (tgt[1] - cy) * sc + H / 2)
    if ext > .02 and tgt is not None:
        dist = math.hypot(tgt[0] - hx, tgt[1] - hy) * ext
        sw = max(5, int(PPM_STICK * CHAR[kind]['ppm']))
        ex, ey = hx + dirx * dist, hy + diry * dist
        fd.line((hx, hy, ex, ey), fill=(255, 255, 255, 255), width=sw + 6)
        fd.line((hx, hy, ex, ey), fill=(20, 20, 20, 255), width=sw)
        r = sw * 1.6; fd.ellipse((ex - r, ey - r, ex + r, ey + r), fill=PAL['yellow'], outline=(20, 20, 20), width=max(3, sw // 2))
    # painel de zoom do celular (faixa atrás da personagem, painel e contorno do aparelho na frente)
    if kind == 'phone':
        px, py, pw, ph = phone_rect_px(); py += dy; kk = ease_out(lt / .35)
        ax, ay = PANEL[0] + PANEL[2] + 12, PANEL[1]
        poly = [(ax, ay + 40), (ax, ay + PANEL_H - 40), (px, py + ph), (px, py)]
        if kk > .01:
            fd.polygon(poly, fill=(255, 255, 255, int(80 * kk)))
            fd.line([poly[0], poly[3]], fill=PAL['navy'] + (int(200 * kk),), width=4); fd.line([poly[1], poly[2]], fill=PAL['navy'] + (int(200 * kk),), width=4)
    a_img = arm_img(kind, int(round(ang)))
    frame.alpha_composite(a_img, (int(pvx - a_img.width / 2), int(pvy - a_img.height / 2)))
    bimg = body_img(m, b, pose, kind)
    frame.alpha_composite(bimg, (int(left), int(ctop + dy)))
    if kind == 'phone' and kk > .01:
        fd.rounded_rectangle((px - 6, py - 6, px + pw + 6, py + ph + 6), 8, outline=PAL['yellow'] + (int(255 * kk),), width=5)
        pim = panel_img(s['screen'])
        if kk < 1: pim = pim.copy(); pim.putalpha(pim.split()[3].point(lambda v: int(v * kk)))
        frame.alpha_composite(pim, (PANEL[0] - 42, int(PANEL[1] - 42 + (1 - kk) * 30)))
    # destaques em coordenadas de tela
    for e in screen_layer:
        if e[0] == 'hl': draw_hl(fd, target_rect(s, e[3], t), e[1], t)
        elif e[0] == 'mark':
            x, y, w, h = target_rect(s, e[3], t); kk = ease_out((t - e[1]) / .3)
            fd.rectangle((x - 6, y - 4, x - 6 + (w + 12) * kk, y + h + 4), fill=PAL['marker'] + (105,))
        elif e[0] == 'tap':
            x, y, w, h = target_rect(s, e[2], t) if kind != 'room' else e[2][1:]
            if kind in ('desk', 'street'): x, y = (x - cx) * sc + W / 2, (y - cy) * sc + H / 2
            kk = (t - e[1]) / .45; r = 20 + 70 * ease_out(kk)
            fd.ellipse((x + w / 2 - r, y + h / 2 - r, x + w / 2 + r, y + h / 2 + r), outline=(255, 255, 255, int(255 * (1 - kk))), width=10)
            fd.ellipse((x + w / 2 - r + 6, y + h / 2 - r + 6, x + w / 2 + r - 6, y + h / 2 + r - 6), outline=PAL['navy'] + (int(230 * (1 - kk)),), width=6)
    # ícones e botão (tela)
    for e in s['ev']:
        if e[0] == 'prop' and e[1] <= t < e[2]:
            im = prop(e[3]); kk = ease_out((t - e[1]) / .3); z = .4 + .6 * kk + .08 * math.sin(min(1, (t - e[1]) / .5) * math.pi)
            im2 = im.resize((max(1, int(im.width * z)), max(1, int(im.height * z))))
            frame.alpha_composite(im2, (int(e[4] - im2.width / 2), int(e[5] - im2.height / 2)))
    # etiquetas
    for e in s['ev']:
        if e[0] == 'label' and e[1] <= t < e[2]:
            opt = e[4] if len(e) > 4 else {}
            im = label_img(e[3], opt.get('big', False), opt.get('maxw', 900), opt.get('style', 'navy'))
            a = min(1, (t - e[1]) / .15, (e[2] - t) / .15 if e[2] < s['t1'] - .05 else 1)
            if a < 1: im = im.copy(); im.putalpha(im.split()[3].point(lambda v: int(v * a)))
            frame.alpha_composite(im, (int((W - im.width) / 2), int(opt.get('y', 175))))
    for (t0, t1, txt) in CAPS:
        if t0 <= t < t1:
            im = caption_img(txt); frame.alpha_composite(im, (int((W - im.width) / 2), int(1238 - im.height / 2))); break
    return frame.convert('RGB')

PPM_STICK = 0.012       # vareta com 1,2 cm de espessura, na escala da cena

def worker(args):
    a, b, path = args
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
    for f in range(a, b): p.stdin.write(render_frame(f).tobytes())
    p.stdin.close(); p.wait(); return path

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--frames'); ap.add_argument('--workers', type=int, default=4); ap.add_argument('--out', default=A('out', 'video.mp4'))
    a = ap.parse_args(); os.makedirs(A('out'), exist_ok=True)
    if a.frames:
        for t in a.frames.split(','):
            render_frame(int(float(t) * FPS)).save(A('out', f'f_{float(t):06.2f}.png'))
        sys.exit()
    n = a.workers; step = math.ceil(NF / n)
    parts = [(k * step, min(NF, (k + 1) * step), A('out', f'part{k}.mp4')) for k in range(n)]
    with Pool(n) as pool: paths = pool.map(worker, parts)
    with open(A('out', 'parts.txt'), 'w') as fh: fh.writelines(f"file '{p}'\n" for p in paths)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', A('out', 'parts.txt'), '-i', AUDIO,
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', a.out], check=True)
    print('ok', a.out)
