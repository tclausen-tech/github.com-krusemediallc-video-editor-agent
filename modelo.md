# Modelo de edição: "Tutorial explicado para criança" com boneco animado

> Modelo extraído da análise quadro a quadro de um Reel de referência (90 s, 720×1280, 30 fps, PT-BR).
> Tema original: *"Te ensinando a vender pro governo como se você tivesse dez anos"* (licitações no PNCP).
> O objetivo é reaproveitar **estilo, animações, ritmo e estrutura** em qualquer tema de tutorial passo a passo.

---

## 1. Ficha técnica

| Item | Valor |
|---|---|
| Formato | Vertical 9:16, 720×1280 (exportar em 1080×1920) |
| FPS | 30 |
| Duração | ~90 s (faixa ideal: 60–90 s) |
| Narração | Voz única, contínua, em off, ~4,2 palavras/s, quase sem pausas (só 1 pausa > 0,35 s em 90 s) |
| Trilha | Sem música marcante; a voz carrega o vídeo |
| Transições | Dois tipos, nenhum dissolve/wipe: **(a) troca de cenário = corte + flash branco de entrada** (~4 quadros, só no cenário/boneco; legenda e etiquetas não piscam); **(b) troca de tela dentro do mesmo mockup = corte seco puro** |
| Personagem | Boneco "palito" desenhado (corpo branco, contorno preto, cabelo castanho, olhos redondos grandes) sobreposto a fotos/gravações reais |

---

## 2. Estilo visual

### 2.1 Camadas (de baixo para cima)
1. **Fundo / cenário** – foto real ou gravação de tela inserida num cenário:
   - *Quarto/escritório* (abertura e CTA) – foto estática de home office.
   - *Monitor em cima da mesa* – gravação de tela "colada" dentro de um monitor fotografado (com post-it e teclado), em perspectiva.
   - *Quadro branco* – quadro branco em parede cinza com piso de madeira (contas e listas).
   - *Celular na mão* – mockup de iPhone segurado pelo boneco, sobre fundo de sala clara (pesquisa de preço / compra).
   - *Locais reais* – foto de porta de casa com caixa, foto de prefeitura (logística/entrega).
2. **Destaques de UI** – retângulo de contorno vermelho, marca-texto amarelo, cursor com anel de clique.
3. **Boneco** – canto inferior direito (às vezes à esquerda para não tapar a UI), ocupando ~35–45% da altura.
4. **Etiqueta verde (label)** – topo da tela.
5. **Legenda falada** – faixa central-baixa.

### 2.2 Tipografia

| Elemento | Fonte (equivalente) | Estilo | Cor | Posição |
|---|---|---|---|---|
| **Legenda (karaokê por frase)** | Montserrat Black/ExtraBold | CAIXA ALTA, ~34 px @720p, contorno preto ~3 px + leve sombra | Branco `#FFFFFF` | Centralizada, y ≈ 76% da altura (logo acima do "peito" do boneco) |
| **Etiqueta verde** | Montserrat Bold/ExtraBold | CAIXA ALTA, ~26 px @720p | Texto branco sobre caixa verde `#1E6630` (cantos retos, padding ~10 px) | Topo, y ≈ 9–10%; centralizada ou alinhada à esquerda sobre a UI |
| **Etiqueta do gancho** | Montserrat Bold | 3 linhas, CAIXA ALTA, mesma caixa verde | Branco / `#1E6630` | Topo, y ≈ 13–19% |
| **Etiqueta do CTA** | Montserrat ExtraBold | ~1,4× maior que as outras, texto entre aspas: `COMENTA "EU"` | Branco / `#1E6630` | Topo |
| **Escrita no quadro branco** | Fonte marcador condensada (ex.: *Bangers*, *Luckiest Guy*, *Permanent Marker*) | CAIXA ALTA | Ver paleta abaixo | Alinhada à esquerda, de cima para baixo |

