# Regras de escrita e tom

O texto e parte do design. Tom inconsistente quebra o sistema mais rapido que cor errada.

## Indice

- [Labels de secao](#labels-de-secao)
- [Tom do lide](#tom-do-lide)
- [Tom do insight · cruzamento](#tom-do-insight--cruzamento)
- [Numeros no texto](#numeros-no-texto)
- [Metadata de tempo](#metadata-de-tempo)
- [Uso do italico](#uso-do-italico)
- [Dia da semana e mes](#dia-da-semana-e-mes)
- [Sinalizacao verbal de prioridade](#sinalizacao-verbal-de-prioridade)

## Labels de secao

**Formato canonico:** `<Palavra-inicial em maiuscula><resto em minuscula>.`

Sempre em sentence case com ponto final. Sempre em Georgia italic 13px terracota (via `.section-label`).

### Vocabulario aprovado

| Secao | Label |
|---|---|
| Resumo narrativo do dia | "Lide do dia." |
| Cruzamento aleatorio de metodologias | "Insight · cruzamento." |
| Mini-calendario do mes | "Abril" (nome do mes, sem ponto) |
| Saude/treino/body | "Corpo." |
| Cronograma do dia | "Agenda." |
| 3 prioridades maximas | "Tres inadiaveis." |
| Tarefas atribuidas (ClickUp) | "Tarefas ClickUp." |
| Saude das frentes do workspace M7 (atrasadas + bloqueadas) | "Workspace M7." |
| Ideias capturadas | "Notas do dia." |
| Previsao do proximo dia | "Amanha." |

### Legado (nao usar no template atual)

Estes labels foram substituidos. Mantidos aqui apenas por contexto historico:

| Label antigo | Substituido por |
|---|---|
| "Foco do dia." | "Lide do dia." |
| "Semana 16." (secao dedicada) | "(sem. 16)" inline no header Abril |
| "PRs da equipe." | "Delegadas." (v1.0-v1.8) → "Workspace M7." (v1.9+, escopo workspace inteiro) |
| "Delegadas." | "Workspace M7." (escopo passou de "tasks delegadas por Bruno" para "saude do workspace M7 inteiro") |

### Nunca usar

- Dois-pontos no fim (`Foco do dia:`)
- Travessao (`— Foco do dia`)
- Colchetes (`[Foco do dia]`)
- Sublinhado ou bold em vez de italico
- UPPERCASE (`FOCO DO DIA`)
- Emoji como prefixo (`📌 Foco do dia`)

## Tom do lide

**Terceira pessoa, tempo presente, tom FT (Financial Times).**

O lide descreve o que o dia reserva, nao o que voce "vai fazer". E redigido como se um jornalista narrasse o dia do Bruno.

### Comparativo

| Errado | Correto |
|---|---|
| "Vou revisar o WBR..." | "Bruno revisa as 14h o WBR..." |
| "Hoje tenho que..." | "Hoje, com Pedro e Fernando..." |
| "Preciso preparar slides" | "Prepara os slides da diretoria..." |

### Extensao

Entre 200 e 400 caracteres. Menor parece resumo superficial; maior parece relatorio.

### Amarracao

Sempre incluir:
- Evento principal do dia (o que acontece)
- Pessoas envolvidas (com quem)
- Metricas quando existirem (em italico via `.metric`)
- Ganho ou consequencia (o que destrava)

## Tom do insight · cruzamento

**Provocativo, aforistico, sem conclusao.**

O Insight cruza **2 conceitos de fontes diferentes** (metodologias, frameworks, autores) para gerar uma ideia nova. Nao explica — provoca. Nao conclui — deixa a tensao.

### Estrutura canonica

```
<Conceito A> <acao>. <Conceito B> <acao contraria/complementar>.
(travessao-mdash) <interpretacao curta>: "<pergunta A>" vs "<pergunta B>".
```

### Exemplo

> Shape Up define um Appetite antes do problema. GPD pergunta Why-Why depois — sao perguntas diferentes: "quanto vale investigar?" vs "por que existe?"

### Citacao

Sempre no formato: `<Conceito A> · <Fonte A>  ×  <Conceito B> · <Fonte B>`

Exemplos de fontes validas:
- Shape Up · Basecamp
- GPD · Falconi
- OKR · Doerr
- Zettelkasten · Luhmann
- Toyota Kata · Rother
- Swiss Editorial · grid tradition

### Extensao

150-250 caracteres no body. Mais curto vira clickbait; maior vira ensaio.

### Tom correto

| Errado (explicativo) | Correto (provocativo) |
|---|---|
| "O Shape Up nos ensina que..." | "Shape Up define..." |
| "A diferenca entre eles e que..." | "Sao perguntas diferentes: X vs Y" |
| "Concluindo, ambos..." | (sem conclusao — deixa em aberto) |
| "Esta abordagem e util porque..." | (remover — o cruzamento e o valor) |

## Numeros no texto

### Regras

- Numeros importantes sempre em italico terracota (ou azul para corpo) via `<em class="metric">`
- Nunca escrever numeros por extenso dentro de dados
- Porcentagens em formato compacto

### Exemplos

| Errado | Correto |
|---|---|
| "as duas da tarde" | "14h" |
| "cinquenta e tres por cento" | "53%" |
| "seis vezes o baseline" | "<em>6x</em> o baseline" |
| "quarenta e sete de sessenta e dois" | "<em>47</em> de 62" |

## Metadata de tempo

### Vocabulario canonico

| Contexto | Forma correta |
|---|---|
| Dia atual | "hoje" (minusculo) |
| Dia anterior | "ontem" |
| Proximo dia | "amanha" |
| Atraso | "+1d atraso", "+2d" |
| Prazo hoje | "ate 14h", "hoje" |
| Prazo em breve | "em 36min", "hoje a tarde" |
| Prazo futuro proximo | "esta semana", "prox semana" |
| Data especifica futura | "dia 2/2", "sex 17" |

### Nunca usar

- "nesta data" (formal demais)
- "presente momento" (formal demais)
- "D-1", "D+3" (jargao corporativo)
- "dias atras" (nebuloso)
- Horas em formato americano (`2pm` em vez de `14h`)

## Uso do italico

O italico Georgia aparece em **tres situacoes apenas**:

### 1. Labels de secao

Sempre terracota, sempre ponto final.

### 2. Entidades destacadas dentro de frases

Em terracota quando e trabalho/foco/pessoa. Em azul petroleo quando e metrica de corpo/treino.

Exemplos:
- Nomes proprios: "1:1 com <em>Pedro</em>"
- Projetos: "publicacao dos <em>Cards de Performance</em>"
- Metricas: "conversao em <em>6.5x</em>"
- Horarios-chave: "as <em>14h</em>"

### 3. Numeros romanos como marcadores

Sempre em italico, sempre opacity 0.5.

## Dia da semana e mes

### Formato de data

Sempre: `<numero> <mes-minusculo>` — `16 abril`, `3 maio`, `27 junho`.

**Nunca:**
- `16/04` (numerico)
- `16 Abril` (mes capitalizado)
- `April 16` (ingles)
- `16 de abril` (preposicional)

### Dias da semana

- No cabecalho: "Quinta-feira" (primeira letra maiuscula, hifen, resto minusculo)
- No calendario: "qui" (abreviacao minuscula de 3 letras)

### Semana do ano

No cabecalho do mini-calendario: "(sem. 16)" — abreviado, entre parenteses, minusculo.
No header__dia-meta: "semana 16" — escrito por extenso, sem parenteses.
Nunca: "semana dezesseis", "W16", "S16".

## Sinalizacao verbal de prioridade

O sistema nao usa badges, pills ou marcadores visuais para prioridade. Em vez disso:

| Prioridade | Tratamento |
|---|---|
| Maxima | Vira parte dos "Tres inadiaveis" |
| Atrasada | Texto inteiro em `.alert` + metadata `+Nd atraso` |
| Proxima | Horario em terracota + item em italico terracota (.agenda__event--now) |
| Normal | Nenhum tratamento especial |

Se algo precisa de "mais atencao" alem disso, o sistema te diz que voce esta tentando gritar visualmente onde a hierarquia ja deveria ter feito o trabalho.
