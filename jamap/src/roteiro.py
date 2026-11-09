"""Roteiro de cenas do vídeo "Vender para o governo vale a pena?" (Jamap).

Formato do modelo.md (seções 1–8): cortes secos, foto real de fundo com
push-in, personagem fixa no canto inferior direito, etiqueta no terço superior,
legenda em blocos de 1–3 palavras e quadro branco com escrita animada a cada
~15–20 s para "traduzir" a ideia. Os tempos vêm de in/words.json (Scribe).
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORDS = json.load(open(os.path.join(ROOT, "in", "words.json")))


def w(i, d=0.0):
    """Início da palavra i (ver índice em in/words.json), com deslocamento opcional."""
    return round(WORDS[i]["s"] + d, 3)


# Estilos de etiqueta: n = azul-marinho, r = alerta vermelho, y = CTA amarelo, hook = gancho 3 linhas.
# Etiqueta: (entrada, saída|None=próxima/fim da cena, texto, estilo, linha 0..2)
# Quadro: itens ("write", t, texto, cor, tamanho) / ("sub", t, linha, texto) / ("strike", t, linha)
#         / ("hl", t, linha) / ("stamp", t, texto). "linha" = índice entre os "write" da cena.
NAVY, RED, GRAY = "navy", "red", "gray"

SCENES = [
    # 1. GANCHO — escritório, promessa por escrito no frame 0
    dict(kind="photo", img="escritorio", t0=0.0, focus=(0.42, 0.42),
         labels=[(0.0, None, "VENDER PARA O\nGOVERNO VALE\n*A PENA?*", "hook", 0)]),
    # 2. CONTEXTO — a empresa que nunca tentou
    dict(kind="photo", img="loja", t0=2.70, focus=(0.30, 0.55),
         labels=[(w(10), None, "SUA EMPRESA", "n", 0),
                 (w(16), None, "GRANDES OPORTUNIDADES", "n", 0),
                 (w(22), None, "NUNCA TENTOU?", "r", 0)]),
    # 3. QUADRO — a ideia sobre licitações
    dict(kind="board", t0=11.70, items=[
        ("write", w(31), "O MOTIVO?", GRAY, 62),
        ("write", w(34), "UMA IDEIA SOBRE", NAVY, 78),
        ("write", w(41, -0.15), "LICITAÇÕES", NAVY, 112),
        ("hl", w(41, 0.75), 2),
    ]),
    # 4. O MITO — papelada
    dict(kind="photo", img="papelada", t0=17.20, focus=(0.5, 0.5),
         labels=[(w(42), None, "MUITA GENTE ACREDITA...", "n", 0),
                 (w(51), None, "COMPLICADO DEMAIS", "r", 0)]),
    # 5. QUADRO — estrutura e burocracia riscadas: MITO!
    dict(kind="board", t0=21.70, items=[
        ("write", 21.85, "O QUE DIZEM:", GRAY, 62),
        ("write", w(55), "ESTRUTURA GIGANTESCA", NAVY, 74),
        ("write", w(59), "BUROCRACIA SEM FIM", NAVY, 74),
        ("strike", w(61), 1),
        ("strike", w(62, 0.05), 2),
        ("stamp", w(65), "MITO!"),
    ]),
    # 6. QUEM PODE — Esplanada
    dict(kind="photo", img="ministerio", t0=28.60, focus=(0.55, 0.45),
         labels=[(w(66), None, "EMPRESAS DE TODOS OS PORTES", "n", 0),
                 (w(70), None, "PODEM PARTICIPAR", "n", 0)]),
    # 7. PEQUENOS NEGÓCIOS
    dict(kind="photo", img="lojista", t0=33.00, focus=(0.47, 0.5),
         labels=[(w(75), None, "PEQUENOS NEGÓCIOS", "n", 0),
                 (w(80), None, "BENEFÍCIOS PREVISTOS EM LEI", "n", 0)]),
    # 8. ATENÇÃO
    dict(kind="photo", img="assinatura", t0=37.90, focus=(0.55, 0.5),
         labels=[(w(85), None, "ATENÇÃO!", "r", 0),
                 (w(87), None, "NÃO É TUDO SIMPLES", "n", 0)]),
    # 9. QUADRO — o que precisa ser avaliado
    dict(kind="board", t0=42.30, items=[
        ("write", w(94), "• EDITAIS COMPLEXOS", NAVY, 70),
        ("write", w(96), "• EXIGÊNCIAS TÉCNICAS", NAVY, 70),
        ("write", w(98), "• PRAZOS", NAVY, 70),
        ("write", w(99), "• FORMAÇÃO DE PREÇOS", NAVY, 70),
        ("write", w(103), "• RISCOS", RED, 70),
    ]),
    # 10. CUSTOS — calculadora
    dict(kind="photo", img="calculadora", t0=50.80, focus=(0.5, 0.5),
         labels=[(w(109), None, "GANHAR A LICITAÇÃO...", "n", 0),
                 (w(112), None, "SEM CALCULAR OS CUSTOS", "r", 0)]),
    # 11. QUADRO — oportunidade vira prejuízo
    dict(kind="board", t0=54.85, items=[
        ("write", w(118), "UMA OPORTUNIDADE", NAVY, 80),
        ("write", w(121, -0.2), "PODE VIRAR", GRAY, 62),
        ("write", w(122), "PREJUÍZO", RED, 120),
    ]),
    # 12. NÃO BASTA DAR UM LANCE — martelo
    dict(kind="photo", img="martelo", t0=58.40, focus=(0.45, 0.5),
         labels=[(w(128), None, "ENTRAR NESSE MERCADO", "n", 0),
                 (w(131), None, "EXIGE MAIS DO QUE...", "n", 0),
                 (w(136), None, "ENCONTRAR UM EDITAL", "n", 0),
                 (w(140), None, "E DAR UM LANCE", "n", 0)]),
    # 13. QUADRO — os três pilares
    dict(kind="board", t0=65.95, items=[
        ("write", w(143), "É PRECISO:", GRAY, 58),
        ("write", w(145), "INTELIGÊNCIA", NAVY, 76),
        ("sub", w(147), 1, "p/ achar boas oportunidades"),
        ("hl", w(148), 1),
        ("write", w(150), "CONHECIMENTO", NAVY, 76),
        ("sub", w(152), 2, "p/ analisar os riscos"),
        ("hl", w(153), 2),
        ("write", w(156), "ESTRATÉGIA", NAVY, 76),
        ("sub", w(158), 3, "p/ cada processo"),
        ("hl", w(159), 3),
    ]),
    # 14. PLANEJAMENTO FINANCEIRO
    dict(kind="photo", img="notebook", t0=76.00, focus=(0.4, 0.5),
         labels=[(w(164), None, "PLANEJAMENTO FINANCEIRO", "n", 0),
                 (w(167), None, "CONTRATOS COM SEGURANÇA", "n", 0)]),
    # 15. QUADRO — boa notícia
    dict(kind="board", t0=81.50, items=[
        ("write", w(173), "BOA NOTÍCIA:", NAVY, 84),
        ("hl", w(175), 0),
        ("write", w(177), "SUA EMPRESA NÃO", NAVY, 74),
        ("write", w(180), "PRECISA ENFRENTAR", NAVY, 74),
        ("write", w(184), "ISSO SOZINHA", RED, 84),
    ]),
    # 16. TECNOLOGIA — data center (etiquetas empilhadas)
    dict(kind="photo", img="datacenter", t0=87.20, focus=(0.5, 0.5),
         labels=[(w(187), w(192), "TECNOLOGIA", "n", 0),
                 (w(188), w(192), "INTELIGÊNCIA ARTIFICIAL", "n", 1),
                 (w(191), w(192), "ESPECIALISTAS", "n", 2),
                 (w(196), None, "MAIS ESTRATÉGICO", "n", 0),
                 (w(199), None, "E ORGANIZADO", "n", 1)]),
    # 17. MERCADO PÚBLICO — Esplanada aérea
    dict(kind="photo", img="esplanada", t0=96.70, focus=(0.5, 0.5),
         labels=[(w(202), None, "MERCADO PÚBLICO", "n", 0),
                 (w(208), None, "CANAL DE CRESCIMENTO", "n", 0)]),
    # 18. QUADRO — a pergunta certa
    dict(kind="board", t0=101.45, items=[
        ("write", w(215), "A QUESTÃO NÃO É SÓ:", GRAY, 60),
        ("write", w(219), "VALE A PENA?", NAVY, 96),
        ("strike", w(227), 1),
        ("write", w(229), "É SABER COMO", NAVY, 80),
        ("write", w(230), "FAZER DO JEITO CERTO", NAVY, 72),
        ("hl", w(233), 3),
    ]),
    # 19. PERGUNTA DO CTA
    dict(kind="photo", img="ministerio", t0=108.70, focus=(0.35, 0.5), zoom0=1.15,
         labels=[(w(236), None, "QUER DESCOBRIR COMO?", "n", 0),
                 (w(241), None, "APROVEITAR AS OPORTUNIDADES", "n", 0)]),
    # 20. CTA — volta ao escritório do início
    dict(kind="cta", img="escritorio", t0=113.80, focus=(0.42, 0.42),
         labels=[(w(247), w(255), "CONHEÇA A JAMAP", "y", 0),
                 (w(255), None, "DÊ O PRIMEIRO PASSO", "y", 0)],
         card=w(249), url=(w(251), w(254, 0.3)), url_text="jamap.com.br"),
]
END = 122.514
