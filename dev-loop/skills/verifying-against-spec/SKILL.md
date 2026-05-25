---
name: verifying-against-spec
description: Cruza cada Acceptance Criteria do SPEC.md contra o estado atual do código, testes e comportamento — produz VERIFY.md com checklist 1-para-1. Gate final antes de fechar a tarefa — falha em qualquer AC não fecha e sugere voltar para plan ou spec. Use após todos os steps do PLAN.md em estado done.
user-invocable: true
---

# Verifying Against Spec

Verifica cada Acceptance Criteria do `SPEC.md` 1-para-1, produzindo `VERIFY.md` que é o gate "done".

## Pré-requisitos

- Todos os steps do `PLAN.md` em `done`
- `.status` em fase `implement` ou `verify`

## Princípio

"Done" não é "passou nos testes" nem "achei que tá ok". **Done = todo AC do SPEC.md verifiquei e passou pelo método declarado**. Se um AC não tem método verificável, o problema é na spec — volte pra `writing-spec`.

## Processo

1. **Ler SPEC.md** — extrair lista de ACs com seus métodos de verificação.
2. **Ler PLAN.md** — confirmar quais steps cobriram cada AC.
3. **Para cada AC**:
   - **test:unit / test:integration** → rodar o teste relevante. Capturar PASS/FAIL.
   - **manual** → executar o procedimento manual (UI check, API call). Documentar input/output.
   - **inspect** → ler o código modificado e confirmar a propriedade.
4. **Edge cases não-spec**:
   - Roda testes existentes pra garantir que não regrediu.
   - Verifica que arquivos `out of scope` do SPEC.md não foram tocados.
5. **Escrever VERIFY.md** usando `templates/VERIFY.tmpl.md`.
6. **Decidir resultado**:
   - **Todos PASS** → atualizar `.status` para fase `done`. Sugerir commit/PR. Sugerir update do CHANGELOG.md.
   - **Algum FAIL** → não fecha. Documentar a causa. Sugerir: "Voltar pra `planning-implementation` (gap no plano) ou `writing-spec` (gap na spec)?"
7. **Não force pass** — se um AC é ambíguo, anote como `INCONCLUSIVE` e devolva pra spec.

## Pós-condição

- `VERIFY.md` existe com 1 linha por AC + status PASS/FAIL/INCONCLUSIVE
- Resultado da regressão de testes existentes documentado
- `.status` em `done` (se todos PASS) ou `verify` (com block)

## Validação interna

- [ ] Cada AC do SPEC.md tem linha em VERIFY.md
- [ ] Cada PASS tem evidência (comando rodado, output ou print)
- [ ] Cada FAIL tem causa atribuída (qual step do PLAN.md, qual gap)
- [ ] Testes existentes não regrediram (rodada documentada)
