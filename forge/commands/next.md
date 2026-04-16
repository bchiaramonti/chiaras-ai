---
description: Executa a próxima skill ou agent pendente da fase atual do Forge
---

# Forge Next

## Objetivo

Avançar o pipeline executando o próximo artefato pendente da fase atual.

## Processo

### 1. Ler `.status`

Ler o arquivo `.status` na raiz do projeto. Se não existir, informar:
"Nenhum projeto Forge encontrado. Execute `/forge:init <nome>` para começar."

### 2. Verificar pré-condição de fase

Se a fase atual **não** for `discovery` (a primeira), verificar que a fase anterior está `completed`. Se não estiver:
- Informar: "A fase anterior ([nome]) ainda não foi concluída."
- Listar artefatos pendentes da fase anterior
- PARAR — não avançar

### 3. Encontrar o próximo artefato pendente

Percorrer os artefatos da `current_phase` na **ordem de execução** (ver tabela abaixo). Encontrar o primeiro com status `pending`.

### 4. Identificar a skill/agent responsável

Usar a tabela de mapeamento para determinar qual skill ou agent deve ser invocado:

| Fase | Artefato | Skill/Agent |
|------|----------|-------------|
| discovery | `problem-statement` | `problem-framing` |
| discovery | `landscape-analysis` | `competitive-landscape` |
| product | `prd` | `product-definition` |
| product | `user-story-map` | `product-definition` |
| product | `shaped-pitch` | `scope-shaper` (agent) |
| product | `mvp-definition` | `scope-shaper` (agent) |
| design | `user-flows` | `user-flow-mapping` |
| design | `user-flows-diagram` | `user-flow-mapping` |
| design | `wireframes` | `wireframe-spec` |
| design | `design-system` | `design-system-bootstrap` |
| design | `design-tokens` | `design-system-bootstrap` |
| architecture | `architecture-overview` | `architecture-design` |
| architecture | `c4-context` | `architecture-design` |
| architecture | `c4-containers` | `architecture-design` |
| architecture | `c4-components` | `architecture-design` |
| architecture | `adrs` | `adr-writer` (chamado por `architecture-design`) |
| architecture | `data-model` | `data-model-designer` |
| architecture | `data-model-diagram` | `data-model-designer` |
| specs | `feature-specs` | `tech-spec-writer` |
| implementation | `code-standards` | `code-standards` |
| implementation | `implementation-plan` | `dev-orchestrator` (agent) |
| quality | `test-strategy` | `test-strategy` |
| quality | `qa-checklist` | `qa-checklist` |
| quality | `security-baseline` | `security-baseline` |
| deploy | `deploy-strategy` | `deploy-strategy` |
| deploy | `observability-setup` | `observability-setup` |

**Nota sobre skills que produzem múltiplos artefatos:** Algumas skills geram mais de um artefato (ex: `product-definition` gera `prd` + `user-story-map`). Quando o primeiro artefato de uma skill multi-artefato estiver `pending`, invocar a skill uma vez — ela gerará todos os seus artefatos de uma vez. Se o segundo artefato ainda estiver `pending` mas o primeiro já estiver `draft`, NÃO re-invocar a skill; a skill já foi executada.

### 5. Verificar pré-requisitos da skill/agent

- Ler o `SKILL.md` (ou agent `.md`) correspondente
- Verificar os **pré-requisitos** listados na skill (ex: artefatos que precisam estar `approved`)
- Se os pré-requisitos **NÃO** estiverem satisfeitos — informar o owner e PARAR:

```
Não é possível executar [skill-name] ainda.

Pré-requisitos não atendidos:
  📝 [artefato-x]: está em "draft" mas precisa estar "approved"

Execute /forge:review para aprovar os artefatos necessários.
```

**Nota:** Isso ocorre com skills que têm dependências intra-fase. Exemplos:
- `competitive-landscape` requer `problem-statement` com status `approved`
- `scope-shaper` requer `prd` e `user-story-map` com status `approved`

O fluxo correto nestes casos é: `/forge:next` → `/forge:review` (aprovar) → `/forge:next` (continuar).

### 6. Invocar a skill/agent

- Seguir as instruções da skill para gerar o(s) artefato(s)

### 7. Verificar resultado

Após execução da skill/agent:
- Verificar que o arquivo do artefato foi efetivamente criado no caminho esperado
- Se não foi criado, informar o erro e PARAR

### 8. Atualizar `.status`

- Marcar o(s) artefato(s) gerados como `draft` no `.status`
- Se a skill gera múltiplos artefatos, marcar TODOS como `draft`

### 9. Informar o owner

Apresentar ao usuário:

```
Artefato gerado: [nome-do-artefato]
Arquivo: [caminho-do-arquivo]
Status: draft

Próximo passo:
  - Revise o artefato gerado
  - Execute /forge:next para o próximo artefato
  - Ou /forge:review quando todos estiverem em draft
```

## Casos especiais

### Nenhum artefato `pending`

Se todos os artefatos da fase estão `draft` ou `approved`:

- Se todos `draft` → "Todos os artefatos estão em draft. Execute `/forge:review` para revisar e aprovar."
- Se todos `approved` → "Todos os artefatos estão aprovados! Execute `/forge:advance` para avançar à próxima fase."
- Se mix de `draft` + `approved` → "Artefatos em draft aguardando revisão. Execute `/forge:review`."

### Última fase (deploy) completa

Se `current_phase` é `deploy` e todos os artefatos estão `approved`:
"Pipeline completo! Todos os artefatos de todas as fases foram aprovados. O projeto está pronto para implementação final."
