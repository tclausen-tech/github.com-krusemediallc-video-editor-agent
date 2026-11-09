"""Roteiro visual (motion clean) sincronizado à narração. Tempos em segundos.

Tipos de cena:
  title  — frase grande centralizada: ('line', t, texto, estilo)  estilo: 'navy' | 'yellow' | 'small'; ('icon', t, nome)
  ui     — cartão de interface (card_*): hl / mark / point
  phone  — personagem segura o celular; a tela aparece no painel de zoom: hl / mark / point / tap
  list   — cartão com itens: ('head', t, texto) ('item', t, ícone, texto, sub) ('strike', t, i) ('stamp', t, texto)
  calc   — cartão de conta: ('tag', t, texto) ('row', t, rótulo, valor, cor) ('divider', t) ('result', t, rótulo, valor, cor)
  portes — cartão com empresas na mesma escala: ('biz', t, nome) + hl/point em 'kiosk' | 'store' | 'tower'; ('badge', t, ícone, texto)
Eventos comuns: ('label', t0, t1, texto[, opções]), ('hl', t0, t1, alvo), ('mark', t0, t1, alvo), ('point', t0, t1, alvo), ('tap', t, alvo)
"""
SCENES = [
 dict(t0=0.00, t1=2.64, kind='title', ev=[
   ('icon', 0.15, 'ic_question'),
   ('line', 0.1, 'VENDER PARA', 'navy'), ('line', 0.5, 'O GOVERNO', 'navy'), ('line', 1.55, 'VALE A PENA?', 'yellow'),
 ]),
 dict(t0=2.64, t1=11.67, kind='ui', card='card_portal', ev=[
   ('label', 3.0, 5.4, 'VOCÊ SABIA?'),
   ('label', 6.0, 8.3, 'GRANDES OPORTUNIDADES'),
   ('hl', 6.3, 9.3, 'card'), ('point', 6.4, 7.6, 'card'),
   ('mark', 7.5, 9.4, 'valor'), ('point', 7.6, 9.2, 'valor'),
   ('label', 9.6, 11.67, 'NUNCA TENTOU?'),
   ('hl', 9.8, 11.67, 'total'), ('point', 9.9, 11.4, 'total'),
 ]),
 dict(t0=11.67, t1=17.11, kind='phone', screen='ph_search', ev=[
   ('hl', 12.2, 13.9, 'busca'), ('point', 12.3, 13.6, 'busca'),
   ('label', 13.5, 17.11, 'O QUE MUITA GENTE PENSA'),
   ('hl', 14.2, 15.3, 'c0'), ('hl', 15.3, 16.3, 'c1'), ('hl', 16.3, 17.11, 'c2'),
   ('point', 14.3, 16.9, 'c1'),
 ]),
 dict(t0=17.11, t1=28.57, kind='list', ev=[
   ('head', 17.5, 'O que muita gente acha:'),
   ('item', 20.1, 'ic_x', 'Complicado demais', ''),
   ('item', 22.3, 'ic_x', 'Estrutura gigante', ''),
   ('item', 24.4, 'ic_x', 'Burocracia sem fim', ''),
   ('point', 20.2, 21.6, ('item', 0)), ('point', 22.4, 23.8, ('item', 1)), ('point', 24.5, 26.4, ('item', 2)),
   ('label', 27.1, 28.57, 'ISSO É UM MITO'),
   ('strike', 27.3, 0), ('strike', 27.5, 1), ('strike', 27.7, 2),
   ('stamp', 27.9, 'MITO!'),
 ]),
 dict(t0=28.57, t1=37.79, kind='portes', ev=[
   ('label', 29.0, 32.8, 'EMPRESAS DE TODOS OS PORTES'),
   ('biz', 29.4, 'tower'), ('biz', 29.8, 'store'), ('biz', 30.2, 'kiosk'),
   ('hl', 30.6, 31.4, 'tower'), ('point', 30.6, 31.3, 'tower'),
   ('hl', 31.4, 32.4, 'store'), ('point', 31.4, 32.3, 'store'),
   ('hl', 32.4, 35.4, 'kiosk'), ('point', 32.5, 35.2, 'kiosk'),
   ('label', 33.2, 35.3, 'PEQUENOS NEGÓCIOS TAMBÉM'),
   ('badge', 35.5, 'ic_scale', 'Benefícios previstos em lei'),
   ('label', 35.5, 37.79, 'BENEFÍCIOS PREVISTOS EM LEI'),
 ]),
 dict(t0=37.79, t1=42.29, kind='title', ev=[
   ('icon', 37.9, 'ic_alert'),
   ('line', 38.0, 'MAS ATENÇÃO:', 'navy'), ('line', 39.6, 'NÃO É TUDO', 'navy'), ('line', 41.1, 'SIMPLES', 'yellow'),
 ]),
 dict(t0=42.29, t1=50.79, kind='ui', card='card_edital', ev=[
   ('label', 42.6, 44.4, 'EDITAIS COMPLEXOS'), ('hl', 43.0, 44.4, 'ed_obj'), ('point', 43.1, 44.3, 'ed_obj'),
   ('label', 44.5, 46.0, 'EXIGÊNCIAS TÉCNICAS'), ('hl', 44.5, 46.0, 'ed_tec'), ('point', 44.6, 45.9, 'ed_tec'),
   ('label', 46.1, 46.95, 'PRAZOS'), ('hl', 46.1, 46.95, 'ed_prazo'), ('point', 46.1, 46.9, 'ed_prazo'),
   ('label', 47.0, 48.4, 'FORMAÇÃO DE PREÇOS'), ('hl', 47.0, 48.4, 'ed_preco'), ('point', 47.0, 48.3, 'ed_preco'),
   ('label', 48.5, 50.79, 'RISCOS'), ('hl', 48.5, 50.79, 'ed_risco'), ('mark', 48.6, 50.79, 'ed_risco'), ('point', 48.6, 50.5, 'ed_risco'),
 ]),
 dict(t0=50.79, t1=58.37, kind='calc', ev=[
   ('tag', 51.0, 'EXEMPLO'),
   ('row', 51.6, 'Valor ganho na licitação', 100000, 'navy'),
   ('label', 52.6, 55.0, 'SEM CALCULAR OS CUSTOS'),
   ('row', 53.2, 'Custo real de execução', 112000, 'red'),
   ('divider', 54.7),
   ('result', 56.2, 'Resultado', -12000, 'red'),
   ('point', 51.7, 52.9, ('row', 0)), ('point', 53.3, 54.6, ('row', 1)), ('point', 56.3, 58.0, ('row', 2)),
   ('label', 57.3, 58.37, 'PREJUÍZO!'),
 ]),
 dict(t0=58.37, t1=65.91, kind='phone', screen='ph_lance', ev=[
   ('label', 60.2, 62.4, 'ESSE MERCADO EXIGE MAIS'),
   ('label', 62.6, 64.75, 'NÃO É SÓ ACHAR UM EDITAL…'),
   ('hl', 63.4, 64.8, 'lance'), ('point', 63.5, 64.7, 'lance'),
   ('label', 64.8, 65.91, '…E DAR UM LANCE'),
   ('hl', 64.8, 65.91, 'btn'), ('tap', 65.1, 'btn'), ('point', 64.85, 65.8, 'btn'),
 ]),
 dict(t0=65.91, t1=75.97, kind='list', ev=[
   ('head', 66.2, 'É preciso:'),
   ('item', 66.7, 'ic_bulb', 'Inteligência', 'para achar boas oportunidades'),
   ('item', 70.2, 'ic_book', 'Conhecimento', 'para analisar os riscos'),
   ('item', 72.8, 'ic_target', 'Estratégia', 'para cada processo'),
   ('point', 66.8, 69.6, ('item', 0)), ('point', 70.3, 72.4, ('item', 1)), ('point', 72.9, 75.4, ('item', 2)),
 ]),
 dict(t0=75.97, t1=81.38, kind='ui', card='card_finance', ev=[
   ('label', 76.3, 78.7, 'PLANEJAMENTO FINANCEIRO'), ('hl', 77.1, 78.8, 'chart'), ('point', 77.2, 78.6, 'chart'),
   ('label', 78.7, 81.38, 'CONTRATOS COM SEGURANÇA'), ('hl', 78.9, 81.38, 'giro'), ('mark', 79.4, 81.38, 'margem'), ('point', 79.0, 81.0, 'giro'),
 ]),
 dict(t0=81.38, t1=87.15, kind='title', ev=[
   ('icon', 81.5, 'ic_people'),
   ('line', 81.7, 'A BOA NOTÍCIA:', 'small'), ('line', 83.1, 'SUA EMPRESA', 'navy'), ('line', 84.3, 'NÃO ESTÁ', 'navy'), ('line', 86.3, 'SOZINHA', 'yellow'),
 ]),
 dict(t0=87.15, t1=96.63, kind='ui', card='card_ai', ev=[
   ('label', 87.9, 89.1, 'TECNOLOGIA'),
   ('label', 89.1, 90.75, 'INTELIGÊNCIA ARTIFICIAL'), ('hl', 89.1, 90.8, 'ia'), ('point', 89.2, 90.7, 'ia'),
   ('label', 90.8, 92.9, 'ESPECIALISTAS'), ('hl', 90.8, 92.9, 'esp'), ('point', 90.9, 92.8, 'esp'),
   ('label', 93.2, 96.63, 'MAIS ESTRATÉGICO E ORGANIZADO'), ('hl', 93.4, 96.63, 'lista'), ('point', 93.5, 95.5, 'lista'),
 ]),
 dict(t0=96.63, t1=101.44, kind='phone', screen='ph_growth', ev=[
   ('label', 96.9, 99.1, 'MERCADO PÚBLICO'),
   ('label', 99.2, 101.44, 'CANAL DE CRESCIMENTO'),
   ('hl', 98.4, 101.44, 'chart'), ('point', 99.3, 101.2, 'chart'),
 ]),
 dict(t0=101.44, t1=108.65, kind='list', ev=[
   ('head', 101.8, 'A questão não é:'),
   ('item', 102.9, 'ic_question', '“Vale a pena?”', ''),
   ('strike', 104.6, 0),
   ('item', 105.5, 'ic_check', 'É saber como fazer', 'do jeito certo'),
   ('point', 103.0, 104.4, ('item', 0)), ('point', 105.6, 108.3, ('item', 1)),
 ]),
 dict(t0=108.65, t1=122.52, kind='title', ev=[
   ('line', 108.9, 'QUER DESCOBRIR', 'navy'), ('line', 109.8, 'COMO?', 'navy'),
   ('clear', 113.8),
   ('line', 114.0, 'CONHEÇA A', 'navy'), ('line', 114.5, 'JAMAP', 'yellow'),
   ('button', 115.4, 'DÊ O PRIMEIRO PASSO'), ('tap', 116.0, 'button'),
   ('line', 118.0, 'mais estratégia e inteligência', 'small'),
 ]),
]
