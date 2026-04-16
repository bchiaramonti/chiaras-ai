# Executive Status Slide Layout (M7-2026 Brand)

Spec for the standardized Executive Status slide — one per active sprint. Based on the vBruno reference pattern (validated manually from Votorantim Energia inspiration).

Full design system reference: [STYLE-GUIDE.md](STYLE-GUIDE.md) | D3 chart theme: [M7-D3-THEME.md](M7-D3-THEME.md)

## Layout Diagram

```
┌──────────────────────────────────────────────────────┐
│ S0 — FUNDAÇÃO                             [M7 Logo]  │  HEADER (Lime 9pt, same as content slides)
│ 3 de 12 tarefas concluídas (25%)                     │  TITLE (TWK Everett 24pt, NOT bold)
├──────────────────────────────────────────────────────┤
│  Cronograma Macro                                    │  ZONE 1: Fieldset label (white rounded rect)
│ ┌────────────────────────────────────────────────────┤
│ │  ◆────◆────◆────★────◇────◇                       │  add_timeline()
│ │  Estrut  Diag  Mape  N2  POP  Apres               │  White box, 0.75pt solid border
│ └────────────────────────────────────────────────────┤
│  Status Executivo       Próximas Atividades          │  ZONE 2+3: Fieldset labels
│ ┌──────────────────────┐ ┌───────────────────────────┤
│ │ • Feito 1            │ │ • Próxima ação 1          │  add_exec_two_columns()
│ │ • Feito 2            │ │ • Próxima ação 2          │  White boxes, 0.75pt solid border
│ │ • Feito 3            │ │ • Próxima ação 3          │  4.58" each column
│ └──────────────────────┘ └───────────────────────────┤
│  Pontos de Atenção                                   │  ZONE 4: Fieldset label (amber)
│ ┌────────────────────────────────────────────────────┤
│ │ • Ponto 1                                          │  add_exec_attention()
│ │ • Ponto 2                                          │  White box, 0.75pt solid border
│ └────────────────────────────────────────────────────┤
│ Atualizado em 24/fev/2026 | Fonte: SPRINT-00.md      │  add_footnote()
│          ◇ Não iniciado  ◆ Em andamento  ◆ Concluído │  Legend (colored diamonds)
└──────────────────────────────────────────────────────┘
```

## Static Layout Architecture

This slide uses a **static layout** with hardcoded EMU coordinates (constants prefixed `_EX_*` in `m7_pptx_lib.py`). Every structural element — boxes, labels, timeline, legend — is placed at a fixed position. **Only the text content changes between reports.**

The method `prs.add_executive_status_slide(...)` handles everything in a single call. It does NOT use the `SlideBuilder` cursor — all zones are placed at absolute coordinates.

## Zone-to-Helper Mapping

| Zone | Internal Helper | Fixed Position |
|------|----------------|----------------|
| Header | `_textbox()` (standard) | MARGIN, HEADER_TOP / TITLE_TOP |
| Zone 1 (Timeline) | `_exec_fieldset_label()` + `_exec_content_box()` + `_exec_timeline_markers()` | Y=1114864 (label), Y=1207298 (box) |
| Zone 2+3 (Columns) | `_exec_fieldset_label()` × 2 + `_exec_content_box()` × 2 | Y=2002681 (labels), Y=2095115 (boxes) |
| Zone 4 (Attention) | `_exec_fieldset_label()` + `_exec_content_box()` | Y=3921761 (label), Y=4014195 (box) |
| Footer | `_textbox()` | Y=4880000 |
| Legend | `_exec_legend()` | Y=4917788 |

## Static Coordinates (EMU)

```python
_EX_LEFT = 320040        # 0.350" — content left edge (wider than MARGIN)
_EX_WIDTH = 8503920      # 9.300" — total content width
_EX_COL_W = 4183380      # 4.575" — each column
_EX_COL_GAP = 137160     # 0.150" — gap between columns
_EX_RIGHT_X = 4640580    # Right column left edge
```

## Visual Style (vBruno Pattern — M7-2026 Brand)

