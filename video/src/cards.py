"""Cartões de interface (formato retrato, 2x) e ícones em SVG para o estilo motion clean."""
import os
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets')
NAVY, YEL, GRAY, TXT = '#001D52', '#FEBF00', '#DDE0DF', '#333333'
CSS = f"""*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1100px;height:1560px;overflow:hidden}}
body{{font-family:Poppins,Inter,sans-serif;color:{TXT};background:#fff;padding:56px 56px}}
.h{{font-size:58px;font-weight:800;color:{NAVY};line-height:1.1}}.sub{{font-size:34px;color:#6B7280;font-weight:600;margin-top:10px}}
.row{{border:3px solid #E6E9EF;border-radius:30px;padding:30px 34px;margin-top:26px}}
.t{{font-size:40px;font-weight:700;color:{NAVY};line-height:1.2}}.s{{font-size:30px;color:#6B7280;font-weight:600}}
.v{{font-size:48px;font-weight:800;color:{NAVY}}}.pill{{display:inline-block;border-radius:30px;padding:8px 22px;font-size:28px;font-weight:700}}
.bar{{height:20px;border-radius:10px;background:#E9ECF2;margin:14px 0}}"""
def page(body, extra=''): return f'<!doctype html><html><head><meta charset=utf-8><style>{CSS}{extra}</style></head><body>{body}</body></html>'

def portal():
    rows = [('Prefeitura · SP', 'Notebooks para escolas', 'R$ 284.500', 'card', 'valor'),
            ('Saúde · MG', 'Material de limpeza', 'R$ 96.320', '', ''),
            ('Câmara · PR', 'Manutenção predial', 'R$ 152.000', '', '')]
    r = ''.join(f'<div class=row {f"data-hl={h}" if h else ""}><div class=s>{o}</div><div class=t>{t}</div>'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-top:14px"><span class=pill style="background:#E6EBF5;color:{NAVY}">● Aberta</span>'
                f'<span class=v {f"data-hl={v}" if v else ""}>{val}</span></div></div>' for o, t, val, h, v in rows)
    return page(f'<div class=h>Oportunidades abertas</div><div data-hl=total class=pill style="background:{NAVY};color:#fff;margin-top:20px;font-size:32px">2.418 licitações hoje</div>{r}')

def edital():
    secs = [('ed_obj', '1. Do objeto', 2), ('ed_tec', '7. Qualificação técnica', 2), ('ed_prazo', '9. Prazos de entrega', 2),
            ('ed_preco', '11. Formação de preços', 2), ('ed_risco', '15. Sanções e penalidades', 2)]
    s = ''.join(f'<div data-hl={k} style="padding:16px 20px;margin:10px -20px;border-radius:20px"><div class=t style="font-size:38px">{t}</div>'
                + ''.join(f'<div class=bar style="width:{w}%"></div>' for w in (96, 78)[:n]) + '</div>' for k, t, n in secs)
    return page(f'<div class=s style="color:{NAVY}">PREFEITURA MUNICIPAL</div><div class=h style="font-size:52px">Edital de Pregão<br>nº 045/2026</div>'
                f'<div class=sub>87 páginas · PDF</div><div style="height:4px;background:{YEL};width:160px;margin:26px 0 14px;border-radius:2px"></div>{s}')

def finance():
    vals = [-38, -22, 10, 34, 52, 70]
    b = ''.join(f'<div style="flex:1;position:relative;height:420px"><div style="position:absolute;left:12%;width:76%;top:{210 - max(v, 0) * 2.8}px;height:{abs(v) * 2.8}px;'
                f'background:{"#D0312D" if v < 0 else NAVY};border-radius:12px"></div></div>' for v in vals)
    k = ''.join(f'<div class=row {h} style="flex:1;margin-top:0;padding:24px 26px"><div class=s>{a}</div><div class=v style="color:{c};font-size:42px">{v}</div></div>'
                for a, v, c, h in [('Receita', 'R$ 284 mil', NAVY, ''), ('Custos', 'R$ 232 mil', '#D0312D', ''), ('Margem', 'R$ 52 mil', NAVY, 'data-hl=margem'), ('Capital de giro', 'R$ 60 mil', '#B07D00', 'data-hl=giro')])
    return page(f'<div class=h>Planejamento<br>financeiro</div><div class=sub>Contrato · 6 meses</div>'
                f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:30px">{k}</div>'
                f'<div data-hl=chart class=row><div class=t style="font-size:34px">Fluxo de caixa</div><div style="display:flex;gap:10px;position:relative;margin-top:16px">{b}'
                f'<div style="position:absolute;left:0;right:0;top:210px;border-top:3px dashed #9CA3AF"></div></div></div>')

