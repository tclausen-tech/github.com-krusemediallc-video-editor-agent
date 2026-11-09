"""Gera HTML/SVG dos cenários (1080x1920)."""
import os
OUT=os.path.join(os.path.dirname(__file__),'..','assets')
def page(w,h,body,css=''):
    return f"""<!doctype html><html><head><meta charset=utf-8><style>
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:{w}px;height:{h}px;overflow:hidden;font-family:Inter,sans-serif}} {css}</style></head><body>{body}</body></html>"""
def plant(x,y,s=1):
    leaves=''.join(f'<ellipse cx="{x+dx*s}" cy="{y+dy*s}" rx="{22*s}" ry="{9*s}" transform="rotate({r} {x+dx*s} {y+dy*s})" fill="{c}"/>' for dx,dy,r,c in [(-30,-20,-30,'#3E8E4F'),(30,-25,30,'#4FA35F'),(-10,-50,-70,'#3E8E4F'),(15,-55,70,'#5DB36C'),(-38,10,-10,'#4FA35F'),(40,8,15,'#3E8E4F'),(0,-75,90,'#4FA35F')])
    return leaves+f'<path d="M{x-28*s} {y+10*s} h{56*s} l{-8*s} {50*s} h{-40*s} z" fill="#E8E1D6" stroke="#CFC6B8" stroke-width="2"/>'
SVG=lambda w,h,inner:f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F4ECE2"/><stop offset="1" stop-color="#E7DACA"/></linearGradient><linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D2A273"/><stop offset="1" stop-color="#B9875A"/></linearGradient><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5AA9F0"/><stop offset="1" stop-color="#BFE3FF"/></linearGradient><radialGradient id="vig" cx=".5" cy=".45" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".18"/></radialGradient><filter id="sh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-opacity=".22"/></filter></defs>{inner}<rect width="{w}" height="{h}" fill="url(#vig)"/></svg>'

def room():
    s='<rect width="1080" height="1920" fill="url(#wall)"/>'
    # window + curtains
    s+='<rect x="700" y="160" width="330" height="760" rx="6" fill="#DDEFFC"/><rect x="700" y="160" width="330" height="760" rx="6" fill="none" stroke="#FFFFFF" stroke-width="16"/><line x1="865" y1="160" x2="865" y2="920" stroke="#fff" stroke-width="12"/>'
    s+='<path d="M660 130 q40 400 0 860 h90 q-30 -430 0 -860z" fill="#FBF8F3" filter="url(#sh)"/><path d="M1080 130 q-40 400 0 860 h-80 q30 -430 0 -860z" fill="#FBF8F3" filter="url(#sh)"/><rect x="640" y="118" width="440" height="14" rx="7" fill="#2B2B2B"/>'
    # corkboard
    s+='<rect x="70" y="330" width="420" height="300" rx="8" fill="#C8955F" stroke="#8C6239" stroke-width="10" filter="url(#sh)"/>'
    for x,y,c,r in [(100,360,'#FFF59D',-4),(210,380,'#FFFFFF',3),(320,350,'#B3E5FC',-2),(120,490,'#F8BBD0',5),(260,500,'#FFFFFF',-3),(380,470,'#C8E6C9',4)]:
        s+=f'<rect x="{x}" y="{y}" width="85" height="95" fill="{c}" transform="rotate({r} {x+40} {y+45})"/><circle cx="{x+42}" cy="{y+8}" r="6" fill="#E53935"/>'
    # shelf + plants
    s+='<rect x="60" y="250" width="440" height="16" rx="4" fill="#A7774C"/>'+plant(130,200,1.1)+plant(420,205,0.9)+'<rect x="230" y="178" width="26" height="72" fill="#4A6FA5"/><rect x="258" y="190" width="22" height="60" fill="#E07A5F"/><rect x="282" y="184" width="24" height="66" fill="#81B29A"/>'
    # desk
    s+='<rect x="0" y="1060" width="1080" height="34" fill="url(#wood)" filter="url(#sh)"/>'
    s+='<rect x="40" y="1094" width="250" height="560" fill="#FFFFFF" stroke="#E2DED8" stroke-width="3"/>'+''.join(f'<rect x="52" y="{1110+i*135}" width="226" height="118" rx="6" fill="#FAFAFA" stroke="#E2DED8" stroke-width="3"/><rect x="135" y="{1160+i*135}" width="60" height="10" rx="5" fill="#222"/>' for i in range(4))
    s+='<rect x="880" y="1094" width="30" height="560" fill="#B98B5E"/>'
    # monitor imac
    s+='<rect x="300" y="700" width="460" height="300" rx="16" fill="#1E1E1E" filter="url(#sh)"/><rect x="316" y="716" width="428" height="250" rx="6" fill="#2F3A4A"/><rect x="316" y="716" width="428" height="250" rx="6" fill="url(#sky)" opacity=".35"/><path d="M500 1000 h60 l12 60 h-84z" fill="#C9CCD1"/>'
    s+='<rect x="580" y="1030" width="160" height="22" rx="8" fill="#E5E7EB"/><circle cx="790" cy="1030" r="26" fill="#F2F2F2" stroke="#D9D9D9" stroke-width="3"/>'+plant(820,980,0.75)
    # floor + rug
    s+='<rect x="0" y="1654" width="1080" height="266" fill="#D9CDBD"/><ellipse cx="560" cy="1800" rx="620" ry="120" fill="#EFE7DC"/>'
    return SVG(1080,1920,s)

