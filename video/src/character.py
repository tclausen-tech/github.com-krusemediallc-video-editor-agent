"""Personagem feminina em SVG — estilo ilustração semi-realista (luz e sombra, proporção ~7,5 cabeças).
Proporções reais: 1,65 m ≈ 1000 unidades. Gera camadas PNG em assets/char/:
  body_m{0-3}_b{0,1}_{down|phone}.png  -> corpo + cabeça (sem o braço que aponta)
  arm.png                              -> braço que aponta (pivô no ombro), desenhado apontando para BAIXO
Coordenadas: canvas 1000x1040 unidades; pivô do braço em PIVOT; topo do cabelo y≈22; sola y≈1020.
A geometria de encaixe (PIVOT, ARM_LEN, PHONE) é a mesma da versão anterior, então motion.py não muda.
"""
import os, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = os.path.join(ROOT, 'assets', 'char'); os.makedirs(OUT, exist_ok=True)

NAVY, NAVY_D, NAVY_L, YEL = '#001D52', '#00123A', '#123A7E', '#FEBF00'
SKIN, SKIN_L, SKIN_D, SKIN_DD = '#E8B795', '#F6D2B6', '#C98D6B', '#A86C4E'
HAIR, HAIR_D, HAIR_L = '#3A2216', '#1E110A', '#7A4A2C'
LIP_U, LIP_L, IRIS = '#A8474F', '#C9606A', '#5A3420'
PANTS, PANTS_L, SHOE = '#20242E', '#323846', '#121212'
PIVOT = (392, 238)            # ombro direito dela (lado esquerdo de quem vê)
ARM_LEN = 300                 # ombro -> centro da mão (unidades)
PHONE = (548, 395, 46, 92)    # celular na mão (x, y, w, h) — 7,5 x 15 cm na escala 1000u = 1,65 m

DEFS = f'''<defs>
<radialGradient id="gSkin" cx=".45" cy=".38" r=".7"><stop offset="0" stop-color="{SKIN_L}"/><stop offset=".55" stop-color="{SKIN}"/><stop offset="1" stop-color="{SKIN_D}"/></radialGradient>
<linearGradient id="gNeck" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SKIN_DD}"/><stop offset=".45" stop-color="{SKIN_D}"/><stop offset="1" stop-color="{SKIN}"/></linearGradient>
<linearGradient id="gHand" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{SKIN_L}"/><stop offset="1" stop-color="{SKIN_D}"/></linearGradient>
<linearGradient id="gHair" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{HAIR_L}"/><stop offset=".35" stop-color="{HAIR}"/><stop offset="1" stop-color="{HAIR_D}"/></linearGradient>
<linearGradient id="gHairB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{HAIR}"/><stop offset="1" stop-color="{HAIR_D}"/></linearGradient>
<linearGradient id="gBlazer" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{NAVY_D}"/><stop offset=".3" stop-color="{NAVY_L}"/><stop offset=".55" stop-color="{NAVY}"/><stop offset="1" stop-color="{NAVY_D}"/></linearGradient>
<linearGradient id="gSleeve" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{NAVY_D}"/><stop offset=".45" stop-color="{NAVY_L}"/><stop offset="1" stop-color="{NAVY_D}"/></linearGradient>
<linearGradient id="gPants" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{PANTS}"/><stop offset=".5" stop-color="{PANTS_L}"/><stop offset="1" stop-color="{PANTS}"/></linearGradient>
<linearGradient id="gShirt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#E4E8F0"/></linearGradient>
<radialGradient id="gIris" cx=".5" cy=".45" r=".55"><stop offset="0" stop-color="#8A5A34"/><stop offset=".7" stop-color="{IRIS}"/><stop offset="1" stop-color="#2A160C"/></radialGradient>
<linearGradient id="gLipL" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{LIP_U}"/><stop offset=".5" stop-color="{LIP_L}"/><stop offset="1" stop-color="{LIP_U}"/></linearGradient>
<filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="soft2" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="1.4"/></filter>
<filter id="o" x="-10%" y="-10%" width="120%" height="120%"><feMorphology in="SourceAlpha" operator="dilate" radius="4" result="d"/>
<feFlood flood-color="#fff"/><feComposite in2="d" operator="in" result="w"/><feMerge><feMergeNode in="w"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>'''

FACE = 'M500 42 C543 42 560 74 558 112 C556 142 546 162 527 176 C514 186 486 186 473 176 C454 162 444 142 442 112 C440 74 457 42 500 42Z'

