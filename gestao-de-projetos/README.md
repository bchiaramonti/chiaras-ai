# Gestão de Projetos

Plugin de gestão de projetos para o [Cowork](https://claude.com/product/cowork). Decomponha objetivos estratégicos em sprints de 2 semanas com entregáveis concretos, depois gere relatórios executivos em PPTX com visualizações de timeline, grids de milestones e gráficos D3. Segue o sistema de marca M7 Investimentos.

## O que faz

Este plugin dá ao Claude a capacidade de planejar e acompanhar projetos de ponta a ponta:

- **Decomposição de metas em sprints** — Quebre objetivos estratégicos em sprints de 2 semanas com tarefas concretas. Gera `ROADMAP.md` com visão geral e `SPRINT-NN.md` para cada sprint, incluindo tarefas, critérios de aceite e dependências.
- **Relatórios de status executivo** — Gere apresentações PPTX profissionais a partir dos arquivos ROADMAP e SPRINT. Inclui slides de timeline com milestones coloridos, métricas de progresso, gráficos D3 (burndown, barras, scatter) e layout executivo com próximas ações e pontos de atenção.

## Skills

| Skill | Descrição |
|-------|-----------|
| `decomposing-goals-into-sprints` | Decompõe objetivos em sprints de 2 semanas com entregáveis concretos |
| `generating-project-status-reports` | Gera relatórios executivos PPTX com gráficos D3 e visualizações de timeline |
| `planning-clickup-sprints` | Configura Sprint Folders no ClickUp a partir de planos locais (ROADMAP/SPRINT) ou do zero |

## Exemplos de Uso

### Criar roadmap de um novo projeto

```
Você: Preciso planejar a implantação do novo CRM para a equipe comercial.
      O prazo final é agosto e precisamos migrar dados, treinar a equipe
      e integrar com o Bitrix24.

Claude: [Analisa o objetivo e identifica os entregáveis principais]
        [Gera ROADMAP.md com 5 sprints de 2 semanas]
        [Cria SPRINT-00.md (Fundação/Diagnóstico) até SPRINT-04.md (Consolidação)]
        [Cada sprint com tarefas começando por verbos de ação e critérios de aceite]
```

### Gerar relatório de status do projeto

```
Você: Gere o relatório de status semanal do projeto de padronização de processos.
      O caminho é 1-projects/padronizacao-processos/

Claude: [Lê ROADMAP.md e identifica sprints ativos (🔵 ou 🔴)]
        [Conta tarefas concluídas vs pendentes em cada SPRINT-NN.md]
        [Gera gráficos D3 de progresso e burndown]
        [Monta PPTX com cover, agenda, roadmap overview, status por sprint e riscos]
```

### Configurar sprints no ClickUp a partir do plano local

```
Você: Sincroniza o plano do projeto padronizacao-rituais com o ClickUp.
      Os arquivos estão em 1-projects/padronizacao-rituais-gestao-m7/

Claude: [Lê ROADMAP.md e identifica 5 sprints (S0–S4)]
        [Verifica workspace ClickUp — encontra Space "Investimentos"]
        [Cria Sprint Folder "Padronização Rituais de Gestão"]
        [Cria Sprint 0 a Sprint 4 com datas do ROADMAP]
        [Popula cada Sprint com tasks dos SPRINT-NN.md]
        [Cria List "Backlog" para items de escopo futuro]
        [Produz relatório: 24 tasks criadas em 5 sprints + 4 backlog items]
```

### Atualizar o roadmap após uma sprint review

```
Você: A Sprint 02 foi concluída. Atualize o ROADMAP.md marcando como
      concluída e verifique se a Sprint 03 pode iniciar.

Claude: [Atualiza status da Sprint 02 para ✅ no ROADMAP.md]
        [Verifica dependências da Sprint 03]
        [Confirma que pré-requisitos estão atendidos]
        [Atualiza o status da Sprint 03 para 🔵 Em andamento]
```

## Agents

Subagentes especializados que Claude invoca automaticamente em contexto isolado. Todos são read-only (não modificam arquivos do projeto).

| Agent | Quando é invocado | Output |
|-------|--------------------|--------|
| `clickup-specialist` | Interações com ClickUp, setup de Sprint Folders, sync de tasks, organização de workspace | Estruturas criadas/atualizadas no ClickUp, relatórios de sync |
| `sprint-reviewer` | Fim de sprint, retrospectivas, análise de velocity | Diagnóstico com completion rate, padrões e recomendações |
| `risk-analyst` | Planejamento, checkpoints, sprints atrasadas (🔴) | Mapa de dependências, matriz de riscos e mitigações |
| `stakeholder-communicator` | Status updates, reuniões com liderança, escalations | E-mails, pautas, talking points adaptados à audiência |

Os quatro agentes se complementam: `clickup-specialist` gerencia o workspace ClickUp, `sprint-reviewer` analisa a sprint, `risk-analyst` mapeia riscos, e `stakeholder-communicator` transforma tudo em comunicação executiva.

## MCP Servers

### ClickUp

Integração com o [ClickUp MCP Server oficial](https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server) via `.mcp.json`. Autenticação por OAuth 2.1 — ao instalar o plugin, rode `/mcp` no Claude Code para completar o OAuth flow no browser.

**Capabilities:**

| Categoria | Exemplos |
|-----------|----------|
| Task Management | Criar/atualizar tasks, bulk operations, tags, anexos |
| Time Tracking | Iniciar/parar timer, registrar tempo manual |
| Workspace | Navegar hierarquia (Spaces → Folders → Lists) |
| Docs | Criar/editar documentos e páginas |
| Chat | Enviar mensagens em canais |
| Search | Busca global no workspace |

## Requisitos

- **Python**: `python-pptx` (geração de PPTX)
- **Node.js** (opcional): `puppeteer@^22` (renderização de gráficos D3 em PNG)