### 2.3 Paleta
| Uso | Cor |
|---|---|
| Etiquetas / "dinheiro bom" / lucro | Verde `#1E6630` (caixa) e verde vivo `#2DB34A` (texto no quadro) |
| "Você paga" (custo) | Vermelho `#D02830` |
| "Governo paga" / títulos de listas | Azul `#2058C8` |
| Títulos neutros no quadro | Preto `#111111` |
| Destaque de campo na UI | Contorno vermelho `#D0323C`, 2–3 px, sem preenchimento |
| Destaque de resultado | Marca-texto amarelo translúcido `#FFE84D` ~60% |
| Legenda | Branco + contorno preto |

Regra de cor: **verde = ganho/ação**, **vermelho = custo**, **azul = quem paga / estrutura**.

### 2.4 Zoom e movimento de câmera
- **Cenas de tela (monitor):** no corte, começa em plano mais aberto (monitor inteiro + mesa) e faz **push-in** rápido (~1,0 → 1,15–1,25×, ease-out) até a tela ocupar a largura. Medido no plano 2: o zoom começa ~0,35 s após o corte (4,77 s) e termina em 5,17 s → **~0,4 s de movimento, ~12 quadros**, com desaceleração forte no fim. Durante o push-in o boneco desliza junto (está "preso" ao cenário); depois segue com **drift lento** (pan vertical sutil) acompanhando a área de interesse da UI (rolagem para baixo à medida que a narração avança).
- **Celular:** entra já grande, com leve **escala + deslize** de assentamento (~2–3 quadros, ~0,1 s, ease-out), junto com o flash branco do corte (conferido em 70,00 s).
- **Quarto, quadro branco, fotos de locais:** câmera praticamente **estática**; o movimento vem do boneco e da escrita.
- Não há zoom "punch" agressivo nem shake: o dinamismo vem da troca constante de legenda, gestos e anotações.

---

## 3. Animações (entrada e saída de cada elemento)

| Elemento | Entrada | Permanência | Saída |
|---|---|---|---|
| **Entrada de cenário** | **Flash branco**: o 1º quadro do novo cenário vem ~70% lavado de branco, o 2º ~40%, o 3º ~15%, e o 4º já está normal (ease-out, ~0,13 s). Aplica-se ao fundo **e** ao boneco | — | O cenário anterior sai em corte seco (sem fade-out) |
| **Troca de tela interna** | Corte seco do conteúdo dentro do monitor/celular; moldura, boneco e vareta continuam (ex.: 40,80 s, 55,60 s, 81,20 s) | — | Corte seco |
| **Legenda** | Corte seco (aparece inteira, sem pop; não sofre o flash branco) | 0,4–1,0 s por bloco de 1–4 palavras, sincronizada à fala | Corte seco para o próximo bloco |
| **Etiqueta verde** | **Fade-in** de 2–4 quadros (~0,1 s), sem escala nem deslize | 1,5–3 s (enquanto o assunto está sendo falado) | **Fade-out** de 2–4 quadros, normalmente **terminando logo antes** do corte ou da troca de tela; às vezes some no corte |
| **Etiqueta do CTA** | Fade-in + leve escala (entra ~1,1× e assenta), ~3 quadros; substitui a etiqueta anterior no mesmo lugar | Até o fim | Fim do vídeo |
| **Etiqueta do gancho** | Já presente no frame 0 | Todo o plano de abertura (~4,4 s) | Some no corte |
| **Boneco** | Quase sempre já em cena no corte. Exceção: na cena da prefeitura (74,83 s) ele **entra andando pela esquerda** carregando a caixa (~0,4 s, ~0,4 s após o corte) | Sempre visível | — |
| Piscada | Olhos fechados por 1–2 quadros a cada ~3–5 s | — | — |
| Gestos do boneco | Troca de pose a cada 1–2 s: acenar, dedo indicador para cima, apontar com vareta, segurar celular/caixa, piscar olhos | — | — |
| **Vareta/ponteiro** | Braço estica uma vareta fina preta (com mãozinha/círculo na ponta) até o elemento citado no exato momento da palavra ("aqui", "ó"); a extensão leva ~5 quadros (~0,17 s), depois a ponta acompanha o cursor/texto | Enquanto o elemento é citado | Recolhe |
| **Contorno vermelho na UI** | Desenha/aparece no momento da citação | 1–3 s | Some quando muda o foco |
| **Marca-texto amarelo** | Aparece sobre o link/resultado quando dito "esse site aqui" | 1–2 s | Corte |
| **Cursor + anel de clique** | Cursor move até o botão e emite um anel circular azul no clique | ~0,3 s | — |
| **Escrita no quadro** | **Write-on** com caneta: o boneco "escreve" letra a letra com o ponteiro, sincronizado com a fala (ex.: "R$ 9 4 1, 9 8" é escrito enquanto ele diz "novecentos e quarenta e um..."). Velocidade medida: "A PREFEITURA PAGA:" (18 caracteres) em ~21 quadros → **~25 caracteres/s**; a ponta da vareta segue a última letra | Linhas anteriores permanecem; o quadro acumula | Corte |
| **Linha de soma** | Traço horizontal desenhado da esquerda para a direita antes do resultado | — | — |
| **Ícones/props** | Caixa de papelão entra com o boneco; **caminhão "CORREIO"** (amarelo) atravessa a base da tela da esquerda para a direita em ~1,3 s, velocidade constante, sincronizado com "mandar por correio" | — | Sai pela lateral oposta |
| **Tela "Compra realizada!"** | Celular com tela verde e check branco aparece no corte | ~1 s | Corte |

