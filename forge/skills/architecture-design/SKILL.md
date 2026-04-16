---
name: architecture-design
description: >-
  Designs software architecture using C4 Model at 3 levels (Context, Containers,
  Components) with Mermaid diagrams. Defines tech stack, communication patterns,
  and data strategy. Use after Design phase is complete. Triggers adr-writer for
  significant decisions. Produces 03-architecture/architecture-overview.md and
  C4 diagrams (c4-context.mermaid, c4-containers.mermaid, c4-components.mermaid).
user-invocable: false
---

# Architecture Design

Projeta a arquitetura de software em 3 níveis do C4 Model com diagramas Mermaid, define stack tecnológica com justificativas, padrões de comunicação e estratégia de dados. Lê todos os artefatos anteriores (Discovery, Product, Design) para tomar decisões informadas e invoca a skill `adr-writer` para documentar cada decisão arquitetural relevante.

## Pré-requisitos

- `01-product/prd.md` com status `approved`
- `02-design/user-flows.md` com status `approved`
- `02-design/wireframes/` com pelo menos 1 wireframe com status `approved`
- `02-design/design-system.md` com status `approved`
- `02-design/design-tokens.json` com status `approved`

## Processo

1. **Ler TODOS os artefatos anteriores:**
   - `00-discovery/problem-statement.md` — extrair: problema, público-alvo, hipótese de solução, critérios de sucesso
   - `00-discovery/landscape-analysis.md` — extrair: concorrentes, gaps, posicionamento
   - `01-product/prd.md` — extrair: personas, épicos, user stories (Must + Should), KPIs, restrições, premissas
   - `01-product/mvp-definition.md` — extrair: escopo MVP, appetite, riscos, limites
   - `01-product/shaped-pitch.md` — extrair: solução moldada, fat-marker sketches, rabbit holes, no-gos
   - `01-product/user-story-map.md` — extrair: backbone, atividades, linha de corte
   - `02-design/user-flows.md` — extrair: fluxos, telas, transições, estados especiais
   - `02-design/wireframes/*.md` — extrair: componentes, ações do usuário, hierarquia de informação
   - `02-design/design-system.md` — extrair: componentes base, tokens visuais
   - `02-design/design-tokens.json` — extrair: tokens programáticos para referência técnica
   - Sintetizar: quais são as exigências técnicas implícitas em todos esses artefatos?

2. **C4 Level 1 — System Context:**
   - Identificar o sistema principal (nome, propósito em 1 frase)
   - Mapear atores/personas que interagem com o sistema (extraídos do PRD)
   - Mapear sistemas externos: APIs de terceiros, serviços de autenticação, gateways de pagamento, serviços de email, analytics, etc.
   - Definir os limites do sistema (o que está dentro vs fora do escopo)
   - Gerar diagrama Mermaid em `03-architecture/c4-context.mermaid`
   - Consultar `references/c4-model-guide.md` para convenções de diagramação

3. **C4 Level 2 — Containers:**
   - Decompor o sistema em containers (unidades deployáveis):
     - Frontend (SPA, SSR, mobile app, CLI)
     - Backend (API server, workers, microservices)
     - Banco de dados (SQL, NoSQL, cache)
     - Serviços auxiliares (queue, storage, CDN)
   - Para cada container: nome, tecnologia, responsabilidade (1 frase)
   - Definir as comunicações entre containers: protocolo (HTTP, gRPC, WebSocket), formato (JSON, protobuf), autenticação
   - Gerar diagrama Mermaid em `03-architecture/c4-containers.mermaid`

4. **C4 Level 3 — Components:**
   - Para cada container principal (especialmente backend), decompor em componentes/módulos:
     - Controllers / Handlers (entry points)
     - Services (business logic)
     - Repositories / DAOs (data access)
     - Middleware (auth, logging, error handling)
     - Utils / Helpers (transversal)
   - Mapear dependências entre componentes (quem chama quem)
   - Alinhar com padrões de Clean Architecture quando aplicável: dependências apontam para dentro (Entities ← Use Cases ← Adapters ← Frameworks)
   - Gerar diagrama Mermaid em `03-architecture/c4-components.mermaid`

