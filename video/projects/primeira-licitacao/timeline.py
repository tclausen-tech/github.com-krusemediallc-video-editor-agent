"""Roteiro visual de "Sua primeira licitação em 4 passos" (Jamap). Tempos em segundos, sincronizados com words.json.
Tipos de cena e eventos: ver docstring de video/src/timeline.py.
"""
SCENES = [
 dict(t0=0.00, t1=5.25, kind='title', ev=[
   ('icon', 0.1, 'ic_search'),
   ('line', 0.25, 'SUA PRIMEIRA', 'navy'), ('line', 0.75, 'LICITAÇÃO', 'navy'), ('line', 1.75, 'AINDA HOJE', 'yellow'),
   ('clear', 3.05),
   ('line', 3.2, 'EU TE MOSTRO', 'small'), ('line', 3.95, 'EM 4 PASSOS', 'yellow'),
 ]),
 dict(t0=5.25, t1=15.35, kind='ui', card='card_pncp', ev=[
   ('label', 5.4, 7.1, 'PASSO 1'),
   ('label', 7.15, 12.1, 'PNCP.GOV.BR'),
   ('hl', 7.2, 9.2, 'url'), ('point', 7.25, 9.1, 'url'),
   ('mark', 9.3, 11.9, 'total'),
   ('label', 12.15, 15.35, 'GRATUITO'),
   ('hl', 12.3, 13.6, 'free'), ('point', 12.35, 13.5, 'free'),
   ('hl', 13.7, 15.35, 'total'), ('point', 13.75, 15.2, 'total'),
 ]),
 dict(t0=15.35, t1=27.45, kind='ui', card='card_filtros', ev=[
   ('label', 15.55, 17.15, 'PASSO 2'),
   ('label', 17.2, 18.25, 'EDITAIS'),
   ('hl', 17.2, 18.25, 'editais'), ('point', 17.25, 18.2, 'editais'), ('tap', 17.4, 'editais'),
   ('label', 18.3, 21.75, 'MODALIDADE: DISPENSA'),
   ('hl', 18.35, 19.75, 'modal'), ('point', 18.4, 19.7, 'modal'),
   ('hl', 19.75, 24.9, 'dispensa'), ('point', 19.8, 24.6, 'dispensa'), ('tap', 20.5, 'dispensa'),
   ('label', 21.8, 24.95, 'COMPRAS MENORES, MENOS EXIGÊNCIAS'),
   ('label', 25.0, 27.45, 'IDEAL PRA COMEÇAR'),
 ]),
 dict(t0=27.45, t1=35.35, kind='ui', card='card_filtros', ev=[
   ('label', 27.65, 28.9, 'PASSO 3'),
   ('label', 28.95, 30.45, 'SEU ESTADO'),
   ('hl', 28.95, 30.45, 'uf'), ('point', 29.0, 30.4, 'uf'),
   ('label', 30.5, 32.2, 'O QUE VOCÊ VENDE'),
   ('hl', 30.5, 34.4, 'palavra'), ('point', 30.55, 34.3, 'palavra'), ('mark', 33.4, 34.4, 'palavra'),
   ('label', 32.25, 35.35, 'EX.: PAPEL A4'),
   ('hl', 34.45, 35.35, 'btn'), ('tap', 34.6, 'btn'), ('point', 34.45, 35.3, 'btn'),
 ]),
 dict(t0=35.35, t1=39.55, kind='phone', screen='ph_resultado', ev=[
   ('label', 35.45, 36.5, 'OLHA SÓ'),
   ('hl', 36.55, 39.55, 'item'), ('point', 36.6, 39.4, 'item'),
   ('label', 37.85, 39.55, '500 CAIXAS'),
   ('tap', 38.9, 'item'),
 ]),
 dict(t0=39.55, t1=45.95, kind='list', ev=[
   ('head', 39.75, 'Abra o aviso e confira:'),
   ('label', 40.9, 45.95, '3 COISAS'),
   ('item', 42.35, 'ic_clock', 'Prazo', 'até quando enviar'),
   ('item', 43.35, 'ic_pin', 'Local', 'onde entregar'),
   ('item', 44.4, 'ic_money', 'Valor estimado', 'R$ 59.500 no exemplo'),
   ('point', 42.4, 43.3, ('item', 0)), ('point', 43.4, 44.35, ('item', 1)), ('point', 44.45, 45.8, ('item', 2)),
 ]),
 dict(t0=45.95, t1=56.25, kind='ui', card='card_plataforma', ev=[
   ('label', 46.05, 47.3, 'PASSO 4'),
   ('label', 47.35, 49.7, 'ENVIE A PROPOSTA'),
   ('hl', 48.7, 51.6, 'plat'), ('point', 48.75, 51.5, 'plat'), ('mark', 49.8, 51.6, 'plat'),
   ('label', 49.75, 53.35, 'PLATAFORMA DO AVISO'),
   ('hl', 52.2, 54.6, 'gov'), ('point', 52.25, 54.5, 'gov'),
   ('label', 53.4, 56.25, 'COMPRAS.GOV.BR'),
   ('hl', 54.6, 56.25, 'cad'), ('point', 54.65, 56.1, 'cad'),
 ]),
 dict(t0=56.25, t1=59.4, kind='title', ev=[
   ('icon', 56.35, 'ic_question'),
   ('line', 56.45, 'ACHOU VÁRIAS?', 'navy'), ('line', 57.3, 'QUAL VALE', 'navy'), ('line', 57.9, 'A PENA?', 'yellow'),
 ]),
 dict(t0=59.4, t1=66.2, kind='ui', card='card_ai', ev=[
   ('label', 59.55, 61.4, 'A JAMAP ANALISA'),
   ('label', 61.45, 62.8, 'INTELIGÊNCIA ARTIFICIAL'), ('hl', 61.45, 62.8, 'ia'), ('point', 61.5, 62.75, 'ia'),
   ('label', 62.8, 64.0, 'ESPECIALISTAS'), ('hl', 62.8, 64.0, 'esp'), ('point', 62.85, 63.95, 'esp'),
   ('label', 64.0, 66.2, 'FOCO NO QUE DÁ LUCRO'), ('hl', 64.0, 66.2, 'lista'), ('point', 64.05, 66.0, 'lista'),
 ]),
 dict(t0=66.2, t1=71.3, kind='title', ev=[
   ('icon', 66.3, 'ic_chat'),
   ('line', 66.35, 'COMENTA', 'navy'), ('line', 66.9, '"EU"', 'yellow'),
   ('line', 68.0, 'te mando o passo a passo', 'small'),
   ('button', 68.7, 'JAMAP'),
 ]),
]