---

## 4. Cortes e ritmo

### 4.1 Números-chave
- **15 planos de cenário** (14 cortes com flash) + **~6 trocas de tela internas** em corte seco, em 90 s → **duração média ~5,5–6 s** por plano de cenário.
- Planos curtos (1,5–4,5 s) para transições narrativas (gancho, entrega, compra); planos longos (7–11 s) para demonstração de tela, **mas** dentro deles a legenda troca a cada ~0,6 s, a etiqueta a cada ~3 s e a UI rola/destaca a cada 1–2 s → **algo muda na tela a cada ≤ 1 s**.
- Legenda: ~140 trocas em 90 s (≈ 1 troca a cada 0,65 s).

### 4.2 Mapa de planos do vídeo de referência

| # | Início–fim (s) | Dur. | Cenário | Fala (resumo) | Overlay |
|---|---|---|---|---|---|
| 1 | 0,00–4,43 | 4,4 | Quarto (boneco acenando) | "Te ensinando a vender pro governo como se você tivesse dez anos, tá? Pega esse bizu aqui." | Etiqueta gancho 3 linhas |
| 2 | 4,43–11,23 | 6,8 | Monitor: Google | "Primeiro passo, digita PNCP licitação… sem acento… dá enter" | `SEM ACENTO`, `DÁ ENTER` |
| 3 | 11,23–15,60 | 4,4 | Monitor: resultado → site | "Vai ser esse site aqui… é o site que tem editais" | `PNCP.GOV.BR`, marca-texto, contorno vermelho |
| 4 | 15,60–18,83 | 3,2 | Quadro branco | "Duas configurações muito importantes" | Escreve `2 CONFIGURAÇÕES / 1. / 2.` |
| 5 | 18,83–29,63 | 10,8 | Monitor: filtros | "A primeira… dispensa… a segunda, tua região…" | `1 - SELECIONE DISPENSA`, `2 - SELECIONE SUA REGIÃO` |
| 6 | 29,63–37,23 | 7,6 | Monitor: palavra-chave | "Em palavra-chave, qualquer produto… lâmpada… enter" | `QUALQUER PRODUTO`, `ENTER OU PESQUISAR` |
| 7 | 37,23–47,60 | 10,4 | Monitor: resultados → edital | "Já tem um monte de oportunidade… Município de Franca… modelo ELPLP80" | `MUNICÍPIO DE FRANCA - SP`, foto do produto + `ELPLP80` |
| 8 | 47,60–52,03 | 4,4 | Quadro branco | "Pagando R$ 941,98 em cada unidade" | Escreve `A PREFEITURA PAGA: R$ 941,98 POR UNIDADE` (verde) |
| 9 | 52,03–62,40 | 10,4 | Celular: Google → Mercado Livre | "Joguei no Google… achei no Mercado Livre… R$ 293" | `VALOR DE MERCADO`, `ACHEI NO MERCADO LIVRE`, `R$ 293` |
| 10 | 62,40–70,03 | 7,6 | Quadro branco | "5 unidades… você paga 1.465… governo paga 4.709… lucro 3 mil" | Escreve conta em preto/vermelho/azul/verde |
| 11 | 70,03–73,20 | 3,2 | Celular | "Aí dependendo… nesse caso compraria no Mercado Livre" | Tela verde "Compra realizada!" |
| 12 | 73,20–74,83 | 1,6 | Foto porta com caixa | "Chegaria na tua casa" | `CHEGOU NA SUA CASA!` |
| 13 | 74,83–78,83 | 4,0 | Foto prefeitura | "Ia lá e entregava, ou manda por correio" | `PREFEITURA`, `ENTREGA NO ÓRGÃO`, `OU MANDA PELO CORREIO`, caminhão entra |
| 14 | 78,83–85,63 | 6,8 | Monitor: PNCP → Compras.gov | "Tem que cadastrar em outro portal… fica pra outro vídeo" | `COMPRAS.GOV.BR`, `FICA PRO PRÓXIMO VÍDEO` |
| 15 | 85,63–90,03 | 4,4 | Quarto (volta ao início) | "Se quer um tutorial… comenta EU" | `TUTORIAL COMPLETO`, `COMENTA "EU"` + caixa de comentário digitando "EU" |

