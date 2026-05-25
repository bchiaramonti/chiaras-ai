---
name: planning-implementation
description: Sintetiza SPEC.md + research-notes.md em PLAN.md literal-executável com passos numerados, ordem de dependência, file paths exatos e hints de dispatch de subagent. Use após research aprovada — o PLAN.md é o contrato que cada subagent dispatched por implementing-plan lê como primeira ação para evitar drift em modelos Opus.
user-invocable: true
---

# Planning Implementation

Produz `PLAN.md` literal o suficiente para Opus 4.7 (e subagents dispatched) executarem sem reinterpretação.

## Pré-requisitos

- `SPEC.md` aprovado
- `research-notes.md` aprovado
- `.status` em fase `research` ou `plan`

## Princípio chave

**Plan-as-contract**: cada step do PLAN.md vai ser lido literalmente por um subagent (ou pelo executor no main thread). Vagueza = drift. Especificidade = execução previsível.

## Anatomia de um step

```markdown
### Step N — <título imperativo>

**Action**: <verbo: create | modify | delete | run | verify>
**File**: `<path exato>` (ou globs)
**Depends on**: Step <M>, Step <K> (ou "—" se independente)
**Subagent**: <yes/no — se yes, qual tipo>
**ACs touched**: AC-1, AC-3
**Details**:
- <bullet específico do que fazer>
- <com referência a função/classe se aplicável>
**Verification (in-step)**: <test/command/inspect>
```

## Processo

1. **Ler SPEC.md** e **research-notes.md** completos.
2. **Derivar grafo de tarefas** — decompor o trabalho em steps de granularidade `commit-size` (cada step ≈ 1 commit).
3. **Ordenar por dependência** — steps que precisam de outros vêm depois. Independentes podem ser paralelizados na execução.
4. **Decidir subagent vs main thread por step** — critérios em `../implementing-plan/references/subagent-dispatch.md`.
5. **Mapear ACs → steps** — cada AC do SPEC.md deve estar coberto por pelo menos 1 step. Se sobrar AC sem cobertura → spec ou plan está faltando algo.
6. **Escrever PLAN.md** usando `templates/PLAN.tmpl.md`.
7. **Sugerir gate opcional**: "Plano gerado. Quer rodar `plan-critic` antes de começar a executar? (recomendado para tarefas G+)"
8. **Atualizar `.status`**: `tasks.<slug>.phase = "plan"`, `artifacts."PLAN.md" = "draft"`.

## Pós-condição

- PLAN.md tem 5-15 steps (heurística — mais que 15 = decompor demais; menos que 5 = quase certo que falta detalhe)
- Cada step tem **todos** os 6 campos da anatomia
- Cada AC do SPEC.md está em pelo menos 1 step

## Validação interna

- [ ] Cobertura: toda AC do SPEC.md aparece em algum step (`ACs touched`)
- [ ] Dependências: grafo é acíclico
- [ ] Nenhum step diz "implementar a feature" — todos são específicos
- [ ] File paths são reais (verificáveis via Read/Bash)
- [ ] Cada subagent dispatch indica qual passo no PLAN.md a ler
