---
name: researching-task
description: Dispatcha subagents Explore em paralelo para investigar o codebase relativo à tarefa, consolida findings em research-notes.md (task-specific) e anexa findings duráveis ao CLAUDE.md (memória persistente entre sessões). Use após SPEC.md aprovada e antes de planejar a implementação.
user-invocable: true
---

# Researching Task

Pesquisa o codebase em paralelo via subagents, consolidando achados em dois destinos: **task-specific** (`research-notes.md`) e **durável** (`CLAUDE.md`).

## Pré-requisitos

- `SPEC.md` existe e está em `draft` ou `approved`
- `.status` aponta para tarefa em fase `spec` ou `research`

## Por que dois destinos

Pesquisa pesada que mora só no main thread queima contexto. Pesquisa que mora só na tarefa some entre sessões. A separação:

- **`research-notes.md`** — sumário consolidado *desta* tarefa. Vive em `.dev-loop/<task>/`. Detalhe que só importa para essa tarefa.
- **`CLAUDE.md`** (seção `## Project Context`) — findings sobre o projeto que valem para *futuras* tarefas. Vive na raiz. Persiste entre sessões.

Findings **duráveis** típicos: arquitetura de módulos, padrões de naming, gotchas reproduzíveis, dependências críticas, decisões com motivo não-óbvio.

Findings **task-specific** típicos: arquivos exatos a tocar nesta feature, integrações isoladas, refs de issue tracker.

## Processo

1. **Ler SPEC.md** completo.
2. **Derivar 3-5 sub-perguntas** que, respondidas, dão chão para planejar. Exemplos:
   - "Como X é implementado atualmente em `<dir>`?"
   - "Onde Y é chamado? Quantos call-sites?"
   - "Há padrão estabelecido para Z neste codebase?"
3. **Dispatchar subagents em paralelo** — `Explore` (built-in) para cada sub-pergunta. Veja `references/parallel-dispatch.md` para o padrão de prompting.
4. **Consolidar respostas** — cada subagent retorna sumário. Você junta em prosa estruturada.
5. **Classificar findings durável vs task-specific**:
   - Aplicável a outras tarefas? → durável → vai pro `CLAUDE.md`
   - Só relevante pra essa tarefa? → task-specific → vai pro `research-notes.md`
6. **Escrever `research-notes.md`** usando `templates/research-notes.tmpl.md` — toda síntese, links pra `CLAUDE.md` quando relevante.
7. **Atualizar `CLAUDE.md`** — anexar findings duráveis na subseção correta de `## Project Context (auto-curated by dev-loop)`. **Dedupe**: se um finding já existe ou contradiz, atualize em vez de duplicar.
8. **Atualizar `.status`**: `tasks.<slug>.phase = "research"`, `artifacts."research-notes.md" = "draft"`.

## Pós-condição

- `research-notes.md` existe, com mínimo 3 sub-perguntas respondidas
- `CLAUDE.md` tem novas entries duráveis (ou nenhuma, se a tarefa não rendeu insights duráveis)
- Nenhum file contents bruto foi puxado pro main thread (só sumários dos subagents)

## Validação interna

- [ ] Mínimo 3 sub-perguntas respondidas
- [ ] Cada subagent retornou sumário < 500 palavras
- [ ] Classificação durável vs task-specific feita explicitamente
- [ ] `CLAUDE.md` não duplica findings que já existem
- [ ] `research-notes.md` referencia (não copia) findings que foram pro `CLAUDE.md`