### 4.3 Padrão de alternância
`Quarto → Tela → Tela → QUADRO → Tela → Tela → Tela → QUADRO → Celular → QUADRO → Celular → Foto → Foto → Tela → Quarto`

- O **quadro branco** aparece a cada ~20–25 s para "resumir/traduzir" o que a tela mostrou (lista, valor, conta).
- Abertura e fechamento no **mesmo cenário** (quarto) → sensação de ciclo fechado.

### 4.4 Microcortes dentro dos planos (sem flash)
| Tempo (s) | Plano | O que muda |
|---|---|---|
| 9,60–9,80 | 2 | Google → página de resultados (etiqueta `SEM ACENTO` sai, `DÁ ENTER` entra) |
| 40,80 | 7 | Lista de resultados → página do edital (Aviso de Contratação) |
| 43,1–43,4 | 7 | Rolagem/troca para a lista de itens com foto do produto |
| 55,60 | 9 | Google Shopping → anúncio do Mercado Livre |
| 81,20 | 14 | PNCP → Compras.gov.br |

Regra: o mockup (monitor/celular), o boneco e a vareta **não** mudam; só o conteúdo da tela troca em corte seco, e a etiqueta anterior faz fade-out nos 2–3 quadros anteriores.

---

## 5. Estrutura narrativa

