---
description: Detalha uma fase específica do pipeline Forge com seus artefatos, skills e dependências
argument-hint: <discovery|product|design|architecture|specs|implementation|quality|deploy>
---

# Forge Phase: $ARGUMENTS

## Objetivo

Mostrar detalhes completos de uma fase do pipeline: skills/agents envolvidos, artefatos esperados com status atual, dependências com fases anteriores e frameworks/metodologias utilizados.

## Processo

### 1. Validar argumento

Se `$ARGUMENTS` estiver vazio ou não for um nome de fase válido, informar:

```
Uso: /forge:phase <nome-da-fase>

Fases válidas:
  discovery       Fase 0 — Entender o problema e o mercado
  product         Fase 1 — Definir produto, personas e MVP
  design          Fase 2 — Fluxos, wireframes e design system
  architecture    Fase 3 — Arquitetura C4, stack e data model
  specs           Fase 4 — Especificações técnicas por feature
  implementation  Fase 5 — Padrões de código e plano de implementação
  quality         Fase 6 — Estratégia de testes, QA e segurança
  deploy          Fase 7 — Estratégia de deploy e observabilidade
```

PARAR se argumento inválido.

### 2. Ler `.status`

Ler o arquivo `.status` na raiz do projeto. Se não existir, informar:
"Nenhum projeto Forge encontrado. Execute `/forge:init <nome>` para começar."

Extrair:
- Status da fase solicitada (`not_started`, `in_progress`, `completed`)
- Status de cada artefato da fase (`pending`, `draft`, `approved`)
- `current_phase` do projeto (para contextualizar se a fase solicitada é passada, atual ou futura)

### 3. Ler `references/pipeline-overview.md`

Extrair para a fase solicitada:
- Seção 2: skill/agent responsável por cada artefato
- Seção 6: ordem de execução das skills dentro da fase
- Seção 5: regras fundamentais aplicáveis

### 4. Apresentar detalhes da fase

Formatar o output com as 4 seções abaixo.

#### 4.1 Header

```
Fase [N] — [Nome da Fase]
Status: [not_started | in_progress | completed]
[Contexto: "Esta é a fase atual" | "Fase já concluída" | "Fase futura — [N] fases à frente"]
```

#### 4.2 Skills e Agents

Tabela com skills/agents da fase, na ordem de execução:

```
Skills/Agents (ordem de execução):

  Ordem  Tipo     Nome                      Descrição
  1      skill    [nome-da-skill]           [descrição curta]
  2      agent    [nome-do-agent]           [descrição curta]
```

Usar a seguinte referência completa:

| Fase | Ordem | Tipo | Nome | Descrição |
|------|-------|------|------|-----------|
| discovery | 1 | skill | problem-framing | Enquadra o problema, público e hipótese de solução |
| discovery | 2 | skill | competitive-landscape | Analisa concorrentes, gaps e posicionamento |
| product | 1 | skill | product-definition | Gera PRD com personas, épicos, user stories e story map |
| product | 2 | agent | scope-shaper | Molda escopo do MVP com appetite e trade-offs |
| design | 1 | skill | user-flow-mapping | Mapeia fluxos de navegação com diagramas Mermaid |
| design | 2 | skill | wireframe-spec | Gera wireframe textual por tela com estados e ações |
| design | 3 | skill | design-system-bootstrap | Define design system com tokens e catálogo de componentes |
| architecture | 1 | skill | architecture-design | Projeta arquitetura C4, stack e padrões (invoca adr-writer) |
| architecture | 2 | skill | data-model-designer | Projeta modelo de dados com diagrama ER |
| specs | 1 | skill | tech-spec-writer | Gera especificação técnica por feature do MVP |
| implementation | 1 | skill | code-standards | Define padrões de código e configurações de linter |
| implementation | 2 | agent | dev-orchestrator | Planeja implementação com dependências e ordem de build |
| quality | 1 | skill | test-strategy | Define estratégia de testes (pirâmide, cobertura) |
| quality | 2 | skill | qa-checklist | Gera checklist de QA para verificação antes do deploy |
| quality | 3 | skill | security-baseline | Avalia segurança contra OWASP Top 10 |
| deploy | 1 | skill | deploy-strategy | Define plataforma, CI/CD, env vars e rollback |
| deploy | 2 | skill | observability-setup | Define logging, error tracking e health checks |

#### 4.3 Artefatos

Tabela com artefatos da fase e status atual (lido do `.status`):

```
Artefatos:

  Artefato                 Arquivo                                      Status     Skill/Agent
  [nome-artefato]          [caminho-do-arquivo]                         [status]   [skill-responsavel]
```

Ícones por status:
- `approved` → "OK"
- `draft` → "DRAFT"
- `pending` → "pendente"

Usar a seguinte referência completa de artefatos por fase:

| Fase | Artefato | Arquivo | Skill/Agent |
|------|----------|---------|-------------|
| discovery | problem-statement | `00-discovery/problem-statement.md` | problem-framing |
| discovery | landscape-analysis | `00-discovery/landscape-analysis.md` | competitive-landscape |
| product | prd | `01-product/prd.md` | product-definition |
| product | user-story-map | `01-product/user-story-map.md` | product-definition |
| product | shaped-pitch | `01-product/shaped-pitch.md` | scope-shaper |
| product | mvp-definition | `01-product/mvp-definition.md` | scope-shaper |
| design | user-flows | `02-design/user-flows.md` | user-flow-mapping |
| design | user-flows-diagram | `02-design/user-flows.mermaid` | user-flow-mapping |
| design | wireframes | `02-design/wireframes/` | wireframe-spec |
| design | design-system | `02-design/design-system.md` | design-system-bootstrap |
| design | design-tokens | `02-design/design-tokens.json` | design-system-bootstrap |
| architecture | architecture-overview | `03-architecture/architecture-overview.md` | architecture-design |
| architecture | c4-context | `03-architecture/c4-context.mermaid` | architecture-design |
| architecture | c4-containers | `03-architecture/c4-containers.mermaid` | architecture-design |
| architecture | c4-components | `03-architecture/c4-components.mermaid` | architecture-design |
| architecture | adrs | `03-architecture/adrs/` | adr-writer (via architecture-design) |
| architecture | data-model | `03-architecture/data-model.md` | data-model-designer |
| architecture | data-model-diagram | `03-architecture/data-model.mermaid` | data-model-designer |
| specs | feature-specs | `04-specs/features/` | tech-spec-writer |
| implementation | code-standards | `05-implementation/code-standards.md` | code-standards |
| implementation | implementation-plan | `05-implementation/implementation-plan.md` | dev-orchestrator |
| quality | test-strategy | `06-quality/test-strategy.md` | test-strategy |
| quality | qa-checklist | `06-quality/qa-checklist.md` | qa-checklist |
| quality | security-baseline | `06-quality/security-baseline.md` | security-baseline |
| deploy | deploy-strategy | `07-deploy/deploy-strategy.md` | deploy-strategy |
| deploy | observability-setup | `07-deploy/observability-setup.md` | observability-setup |

#### 4.4 Dependências

Mostrar o que deve estar concluído antes de entrar nesta fase:

```
Dependências:

  Fase anterior que deve estar completed:
    [nome-da-fase-anterior] — [lista de artefatos que devem estar approved]
```

Usar a seguinte referência de dependências:

| Fase | Depende de (fase anterior completed) | Artefatos-chave que alimentam |
|------|--------------------------------------|-------------------------------|
| discovery | *(nenhuma — ponto de partida)* | — |
| product | discovery | problem-statement, landscape-analysis |
| design | product | prd, user-story-map, mvp-definition |
| architecture | design | user-flows, wireframes, design-system, design-tokens |
| specs | architecture | architecture-overview, data-model, ADRs |
| implementation | specs | feature-specs (todas) |
| quality | implementation | code-standards, implementation-plan |
| deploy | quality | test-strategy, qa-checklist, security-baseline |

Se a fase solicitada é `discovery`, informar: "Esta é a fase inicial do pipeline — sem dependências."

#### 4.5 Frameworks e Metodologias

Mostrar os frameworks/metodologias utilizados na fase:

```
Frameworks e Metodologias:

  - [Nome do Framework] — [como é usado nesta fase]
```

Usar a seguinte referência:

| Fase | Frameworks/Metodologias |
|------|------------------------|
| discovery | Problem Statement Canvas (IDEO), Jobs To Be Done (Christensen), Double Diamond (Design Council) |
| product | User Story Mapping (Jeff Patton), MoSCoW Prioritization (Dai Clegg), Shape Up — Appetite + Pitch (Ryan Singer) |
| design | Atomic Design (Brad Frost), WCAG 2.1 (W3C), W3C Design Tokens |
| architecture | C4 Model (Simon Brown), ADR (Michael Nygard), Clean Architecture (Robert C. Martin) |
| specs | Google Design Docs (Google Engineering) |
| implementation | Conventional Commits (conventionalcommits.org) |
| quality | Pirâmide de Testes (Mike Cohn), Testing Trophy (Kent C. Dodds), OWASP Top 10, WCAG 2.1 |
| deploy | Semantic Versioning (semver.org), Keep a Changelog (keepachangelog.com) |

Para descrições detalhadas de cada framework, referenciar `references/frameworks-glossary.md`.

### 5. Sugerir próximo passo

Com base no status da fase solicitada e na `current_phase` do projeto:

| Situação | Sugestão |
|----------|----------|
| Fase solicitada é futura | "Esta fase ainda não foi iniciada. A fase atual é [current_phase]." |
| Fase solicitada é a atual, com `pending` | "Execute `/forge:next` para gerar o próximo artefato." |
| Fase solicitada é a atual, todos `draft` | "Execute `/forge:review` para revisar e aprovar os artefatos." |
| Fase solicitada é a atual, todos `approved` | "Fase pronta! Execute `/forge:advance` para avançar." |
| Fase solicitada é a atual, mix | "Execute `/forge:next` ou `/forge:review` conforme os artefatos pendentes." |
| Fase solicitada está completed | "Esta fase já foi concluída. Use `/forge:status` para ver o progresso geral." |