def ai():
    rows = [('Notebooks · SP', 96), ('Limpeza · MG', 91), ('Manutenção · PR', 74)]
    r = ''.join(f'<div style="margin:18px 0"><div style="display:flex;justify-content:space-between" class=t><span style="font-size:34px">{a}</span><span style="font-size:34px">{p}%</span></div>'
                f'<div class=bar style="height:22px"><div style="width:{p}%;height:100%;background:{NAVY if p > 80 else YEL};border-radius:11px"></div></div></div>' for a, p in rows)
    return page(f'<div data-hl=ia style="background:linear-gradient(135deg,{NAVY},#0B3A8A);color:#fff;border-radius:34px;padding:40px">'
                f'<div style="font-size:30px;font-weight:700;color:{YEL}">✦ INTELIGÊNCIA ARTIFICIAL</div><div style="font-size:52px;font-weight:800;line-height:1.15;margin-top:8px">37 oportunidades compatíveis</div></div>'
                f'<div data-hl=lista class=row><div class=s>COMPATIBILIDADE</div>{r}</div>'
                f'<div data-hl=esp class=row style="display:flex;gap:24px;align-items:flex-start"><div style="min-width:90px;height:90px;border-radius:50%;background:{YEL};color:{NAVY};font-weight:800;font-size:36px;display:flex;align-items:center;justify-content:center">ES</div>'
                f'<div><div class=t style="font-size:36px">Especialista</div><div class=s style="font-size:30px;line-height:1.35">Edital analisado: prazo viável, margem mínima de 18%.</div></div></div>')

# ---------- ícones (256x256, fundo transparente) ----------
def icon(inner, bg=NAVY):
    return (f'<!doctype html><html><body style="margin:0;background:transparent"><svg width="256" height="256" viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">'
            f'<circle cx="128" cy="128" r="120" fill="{bg}"/>{inner}</svg></body></html>')
ST = 'fill="none" stroke="#fff" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"'
ICONS = {
    'ic_x': icon(f'<path d="M88 88 L168 168 M168 88 L88 168" {ST}/>', '#D0312D'),
    'ic_check': icon(f'<path d="M78 132 L114 166 L180 92" {ST}/>'),
    'ic_alert': icon(f'<path d="M128 70 V146" {ST}/><circle cx="128" cy="184" r="11" fill="{NAVY}"/>'.replace('#fff', NAVY), YEL),
    'ic_bulb': icon(f'<path d="M100 160 q-30 -24 -30 -58 a58 58 0 0 1 116 0 q0 34 -30 58 z" {ST}/><path d="M104 186 h48 M110 206 h36" {ST}/>'),
    'ic_book': icon(f'<path d="M66 80 h48 q14 0 14 14 v96 q0 -12 -14 -12 h-48z M190 80 h-48 q-14 0 -14 14 v96 q0 -12 14 -12 h48z" {ST}/>'),
    'ic_target': icon(f'<circle cx="128" cy="128" r="62" {ST}/><circle cx="128" cy="128" r="30" {ST}/><circle cx="128" cy="128" r="8" fill="{YEL}"/>'),
    'ic_scale': icon(f'<path d="M128 66 V194 M88 194 h80 M70 92 h116" {ST}/><path d="M70 92 l-22 50 h44z M186 92 l-22 50 h44z" {ST}/>'),
    'ic_people': icon(f'<circle cx="100" cy="102" r="24" {ST}/><circle cx="162" cy="102" r="24" {ST}/><path d="M56 186 q4 -46 44 -46 q40 0 44 46 M124 186 q4 -46 38 -46 q36 0 40 46" {ST}/>'),
    'ic_question': icon(f'<path d="M98 100 q0 -34 32 -34 q32 0 32 30 q0 22 -32 34 v20" {ST}/><circle cx="130" cy="190" r="11" fill="#fff"/>', YEL).replace(ST, ST.replace('#fff', NAVY)).replace('fill="#fff"/>', f'fill="{NAVY}"/>'),
}
if __name__ == '__main__':
    for n, f in [('card_portal', portal), ('card_edital', edital), ('card_finance', finance), ('card_ai', ai)]:
        open(os.path.join(OUT, n + '.html'), 'w').write(f())
    for n, h in ICONS.items(): open(os.path.join(OUT, n + '.html'), 'w').write(h)
    print('ok')
