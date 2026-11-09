"""Personagem feminina "Jana" (identidade Jamap) — mascote vetorial estilo "fofo moderno", em SVG.

Estilo: cabeça grande (~3 cabeças de altura), rosto arredondado, olhos grandes com dois brilhos, franja cortina,
cabelo castanho ondulado até os ombros, bochechas rosadas, cabeça levemente inclinada. Roupa: blazer azul-marinho
Jamap, blusa branca, colar com pingente amarelo, saia evasê amarela e sapatilha azul-marinho. Contorno escuro fino +
borda branca de "adesivo".

Canvas 1000x1040 unidades; sola em y≈1020. Gera em assets/char/:
  body_m{0-3}_b{0,1}_{down|phone}.png  -> corpo + cabeça (sem o braço que aponta)
  arm.png                              -> braço que aponta (pivô no ombro), desenhado apontando para BAIXO
meta.json guarda pivô, comprimento do braço e o retângulo do celular, que motion.py lê.
"""
import os, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = os.path.join(ROOT, 'assets', 'char'); os.makedirs(OUT, exist_ok=True)

NAVY, NAVY_D, NAVY_L, YEL, YEL_D, YEL_L = '#001D52', '#00102F', '#1D4796', '#FEBF00', '#E0A200', '#FFD54D'
SKIN, SKIN_L, SKIN_D = '#FFD9C2', '#FFE9DC', '#F2B597'
HAIR, HAIR_D, HAIR_L = '#6B3A26', '#3E1F14', '#9C5E3E'
LINE = '#2A1A2E'
PIVOT = (408, 440)            # ombro direito dela (lado esquerdo de quem vê)
ARM_LEN = 196                 # ombro -> centro da mão
PHONE = (566, 520, 46, 92)    # celular na mão (x, y, w, h)
TILT = 'rotate(-4 500 400)'   # inclinação charmosa da cabeça

DEFS = f'''<defs>
<radialGradient id="gSkin" cx=".5" cy=".45" r=".65"><stop offset="0" stop-color="{SKIN_L}"/><stop offset=".7" stop-color="{SKIN}"/><stop offset="1" stop-color="{SKIN_D}"/></radialGradient>
<linearGradient id="gLimb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{SKIN_D}"/><stop offset=".45" stop-color="{SKIN_L}"/><stop offset="1" stop-color="{SKIN}"/></linearGradient>
<linearGradient id="gHair" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{HAIR_L}"/><stop offset=".45" stop-color="{HAIR}"/><stop offset="1" stop-color="{HAIR_D}"/></linearGradient>
<linearGradient id="gHairB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{HAIR}"/><stop offset="1" stop-color="{HAIR_D}"/></linearGradient>
<linearGradient id="gBlazer" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{NAVY_L}"/><stop offset=".55" stop-color="{NAVY}"/><stop offset="1" stop-color="{NAVY_D}"/></linearGradient>
<linearGradient id="gSleeve" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{NAVY_L}"/><stop offset="1" stop-color="{NAVY}"/></linearGradient>
<linearGradient id="gSkirt" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{YEL_L}"/><stop offset=".6" stop-color="{YEL}"/><stop offset="1" stop-color="{YEL_D}"/></linearGradient>
<radialGradient id="gIris" cx=".5" cy=".7" r=".75"><stop offset="0" stop-color="#C7834A"/><stop offset=".45" stop-color="#7A4224"/><stop offset="1" stop-color="#2A120A"/></radialGradient>
<filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="5"/></filter>
<filter id="soft2" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="2"/></filter>
<filter id="o" x="-10%" y="-10%" width="120%" height="120%">
 <feMorphology in="SourceAlpha" operator="dilate" radius="3" result="d1"/><feFlood flood-color="{LINE}"/><feComposite in2="d1" operator="in" result="dark"/>
 <feMorphology in="SourceAlpha" operator="dilate" radius="9" result="d2"/><feFlood flood-color="#fff"/><feComposite in2="d2" operator="in" result="white"/>
 <feMerge><feMergeNode in="white"/><feMergeNode in="dark"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>'''