| Element | Style |
|---------|-------|
| Title | TWK Everett 24pt, NOT bold (M7-2026: authority from size, not weight) |
| Fieldset labels | Rounded rect with **solid white fill**, TWK Everett 9pt bold |
| Content boxes | Rectangle, **solid white fill (#FFFFFF)**, **0.75pt solid border (#D0D0CC)** |
| Bullet text | TWK Everett 9pt bold, #4F4E3C (verde-medio) |
| Column width | 4.575" each, 0.15" gap between them |
| Timeline line | Solid blue (#3B82F6) rectangle |
| Legend | 4 colored diamonds below footnote at Y=5.38" |

## Timeline Milestone Status

**Máximo 7 milestones** por timeline. Se o sprint tiver mais de 7 grupos de tarefas, agrupar os menos significativos em um único marco. Milestones devem corresponder a entregas tangíveis do cronograma, não a cada tarefa individual. Labels devem caber em ~1.4" (~1295400 EMU) de largura, com até 2 linhas usando `\n`.

| Status | Visual | Color | Constant |
|--------|--------|-------|----------|
| `"done"` | Filled diamond ◆ (0.18") | Green | `C.GREEN_DONE` (#00B050) |
| `"current"` | Filled diamond ◆ (0.18") | Blue | `C.BLUE` (#3B82F6) |
| `"pending"` | Hollow diamond ◇ (0.13") | Gray border | `C.SEPARATOR` (#D0D0CC) |

## Legend Items (auto-generated)

| Label | Diamond Color | Constant |
|-------|--------------|----------|
| Não iniciado | Gray | `C.SEPARATOR` |
| Em andamento | Blue | `C.BLUE` |
| Atrasado | Dark Red | `C.RED_DARK` (#C00000) |
| Concluído | Green | `C.GREEN_DONE` (#00B050) |

## Item Count Limits

| Zone | Max Items | Overflow Action |
|------|-----------|----------------|
| Status Executivo (left) | 6 | Move remaining to Detail slide |
| Próximas Atividades (right) | 6 | Move remaining to Detail slide |
| Pontos de Atenção | 3 | Summarize or create separate Risks slide |

## Title Writing Rules

The slide title must be a **conclusion, not a description**:

**REGRA**: O título DEVE seguir o padrão curto: `"N de M tarefas concluídas (X%)"`.
NÃO adicionar "— insight" ou qualquer complemento após o percentual fechado.

| Status | Exemplo |
|--------|---------|
| ✅ Correto | "3 de 12 tarefas concluídas (25%)" |
| ✅ Correto | "8 de 13 tarefas concluídas (62%)" |
| ❌ Errado | "3 de 12 tarefas concluídas (25%) — diagnóstico em 75%" |
| ❌ Errado | "8 de 13 tarefas concluídas (62%) — piloto avançando" |

Pattern: `[N de M tarefas concluídas (X%)]` — sem complementos.

## Roadmap Overview (Milestone Grid)

The Roadmap slide uses `add_milestone_table()` for a visual milestone grid:

```python
s = prs.add_content_slide("00", "ROADMAP",
    "1 de 5 sprints em execução — projeto iniciado em 24/fev",
    title_size=20)  # Smaller title to give more room to the table

s.add_milestone_table(
    headers=["Sprint", "Título", "Período", "Diagnóstico", "Processo",
             "Relatórios", "Automação", "Treinamento", "Piloto", "Rotina"],
    rows=[
        ["S0", "Processo Macro", "24/fev → 07/mar",
         ("check", C.BLUE_OFFICE), ("check", C.BLUE_OFFICE),
         "-", "-", "-", "-", "-"],
        ["S1", "Investimentos", "10/mar → 21/mar",
         ("check", C.SEPARATOR), ("check", C.SEPARATOR),
         ("check", C.SEPARATOR), ("check", C.SEPARATOR),
         ("check", C.SEPARATOR), ("check", C.SEPARATOR),
         ("check", C.SEPARATOR)],
    ]
)
```

Cell types:
- Plain string: text (TWK Everett 8pt)
- `("check", C.BLUE_OFFICE)`: Webdings "n" (■) in blue — active sprint milestone
- `("check", C.SEPARATOR)`: Webdings "n" (■) in gray — future milestone
- `"-"`: centered dash — not applicable

## Complete Code Example

```python
import sys, os

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SKILL_DIR, "scripts"))
from m7_pptx_lib import M7Presentation, C

prs = M7Presentation()

# --- Cover ---
prs.add_cover(
    project_label="STATUS REPORT",
    title="Padronização dos Rituais\nde Gestão M7",
    tagline="Semana 24/fev — 07/mar/2026",
    footer="M7 Investimentos | Fevereiro 2026"
)

# --- Agenda ---
prs.add_agenda([
    "Visão Geral do Roadmap",
    "Sprint 0 — Fundação (em andamento)",
    "Riscos e Pontos de Atenção",
    "Próximos Passos",
], project_label="STATUS REPORT")

# --- Roadmap Overview (milestone grid) ---
s = prs.add_content_slide("00", "ROADMAP",
    "1 de 5 sprints em execução — projeto iniciado em 24/fev",
    title_size=20)
s.add_milestone_table(
    headers=["Sprint", "Título", "Período", "Diagnóstico", "Processo",
             "Relatórios", "Automação", "Treinamento", "Piloto", "Rotina"],
    rows=[
        ["S0", "Processo Macro", "24/fev → 07/mar",
         ("check", C.BLUE_OFFICE), ("check", C.BLUE_OFFICE),
         "-", "-", "-", "-", "-"],
        ["S1", "Investimentos", "10/mar → 21/mar",
         ("check", C.SEPARATOR), ("check", C.SEPARATOR),
         ("check", C.SEPARATOR), ("check", C.SEPARATOR),
         ("check", C.SEPARATOR), ("check", C.SEPARATOR),
         ("check", C.SEPARATOR)],
    ]
)
s.add_footnote("Fonte: ROADMAP.md | Atualizado em 24/fev/2026")

# --- Section Divider ---
prs.add_section_divider("S0", "FUNDAÇÃO",
    "Base Metodológica dos\nRituais de Gestão N2")

# --- Executive Status (returns slide, not SlideBuilder) ---
prs.add_executive_status_slide(
    section_num="S0",
    section_label="FUNDAÇÃO",
    title="3 de 12 tarefas concluídas (25%)",
    milestones=[
        ("Estruturar\nprojeto", "done"),
        ("Organizar\nreferências", "done"),
        ("Cadeia de\nvalor N1", "done"),
        ("Diagnosticar\nrituais", "current"),
        ("Desenhar\nprocesso N2", "pending"),
        ("POP +\nTemplates", "pending"),
        ("Validar c/\ndiretoria", "pending"),
    ],
    done_items=[
        "Estruturou projeto (repositório, BRIEFING, CLAUDE.md)",
        "Organizou material de referência (BPM, PDCA, rituais)",
        "Mapeou cadeia de valor M7 N1 (v2.0)",
    ],
    next_items=[
        "Diagnosticar rituais informais existentes",
        "Desenhar processo Ritual N2 (N1→N4)",
        "Definir modelo-padrão e KPIs/PPIs",
        "Criar POP genérico e template de pauta",
        "Definir arquitetura de automação Cowork",
        "Apresentar modelo à diretoria (gate S1)",
    ],
    risk_items=[
        "Sprint na 1ª semana — 9 tarefas restantes para entregar até 07/mar",
        "Validação com diretoria é gate obrigatório para iniciar S1",
        "Aceites em 14% (1/7) — maioria depende do desenho do processo",
    ],
    footnote="Atualizado em 24/fev/2026 | Fonte: SPRINT-00.md",
)

# --- Risks ---
s = prs.add_content_slide("03", "RISCOS",
    "6 riscos mapeados — 2 com probabilidade alta")
s.add_status_card("R1 — Baixa adesão da liderança aos rituais", [
    "Probabilidade: Alta | Impacto: Crítico",
    "Contramedida: Envolver diretoria no gate do S0",
], status="negative")

# --- Closing ---
prs.add_closing(
    title="PRÓXIMOS PASSOS",
    cta="Concluir Sprint 0 (Fundação)\naté 07/mar/2026",
    footer="M7 Investimentos"
)

prs.save("reports/2026-02-24-status-report.pptx")
```

## Backward Compatibility

The old pattern using `add_blank_slide` + `add_metric_row` + `add_two_columns` + `add_status_card` still works for non-executive slides. The new methods are additive. The old `add_simple_table()` also remains available for simple text tables.
