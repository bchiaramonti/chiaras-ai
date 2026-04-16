---
name: generating-project-status-reports
description: "Generates Status Report PPTX from ROADMAP.md and SPRINT-NN.md files produced by decomposing-goals-into-sprints. Creates executive status slides per active sprint, optional D3 charts (burndown, task completion), and roadmap overview. Uses m7_pptx_lib.py building blocks and D3 chart pipeline. Use when user asks for status report, project update, sprint report, or progress presentation."
---

# Project Status Report Generator

Generate presentation-quality Status Reports from sprint planning files. Each active sprint becomes a section with a standardized Executive Status slide showing progress, accomplishments, next actions, and attention points.

## Philosophy

> "Status reports answer 3 questions: Where are we? What happened? What's next?"

A good status report is **not a list of tasks**. It tells the story of project progress with conclusive titles, quantified metrics, and clear next steps. Each slide should answer one question for the audience.

## Self-Contained Dependencies

This skill ships with all dependencies bundled:

```
<this-skill>/
├── scripts/
│   ├── m7_pptx_lib.py       # M7 PPTX building blocks library (v4 — M7-2026 Brand)
│   ├── render_chart.js       # Puppeteer HTML→PNG chart renderer
│   └── package.json          # Node.js deps (puppeteer)
├── templates/                # D3.js chart templates (7 types + base, M7-2026 theme)
│   ├── chart-base.html
│   ├── line-chart.html
│   ├── bar-chart-horizontal.html
│   ├── grouped-bar-chart.html
│   ├── stacked-bar-chart.html
│   ├── diverging-bar-chart.html
│   ├── scatter-plot.html
│   └── histogram.html
├── assets/
│   ├── m7-logo-dark.png       # M7 logo (dark) for light slides
│   ├── m7-logo-offwhite.png   # M7 logo (offwhite) for dark slides
│   ├── m7-hero-dark.png       # Cover background image (darkened hero)
│   └── m7-logo.png            # Standard logo (fallback)
└── references/               # Documentation
    ├── CHART-RECIPES.md
    ├── EXECUTIVE-STATUS-LAYOUT.md
    ├── M7-D3-THEME.md
    ├── PARSING-GUIDE.md
    └── STYLE-GUIDE.md
```

### Prerequisites

```bash
# Python (for PPTX generation)
pip install python-pptx

# Node.js (only if using D3 charts)
cd <this-skill>/scripts
npm install
```

## Inputs

| Input | Source | Required? |
|-------|--------|-----------|
| ROADMAP.md | User's project directory | Yes |
| SPRINT-NN.md | User's project `sprints/` directory | Yes (at least 1 active) |
| Report date | User or today's date | Yes |
| Output path | **Ask the user** | Yes |

The ROADMAP.md and SPRINT-NN.md files are produced by the `decomposing-goals-into-sprints` skill. See [references/PARSING-GUIDE.md](references/PARSING-GUIDE.md) for exact parsing rules.

## Workflow

### Phase 0: Gather Inputs

**Before starting generation, ask the user:**

1. **Where is the project?** — Path to the directory containing ROADMAP.md and sprints/
2. **Where to save the PPTX?** — Output path for the generated file (suggest `<project>/reports/YYYY-MM-DD-status-report.pptx` as default)
3. **Include D3 charts?** — Whether to generate optional data visualizations
4. **Quais são os processos de execução?** — Colunas da tabela Roadmap que representam as etapas que cada sprint/UN percorre (ex: Diagnóstico, Processo, Relatórios, Automação, Treinamento, Piloto, Rotina). Se o ROADMAP.md tiver uma seção `## Processos de Execução` ou tabela com colunas além de Sprint/Título/Período/Produto/Status, extrair de lá. Caso contrário, perguntar ao usuário. Estes processos definem as colunas do slide Roadmap.

If the user provides a ROADMAP.md path directly, derive the project directory from it.

### Phase 1: Parse Sprint Data

Read the project's sprint files and extract structured data:

