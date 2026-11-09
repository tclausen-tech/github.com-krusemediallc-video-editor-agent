"""Telas (mockups de UI) para monitor (1512x1020) e celular (600x1260). Elementos com data-hl viram alvos de destaque."""
import os
OUT=os.path.join(os.path.dirname(__file__),'..','assets')
CSS="""*{margin:0;padding:0;box-sizing:border-box}body{font-family:Inter,sans-serif;color:#1f2933;background:#fff;overflow:hidden}
.chrome{height:64px;background:#ECEDEF;display:flex;align-items:center;gap:12px;padding:0 22px;border-bottom:1px solid #d5d7db}
.dot{width:16px;height:16px;border-radius:50%}.url{flex:1;margin-left:24px;height:40px;background:#fff;border-radius:20px;display:flex;align-items:center;padding:0 20px;font-size:20px;color:#555}
.bar{height:12px;border-radius:6px;background:#E3E6EA;margin:9px 0}
.btn{display:inline-block;background:#1E6630;color:#fff;font-weight:700;border-radius:10px;padding:12px 22px}
.tag{display:inline-block;font-size:17px;font-weight:700;border-radius:8px;padding:5px 12px}
"""
def chrome(url): return f'<div class=chrome><div class=dot style="background:#FF5F57"></div><div class=dot style="background:#FEBC2E"></div><div class=dot style="background:#28C840"></div><div class=url>🔒&nbsp; {url}</div></div>'
def page(w,h,body,extra=''): return f'<!doctype html><html><head><meta charset=utf-8><style>html,body{{width:{w}px;height:{h}px}}{CSS}{extra}</style></head><body>{body}</body></html>'
def bars(n,widths=(100,92,97,70)): return ''.join(f'<div class=bar style="width:{widths[i%len(widths)]}%"></div>' for i in range(n))

def portal():
    cards=[('Prefeitura Municipal · SP','Aquisição de notebooks para escolas','R$ 284.500,00','Aberta','5 dias'),
           ('Secretaria de Saúde · MG','Material de limpeza e higiene','R$ 96.320,00','Aberta','8 dias'),
           ('Câmara Municipal · PR','Serviço de manutenção predial','R$ 152.000,00','Aberta','3 dias'),
           ('Instituto Federal · GO','Mobiliário para laboratório','R$ 61.780,00','Aberta','12 dias')]
    c=''.join(f'''<div {'data-hl=card' if i==0 else ''} style="border:2px solid #E3E6EA;border-radius:16px;padding:22px 26px;margin-bottom:18px;display:flex;justify-content:space-between;align-items:center">
<div><div style="font-size:19px;color:#6b7280;font-weight:600">{o}</div><div style="font-size:27px;font-weight:800;margin:6px 0 10px">{t}</div><span class=tag style="background:#E7F5EC;color:#1E6630">● {s}</span> <span class=tag style="background:#FFF4E5;color:#B45309">Encerra em {d}</span></div>
<div style="text-align:right"><div style="font-size:17px;color:#6b7280">Valor estimado</div><div {'data-hl=valor' if i==0 else ''} style="font-size:32px;font-weight:800;color:#1E6630">{v}</div></div></div>''' for i,(o,t,v,s,d) in enumerate(cards))
    body=chrome('portal-de-licitacoes / oportunidades')+f'''<div style="padding:30px 44px"><div style="display:flex;justify-content:space-between;align-items:center"><div style="font-size:40px;font-weight:800">Oportunidades abertas</div><div data-hl=total style="font-size:22px;background:#1E6630;color:#fff;border-radius:30px;padding:10px 22px;font-weight:700">2.418 licitações hoje</div></div>
<div style="display:flex;gap:12px;margin:20px 0 24px"><div style="flex:1;height:54px;border:2px solid #D1D5DB;border-radius:12px;display:flex;align-items:center;padding:0 18px;font-size:21px;color:#9CA3AF">🔍 Buscar por produto ou serviço…</div><div class=btn style="font-size:21px">Filtrar</div></div>{c}</div>'''
    return page(1512,1020,body)

def edital():
    secs=[('ed_obj','1. DO OBJETO',3),('ed_tec','7. DA QUALIFICAÇÃO TÉCNICA',4),('ed_prazo','9. DOS PRAZOS DE ENTREGA',3),('ed_preco','11. DA PROPOSTA E FORMAÇÃO DE PREÇOS',4),('ed_risco','15. DAS SANÇÕES E PENALIDADES',3)]
    s=''.join(f'<div data-hl={k} style="padding:8px 10px;margin:4px -10px"><div style="font-size:20px;font-weight:800;margin-bottom:4px">{t}</div>{bars(n)}</div>' for k,t,n in secs)
    body=chrome('edital_pregao_045-2026.pdf')+f'''<div style="background:#525659;height:956px;display:flex;justify-content:center;padding-top:22px">
<div data-hl=doc style="width:900px;background:#fff;padding:40px 60px;box-shadow:0 6px 20px rgba(0,0,0,.4)"><div style="text-align:center;font-size:17px;color:#555;font-weight:600">PREFEITURA MUNICIPAL · SECRETARIA DE ADMINISTRAÇÃO</div>
<div style="text-align:center;font-size:30px;font-weight:900;margin:8px 0 2px">EDITAL DE PREGÃO ELETRÔNICO Nº 045/2026</div><div style="text-align:center;font-size:17px;color:#777;margin-bottom:14px">Processo administrativo 1.209/2026 · 87 páginas</div>{s}</div>
<div style="position:absolute;right:40px;top:90px;background:#fff;border-radius:10px;padding:8px 16px;font-size:18px;font-weight:700">Página 1 de 87</div></div>'''
    return page(1512,1020,body)

