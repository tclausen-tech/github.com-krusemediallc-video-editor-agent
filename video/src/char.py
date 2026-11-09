"""Gera variações do personagem: base, piscada, boca aberta (3 níveis), com contorno branco tipo adesivo."""
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import sys
import os; W=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))+'/'
base=Image.open(W+'char_rembg.png').convert('RGBA')
orig=Image.open(W+'in/char.webp').convert('RGB')
skin=orig.getpixel((720,975)); print('skin',skin)
EYES=[(780,856),(1220,856)]
def blink(im,amt=1.0):
    im=im.copy()
    lay=Image.new('RGBA',im.size,(0,0,0,0)); ld=ImageDraw.Draw(lay)
    for cx,cy in EYES:
        top=orig.getpixel((cx,cy-110)); bot=orig.getpixel((cx,cy+118))
        for y in range(cy-105,cy+111):
            t=(y-(cy-105))/216
            c=tuple(int(top[i]*(1-t)+bot[i]*t) for i in range(3))
            ld.line((cx-120,y,cx+120,y),fill=c+(255,))
        # soft crease shadow + lash line (closed eye)
        ld.arc((cx-104,cy-70,cx+104,cy+38),12,168,fill=(150,95,75,140),width=16)
        ld.arc((cx-100,cy-62,cx+100,cy+30),14,166,fill=(28,18,14,255),width=10)
    m=Image.new('L',im.size,0); md=ImageDraw.Draw(m)
    for cx,cy in EYES: md.ellipse((cx-118,cy-96,cx+118,cy+104),fill=255)
    m=m.filter(ImageFilter.GaussianBlur(3))
    lay.putalpha(ImageChops.multiply(lay.split()[3],m))
    im.alpha_composite(lay); return im
def mouth(im,h):
    if h<=0: return im
    im=im.copy(); lay=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
    cx,cy=1002,1168; w=170+h*1.2
    box=(cx-w/2,cy-h*0.45,cx+w/2,cy+h)
    d.ellipse(box,fill=(74,24,26,255))
    d.ellipse((cx-w*0.32,cy+h*0.25,cx+w*0.32,cy+h*1.15),fill=(190,84,80,255))
    d.rounded_rectangle((cx-w*0.33,cy-h*0.45,cx+w*0.33,cy-h*0.45+max(5,h*0.24)),radius=6,fill=(236,228,218,255))
    m=Image.new('L',im.size,0); ImageDraw.Draw(m).ellipse(box,fill=255)
    m=m.filter(ImageFilter.GaussianBlur(2.5))
    lay=lay.filter(ImageFilter.GaussianBlur(1.2))
    lay.putalpha(ImageChops.multiply(lay.split()[3],m))
    im.alpha_composite(lay); return im
    im=im.copy(); lay=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
    cx,cy=1002,1172; w=200+h
    d.chord((cx-w//2,cy-h*0.35,cx+w//2,cy+h),0,180,fill=(70,22,24,255))
    d.rectangle((cx-w//2,cy-h*0.35,cx+w//2,cy+1),fill=(70,22,24,255))
    # teeth
    d.rectangle((cx-w//2+30,cy-h*0.35,cx+w//2-30,cy-h*0.35+max(6,h*0.22)),fill=(245,240,235,255))
    # tongue
    d.chord((cx-w//3,cy+h*0.35,cx+w//3,cy+h*1.25),180,360,fill=(196,82,78,255))
    m=Image.new('L',im.size,0); ImageDraw.Draw(m).chord((cx-w//2,cy-h*0.35-40,cx+w//2,cy+h),0,180,fill=255)
    ImageDraw.Draw(m).rectangle((cx-w//2,cy-h*0.35,cx+w//2,cy+1),fill=255)
    lay.putalpha(ImageChops.multiply(lay.split()[3],m.filter(ImageFilter.GaussianBlur(3))))
    im.alpha_composite(lay); return im
def sticker(im,r=14):
    a=im.split()[3]
    a2=a.filter(ImageFilter.MaxFilter(2*r+1)).filter(ImageFilter.GaussianBlur(1.5))
    out=Image.new('RGBA',im.size,(255,255,255,0)); out.putalpha(a2)
    out.alpha_composite(im); return out
out={}
for b in [0,1]:
  for mo in [0,1,2,3]:
    im=base
    if b: im=blink(im)
    im=mouth(im,[0,28,48,68][mo])
    im=sticker(im)
    im=im.resize((1000,1000),Image.LANCZOS)
    im.save(W+f'char_b{b}_m{mo}.png')
