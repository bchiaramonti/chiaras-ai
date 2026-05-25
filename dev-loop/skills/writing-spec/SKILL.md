---
name: writing-spec
description: Estrutura uma tarefa em SPEC.md com os 4 campos do single-turn pattern (intent, constraints, acceptance criteria, file locations). Use no início de cada tarefa do dev-loop, antes de pesquisar ou planejar — a spec é o contrato que research, plan, implement e verify leem a jusante.
user-invocable: true
---

# Writing Spec

Estrutura uma tarefa em `SPEC.md` seguindo o **single-turn pattern** do Opus 4.7. A spec é o contrato — tudo a jusante (research, plan, implement, verify) lê dela.

## Pré-requisitos

- `.dev-loop/<task-slug>/` deve existir (criado por `/dev-loop:start`)
- `.dev-loop/.status` aponta para uma tarefa em fase `spec`

## Os 4 campos obrigatórios

Toda SPEC.md tem **4 seções não-negociáveis**. Se qualquer uma estiver incompleta, a spec não fecha.

### 1. Intent
- Frase única no formato "Como/Para [persona], quero [resultado], para que [benefício]"
- O QUE e PARA QUEM. Não o COMO.

### 2. Constraints
- Tecnologias obrigatórias (linguagem, framework, libs)
- Limites de performance, custo, prazo
- Compatibilidade com código existente
- Não-fazeres explícitos ("não introduzir nova dependência X")

### 3. Acceptance Criteria
- Lista verificável. Cada AC tem:
  - Descrição (Given/When/Then ou checklist)
  - Método de verificação (`test:unit` / `test:integration` / `manual` / `inspect`)
- Mínimo: 3 ACs. Máximo recomendado: 8.
- Cada AC é independentemente verdadeiro/falso.

### 4. File locations
- Caminhos exatos de arquivos a CRIAR
- Caminhos exatos de arquivos a MODIFICAR
- Padrões glob são aceitáveis quando houver many-files

## Processo

1. **Ler input do usuário** — a descrição inicial da tarefa.
2. **Identificar gaps** — quais dos 4 campos estão claros? Quais faltam?
3. **Batched questions** — se houver gaps, fazer TODAS as perguntas em UM bloco via `AskUserQuestion`. Máximo 5 perguntas. Não fazer round-trips.
4. **Inferir o inferível** — se `CLAUDE.md` ou código existente respondem, não pergunte. Marque como `(inferido de <fonte>)`.
5. **Escrever SPEC.md** usando `templates/SPEC.tmpl.md`.
6. **Atualizar `.dev-loop/.status`**: `tasks.<slug>.artifacts."SPEC.md" = "draft"`.
7. **Sugerir gate opcional**: "Spec gerado. Quer rodar `spec-auditor` antes de prosseguir para research? (recomendado para tarefas G+)"

## Pós-condição

- `SPEC.md` existe em `.dev-loop/<slug>/SPEC.md`
- Os 4 campos têm conteúdo real (sem placeholder)
- Cada AC é verificável

## Validação interna (antes de salvar)

- [ ] Intent tem persona + resultado + benefício
- [ ] Constraints lista pelo menos 1 item (mesmo que seja "nenhuma constraint explícita")
- [ ] Mínimo 3 ACs, cada um com método de verificação declarado
- [ ] File locations exatos (ou globs justificados)
- [ ] Nenhuma seção contém TODO/placeholder
