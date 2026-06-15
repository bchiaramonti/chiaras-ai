# Regras de escrita e tom (weekly)

> _Migrado da generating-weekly-planner e alinhado à arquitetura Supabase: o output é o objeto canônico (forma enxuta), gravado pela skill writing-week-to-supabase; o front Next.js/Vercel renderiza._

O texto e parte do produto. Tom inconsistente quebra o sistema mais rapido que qualquer outra coisa. Esta referencia estende as regras de texto da daily com estruturas especificas do weekly. **Trata so de texto** — tipografia, cor e layout sao responsabilidade do front Next.js, nao desta referencia.

## Indice

- [Vocabulario de secoes (nomes canonicos)](#vocabulario-de-secoes-nomes-canonicos)
- [Tom da Tese da semana](#tom-da-tese-da-semana)
- [Tom do Insight · cruzamento (semanal)](#tom-do-insight--cruzamento-semanal)
- [Criterio de vitoria · estrutura (discutir, nao persistir v1)](#criterio-de-vitoria--estrutura-discutir-nao-persistir-v1)
- [Orquestra · tema do dia](#orquestra--tema-do-dia)
- [Foco da semana · criterio "pronto quando"](#foco-da-semana--criterio-pronto-quando)
- [Prazos duros · ancoragem (discutir, nao persistir v1)](#prazos-duros--ancoragem-discutir-nao-persistir-v1)
- [Riscos · mitigacao acionavel](#riscos--mitigacao-acionavel)
- [Preflight · respostas](#preflight--respostas)
- [Numeros no texto](#numeros-no-texto)
- [Metadata de tempo semanal](#metadata-de-tempo-semanal)
- [Dia da semana e mes](#dia-da-semana-e-mes)
- [Tags de classificacao na Corpo · semana (discutir, nao persistir v1)](#tags-de-classificacao-na-corpo--semana-discutir-nao-persistir-v1)
- [Consistencia com daily](#consistencia-com-daily)

## Vocabulario de secoes (nomes canonicos)

Os nomes abaixo sao o vocabulario fixo de cada secao do weekly — sao **conteudo de texto** (como a secao se chama), nao especificacao de tipografia (cor, fonte e estilo sao do front). O front pode aplicar qualquer enfase visual; o que esta fixo aqui e o **nome** e a **redacao**.

**Redacao do nome:** sentence case com ponto final (ex: "Lide da semana."), exceto o nome do ano ("2026", sem ponto).

### Vocabulario aprovado (weekly)

| Secao | Nome canonico | v1 enxuta |
|---|---|---|
| Identidade da semana | (sem nome textual — a propria "semana 16" e o destaque) | persistido |
| Narrativa/aposta da semana | "Lide da semana." | persistido (Tese) |
| Cruzamento criativo | "Insight · cruzamento." | persistido (Insight) |
| 5 dias seg-sex | "Orquestra da semana." | persistido (Orquestra) |
| Tres focos da semana | "Foco da semana." | persistido (Foco) |
| Pre-mortem com mitigacao | "Riscos & fogos." | persistido (Riscos) |
| Filtro estrategico antes de comecar | "Preflight · antes de comecar." | persistido (Preflight) |
| Retrospectiva da semana | "Review." | persistido (Review) |
| Agregados de saude/treino | "Corpo · semana." | discutir, nao persistir (v1) |
| Critério da semana | "Criterio de vitoria." | discutir, nao persistir (v1) |
| Deadlines externos ancorados | "Prazos duros." | discutir, nao persistir (v1) |
| Metas trimestrais | "Metas Q2 2026." | discutir, nao persistir (v1) |

### Micro-headers dentro da Orquestra

Quando a Orquestra detalha o dia, usar estes nomes curtos para os blocos internos (texto, sem caixa-alta imposta — o front decide a forma):
- "manha · deep"
- "manha · prep"
- "tarde · meetings"
- "tarde · deep (3h)"
- "entrega"

### Legado (nao usar no weekly)

Estes nomes sao do daily e nao aparecem no weekly:

| Daily | Weekly substituto |
|---|---|
| "Lide do dia." | "Lide da semana." |
| "Tres inadiaveis." | "Foco da semana." |
| "Agenda." | "Orquestra da semana." |
| "Amanha." | "Preflight · antes de comecar." |
| "Foco do dia." (legado v1.3) | "Lide da semana." |

### Nunca usar (na redacao do nome)

- Dois-pontos no fim (`Lide da semana:`)
- Travessao (`— Lide da semana`)
- Colchetes (`[Lide da semana]`)
- Emoji como prefixo

## Tom da Tese da semana

**Terceira pessoa, tempo presente, tom FT (Financial Times) argumentativo.**

A Tese e uma **aposta editorial** — nao descreve o que aconteceu nem o que vai fazer, mas **argumenta o que a semana compra**.

### Comparativo

| Errado (lista descritiva) | Correto (aposta argumentativa) |
|---|---|
| "Vou fechar o m7-controle, fazer 3 treinos, e publicar a skill." | "A S17 aposta no **fechamento do m7-controle** com a diretoria para destravar **o desdobramento de metas Q2**, apos a S16 ter validado o pipeline E2-E6." |
| "Semana cheia de reunioes e entregas importantes." | "A semana inverte a carga: menos horas, mais densidade — qua 15 blindada como maker day sustenta o **Foco da semana**, o resto e execucao." |
| "Preciso preparar a apresentacao e cuidar do sono." | "A Tese sustenta que **apresentacao de sex > tudo** — qui 17h vira ancoragem imovel de ensaio, e o **sono ≥ 7h de seg a qui** e condicao, nao aspiracao." |

### Amarracao obrigatoria

A Tese deve conter pelo menos 2 dos 3 elementos:
1. **Referencia a retrospectiva S-1** (o que foi destravado ou aprendido)
2. **Referencia a Q2** (qual objetivo avanca, ou qual marco parcial)
3. **Implicacao/destrave** (o que essa semana abre para as proximas)

### Extensao

200-400 caracteres. Abaixo vira telegrama; acima vira relatorio.

## Tom do Insight · cruzamento (semanal)

Mesmas regras da daily (provocativo, aforistico, sem conclusao). Ver [insight-cruzamento.md](insight-cruzamento.md).

**Especificidade weekly:** o cruzamento tensiona **dilemas estrategicos semanais** (direcao, alocacao, delegacao), nao dilemas de execucao diaria. Exemplos:

- Weekly: "Shape Up define Appetite antes do problema, GPD pergunta Why depois — sao perguntas diferentes sobre **quanto investir** nesta semana e **onde esta a causa-raiz** do que travou na S-1."
- Daily: "Shape Up × GPD — quanto vale investigar? vs por que existe?"

A weekly tende a ser mais longa (200-280 chars) por carregar o horizonte maior.

## Criterio de vitoria · estrutura (discutir, nao persistir v1)

> **v1 enxuta:** os 4 checks sao **discutidos** na conversa, nao persistidos no objeto canonico. As regras de redacao abaixo valem para essa discussao.

**4 checks binarios. Cada um cabe em 1 linha.**

Formato por check:
```
[ ] <Outcome verificavel com verbo de estado>
```

### Regras de redacao

- **Verificavel**: binario (feito / nao feito). Nao "avancar" mas "publicar", "aprovar", "entregar".
- **Conciso**: maximo 40 chars por check. Mais longo vira paragrafo.
- **Verbo de estado no final**: "WBR Invest **aprovado**", "skill **publicada**", "treinos **completos**".

### Exemplos

Bom:
```
[ ] WBR Invest aprovado pela diretoria
[ ] Cards de Performance em producao
[ ] Weekly planner skill publicada
[ ] 3 treinos longos + sono medio ≥ 7h
```

Ruim:
```
[ ] Avancar no m7-controle                  (nao e binario)
[ ] Trabalhar no planejamento da semana     (vago)
[ ] Cuidar do corpo e da saude              (sem criterio)
[ ] Entregar 5 coisas                       (lista disfarcada)
```

## Orquestra · tema do dia

O **tema** de cada dia e uma linha curta que captura o **papel narrativo** daquele dia na semana.

### Regras

- **Sentence case, sem ponto final** (e titulo de secao, nao frase)
- **1 linha, maximo 30 chars**
- Sem numero (o dia ja tem data)

### Vocabulario recomendado

- `weekly review & kickoff` (seg, abrir a semana)
- `alinhamento tecnico` (ter, 1:1s)
- `maker day · codar` (qua, deep work)
- `ritual & presenca` (qui, reunioes estruturadas)
- `dia D · diretoria` (sex, evento externo)
- `buffer & shutdown` (sex tarde, fechar a semana)
- `plano & prep` (seg, planejar)
- `foco profundo` (qua/qui, quando ha bloco 4h+)

### Anti-padroes

| Ruim | Melhor |
|---|---|
| "Segunda (dia de planejamento do que precisa fazer)" | "weekly review & kickoff" |
| "deep work para codar weekly-planner" (muito longo) | "maker day · codar" |
| "MEETINGS" (caixa alta, sem narrativa) | "ritual & presenca" |

## Foco da semana · criterio "pronto quando"

Cada item do Foco tem **2 partes de texto**:
1. **Titulo** — frase condensada, com as entidades-ancora identificadas (a enfase visual e do front)
2. **Criterio "pronto quando"** — linha curta abaixo

### Exemplo (texto)

- Titulo: `Fechar WBR de Investimentos com Cards em producao`
- Criterio: `pronto quando: diretoria aprova sex · cards publicados`

### Regras do "pronto quando"

- Inicia sempre com `pronto quando:` em minusculo
- Verbo no **presente** (aprova, publica, fecha) — estado, nao acao futura
- Separar multiplas condicoes com `·`
- Max 50 chars

### Anti-padroes

| Ruim | Melhor |
|---|---|
| "pronto quando: tiver avancado" | "pronto quando: diretoria aprova sex" |
| "pronto quando o Pedro responder..." | "pronto quando: resposta Pedro + PR merged" |
| Foco sem "pronto quando" | Obrigatorio — sem isso vira tema |

## Prazos duros · ancoragem (discutir, nao persistir v1)

> **v1 enxuta:** os Prazos duros sao **discutidos**, nao persistidos como secao. As regras de ancoragem abaixo valem para a discussao e para quando integra-los a Orquestra/Riscos.

Cada prazo e ancorado a um **dia especifico**. Texto canonico do prazo:

```
<dia da semana abreviado> <data> · <titulo da entrega> [· +Nd atraso]
```

Exemplo: `seg 13 · Consolidar receitas comissionamento 04/26 · +3d atraso`

### Regras de redacao

- Sempre indicar o dia-ancora (seg/ter/qua/qui/sex + numero)
- Status atrasado sempre como `+Nd atraso`

## Riscos · mitigacao acionavel

Cada risco tem **2 linhas de texto**:

```
<Titulo do risco>
mitigacao: <acao concreta com verbo>
```

### Regras da mitigacao

- **Verbo imperativo**: escalar, bloquear, dormir, avisar, criar
- **Especificidade temporal**: "na ter", "qui 17h", "antes de sex"
- **Multiplas acoes separadas por `;`**

### Exemplos

Bom:
```
SQL consorcios parado no Rafa ha 5d
mitigacao: escalar com Fernando na ter; bloquear 1h qua para alternativa manual

Sono medio em queda · pode comprometer sex
mitigacao: dormir 22h30 na qui; sem telas depois das 21h
```

Ruim:
```
Muita coisa para fazer
mitigacao: me organizar melhor          (generico)

Pedro pode nao responder
mitigacao: aguardar                      (nao e mitigacao, e resignacao)
```

## Preflight · respostas

Cada pergunta do Preflight tem **resposta em 1-2 linhas**.

### Exemplo (texto)

- Pergunta: `O que define vitoria nesta semana?`
- Resposta: `Cards aprovados pela diretoria e publicados em producao na sex — o resto e consequencia.`

### Regras das respostas

- **Sentence case, ponto final obrigatorio** (sao frases, nao labels)
- **Concretas**: nome de projeto, dia, hora
- **1-2 linhas** — se passa disso, nao e preflight, e tese

### Templates por pergunta

1. **O que define vitoria?** → `<outcome concreto> — <frase condensando o resto>`
   Ex: "Cards aprovados pela diretoria e publicados em producao na sex — o resto e consequencia."

2. **Onde esta o deep work?** → `<dia(s) + horas bloqueadas> · <qualificador imovel>`
   Ex: "Qua 15 blindada (7h total) · manhas de seg e ter (2h cada) · nao dilua."

3. **Onde vou dizer nao?** → `<item 1> · <item 2> [· <item 3>]`
   Ex: "Qualquer convite para qua 15 · 1:1s novos com assessores (remarcar p/ S17)."

4. **Qual o maior risco?** → `<risco> — <mitigacao imediata>`
   Ex: "Chegar na sex sem ensaiar a apresentacao — forcar ensaio na qui 17h, sem excecao."

### Anti-padroes

| Ruim | Melhor |
|---|---|
| Resposta em prosa longa (3+ linhas) | Condensar em 1-2 linhas |
| "Nao sei ainda" | Se nao sabe, a regra nao foi cumprida — voltar e preencher |
| Resposta sem entidade concreta | Colocar dia/hora/projeto especifico |

## Numeros no texto

### Regras (iguais ao daily)

- Numeros importantes sao identificados como metricas no texto (a enfase visual e do front)
- Nunca escrever numeros por extenso dentro de dados

### Numeros especificos do weekly

| Contexto | Formato |
|---|---|
| Semana do ano | "semana 16", "S17" (abreviado) |
| TSS total | "TSS 320" (sem unidade explicita) |
| Sono medio | "7.2h", "6.4h" (1 casa decimal) |
| TSB | "+5", "-12" (sempre com sinal) |
| Peso delta | "+0.3kg", "-0.6kg" (sempre com sinal + unidade) |
| Confidence Q2 | "65%", "30%" (percentual inteiro) |

## Metadata de tempo semanal

### Vocabulario canonico

| Contexto | Forma correta |
|---|---|
| Semana alvo atual | "esta semana" |
| Semana passada | "S-1", "semana passada" |
| Proxima semana | "S+1", "proxima semana" |
| Semana especifica | "S17", "semana 17" |
| Range da semana | "13-17 abril" (com traco, nao "13 a 17") |
| Dia da semana no planner | "seg 13", "ter 14", etc. (abreviado + numero) |
| Dia da semana em prosa | "segunda", "terca", "sexta" (por extenso) |

### Nunca usar

- "D-1", "D+3" (jargao de projeto, nao editorial)
- "week" em ingles
- "13/04 a 17/04" (formato numerico)
- "semana do dia 13 ao 17" (preposicional)

## Dia da semana e mes

### Formato de data (range da semana)

Sempre: `<inicio> — <fim> <mes-minusculo>`

Correto:
- `13 — 17 abril`
- `20 — 24 abril`
- `27 abril — 1 maio` (quando cruza mes)

Nunca:
- `13/04 - 17/04` (numerico)
- `13 Abril a 17 Abril` (capitalizado + preposicao)
- `April 13 - 17` (ingles)

### Dias da semana (na Orquestra)

Texto canonico de cada dia: `<weekday-3-letras> <numero-dia>` — ex.: `seg 13`, `ter 14`, `qua 15`, `qui 16`, `sex 17`. O destaque do dia atual (dia de geracao do weekly) e responsabilidade do front; aqui basta identificar qual e o dia atual.

### Sem fim de semana

**Regra estrita**: o weekly cobre apenas seg-sex. Nao incluir sab/dom na Orquestra nem na Agenda. Se houver compromisso familiar no fim de semana que impacta a semana, mencionar no Preflight (resposta ao "Onde vou dizer nao?") ou na Tese — nunca como coluna extra.

## Nome da semana

### Conteudo de identidade da semana

Os campos de texto que identificam a semana (o front decide a forma):
- dia/data de geracao: `Sexta-feira · 17 abril`
- numero da semana: `semana 16`
- range: `13 — 17 abril`
- meta de contexto: `Q2 · sem. 3/13 · 36 restantes` (no formato `Q{N} · sem. {W}/{TOTAL} · {N} restantes`)

### Abreviacao no texto corrente

- Em referencias: `S16`, `S17` (sem ponto)
- Em labels: `sem. 3/13` (com ponto, minusculo)

## Tags de classificacao na Corpo · semana (discutir, nao persistir v1)

> **v1 enxuta:** Corpo · semana e **discutido**, nao persistido. As regras de redacao das tags valem para a discussao.

Cada KPI de Corpo · semana recebe uma **tag de 1 palavra** classificando o status. As regras de redacao:

### Vocabulario fixo (nao inventar sinonimos)

As tags sao **fixas por KPI** — sao termos tecnicos de treino (bandas de Banister para TSB, por exemplo), nao adjetivos livres. Ver matriz completa em [extracao-dados.md secao 4](extracao-dados.md#4-corpo--semana-trainingpeaks-mcp--opcional-nao-persistido-na-v1).

| KPI | Tags validas |
|---|---|
| peso Δ | `estável`, `em queda`, `subindo` |
| sono medio | `ideal`, `ok`, `baixo` |
| TSS total | `saudável`, `leve`, `pesado`, `crítico` |
| TSB | `produtivo`, `neutro`, `fresco`, `overreach`, `destreino` |

### Regras de redacao

- **Uma palavra** (ou no maximo "em queda" = 2 palavras mas 1 conceito)
- **Sem parenteses**
- **Sem pontos finais**
- **Sem acronimos nao-listados**
- **Minusculas** exceto se for termo tecnico estrangeiro (ex: `overreach` — termo tecnico do metodo Banister, fica minusculo mesmo assim por consistencia)
- Se o dado esta ausente, a tag e **totalmente omitida** (nao gerar tag vazia)

### Anti-padroes

| Ruim | Melhor |
|---|---|
| `Saudavel` | `saudável` (mesma grafia da matriz) |
| `sobrecarga funcional` | `pesado` (usar termo da matriz) |
| `ok (quase ideal)` | `ok` (sem parentese) |
| `neutro.` | `neutro` (sem ponto) |
| `?` quando dado falta | Omitir tag totalmente |

## Consistencia com daily

Onde a skill compartilha vocabulario de texto com a daily, **usar identicamente**:
- mesmo criterio de identificacao de entidades-ancora no texto
- mesmos rotulos de metrica inline para numeros
- mesma redacao de nome de secao

Onde difere, **explicitar**: Foco da semana (weekly) vs MITs (daily), Preflight (weekly) vs Amanha (daily), Tese / Lide da semana (weekly) vs Lide do dia (daily).