def eyes(blink):
    s = ''
    for cx, sgn in ((476, -1), (524, 1)):
        # sombra da órbita / pálpebra
        s += f'<ellipse cx="{cx}" cy="104" rx="19" ry="9" fill="{SKIN_D}" opacity=".35" filter="url(#soft2)"/>'
        if blink:
            s += f'<path d="M{cx-16} 108 Q{cx} 117 {cx+16} 108" fill="none" stroke="#1A100B" stroke-width="3.2" stroke-linecap="round"/>'
            for k in (-10, -3, 4, 11):
                s += f'<path d="M{cx+k} {112+abs(k)*-.15} l{k*.25} 5" stroke="#1A100B" stroke-width="1.8" stroke-linecap="round"/>'
        else:
            eye = f'M{cx-16} 109 Q{cx-4} 98 {cx+16} 107 Q{cx+4} 118 {cx-16} 109Z'
            s += f'<path d="{eye}" fill="#FBF7F4"/>'
            s += f'<clipPath id="ce{cx}"><path d="{eye}"/></clipPath><g clip-path="url(#ce{cx})">'
            s += f'<circle cx="{cx+1}" cy="108" r="7.6" fill="url(#gIris)"/><circle cx="{cx+1}" cy="108" r="3.4" fill="#0E0805"/>'
            s += f'<path d="M{cx-16} 101 Q{cx} 97 {cx+16} 101 L{cx+16} 104 Q{cx} 101 {cx-16} 105Z" fill="#000" opacity=".22"/></g>'
            s += f'<circle cx="{cx+3.6}" cy="105.4" r="2.1" fill="#fff"/><circle cx="{cx-2}" cy="110.5" r=".9" fill="#fff" opacity=".8"/>'
            # cílio superior (mais grosso no canto externo) + vinco
            s += f'<path d="M{cx-17} 109 Q{cx-4} 96.5 {cx+17} 106" fill="none" stroke="#140C08" stroke-width="2.8" stroke-linecap="round"/>'
            ox = cx + 17 * sgn
            s += f'<path d="M{ox} {106 if sgn>0 else 109} l{4*sgn} -4 M{ox-3*sgn} {104 if sgn>0 else 106} l{3*sgn} -5" stroke="#140C08" stroke-width="1.8" stroke-linecap="round"/>'
            s += f'<path d="M{cx-13} 99 Q{cx} 92 {cx+14} 98" fill="none" stroke="{SKIN_DD}" stroke-width="1.3" opacity=".6"/>'
            s += f'<path d="M{cx-12} 113 Q{cx} 116.5 {cx+13} 110.5" fill="none" stroke="{SKIN_DD}" stroke-width="1" opacity=".5"/>'
        # sobrancelha afinando para fora
        bx = cx - 19 if sgn < 0 else cx - 17
        s += (f'<path d="M{cx-19*-sgn if False else cx-19} 92 Q{cx} 84 {cx+19} 90" fill="none" stroke="{HAIR_D}" stroke-width="3.6" stroke-linecap="round" opacity=".9"/>'
              if sgn > 0 else
              f'<path d="M{cx+19} 92 Q{cx} 84 {cx-19} 90" fill="none" stroke="{HAIR_D}" stroke-width="3.6" stroke-linecap="round" opacity=".9"/>')
    return s

def nose():
    return (f'<path d="M496 112 Q493 128 490 138" fill="none" stroke="{SKIN_D}" stroke-width="2.4" opacity=".55" filter="url(#soft2)"/>'
            f'<ellipse cx="502" cy="126" rx="3" ry="10" fill="{SKIN_L}" opacity=".7" filter="url(#soft2)"/>'
            f'<path d="M490 140 Q494 145 500 143 Q506 145 510 140" fill="none" stroke="{SKIN_DD}" stroke-width="2" stroke-linecap="round" opacity=".75"/>'
            f'<ellipse cx="500" cy="146" rx="8" ry="2.5" fill="{SKIN_D}" opacity=".45" filter="url(#soft2)"/>')

