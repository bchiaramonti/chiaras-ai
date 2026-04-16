---
name: planning-clickup-sprints
description: >
  Plan and configure sprints in ClickUp from local project plans or from scratch. Creates Sprint
  Folders, populates sprints with tasks from ROADMAP.md/SPRINT-NN.md files, sets up backlogs,
  configures dates and assignees, and validates the sprint structure. Use when the user asks to
  set up sprints in ClickUp, sync a project plan to ClickUp, create a Sprint Folder, populate
  a backlog, plan a new sprint cycle, or organize work into ClickUp sprints. Also use when
  discussing sprint setup, sprint folder configuration, or ClickUp sprint workflow.
---

# Planejamento de Sprints no ClickUp

Configure e popule sprints no ClickUp a partir de planos locais (ROADMAP.md / SPRINT-NN.md)
ou do zero, garantindo hierarquia correta, tasks bem formatadas e backlog organizado.

## Filosofia

**"O plano vive no ROADMAP — a execução vive no ClickUp."**

O ClickUp é a ferramenta de execução. O planejamento pode vir de arquivos locais (gerados pela
skill `decomposing-goals-into-sprints`) ou ser feito direto no ClickUp. Esta skill garante que
a estrutura no ClickUp esteja correta e completa para execução.

## Pré-requisitos

- ClickUp MCP Server conectado (via `.mcp.json`)
- Workspace com pelo menos 1 Space configurado
- (Opcional) Arquivos ROADMAP.md e sprints/SPRINT-NN.md se sincronizando de plano local

## Workflow Principal

### Fase 1: Reconhecimento

Antes de criar qualquer coisa, entenda o estado atual.

1. **Ler workspace** — Use `clickup_get_workspace_hierarchy` para mapear Spaces, Folders e Lists existentes
2. **Identificar destino** — Pergunte ao usuário qual Space usar (ou se precisa criar)
3. **Verificar existência** — Cheque se já existe um Sprint Folder para o projeto
4. **Ler plano local** (se disponível) — Parse ROADMAP.md para visão geral, cada SPRINT-NN.md para tasks

```
Checklist de reconhecimento:
- [ ] Workspace hierarchy mapeada
- [ ] Space destino identificado
- [ ] Sprint Folder existente verificado
- [ ] Plano local lido e parseado (se aplicável)
```

### Fase 2: Criar Estrutura

Montar a hierarquia no ClickUp seguindo o modelo correto.

#### Opção A: Novo Sprint Folder (projeto novo)

1. Pergunte: **Qual o nome do projeto?** (será o nome do Sprint Folder)
2. Pergunte: **Quantos sprints no ciclo inicial?**
3. Pergunte: **Data de início do primeiro sprint?**
4. Pergunte: **Duração de cada sprint?** (default: 2 semanas)
5. **Criar Sprint Folder** via `clickup_create_folder` no Space destino
6. O primeiro Sprint é criado automaticamente pelo ClickUp
7. **Criar Sprints adicionais** como Lists dentro do Sprint Folder
8. **Criar List "Backlog"** dentro do Sprint Folder para tasks não alocadas

```
Resultado esperado:
Space: [nome]
└── Sprint Folder: [nome do projeto]
    ├── Sprint 1 (DD/MM - DD/MM)
    ├── Sprint 2 (DD/MM - DD/MM)
    ├── ...
    └── Backlog
```

#### Opção B: Populando Sprint Folder existente

1. Use `clickup_get_workspace_hierarchy` para encontrar o Sprint Folder
2. Use `clickup_get_list` para cada Sprint existente
3. Compare com o plano local para identificar o que falta criar

#### Opção C: Sem plano local (do zero)

1. Criar Sprint Folder
2. Guiar o usuário na definição de objetivos por sprint
3. Criar tasks diretamente no ClickUp conforme definido

### Fase 3: Popular Tasks

Para cada sprint, criar tasks a partir dos arquivos SPRINT-NN.md.

#### Parsing de SPRINT-NN.md

```markdown
# Sprint 0 — Fundação               → Nome do Sprint: "Sprint 0 — Fundação"
**Período:** 24/fev → 07/mar        → start_date: 2026-02-24, due_date: 2026-03-07

### Diagnóstico                      → Tag de grupo: "diagnóstico"
- [ ] **Entrevistar 8 gestores**     → Task name: "Entrevistar 8 gestores"
      — roteiro semi-estruturado       → Description: "roteiro semi-estruturado, 30min cada"
  - critério de aceite 1              → Description (append): "\n\nCritérios de aceite:\n- critério 1"
```

#### Regras de Criação de Tasks

| Campo ClickUp | Origem | Regra |
|---------------|--------|-------|
| `name` | Texto em negrito após `- [ ]` | Remover `**` e markdown formatting |
| `description` | Texto após `—` + critérios indentados | Markdown formatado |
| `list_id` | Sprint correspondente no ClickUp | Obrigatório — buscar via hierarchy |
| `due_date` | Período do sprint no SPRINT file | Data fim do sprint (formato YYYY-MM-DD) |
| `start_date` | Período do sprint no SPRINT file | Data início do sprint |
| `priority` | Inferido (ver tabela abaixo) | normal como default |
| `tags` | Nome do grupo lógico + "sprint-NN" | Array de strings |
| `assignees` | Campo "Responsável" do SPRINT file | Resolver via `clickup_resolve_assignees` |

