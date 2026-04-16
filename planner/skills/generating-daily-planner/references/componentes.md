# Componentes centrais

Especificacao de cada componente do sistema. Use estas classes CSS (definidas em `tokens.css`) em vez de inventar novas.

## Indice

- [Layout geral](#layout-geral)
- [HEADER · 5 zonas horizontais](#header--5-zonas-horizontais)
  - [1. Dia](#1-dia)
  - [2. Lide do dia](#2-lide-do-dia)
  - [3. Insight · cruzamento](#3-insight--cruzamento)
  - [4. Mes · mini-calendario](#4-mes--mini-calendario)
  - [5. Corpo · stack vertical](#5-corpo--stack-vertical)
- [BODY · 3 colunas](#body--3-colunas)
  - [6. Section header (label + meta direita)](#6-section-header-label--meta-direita)
  - [7. Agenda enumerada](#7-agenda-enumerada)
  - [8. Tres inadiaveis](#8-tres-inadiaveis)
  - [9. Tarefas ClickUp](#9-tarefas-clickup)
  - [10. Delegadas](#10-delegadas)
- [FOOTER · 2 colunas](#footer--2-colunas)
  - [11. Notas do dia](#11-notas-do-dia)
  - [12. Amanha](#12-amanha)
- [Utilitarios transversais](#utilitarios-transversais)

## Layout geral

O planner tem **tres zonas verticais empilhadas**:

```
header (5 zonas horizontais)
body (3 colunas)
footer (2 colunas)
```

Separadas por divisores horizontais finos. Sem ornamento alem disso.

## HEADER · 5 zonas horizontais

**Classe:** `.header` (flex-row, gap 24px, padding-bottom 18px, border-bottom fino)

Ordem fixa das zonas (esquerda para direita):

| # | Zona | Classe | Largura | Proposito |
|---|---|---|---|---|
| 1 | Dia | `.header__dia` | 220px fixa | Data gigante, ancora visual |
| 2 | Lide | `.header__lide` | flex:1 | Narrativa do dia (~280 chars) |
| 3 | Insight | `.header__insight` | 240px fixa | Cruzamento aleatorio de metodologias |
| 4 | Mes | `.header__mes` | 150px fixa | Mini-calendario do mes |
| 5 | Corpo | `.header__corpo` | 130px fixa | 3 KPIs verticais |

### 1. Dia

**Classes:** `.header__dia` + `.header__dia-weekday` + `.header__dia-main` + `.header__dia-meta`

Hero visual do dia. Data em 56px Georgia light, "abril" em italic terracota. Weekday acima (italic terracota 12px). Meta abaixo (italic 11px muted).

```html
<div class="header__dia">
  <div class="header__dia-weekday">Quinta-feira</div>
  <div class="header__dia-main">16 <em>abril</em></div>
  <div class="header__dia-meta">dia 106/365 · semana 16</div>
</div>
```

### 2. Lide do dia

**Classes:** `.header__lide` + `.header__lide-body`

Paragrafo jornalistico de 2-4 frases (200-400 caracteres). Entidades importantes em `<em>` terracota italic. Precedido pelo label `.section-label`.

```html
<div class="header__lide">
  <div class="section-label">Lide do dia.</div>
  <p class="header__lide-body">
    Bruno revisa as <em>14h</em>, com Pedro e Fernando, o WBR de Investimentos
    para validar o <em>pipeline GPD</em> antes da diretoria de sexta...
  </p>
</div>
```

**Extensao:** 200-400 chars. Menor parece resumo; maior parece relatorio.

### 3. Insight · cruzamento

**Classes:** `.header__insight` + `.header__insight-top` + `.header__insight-shuffle` + `.header__insight-body` + `.header__insight-cite`

Cruzamento aleatorio de metodologias/conceitos. Texto em italic 12px. Citacao das duas fontes em 10px muted. Icone ↻ no topo-direito (affordance para shuffle).

```html
<div class="header__insight">
  <div class="header__insight-top">
    <div class="section-label">Insight · cruzamento.</div>
    <div class="header__insight-shuffle">↻</div>
  </div>
  <p class="header__insight-body">
    Shape Up define um Appetite antes do problema. GPD pergunta Why-Why depois
    &mdash; sao perguntas diferentes: <em>"quanto vale investigar?"</em> vs
    <em>"por que existe?"</em>
  </p>
  <div class="header__insight-cite">Shape Up · Basecamp × GPD · Falconi</div>
</div>
```

**Regra:** cruzar **2 conceitos de fontes diferentes** (ex: Shape Up × GPD, Zettelkasten × OKR). Nunca 3+. Texto provocativo, 150-250 chars.

### 4. Mes · mini-calendario

**Classes:** `.header__mes` + `.header__mes-title` + `.header__mes-title-meta` + `.header__mes-weekdays` + `.header__mes-grid` + `.header__mes-grid-row`

Grid de 7x5 mostrando o mes inteiro. Dia atual destacado com `.is-today` (accent + bg-elevated + radius 6). Dias futuros com `.is-future`. Dias de outros meses ou fins-de-semana muted com `.is-subtle`.

```html
<div class="header__mes">
  <div class="header__mes-title">
    <div class="section-label">Abril</div>
    <div class="header__mes-title-meta">(sem. 16)</div>
  </div>

  <div class="header__mes-weekdays">
    <div>s</div><div>t</div><div>q</div><div>q</div><div>s</div><div>s</div><div>d</div>
  </div>

  <div class="header__mes-grid">
    <div class="header__mes-grid-row">
      <div class="is-subtle">30</div>
      <div class="is-subtle">31</div>
      <div>1</div>
      <div>2</div>
      <div>3</div>
      <div class="is-subtle">4</div>
      <div class="is-subtle">5</div>
    </div>
    <!-- mais 4 rows -->
    <div class="header__mes-grid-row">
      <div>13</div>
      <div>14</div>
      <div>15</div>
      <div class="is-today">16</div>
      <div class="is-future">17</div>
      <div class="is-subtle">18</div>
      <div class="is-subtle">19</div>
    </div>
  </div>
</div>
```

**Regras de coloracao por dia:**
- Dia atual → `.is-today` (terracota + fundo elevated)
- Dias futuros (17+) → `.is-future` (text-primary)
- Dias passados do mes (1-15) → default (text-secondary)
- Fins de semana (sab/dom) → `.is-subtle` (text-subtle)
- Dias de outros meses (30 31 do mes anterior, 1 2 3 do proximo) → `.is-subtle`

### 5. Corpo · stack vertical

**Classes:** `.header__corpo` + `.header__corpo-row` + `.header__corpo-label` + `.header__corpo-value` + `.header__corpo-number` + `.header__corpo-unit`

Label "Corpo." em azul petroleo (`.section-label--body`). Abaixo, 3 rows verticais de KPI: label esquerda, numero direita. Numeros em Inter sans 20px tabular. Sem grafico, sem barra — so numero puro.

```html
<div class="header__corpo">
  <div class="section-label section-label--body">Corpo.</div>

  <div class="header__corpo-row">
    <div class="header__corpo-label">peso</div>
    <div class="header__corpo-value">
      <div class="header__corpo-number">104.8</div>
      <div class="header__corpo-unit">kg</div>
    </div>
  </div>

  <div class="header__corpo-row">
    <div class="header__corpo-label">TSS sem</div>
    <div class="header__corpo-value">
      <div class="header__corpo-number header__corpo-number--body">387</div>
    </div>
  </div>

  <div class="header__corpo-row">
    <div class="header__corpo-label">sono</div>
    <div class="header__corpo-value">
      <div class="header__corpo-number header__corpo-number--alert">6.8</div>
      <div class="header__corpo-unit">h</div>
    </div>
  </div>
</div>
```

**Regras de cor do numero:**
- Dados neutros (peso) → default primary
- Dados de performance/treino (TSS, FTP, VO2, ritmo) → `--body` (azul petroleo)
- Dados em alerta (sono baixo, fadiga alta, semana zerada) → `--alert` (terracota escuro)

## BODY · 3 colunas

**Classe:** `.body` (flex-row, gap 32px, align-items flex-start). Cada coluna: `.body__col` (flex:1, gap 14px).

Composicao fixa:
1. Coluna 1 → Agenda
2. Coluna 2 → Tres inadiaveis + Tarefas ClickUp
3. Coluna 3 → Delegadas

### 6. Section header (label + meta direita)

**Classes:** `.section-header` + `.section-header__meta`

Pattern repetido em toda secao do body/footer: label italic terracota a esquerda, metadata (contadores, status) italic muted a direita.

```html
<div class="section-header">
  <div class="section-label">Agenda.</div>
  <div class="section-header__meta">6 eventos · 8h bloqueadas</div>
</div>
```

Quando houver alerta dentro da meta, envelope no `<span class="alert">`:

```html
<div class="section-header__meta"><span class="alert">2 atrasadas</span> · 8 abertas</div>
```

### 7. Agenda enumerada

**Classes:** `.agenda-enum` + `.agenda-enum__row` + `.agenda-enum__hour` + `.agenda-enum__event`

Lista vertical com **todas** as horas relevantes do dia (normalmente 07:00 a 19:00 de hora em hora, mais meias-horas se houver eventos iniciando em :30). Horas sem evento mostram "—". Hora atual destacada com `--now`. Gap grande antes de uma hora longe da sequencia (ex: 19:00 depois de 14:30).

```html
<div class="agenda-enum">
  <!-- Hora vazia -->
  <div class="agenda-enum__row">
    <div class="agenda-enum__hour agenda-enum__hour--empty">07:00</div>
    <div class="agenda-enum__event agenda-enum__event--empty">&mdash;</div>
  </div>

  <!-- Hora com evento -->
  <div class="agenda-enum__row">
    <div class="agenda-enum__hour">07:30</div>
    <div class="agenda-enum__event">Corrida no parque</div>
  </div>

  <!-- Hora atual (now) -->
  <div class="agenda-enum__row">
    <div class="agenda-enum__hour agenda-enum__hour--now">11:00</div>
    <div class="agenda-enum__event agenda-enum__event--now">1:1 com Pedro · agora</div>
  </div>

  <!-- Entidade destacada dentro do evento -->
  <div class="agenda-enum__row">
    <div class="agenda-enum__hour">09:00</div>
    <div class="agenda-enum__event">Revisao <em>WBR Investimentos</em></div>
  </div>

  <!-- Gap visual antes do proximo (evento distante) -->
  <div class="agenda-enum__row agenda-enum__row--gap">
    <div class="agenda-enum__hour">19:00</div>
    <div class="agenda-enum__event">Jantar em familia</div>
  </div>
</div>
```

### 8. Tres inadiaveis

**Classes:** `.inadiaveis__item` + `.inadiaveis__roman` + `.inadiaveis__task` + `.inadiaveis__meta`. Modificador `--delayed` para atraso.

**Sempre exatamente 3 itens** — forca priorizacao real. Romanos i./ii./iii. em 28px italic terracota opacity 0.5 como ancora visual (token `--fs-roman`). A coluna dos romanos tem 28px fixos, suficiente para ancorar sem esmagar o task ao lado.

```html
<div class="section-header">
  <div class="section-label">Tres inadiaveis.</div>
  <div class="section-header__meta">0/3</div>
</div>

<div class="inadiaveis__item">
  <div class="inadiaveis__roman">i.</div>
  <div class="inadiaveis__task">
    Concluir revisao do <em>WBR de Investimentos</em>
    <span class="inadiaveis__meta">· ate 14h</span>
  </div>
</div>

<div class="inadiaveis__item inadiaveis__item--delayed">
  <div class="inadiaveis__roman">ii.</div>
  <div class="inadiaveis__task">
    Publicar skill do daily planner
    <span class="inadiaveis__meta">· +1d atraso</span>
  </div>
</div>

<div class="inadiaveis__item">
  <div class="inadiaveis__roman">iii.</div>
  <div class="inadiaveis__task">Slides da diretoria</div>
</div>
```

### 9. Tarefas ClickUp

**Classes:** `.tasks` + `.tasks__list` + `.tasks__row` + `.tasks__title` + `.tasks__title-meta` + `.tasks__due` + `.tasks__more`. Modificador `.tasks__row--delayed` para atraso.

Bloco apos "Tres inadiaveis", separado por border-top fino. Lista densa de tarefas do ClickUp atribuidas a mim. Cada linha: titulo + metadata inline (via `.tasks__title-meta`) + data/prazo direita. Linhas atrasadas em alert.

**Regra de metadata (`.tasks__title-meta`):** sempre dois segmentos separados por middot (`·`), **lista primeiro, tag(s) depois** — espelha a hierarquia do ClickUp e evita ambiguidade. Se houver multiplas tags, separar por virgula dentro do segmento tag. Se nao houver tag, mostrar so a lista. Nunca mostrar so a tag sem a lista.

Formato:
```
· <nome da lista> · <tag1>[, <tag2>]
```

Exemplos validos:
- `· Chamados TI · captacao-receita` (1 lista + 1 tag)
- `· Sprint S1 Invest · funil-vendas, alta-prioridade` (1 lista + 2 tags)
- `· Familia` (1 lista, sem tag)

Evitar:
- `· captacao-receita` (so tag, sem lista)
- `· Chamados TI / captacao-receita` (separador diferente)

```html
<div class="tasks">
  <div class="section-header">
    <div class="section-label">Tarefas ClickUp.</div>
    <div class="section-header__meta"><span class="alert">2 atrasadas</span> · 8 abertas</div>
  </div>

  <div class="tasks__list">
    <div class="tasks__row">
      <div class="tasks__title">Revisar PR do m7-controle <span class="tasks__title-meta">· AI Plugins · dev</span></div>
      <div class="tasks__due">hoje</div>
    </div>
    <div class="tasks__row tasks__row--delayed">
      <div class="tasks__title">Responder Bia sobre ferias julho <span class="tasks__title-meta">· Familia · planejamento</span></div>
      <div class="tasks__due">+1d atraso</div>
    </div>
    <div class="tasks__row tasks__row--delayed">
      <div class="tasks__title">TSM-874 Views Cubo ClickHouse Gold <span class="tasks__title-meta">· Chamados TI · captacao-receita</span></div>
      <div class="tasks__due">+75d</div>
    </div>
    <div class="tasks__more">+ 3 tarefas · ver todas ↗</div>
  </div>
</div>
```

**Limite visivel:** 5-6 linhas. Acima disso, truncar com `.tasks__more` ("+ N tarefas · ver todas ↗").

### 10. Delegadas

**Classes:** `.delegadas__group` + `.delegadas__project`. Usa `.tasks__row` e variantes internamente.

Tarefas que voce delegou e precisa acompanhar. **Agrupadas por projeto** (unico bloco no sistema com subgrupos). Cada projeto tem seu mini-header italic muted. Rows seguem o mesmo padrao de `.tasks__row` (titulo · pessoa + due).

```html
<div class="section-header">
  <div class="section-label">Delegadas.</div>
  <div class="section-header__meta"><span class="alert">1 atrasada</span> · 7 abertas</div>
</div>

<div class="delegadas__group">
  <div class="delegadas__project">Padronizacao Rituais</div>
  <div class="tasks__row tasks__row--delayed">
    <div class="tasks__title">Validar fluxograma G2.3 <span class="tasks__title-meta">· Ana</span></div>
    <div class="tasks__due">ontem</div>
  </div>
  <div class="tasks__row">
    <div class="tasks__title">Testar material-generator <span class="tasks__title-meta">· Paulo</span></div>
    <div class="tasks__due">hoje</div>
  </div>
</div>

<div class="delegadas__group">
  <div class="delegadas__project">Desdobramento Metas 2026</div>
  <!-- ... -->
</div>
```

## FOOTER · 2 colunas

**Classe:** `.footer` (flex-row, gap 32, padding-top 18, border-top fino).

Composicao fixa:
1. Coluna 1 (flex:1) → Notas do dia
2. Coluna 2 (500px fixa) → Amanha

### 11. Notas do dia

**Classes:** `.footer__notas` + `.note` + `.note__bullet` + `.note__text` + `.note__time`.

Ideias capturadas ao longo do dia. Travessao (—) em terracota + texto + hora em Inter tabular direita. Linhas divisoras entre itens.

```html
<section class="footer__notas">
  <div class="section-header">
    <div class="section-label">Notas do dia.</div>
    <div class="section-header__meta">quick capture ↗</div>
  </div>

  <div class="note">
    <span class="note__bullet">—</span>
    <div class="note__text">Transformar planner em skill, gerar HTML via cron matinal.</div>
    <div class="note__time">08:42</div>
  </div>

  <div class="note">
    <span class="note__bullet">—</span>
    <div class="note__text">Shape Up define Appetite antes do problema, GPD pergunta Why depois.</div>
    <div class="note__time">11:30</div>
  </div>
</section>
```

### 12. Amanha

**Classes:** `.footer__amanha` + `.footer__amanha-body`. Spans internos: `em.ancora` (foco) e `em.time` (horarios).

Preview do dia seguinte em prosa. Comeca com "Ancora:" (compromisso mais importante amanha) seguido dos horarios chave inline. Horarios em Inter sans italic terracota via `<em class="time">`.

```html
<section class="footer__amanha">
  <div class="section-header">
    <div class="section-label">Amanha.</div>
    <div class="section-header__meta">sex, 17 abril · 5 eventos</div>
  </div>

  <p class="footer__amanha-body">
    <em class="ancora">Ancora:</em> apresentacao para diretoria as
    <em class="time">10:00</em>, chegar as 09:30 para setup.
    <em class="time">07:00</em> corrida longa 10k.
    <em class="time">14:30</em> review de codigos m7-controle.
  </p>
</section>
```

## Utilitarios transversais

### Metrica inline (dentro de prosa)

**Classes:** `.metric` (terracota padrao), `.metric--body` (azul petroleo), `.metric--alert` (terracota escuro).

Para destacar numeros dentro de paragrafo corrido:

```html
<p>Ativacoes 300k+ em <span class="metric">47</span> de 62, conversao ML em <span class="metric">6.5x</span> o baseline.</p>
```

### Label de secao

**Classe:** `.section-label` (terracota padrao), `.section-label--body` (azul petroleo para Corpo), `.section-label--muted` (cinza para auxiliares).

Sempre em sentence case com ponto final. Exemplos: "Lide do dia.", "Tres inadiaveis.", "Agenda.", "Corpo.", "Delegadas.", "Tarefas ClickUp.", "Insight · cruzamento.", "Notas do dia.", "Amanha.".