1. **Read ROADMAP.md** — extract Big Goal, sprint table (all sprints with status), dependencies, and risks
2. **Identify active sprints** — filter for Status = `🔵` (Em andamento) or `🔴` (Bloqueado)
3. **Read each active SPRINT-NN.md** — extract:
   - Tasks: count `[x]` (done) and `[ ]` (pending), grouped by `### Group`
   - Acceptance criteria: count `[x]` and `[ ]` under `## Critérios de Aceite`
   - Notes: free text under `## Notas` (becomes attention points)
   - Period, responsible, objective
4. **Compute metrics** per sprint:
   - `pct_complete` = tasks_done / tasks_total
   - `pct_aceites` = aceites_done / aceites_total
   - Color: >= 75% Green, 50-74% Blue, 25-49% Amber, < 25% Red
5. **Format title**: O título do Executive Status DEVE seguir estritamente o padrão curto: `"N de M tarefas concluídas (X%)"`. NÃO adicionar insights, complementos ou subtítulos após o percentual (ex: ❌ "— diagnóstico em 75%"). O título é um fato quantitativo, não uma narrativa.

Full parsing spec: [references/PARSING-GUIDE.md](references/PARSING-GUIDE.md)

### Phase 2: Determine Report Structure

The report follows a fixed slide sequence:

| # | Slide Type | Background | Building Block |
|---|-----------|------------|----------------|
| 1 | Cover | DARK | `prs.add_cover()` |
| 2 | Agenda | DARK | `prs.add_agenda()` |
| 3 | Roadmap Overview | LIGHT | `add_content_slide()` + `add_milestone_table()` |
| — | *Per active sprint:* | | |
| 4 | Section Divider | DARK | `prs.add_section_divider()` |
| 5 | **Executive Status** | LIGHT | `prs.add_executive_status_slide()` |
| 6 | Detail Slide (optional) | LIGHT | Chart PNG or task breakdown |
| — | *End of sprints* | | |
| N-1 | Risks | LIGHT | `add_content_slide()` + `add_status_card()` |
| N | Closing | DARK | `prs.add_closing()` |

**Roadmap slide**: DEVE usar `add_milestone_table()` (não `add_simple_table()`). As colunas devem ser: Sprint, Título, Período, e depois **uma coluna por processo de execução** (obtidos na Phase 0). Não usar colunas genéricas como "Produto" ou "Status". Cada célula de processo: `("check", C.BLUE_OFFICE)` para ativo/concluído no sprint atual, `("check", C.SEPARATOR)` para sprints futuros, `"-"` para processos não aplicáveis àquele sprint.

### Phase 3: Generate D3 Charts (Optional)

If the user requests charts or historical data is available:

| Chart | Template (in `templates/`) | When |
|-------|---------------------------|------|
| Sprint Completion Bars | `bar-chart-horizontal.html` | 2+ sprints in roadmap |
| Task Burndown | `line-chart.html` | Historical burndown data exists |
| Task Breakdown | `stacked-bar-chart.html` | Sprint has 3+ task groups |

Render pipeline: write HTML → `node <this-skill>/scripts/render_chart.js <in.html> <out.png>` → embed PNG in PPTX.

Full chart data formats: [references/CHART-RECIPES.md](references/CHART-RECIPES.md)

### Phase 4: Assemble PPTX

Write a Python script that:

1. Imports `m7_pptx_lib.py` from this skill's `scripts/` directory
2. Creates structural slides (cover, agenda, dividers, closing)
3. Builds Executive Status slides using composed building blocks
4. Embeds any D3 chart PNGs
5. Saves to the **user-specified output path**

```python
import sys
import os

# Use this skill's bundled library — resolve path dynamically
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SKILL_DIR, "scripts"))
# Or if running from a workspace, point to the discovered skill path:
# sys.path.insert(0, "<discovered-path-to-this-skill>/scripts")

from m7_pptx_lib import M7Presentation, C
```

**IMPORTANT**: The generated script must resolve the path to `m7_pptx_lib.py` dynamically. Use `os.path` to build the path relative to the script location or the discovered skill directory. Never hardcode absolute paths.