| Bloco | Tempo | % | Função | Fórmula de fala |
|---|---|---|---|---|
| **Gancho** | 0–4,4 s | 5% | Promessa + simplificação extrema | "Te ensinando a **[resultado desejado]** como se você tivesse **dez anos** de idade, tá? Pega esse bizu aqui." |
| **Contexto / Passo 1** | 4,4–15,6 s | 12% | Onde começar (ferramenta/site) | "Ó, primeiro passo, cê vai digitar aqui no Google: **[termo]**… vai ser esse site aqui, mas presta atenção, ó." |
| **Configuração** | 15,6–37 s | 24% | Lista numerada no quadro + execução na tela | "Cê tem que fazer **[N] configurações** muito importantes. A primeira… a segunda… e aqui em cima…" |
| **Demonstração com caso real** | 37–70 s | 37% | Exemplo concreto com números (preço pago × preço de mercado → lucro) | "Por exemplo, essa oportunidade aqui: **[quem]** tá querendo comprar **[o quê]** e tá pagando **[R$ X]**… achei no **[loja]** a **[R$ Y]**… nessa brincadeira cê já poderia ganhar uns **[R$ Z]**." |
| **Logística / objeção** | 70–79 s | 10% | Como funciona na prática (tirar medo) | "Cê compraria… chegaria na tua casa… ia lá e entregava, ou manda por correio." |
| **Gancho para continuação** | 79–85,6 s | 7% | Loop aberto (próximo vídeo) | "Mas aí cê tem que cadastrar em outro portal… só que isso vai ficar pra outro vídeo." |
| **CTA** | 85,6–90 s | 5% | Comentário com palavra-chave (gatilho de DM/automação) | "Se você quer um **tutorial completo** pra **[resultado]**, comenta **'[PALAVRA]'** aqui que eu vou te mandar." |

Princípios de roteiro:
- Linguagem oral, informal, 2ª pessoa ("cê", "tua", "ó", "pessoal", "bizu").
- Dêiticos constantes ("aqui", "esse", "ó") → cada um deve ter um **ponteiro/destaque visual** no frame.
- Números falados por extenso viram números **escritos** no quadro.
- A promessa do gancho é paga com um **número de lucro** no meio do vídeo.

---

## 6. Regras de reaproveitamento (checklist de edição)

1. [ ] Gancho em ≤ 4,5 s, com etiqueta verde de 3 linhas repetindo a promessa por escrito.
2. [ ] Troca de cenário a cada 3–11 s com corte + flash branco de 4 quadros (só no fundo/boneco); trocas de tela dentro do mockup em corte seco.
3. [ ] Legenda em blocos de 1–4 palavras, Montserrat Black branca com contorno preto, y ≈ 76%.
4. [ ] Etiqueta verde (`#1E6630`) com fade de ~0,15 s para cada termo-chave/passo ("1 - …", "2 - …").
5. [ ] Toda vez que a fala disser "aqui"/"esse"/"ó", mostrar ponteiro + contorno vermelho ou marca-texto.
6. [ ] Gravações de tela dentro de mockup de monitor, com push-in de ~1,2× no início do plano.
7. [ ] Quadro branco a cada ~20 s com escrita animada em fonte marcador e código de cores (vermelho custo, azul fonte, verde lucro).
8. [ ] Pesquisas no celular com mockup de iPhone segurado pelo boneco.
9. [ ] Boneco sempre em cena, mudando de gesto a cada 1–2 s, posicionado para não cobrir a UI.
10. [ ] Fechar no mesmo cenário da abertura, com etiqueta CTA maior + animação de comentário sendo digitado.
11. [ ] Algo deve mudar na tela pelo menos a cada 1 s.

---

## 7. Template de planejamento (preencher para um novo vídeo)