FACE = ('M500 112 C588 112 638 170 638 246 C638 306 600 350 546 364 C526 370 512 372 500 372 '
        'C488 372 474 370 454 364 C400 350 362 306 362 246 C362 170 412 112 500 112Z')
EY = 262

def eyes(blink):
    s = ''
    for cx, sg in ((446, -1), (554, 1)):
        if blink:   # olho fechado sorrindo (arco para cima) + cílio
            s += f'<path d="M{cx-24} {EY+4} Q{cx} {EY-14} {cx+24} {EY+4}" fill="none" stroke="{LINE}" stroke-width="6" stroke-linecap="round"/>'
            ox = cx + 24 * sg
            s += f'<path d="M{ox-2*sg} {EY+1} l{8*sg} -6" stroke="{LINE}" stroke-width="4" stroke-linecap="round"/>'
        else:
            s += f'<ellipse cx="{cx}" cy="{EY}" rx="25" ry="31" fill="#FFFFFF"/>'
            s += f'<clipPath id="ce{cx}"><ellipse cx="{cx}" cy="{EY}" rx="25" ry="31"/></clipPath><g clip-path="url(#ce{cx})">'
            s += f'<ellipse cx="{cx+2*sg}" cy="{EY+4}" rx="21" ry="27" fill="url(#gIris)"/>'
            s += f'<ellipse cx="{cx+2*sg}" cy="{EY+6}" rx="10" ry="13" fill="#1A0904"/>'
            s += f'<ellipse cx="{cx}" cy="{EY-24}" rx="30" ry="14" fill="#2A120A" opacity=".35"/></g>'   # sombra da pálpebra
            s += f'<ellipse cx="{cx-7}" cy="{EY-8}" rx="8" ry="10" fill="#fff"/><circle cx="{cx+9}" cy="{EY+14}" r="4" fill="#fff" opacity=".9"/>'
            s += f'<path d="M{cx-6} {EY+20} Q{cx+4} {EY+26} {cx+14} {EY+18}" stroke="#E7A36B" stroke-width="2.5" fill="none" opacity=".7"/>'
            # cílio superior grosso + dois cílios no canto externo
            s += f'<path d="M{cx-27} {EY-4} C{cx-22} {EY-34} {cx+22} {EY-36} {cx+28} {EY-6}" fill="none" stroke="{LINE}" stroke-width="7" stroke-linecap="round"/>'
            ox = cx + 27 * sg
            s += f'<path d="M{ox-1*sg} {EY-10} q{7*sg} -2 {12*sg} -10 M{ox-6*sg} {EY-20} q{5*sg} -4 {8*sg} -12" stroke="{LINE}" stroke-width="4" fill="none" stroke-linecap="round"/>'
        # sobrancelha suave (arco alegre)
        s += f'<path d="M{cx-20} {EY-50} Q{cx+2*sg} {EY-62} {cx+22} {EY-52}" fill="none" stroke="{HAIR_D}" stroke-width="6" stroke-linecap="round"/>'
    return s

def mouth(m):
    y = 326
    if m == 0:   # sorriso fechado
        return (f'<path d="M478 {y-4} Q500 {y+16} 522 {y-4}" fill="none" stroke="{LINE}" stroke-width="5" stroke-linecap="round"/>'
                f'<path d="M488 {y+6} Q500 {y+12} 512 {y+6}" fill="none" stroke="#E2788A" stroke-width="3" stroke-linecap="round" opacity=".6"/>')
    w = [0, 14, 18, 21][m]; h = [0, 12, 20, 27][m]
    return (f'<path d="M{500-w} {y-4} Q500 {y-1} {500+w} {y-4} Q{500+w} {y+h} 500 {y+h+2} Q{500-w} {y+h} {500-w} {y-4}Z" fill="#7A1E35" stroke="{LINE}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M{500-w+4} {y-2} Q500 {y} {500+w-4} {y-2} L{500+w-6} {y+3} Q500 {y+5} {500-w+6} {y+3}Z" fill="#fff"/>'
            f'<ellipse cx="500" cy="{y+h-3}" rx="{w*.55}" ry="{max(3, h*.28)}" fill="#F0788C"/>')

