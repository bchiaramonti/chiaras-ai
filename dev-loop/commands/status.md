---
description: Mostra a fase atual da tarefa em curso, status dos artefatos e próxima skill recomendada
---

# /dev-loop:status

Lê `.dev-loop/.status` e mostra o estado da tarefa atual de forma compacta.

## Processo

1. **Ler `.dev-loop/.status`** — se não existir, responder: "Nenhum dev-loop inicializado neste projeto. Use `/dev-loop:start <task>` para começar."
2. **Identificar `current_task`** — se `null`, listar TODAS as tarefas em `tasks` com seu phase + status, e marcar qual seria reativável.
3. **Para a tarefa atual**, mostrar:
   - 📋 **Tarefa**: `<slug>`
   - 📅 **Iniciada**: `<started_at>`
   - 🔄 **Fase**: `<phase>`
   - 📂 **Artefatos**:
     - SPEC.md: `<status>` (✅ approved | 📝 draft | ⏳ pending)
     - research-notes.md: `<status>`
     - PLAN.md: `<status>`
     - VERIFY.md: `<status>`
   - ▶️ **Próximo passo**: `<skill ou ação recomendada>`

## Mapeamento fase → próximo passo

| Fase atual | Próxima ação recomendada |
|---|---|
| `scaffold` | `/scaffolding-project` (concluir setup) |
| `spec` | `/writing-spec` (ou `spec-auditor` se SPEC.md em draft) |
| `research` | `/researching-task` |
| `plan` | `/planning-implementation` (ou `plan-critic` se PLAN.md em draft) |
| `implement` | `/implementing-plan` |
| `verify` | `/verifying-against-spec` |
| `done` | Tarefa finalizada — commit/PR, ou `/dev-loop:start <nova>` |
| `blocked` | Investigar VERIFY.md para causa, voltar para `/planning-implementation` ou `/writing-spec` |

## Output esperado (exemplo)

```
📋 Tarefa: adicionar-cache-redis
📅 Iniciada: 2026-05-25
🔄 Fase: plan

📂 Artefatos:
   ✅ SPEC.md (approved)
   ✅ research-notes.md (approved)
   📝 PLAN.md (draft)
   ⏳ VERIFY.md (pending)

▶️ Próximo passo: /planning-implementation
   💡 Tip: para tarefas G+, considere /plan-critic antes de implementar.
```

## Notas

- Comando é **puro leitor** — não modifica estado.
- Se houver múltiplas tarefas in-flight, listar todas mas destacar `current_task`.