def board():
    s='<rect width="1080" height="1920" fill="#E6E4E8"/><rect y="0" width="1080" height="1350" fill="url(#wall)" opacity=".25"/>'
    s+='<rect x="0" y="1350" width="1080" height="570" fill="#B98552"/>'
    import random; random.seed(3)
    for i,y in enumerate(range(1350,1920,64)):
        s+=f'<line x1="0" y1="{y}" x2="1080" y2="{y}" stroke="#94643A" stroke-width="4"/>'
        off=random.randint(0,300)
        for x in range(off,1080,380): s+=f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+64}" stroke="#94643A" stroke-width="4"/>'
        s+=f'<rect x="0" y="{y+6}" width="1080" height="10" fill="#C99561" opacity=".5"/>'
    s+='<rect x="0" y="1336" width="1080" height="18" fill="#F4F4F4"/>'
    s+='<rect x="30" y="300" width="1020" height="960" rx="10" fill="#BFC3C9" filter="url(#sh)"/><rect x="48" y="318" width="984" height="924" fill="#FFFFFF"/><rect x="48" y="318" width="984" height="924" fill="#EEF1F6" opacity=".55"/><rect x="48" y="318" width="984" height="300" fill="#FFFFFF" opacity=".5"/><rect x="140" y="1260" width="800" height="22" rx="4" fill="#A8ADB4"/>'
    return SVG(1080,1920,s)

def desk():
    s='<rect width="1080" height="1920" fill="#EDEBEE"/><rect width="1080" height="1250" fill="url(#wall)" opacity=".3"/>'
    s+='<rect x="0" y="1230" width="1080" height="690" fill="url(#wood)"/><rect x="0" y="1230" width="1080" height="10" fill="#E2B88B"/>'
    s+='<path d="M480 1020 h120 l30 210 h-180z" fill="#2A2A2A"/><ellipse cx="540" cy="1240" rx="200" ry="26" fill="#222" filter="url(#sh)"/>'
    s+='<rect x="20" y="300" width="1040" height="740" rx="22" fill="#141414" filter="url(#sh)"/><rect x="36" y="316" width="1008" height="680" rx="6" fill="#fff"/>'
    s+='<g transform="rotate(-5 120 1180)"><rect x="40" y="1090" width="170" height="160" fill="#FFE96B" filter="url(#sh)"/><path d="M60 1140 h120 M60 1170 h100 M60 1200 h110" stroke="#7A6A00" stroke-width="5" stroke-linecap="round"/></g>'
    s+='<rect x="120" y="1420" width="840" height="300" rx="20" fill="#F4F4F4" filter="url(#sh)"/>'
    for r in range(4):
        for c in range(12): s+=f'<rect x="{150+c*67}" y="{1445+r*66}" width="56" height="54" rx="8" fill="#FFFFFF" stroke="#DADADA" stroke-width="2"/>'
    s+='<rect x="0" y="1760" width="1080" height="160" fill="#2B2B2B" opacity=".85"/>'
    return SVG(1080,1920,s)