def head(m, b):
    s = f'<path d="{FACE}" fill="url(#gSkin)"/>'
    s += f'<path d="M370 200 Q500 150 630 200 L630 230 Q500 186 370 230Z" fill="{SKIN_D}" opacity=".45" filter="url(#soft)"/>'   # sombra da franja
    s += f'<ellipse cx="418" cy="312" rx="26" ry="15" fill="#FF8C9A" opacity=".45" filter="url(#soft2)"/><ellipse cx="582" cy="312" rx="26" ry="15" fill="#FF8C9A" opacity=".45" filter="url(#soft2)"/>'
    s += f'<path d="M410 306 l8 -6 M420 310 l8 -6 M574 306 l8 -6 M584 310 l8 -6" stroke="#fff" stroke-width="2.5" stroke-linecap="round" opacity=".7"/>'
    s += f'<path d="M496 298 Q501 302 506 297" fill="none" stroke="#D98C72" stroke-width="3.5" stroke-linecap="round"/>'   # nariz pequeno
    s += eyes(b) + mouth(m)
    return s

def hair_back():
    return (f'<g transform="{TILT}"><path d="M500 52 C380 50 330 140 336 250 C340 320 326 380 332 440 C338 488 368 510 392 494 '
            f'C404 518 438 520 446 494 L554 494 C562 520 596 518 608 494 C632 510 662 488 668 440 '
            f'C674 380 660 320 664 250 C670 140 620 50 500 52Z" fill="url(#gHairB)"/></g>')

def hair_front():
    s = f'<g transform="{TILT}">'
    # calota com volume
    s += f'<path d="M352 250 C340 130 410 66 500 66 C590 66 660 130 648 250 C636 190 600 150 560 138 C540 132 520 128 500 128 C480 128 460 132 440 138 C400 150 364 190 352 250Z" fill="url(#gHair)"/>'
    # franja cortina (risca no meio)
    s += f'<path d="M500 96 C470 124 430 150 400 196 C386 218 376 246 372 272 C392 236 420 206 452 186 C476 170 492 140 500 112Z" fill="url(#gHair)"/>'
    s += f'<path d="M500 96 C530 124 570 150 600 196 C614 218 624 246 628 272 C608 236 580 206 548 186 C524 170 508 140 500 112Z" fill="url(#gHair)"/>'
    # mechas laterais emoldurando o rosto, com cacho para fora na ponta
    s += (f'<path d="M372 240 C356 300 362 360 350 420 C344 452 330 470 344 488 C360 480 378 460 384 430 '
          f'C392 390 386 340 392 290Z" fill="url(#gHair)"/>')
    s += (f'<path d="M628 240 C644 300 638 360 650 420 C656 452 670 470 656 488 C640 480 622 460 616 430 '
          f'C608 390 614 340 608 290Z" fill="url(#gHair)"/>')
    # brilho do cabelo (faixa clara no topo)
    s += f'<path d="M408 122 C450 92 550 92 592 122" fill="none" stroke="#C88A64" stroke-width="10" stroke-linecap="round" opacity=".55"/>'
    s += f'<path d="M430 112 C460 98 486 94 500 94" fill="none" stroke="#F0C29E" stroke-width="5" stroke-linecap="round" opacity=".6"/>'
    s += f'<path d="M462 150 C450 170 430 190 414 214 M538 150 C550 170 570 190 586 214" stroke="{HAIR_D}" stroke-width="3" fill="none" opacity=".5"/>'
    # presilha amarela Jamap
    s += f'<g transform="rotate(-25 590 150)"><rect x="566" y="140" width="48" height="16" rx="8" fill="{YEL}" stroke="{YEL_D}" stroke-width="2"/></g>'
    return s + '</g>'

