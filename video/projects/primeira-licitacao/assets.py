"""Cartões, tela de celular e ícones do vídeo "Sua primeira licitação em 4 passos" (identidade Jamap).
Gera HTML em video/assets/; depois: node video/src/render_assets.js  (gera os PNG e as caixas de destaque).
Exemplo fictício (Prefeitura de Vale Verde) com valor abaixo do limite de dispensa por valor.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
from cards import page, icon, ST, NAVY, YEL, OUT

GRN = '#1F7A45'

def chrome(url):
    return (f'<div style="display:flex;align-items:center;gap:14px;background:#EEF1F6;border-radius:26px;padding:18px 26px;margin-bottom:34px">'
            f'<span style="width:18px;height:18px;border-radius:50%;background:#FF5F57"></span><span style="width:18px;height:18px;border-radius:50%;background:#FEBC2E"></span>'
            f'<span style="width:18px;height:18px;border-radius:50%;background:#28C840"></span>'
            f'<span data-hl=url style="flex:1;background:#fff;border-radius:18px;padding:10px 20px;font-size:30px;color:#444;font-weight:600">🔒 {url}</span></div>')

def pncp():
    stats = ''.join(f'<div class=row style="flex:1;margin-top:0;padding:22px 24px"><div class=v style="font-size:34px">{v}</div><div class=s style="font-size:26px">{l}</div></div>'
                    for v, l in [('Municípios', 'prefeituras e câmaras'), ('Estados', 'secretarias'), ('União', 'órgãos federais')])
    return page(f'{chrome("pncp.gov.br")}'
                f'<div class=s style="color:{NAVY}">PORTAL NACIONAL DE</div><div class=h>Contratações<br>Públicas</div>'
                f'<div data-hl=busca class=row style="display:flex;align-items:center;gap:18px;font-size:34px;color:#9CA3AF">🔍 Buscar contratações…</div>'
                f'<div style="display:flex;gap:16px;margin-top:22px">'
                f'<div data-hl=editais class=pill style="background:{NAVY};color:#fff;font-size:32px;padding:14px 26px">Editais e avisos</div>'
                f'<div class=pill style="background:#E6EBF5;color:{NAVY};font-size:32px;padding:14px 26px">Atas</div>'
                f'<div class=pill style="background:#E6EBF5;color:{NAVY};font-size:32px;padding:14px 26px">Contratos</div></div>'
                f'<div data-hl=total style="margin-top:30px"><div class=s style="margin-bottom:14px">Compras publicadas por</div><div style="display:flex;gap:16px">{stats}</div></div>'
                f'<div class=row style="display:flex;justify-content:space-between;align-items:center"><span class=t>Acesso</span>'
                f'<span data-hl=free class=pill style="background:#E3F4EA;color:{GRN};font-size:32px">✓ Gratuito</span></div>')

def filtros():
    opts = [('Pregão eletrônico', ''), ('Concorrência', ''), ('Dispensa', 'dispensa'), ('Inexigibilidade', '')]
    o = ''.join(f'<div {"data-hl="+k if k else ""} style="padding:14px 22px;font-size:34px;font-weight:{800 if k else 600};'
                f'color:{NAVY if k else "#6B7280"};{"background:#FFF6D6;border-radius:16px" if k else ""}">{"☑ " if k else "☐ "}{t}</div>' for t, k in opts)
    return page(f'{chrome("pncp.gov.br/editais")}'
                f'<div style="display:flex;gap:16px"><div data-hl=editais class=pill style="background:{NAVY};color:#fff;font-size:32px;padding:14px 26px">Editais e avisos</div>'
                f'<div class=pill style="background:#E6EBF5;color:{NAVY};font-size:32px;padding:14px 26px">Atas</div></div>'
                f'<div class=h style="font-size:48px;margin-top:30px">Filtros</div>'
                f'<div data-hl=modal class=row style="padding:20px 24px"><div class=s>Modalidade</div>{o}</div>'
                f'<div data-hl=uf class=row style="display:flex;justify-content:space-between;align-items:center"><div><div class=s>Estado (UF)</div><div class=t>São Paulo</div></div><span style="font-size:40px;color:{NAVY}">▾</span></div>'
                f'<div data-hl=palavra class=row><div class=s>Palavra-chave</div><div class=t>papel A4<span style="color:{NAVY};font-weight:300">|</span></div></div>'
                f'<div data-hl=btn style="margin-top:26px;background:{YEL};color:{NAVY};border-radius:24px;padding:24px;text-align:center;font-size:40px;font-weight:800">Pesquisar</div>')

def plataforma():
    return page(f'<div class=s style="color:{NAVY}">AVISO DE CONTRATAÇÃO DIRETA</div><div class=h style="font-size:50px">Papel A4 · 500 caixas</div>'
                f'<div data-hl=plat class=row style="background:#F7F9FC"><div class=s>Onde enviar a proposta</div><div class=t>Plataforma indicada no aviso</div></div>'
                f'<div style="text-align:center;font-size:44px;color:{NAVY};margin:10px 0">↓</div>'
                f'<div data-hl=gov class=row style="border-color:{NAVY}"><div style="display:flex;align-items:center;gap:20px">'
                f'<div style="width:86px;height:86px;border-radius:22px;background:{NAVY};color:{YEL};font-size:46px;font-weight:900;display:flex;align-items:center;justify-content:center">C</div>'
                f'<div><div class=t style="font-size:44px">Compras.gov.br</div><div class=s>a mais usada</div></div></div></div>'
                f'<div data-hl=cad class=row><div class=t style="font-size:36px">Cadastro de fornecedor</div>'
                + ''.join(f'<div class=s style="margin-top:12px;font-size:30px">{n}  {t}</div>' for n, t in [('①', 'Entrar com a conta gov.br'), ('②', 'Informar o CNPJ da empresa'), ('③', 'Enviar a proposta no prazo')])
                + f'<div style="margin-top:22px;background:{NAVY};color:#fff;border-radius:20px;padding:20px;text-align:center;font-size:34px;font-weight:800">Entrar com gov.br</div></div>')

def ph_resultado():
    PH = '<div style="height:70px;display:flex;justify-content:space-between;align-items:center;padding:0 40px;font-weight:700;font-size:24px"><span>9:41</span><span>●●● ▮</span></div>'
    res = [('Prefeitura de Vale Verde · SP', 'Papel A4 75 g — 500 caixas (5 resmas cada)', 'R$ 59.500,00', 'item'),
           ('Câmara de Santa Rita · SP', 'Papel A4 reciclado — 120 caixas', 'R$ 15.840,00', ''),
           ('Escola Técnica · SP', 'Papel A4 e envelopes', 'R$ 8.210,00', '')]
    r = ''.join(f'<div {"data-hl="+k if k else ""} style="background:#fff;border-radius:20px;padding:22px 24px;margin:16px 0;box-shadow:0 2px 6px rgba(0,0,0,.08)">'
                f'<span style="font-size:18px;font-weight:800;color:#C98A00;background:#FFF6D6;border-radius:8px;padding:4px 10px">DISPENSA</span>'
                f'<div style="font-size:20px;color:#6b7280;font-weight:600;margin-top:10px">{o}</div><div style="font-size:26px;font-weight:800;line-height:1.25;margin:4px 0 8px">{t}</div>'
                f'<div style="font-size:28px;font-weight:900;color:{NAVY}">{v}</div></div>' for o, t, v, k in res)
    body = (PH + f'<div style="padding:6px 28px"><div style="height:66px;border-radius:33px;border:2px solid #ddd;background:#fff;display:flex;align-items:center;padding:0 24px;font-size:24px">🔍 papel A4 · SP · Dispensa</div>'
            f'<div style="font-size:22px;color:#6b7280;margin:18px 4px 0;font-weight:600">38 resultados</div>{r}</div>')
    return (f'<!doctype html><html><head><meta charset=utf-8><style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:600px;height:1260px;overflow:hidden}}'
            f'body{{font-family:Poppins,Inter,sans-serif;color:#1f2933;background:#F4F5F7}}</style></head><body>{body}</body></html>')

ICONS = {
    'ic_search': icon(f'<circle cx="114" cy="114" r="46" {ST}/><path d="M148 148 L188 188" {ST}/>'),
    'ic_clock': icon(f'<circle cx="128" cy="128" r="64" {ST}/><path d="M128 92 V130 L154 146" {ST}/>'),
    'ic_pin': icon(f'<path d="M128 196 C96 156 76 130 76 104 a52 52 0 0 1 104 0 c0 26 -20 52 -52 92z" {ST}/><circle cx="128" cy="104" r="18" {ST}/>'),
    'ic_money': icon(f'<rect x="58" y="84" width="140" height="88" rx="14" {ST}/><circle cx="128" cy="128" r="20" {ST}/>'),
    'ic_chat': icon(f'<path d="M66 82 h124 q14 0 14 14 v62 q0 14 -14 14 h-70 l-34 28 v-28 h-20 q-14 0 -14 -14 v-62 q0 -14 14 -14z" {ST}/>'
                    f'<text x="128" y="148" text-anchor="middle" font-family="Poppins" font-weight="900" font-size="48" fill="{YEL}">EU</text>'),
}

if __name__ == '__main__':
    for n, f in [('card_pncp', pncp), ('card_filtros', filtros), ('card_plataforma', plataforma), ('ph_resultado', ph_resultado)]:
        open(os.path.join(OUT, n + '.html'), 'w').write(f())
    for n, h in ICONS.items(): open(os.path.join(OUT, n + '.html'), 'w').write(h)
    print('ok')