def sala():
    s='<rect width="1080" height="1920" fill="#F3EEE8"/>'
    for x in [80,420,760]: s+=f'<rect x="{x}" y="120" width="260" height="900" rx="6" fill="none" stroke="#E2D9CE" stroke-width="10"/>'
    s+='<rect x="0" y="1180" width="1080" height="740" fill="#E8DFD3"/><path d="M-40 1300 q0 -160 160 -160 h840 q160 0 160 160 v320 h-1160z" fill="#F7F3EE" filter="url(#sh)"/><rect x="60" y="1220" width="320" height="260" rx="40" fill="#EFE8DE"/><rect x="420" y="1220" width="320" height="260" rx="40" fill="#EFE8DE"/>'
    s+='<ellipse cx="900" cy="1060" rx="80" ry="110" fill="#E9DFD2"/>'+plant(940,1080,1.3)
    return SVG(1080,1920,s)

def building():
    s='<rect width="1080" height="1920" fill="url(#sky)"/>'
    for cx,cy,sc in [(180,240,1.2),(820,180,1),(600,380,.8)]:
        s+=''.join(f'<circle cx="{cx+dx*sc}" cy="{cy+dy*sc}" r="{r*sc}" fill="#fff" opacity=".95"/>' for dx,dy,r in [(0,0,55),(60,-20,65),(125,5,50),(60,25,55)])
    s+='<rect x="0" y="1180" width="1080" height="740" fill="#9AA3AB"/><rect x="0" y="1180" width="1080" height="70" fill="#C9CED3"/>'
    for x in range(0,1080,160): s+=f'<rect x="{x+40}" y="1560" width="90" height="16" fill="#fff" opacity=".8"/>'
    # building
    s+='<rect x="120" y="700" width="840" height="480" fill="#F6E7B5" filter="url(#sh)"/><path d="M90 700 L540 470 L990 700z" fill="#F0D98C" stroke="#E2C46A" stroke-width="8"/><circle cx="540" cy="610" r="44" fill="#fff" stroke="#E2C46A" stroke-width="8"/>'
    s+='<rect x="100" y="690" width="880" height="26" fill="#E9D18A"/>'
    for x in range(170,950,110): s+=f'<rect x="{x}" y="740" width="44" height="400" fill="#FFFDF5" stroke="#E6D5A0" stroke-width="4"/>'
    s+='<rect x="460" y="960" width="160" height="220" rx="80" fill="#6B4B2A"/>'
    for x in [230,340,700,810]: s+=f'<rect x="{x-10}" y="800" width="60" height="90" fill="#7DB3D8" stroke="#fff" stroke-width="5"/>'
    s+='<rect x="100" y="1150" width="880" height="40" fill="#E0C987"/><rect x="60" y="1190" width="960" height="30" fill="#D9C07A"/>'
    s+='<line x1="540" y1="470" x2="540" y2="330" stroke="#555" stroke-width="8"/><rect x="540" y="330" width="120" height="76" fill="#009C3B"/><path d="M600 338 L652 368 L600 398 L548 368z" fill="#FFDF00"/><circle cx="600" cy="368" r="17" fill="#002776"/>'
    return SVG(1080,1920,s)

for name,fn in [('bg_room',room),('bg_board',board),('bg_desk',desk),('bg_sala',sala),('bg_building',building)]:
    open(os.path.join(OUT,name+'.html'),'w').write(page(1080,1920,fn()))
print('ok')