def head_group(m, b):
    return (f'<g transform="{TILT}">{head(m, b)}'
            f'<circle cx="364" cy="318" r="9" fill="none" stroke="{YEL}" stroke-width="4"/><circle cx="636" cy="318" r="9" fill="none" stroke="{YEL}" stroke-width="4"/></g>'
            + hair_front())

def legs():
    return (f'<path d="M458 760 C454 830 456 900 462 968 L494 968 C496 900 498 830 496 760Z" fill="url(#gLimb)"/>'
            f'<path d="M504 760 C502 830 504 900 506 968 L538 968 C544 900 546 830 542 760Z" fill="url(#gLimb)"/>'
            # sapatilhas azul-marinho com laço amarelo
            f'<path d="M454 960 L498 960 C502 980 500 1000 494 1012 L444 1012 C430 1012 428 996 440 990 C448 984 452 974 454 960Z" fill="{NAVY}"/>'
            f'<path d="M502 960 L546 960 C548 974 552 984 560 990 C572 996 570 1012 556 1012 L506 1012 C500 1000 498 980 502 960Z" fill="{NAVY}"/>'
            f'<path d="M444 1012 L496 1012 L494 1020 L446 1020Z M504 1012 L556 1012 L554 1020 L506 1020Z" fill="{NAVY_D}"/>'
            f'<circle cx="470" cy="976" r="6" fill="{YEL}"/><circle cx="530" cy="976" r="6" fill="{YEL}"/>')

def torso():
    s = ''
    s += f'<path d="M482 356 L518 356 L520 412 L480 412Z" fill="{SKIN_D}"/>'                               # pescoço
    # saia evasê amarela
    s += f'<path d="M436 620 L564 620 C586 680 600 730 606 780 C560 796 440 796 394 780 C400 730 414 680 436 620Z" fill="url(#gSkirt)"/>'
    s += f'<path d="M470 640 L452 784 M530 640 L548 784 M500 640 L500 790" stroke="{YEL_D}" stroke-width="3" opacity=".6"/>'
    # blusa branca
    s += f'<path d="M446 410 L554 410 L560 640 L440 640Z" fill="#FFFFFF"/><path d="M446 410 L554 410 L560 640 L440 640Z" fill="#E6E9F2" opacity=".35"/>'
    s += f'<path d="M474 404 Q500 446 526 404Z" fill="{SKIN}"/>'
    s += f'<path d="M482 398 Q500 440 518 398" fill="none" stroke="{YEL_D}" stroke-width="2.5"/><path d="M500 428 l9 11 l-9 11 l-9 -11z" fill="{YEL}" stroke="{YEL_D}" stroke-width="2"/>'
    # blazer curto e acinturado, aberto
    s += (f'<path d="M402 430 C410 414 440 404 470 402 L488 470 L478 560 C476 590 472 620 470 652 L432 652 '
          f'C420 652 412 642 414 630 C420 600 426 580 428 560 C422 520 410 480 402 430Z" fill="url(#gBlazer)"/>')
    s += (f'<path d="M598 430 C590 414 560 404 530 402 L512 470 L522 560 C524 590 528 620 530 652 L568 652 '
          f'C580 652 588 642 586 630 C580 600 574 580 572 560 C578 520 590 480 598 430Z" fill="url(#gBlazer)"/>')
    s += f'<path d="M470 402 L492 500 L478 506 L452 450 L466 440 L446 420Z" fill="{NAVY_L}"/><path d="M530 402 L508 500 L522 506 L548 450 L534 440 L554 420Z" fill="{NAVY}"/>'
    s += f'<circle cx="540" cy="462" r="9" fill="{YEL}" stroke="#fff" stroke-width="2.5"/>'                 # broche Jamap
    s += f'<path d="M436 600 h28 M536 600 h28" stroke="{NAVY_D}" stroke-width="4" stroke-linecap="round"/>'
    return s