```text
TEMA: ______________________   PALAVRA DO CTA: "____"

[01] 0,0–4,5s  | QUARTO        | Gancho: "Te ensinando a ____ como se você tivesse dez anos"     | Etiqueta 3 linhas
[02] 4,5–11s   | MONITOR       | Passo 1: onde buscar "____"                                     | Etiquetas: ____
[03] 11–15,5s  | MONITOR       | "Vai ser esse site aqui" → ____                                 | Etiqueta: URL
[04] 15,5–19s  | QUADRO        | "N configurações importantes" (lista 1., 2.)                    | Write-on azul
[05] 19–30s    | MONITOR       | Config 1 / Config 2                                             | "1 - ____", "2 - ____"
[06] 30–37s    | MONITOR       | Busca/filtro final                                              | Etiqueta: ____
[07] 37–47s    | MONITOR       | Exemplo real: quem / o quê                                      | Etiqueta: ____
[08] 47–52s    | QUADRO        | Valor que paga: R$ ____                                         | Write-on verde
[09] 52–62s    | CELULAR       | Preço de mercado: R$ ____                                       | "VALOR DE MERCADO"
[10] 62–70s    | QUADRO        | Conta: custo (vermelho) × receita (azul) = lucro (verde)        | Write-on
[11] 70–79s    | FOTOS/CELULAR | Logística (compra → chega → entrega)                            | Etiquetas curtas
[12] 79–85,5s  | MONITOR       | Próximo passo "fica pro próximo vídeo"                          | Etiqueta
[13] 85,5–90s  | QUARTO        | CTA: comenta "____"                                             | Etiqueta grande + caixa de comentário
```

---

## 8. Transcrição de referência (para calibrar tom e ritmo)

> Te ensinando a vender pro governo como se você tivesse dez anos de idade, tá? Pegue esse bizu aqui. Ó, primeiro passo, cê vai digitar aqui no Google: PNCP licitação. Pode fazer separado mesmo, aqui sem acento, cê vai dar um enter aqui. Deu enter, vai ser esse site aqui, mas presta atenção, ó. É o site aqui que tem editais. Então vamo lá pessoal, entrou no site, cê tem que fazer duas configurações que são muito importantes, ó. A primeira é aqui na direita, essa é a mais importante. Cê vai selecionar por dispensa, que é a mais fácil pra quem tá começando. A segunda, cê vai selecionar a tua região, eu sou do DF, mas eu vou escolher São Paulo, porque lá tem muita oportunidade. E aqui em cima, em palavras-chave, cê pode escolher qualquer produto que cê quer vender. Eu vou pesquisar aqui, ó, por lâmpada. Aí dá um enter ou dá um pesquisar aqui embaixo. Aí aqui pessoal, já tem um monte de oportunidade, ó. Por exemplo, essa oportunidade aqui. Município de Franca, lá de São Paulo, tá querendo comprar essa lâmpada modelo ELPLP80 pra projetor Epson. E ele tá pagando novecentos e quarenta e um reais, quase novecentos e quarenta e dois em cada unidade. Aí eu peguei esse modelo aqui e joguei lá no Google mesmo pra pesquisar o valor de mercado e achei ela aqui no Mercado Livre. E aqui no Mercado Livre eu achei essa mesma lâmpada, igualzinha, eles tão pedindo, ó, a duzentos e noventa e três reais. Considerando que são cinco unidades, isso aqui vai dar uns mil quatrocentos e pouco, isso daqui dá quatro mil e setecentos. Nessa brincadeira aqui, cê já poderia, né, ganhar uns três mil aí, dependendo. Nesse caso aqui, cê compraria no Mercado Livre, chegaria na tua casa, depois que você recebesse, cê ia lá no lugar e entregava, ou senão cê pode mandar por correio também. Aí aqui nesse site PNCP, cê já consegue ver a oportunidade, mas aí cê tem que cadastrar em um outro portal, que é o portal de compras públicas, só que cê vai ter que ficar pra outro vídeo. Mas se você quer um tutorial pra aprender a encontrar já suas primeiras oportunidades, comenta "eu" aqui que eu vou te mandar.

---

### Notas de método
- Cortes detectados por `ffmpeg` (`select='gt(scene,0.15)'`) e conferidos visualmente; tempos com precisão de ±1 frame. Alguns cortes entre telas parecidas (ex.: PNCP → Compras.gov **81,20 s**) só aparecem com limiar baixo. Verificação quadro a quadro (30 fps) feita com diferença média de luminância entre quadros: o padrão "pico + 3 quadros decrescentes" após cada corte de cenário é o flash branco; picos isolados sem cauda são trocas de tela internas.
- Animações conferidas a 10 fps nos trechos de transição; cores medidas por amostragem de pixels (podem variar ±5% pela compressão do vídeo).
- Fontes são **equivalentes visuais** (o vídeo não carrega metadados de fonte).
- Transcrição obtida por speech-to-text (ElevenLabs Scribe).