def mouth(m):
    y = 159
    if m == 0:
        return (f'<path d="M484 {y} Q492 {y-6} 500 {y-3} Q508 {y-6} 516 {y} Q500 {y+1} 484 {y}Z" fill="{LIP_U}"/>'
                f'<path d="M484 {y} Q500 {y+1} 516 {y} Q509 {y+10} 500 {y+10} Q491 {y+10} 484 {y}Z" fill="url(#gLipL)"/>'
                f'<path d="M485 {y} Q500 {y+2.2} 515 {y}" fill="none" stroke="#6E2A30" stroke-width="1.6" stroke-linecap="round"/>'
                f'<ellipse cx="502" cy="{y+5}" rx="5" ry="1.6" fill="#fff" opacity=".35"/>'
                f'<path d="M480 {y-1} q2 2 4 1 M520 {y-1} q-2 2 -4 1" stroke="{SKIN_DD}" stroke-width="1.2" fill="none" opacity=".6"/>')
    h = [0, 5, 9, 13][m]; w = [0, 15, 16, 17][m]
    return (f'<path d="M{500-w} {y} Q500 {y-3} {500+w} {y} Q{500+w-3} {y+h} 500 {y+h+1} Q{500-w+3} {y+h} {500-w} {y}Z" fill="#4A1418"/>'
            f'<path d="M{500-w+3} {y+.5} Q500 {y-1.5} {500+w-3} {y+.5} L{500+w-5} {y+1+min(3,h*.35)} Q500 {y+min(2,h*.3)} {500-w+5} {y+1+min(3,h*.35)}Z" fill="#F4F0EC"/>'
            f'<ellipse cx="500" cy="{y+h-1}" rx="{w*.55}" ry="{max(1.5,h*.28)}" fill="#C25A63"/>'
            f'<path d="M{500-w-1} {y} Q492 {y-7} 500 {y-4} Q508 {y-7} {500+w+1} {y} Q500 {y-1} {500-w-1} {y}Z" fill="{LIP_U}"/>'
            f'<path d="M{500-w-1} {y} Q{500-w+2} {y+h+2} 500 {y+h+7} Q{500+w-2} {y+h+2} {500+w+1} {y} Q{500+w-3} {y+h+1} 500 {y+h+2} Q{500-w+3} {y+h+1} {500-w-1} {y}Z" fill="url(#gLipL)"/>')

def head(m, b):
    s = f'<path d="{FACE}" fill="url(#gSkin)"/>'
    # contorno do rosto (sombra lateral e mandíbula), blush, queixo
    s += f'<path d="M444 112 C444 142 455 162 474 176 C486 184 500 185 500 185 C488 182 470 170 460 150 C452 134 450 120 452 106Z" fill="{SKIN_D}" opacity=".35" filter="url(#soft)"/>'
    s += f'<ellipse cx="462" cy="134" rx="14" ry="8" fill="#E07B78" opacity=".28" filter="url(#soft)"/><ellipse cx="538" cy="134" rx="14" ry="8" fill="#E07B78" opacity=".28" filter="url(#soft)"/>'
    s += f'<ellipse cx="500" cy="176" rx="12" ry="5" fill="{SKIN_L}" opacity=".5" filter="url(#soft)"/>'
    s += f'<ellipse cx="500" cy="70" rx="24" ry="12" fill="{SKIN_L}" opacity=".5" filter="url(#soft)"/>'
    s += eyes(b) + nose() + mouth(m)
    return s

def hair_back():
    return (f'<path d="M500 24 C426 22 410 80 416 140 C420 190 404 250 396 300 C392 330 410 346 438 338 C452 334 462 300 462 270 L538 270 '
            f'C538 300 548 334 562 338 C590 346 608 330 604 300 C596 250 580 190 584 140 C590 80 574 22 500 24Z" fill="url(#gHairB)"/>')

def hair_front():
    # calota + franja lateral (risca à esquerda de quem vê) e mechas que cobrem as orelhas
    s = (f'<path d="M436 114 C432 58 460 24 500 24 C546 24 570 58 566 114 C552 84 524 62 486 50 C470 60 452 80 446 108 Z" fill="url(#gHair)"/>')
    s += f'<path d="M446 100 C434 150 436 204 422 242 C444 238 456 204 456 160 C456 134 452 114 450 104 Z" fill="url(#gHair)"/>'
    s += f'<path d="M562 98 C574 150 568 204 582 242 C560 238 548 204 548 160 C548 134 552 112 556 102 Z" fill="url(#gHair)"/>'
    for d, c, w, o in [('M486 50 C520 60 548 80 562 108', HAIR_L, 2.4, .8), ('M490 36 C470 46 452 70 446 100', HAIR_L, 2, .6),
                       ('M506 30 C534 36 556 56 564 86', '#B0805A', 1.6, .6), ('M448 120 C444 160 440 200 430 236', HAIR_L, 1.8, .5),
                       ('M556 120 C560 160 566 200 576 236', HAIR_D, 2.2, .7), ('M492 52 C516 66 540 84 552 104', HAIR_D, 1.6, .6)]:
        s += f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" opacity="{o}"/>'
    return s