### Phase 5: Review

Before delivering, check:

- [ ] Every slide title is a **conclusion**, not a description
- [ ] Metrics are accurate (task counts match SPRINT-NN.md checkboxes)
- [ ] Attention points come from actual Notes section or blocked items
- [ ] Risks match ROADMAP.md (no invented risks)
- [ ] Dates use DD/MM format
- [ ] No more than 4 items per column in Executive Status
- [ ] Título do Executive Status segue padrão curto: "N de M tarefas concluídas (X%)" — sem complementos após o percentual
- [ ] Timeline tem no máximo 7 milestones — agrupar se necessário
- [ ] Roadmap usa `add_milestone_table()` com colunas de processos de execução (não tabela genérica)
- [ ] Output path is correct (as specified by user)

## Executive Status Slide

The core slide of every status report. One per active sprint. Based on the vBruno reference pattern — fieldset-legend sections with white fill, solid thin borders, and a timeline legend at the bottom.

```
┌──────────────────────────────────────────────────────┐
│ S0 — FUNDAÇÃO                             [M7 Logo]  │  Header (Lime 9pt)
│ 3 de 12 tarefas concluídas (25%)                     │  Title (TWK Everett 24pt, NOT bold)
├──────────────────────────────────────────────────────┤
│  Cronograma Macro                                    │  Zone 1: Timeline
│ ┌────────────────────────────────────────────────────┤  White box, 0.75pt border
│ │  ◆────◆────◆────★────◇────◇                       │  Green=done, Blue=current
│ │  Estrut  Diag  Mape  N2  POP  Apres               │
│ └────────────────────────────────────────────────────┤
│  Status Executivo       Próximas Atividades          │  Zone 2+3: Fieldset labels
│ ┌──────────────────────┐ ┌───────────────────────────┤  White boxes, 4.58" each
│ │ • Feito 1            │ │ • Próxima ação 1          │
│ │ • Feito 2            │ │ • Próxima ação 2          │
│ └──────────────────────┘ └───────────────────────────┤
│  Pontos de Atenção                                   │  Zone 4: Full-width
│ ┌────────────────────────────────────────────────────┤  White box, amber label
│ │ • Ponto 1                                          │
│ └────────────────────────────────────────────────────┤
│ Atualizado em DD/MMM/YYYY | Fonte: SPRINT-NN.md      │  Footnote
│          ◇ Não iniciado  ◆ Em andamento  ◆ Concluído │  Legend (auto-generated)
└──────────────────────────────────────────────────────┘
```

**Zone mapping:**

| Zone | Method | Data Source |
|------|--------|-------------|
| Header | `prs.add_executive_status_slide(section_num, section_label, title, ...)` | Sprint code + conclusive title |
| Timeline | `sb.add_timeline()` | Milestones with status (done/current/pending) |
| Columns | `sb.add_exec_two_columns()` | Left = `[x]` tasks (max 6), Right = `[ ]` tasks (max 6) |
| Attention | `sb.add_exec_attention()` | Notes section + risks (max 3) |
| Footer | `sb.add_footnote()` | Report date + source file |
| Legend | Auto-generated | 4 colored diamonds at bottom center |

