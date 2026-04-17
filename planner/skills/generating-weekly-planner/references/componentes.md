# Componentes centrais (weekly)

Especificacao de cada componente do sistema weekly. Use estas classes CSS (definidas em `tokens.css`) em vez de inventar novas.

## Indice

- [Layout geral · 4 bands fit-screen](#layout-geral--4-bands-fit-screen)
- [BAND 1 · Header (contexto)](#band-1--header-contexto)
  - [1. Semana hero](#1-semana-hero)
  - [2. Lide da semana](#2-lide-da-semana)
  - [3. Insight · cruzamento](#3-insight--cruzamento)
  - [4. Ano · 52 semanas](#4-ano--52-semanas)
  - [5. Corpo · semana](#5-corpo--semana)
- [BAND 2 · Orquestra (5 dias)](#band-2--orquestra-5-dias)
  - [6. Coluna de dia](#6-coluna-de-dia)
- [BAND 3 · Compromissos](#band-3--compromissos)
  - [7. Tres grandes da semana](#7-tres-grandes-da-semana)
  - [8. Criterio de vitoria](#8-criterio-de-vitoria)
  - [9. Prazos duros](#9-prazos-duros)
  - [10. Riscos & fogos](#10-riscos--fogos)
  - [11. Metas Q2](#11-metas-q2)
- [BAND 4 · Preflight](#band-4--preflight)
  - [12. Preflight grid](#12-preflight-grid)
- [Utilitarios transversais](#utilitarios-transversais)

## Layout geral · 4 bands fit-screen

O weekly tem **4 bands horizontais empilhadas** dentro de um fit-screen adaptativo (100vw × 100vh, baseline de design 1440×1000):

```
body (flex column, padding 28px 32px, gap 22px, height 1000px fixed)
├── BAND 1 · Header       (flex-shrink:0, ~180px)
├── BAND 2 · Orquestra    (flex:1, cresce para empurrar preflight ao fundo)
├── BAND 3 · Compromissos (flex-shrink:0, ~210px)
└── BAND 4 · Preflight    (flex-shrink:0, ~100px, ancorado ao fundo)
```

**Chave do fit-screen:** `flex:1` na Orquestra (Band 2) empurra Band 3 e Band 4 para baixo. Se a Orquestra for mais compacta que o espaco disponivel, ela CRESCE preenchendo — e o Preflight sempre fica ancorado ao limite inferior.

Divisores horizontais finos (`0.5px solid --divider`) separam as bands.

## BAND 1 · Header (contexto)

**Classe:** `.band-1` (flex-row, gap 24px, align-items flex-start, padding-bottom 18px, border-bottom fino, min-height 180px)

Ordem fixa das zonas (esquerda para direita):

| # | Zona | Classe | Largura | Proposito |
|---|---|---|---|---|
| 1 | Semana | `.band-1__semana` | 220px fixa | Hero visual da identidade da semana |
| 2 | Lide | `.band-1__lide` | flex:1 | Aposta argumentativa (~280 chars) |
| 3 | Insight | `.band-1__insight` | 240px fixa | Cruzamento de frameworks |
| 4 | Ano | `.band-1__ano` | 160px fixa | Grid 52 semanas (4 linhas = Q1..Q4) |
| 5 | Corpo | `.band-1__corpo` | 150px fixa | 4 KPIs semanais agregados |

### 1. Semana hero

**Classes:** `.band-1__semana` + `.band-1__semana-weekday` + `.band-1__semana-hero` + `.band-1__semana-word` + `.band-1__semana-number` + `.band-1__semana-range` + `.band-1__semana-meta`

Hero da identidade. O **numero** da semana e o protagonista (72px Georgia light), "semana" vira label silencioso (22px italic muted).

```html
<div class="band-1__semana">
  <div class="band-1__semana-weekday">Sexta-feira &middot; 17 abril</div>
  <div class="band-1__semana-hero">
    <span class="band-1__semana-word">semana</span>
    <span class="band-1__semana-number">16</span>
  </div>
  <div class="band-1__semana-range">13 <span class="dash">&mdash;</span> 17 <em>abril</em></div>
  <div class="band-1__semana-meta">Q2 &middot; sem. 3/13 &middot; 36 restantes</div>
</div>
```

### 2. Lide da semana

**Classes:** `.band-1__lide` + `.band-1__lide-body`

Paragrafo jornalistico argumentativo de 2-4 frases (200-400 chars). Entidades importantes em `<em>` terracota italic. Precedido pelo label `.section-label`.

```html
<div class="band-1__lide">
  <div class="section-label">Lide da semana.</div>
  <p class="band-1__lide-body">
    Bruno encerra o mes de testes do <em>m7-controle</em> com a apresentacao para a diretoria na <em>sexta as 10h</em>, destravando a publicacao dos Cards de Performance em producao. No corpo, fecha a semana com tres treinos longos e <em>TSS 320</em>.
  </p>
</div>
```

### 3. Insight · cruzamento

**Classes:** `.band-1__insight` + `.band-1__insight-top` + `.band-1__insight-shuffle` + `.band-1__insight-body` + `.band-1__insight-cite`

Identico ao daily mas com conteudo de tensionamento semanal. Ver [insight-cruzamento.md](insight-cruzamento.md) para geracao.

```html
<div class="band-1__insight">
  <div class="band-1__insight-top">
    <div class="section-label">Insight &middot; cruzamento.</div>
    <div class="band-1__insight-shuffle">&#8635;</div>
  </div>
  <p class="band-1__insight-body">
    OKR tem cadencia trimestral, Scrum tem cadencia quinzenal &mdash; a semana nao e ancora natural de nenhum dos dois. <em>"O que move o Q2?"</em> vs <em>"o que entrega na sprint?"</em>
  </p>
  <div class="band-1__insight-cite">OKR &middot; Doerr &times; Scrum &middot; Sutherland</div>
</div>
```

### 4. Ano · 52 semanas

**Classes:** `.band-1__ano` + `.band-1__ano-title` + `.band-1__ano-title-meta` + `.band-1__ano-quarters` + `.band-1__ano-grid` + `.band-1__ano-grid-row`

Grid de **4 linhas × 13 semanas** (cada linha = 1 trimestre). Semana atual destacada com `.is-current-week` (accent + bg-elevated + radius 3px). Semanas passadas do Q atual com `.is-past-week`. Semanas futuras do Q atual com `.is-future`. Semanas de Qs passados com `.is-past-q`.

```html
<div class="band-1__ano">
  <div class="band-1__ano-title">
    <div class="section-label">2026</div>
    <div class="band-1__ano-title-meta">(Q2 &middot; abr&ndash;jun)</div>
  </div>

  <div class="band-1__ano-quarters">
    <div>Q1</div>
    <div class="is-current-q">Q2</div>
    <div>Q3</div>
    <div>Q4</div>
  </div>

  <div class="band-1__ano-grid">
    <!-- Q1: weeks 1-13 (is-past-q) -->
    <div class="band-1__ano-grid-row">
      <div class="is-past-q">1</div>
      <!-- ... 12 mais ... -->
      <div class="is-past-q">13</div>
    </div>
    <!-- Q2: weeks 14-26 (mix de past-week, current-week, future) -->
    <div class="band-1__ano-grid-row">
      <div class="is-past-week">14</div>
      <div class="is-past-week">15</div>
      <div class="is-current-week">16</div>
      <div class="is-future">17</div>
      <!-- ... -->
    </div>
    <!-- Q3: weeks 27-39 (is-future) -->
    <!-- Q4: weeks 40-52 (is-future) -->
  </div>
</div>
```

**Regras de coloracao:**
- Q atual (Q2) em terracota `--accent-primary`; outros em `--text-subtle`
- Semana atual (16) com fundo `--bg-elevated` + radius 3px + terracota
- Semanas passadas do Q atual em `--text-secondary`
- Semanas futuras em `--text-primary`
- Semanas de Qs passados em `--text-subtle`

### 5. Corpo · semana

**Classes:** `.band-1__corpo` + `.band-1__corpo-row` + `.band-1__corpo-label` + `.band-1__corpo-value` + `.band-1__corpo-number` + `.band-1__corpo-unit` + `.band-1__corpo-tag` (v1.8.0)

Label "Corpo · semana." em azul petroleo (`.section-label--body`). **4 rows em grid 3-col** (`48px 1fr auto`): label esquerda, valor centro alinhado a direita, tag com classificacao no fim. Numeros em Inter sans 20px tabular. Tag em Georgia italic 10px.

**Ordem fixa dos KPIs (v1.8.0):** `peso Δ → sono medio → TSS total → TSB` (identica a daily para paridade de leitura).

```html
<div class="band-1__corpo">
  <div class="section-label section-label--body">Corpo &middot; semana.</div>

  <!-- 1. Peso Delta -->
  <div class="band-1__corpo-row">
    <div class="band-1__corpo-label">peso &Delta;</div>
    <div class="band-1__corpo-value">
      <div class="band-1__corpo-number">&minus;0.6</div>
      <div class="band-1__corpo-unit">kg</div>
    </div>
    <div class="band-1__corpo-tag band-1__corpo-tag--body">em queda</div>
  </div>

  <!-- 2. Sono medio -->
  <div class="band-1__corpo-row">
    <div class="band-1__corpo-label">sono medio</div>
    <div class="band-1__corpo-value">
      <div class="band-1__corpo-number band-1__corpo-number--alert">6.4</div>
      <div class="band-1__corpo-unit">h</div>
    </div>
    <div class="band-1__corpo-tag band-1__corpo-tag--alert">baixo</div>
  </div>

  <!-- 3. TSS total -->
  <div class="band-1__corpo-row">
    <div class="band-1__corpo-label">TSS total</div>
    <div class="band-1__corpo-value">
      <div class="band-1__corpo-number band-1__corpo-number--body">320</div>
    </div>
    <div class="band-1__corpo-tag band-1__corpo-tag--body">saudável</div>
  </div>

  <!-- 4. TSB -->
  <div class="band-1__corpo-row">
    <div class="band-1__corpo-label">TSB</div>
    <div class="band-1__corpo-value">
      <div class="band-1__corpo-number band-1__corpo-number--body">&minus;12</div>
    </div>
    <div class="band-1__corpo-tag band-1__corpo-tag--body">produtivo</div>
  </div>
</div>
```

**Exemplo de fallback (TP MCP indisponivel ou dado ausente):**

```html
<!-- Valor como travessao + tag omitida -->
<div class="band-1__corpo-row">
  <div class="band-1__corpo-label">peso &Delta;</div>
  <div class="band-1__corpo-value">
    <div class="band-1__corpo-number band-1__corpo-number--empty">&mdash;</div>
  </div>
  <!-- nao renderizar tag quando nao ha dado -->
</div>
```

**Regras (detalhadas em [extracao-dados.md](extracao-dados.md) secao 4):**
- Valor e tag **compartilham a mesma classe CSS de cor** (coerencia visual)
- Tag sempre em 1 palavra, italic, `white-space: nowrap`
- Dado ausente: numero `&mdash;` com `--empty`, tag omitida (nunca inventar)

**Mapeamento rapido das tags** (ver matriz completa em extracao-dados.md):
- **peso Δ**: `estável` (<=1kg) · `em queda` (< -1kg, body) · `subindo` (> +1kg, warn)
- **sono medio**: `ideal` (>=7h, body) · `ok` (6-7h) · `baixo` (<6h, alert)
- **TSS total**: `saudável` (150-450, body) · `leve` (<150, warn) · `pesado` (>450, alert) · `crítico` (0 em 3+ dias, alert)
- **TSB**: `produtivo` (-30 a -10, body) · `neutro` (-10 a +5) · `fresco` (+5 a +25, warn) · `overreach` (<-30, alert) · `destreino` (>+25, alert)

## BAND 2 · Orquestra (5 dias)

**Classe:** `.band-2` (flex column, gap 14px, `flex:1` — cresce para empurrar preflight ao fundo)

Contém:
- `.band-2__header` (section-header + meta da orquestra)
- `.band-2__grid` (flex-row, gap 20px, align-items stretch, `flex:1` — cresce para que dias se estiquem verticalmente)

```html
<section class="band-2">
  <div class="section-header">
    <div class="section-label">Orquestra da semana.</div>
    <div class="section-header__meta">5 dias &middot; 12 meetings &middot; <em>18h deep work</em> &middot; 14h shallow</div>
  </div>
  <div class="band-2__grid">
    <!-- 5 colunas de dia -->
  </div>
</section>
```

### 6. Coluna de dia

**Classes:** `.day` + `.day--today` (modifier para dia atual) + sub-classes internas

Cada coluna tem **6 blocos verticais** ordenados:

1. **day-head** (weekday + numero + energia)
2. **tema** (italic terracota, 1 linha)
3. **deep block** (label + conteudo)
4. **meetings block** (label + lista de compromissos)
5. **spacer** (espaço automatico via `margin-top:auto` na entrega)
6. **entrega** (label + frase italic terracota, alinhada ao fundo da coluna)

```html
<div class="day">
  <!-- Head -->
  <div class="day__head">
    <div class="day__head-title">
      <span class="day__weekday">seg</span>
      <span class="day__number">13</span>
    </div>
    <div class="day__energia">alta</div>
  </div>

  <!-- Tema -->
  <div class="day__tema">weekly review &amp; kickoff</div>

  <!-- Manha · Deep -->
  <div class="day__block">
    <div class="day__block-label">manha &middot; deep</div>
    <div class="day__block-body">Revisar <em>metas Q2</em> e fechar plano da semana 16.</div>
  </div>

  <!-- Tarde · Meetings -->
  <div class="day__block">
    <div class="day__block-label">tarde &middot; meetings</div>
    <div class="day__meetings">
      <div class="day__meeting">
        <span class="day__meeting-hour">14h</span>
        <span class="day__meeting-title">Kickoff WBR Invest</span>
      </div>
      <div class="day__meeting">
        <span class="day__meeting-hour">16h</span>
        <span class="day__meeting-title">1:1 Fernando</span>
      </div>
    </div>
  </div>

  <!-- Entrega (ancorada ao fundo via margin-top:auto) -->
  <div class="day__entrega">
    <div class="day__block-label">entrega</div>
    <div class="day__entrega-body">Plano semanal fechado no planner</div>
  </div>
</div>
```

### Modifier · dia atual (hoje)

**Classe:** `.day--today`

Aplicada na coluna do dia em que o weekly esta sendo gerado (ou no "dia D" da semana se houver um). Efeito visual: border-top em terracota + weekday/number em accent + tema em italic accent.

```html
<div class="day day--today">
  <div class="day__head">
    <div class="day__head-title">
      <span class="day__weekday">sex &middot; hoje</span>
      <span class="day__number">17</span>
    </div>
    <div class="day__energia">alta</div>
  </div>

  <div class="day__tema">dia D &middot; diretoria</div>
  <!-- ... mesmo pattern ... -->
</div>
```

### Modifier · dia protegido (maker day)

**Classe:** `.day--protected`

Para dias com 0-1 meetings. No lugar da lista de meetings, um placeholder `"sem meetings · dia protegido"` em italic muted.

```html
<div class="day__meetings day__meetings--protected">
  <div class="day__meetings-empty">
    <span>&mdash;</span>
    <span><em>sem meetings &middot; dia protegido</em></span>
  </div>
</div>
```

### Valores validos de energia

Exibido no canto superior direito do day__head:

- `alta` · default
- `media` · default
- `baixa` · muted
- `alta · deep` · quando dia e maker day
- `media · prep` · quando dia e preparacao para evento grande
- `alta · D` · quando dia e evento externo (modifier `.day--today` ativo)

## BAND 3 · Compromissos

**Classe:** `.band-3` (flex row, gap 36px, align-items flex-start, padding-top 18px, border-top fino)

3 colunas de compromissos:

| Col | Conteudo | Classe |
|---|---|---|
| A | Tres grandes + Criterio de vitoria | `.band-3__grandes` |
| B | Prazos duros + Metas Q2 | `.band-3__prazos` |
| C | Riscos & fogos | `.band-3__riscos` |

Cada coluna com `flex:1 min-width:0`.

### 7. Tres grandes da semana

**Classes:** `.band-3__grandes` + `.grande__item` + `.grande__roman` + `.grande__body` + `.grande__task` + `.grande__criterio`

Seguem o mesmo padrao dos **Tres inadiaveis** da daily (romanos i./ii./iii.), mas com criterio "pronto quando" abaixo de cada task.

```html
<div class="band-3__grandes">
  <div class="section-header">
    <div class="section-label">Tres grandes da semana.</div>
    <div class="section-header__meta">big 3 &middot; derivados de Q2</div>
  </div>

  <div class="grande__item">
    <div class="grande__roman">i.</div>
    <div class="grande__body">
      <div class="grande__task">Fechar <em>WBR de Investimentos</em> com Cards em producao</div>
      <div class="grande__criterio">pronto quando: diretoria aprova sex &middot; cards publicados</div>
    </div>
  </div>

  <div class="grande__item">
    <div class="grande__roman">ii.</div>
    <div class="grande__body">
      <div class="grande__task">Publicar <em>weekly-planner skill</em> com template + cron</div>
      <div class="grande__criterio">pronto quando: gera planner auto na seg matinal</div>
    </div>
  </div>

  <div class="grande__item">
    <div class="grande__roman">iii.</div>
    <div class="grande__body">
      <div class="grande__task">Bloco <em class="metric--body">3 treinos</em> + sono medio &geq; 7h</div>
      <div class="grande__criterio">pronto quando: TSS 320+ &middot; sono dom validado</div>
    </div>
  </div>
</div>
```

**Regras:**
- Roman numeral em 28px Georgia italic opacity 0.5 terracota
- Slot do roman fixo em 36px (evita wrap de "iii.")
- Task em 13px Georgia line-height 18px
- Criterio em 11px Georgia italic muted (sempre inicia com "pronto quando:")

### 8. Criterio de vitoria

**Classes:** `.band-3__criterio` + `.criterio__item`

Pode viver como bloco separado em Band 1 (opcional) OU integrado na col de Big 3. Convencao weekly: manter em Band 1 ao lado do Corpo ou como coluna propria em Band 3, a escolha do layout final. No template de referencia, Criterio fica na Band 3 como um bloco vertical compacto.

```html
<div class="band-3__criterio">
  <div class="section-label">Criterio de vitoria.</div>
  <ul class="criterio__list">
    <li class="criterio__item">
      <span class="criterio__box">&#9744;</span>
      <span class="criterio__text">WBR Invest aprovado pela diretoria</span>
    </li>
    <li class="criterio__item">
      <span class="criterio__box">&#9744;</span>
      <span class="criterio__text">Cards de Performance em producao</span>
    </li>
    <li class="criterio__item">
      <span class="criterio__box">&#9744;</span>
      <span class="criterio__text">Weekly planner skill publicada</span>
    </li>
    <li class="criterio__item criterio__item--body">
      <span class="criterio__box">&#9744;</span>
      <span class="criterio__text">3 treinos longos + sono medio &geq; <em>7h</em></span>
    </li>
  </ul>
</div>
```

**Regras:**
- Box unicode `&#9744;` (☐) em 9px Inter cor terracota (ou azul petroleo para check de corpo via `--body` modifier)
- Check de corpo usa modifier `.criterio__item--body` → box em azul petroleo

### 9. Prazos duros

**Classes:** `.band-3__prazos` + `.prazo__item` + `.prazo__dia` + `.prazo__titulo` + `.prazo__status`

Cada prazo ancorado a um dia especifico:

```html
<div class="band-3__prazos">
  <div class="section-header">
    <div class="section-label">Prazos duros.</div>
    <div class="section-header__meta">4 deadlines &middot; <span class="alert">1 atrasado</span></div>
  </div>

  <div class="prazo__list">
    <div class="prazo__item prazo__item--atrasado">
      <div class="prazo__dia">
        <span class="prazo__dia-weekday">seg</span>
        <span class="prazo__dia-number">13</span>
      </div>
      <div class="prazo__titulo">Consolidar receitas <em>comissionamento 04/26</em> <span class="prazo__status">&middot; +3d atraso</span></div>
    </div>

    <div class="prazo__item">
      <div class="prazo__dia">
        <span class="prazo__dia-weekday">qua</span>
        <span class="prazo__dia-number">15</span>
      </div>
      <div class="prazo__titulo">Enviar briefing da diretoria para Ana</div>
    </div>

    <div class="prazo__item prazo__item--hoje">
      <div class="prazo__dia">
        <span class="prazo__dia-weekday">sex</span>
        <span class="prazo__dia-number">17</span>
      </div>
      <div class="prazo__titulo"><em>Apresentacao diretoria</em> 10h &middot; m7-controle aprovado</div>
    </div>
  </div>
</div>
```

### 10. Riscos & fogos

**Classes:** `.band-3__riscos` + `.risco__item` + `.risco__titulo` + `.risco__mitigacao`

Lista de pre-mortems com mitigacao. Separador entre items: border-bottom fino.

```html
<div class="band-3__riscos">
  <div class="section-header">
    <div class="section-label">Riscos &amp; fogos.</div>
    <div class="section-header__meta">pre-mortem</div>
  </div>

  <div class="risco__list">
    <div class="risco__item">
      <div class="risco__titulo"><em class="alert">SQL consorcios parado no Rafa ha 5d</em></div>
      <div class="risco__mitigacao">mitigacao: escalar com Fernando na ter; bloquear 1h qua para alternativa manual</div>
    </div>

    <div class="risco__item">
      <div class="risco__titulo"><em>Sono medio em queda &middot; pode comprometer sex</em></div>
      <div class="risco__mitigacao">mitigacao: dormir 22h30 na qui; sem telas depois das 21h</div>
    </div>

    <div class="risco__item">
      <div class="risco__titulo"><em>Qua 15 protegida pode ser invadida</em></div>
      <div class="risco__mitigacao">mitigacao: bloquear agenda seg; avisar time que qua = maker day</div>
    </div>
  </div>
</div>
```

### 11. Metas Q2

**Classes:** `.band-3__metas` + `.meta__row` + `.meta__title` + `.meta__pct` + `.meta__status`

Opcional — pode viver em Band 1 ou Band 3 (decisao de layout). Exibe 2-4 objetivos Q2 com confidence.

```html
<div class="band-3__metas">
  <div class="section-header">
    <div class="section-label">Metas Q2 2026.</div>
    <div class="section-header__meta">sem. 3/13</div>
  </div>

  <div class="meta__list">
    <div class="meta__row">
      <div class="meta__title">Publicar <em>m7-controle</em> em 3 verticais</div>
      <div class="meta__pct">65% <span class="meta__status">&middot; prox</span></div>
    </div>

    <div class="meta__row">
      <div class="meta__title">Desdobrar metas 2026 &middot; 4 verticais</div>
      <div class="meta__pct alert">30% <span class="meta__status alert">&middot; risco</span></div>
    </div>

    <div class="meta__row">
      <div class="meta__title">Maratona junho <em class="metric--body">sub-4h</em></div>
      <div class="meta__pct">50% <span class="meta__status">&middot; ok</span></div>
    </div>
  </div>
</div>
```

## BAND 4 · Preflight

**Classe:** `.band-4` (flex column, gap 10px, padding-top 18px, border-top fino, flex-shrink:0 — **ancorado ao fundo naturalmente**)

Contem section-header + grid horizontal de 4 perguntas.

### 12. Preflight grid

**Classes:** `.band-4` + `.band-4__grid` + `.preflight__item` + `.preflight__pergunta` + `.preflight__resposta`

```html
<section class="band-4">
  <div class="section-header">
    <div class="section-label">Preflight &middot; antes de comecar.</div>
    <div class="section-header__meta">shutdown ritual reverso &middot; 4 perguntas</div>
  </div>

  <div class="band-4__grid">
    <div class="preflight__item">
      <div class="preflight__pergunta">O que define vitoria nesta semana?</div>
      <div class="preflight__resposta">Cards aprovados pela diretoria e publicados em producao na sex &mdash; o resto e consequencia.</div>
    </div>

    <div class="preflight__item">
      <div class="preflight__pergunta">Onde esta o deep work?</div>
      <div class="preflight__resposta">Qua 15 blindada (7h total) &middot; manhas de seg e ter (2h cada) &middot; nao dilua.</div>
    </div>

    <div class="preflight__item">
      <div class="preflight__pergunta">Onde vou dizer nao?</div>
      <div class="preflight__resposta">Qualquer convite para qua 15 &middot; 1:1s novos com assessores (remarcar p/ S17).</div>
    </div>

    <div class="preflight__item">
      <div class="preflight__pergunta">Qual e o maior risco?</div>
      <div class="preflight__resposta">Chegar na sex sem ensaiar a apresentacao &mdash; forcar ensaio na qui 17h, sem excecao.</div>
    </div>
  </div>
</section>
```

**Regras:**
- Grid de 4 colunas flex, gap 36px
- Pergunta em 12px Georgia cor `--text-secondary`
- Resposta em 13px Georgia italic cor `--text-primary`
- Cada coluna `flex:1` para distribuir espaco igual

## Utilitarios transversais

### Section header · pattern compartilhado

Mesmo pattern da daily:

```html
<div class="section-header">
  <div class="section-label">[Nome da secao].</div>
  <div class="section-header__meta">[metadata opcional]</div>
</div>
```

- Label sempre em italic terracota 13px com ponto final
- Meta em Inter 11px italic muted a direita
- Alertas dentro da meta: `<span class="alert">...</span>` em terracota escuro

### Metrica inline

Identico ao daily — `.metric`, `.metric--body`, `.metric--alert` para destacar numeros dentro de paragrafos.

### Cor dinamica por estado

| Estado | Classe / modifier | Cor |
|---|---|---|
| Dia atual na Orquestra | `.day--today` | `--accent-primary` (border-top + weekday + number) |
| Dia protegido | `.day--protected` | default (placeholder em italic muted) |
| Prazo atrasado | `.prazo__item--atrasado` | `--alert` (dia + status) |
| Prazo hoje/alvo | `.prazo__item--hoje` | `--accent-primary` (dia + number em accent) |
| Meta Q2 em risco | `.meta__row .alert` em pct/status | `--alert` |
| Meta Q2 ok | default | neutral |
| Semana atual (grid ano) | `.is-current-week` | `--accent-primary` + `--bg-elevated` |
| KPI de corpo positivo | `.band-1__corpo-number--body` | `--accent-secondary` (azul petroleo) |
| KPI de corpo em alerta | `.band-1__corpo-number--alert` | `--alert` (terracota escuro) |

### Alinhamento da entrega entre dias

Cada coluna de dia tem `display: flex; flex-direction: column` e a `.day__entrega` tem `margin-top: auto`. Isso faz com que todas as entregas se alinhem horizontalmente no fundo das colunas — **criando um "piso" visual ritmico** atraves da Orquestra.

**Nao quebrar isso.** Se a entrega nao esta alinhada, investigar antes de adicionar padding artificial.

## Diferencas vs componentes da daily

| Daily | Weekly | Motivo |
|---|---|---|
| Header 5-zone com Mes calendario | Header 5-zone com Ano (52 semanas) | Horizonte maior → calendario trimestral |
| Body 3-col (Agenda + MITs + Workspace M7) | Band 2 Orquestra 5 cols dia a dia | Orquestracao vs execucao |
| Footer 2-col (Notas + Amanha) | Band 4 Preflight 4 perguntas ancorado | Shutdown reverso vs preview do proximo dia |
| Corpo 3 rows (peso, TSS sem, sono) | Corpo 4 rows (peso Δ, TSS total, sono medio, TSB) | Agregados semanais + TSB |
| Lide do dia | Lide da semana + Tese + Criterio | Aposta argumentativa vs resumo descritivo |
| Tres inadiaveis | Tres grandes + "pronto quando" | Big 3 derivados de Q2 |
| Agenda enumerada hora a hora | Orquestra 5 colunas narrativas | Tempo como espaco vs como linha |