def finance():
    vals=[(-38,'Mês 1'),(-22,'Mês 2'),(10,'Mês 3'),(34,'Mês 4'),(52,'Mês 5'),(70,'Mês 6')]
    b=''.join(f'<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:330px;position:relative"><div style="position:absolute;top:{165 - max(v,0)*2.2}px;width:70%;height:{abs(v)*2.2}px;background:{"#D02830" if v<0 else "#2DB34A"};border-radius:6px"></div><div style="position:absolute;bottom:-34px;font-size:18px;color:#6b7280">{m}</div></div>' for v,m in vals)
    body=chrome('gestao-de-contratos / planejamento-financeiro')+f'''<div style="padding:30px 44px"><div style="font-size:38px;font-weight:800;margin-bottom:22px">Planejamento financeiro do contrato</div>
<div style="display:flex;gap:20px">{''.join(f'<div {h} style="flex:1;border:2px solid #E3E6EA;border-radius:16px;padding:20px 24px"><div style="font-size:19px;color:#6b7280;font-weight:600">{a}</div><div style="font-size:36px;font-weight:800;color:{c}">{v}</div></div>' for a,v,c,h in [('Receita do contrato','R$ 284.500','#2058C8',''),('Custos previstos','R$ 231.900','#D02830',''),('Margem líquida','R$ 52.600','#1E6630','data-hl=margem'),('Capital de giro','R$ 60.000','#B45309','data-hl=giro')])}</div>
<div data-hl=chart style="margin-top:26px;border:2px solid #E3E6EA;border-radius:16px;padding:22px 28px 48px"><div style="font-size:22px;font-weight:800;margin-bottom:6px">Fluxo de caixa acumulado</div><div style="display:flex;gap:10px;border-bottom:3px solid #9CA3AF;position:relative">{b}<div style="position:absolute;left:0;right:0;top:165px;border-top:2px dashed #9CA3AF"></div></div></div></div>'''
    return page(1512,1020,body)

def ai():
    rows=[('Notebooks para escolas · SP','96%','#1E6630','Baixo'),('Material de limpeza · MG','91%','#1E6630','Baixo'),('Manutenção predial · PR','74%','#B45309','Médio'),('Mobiliário laboratório · GO','68%','#B45309','Médio')]
    r=''.join(f'<div style="display:flex;align-items:center;gap:18px;padding:14px 0;border-bottom:1px solid #EEE"><div style="flex:1;font-size:22px;font-weight:700">{a}</div><div style="width:200px;height:14px;background:#EEE;border-radius:7px"><div style="width:{p};height:100%;background:{c};border-radius:7px"></div></div><div style="width:70px;font-weight:800;font-size:22px;color:{c}">{p}</div><span class=tag style="background:#F3F4F6;color:{c}">Risco {k}</span></div>' for a,p,c,k in rows)
    body=chrome('painel-de-oportunidades / inteligencia')+f'''<div style="display:flex;height:956px"><div style="width:230px;background:#11251A;color:#cfe8d6;padding:30px 24px;font-size:20px;line-height:2.4"><div style="color:#fff;font-weight:800;font-size:24px;margin-bottom:16px">◆ Painel</div>Oportunidades<br>Editais<br>Riscos<br>Propostas<br>Contratos</div>
<div style="flex:1;padding:30px 36px"><div data-hl=ia style="background:linear-gradient(90deg,#1E6630,#2DB34A);color:#fff;border-radius:18px;padding:24px 28px;display:flex;align-items:center;gap:22px"><div style="font-size:52px">✦</div><div><div style="font-size:20px;opacity:.9;font-weight:600">INTELIGÊNCIA ARTIFICIAL</div><div style="font-size:34px;font-weight:800">37 oportunidades compatíveis com sua empresa</div></div></div>
<div data-hl=lista style="margin-top:22px;border:2px solid #E3E6EA;border-radius:16px;padding:12px 26px"><div style="font-size:20px;color:#6b7280;font-weight:700;padding:8px 0">COMPATIBILIDADE · ANÁLISE DE RISCO</div>{r}</div>
<div data-hl=esp style="margin-top:22px;display:flex;gap:16px;align-items:flex-start"><div style="width:62px;height:62px;border-radius:50%;background:#2058C8;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:24px">ES</div><div style="background:#EEF3FB;border-radius:4px 18px 18px 18px;padding:16px 22px;font-size:22px;max-width:760px"><b>Especialista</b><br>Analisei o edital: documentação ok, prazo de entrega viável. Sugiro margem mínima de 18%.</div></div></div></div>'''
    return page(1512,1020,body)

