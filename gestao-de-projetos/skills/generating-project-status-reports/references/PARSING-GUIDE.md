# Parsing Guide: ROADMAP.md + SPRINT-NN.md

How to extract structured data from the files produced by `decomposing-goals-into-sprints`.

## Source Files

| File | Location | Content |
|------|----------|---------|
| ROADMAP.md | `<project>/ROADMAP.md` | Big Goal, sprint table, dependencies, risks |
| SPRINT-NN.md | `<project>/sprints/SPRINT-NN.md` | Per-sprint tasks, status, acceptance criteria |

## Parsing ROADMAP.md

### Big Goal

Extract the blockquote under `## Big Goal`:

```
## Big Goal

> A equipe de Performance terá rituais padronizados até mai/2026...
```

Everything after `> ` on the first blockquote line(s) is the Big Goal text.

### Sprint Table

The `## Visão Geral` section contains a markdown table with this structure:

```
| Sprint | Título | Período | Produto | Responsável | Status |
|--------|--------|---------|---------|-------------|--------|
| S0 | [Fundação](sprints/SPRINT-00.md) | 24/fev → 07/mar | Mapeamento AS-IS completo | Bruno | ⬚ |
```

**Column extraction:**
- Col 0 (Sprint): code like `S0`, `S1`, etc.
- Col 1 (Título): may contain markdown link `[text](path)` — extract the text
- Col 2 (Período): format `DD/MM → DD/MM` (uses arrow `→`)
- Col 3 (Produto): plain text deliverable
- Col 4 (Responsável): owner name(s)
- Col 5 (Status): emoji character

**Status emoji mapping:**

| Emoji | Meaning | Filter for report? |
|-------|---------|-------------------|
| `⬚` | Pendente | No (skip) |
| `🔵` | Em andamento | **Yes — create Executive Status slide** |
| `✅` | Concluído | Show in Roadmap Overview table only |
| `🔴` | Bloqueado | **Yes — create Executive Status slide (highlight)** |

### Dependencies Table

Under `## Dependências`:

```
| Sprint | Depende de | Desbloqueia |
|--------|-----------|-------------|
| S0 | — | S1, S2, S3 |
```

Parse as list of `(sprint, depends_on[], unblocks[])` tuples.

### Risks Table

Under `## Riscos`:

```
| # | Risco | Probabilidade | Impacto | Contramedida |
|---|-------|--------------|---------|-------------|
| R1 | Baixa adesão dos gestores | Alta | Crítico | Sponsor valida antes do rollout |
```

Parse all rows. For the Status Report, use risks in the Risks slide.

---

## Parsing SPRINT-NN.md

### Header Fields

First 3 bold fields after the `# Sprint N — Title` heading:

```
**Período:** Sem. 1-2: 24/fev → 07/mar
**Responsável:** Bruno (Performance)
**Status:** 🔵 Em andamento
```

Extract:
- `period`: text after `**Período:**` — the `DD/MM → DD/MM` part
- `responsible`: text after `**Responsável:**`
- `status`: emoji after `**Status:**`

### Objective & Product

- `objective`: paragraph under `## Objetivo`
- `product`: blockquote text under `## Produto do Sprint`

### Tasks (Checkbox Counting)

Tasks live under `## Tarefas`, grouped by `### Group Name` headings:

```
### Diagnóstico

- [x] **Entrevistar 8 gestores** — roteiro semi-estruturado
- [ ] **Mapear fluxos AS-IS** — um diagrama por funil
- [x] **Levantar KPIs atuais** — extrair do BI
```

**Parsing rules:**
- `- [x]` = completed task
- `- [ ]` = pending task
- The `### Group Name` before tasks defines the domain group
- Task text: everything after `] ` on the line (includes bold verb + description)
- Stop parsing tasks when reaching `## Critérios de Aceite` or next `##` heading

**For the Executive Status slide:**
- `completed_tasks`: list of task texts from `[x]` lines
- `pending_tasks`: list of task texts from `[ ]` lines
- `tasks_total`: count of all task lines
- `tasks_done`: count of `[x]` lines
- `task_groups`: dict of `{group_name: {done: N, total: M}}`

### Acceptance Criteria

Under `## Critérios de Aceite`:

```
- [x] 6 funis mapeados com fluxo AS-IS documentado
- [ ] Diretoria validou diagnóstico (ata de reunião)
```

