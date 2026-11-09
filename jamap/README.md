# Vender para o governo vale a pena? — vídeo Jamap

Projeto feito do zero no formato descrito em `../modelo.md` (seções 1–8), com a identidade do site jamap.com.br.

## Formato aplicado
- 1080×1920, 30 fps, 122,5 s, narração `in/narracao.mp3`.
- **Cortes secos com flash** a cada 3–10 s (20 planos): **meio a meio** entre **fotos reais** (10 planos, Wikimedia Commons, ver `assets/photos/CREDITOS.md`) e **motion graphics** (10 planos, `src/motion.py`).
- Foto de fundo com **push-in** rápido de 1,0 → 1,12× em 0,35 s (ease-out) e drift lento.
- **Motion "pow"**: fundo azul-marinho ou amarelo com pontos, anéis girando e faixa diagonal; palavras entram uma a uma com pop elástico; marca-texto, risco vermelho, carimbo "MITO!", barras que crescem (MEI → GRANDE) e selo; flash e tremida nos impactos.
- **Personagem** (`assets/personagem/personagem.webp`) fixa no canto inferior direito, com boca guiada pelo volume da voz, respiração e pulinho quando entra uma etiqueta.
- **Etiqueta** no terço superior (y ≈ 26%), entrando em pop (0,6 → 1,08 → 1,0 em 0,2 s). O gancho tem 3 linhas e o CTA usa caixa amarela maior.
- **Legenda** em blocos de 1–3 palavras (Poppins Black, branca com contorno), em y ≈ 76%.
- **CTA**: volta ao escritório da abertura, com cartão Jamap e endereço `jamap.com.br` sendo digitado.

## Identidade jamap.com.br
| Uso | Cor |
|---|---|
| Etiquetas, fundo do motion | Azul-marinho `#001D52` |
| Destaque, CTA, marca-texto, faixa das etiquetas | Amarelo `#FEBF00` |
| Alerta, custo, risco | Vermelho `#EF4444` |
| Texto secundário | Cinza `#606060` |

Fonte: Poppins (a mesma do site), baixada do repositório google/fonts.

## Como gerar
```bash
cd jamap/src
python3 render.py --frames 1.0,27.9 --guides   # confere quadros (salvos em jamap/previews)
python3 render.py                              # gera ../../output/vale-a-pena-vender-para-o-governo.mp4
```
- Cenas e tempos: `src/roteiro.py` (tempos por palavra em `in/words.json`, transcritos com ElevenLabs Scribe).
- Fotos: `src/commons.py "<busca>" <pasta>` gera folhas de contato e `src/fetch_photos.py` baixa as escolhidas.
