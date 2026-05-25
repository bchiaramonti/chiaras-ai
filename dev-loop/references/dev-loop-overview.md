# Dev-Loop Overview

## State machine

```
   ┌──────────────────────────────────────────────────────────────────┐
   │                                                                  │
   │  ⓪ scaffold → ① spec → ② research → ③ plan → ④ implement → ⑤ verify
   │                                                                  │
   │      ↓          ↓          ↓             ↓         ↓         ↓   │
   │  .dev-loop/  SPEC.md   research-      PLAN.md   diffs +   VERIFY │
   │  CLAUDE.md             notes.md +               commits   .md    │
   │                        CLAUDE.md                                 │
   │                        (durable)                                 │
   │                                                                  │
   │                                ↑                                 │
   │                       verify fail loops back                     │
   │                       to ③ plan ou ① spec                        │
   └──────────────────────────────────────────────────────────────────┘
```

## File layout (por projeto e por tarefa)

```
<project root>/
├── CLAUDE.md                              # Durável (cresce com tarefas)
└── .dev-loop/
    ├── .status                            # JSON: current_task, phases
    └── <task-slug>/
        ├── SPEC.md
        ├── research-notes.md
        ├── PLAN.md
        └── VERIFY.md
```

## Phase gates

| From → To | Gate | Auditor opcional |
|---|---|---|
| spec → research | SPEC.md completo (4 campos) | `spec-auditor` (recomendado para G+) |
| research → plan | research-notes.md gerado, CLAUDE.md atualizado | — |
| plan → implement | PLAN.md literal-executável | `plan-critic` (recomendado para G+ ou 3+ subagents) |
| implement → verify | Todos os steps do PLAN.md done | — |
| verify → done | Todos os ACs ✓ em VERIFY.md | — (gate é a própria skill) |

## `.status` schema (versão 1)

```json
{
  "schema_version": 1,
  "project_initialized": true,
  "initialized_at": "YYYY-MM-DD",
  "current_task": "<slug>" | null,
  "tasks": {
    "<slug>": {
      "phase": "scaffold" | "spec" | "research" | "plan" | "implement" | "verify" | "done" | "blocked",
      "started_at": "YYYY-MM-DD",
      "artifacts": {
        "SPEC.md": null | "draft" | "approved",
        "research-notes.md": null | "draft" | "approved",
        "PLAN.md": null | "draft" | "approved",
        "VERIFY.md": null | "draft" | "done"
      }
    }
  }
}
```

## Mapa skill → fase → artefato

| Skill | Fase de entrada | Artefato produzido | Fase de saída |
|---|---|---|---|
| `scaffolding-project` | — (pre-init) | `.dev-loop/`, `CLAUDE.md` | `scaffold` done |
| `writing-spec` | scaffold/spec | `SPEC.md` | spec |
| `researching-task` | spec | `research-notes.md`, +CLAUDE.md | research |
| `planning-implementation` | research | `PLAN.md` | plan |
| `implementing-plan` | plan | (código + commits) | implement |
| `verifying-against-spec` | implement | `VERIFY.md` | verify → done |

## Agentes auditores

| Agente | Quando | Output |
|---|---|---|
| `spec-auditor` | Antes de `researching-task` | Grade A-D por dimensão + gaps |
| `plan-critic` | Antes de `implementing-plan` | Issues priorizadas 🔴🟡🟢 |

Ambos são read-only, têm contexto isolado, e retornam relatório curto.
