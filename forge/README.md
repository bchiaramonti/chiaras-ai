# Forge

> Meta-plugin de engenharia de software que transforma ideias em software pronto para produção através de 8 fases sequenciais.

Forge é um plugin para [Claude Code](https://claude.ai/code) que implementa um pipeline completo de desenvolvimento de software — da descoberta do problema até o deploy em produção. Cada fase gera artefatos estruturados que alimentam a próxima, garantindo rastreabilidade e coerência ao longo de todo o ciclo.

## Pipeline

```
Discovery → Product → Design → Architecture → Specs → Implementation → Quality → Deploy
   (00)       (01)     (02)       (03)         (04)       (05)           (06)     (07)
```

| Fase | Objetivo | Artefatos |
|------|----------|-----------|
| **00 — Discovery** | Entender o problema e o mercado | Problem Statement, Landscape Analysis |
| **01 — Product** | Definir o produto e escopo MVP | PRD, User Story Map, Shaped Pitch, MVP Definition |
| **02 — Design** | Projetar fluxos, telas e design system | User Flows, Wireframes, Design System, Design Tokens |
| **03 — Architecture** | Definir arquitetura e modelo de dados | Architecture Overview, C4 Diagrams, ADRs, Data Model |
| **04 — Specs** | Especificações técnicas por feature | Tech Specs (1 por feature MVP) |
| **05 — Implementation** | Padrões de código e orquestração | Code Standards, Plano de Implementação |
| **06 — Quality** | Testes, QA, segurança | Test Strategy, QA Checklist, Security Baseline |
| **07 — Deploy** | Estratégia de deploy e observabilidade | Deploy Strategy, Observability Setup |

## Instalação

O Forge faz parte do marketplace `bchiaramonti-plugins`. Para habilitá-lo em um projeto, adicione ao `settings.json` do Claude Code:

```json
{
  "enabledPlugins": {
    "forge@bchiaramonti-plugins": true
  }
}
```

## Quick Start

```
# 1. Inicializar um novo projeto
/forge:init meu-projeto

# 2. Ver o status atual do pipeline
/forge:status

# 3. Executar a próxima skill pendente
/forge:next

# 4. Revisar os artefatos da fase atual
/forge:review

# 5. Avançar para a próxima fase (requer todos artefatos approved)
/forge:advance
```

## Commands

| Command | Descrição |
|---------|-----------|
| `/forge:init <nome>` | Inicializa um novo projeto Forge com estrutura de diretórios, `.status`, CLAUDE.md e templates base |
| `/forge:status` | Mostra fase atual, artefatos pendentes e progresso geral com barras visuais e timeline |
| `/forge:next` | Executa a próxima skill ou agent pendente para gerar o próximo artefato |
| `/forge:phase <nome>` | Mostra detalhes de uma fase específica: skills, artefatos, dependências, frameworks |
| `/forge:review` | Revisa artefatos da fase atual por completude e coerência intra/inter-fase |
| `/forge:advance` | Marca a fase atual como completa e avança para a próxima (gate: todos artefatos approved) |

## Skills (17)

Todas as skills são invocadas automaticamente pelo pipeline (`user-invocable: false`). Não aparecem no menu `/`.

### Discovery (Fase 00)

| Skill | Artefato |
|-------|----------|
| `problem-framing` | `00-discovery/problem-statement.md` |
| `competitive-landscape` | `00-discovery/landscape-analysis.md` |

### Product (Fase 01)

| Skill | Artefato |
|-------|----------|
| `product-definition` | `01-product/prd.md`, `01-product/user-story-map.md` |

### Design (Fase 02)

| Skill | Artefato |
|-------|----------|
| `user-flow-mapping` | `02-design/user-flows.md`, `02-design/user-flows.mermaid` |
| `wireframe-spec` | `02-design/wireframes/*.md` |
| `design-system-bootstrap` | `02-design/design-system.md`, `02-design/design-tokens.json` |

### Architecture (Fase 03)

| Skill | Artefato |
|-------|----------|
| `architecture-design` | `03-architecture/architecture-overview.md`, diagramas C4 |
| `adr-writer` | `03-architecture/adrs/NNN-titulo.md` |
| `data-model-designer` | `03-architecture/data-model.md`, `03-architecture/data-model.mermaid` |

### Specs (Fase 04)

| Skill | Artefato |
|-------|----------|
| `tech-spec-writer` | `04-specs/features/*.md` (1 por feature) |

### Implementation (Fase 05)

| Skill | Artefato |
|-------|----------|
| `code-standards` | `05-implementation/code-standards.md` + configs |

### Quality (Fase 06)

| Skill | Artefato |
|-------|----------|
| `test-strategy` | `06-quality/test-strategy.md` |
| `qa-checklist` | `06-quality/qa-checklist.md` |
| `security-baseline` | `06-quality/security-baseline.md` |

### Deploy (Fase 07)

| Skill | Artefato |
|-------|----------|
| `deploy-strategy` | `07-deploy/deploy-strategy.md` |
| `observability-setup` | `07-deploy/observability-setup.md` |

### Cross-phase

| Skill | Artefato |
|-------|----------|
| `changelog-manager` | `CHANGELOG.md` (invocado automaticamente por `forge:advance`) |

## Agents (2)

| Agent | Modelo | Quando é invocado |
|-------|--------|-------------------|
| `scope-shaper` | Opus | Após PRD e User Story Map approved — negocia escopo vs. tempo, gera Shaped Pitch e MVP Definition |
| `dev-orchestrator` | Opus | Na fase Implementation — lê todos os artefatos, constrói grafo de dependências e sequencia tarefas |

## Shared References

O plugin inclui 3 documentos de referência compartilhados entre todas as skills:

- **pipeline-overview.md** — Diagrama do pipeline, mapa skill→fase→artefato, template `.status`
- **frameworks-glossary.md** — 17 frameworks de engenharia de software referenciados pelas skills
- **phase-dependency-map.md** — Grafo de dependências entre skills com diagrama Mermaid

## Requisitos

- **Claude Code** — versão mais recente
- **Modelo Opus** — necessário para os agents `scope-shaper` e `dev-orchestrator`
- **Git** — `forge:init` inicializa um repositório git automaticamente

## Licença

[MIT](LICENSE)
