"""Roteiro visual sincronizado à narração (tempos em segundos, vindos da transcrição palavra a palavra).
Tipos de evento:
 label(t0,t1,texto[,big,y])  hl(t0,t1,alvo)  mark(t0,t1,alvo)  point(t0,t1,alvo)  tap(t,alvo)
 write(t0,dur,texto,x,y,tam,cor)  strike(t0,dur,x0,y,x1,cor)  stamp(t,texto,cx,cy,tam,cor)
 prop(t0,t1,nome,x,y,anim)
"""
R, B, G, K = 'red', 'navy', 'navy_mk', 'text'   # navy_mk = azul com marca-texto amarelo

SCENES = [
 # 1 GANCHO — quarto
 dict(t0=0.00, t1=2.64, kind='room', ev=[
   ('label', 0.0, 2.64, 'VENDER PARA O GOVERNO VALE A PENA?', dict(y=230, maxw=620, big=True)),
   ('prop', 1.6, 2.64, 'question', 850, 700, 'pop'),
 ]),
 # 2 CONTEXTO — portal de oportunidades
 dict(t0=2.64, t1=11.67, kind='desk', screen='scr_portal', ev=[
   ('label', 3.0, 5.4, 'VOCÊ SABIA?'),
   ('label', 6.0, 8.3, 'GRANDES OPORTUNIDADES'),
   ('hl', 6.3, 9.0, 'card'), ('point', 6.4, 7.6, 'card'),
   ('mark', 7.5, 9.4, 'valor'), ('point', 7.6, 9.2, 'valor'),
   ('label', 9.6, 11.67, 'NUNCA TENTOU?'),
   ('hl', 9.8, 11.67, 'total'), ('point', 9.9, 11.4, 'total'),
 ]),
 # 3 — o que muita gente pensa (celular)
 dict(t0=11.67, t1=17.11, kind='phone', screen='ph_search', ev=[
   ('hl', 12.2, 13.9, 'busca'), ('point', 12.3, 13.6, 'busca'),
   ('label', 13.5, 17.11, 'O QUE MUITA GENTE PENSA'),
   ('hl', 14.2, 15.3, 'c0'), ('hl', 15.3, 16.3, 'c1'), ('hl', 16.3, 17.11, 'c2'),
   ('point', 14.3, 16.9, 'c1'),
 ]),
 # 4 — quadro: os mitos
 dict(t0=17.11, t1=28.57, kind='board', ev=[
   ('write', 17.5, 1.3, 'O QUE MUITA GENTE ACHA:', 95, 370, 70, K),
   ('write', 20.1, 1.0, '- COMPLICADO DEMAIS', 95, 500, 84, R),
   ('write', 22.3, 1.2, '- ESTRUTURA GIGANTE', 95, 620, 84, R),
   ('write', 24.4, 1.4, '- BUROCRACIA SEM FIM', 95, 740, 84, R),
   ('label', 27.1, 28.57, 'ISSO É UM MITO'),
   ('strike', 27.3, .25, 85, 548, 760, B), ('strike', 27.5, .25, 85, 668, 760, B), ('strike', 27.7, .25, 85, 788, 800, B),
   ('stamp', 27.9, 'MITO!', 430, 1010, 190, B),
 ]),
 # 5 — todos os portes (rua: todas as empresas na mesma escala, 45 px/m)
 dict(t0=28.57, t1=37.79, kind='street', ev=[
   ('label', 29.0, 32.8, 'EMPRESAS DE TODOS OS PORTES'),
   ('hl', 30.3, 31.3, ('rect', 600, 170, 360, 1080)), ('point', 30.3, 31.2, ('rect', 600, 600, 360, 200)),
   ('hl', 31.3, 32.4, ('rect', 240, 980, 315, 270)), ('point', 31.3, 32.3, ('rect', 240, 980, 315, 270)),
   ('label', 33.2, 35.3, 'PEQUENOS NEGÓCIOS TAMBÉM'),
   ('hl', 32.4, 35.4, ('rect', 34, 1086, 174, 164)), ('point', 32.5, 35.2, ('rect', 34, 1086, 174, 164)),
   ('label', 35.5, 37.79, 'BENEFÍCIOS PREVISTOS EM LEI'),
 ]),
 # 6 — atenção (quarto)
 dict(t0=37.79, t1=42.29, kind='room', ev=[
   ('label', 38.0, 40.2, 'MAS ATENÇÃO!'),
   ('prop', 38.1, 42.29, 'warn', 360, 760, 'pop'),
   ('label', 40.2, 42.29, 'NÃO É TUDO SIMPLES'),
 ]),
 # 7 — a complexidade do edital (monitor)
 dict(t0=42.29, t1=50.79, kind='desk', screen='scr_edital', zoom=1.45, ev=[
   ('label', 42.6, 44.4, 'EDITAIS COMPLEXOS'), ('hl', 43.0, 44.4, 'ed_obj'), ('point', 43.1, 44.3, 'ed_obj'),
   ('label', 44.5, 46.0, 'EXIGÊNCIAS TÉCNICAS'), ('hl', 44.5, 46.0, 'ed_tec'), ('point', 44.6, 45.9, 'ed_tec'),
   ('label', 46.1, 46.95, 'PRAZOS'), ('hl', 46.1, 46.95, 'ed_prazo'), ('point', 46.1, 46.9, 'ed_prazo'),
   ('label', 47.0, 48.4, 'FORMAÇÃO DE PREÇOS'), ('hl', 47.0, 48.4, 'ed_preco'), ('point', 47.0, 48.3, 'ed_preco'),
   ('label', 48.5, 50.79, 'RISCOS'), ('hl', 48.5, 50.79, 'ed_risco'), ('mark', 48.6, 50.79, 'ed_risco'), ('point', 48.6, 50.5, 'ed_risco'),
 ]),
 # 8 — quadro: lucro que vira prejuízo
 dict(t0=50.79, t1=58.37, kind='board', ev=[
   ('write', 51.0, .6, 'EXEMPLO:', 95, 370, 64, K),
   ('write', 51.6, 1.0, 'GANHOU: R$ 100.000', 95, 480, 84, B),
   ('label', 52.6, 55.0, 'SEM CALCULAR OS CUSTOS'),
   ('write', 53.2, 1.3, 'CUSTO REAL: R$ 112.000', 95, 600, 84, R),
   ('strike', 54.7, .4, 95, 728, 900, K),
   ('write', 56.2, 1.2, 'PREJUÍZO = -R$ 12.000', 95, 770, 104, R),
   ('label', 57.3, 58.37, 'PREJUÍZO!'),
 ]),
 # 9 — não é só dar um lance (celular)
 dict(t0=58.37, t1=65.91, kind='phone', screen='ph_lance', ev=[
   ('label', 60.2, 62.4, 'ESSE MERCADO EXIGE MAIS'),
   ('label', 62.6, 64.75, 'NÃO É SÓ ACHAR UM EDITAL…'),
   ('hl', 63.4, 64.8, 'lance'), ('point', 63.5, 64.7, 'lance'),
   ('label', 64.8, 65.91, '…E DAR UM LANCE'),
   ('hl', 64.8, 65.91, 'btn'), ('tap', 65.1, 'btn'), ('point', 64.85, 65.8, 'btn'),
 ]),
 # 10 — quadro: o que é preciso
 dict(t0=65.91, t1=75.97, kind='board', ev=[
   ('write', 66.2, .6, 'É PRECISO:', 95, 370, 80, K),
   ('write', 66.7, .8, '1. INTELIGÊNCIA', 95, 490, 88, B),
   ('write', 67.8, 1.0, '> BOAS OPORTUNIDADES', 150, 595, 58, K),
   ('write', 70.2, .9, '2. CONHECIMENTO', 95, 690, 88, B),
   ('write', 71.2, .9, '> ANALISAR OS RISCOS', 150, 795, 58, K),
   ('write', 72.8, .8, '3. ESTRATÉGIA', 95, 890, 88, B),
   ('write', 73.8, 1.1, '> CADA PROCESSO', 150, 995, 58, K),
 ]),
 # 11 — planejamento financeiro (monitor)
 dict(t0=75.97, t1=81.38, kind='desk', screen='scr_finance', ev=[
   ('label', 76.3, 78.7, 'PLANEJAMENTO FINANCEIRO'), ('hl', 77.1, 78.8, 'chart'), ('point', 77.2, 78.6, 'chart'),
   ('label', 78.7, 81.38, 'CONTRATOS COM SEGURANÇA'), ('hl', 78.9, 81.38, 'giro'), ('mark', 79.4, 81.38, 'margem'), ('point', 79.0, 81.0, 'giro'),
 ]),
 # 12 — a boa notícia (quarto)
 dict(t0=81.38, t1=87.15, kind='room', ev=[
   ('label', 81.7, 83.5, 'A BOA NOTÍCIA'),
   ('label', 83.6, 87.15, 'SUA EMPRESA NÃO PRECISA ESTAR SOZINHA'),
 ]),
 # 13 — tecnologia + IA + especialistas (monitor)
 dict(t0=87.15, t1=96.63, kind='desk', screen='scr_ai', ev=[
   ('label', 87.9, 89.1, 'TECNOLOGIA'),
   ('label', 89.1, 90.75, 'INTELIGÊNCIA ARTIFICIAL'), ('hl', 89.1, 90.8, 'ia'), ('point', 89.2, 90.7, 'ia'),
   ('label', 90.8, 92.9, 'ESPECIALISTAS'), ('hl', 90.8, 92.9, 'esp'), ('point', 90.9, 92.8, 'esp'),
   ('label', 93.2, 96.63, 'MAIS ESTRATÉGICO E ORGANIZADO'), ('hl', 93.4, 96.63, 'lista'), ('point', 93.5, 95.5, 'lista'),
 ]),
 # 14 — canal de crescimento (celular)
 dict(t0=96.63, t1=101.44, kind='phone', screen='ph_growth', ev=[
   ('label', 96.9, 99.1, 'MERCADO PÚBLICO'),
   ('label', 99.2, 101.44, 'CANAL DE CRESCIMENTO'),
   ('hl', 98.4, 101.44, 'chart'), ('point', 99.3, 101.2, 'chart'),
 ]),
 # 15 — quadro: a questão certa
 dict(t0=101.44, t1=108.65, kind='board', ev=[
   ('write', 101.8, .9, 'A QUESTÃO NÃO É:', 95, 370, 70, K),
   ('write', 102.9, 1.4, '"SERÁ QUE VALE A PENA?"', 95, 480, 82, B),
   ('strike', 104.6, .35, 90, 528, 930, R),
   ('write', 105.5, .7, 'É SABER:', 95, 640, 70, K),
   ('write', 106.2, 1.0, 'COMO FAZER', 95, 740, 120, G),
   ('write', 107.3, 1.1, 'DO JEITO CERTO!', 95, 880, 120, G),
 ]),
 # 16 — CTA (quarto)
 dict(t0=108.65, t1=122.52, kind='room', ev=[
   ('label', 108.9, 113.6, 'QUER DESCOBRIR COMO?'),
   ('label', 114.0, 122.52, 'CONHEÇA A JAMAP', dict(big=True, y=170, style='yellow')),
   ('prop', 115.3, 122.52, 'cta_btn', 540, 520, 'popc'), ('tap', 116.0, ('rect', 440, 490, 260, 60)),
   ('label', 118.0, 122.52, 'MAIS ESTRATÉGIA E INTELIGÊNCIA', dict(y=300)),
 ]),
]