---

## 9. Formato do projeto: motion clean + área segura

> A partir desta versão o projeto usa um formato **motion clean**, que substitui os cenários ilustrados e os cortes secos da referência. Continuam valendo a estrutura (seção 5), as etiquetas, as legendas sincronizadas, os destaques e a vareta.

### 9.1 Layout e área segura (Instagram, Reels, TikTok, Shorts)
| Zona | Coordenadas (1080×1920) | Motivo |
|---|---|---|
| Grade do perfil 4:5 | y 285–1635 | o Instagram recorta o Reels assim na grade do perfil |
| Grade do perfil 3:4 | y 240–1680 | recorte novo da grade |
| Evitar no topo | y < 250 | barra superior e nome do áudio |
| Evitar embaixo | y > 1500 | usuário, legenda e botão de seguir |
| Evitar à direita | x > 950, y 960–1700 | curtir, comentar, compartilhar |
| **Área segura usada** | **x 60–940, y 300–1490** | tudo o que importa fica aqui |

- **Etiqueta:** topo da área segura (y = 300), centralizada.
- **Coluna de conteúdo:** x 60–640, a partir de y = 410. Recebe os cartões, os títulos e o painel de zoom do celular.
- **Personagem:** fixa à direita, com centro em x = 800 e pés em y = 1470. Mede 900 px de altura (1,65 m) e não muda de tamanho entre as cenas. Ocupa x ≈ 640–930.
- **Legenda:** centro em y = 1385, dentro da grade 4:5 e acima da legenda do Reels.

### 9.2 Linguagem visual
- **Fundo:** gradiente claro (`#F6F8FC` → `#E5EAF2`) com grade de pontos sutil e círculos desfocados azul-marinho e amarelo que se movem devagar.
- **Cartões:** brancos, cantos de 40 px, sombra suave azul-marinho. O conteúdo entra deslizando da esquerda com fade (0,45 s, ease-out) e sai com fade para a esquerda (0,2 s). Não há corte seco: o fundo e a personagem continuam no lugar e só o conteúdo troca.
- **Tipos de cena:**
  - `title`: frase grande, e a palavra-chave ganha fundo amarelo que se estende.
  - `ui`: cartão de interface.
  - `phone`: a personagem segura o celular e a tela aparece num painel com lupa.
  - `list`: itens com ícone que entram um a um e podem ser riscados, mais o carimbo "MITO!".
  - `calc`: valores que contam até o número final.
  - `portes`: empresas que crescem a partir do chão, na mesma escala.
- **Legenda karaokê:** Poppins Black em branco, com contorno azul-marinho; a palavra falada no momento fica amarela.
- **Destaque:** contorno arredondado amarelo com borda azul-marinho. O marca-texto é amarelo translúcido. A vareta termina na borda direita do item, para não cobrir o texto.

### 9.3 Personagem
- Vetorial e feminina: cabelo castanho-escuro, blazer azul-marinho, blusa branca, detalhes amarelos (`video/src/character.py`).
- **Proporções reais (1,65 m).** O celular na mão tem o tamanho real (7,5 × 15 cm); a tela é lida no painel de zoom.
- Animação: boca guiada pelo volume da voz, piscada, balanço leve e um pulinho quando entra uma etiqueta ou um item. O braço gira no ombro até o item citado.

### 9.4 Paleta (jamap.com.br)
| Uso | Cor |
|---|---|
| Principal: etiquetas, títulos, blazer, contornos | Azul-marinho `#001D52` |
| Destaque: palavra-chave, palavra ativa da legenda, marca-texto, carimbo, faixa das etiquetas | Amarelo `#FEBF00` |
| Neutro | Cinza `#DDE0DF` |
| Texto secundário | `#333333` |
| Custo, prejuízo e erro (exceção) | Vermelho `#D0312D` |
- Fonte: **Poppins** (Black, ExtraBold, SemiBold). Cores ficam em `PAL` em `video/src/engine.py`.