#### Mapeamento de Prioridade

| Contexto da task | Prioridade |
|-----------------|-----------|
| Bloqueia outro sprint (dependência declarada) | high |
| Envolve stakeholder externo ou aprovação | high |
| Task de validação ou review | normal |
| Documentação, manual, cleanup | low |
| Default | normal |

#### Critérios de Aceite → Checklist

Se o SPRINT file tem critérios de aceite sob `## Critérios de Aceite`, crie-os como
itens na description da task principal (com checkbox markdown `- [ ]`):

```markdown
## Critérios de Aceite
- [ ] 6 funis mapeados com fluxo AS-IS documentado
- [ ] Matriz de dores consolidada e priorizada
```

### Fase 4: Configurar Backlog

O Backlog é uma List regular dentro do Sprint Folder.

1. **Criar List "Backlog"** se não existir
2. **Popular com items não alocados** — tasks que existem no ROADMAP mas não pertencem a nenhum sprint específico
3. **Definir prioridades** — Ordenar por prioridade (urgent > high > normal > low)
4. **Marcar items candidatos** — Se o ROADMAP tem seção de "Decisões de Escopo" com items fora de escopo que podem voltar, adicionar como low priority no Backlog

### Fase 5: Validação

Após criar tudo, verificar a integridade da estrutura.

```
Checklist de validação:
- [ ] Sprint Folder existe com nome correto
- [ ] Cada sprint tem datas de início e fim
- [ ] Sprints não se sobrepõem em datas
- [ ] Cada task tem nome, description e due_date
- [ ] Backlog List existe
- [ ] Nenhuma task está orphan (sem List)
- [ ] Total de tasks por sprint ≤ 15
- [ ] Tasks com dependências estão em sprints sequenciais
```

### Fase 6: Relatório de Execução

Ao finalizar, produzir um relatório resumido:

```markdown
## Sprint Planning — Relatório de Setup

**Projeto**: [nome]
**Space**: [nome do space]
**Sprint Folder**: [nome] (ID: XXXXXX)

### Estrutura Criada

| Sprint | Tasks | Período | List ID |
|--------|-------|---------|---------|
| Sprint 0 — Fundação | 9 tasks | 24/fev → 07/mar | 12345 |
| Sprint 1 — Investimentos | 11 tasks | 10/mar → 21/mar | 12346 |
| Backlog | 4 items | — | 12347 |

### Totais
- **Tasks criadas**: 24
- **Sprints configurados**: 3
- **Backlog items**: 4

### Próximos Passos
1. Revisar tasks no ClickUp e ajustar assignees
2. Lock sprint forecast no Sprint 0
3. Configurar Sprint Automations (se Business Plan)
```

## Cenários Especiais

### Replanejar sprints (mid-cycle)

Quando o usuário quer reorganizar sprints em andamento:

1. **NÃO deletar tasks existentes** — Mover para o sprint correto
2. Verificar spillover pending
3. Atualizar datas se necessário
4. Registrar motivo do replanejamento como comentário

### Sincronizar ClickUp → Local

Quando o estado do ClickUp está mais atualizado que os arquivos locais:

1. Ler tasks de cada Sprint List no ClickUp
2. Comparar com `- [ ]` / `- [x]` nos SPRINT files
3. Propor atualizações nos arquivos locais (com confirmação do usuário)

### Múltiplos projetos no mesmo Space

Cada projeto deve ter seu próprio Sprint Folder:
```
Space: Investimentos
├── Sprint Folder: Padronização RG
│   ├── Sprint 1
│   └── Backlog
├── Sprint Folder: Implantação CRM
│   ├── Sprint 1
│   └── Backlog
└── Folder regular: Referências (docs compartilhados)
```

## Integração com Outras Skills e Agents

| Componente | Relação |
|-----------|---------|
| `decomposing-goals-into-sprints` | **Input**: Usa ROADMAP.md e SPRINT-NN.md como fonte para popular o ClickUp |
| `sprint-reviewer` | **Downstream**: Após sprints executados, analisa delivery vs planejado |
| `risk-analyst` | **Parallel**: Pode ser invocado durante o planejamento para mapear riscos |
| `clickup-specialist` | **Agent**: Consulta especializada sobre ClickUp hierarchy e operações |
| `generating-project-status-reports` | **Downstream**: Usa dados de sprint para gerar relatórios executivos |

## Anti-Patterns to Avoid

- **Nunca criar Sprint Folder sem confirmar o Space** — Pergunte ao usuário
- **Nunca popular tasks sem ler o SPRINT file inteiro** — Contexto importa
- **Nunca ignorar tasks existentes** — Sempre cheque duplicatas antes de criar
- **Nunca criar Sprint sem datas** — Sprints precisam de start_date e due_date
- **Nunca exceder 15 tasks por sprint** — Se o SPRINT file tem mais, alerte o usuário
- **Nunca assumir assignees** — Resolva via `clickup_resolve_assignees` ou pergunte
- **Nunca deletar tasks do ClickUp** — Mova para Backlog ou archive, nunca delete
- **Nunca criar estrutura sem reconhecimento** — Fase 1 é obrigatória
