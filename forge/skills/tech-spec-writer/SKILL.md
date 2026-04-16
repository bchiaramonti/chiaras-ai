---
name: tech-spec-writer
description: >-
  Generates detailed technical specifications for each MVP feature, enabling
  implementation without ambiguity. Use after data model is defined. Each spec
  covers endpoints, data models, business rules, validations, error handling,
  and technical acceptance criteria. Produces one spec file per feature in
  04-specs/features/.
user-invocable: false
---

# Tech Spec Writer

Gera especificações técnicas detalhadas por feature no formato Google Design Docs. Cada spec funciona como contrato entre a fase de planejamento e a implementação — deve conter tudo que um desenvolvedor precisa para implementar a feature sem ambiguidade, referenciando entidades do data model, endpoints da arquitetura e regras de negócio do PRD.

## Pré-requisitos

- `03-architecture/data-model.md` com status `approved`
- `03-architecture/architecture-overview.md` com status `approved`
- `01-product/prd.md` com status `approved`

## Processo

1. **Ler TODOS os artefatos anteriores:**
   - `01-product/prd.md` — extrair: épicos, user stories (Must + Should), MoSCoW, KPIs, restrições, premissas, fora de escopo
   - `01-product/mvp-definition.md` — extrair: escopo MVP, appetite, linha de corte
   - `01-product/user-story-map.md` — extrair: backbone, atividades, priorização
   - `02-design/user-flows.md` — extrair: fluxos por épico, telas, transições, estados especiais
   - `02-design/wireframes/*.md` — extrair: ações do usuário por tela, validações visuais, componentes
   - `03-architecture/architecture-overview.md` — extrair: stack tecnológica, containers, padrões de comunicação, estratégia de dados
   - `03-architecture/data-model.md` — extrair: entidades, atributos, relacionamentos, índices
   - `03-architecture/c4-components.mermaid` — extrair: componentes/módulos internos, dependências
   - `03-architecture/adrs/*.md` — extrair: decisões que impactam implementação (auth, API style, banco)
   - Sintetizar: quais features do MVP precisam de spec, e quais artefatos alimentam cada uma?

2. **Identificar features do MVP que requerem spec:**
   - Filtrar user stories "Must Have" do PRD (coluna MoSCoW)
   - Agrupar user stories por feature/épico funcional
   - Cada feature pode cobrir 1 ou mais user stories relacionadas (não quebrar em specs menores que 1 user story)
   - Nomear cada feature com kebab-case descritivo (ex: `autenticacao-login`, `gestao-usuarios`, `dashboard-principal`)
   - Listar as features a serem especificadas antes de começar a escrita

3. **Para cada feature — detalhar a spec completa:**
   - **Referência:** vincular ao épico, user stories (IDs do PRD), prioridade MoSCoW
   - **Descrição:** o que a feature faz em 1-2 parágrafos (perspectiva funcional)
   - **Endpoints / Rotas:**
     - Método HTTP (GET, POST, PUT, PATCH, DELETE)
     - Rota completa com path params (ex: `/api/v1/users/:id`)
     - Autenticação requerida (pública, autenticada, role específica)
     - Request body (campos, tipos, obrigatórios)
     - Response body (estrutura JSON, status codes)
   - **Modelo de Dados:** quais entidades do `data-model.md` são lidas/escritas, com campos específicos usados
   - **Regras de Negócio:** lógica do domínio que não é validação de campo (ex: "usuário só pode ter 3 projetos ativos", "preço mínimo é R$10")
   - **Validações:** campo, regra, mensagem de erro específica
   - **Tratamento de Erros:** condição de erro, HTTP status code, response payload
   - **Dependências:** outras features, serviços externos, ou configurações necessárias
   - **Critérios de Aceite Técnicos:** checklist verificável (ex: "response time < 200ms para listagem")
   - **Notas de Implementação:** hints, gotchas, referências a ADRs, decisões de design

4. **Gerar 1 arquivo por feature usando template:**
   - Usar `templates/tech-spec.tmpl.md` como base
   - Salvar em `04-specs/features/<nome-da-feature>.md`
   - Cada arquivo deve ser auto-suficiente: compreensível sem ler outras specs
   - Garantir que referências a entidades usam os mesmos nomes do `data-model.md`
   - Garantir que rotas/endpoints são consistentes com o API style definido nos ADRs

5. **Atualizar `.status`:**
   - Artifact `feature-specs` → `draft`

## Artefatos Gerados

- `04-specs/features/<nome-da-feature>.md` — 1 arquivo por feature (via `templates/tech-spec.tmpl.md`)

## Validação

Antes de marcar como `draft`, verificar:

- [ ] Toda user story "Must Have" do PRD tem pelo menos 1 spec correspondente
- [ ] Nenhuma spec criada para user story que não seja "Must Have" do MVP
- [ ] Endpoints incluem: método HTTP, rota completa, e requisito de autenticação
- [ ] Request/response bodies com campos, tipos e exemplos
- [ ] Validações incluem: campo, regra e mensagem de erro específica
- [ ] Tratamento de erros com HTTP status code e response payload definidos
- [ ] Critérios de aceite técnicos são objetivos e verificáveis (mensuráveis, sem "deve ser rápido")
- [ ] Entidades referenciadas existem no `data-model.md` com os mesmos nomes
- [ ] Rotas seguem o padrão de API definido nos ADRs (REST, versionamento, naming)
- [ ] Nomes dos arquivos seguem kebab-case derivado do nome da feature
- [ ] Cada spec é auto-suficiente: links para PRD, data model e ADRs relevantes
- [ ] Dependências entre features estão explícitas (feature X depende de feature Y)