### 9.5 Como gerar um vídeo novo
1. Coloque a narração em `video/in/` e transcreva com tempos por palavra (ElevenLabs Scribe) → `video/words.json`.
2. Escreva as cenas em `video/src/timeline.py`.
3. Gere os cartões, ícones e telas do celular: `python3 video/src/cards.py && python3 video/src/screens.py && node video/src/render_assets.js`.
4. Gere a personagem: `python3 video/src/character.py && node video/src/render_char.js`.
5. Confira quadros com as guias da área segura: `python3 video/src/motion.py --frames 10,20 --guides`.
6. Gere o vídeo: `python3 video/src/motion.py` (1080×1920, 30 fps, H.264 + AAC).

### Personagem (versão atual)
- Ilustração semi-realista em SVG (`video/src/character.py`): luz e sombra em pele, cabelo e roupa, proporção ~7,5 cabeças, olhos com íris e cílios, lábios em dois tons, blazer azul-marinho Jamap acinturado, scarpin.
- Mesma geometria de encaixe da versão anterior (pivô do ombro, braço que aponta, celular em escala real), então `motion.py` não muda.
- Para uma personagem **fotorrealista**, é preciso uma imagem gerada fora daqui (corpo inteiro, fundo branco, boca fechada); ver prompt sugerido no histórico do projeto.

---

## 10. Personagem "Jana" e projetos por pasta

### 10.1 Personagem atual (estilo mascote)
- Gerada por `video/src/character.py`. Cabeça grande (~3 cabeças de altura), rosto arredondado e olhos grandes com dois brilhos. Franja cortina, cabelo castanho ondulado até os ombros, bochechas rosadas e cabeça inclinada 4°.
- Roupa na identidade Jamap: blazer azul-marinho com broche amarelo, blusa branca, colar com pingente amarelo, saia evasê amarela, sapatilha azul-marinho e presilha amarela no cabelo.
- Contorno escuro fino e borda branca de adesivo. A piscada é o olho fechado sorrindo.
- Mantém a interface de camadas (`body_m{0-3}_b{0,1}_{down|phone}`, `arm`, `meta.json`), então `motion.py` não muda. A prévia fica em `video/projects/primeira-licitacao/personagem-jana.png`.

### 10.2 Projetos
Cada vídeo novo vive em `video/projects/<nome>/` com `roteiro.txt`, `narr.mp3`, `words.json`, `timeline.py` e `assets.py` (cartões próprios).
1. Narração com tempos por palavra: ElevenLabs `text-to-speech/{voz}/with-timestamps` (no plano gratuito, só vozes padrão da conta; a voz atual é a Jessica, no `eleven_multilingual_v2`). Siglas vão por extenso no texto falado ("pê ene cê pê") e voltam à grafia de tela ao montar `words.json`.
2. Cartões: `python3 video/projects/<nome>/assets.py && node video/src/render_assets.js <prefixo>`.
3. Personagem: `python3 video/src/character.py && node video/src/render_char.js`.
4. Quadros de teste: `VPROJ=<nome> python3 video/src/motion.py --frames 10,20`.
5. Vídeo: `VPROJ=<nome> python3 video/src/motion.py --workers 8` → `video/out/<nome>.mp4` (copiar para `output/`).

### 10.3 Projeto "primeira-licitacao" (70,6 s)
Tutorial "Sua primeira licitação em 4 passos": PNCP → filtro Dispensa → estado e palavra-chave → plataforma do aviso (Compras.gov.br), com CTA da Jamap ("comenta EU"). O exemplo é fictício: Prefeitura de Vale Verde/SP, 500 caixas de papel A4, R$ 59.500, abaixo do limite de dispensa por valor.
