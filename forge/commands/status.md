---
description: Mostra a fase atual do projeto Forge, artefatos pendentes e progresso geral
---

# Forge Status

## Objetivo

Ler `.status` e apresentar uma visão clara e visual do progresso do projeto.

## Processo

### 1. Ler `.status`

Ler o arquivo `.status` na raiz do projeto. Se não existir, informar:
"Nenhum projeto Forge encontrado. Execute `/forge:init <nome>` para começar."

### 2. Calcular progresso

- Contar fases com status `completed` / total (8)
- Identificar `current_phase` e seus artefatos
- Para cada artefato da fase atual, verificar o status (`pending`, `draft`, `approved`)

### 3. Formatar output visual

Apresentar no seguinte formato:

```
Status do Projeto: [NOME DO PROJETO]

Fase atual: [N] [Nome da Fase]  [BARRA DE PROGRESSO]  [XX]%

Artefatos da fase:
  [ICONE] [nome-do-artefato]  ([status])
  [ICONE] [nome-do-artefato]  ([status])
  ...

Progresso geral: [BARRA] [N]/8 fases completas
```

#### Ícones por status de artefato
- `approved` → checkmark verde (usar texto "OK")
- `draft` → lápis (usar texto "DRAFT — aguardando revisão")
- `pending` → relógio (usar texto "pendente")

#### Barra de progresso da fase
Calcular percentual de artefatos da fase atual:
- `approved` = 100% do peso
- `draft` = 50% do peso
- `pending` = 0%

### 4. Sugerir próximo passo

Com base no estado atual, sugerir a ação mais adequada:

| Estado | Sugestão |
|--------|----------|
| Todos `pending` | "Execute `/forge:next` para começar o próximo artefato." |
| Algum `draft`, algum `pending` | "Execute `/forge:next` para avançar ao próximo artefato pendente." |
| Todos `draft` | "Todos os artefatos estão em draft. Execute `/forge:review` para revisar e aprovar." |
| Todos `approved` | "Fase pronta! Execute `/forge:advance` para avançar para a próxima fase." |
| Mix de `draft` e `approved` | "Execute `/forge:review` para revisar os artefatos em draft." |

### 5. Mostrar timeline de fases

Abaixo do status da fase atual, mostrar um resumo compacto de todas as 8 fases:

```
Pipeline:
  [OK] 0 Discovery        concluída em YYYY-MM-DD
  [>>] 1 Product           em andamento
  [  ] 2 Design
  [  ] 3 Architecture
  [  ] 4 Specs
  [  ] 5 Implementation
  [  ] 6 Quality
  [  ] 7 Deploy
```

Legenda:
- `[OK]` = fase `completed`
- `[>>]` = fase `in_progress` (current_phase)
- `[  ]` = fase `not_started`
