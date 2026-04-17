# Regras de escrita e tom (weekly)

O texto e parte do design. Tom inconsistente quebra o sistema mais rapido que cor errada. Esta referencia estende as regras da daily com labels e estruturas especificas do weekly.

## Indice

- [Labels de secao](#labels-de-secao)
- [Tom da Tese da semana](#tom-da-tese-da-semana)
- [Tom do Insight · cruzamento (semanal)](#tom-do-insight--cruzamento-semanal)
- [Criterio de vitoria · estrutura](#criterio-de-vitoria--estrutura)
- [Orquestra · tema do dia](#orquestra--tema-do-dia)
- [Big 3 · criterio "pronto quando"](#big-3--criterio-pronto-quando)
- [Prazos duros · ancoragem](#prazos-duros--ancoragem)
- [Riscos · mitigacao acionavel](#riscos--mitigacao-acionavel)
- [Preflight · respostas italic](#preflight--respostas-italic)
- [Numeros no texto](#numeros-no-texto)
- [Metadata de tempo semanal](#metadata-de-tempo-semanal)
- [Dia da semana e mes](#dia-da-semana-e-mes)
- [Nome da semana](#nome-da-semana)

## Labels de secao

**Formato canonico:** `<Palavra-inicial em maiuscula><resto em minuscula>.`

Sempre em sentence case com ponto final. Sempre em Georgia italic 13px terracota (via `.section-label`). Exceto os de contexto trimestral/anual que usam cor secundaria ou neutra.

### Vocabulario aprovado (weekly)

| Secao | Label |
|---|---|
| Identidade da semana (zona 1) | Nenhum label textual — a propria "semana 16" e o hero |
| Narrativa/aposta da semana | "Lide da semana." |
| Cruzamento criativo | "Insight · cruzamento." |
| Grid anual de 52 semanas | "2026" (nome do ano, sem ponto) |
| Agregados de saude/treino | "Corpo · semana." (azul petroleo) |
| 5 dias seg-sex | "Orquestra da semana." |
| Weekly Big 3 | "Tres grandes da semana." |
| Critério da semana | "Criterio de vitoria." |
| Deadlines externos ancorados | "Prazos duros." |
| Pre-mortem com mitigacao | "Riscos & fogos." |
| Filtro estrategico antes de comecar | "Preflight · antes de comecar." |
| Metas trimestrais | "Metas Q2 2026." |

### Sub-labels UPPERCASE (Inter, dentro da Orquestra)

Exclusivos para os micro-headers dentro de cada coluna de dia:
- `MANHA · DEEP`
- `MANHA · PREP`
- `TARDE · MEETINGS`
- `TARDE · DEEP (3H)`
- `ENTREGA`

Formato: Inter 9px weight 600 letter-spacing 0.12em text-transform:uppercase color `--text-subtle`. Sao labels tecnicos dentro da narrativa — a unica excecao permitida a caixa alta.

### Legado (nao usar no weekly)

Estes labels sao do daily e nao aparecem no weekly:

| Daily | Weekly substituto |
|---|---|
| "Lide do dia." | "Lide da semana." |
| "Tres inadiaveis." | "Tres grandes da semana." |
| "Agenda." | "Orquestra da semana." |
| "Amanha." | "Preflight · antes de comecar." |
| "Foco do dia." (legado v1.3) | "Lide da semana." |

### Nunca usar

- Dois-pontos no fim (`Lide da semana:`)
- Travessao (`— Lide da semana`)
- Colchetes (`[Lide da semana]`)
- Sublinhado ou bold em vez de italico
- UPPERCASE exceto nos sub-labels da Orquestra
- Emoji como prefixo

## Tom da Tese da semana

**Terceira pessoa, tempo presente, tom FT (Financial Times) argumentativo.**

A Tese e uma **aposta editorial** — nao descreve o que aconteceu nem o que vai fazer, mas **argumenta o que a semana compra**.

### Comparativo

| Errado (lista descritiva) | Correto (aposta argumentativa) |
|---|---|
| "Vou fechar o m7-controle, fazer 3 treinos, e publicar a skill." | "A S17 aposta no **fechamento do m7-controle** com a diretoria para destravar **o desdobramento de metas Q2**, apos a S16 ter validado o pipeline E2-E6." |
| "Semana cheia de reunioes e entregas importantes." | "A semana inverte a carga: menos horas, mais densidade — qua 15 blindada como maker day sustenta os **Big 3**, o resto e execucao." |
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

## Criterio de vitoria · estrutura

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

### Cor dos checkboxes

- Checks de trabalho/foco: terracota (`--accent-primary`)
- Checks de corpo: azul petroleo (`--accent-secondary`)

## Orquestra · tema do dia

O **tema** de cada dia e uma **linha italic** em terracota que captura o **papel narrativo** daquele dia na semana.

### Regras

- **Italic Georgia**, `font-size: 13px`, `color: --accent-primary`
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

## Big 3 · criterio "pronto quando"

Cada Big 3 tem **2 partes**:
1. **Titulo** (frase condensada em terracota italic para entidades)
2. **Criterio "pronto quando"** (linha italic muted abaixo)

### Formato

```html
<div>Fechar <em>WBR de Investimentos</em> com Cards em producao</div>
<div class="criterio">pronto quando: diretoria aprova sex · cards publicados</div>
```

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
| Big 3 sem "pronto quando" | Obrigatorio — sem isso vira tema |

## Prazos duros · ancoragem

Cada prazo e ancorado a um **dia especifico** no formato:

```
<WEEKDAY UPPERCASE> <DATA> | <TITULO DA ENTREGA>
```

### Formato HTML

```html
<div class="prazo">
  <span class="dia">SEG 13</span>
  <span class="titulo">Consolidar receitas <em>comissionamento 04/26</em></span>
  <span class="status atrasado">+3d atraso</span>
</div>
```

### Regras de cor

- Ancora "SEG 13" em `--text-subtle` (neutro)
- Ancora em terracota `--accent-primary` se e o dia atual ou alvo critico
- Ancora em `--alert` se o prazo esta atrasado
- Status atrasado sempre como `+Nd atraso`

## Riscos · mitigacao acionavel

Cada risco tem **2 linhas**:

```
<Titulo do risco em italic>
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

### Cor do titulo do risco

- Default: `--text-primary` (neutro)
- `--alert` quando risco e dependencia atrasada ou bloqueio externo ativo

## Preflight · respostas italic

Cada pergunta do Preflight tem **resposta em 1-2 linhas italic**.

### Formato HTML

```html
<div class="preflight-item">
  <div class="pergunta">O que define vitoria nesta semana?</div>
  <div class="resposta"><em>Cards aprovados pela diretoria e publicados em producao na sex — o resto e consequencia.</em></div>
</div>
```

### Regras das respostas

- **Georgia italic 13px**, cor `--text-primary`
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

- Numeros importantes sempre em italico terracota via `<em class="metric">`
- Azul petroleo (`--body`) para dados de performance/treino
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

Formato: `<WEEKDAY-3-LETRAS> <NUMERO-DIA>`

- `SEG 13`, `TER 14`, `QUA 15`, `QUI 16`, `SEX 17`
- WEEKDAY em Inter 10px weight 600 letter-spacing 0.15em uppercase color `--text-secondary`
- NUMERO em Georgia 32px weight 300 letter-spacing -0.03em color `--text-primary`
- Para sex atual (dia da geracao do weekly): cor `--accent-primary` em ambos + border-top accent na coluna

### Sem fim de semana

**Regra estrita**: o weekly cobre apenas seg-sex. Nao incluir sab/dom na Orquestra nem na Agenda. Se houver compromisso familiar no fim de semana que impacta a semana, mencionar no Preflight (resposta ao "Onde vou dizer nao?") ou na Tese — nunca como coluna extra.

## Nome da semana

### Formato no hero (Zona 1)

```html
<div class="weekday">Sexta-feira · 17 abril</div>
<div class="hero">
  <span class="word">semana</span>
  <span class="number">16</span>
</div>
<div class="range">13 <span class="dash">—</span> 17 <em>abril</em></div>
<div class="meta">Q2 · sem. 3/13 · 36 restantes</div>
```

### Regras

- **"semana"** em Georgia 22px italic `--text-secondary` (label silencioso)
- **"16"** em Georgia 72px weight 300 `--text-primary` (hero puro)
- Weekday no topo em italic terracota (referencia ao dia de geracao)
- Range abaixo em Georgia 13px com mes em italic terracota
- Meta em Georgia 11px italic muted: `Q{N} · sem. {W}/{TOTAL} · {N} restantes`

### Abreviacao no texto corrente

- Em referencias: `S16`, `S17` (sem ponto)
- Em labels: `sem. 3/13` (com ponto, minusculo)

## Tags de classificacao na Corpo · semana (v1.8.0)

A partir da v1.8.0, cada KPI da zona Corpo · semana exibe uma **tag de 1 palavra** a direita do valor, classificando o status. As regras de redacao:

### Vocabulario fixo (nao inventar sinonimos)

As tags sao **fixas por KPI** — sao termos tecnicos de treino (bandas de Banister para TSB, por exemplo), nao adjetivos livres. Ver matriz completa em [extracao-dados.md secao 4](extracao-dados.md#4-corpo--semana-trainingpeaks-mcp).

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
- **Italic Georgia 10px**, mesma cor do numero do KPI
- Se o dado esta ausente (`&mdash;`), a tag e **totalmente omitida** do HTML (nao renderizar tag vazia)

### Anti-padroes

| Ruim | Melhor |
|---|---|
| `Saudavel` | `saudável` (mesma grafia da matriz) |
| `sobrecarga funcional` | `pesado` (usar termo da matriz) |
| `ok (quase ideal)` | `ok` (sem parentese) |
| `neutro.` | `neutro` (sem ponto) |
| `?` quando dado falta | Omitir tag totalmente |

## Consistencia com daily

Onde a skill compartilha vocabulario com a daily, **usar identicamente**:
- `<em>` para entidades destacadas
- Cores `--accent-primary`, `--accent-secondary`, `--alert` com mesmos significados
- `.metric` para numeros inline
- `.section-label` para labels de secao

Onde difere, **explicitar na orquestra**: Big 3 (weekly) vs MITs (daily), Preflight (weekly) vs Amanha (daily), Tese (weekly) vs Lide (daily).