**Milestone status**: `"done"` = filled green diamond (#00B050), `"current"` = filled blue diamond (#3B82F6), `"pending"` = hollow gray diamond.

**Timeline milestones**: Máximo **7 milestones** por timeline. Se o sprint tiver mais de 7 grupos de tarefas, agrupar os menos significativos. Milestones devem corresponder a marcos reais do cronograma (entregas tangíveis), não a cada tarefa individual. Cada label deve caber em ~1.4" de largura (2 linhas com quebra no `\n`).

**Titles are conclusions**: Padrão estrito: `"N de M tarefas concluídas (X%)"`. NÃO adicionar insights ou complementos após o percentual.

Full layout spec with EMU positions and code example: [references/EXECUTIVE-STATUS-LAYOUT.md](references/EXECUTIVE-STATUS-LAYOUT.md)

## Other Slide Types

### Cover

```python
prs.add_cover(
    project_label="STATUS REPORT",
    title="Nome do Projeto",
    tagline="Quinzena DD/MM — DD/MM",
    footer="M7 Investimentos | Mês YYYY"
)
```

### Roadmap Overview

Use `add_milestone_table()` for a visual milestone grid with Webdings checkmarks. Use `title_size=20` on `add_content_slide()` for a more compact title.

```python
s = prs.add_content_slide("00", "ROADMAP",
    "1 de 5 sprints em execução — projeto iniciado em 24/fev",
    title_size=20)
s.add_milestone_table(
    headers=["Sprint", "Título", "Período", "Diagnóstico", "Processo", ...],
    rows=[
        ["S0", "Processo Macro", "24/fev → 07/mar",
         ("check", C.BLUE_OFFICE), ("check", C.BLUE_OFFICE), "-", ...],
        ...
    ]
)
```

Cell value types: plain string (text), `("check", color)` (Webdings ■), `"-"` (dash/N.A.).

The old `add_simple_table()` is still available for plain text tables.

### Risks Slide

One `add_status_card()` per risk from ROADMAP.md:

```python
s.add_status_card("Descrição do risco", [
    "Probabilidade: Alta | Impacto: Crítico",
    "Contramedida: Ação preventiva descrita",
], status="negative")  # or "warning" for medium risks
```

- `status="negative"` for Alta probabilidade or Crítico impacto
- `status="warning"` for Média probabilidade
- `status="neutral"` for Baixa probabilidade

### Closing

```python
prs.add_closing(
    title="PRÓXIMOS PASSOS",
    cta="Ação principal\naté DD/MMM",
    footer="M7 Investimentos"
)
```

The CTA should be the single most important next action, typically completing the current active sprint.

## M7 Design System (M7-2026 Brand)

Full style guide: [references/STYLE-GUIDE.md](references/STYLE-GUIDE.md)

**Critical rules:**
- **Cover bg**: `m7-hero-dark.png` full-bleed image (fallback: solid `#424135`)
- **DARK bg** (`#424135` Verde Caqui): Agenda, Section Divider, Closing
- **LIGHT bg** (`#fffdef` Off-White): ALL content slides
- **Font**: TWK Everett (headings NOT bold, authority from size) — fallback Arial
- **Slide size**: 10" × 5.625" (16:9 widescreen)
- **Logo**: Every slide, top-right. Dark logo on light bg, off-white logo on dark bg
- **Accent**: Lime `#EEF77C` on max 1-2 elements per slide (DECORATIVE ONLY)

## Important Rules

1. **Ask where to save** — Always ask the user for the output path before generating
2. **1 frente = 1 active sprint** — each sprint with status `🔵` or `🔴` gets a section
3. **Titles are conclusions** — "Piloto avançando com 62%" not "Status do Sprint 1"
4. **Max 4 items per column** — overflow goes to a Detail slide
5. **Max 3 attention points** — summarize if more exist in Notes
6. **Dates in DD/MM** — follow Brazilian format throughout
7. **Tasks start with verbs** — inherited from the sprint planning format
8. **No traffic lights** — use numeric metrics with semantic colors instead
9. **Charts are optional** — the report works without them; D3 charts enhance, not replace
10. **Dynamic paths only** — never hardcode absolute filesystem paths in generated scripts; use `os.path` relative resolution
11. **One report per date** — suggest `YYYY-MM-DD-status-report.pptx` naming for version history

## Additional Resources

- **PPTX style guide**: [references/STYLE-GUIDE.md](references/STYLE-GUIDE.md)
- **D3 theme mapping**: [references/M7-D3-THEME.md](references/M7-D3-THEME.md)
- **Chart data formats**: [references/CHART-RECIPES.md](references/CHART-RECIPES.md)
- **Executive Status layout**: [references/EXECUTIVE-STATUS-LAYOUT.md](references/EXECUTIVE-STATUS-LAYOUT.md)
- **Sprint parsing rules**: [references/PARSING-GUIDE.md](references/PARSING-GUIDE.md)
