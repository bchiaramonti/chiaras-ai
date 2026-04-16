# User Story Map — <PROJECT_NAME>

> **Fase:** Product
> **Skill:** product-definition
> **Status:** draft
> **Data:** <YYYY-MM-DD>
> **Referência:** Jeff Patton — User Story Mapping

---

## 1. Backbone (Jornada do Usuário)

<!-- O backbone representa as atividades principais do usuário em ordem cronológica de uso. Cada atividade é um épico do PRD. Ler da esquerda para a direita = jornada completa do usuário. -->

| Ordem | Atividade | Épico (PRD) | Persona principal |
|-------|-----------|-------------|-------------------|
| 1 | <ATIVIDADE_1> | <EPICO_1> | <PERSONA_1> |
| 2 | <ATIVIDADE_2> | <EPICO_2> | <PERSONA_2> |
| 3 | <ATIVIDADE_3> | <EPICO_3> | <PERSONA_3> |

<!-- Adicionar atividades conforme necessário -->

---

## 2. Detalhamento por Atividade

<!-- Para cada atividade do backbone, listar as stories em ordem de prioridade (de cima para baixo = mais importante para menos importante). A posição vertical define a prioridade. -->

### Atividade 1: <ATIVIDADE_1>

| Prioridade | ID | User Story | MoSCoW |
|------------|-----|-----------|--------|
| 1 (topo) | US-<ID> | <STORY_RESUMIDA> | Must |
| 2 | US-<ID> | <STORY_RESUMIDA> | Must |
| 3 | US-<ID> | <STORY_RESUMIDA> | Should |
| 4 | US-<ID> | <STORY_RESUMIDA> | Could |

### Atividade 2: <ATIVIDADE_2>

| Prioridade | ID | User Story | MoSCoW |
|------------|-----|-----------|--------|
| 1 (topo) | US-<ID> | <STORY_RESUMIDA> | Must |
| 2 | US-<ID> | <STORY_RESUMIDA> | Should |
| 3 | US-<ID> | <STORY_RESUMIDA> | Won't |

### Atividade 3: <ATIVIDADE_3>

| Prioridade | ID | User Story | MoSCoW |
|------------|-----|-----------|--------|
| 1 (topo) | US-<ID> | <STORY_RESUMIDA> | Must |
| 2 | US-<ID> | <STORY_RESUMIDA> | Could |

<!-- Adicionar atividades conforme necessário -->

---

## 3. Linha de Corte MVP

<!-- A linha de corte separa o que entra no MVP (acima) do que fica para versões futuras (abaixo). Deve ser consistente com a priorização MoSCoW do PRD: Must + Should = MVP. -->

### Acima da linha (MVP)

| Atividade | Stories incluídas | Qtd |
|-----------|------------------|-----|
| <ATIVIDADE_1> | US-<IDS> | <QTD> |
| <ATIVIDADE_2> | US-<IDS> | <QTD> |
| <ATIVIDADE_3> | US-<IDS> | <QTD> |
| **Total MVP** | | **<TOTAL>** |

### Abaixo da linha (Versão futura)

| Atividade | Stories excluídas | MoSCoW | Motivo |
|-----------|------------------|--------|--------|
| <ATIVIDADE_N> | US-<IDS> | Could | <MOTIVO> |
| <ATIVIDADE_N> | US-<IDS> | Won't | <MOTIVO> |

---

## 4. Visualização

<!-- Representação visual simplificada do mapa. Cada coluna = atividade do backbone. Cada linha = nível de prioridade. A linha `---MVP---` separa o escopo. -->

```
| Atividade 1     | Atividade 2     | Atividade 3     |  ← Backbone
|-----------------|-----------------|-----------------|
| US-001 (Must)   | US-004 (Must)   | US-006 (Must)   |  ← Essencial
| US-002 (Must)   | US-005 (Should) |                 |
| US-003 (Should) |                 |                 |
|═══════ MVP ═════|═══════ MVP ═════|═══════ MVP ═════|  ← Linha de corte
| US-0XX (Could)  | US-0XX (Won't)  | US-0XX (Could)  |  ← Futuro
```

<!-- Substituir pelo mapa real do projeto. Ajustar colunas conforme atividades. -->

---

## Status

- **Criado em:** <YYYY-MM-DD>
- **Última atualização:** <YYYY-MM-DD>
- **Status:** draft
- **Aprovado por:** —
- **Data de aprovação:** —