5. **Definir stack tecnológica com justificativa:**
   - Linguagem(ns) e runtime
   - Framework web (frontend e backend)
   - Banco de dados (primário e cache)
   - Ferramentas de build, bundler, package manager
   - Para cada escolha: justificativa técnica vinculada ao contexto do projeto (personas, escala, complexidade, constraints do PRD)
   - Considerar: maturidade do ecossistema, curva de aprendizado da equipe, performance, custo operacional

6. **Definir padrões de comunicação:**
   - API style: REST, GraphQL, gRPC, ou híbrido — com justificativa
   - Comunicação em tempo real: WebSocket, SSE, polling — se necessário (verificar user flows)
   - Comunicação assíncrona: filas (Redis, RabbitMQ, SQS) — se necessário
   - Formato de dados: JSON, protobuf, MessagePack
   - Versionamento de API: URL path, header, query param
   - Autenticação/autorização: JWT, OAuth2, session-based — com justificativa

7. **Definir estratégia de dados:**
   - Tipo de banco: SQL (PostgreSQL, MySQL) vs NoSQL (MongoDB, DynamoDB) — com justificativa
   - ORM/ODM: qual usar e por quê
   - Caching: estratégia (cache-aside, write-through), ferramenta (Redis, Memcached), TTL policy
   - Migrations: ferramenta e estratégia de versionamento do schema
   - Backup e recovery: frequência, retenção, recovery time objective (RTO)
   - Se multi-tenant: estratégia de isolamento (schema, row-level, database)

8. **Para cada decisão relevante — invocar skill `adr-writer`:**
   - Identificar decisões arquiteturais que têm alternativas razoáveis (não são "óbvias")
   - Mínimo esperado de ADRs:
     - Escolha de stack tecnológica
     - Escolha de banco de dados
     - Padrão de comunicação (API style)
     - Estratégia de autenticação
   - Para cada decisão, invocar `adr-writer` passando: contexto, decisão, alternativas consideradas
   - ADRs são salvos em `03-architecture/adrs/NNN-titulo.md` (numeração sequencial)

9. **Gerar artefatos:**
   - `03-architecture/architecture-overview.md` — documento narrativo com:
     - Visão geral da arquitetura (1 parágrafo)
     - Diagrama de contexto (referência ao .mermaid)
     - Stack tecnológica (tabela: camada / tecnologia / justificativa)
     - Containers e responsabilidades (tabela)
     - Padrões de comunicação (tabela: de / para / protocolo / formato)
     - Estratégia de dados (seções: banco, caching, migrations)
     - Componentes por container (tabela ou sub-seções)
     - Referências cruzadas: links para ADRs, PRD, wireframes
     - Lista de ADRs gerados com links
   - `03-architecture/c4-context.mermaid` — diagrama Level 1
   - `03-architecture/c4-containers.mermaid` — diagrama Level 2
   - `03-architecture/c4-components.mermaid` — diagrama Level 3

10. **Atualizar `.status`:**
    - Artifact `architecture-overview` → `draft`
    - Artifact `c4-context` → `draft`
    - Artifact `c4-containers` → `draft`
    - Artifact `c4-components` → `draft`

## Artefatos Gerados

- `03-architecture/architecture-overview.md`
- `03-architecture/c4-context.mermaid`
- `03-architecture/c4-containers.mermaid`
- `03-architecture/c4-components.mermaid`

> Para guia prático de C4 com Mermaid, ver [c4-model-guide.md](references/c4-model-guide.md)

## Validação

Antes de marcar como `draft`, verificar:

- [ ] 3 diagramas C4 renderizam sem erros de sintaxe Mermaid
- [ ] Diagrama de contexto inclui todos os atores/personas do PRD
- [ ] Diagrama de containers cobre todas as unidades deployáveis do sistema
- [ ] Diagrama de componentes detalha pelo menos o container principal (backend)
- [ ] Stack tecnológica tem justificativa para cada escolha (não apenas "é popular")
- [ ] Padrões de comunicação definidos para todas as interações entre containers
- [ ] Estratégia de dados inclui: tipo de banco, ORM, caching, migrations
- [ ] Pelo menos 4 ADRs gerados (stack, banco, API style, autenticação)
- [ ] ADRs numerados sequencialmente (001, 002, ...)
- [ ] architecture-overview.md referencia os 3 diagramas .mermaid
- [ ] architecture-overview.md referencia os ADRs gerados com links
- [ ] Nenhuma decisão relevante sem ADR correspondente
- [ ] Terminologia consistente entre overview, diagramas e ADRs