def left_arm(pose):  # braço esquerdo dela (lado direito de quem vê)
    if pose == 'down':
        return (f'<path d="M596 236 C618 242 626 262 628 290 L638 470 C639 486 628 494 616 494 L604 494 C592 494 586 486 586 472 L574 280 Z" fill="url(#gSleeve)"/>'
                f'<path d="M588 470 h46 v14 q-23 6 -46 0z" fill="#E9EDF3"/>'
                f'<path d="M596 484 C592 500 594 520 604 530 C612 538 626 536 630 524 C634 510 632 494 628 484Z" fill="url(#gHand)"/>'
                f'<path d="M602 512 q2 10 6 16 M610 514 q1 10 4 16 M618 512 q0 9 2 14" stroke="{SKIN_DD}" stroke-width="1.2" fill="none" opacity=".6"/>')
    px, py, pw, ph = PHONE
    return (f'<path d="M596 236 C618 242 626 262 628 290 L634 390 C635 408 622 416 610 414 L600 412 C590 410 584 402 584 390 L574 280 Z" fill="url(#gSleeve)"/>'
            f'<path d="M630 388 C636 410 622 424 606 430 L556 448 C540 454 530 444 532 432 C534 420 546 414 556 410 L604 392 Z" fill="url(#gSleeve)"/>'
            f'<rect x="{px-5}" y="{py-5}" width="{pw+10}" height="{ph+10}" rx="9" fill="#18181B"/>'
            f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="6" fill="#2A2C33"/>'
            f'<rect x="{px+4}" y="{py+4}" width="{pw*.35}" height="{ph-8}" rx="4" fill="#fff" opacity=".07"/>'
            f'<circle cx="{px+11}" cy="{py+11}" r="4.5" fill="#0D0D0F" stroke="#4A4A50" stroke-width="2"/>'
            f'<path d="M{px+pw*.3} {py+ph*.48} C{px+pw*.25} {py+ph*.75} {px+pw*.5} {py+ph*.85} {px+pw+8} {py+ph*.78} C{px+pw+16} {py+ph*.66} {px+pw+10} {py+ph*.5} {px+pw} {py+ph*.46}Z" fill="url(#gHand)"/>'
            f'<path d="M{px+pw*.35} {py+ph*.6} q-8 4 -6 12" stroke="{SKIN_D}" stroke-width="5" stroke-linecap="round" fill="none"/>')

