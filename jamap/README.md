# Vender para o governo vale a pena? — vídeo Jamap

Projeto feito do zero no formato descrito em `../modelo.md` (seções 1–8), com a identidade do site jamap.com.br.

## Formato aplicado
- 1080×1920, 30 fps, 122,5 s, narração `in/narracao.mp3`.
- **Cortes secos** a cada 3–9 s (20 planos), alternando **fotos reais** (Wikimedia Commons, ver `assets/photos/CREDITOS.md`) e **quadro branco** com escrita animada.
- Foto de fundo com **push-in** de 1,0 → 1,12× em 0,7 s (ease-out) e drift lento.
- **Personagem** (`assets/personagem/personagem.webp`) fixa no canto inferior direito, com boca guiada pelo volume da voz, respiração e pulinho quando entra uma etiqueta.
- **Etiqueta** no terço superior (y ≈ 26%), com fade de 3 quadros e leve scale-up. O gancho tem 3 linhas e o CTA usa caixa amarela maior.
- **Legenda** em blocos de 1–3 palavras (Poppins Black, branca com contorno), em y ≈ 76%.
- **Quadro branco**: escrita com marcador sincronizada à fala, marca-texto amarelo, risco vermelho e carimbo "MITO!".
- **CTA**: volta ao escritório da abertura, com cartão Jamap e endereço `jamap.com.br` sendo digitado.

## Identidade jamap.com.br
| Uso | Cor |
|---|---|
| Etiquetas, texto do quadro | Azul-marinho `#001D52` |
| Destaque, CTA, marca-texto, faixa das etiquetas | Amarelo `#FEBF00` |
| Alerta, custo, risco | Vermelho `#EF4444` |
| Texto secundário | Cinza `#606060` |

Fontes: Poppins (site) e Permanent Marker (quadro), baixadas do repositório google/fonts.

## Como gerar
```bash
cd jamap/src
python3 render.py --frames 1.0,27.9 --guides   # confere quadros (salvos em jamap/previews)
python3 render.py                              # gera ../../output/vale-a-pena-vender-para-o-governo.mp4
```
- Cenas e tempos: `src/roteiro.py` (tempos por palavra em `in/words.json`, transcritos com ElevenLabs Scribe).
- Fotos: `src/commons.py "<busca>" <pasta>` gera folhas de contato e `src/fetch_photos.py` baixa as escolhidas.
