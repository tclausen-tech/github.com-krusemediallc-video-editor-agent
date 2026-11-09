"""Personagem feminina em SVG (estilo flat, proporções reais: 1,65 m ≈ 1000 unidades).
Gera camadas PNG em assets/char/:
  body_m{0-3}_b{0,1}_{down|phone}.png  -> corpo + cabeça (sem o braço que aponta)
  arm.png                              -> braço que aponta (pivô no ombro), desenhado apontando para BAIXO
Coordenadas: canvas 1000x1040 unidades; pivô do braço em PIVOT; topo do cabelo y=20; sola y=1020.
"""
import os, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = os.path.join(ROOT, 'assets', 'char'); os.makedirs(OUT, exist_ok=True)

NAVY, NAVY2, YEL = '#001D52', '#0B2C6B', '#FEBF00'
SKIN, SKIN2 = '#E9B48F', '#D79B76'
HAIR, HAIR2 = '#2E1B12', '#4A2C1C'
PANTS, SHOE, LIP = '#2B2F3A', '#151515', '#B8505A'
PIVOT = (392, 238)            # ombro direito dela (lado esquerdo de quem vê)
ARM_LEN = 300                 # ombro -> centro da mão (unidades)
PHONE = (548, 395, 46, 92)    # celular na mão (x, y, w, h) — 7,5 x 15 cm na escala 1000u = 1,65 m

def eyes(blink):
    s = ''
    for cx in (472, 528):
        if blink:
            s += f'<path d="M{cx-17} 112 q17 11 34 0" fill="none" stroke="#1B1210" stroke-width="4.5" stroke-linecap="round"/>'
            s += f'<path d="M{cx-15} 116 l-4 5 M{cx} 119 v6 M{cx+15} 116 l4 5" stroke="#1B1210" stroke-width="2.5" stroke-linecap="round"/>'
        else:
            s += f'<ellipse cx="{cx}" cy="112" rx="15" ry="17" fill="#fff"/>'
            s += f'<circle cx="{cx+1}" cy="114" r="10.5" fill="#6B3A22"/><circle cx="{cx+1}" cy="114" r="5.5" fill="#120B08"/>'
            s += f'<circle cx="{cx+4}" cy="109" r="3.2" fill="#fff"/>'
            s += f'<path d="M{cx-18} 104 q18 -14 36 -1" fill="none" stroke="#1B1210" stroke-width="5" stroke-linecap="round"/>'
            s += f'<path d="M{cx+15} 101 l7 -5 M{cx+12} 99 l5 -6" stroke="#1B1210" stroke-width="2.5" stroke-linecap="round"/>' if cx > 500 else \
                 f'<path d="M{cx-15} 101 l-7 -5 M{cx-12} 99 l-5 -6" stroke="#1B1210" stroke-width="2.5" stroke-linecap="round"/>'
        s += f'<path d="M{cx-18} 86 q18 -10 34 -2" fill="none" stroke="{HAIR}" stroke-width="5.5" stroke-linecap="round"/>'
    return s

def mouth(m):
    if m == 0:
        return f'<path d="M486 160 q14 10 28 0" fill="none" stroke="{LIP}" stroke-width="5" stroke-linecap="round"/>'
    h = [0, 7, 12, 17][m]; w = [0, 13, 16, 18][m]
    return (f'<path d="M{500-w} 158 q{w} -4 {2*w} 0 q-3 {h+6} -{w} {h+6} q-{w-3} 0 -{w} -{h+6}z" fill="#5B1820" stroke="{LIP}" stroke-width="3.5" stroke-linejoin="round"/>'
            f'<path d="M{500-w+4} 159.5 h{2*w-8}" stroke="#fff" stroke-width="{2+m}" stroke-linecap="round"/>'
            f'<ellipse cx="500" cy="{158+h+1}" rx="{w*0.55}" ry="{max(2,h*0.3)}" fill="#D9707A"/>')

def hair_back():
    return (f'<path d="M418 78 q-2 -70 82 -70 q84 0 82 70 q14 60 8 140 q-4 70 22 120 q-60 18 -112 -8 q-10 -40 0 -90 '
            f'q0 0 0 0 h0 q10 50 0 90 q-52 26 -112 8 q26 -50 22 -120 q-6 -80 8 -140z" fill="{HAIR}"/>')

def hair_front():
    return (f'<path d="M434 92 q-6 -64 66 -70 q74 -2 70 74 q-30 -40 -82 -38 q-20 16 -54 34z" fill="{HAIR}"/>'
            f'<path d="M488 62 q30 -10 66 6" fill="none" stroke="{HAIR2}" stroke-width="4" stroke-linecap="round"/>'
            f'<path d="M436 96 q-10 50 -2 100" fill="none" stroke="{HAIR}" stroke-width="16" stroke-linecap="round"/>'
            f'<path d="M565 96 q10 50 2 100" fill="none" stroke="{HAIR}" stroke-width="16" stroke-linecap="round"/>')