PH="""<div style="height:70px;display:flex;justify-content:space-between;align-items:center;padding:0 40px;font-weight:700;font-size:24px"><span>9:41</span><span>●●● ▮</span></div>"""
def ph_search():
    res=[('“Vender pro governo é muita burocracia, desisti.”','👎 132'),('“Isso é só pra empresa grande.”','👎 98'),('“Precisa de uma estrutura enorme pra participar.”','👎 76'),('“Muito complicado, nem tento.”','👎 54')]
    r=''.join(f'<div {"data-hl=c%d"%i} style="background:#fff;border-radius:18px;padding:22px 24px;margin:16px 0;box-shadow:0 2px 6px rgba(0,0,0,.08)"><div style="display:flex;gap:12px;align-items:center;margin-bottom:10px"><div style="width:44px;height:44px;border-radius:50%;background:{c}"></div><div style="font-weight:700;font-size:21px;color:#555">usuário{i+1}</div></div><div style="font-size:26px;font-weight:600;line-height:1.3">{t}</div><div style="color:#888;font-size:20px;margin-top:8px">{l}</div></div>' for i,((t,l),c) in enumerate(zip(res,['#F6AD55','#63B3ED','#B794F4','#68D391'])))
    body=PH+f'<div style="padding:10px 30px"><div data-hl=busca style="height:74px;border-radius:37px;border:2px solid #ddd;display:flex;align-items:center;padding:0 26px;font-size:25px">🔍 vender para o governo é difícil?</div><div style="font-size:22px;color:#777;margin:22px 4px 0">O que as pessoas dizem</div>{r}</div>'
    return page(600,1260,body,'body{background:#F4F5F7}')
def ph_lance():
    body=PH+'''<div style="padding:10px 34px"><div style="font-size:22px;color:#6b7280;font-weight:600">Sala de disputa · Pregão 045/2026</div><div style="font-size:34px;font-weight:800;margin:8px 0 20px">Item 1 · Notebooks (40 un.)</div>
<div data-hl=lance style="background:#F3F4F6;border-radius:18px;padding:22px"><div style="font-size:21px;color:#6b7280">Melhor lance atual</div><div style="font-size:52px;font-weight:900;color:#D02830">R$ 268.900</div><div style="font-size:20px;color:#6b7280">⏱ 00:01:42 para encerrar</div></div>
<div style="margin-top:22px;font-size:21px;color:#6b7280">Seu lance</div><div style="height:80px;border:3px solid #2058C8;border-radius:16px;display:flex;align-items:center;padding:0 22px;font-size:34px;font-weight:800;margin-top:8px">R$ 259.000</div>
<div data-hl=btn style="margin-top:26px;height:96px;border-radius:20px;background:#1E6630;color:#fff;font-size:34px;font-weight:900;display:flex;align-items:center;justify-content:center">DAR LANCE</div>
<div style="margin-top:28px">'''+''.join(f'<div style="display:flex;justify-content:space-between;padding:14px 0;border-bottom:1px solid #eee;font-size:22px"><span>Fornecedor {i}</span><b>R$ {v}</b></div>' for i,v in [(7,'268.900'),(3,'271.400'),(12,'275.000'),(5,'279.990')])+'</div></div>'
    return page(600,1260,body)
def ph_growth():
    vals=[(30,0),(34,0),(36,8),(38,16),(40,28),(42,44)]
    b=''.join(f'<div style="flex:1;display:flex;flex-direction:column;justify-content:flex-end;height:520px;gap:0"><div style="height:{g*6}px;background:#2DB34A;border-radius:8px 8px 0 0"></div><div style="height:{p*6}px;background:#2058C8;border-radius:{0 if g else 8}px {0 if g else 8}px 0 0"></div><div style="text-align:center;font-size:18px;color:#888;margin-top:8px">T{i+1}</div></div>' for i,(p,g) in enumerate(vals))
    body=PH+f'''<div style="padding:10px 34px"><div style="font-size:22px;color:#6b7280;font-weight:600">Faturamento da empresa</div><div data-hl=num style="font-size:50px;font-weight:900;color:#1E6630;line-height:1.1">Novo canal de receita</div><div style="font-size:21px;color:#6b7280;margin-bottom:24px">ilustração · por trimestre</div>
<div data-hl=chart style="display:flex;gap:14px;align-items:flex-end">{b}</div>
<div style="margin-top:30px;font-size:22px"><span style="display:inline-block;width:20px;height:20px;background:#2058C8;border-radius:4px"></span> Clientes privados &nbsp; <span style="display:inline-block;width:20px;height:20px;background:#2DB34A;border-radius:4px"></span> <b>Mercado público</b></div></div>'''
    return page(600,1260,body)
for n,f in [('scr_portal',portal),('scr_edital',edital),('scr_finance',finance),('scr_ai',ai),('ph_search',ph_search),('ph_lance',ph_lance),('ph_growth',ph_growth)]:
    open(os.path.join(OUT,n+'.html'),'w').write(f())
print('ok')
