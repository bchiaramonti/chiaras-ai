# PLAN — <TASK_NAME>

> **Fase:** plan
> **Status:** draft
> **Data:** <YYYY-MM-DD>
> **Princípio**: este plano é lido **literalmente** por cada subagent dispatched durante implement. Vagueza vira drift.

---

## Resumo

<!-- 2-3 frases: o que o conjunto de steps entrega. -->

## Cobertura de ACs

| AC do SPEC.md | Coberta em |
|---------------|------------|
| AC-1 | Step 1, Step 3 |
| AC-2 | Step 2 |
| AC-3 | Step 4 |

## Grafo de dependências

```
Step 1 → Step 2 → Step 4
            ↘ Step 3 ↗
```

(Mermaid opcional se ajudar)

---

## Steps

### Step 1 — <título imperativo>

- **Action**: create | modify | delete | run | verify
- **File**: `<path>`
- **Depends on**: —
- **Subagent**: no (main thread)
- **ACs touched**: AC-1
- **Details**:
  - <bullet>
- **Verification (in-step)**: `<comando ou método>`

### Step 2 — <título>

- **Action**: 
- **File**: 
- **Depends on**: Step 1
- **Subagent**: yes (`general-purpose` — implementar isoladamente)
- **ACs touched**: 
- **Details**:
  - 
- **Verification (in-step)**: 

<!-- ... mais steps ... -->

---

## Status

- **Status:** draft
- **Próximo passo:** `/implementing-plan` (ou `plan-critic` antes, se G+ ou alto risco)
