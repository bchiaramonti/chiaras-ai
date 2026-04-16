---
name: decomposing-goals-into-sprints
description: >
  Decompõe objetivos estratégicos em sprints de 2 semanas com entregas concretas, tarefas detalhadas
  e critérios de aceite. Gera ROADMAP.md com visão executiva e pasta sprints/ com SPRINT-NN.md por sprint.
  Use when the user asks to break down goals, create a roadmap, plan sprints, decompose objectives,
  build a project plan, define milestones, or structure a backlog. Also use when starting a new project
  and needing an execution plan with dates, owners, and deliverables.
---

# Decomposição de Objetivos em Sprints

Transforme objetivos estratégicos em planos de execução com sprints de 2 semanas, entregas concretas e critérios de aceite.

## Filosofia

**"Decomponha até que cada sprint caiba em 2 semanas e cada tarefa comece com um verbo."**

Um bom plano responde 3 perguntas para cada sprint:
1. **O que estará rodando** ao final? (Produto, não tarefa intermediária)
2. **Como saberemos** que está pronto? (Critérios de aceite verificáveis)
3. **O que bloqueia** o início? (Dependências explícitas)

## Workflow

### 1. Entender o objetivo (Big Goal)

Resuma em **1 frase** o que deve existir quando tudo estiver pronto:

```
[QUEM] terá [O QUE] funcionando até [QUANDO], resultando em [IMPACTO].

Exemplo: "A equipe de Performance terá rituais de gestão padronizados
para 6 funis até mai/2026, reduzindo 80% do tempo em reports manuais."
```

Se o usuário fornecer um objetivo vago, **pergunte** antes de decompor:
- Qual o prazo final?
- Quem é o responsável?
- O que "pronto" significa na prática?

### 2. Identificar entregas finais

Liste tudo que precisa existir quando o objetivo estiver 100% concluído:

- Artefatos (documentos, templates, dashboards, código)
- Processos rodando (rituais, automações, pipelines)
- Capacitações (treinamentos, manuais, handoffs)

**Regra**: Se não é verificável ("melhorar a comunicação"), não é entrega. Reformule como algo concreto ("manual de comunicação publicado e treinamento realizado").

### 3. Agrupar em sprints de 2 semanas

```
Sprint 0 — Fundação       (SEMPRE primeiro: diagnóstico, mapeamento, setup)
Sprint 1 — [Primeiro domínio/entrega]
Sprint 2 — [Segundo domínio/entrega]
Sprint N — Consolidação    (SEMPRE último: escala, documentação, handoff)
```

**Critérios de agrupamento:**
- Cada sprint entrega algo **operacional** (rodando, publicado, validado)
- Sprints com dependência forte ficam em sequência
- Sprints independentes podem ser executados em paralelo
- Max 5-8 sprints por projeto (se mais, divida o projeto)

### 4. Detalhar tarefas por sprint

Cada tarefa segue o formato: **Verbo + Objeto + Detalhe**

```
- [ ] Mapear processos AS-IS dos 6 funis — entrevistas com gestores
- [ ] Configurar template de report no Cowork — incluir KPIs definidos no S0
- [ ] Validar ritual N2 com gestor de Investimentos — reunião presencial
```

**Regras de tarefas:**
- Sempre começa com verbo (Criar, Configurar, Mapear, Validar, Treinar, Documentar)
- Max 15 tarefas por sprint
- Se > 15, divida o sprint ou agrupe tarefas relacionadas
- Inclua tarefas de validação (não só criação)

### 5. Mapear dependências e riscos

Para cada sprint, declare:
- **Depende de**: quais sprints devem estar concluídos antes
- **Desbloqueia**: quais sprints ficam disponíveis após conclusão
- **Riscos**: o que pode atrasar e qual a contramedida

## Formato de Output

A skill gera **2 tipos de arquivo** no diretório do projeto:

```
<projeto>/
├── ROADMAP.md              ← Visão geral executiva
└── sprints/
    ├── SPRINT-00.md        ← Detalhamento Sprint 0
    ├── SPRINT-01.md        ← Detalhamento Sprint 1
    ├── SPRINT-02.md
    └── ...
```

### ROADMAP.md

Visão executiva compacta: Big Goal, tabela de sprints com links, dependências e riscos.

### SPRINT-NN.md

Detalhamento de cada sprint: objetivo, produto, tarefas (checkbox), responsável, critérios de aceite.

Para os templates completos com exemplos, veja [references/templates.md](references/templates.md).

## Regras de Qualidade

### Por Sprint

- [ ] Cabe em 2 semanas?
- [ ] Tem "Produto" concreto e verificável?
- [ ] Tarefas começam com verbo?
- [ ] Max 15 tarefas?
- [ ] Dependências declaradas?
- [ ] Critérios de aceite objetivos?

### Por Roadmap

- [ ] Sprint 0 é fundação/diagnóstico?
- [ ] Último sprint inclui consolidação/handoff?
- [ ] Dependências formam DAG (sem ciclos)?
- [ ] Total ≤ 8 sprints (senão, divida o projeto)?
- [ ] Big Goal é 1 frase clara?
- [ ] Riscos mapeados com contramedidas?

## Regras Importantes

1. **Produto, não tarefa** — O sprint entrega algo "rodando", não um artefato intermediário
2. **Sprint 0 sempre** — Todo projeto começa com fundação (diagnóstico, setup, mapeamento)
3. **Verbo primeiro** — Cada tarefa é acionável ("Criar X", não "X precisa ser criado")
4. **15 é o máximo** — Se tem mais tarefas, o sprint é grande demais
5. **Dependência explícita** — Se Sprint 2 precisa do 1, declare
6. **Critérios verificáveis** — "Melhorar" não é critério. "Tempo < 2h/semana" é
7. **Datas reais** — Use semanas do calendário (DD/MM → DD/MM), não "semana 1"
8. **Pergunte antes de assumir** — Se o objetivo é vago, peça clarificação