def left_arm(pose):  # braço esquerdo dela (lado direito de quem vê)
    if pose == 'down':
        return (f'<path d="M598 232 q24 6 28 40 l18 210 q2 18 -18 18 h-12 q-16 0 -18 -16 l-24 -205z" fill="{NAVY}"/>'
                f'<rect x="606" y="482" width="40" height="16" rx="6" fill="#fff"/>'
                f'<ellipse cx="624" cy="512" rx="19" ry="22" fill="{SKIN}"/>')
    # segurando o celular na frente do peito
    px, py, pw, ph = PHONE
    return (f'<path d="M598 232 q24 6 28 40 l10 120 q2 20 -16 22 l-10 0 q-14 -2 -16 -18 l-20 -125z" fill="{NAVY}"/>'
            f'<path d="M626 392 q4 22 -16 30 l-60 26 q-16 6 -22 -8 q-6 -14 10 -22 l58 -32z" fill="{NAVY}"/>'
            f'<rect x="{px-6}" y="{py-6}" width="{pw+12}" height="{ph+12}" rx="10" fill="#1A1A1A"/>'
            f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="7" fill="#2A2A2E"/>'
            f'<circle cx="{px+11}" cy="{py+11}" r="5" fill="#111" stroke="#444" stroke-width="2"/>'
            f'<ellipse cx="{px+pw/2+6}" cy="{py+ph*0.62}" rx="22" ry="17" fill="{SKIN}"/>'
            f'<path d="M{px+pw/2-14} {py+ph*0.52} q-10 8 0 18" fill="none" stroke="{SKIN2}" stroke-width="3"/>')

def body(m, b, pose):
    s = hair_back()
    # pernas + sapatos
    s += f'<path d="M410 520 h88 l-6 440 h-62z" fill="{PANTS}"/><path d="M502 520 h88 l-20 440 h-62z" fill="{PANTS}"/>'
    s += f'<path d="M424 958 h66 q12 0 12 14 v18 h-96 q0 -32 18 -32z" fill="{SHOE}"/><path d="M510 958 h66 q18 0 18 32 h-96 v-18 q0 -14 12 -14z" fill="{SHOE}"/>'
    # pescoço
    s += f'<path d="M478 176 h44 v54 q-22 14 -44 0z" fill="{SKIN2}"/>'
    # tronco (blazer) + blusa
    s += f'<path d="M402 232 q40 -18 98 -10 q58 -8 98 10 q14 8 12 30 l-16 250 q-2 18 -20 18 h-148 q-18 0 -20 -18 l-16 -250 q-2 -22 12 -30z" fill="{NAVY}"/>'
    s += f'<path d="M466 226 h68 l-34 116z" fill="#FFFFFF"/><path d="M478 226 q22 26 44 0" fill="{SKIN}"/>'
    s += f'<path d="M466 226 l34 116 l-30 -20 l-20 -70z" fill="{NAVY2}"/><path d="M534 226 l-34 116 l30 -20 l20 -70z" fill="{NAVY2}"/>'
    s += f'<circle cx="548" cy="300" r="9" fill="{YEL}"/>'
    s += f'<rect x="404" y="508" width="192" height="16" rx="4" fill="#0A1633"/><rect x="490" y="508" width="20" height="16" rx="3" fill="{YEL}"/>'
    s += left_arm(pose)
    # cabeça
    s += f'<ellipse cx="434" cy="122" rx="10" ry="15" fill="{SKIN2}"/><ellipse cx="566" cy="122" rx="10" ry="15" fill="{SKIN2}"/>'
    s += f'<circle cx="432" cy="142" r="6" fill="{YEL}"/><circle cx="568" cy="142" r="6" fill="{YEL}"/>'
    s += f'<path d="M438 100 q0 -70 62 -70 q62 0 62 70 q0 52 -24 76 q-16 16 -38 16 q-22 0 -38 -16 q-24 -24 -24 -76z" fill="{SKIN}"/>'
    s += f'<ellipse cx="456" cy="140" rx="11" ry="7" fill="#E88B8B" opacity=".45"/><ellipse cx="544" cy="140" rx="11" ry="7" fill="#E88B8B" opacity=".45"/>'
    s += f'<path d="M500 118 q-6 16 -2 22 q4 2 8 0" fill="none" stroke="{SKIN2}" stroke-width="3.5" stroke-linecap="round"/>'
    s += eyes(b) + mouth(m) + hair_front()
    return s

def arm():
    """Braço apontando para baixo a partir do pivô (0,0)."""
    return (f'<path d="M-24 -6 q24 -14 48 0 l-2 250 q0 16 -16 16 h-12 q-16 0 -16 -16z" fill="{NAVY}"/>'
            f'<rect x="-20" y="246" width="40" height="16" rx="6" fill="#fff"/>'
            f'<ellipse cx="0" cy="{ARM_LEN-24}" rx="18" ry="20" fill="{SKIN}"/>'
            f'<path d="M-6 {ARM_LEN-8} q6 30 4 46" stroke="{SKIN}" stroke-width="13" stroke-linecap="round" fill="none"/>')

def svg(inner, w=1000, h=1040, vb='0 0 1000 1040'):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{vb}">{inner}</svg>'

def outlined(inner):
    # contorno branco tipo adesivo (mesma linguagem visual da versão anterior)
    return (f'<defs><filter id="o" x="-10%" y="-10%" width="120%" height="120%"><feMorphology in="SourceAlpha" operator="dilate" radius="5" result="d"/>'
            f'<feFlood flood-color="#fff"/><feComposite in2="d" operator="in" result="w"/><feMerge><feMergeNode in="w"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
            f'<g filter="url(#o)">{inner}</g>')

if __name__ == '__main__':
    pages = {}
    for pose in ('down', 'phone'):
        for m in range(4):
            for b in (0, 1):
                pages[f'body_m{m}_b{b}_{pose}'] = svg(outlined(body(m, b, pose)), 2000, 2080)
    pages['arm'] = svg(outlined(arm()), 1440, 1440, '-360 -360 720 720')   # pivô no centro (720,720) px
    for k, v in pages.items():
        open(os.path.join(OUT, k + '.html'), 'w').write(f'<!doctype html><html><body style="margin:0;background:transparent">{v}</body></html>')
    json.dump(dict(pivot=PIVOT, arm_len=ARM_LEN, arm_pivot_px=[720, 720], scale_px_per_unit=2, phone=PHONE), open(os.path.join(OUT, 'meta.json'), 'w'))
    print(len(pages), 'páginas')