def body(m, b, pose):
    s = hair_back()
    # pernas (calça social com vinco) + scarpin
    s += f'<path d="M414 520 L498 520 L494 958 L440 958 Z" fill="url(#gPants)"/><path d="M502 520 L586 520 L562 958 L508 958 Z" fill="url(#gPants)"/>'
    s += f'<path d="M458 540 L466 950 M544 540 L534 950" stroke="#454C5C" stroke-width="2" opacity=".7"/>'
    s += f'<path d="M496 524 L500 600" stroke="#151820" stroke-width="3"/>'
    s += f'<path d="M438 956 L496 956 C500 968 500 980 496 990 L424 990 C424 972 430 962 438 956Z" fill="{SHOE}"/><path d="M430 990 L434 1012 L442 1012 L444 990Z" fill="{SHOE}"/>'
    s += f'<path d="M506 956 L564 956 C572 962 578 972 578 990 L506 990 C502 980 502 968 506 956Z" fill="{SHOE}"/><path d="M558 990 L560 1012 L568 1012 L572 990Z" fill="{SHOE}"/>'
    s += f'<path d="M440 960 L494 960" stroke="#3A3A3A" stroke-width="2"/><path d="M508 960 L562 960" stroke="#3A3A3A" stroke-width="2"/>'
    # blazer acinturado
    s += (f'<path d="M404 234 C440 216 470 220 500 222 C530 220 560 216 596 234 C612 242 612 262 610 280 L590 420 C586 446 594 480 598 512 '
          f'C598 524 590 530 578 530 L422 530 C410 530 402 524 402 512 C406 480 414 446 410 420 L390 280 C388 262 388 242 404 234Z" fill="url(#gBlazer)"/>')
    # pescoço com sombra do queixo (desenhado sobre a gola)
    s += f'<path d="M482 168 L518 168 L520 236 L480 236Z" fill="url(#gNeck)"/>'
    s += f'<path d="M466 226 L534 226 L500 352 Z" fill="url(#gShirt)"/><path d="M478 226 Q500 252 522 226 Z" fill="{SKIN}"/>'
    s += f'<path d="M482 226 Q500 244 518 226" fill="none" stroke="{SKIN_D}" stroke-width="1.5" opacity=".6"/>'
    # lapelas
    s += f'<path d="M466 224 L500 352 L486 360 L452 270 L470 252 L448 238 Z" fill="{NAVY_L}"/><path d="M534 224 L500 352 L514 360 L548 270 L530 252 L552 238 Z" fill="{NAVY_D}"/>'
    s += f'<path d="M466 224 L500 352 M534 224 L500 352" stroke="#000A24" stroke-width="2" opacity=".6"/>'
    s += f'<circle cx="506" cy="392" r="6" fill="#0A1633" stroke="#33508A" stroke-width="1.5"/><circle cx="506" cy="440" r="6" fill="#0A1633" stroke="#33508A" stroke-width="1.5"/>'
    s += f'<path d="M500 352 L506 530" stroke="#000A24" stroke-width="2" opacity=".55"/>'
    s += f'<path d="M424 430 Q444 436 468 430 M532 430 Q556 436 576 430" stroke="#000A24" stroke-width="2" fill="none" opacity=".5"/>'
    s += f'<circle cx="548" cy="296" r="7" fill="{YEL}" stroke="#C99600" stroke-width="1.5"/>'
    s += f'<path d="M420 300 C430 360 432 400 428 430" stroke="#000A24" stroke-width="6" opacity=".25" fill="none" filter="url(#soft)"/>'
    s += left_arm(pose)
    # orelhas (meio escondidas) + brinco pequeno dourado
    s += head(m, b) + hair_front()
    s += f'<circle cx="447" cy="140" r="3.6" fill="{YEL}"/><circle cx="553" cy="140" r="3.6" fill="{YEL}"/>'
    return s

def arm():
    """Braço apontando para baixo a partir do pivô (0,0), com mão de dedo indicador estendido."""
    L = ARM_LEN
    return (f'<path d="M-26 -8 C-8 -20 14 -18 26 -6 L22 {L-60} C22 {L-46} 12 {L-40} 0 {L-40} C-12 {L-40} -22 {L-46} -22 {L-60} Z" fill="url(#gSleeve)"/>'
            f'<path d="M-6 0 L-4 {L-60}" stroke="#000A24" stroke-width="3" opacity=".35"/>'
            f'<path d="M-22 {L-62} h44 v16 q-22 7 -44 0z" fill="#E9EDF3"/>'
            f'<path d="M-17 {L-46} C-20 {L-32} -18 {L-16} -10 {L-8} C-4 {L-2} 6 {L-2} 12 {L-8} C18 {L-16} 18 {L-34} 16 {L-46} Z" fill="url(#gHand)"/>'
            f'<path d="M-6 {L-12} C-7 {L+6} -5 {L+26} -2 {L+38} C0 {L+44} 6 {L+44} 7 {L+38} C8 {L+24} 8 {L+6} 6 {L-10} Z" fill="url(#gHand)"/>'
            f'<path d="M-1 {L+36} q3 3 6 0" stroke="#F3D9C8" stroke-width="2" fill="none"/>'
            f'<path d="M-12 {L-14} q4 6 10 6 M8 {L-16} q4 2 6 -2" stroke="{SKIN_DD}" stroke-width="1.4" fill="none" opacity=".6"/>')

def svg(inner, w=1000, h=1040, vb='0 0 1000 1040'):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{vb}">{DEFS}<g filter="url(#o)">{inner}</g></svg>'

if __name__ == '__main__':
    pages = {}
    for pose in ('down', 'phone'):
        for m in range(4):
            for b in (0, 1):
                pages[f'body_m{m}_b{b}_{pose}'] = svg(body(m, b, pose), 2000, 2080)
    pages['arm'] = svg(arm(), 1440, 1440, '-360 -360 720 720')   # pivô no centro (720,720) px
    for k, v in pages.items():
        open(os.path.join(OUT, k + '.html'), 'w').write(f'<!doctype html><html><body style="margin:0;background:transparent">{v}</body></html>')
    json.dump(dict(pivot=PIVOT, arm_len=ARM_LEN, arm_pivot_px=[720, 720], scale_px_per_unit=2, phone=PHONE), open(os.path.join(OUT, 'meta.json'), 'w'))
    print(len(pages), 'páginas')