def left_arm(pose):  # braço esquerdo dela (lado direito de quem vê)
    if pose == 'down':
        return (f'<path d="M578 428 C604 430 618 450 620 476 L626 596 L590 600 L580 480Z" fill="url(#gSleeve)"/>'
                f'<path d="M588 592 L628 588 L630 604 L590 608Z" fill="#FFFFFF"/>'
                f'<ellipse cx="610" cy="626" rx="21" ry="24" fill="url(#gLimb)"/>'
                f'<path d="M600 640 q6 6 14 4" stroke="{SKIN_D}" stroke-width="2.5" fill="none"/>')
    px, py, pw, ph = PHONE
    return (f'<path d="M578 428 C604 430 618 450 620 476 L628 560 C630 580 614 590 600 586 L596 584 C584 580 580 570 580 558 L578 480Z" fill="url(#gSleeve)"/>'
            f'<path d="M626 548 C632 572 616 590 596 592 L580 594 C566 596 560 582 566 572 C572 562 584 560 592 558Z" fill="url(#gSleeve)"/>'
            f'<rect x="{px-5}" y="{py-5}" width="{pw+10}" height="{ph+10}" rx="10" fill="#1E1E24"/>'
            f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="7" fill="#33363F"/>'
            f'<rect x="{px+4}" y="{py+4}" width="{pw*.35}" height="{ph-8}" rx="4" fill="#fff" opacity=".1"/>'
            f'<ellipse cx="{px+pw*.55}" cy="{py+ph*.72}" rx="24" ry="20" fill="url(#gLimb)"/>'
            f'<path d="M{px+pw*.3} {py+ph*.62} q-10 6 -8 16" stroke="{SKIN_D}" stroke-width="7" stroke-linecap="round" fill="none"/>')

def body(m, b, pose):
    return hair_back() + legs() + torso() + left_arm(pose) + head_group(m, b)

def arm():
    """Braço que aponta, desenhado para BAIXO a partir do pivô (0,0); termina na mão com o indicador estendido."""
    L = ARM_LEN
    return (f'<path d="M-24 -10 C-10 -24 14 -22 24 -8 L20 {L-30} L-20 {L-30}Z" fill="url(#gSleeve)"/>'
            f'<path d="M-21 {L-36} L21 {L-36} L22 {L-22} L-22 {L-22}Z" fill="#FFFFFF"/>'
            f'<ellipse cx="0" cy="{L}" rx="20" ry="22" fill="url(#gLimb)"/>'
            f'<path d="M-7 {L+8} C-8 {L+24} -6 {L+40} -2 {L+50} C1 {L+56} 8 {L+55} 9 {L+48} C10 {L+36} 8 {L+20} 7 {L+8}Z" fill="url(#gLimb)"/>'
            f'<path d="M-12 {L+4} q8 8 18 4" stroke="{SKIN_D}" stroke-width="2.5" fill="none"/>')

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
    # prévia: em repouso, apontando com o celular e close do rosto falando
    prev = (f'<svg xmlns="http://www.w3.org/2000/svg" width="2300" height="1040" viewBox="0 0 2300 1040">{DEFS}'
            f'<rect width="2300" height="1040" fill="#EEF1F7"/>'
            f'<g filter="url(#o)"><g transform="translate({PIVOT[0]} {PIVOT[1]}) rotate(8)">{arm()}</g>{body(0, 0, "down")}</g>'
            f'<g transform="translate(700 0)"><g filter="url(#o)"><g transform="translate({PIVOT[0]} {PIVOT[1]}) rotate(140)">{arm()}</g>{body(2, 0, "phone")}</g></g>'
            f'<g transform="translate(1400 0) scale(1.9) translate(-260 -20)"><g filter="url(#o)">{hair_back()}{torso()}{head_group(1, 0)}</g></g></svg>')
    open(os.path.join(OUT, '_preview.html'), 'w').write(f'<!doctype html><html><body style="margin:0">{prev}</body></html>')
    print(len(pages), 'páginas')
