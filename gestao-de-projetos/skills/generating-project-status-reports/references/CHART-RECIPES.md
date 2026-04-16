# D3 Chart Recipes for Status Reports

Optional D3.js charts to enhance Status Report presentations. All templates are bundled in this skill's `templates/` directory — this file documents how to format data for each recipe.

**Theme**: All chart templates use the M7-2026 brand palette. Full D3 color mapping: [M7-D3-THEME.md](M7-D3-THEME.md)

## When to Use Charts

Charts are **optional** — the Executive Status slides work without them. Add charts when:
- Multiple sprints are active (Sprint Completion Bars)
- Historical data exists across report dates (Task Burndown)
- A sprint has 3+ task groups (Task Breakdown by Domain)
- The audience prefers visual dashboards over text lists

## Rendering Pipeline

```bash
# 1. Generate HTML from template (Claude replaces {{DATA_JSON}})
# 2. Render to PNG
node <this-skill>/scripts/render_chart.js workspace/charts/<name>.html workspace/charts/<name>.png
# 3. Embed in PPTX
slide.slide.shapes.add_picture("workspace/charts/<name>.png",
    left=Emu(548640), top=Emu(1371600), width=Emu(8046720), height=Emu(2743200))
```

---

## Recipe 1: Sprint Completion Bars

**When**: 2+ sprints in the roadmap (any status).
**Template**: `templates/bar-chart-horizontal.html`
**Slide placement**: After the Roadmap Overview slide.

**Data format:**

```json
{
  "items": [
    { "label": "S0 — Fundação", "value": 100 },
    { "label": "S1 — Investimentos", "value": 62, "highlight": true },
    { "label": "S2 — Crédito", "value": 0 },
    { "label": "S3 — Seguros", "value": 0 },
    { "label": "S4 — Consolidação", "value": 0 }
  ],
  "sorted": false,
  "valueFormat": ",.0f",
  "valueSuffix": "%",
  "highlightTop": 0
}
```

**Key settings:**
- `sorted: false` — preserves chronological sprint order (not magnitude order)
- `highlight: true` on the active sprint(s) — draws attention
- `highlightTop: 0` — disables auto-highlight (we control it explicitly)
- Values are `pct_complete` from parsed task counts

---

## Recipe 2: Task Burndown

**When**: Historical data from multiple report dates (at least 3 data points).
**Template**: `templates/line-chart.html`
**Slide placement**: Detail slide after the Executive Status of the relevant sprint.

**Data format:**

```json
{
  "labels": ["24/fev", "28/fev", "03/mar", "07/mar", "10/mar", "14/mar"],
  "series": [
    {
      "name": "Tarefas Pendentes",
      "values": [13, 11, 9, 7, 5, 5],
      "highlight": true
    },
    {
      "name": "Ideal (linear)",
      "values": [13, 10.4, 7.8, 5.2, 2.6, 0],
      "highlight": false,
      "dashed": true
    }
  ],
  "annotations": [
    {
      "index": 5,
      "text": "Stall: bloqueio CRM",
      "position": "above",
      "seriesIndex": 0
    }
  ],
  "yLabel": "Tarefas Pendentes",
  "yFormat": ",.0f"
}
```

**Key settings:**
- "Ideal" series uses `dashed: true` as a reference line
- Annotations mark significant events (blockers, breakthroughs)
- If actual line is above ideal → sprint is behind; below → ahead

**How to collect burndown data:**
Each time a Status Report is generated, record `(date, tasks_remaining)` for each active sprint. Store in `<project>/reports/burndown-data.json`:

```json
{
  "S1": [
    { "date": "10/mar", "remaining": 13 },
    { "date": "14/mar", "remaining": 5 }
  ]
}
```

---

## Recipe 3: Task Breakdown by Domain

**When**: A sprint has 3+ task groups (from `### Group Name` in SPRINT-NN.md).
**Template**: `templates/stacked-bar-chart.html`
**Slide placement**: Detail slide after the Executive Status of the relevant sprint.

**Data format:**

```json
{
  "categories": ["S0", "S1", "S2"],
  "series": [
    { "name": "Diagnóstico", "values": [4, 2, 0] },
    { "name": "Customização", "values": [0, 3, 0] },
    { "name": "Dados", "values": [3, 2, 0] },
    { "name": "Validação", "values": [2, 1, 0] }
  ],
  "normalized": false,
  "valueFormat": ",.0f"
}
```

**Key settings:**
- `normalized: false` — shows absolute task counts (not percentages)
- Series = task group names from `### Group` headers
- Values = `tasks_done` count per group per sprint
- Categories = sprint codes

**Variant — single sprint, done vs pending:**

```json
{
  "categories": ["Diagnóstico", "Customização", "Dados", "Validação"],
  "series": [
    { "name": "Concluídas", "values": [4, 3, 2, 1] },
    { "name": "Pendentes", "values": [0, 2, 1, 3] }
  ],
  "normalized": false,
  "valueFormat": ",.0f"
}
```

Use `grouped-bar-chart.html` template for this variant (side-by-side bars instead of stacked).
