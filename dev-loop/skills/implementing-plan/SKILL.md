---
name: implementing-plan
description: Executa o PLAN.md passo a passo. Para cada step marcado como subagent dispatcha com prompt mandatory-first-read que força o subagent a ler o PLAN.md completo antes de agir (anti-drift de modelos Opus). Steps no main thread executam sequencialmente respeitando o grafo de dependência. Use após PLAN.md aprovado.
user-invocable: true
---

# Implementing Plan

Executa o `PLAN.md` step-by-step. Cada subagent dispatched recebe o prompt **mandatory-first-read** que garante que ele leia o plano completo antes de agir.

## Pré-requisitos

- `PLAN.md` aprovado (ou rodado por `plan-critic`)
- `.status` em fase `plan` ou `implement`

## O prompt mandatory-first-read

Quando o PLAN.md marca um step como `Subagent: yes`, o dispatch dele começa **literalmente** assim:

```
Your FIRST ACTION must be: Read .dev-loop/<task>/PLAN.md in full.
Then execute Step <N> as specified there.
You may read SPEC.md, research-notes.md, and any file referenced by Step <N>.

When done: return a summary of what was changed (files + diff hints) — do NOT
return full file contents. The main thread will verify and commit.
```

Isso elimina o drift documentado em Opus 4.7 quando subagents recebem só "execute step N" sem o contrato completo. Veja `references/subagent-dispatch.md`.

## Processo

1. **Ler PLAN.md** completo. Marcar steps com state: `pending | in_progress | done | blocked`.
2. **Identificar próximo step** a executar:
   - Todos os `Depends on` devem estar `done`.
   - Se múltiplos elegíveis e nenhum depende do outro, escolher o primeiro pela ordem do plano (ou paralelizar — ver abaixo).
3. **Decidir mode**:
   - **Main thread**: ler arquivos, fazer edits, rodar verification.
   - **Subagent**: usar `Agent` tool com o mandatory-first-read prompt.
4. **Executar step** + rodar `Verification (in-step)` declarado.
5. **Se passou**: marcar `done`, atualizar `.status`, commit (opcional, se git existir), próximo step.
6. **Se falhou**: marcar `blocked`, parar, reportar ao usuário com diagnóstico — não tente magic-fix sem diagnose.
7. **Quando todos os steps `done`**: atualizar `.status` para fase `verify`, sugerir `/verifying-against-spec`.

## Estratégia de paralelismo

Steps com `Depends on: —` (independentes) podem ser dispachados em paralelo **se forem subagent steps**. Main-thread steps são sequenciais por natureza.

Não force paralelismo se o ganho é < custo do dispatch. Heurística: paralelizar 2+ steps `M` ou maiores; serializar `P`.

## Pós-condição

- Todos os steps marcados `done` em PLAN.md
- Código modificado segundo `Details` de cada step
- `.status` atualizado para fase `verify`

## Validação interna

- [ ] Nenhum step `pending` ou `in_progress` ao fim
- [ ] Cada subagent dispatched recebeu o prompt mandatory-first-read literal
- [ ] `Verification (in-step)` rodou e passou para cada step
- [ ] Mudanças no código estão alinhadas com `File:` e `Details:` (não tem code drift do plano)
