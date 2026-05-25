# VERIFY — <TASK_NAME>

> **Fase:** verify
> **Status:** running | done | blocked
> **Data:** <YYYY-MM-DD>

---

## Acceptance Criteria — 1-para-1 com SPEC.md

| AC | Descrição | Método | Resultado | Evidência |
|----|-----------|--------|-----------|-----------|
| AC-1 | <copiar do SPEC> | test:unit | ✅ PASS | `pytest tests/test_x.py::test_y` saída green |
| AC-2 | | test:integration | ✅ PASS | |
| AC-3 | | manual | ❌ FAIL | Input X → esperado Y, recebido Z |

## Regressão

- [ ] Testes existentes rodados: `<comando>` — resultado: `<X passed, 0 failed>`
- [ ] Arquivos out-of-scope NÃO foram tocados: `<verificação git diff>`

## Edge cases adicionais

| # | Caso | Resultado |
|---|------|-----------|
| 1 | <ex: input vazio> | ✅ tratado |
| 2 | <ex: payload grande> | ⚠️ não testado |

## Diagnóstico (se FAIL)

<!-- Para cada FAIL, mapear: AC → Step do PLAN.md → causa raiz → recomendação -->

- **AC-3 FAIL**: Step 4 do PLAN.md gerou comportamento incorreto. Causa: `<descrição>`. Recomendação: `<voltar pra planning ou writing-spec>`.

---

## Decisão

- [ ] Todos PASS → tarefa **DONE**. Próximo: commit/PR + update CHANGELOG.md.
- [ ] Algum FAIL → tarefa **BLOCKED**. Voltar para: `<skill>`.
