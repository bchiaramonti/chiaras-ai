---
description: Marca a fase atual como completa e avança para a próxima fase do Forge
---

# Forge Advance

## Objetivo

Fechar a fase atual e abrir a próxima. Esta é a única forma de transitar entre fases — nunca pular.

## Processo

### 1. Ler `.status`

Ler o arquivo `.status` na raiz do projeto. Identificar a `current_phase` e verificar o status de todos os artefatos.

Se não existir `.status`:
"Nenhum projeto Forge encontrado. Execute `/forge:init <nome>` para começar."

### 2. Verificar gate de aprovação

Verificar se **TODOS** os artefatos da fase atual estão com status `approved`.

Se **NÃO** — listar o que falta e BLOQUEAR:

```
Não é possível avançar. Artefatos pendentes na fase [nome]:

  📝 [artefato-1]: draft — aguardando aprovação
  ⏳ [artefato-2]: pending — ainda não gerado

Execute /forge:review para revisar os artefatos em draft.
Execute /forge:next para gerar os artefatos pendentes.
```

**NUNCA avançar com artefatos não aprovados.** Este é o gate mais importante do pipeline.

### 3. Marcar fase como `completed`

Se todos os artefatos estão `approved`:

- Atualizar `.status`: fase atual → `status: "completed"`
- Preencher `completed_at` com a data de hoje (`YYYY-MM-DD`)

### 4. Registrar no changelog

Invocar a skill `changelog-manager` para registrar a conclusão da fase:

- Ler `CHANGELOG.md`
- Adicionar entry sob `[Unreleased]` → `Added`:
  - "Fase [Nome] concluída: [lista dos artefatos gerados]"
- Salvar `CHANGELOG.md`

**Nota:** Se a skill `changelog-manager` ainda não estiver disponível (fases iniciais do desenvolvimento do plugin), fazer a atualização manualmente seguindo o formato Keep a Changelog.

### 5. Avançar para a próxima fase

Mapa de transição de fases:

| Fase Atual | Próxima Fase |
|------------|-------------|
| discovery | product |
| product | design |
| design | architecture |
| architecture | specs |
| specs | implementation |
| implementation | quality |
| quality | deploy |
| deploy | *(pipeline completo)* |

- Atualizar `current_phase` no `.status` para a próxima fase
- Atualizar a próxima fase: `status: "in_progress"`, `started_at: "YYYY-MM-DD"`

### 6. Apresentar resumo

```
Fase [N] — [Nome] concluída!

Artefatos entregues:
  ✅ [artefato-1]
  ✅ [artefato-2]

Entrando na Fase [N+1] — [Nome da próxima fase]

Artefatos esperados:
  ⏳ [artefato-a] (skill: [skill-name])
  ⏳ [artefato-b] (skill: [skill-name])

Execute /forge:next para começar.
```

## Caso especial: Pipeline completo

Se a fase atual é `deploy` e todos os artefatos estão `approved`:

- Marcar `deploy` como `completed`
- Registrar no changelog
- NÃO tentar avançar (não há próxima fase)

Apresentar:

```
Pipeline Forge COMPLETO!

Todas as 8 fases foram concluídas com sucesso:
  ✅ 0 — Discovery
  ✅ 1 — Product
  ✅ 2 — Design
  ✅ 3 — Architecture
  ✅ 4 — Specs
  ✅ 5 — Implementation
  ✅ 6 — Quality
  ✅ 7 — Deploy

O projeto [nome] está pronto para execução.
Todos os artefatos estão documentados e aprovados.
```
