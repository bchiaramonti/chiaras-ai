# Referência: ClickUp Sprint Planning

Guia de referência rápida para operações de sprint no ClickUp via MCP.

---

## Hierarquia do ClickUp

```
Workspace (organização)
└── Space (equipe/departamento)
    ├── Folder (agrupamento regular)
    │   └── List (contém tasks)
    ├── Sprint Folder (agrupamento ágil)
    │   ├── Sprint N (List especial com datas)
    │   └── Backlog (List regular)
    └── List (pode existir solto no Space)
        └── Task
            └── Subtask → Nested Subtask → Checklist
```

## Sprint Folder: Conceitos-Chave

### Statuses Automáticos

| Status | Quando | Trigger |
|--------|--------|---------|
| Not Started | Antes da data de início | Automático |
| In Progress | Na data de início | Automático |
| Done | Na data de fim | Automático (1 min antes do horário de início) |

### Spillover

- 24h antes do fim: **badge** + **banner** alertam tasks incompletas
- Tasks incompletas migram para próximo Sprint automaticamente
- Tasks com status "Done" permanecem no sprint original
- Revisão manual possível antes da migração

### Sprint Automations (Business Plan+)

- Quando sprint é Done → cria próximo sprint automaticamente
- Novos sprints adicionados após os existentes
- Automação de Done está **sempre ativa** em todos os planos

## Mapeamento: SPRINT-NN.md → ClickUp Tasks

### Exemplo Completo

**Input (SPRINT-01.md):**
```markdown
# Sprint 1 — Investimentos

**Período:** Sem. 3-4: 10/mar → 21/mar
**Responsável:** Bruno + Gestor

## Tarefas

### Setup
- [ ] **Configurar template de report** — no Cowork, incluir KPIs do S0
- [ ] **Definir cadência do ritual N2** — semanal, 30min, toda segunda

### Validação
- [ ] **Validar ritual N2 com gestor** — reunião presencial de 1h

## Critérios de Aceite
- [ ] Ritual N2 de Investimentos rodando por 2 semanas
- [ ] Template de report aprovado pelo gestor
```

**Output (ClickUp tasks):**

| # | Task Name | Priority | Tags | Due Date |
|---|-----------|----------|------|----------|
| 1 | Configurar template de report — no Cowork, incluir KPIs do S0 | normal | setup, sprint-01 | 2026-03-21 |
| 2 | Definir cadência do ritual N2 — semanal, 30min, toda segunda | normal | setup, sprint-01 | 2026-03-21 |
| 3 | Validar ritual N2 com gestor — reunião presencial de 1h | high | validação, sprint-01 | 2026-03-21 |

**Task 3 description:**
```markdown
Reunião presencial de 1h com gestor de Investimentos para validar o ritual N2.

## Critérios de Aceite
- [ ] Ritual N2 de Investimentos rodando por 2 semanas
- [ ] Template de report aprovado pelo gestor
```

## Operações MCP: Receitas Comuns

### Criar Sprint Folder + Sprints

```
1. clickup_get_workspace_hierarchy → identificar space_id
2. clickup_create_folder(space_id, name="Projeto X") → folder_id
3. clickup_create_list_in_folder(folder_id, name="Sprint 1 (10/mar - 21/mar)")
4. clickup_create_list_in_folder(folder_id, name="Sprint 2 (24/mar - 04/abr)")
5. clickup_create_list_in_folder(folder_id, name="Backlog")
```

### Popular Sprint com Tasks

```
1. clickup_get_list(list_name="Sprint 1") → list_id
2. clickup_resolve_assignees(["bruno"]) → user_ids
3. Para cada task no SPRINT file:
   clickup_create_task(
     list_id=list_id,
     name="Task name",
     description="Description + critérios",
     due_date="2026-03-21",
     start_date="2026-03-10",
     priority="normal",
     tags=["sprint-01", "grupo-lógico"],
     assignees=[user_id]
   )
```

### Buscar Tasks de um Sprint

```
clickup_search(
  keywords="sprint",
  filters={
    asset_types: ["task"],
    location: { subcategories: [list_id] },
    task_statuses: ["active"]
  }
)
```

### Mover Task entre Sprints

```
1. clickup_get_task(task_id) → verificar estado atual
2. clickup_update_task(task_id, list_id=novo_sprint_list_id)
```

## Validação de Qualidade

### Por Sprint

| Critério | Como verificar |
|----------|---------------|
| Datas configuradas | Sprint tem start_date e due_date |
| Tasks ≤ 15 | Contar tasks na List |
| Tasks têm nomes claros | Começam com verbo de ação |
| Assignees resolvidos | Não tem tasks sem assignee |
| Prioridades definidas | Nenhuma task sem priority |
| Tags de rastreabilidade | Todas tem tag "sprint-NN" |

### Por Sprint Folder

| Critério | Como verificar |
|----------|---------------|
| Backlog List existe | Verificar Lists no Folder |
| Sprints em sequência | Datas não se sobrepõem |
| Naming consistente | "Sprint N (DD/MM - DD/MM)" |
| Não excede 8 sprints | Se mais, dividir o projeto |

## Formato de Datas

O ClickUp aceita:
- `YYYY-MM-DD` — ex: `2026-03-10`
- `YYYY-MM-DD HH:MM` — ex: `2026-03-10 09:00`

Ao converter de SPRINT files:
- `10/mar` → `2026-03-10`
- `Sem. 3-4: 10/mar → 21/mar` → start: `2026-03-10`, due: `2026-03-21`
- Use o ano corrente (2026) salvo indicação contrária