Same `[x]`/`[ ]` counting:
- `aceites_total`: count of all criteria
- `aceites_done`: count of `[x]` criteria

### Notes (Attention Points)

Under `## Notas`:

Free text. Each non-empty line or bullet becomes a potential "Ponto de Atenção" for the Executive Status slide. If the section says `[Preencher durante/após execução.]`, treat as empty.

---

## Computed Metrics

After parsing, compute these derived values per sprint:

```python
pct_complete = round(tasks_done / tasks_total * 100) if tasks_total > 0 else 0
pct_aceites = round(aceites_done / aceites_total * 100) if aceites_total > 0 else 0

# Color logic (replaces traffic lights)
def status_color(pct):
    if pct >= 75: return "C.GREEN"
    if pct >= 50: return "C.BLUE"
    if pct >= 25: return "C.AMBER"
    return "C.RED"

tasks_color = status_color(pct_complete)
aceites_color = status_color(pct_aceites)
```

---

## Processos de Execução (Colunas do Roadmap)

Os processos de execução definem as colunas da tabela Roadmap. Cada sprint/UN percorre esses processos sequencialmente.

### Extração automática

Verificar se o ROADMAP.md contém uma seção `## Processos de Execução` ou `## Processos`:

```markdown
## Processos de Execução

| Processo | Descrição |
|----------|-----------|
| Diagnóstico | Entrevistas, mapeamento AS-IS |
| Processo | Desenho do fluxo N2 (N1→N4) |
| Relatórios | Dashboard operacional e materiais |
| Automação | Plugins Cowork e automações |
| Treinamento | Capacitação dos gestores |
| Piloto | Execução piloto acompanhada |
| Rotina | Ritual rodando em SDCA |
```

Se encontrada, usar os nomes da coluna "Processo" como headers da `add_milestone_table()`.

### Fallback — perguntar ao usuário

Se o ROADMAP.md não tiver essa seção, perguntar ao usuário na Phase 0:
> "Quais processos de execução cada sprint percorre? (ex: Diagnóstico, Processo, Relatórios, Automação, Treinamento, Piloto, Rotina)"

### Mapeamento para a tabela

Para cada sprint/processo, determinar o status da célula:
- Sprint ativo (`🔵`) + processo já concluído → `("check", C.BLUE_OFFICE)` (azul)
- Sprint ativo (`🔵`) + processo em andamento → `("check", C.BLUE_OFFICE)` (azul)
- Sprint futuro (`⬚`) → `("check", C.SEPARATOR)` (cinza)
- Sprint concluído (`✅`) + processo concluído → `("check", C.GREEN_DONE)` (verde)
- Processo não aplicável ao sprint → `"-"` (dash)

---

## Output Data Structure

Conceptual Python dict that Claude builds mentally when parsing:

```python
project = {
    "name": "Padronização dos Rituais de Gestão",
    "big_goal": "A equipe de Performance terá rituais...",
    "report_date": "14/mar/2026",
    "sprints": [
        {
            "code": "S0",
            "title": "Fundação",
            "period": "24/fev → 07/mar",
            "product": "Mapeamento AS-IS completo",
            "responsible": "Bruno",
            "status": "completed",       # from ✅
            "tasks_total": 9,
            "tasks_done": 9,
            "pct_complete": 100,
        },
        {
            "code": "S1",
            "title": "Investimentos",
            "period": "10/mar → 21/mar",
            "product": "Ritual N2 rodando",
            "responsible": "Bruno + Gestor",
            "status": "in_progress",     # from 🔵
            "tasks_total": 13,
            "tasks_done": 8,
            "pct_complete": 62,
            "aceites_total": 7,
            "aceites_done": 3,
            "completed_tasks": ["Entrevistou gestor...", ...],
            "pending_tasks": ["Treinar equipe...", ...],
            "task_groups": {
                "Diagnóstico": {"done": 4, "total": 4},
                "Customização": {"done": 3, "total": 5},
                "Validação": {"done": 1, "total": 4},
            },
            "attention_points": ["Plugin Cowork MVP...", ...],
        },
    ],
    "risks": [
        {
            "id": "R1",
            "description": "Baixa adesão dos gestores",
            "probability": "Alta",
            "impact": "Crítico",
            "countermeasure": "Sponsor valida antes do rollout",
        },
    ],
    "dependencies": [...],
}
```
