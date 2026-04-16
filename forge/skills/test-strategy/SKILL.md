---
name: test-strategy
description: >-
  Defines the testing strategy: what to test at each layer, tools, minimum coverage,
  and test templates. Based on Test Pyramid and Testing Trophy frameworks.
  Use during or after implementation starts. Produces 06-quality/test-strategy.md.
user-invocable: false
---

# Test Strategy

Define estratégia de testes completa por camada, usando a Pirâmide de Testes e o Testing Trophy como referência. Lê a arquitetura para entender as camadas do sistema e as tech specs para saber o que testar. Produz um documento que funciona como contrato de qualidade: qual tipo de teste cobre cada camada, com quais ferramentas, e qual cobertura mínima exigir.

## Pré-requisitos

- `03-architecture/architecture-overview.md` com status `approved` (stack e layers)
- `04-specs/features/` com pelo menos 1 feature spec com status `approved`

## Processo

1. **Ler arquitetura para entender as camadas do sistema:**
   - Extrair de `architecture-overview.md`:
     - Stack tecnológica (linguagem, frameworks, runtime)
     - Containers e componentes (C4 Level 2 e 3)
     - Camadas internas: controllers, services, repositories, middleware, utils
     - Padrões de comunicação: REST, GraphQL, WebSocket, filas
     - Estratégia de dados: banco, ORM, caching
   - Extrair de `03-architecture/adrs/*.md`:
     - Decisões que impactam testabilidade (ex: escolha de ORM, estratégia de auth)
   - Mapear as camadas testáveis do sistema em uma tabela

2. **Definir o que testar em cada camada:**
   - Consultar `references/test-pyramid-guide.md` para framework de decisão
   - Para cada camada identificada no step 1, definir:
     - **Unit tests** — funções puras, regras de negócio, validações, transformações de dados
       - Isolar dependências com mocks/stubs
       - Foco: lógica de domínio nos services e utils
       - Não testar: getters/setters triviais, código gerado, configs
     - **Integration tests** — interação entre componentes reais
       - Foco: service → repository → banco real (test DB), controller → service
       - HTTP handlers com request/response real (supertest, httptest)
       - Comunicação com serviços externos: usar containers (testcontainers) ou mocks
     - **End-to-end tests** — fluxos completos do usuário
       - Foco: happy paths dos user flows críticos (derivados de `02-design/user-flows.md`)
       - Simular interação do usuário (browser, API calls sequenciais)
       - Mínimo: 1 E2E por fluxo crítico do MVP
   - Documentar em tabela: camada | tipo de teste | o que testa | o que não testa

3. **Escolher ferramentas de teste por camada:**
   - Baseado na stack identificada no step 1:
     - **TypeScript/JavaScript:**
       - Unit + Integration: Vitest (preferência) ou Jest
       - E2E (API): Supertest
       - E2E (Browser): Playwright (preferência) ou Cypress
       - Mocking: vi.mock (Vitest) ou jest.mock
     - **Python:**
       - Unit + Integration: pytest
       - E2E (API): httpx + pytest-asyncio
       - E2E (Browser): Playwright for Python
       - Mocking: pytest-mock, unittest.mock
       - Fixtures: pytest fixtures + conftest.py
     - **Go:**
       - Unit + Integration: testing (stdlib) + testify
       - E2E (API): net/http/httptest
       - Mocking: gomock ou mockery
       - DB: testcontainers-go
   - Para TODAS as stacks:
     - Coverage: ferramenta nativa ou Istanbul/coverage.py/go tool cover
     - CI runner: como executar no pipeline (npm test, pytest, go test ./...)
   - Documentar em tabela: tipo de teste | ferramenta | comando de execução

4. **Definir cobertura mínima esperada:**
   - Targets por camada (adaptáveis por projeto):
     - **Unit tests:** ≥ 80% de cobertura em services e business logic
     - **Integration tests:** ≥ 60% de cobertura em handlers/controllers
     - **E2E tests:** cobertura de 100% dos happy paths dos fluxos críticos
   - **Global:** ≥ 70% de cobertura total (linhas)
   - Métricas complementares:
     - Branch coverage (caminhos lógicos) — ≥ 60%
     - Mutation testing score (se aplicável) — ≥ 50%
   - Definir quando bloquear merge por cobertura (CI gate):
     - PR que reduz cobertura global: bloquear
     - Novo código sem testes: warning (não bloquear no MVP, bloquear pós-v1)

5. **Criar templates/exemplos de teste:**
   - Para cada tipo de teste (unit, integration, e2e):
     - Estrutura do arquivo de teste (imports, setup, describe/it blocks)
     - Padrão de naming: `describe('<Module>') → it('should <behavior>')` ou equivalente
     - Padrão Arrange-Act-Assert (AAA) explícito
     - Exemplo de mock/stub para dependências comuns
   - Para testes de API:
     - Template de request + assertion de status code + body
     - Template de autenticação em testes (JWT mock, session mock)
   - Para testes de banco:
     - Template de setup/teardown (criar/limpar dados de teste)
     - Uso de transações para isolamento (rollback após cada teste)
   - Documentar templates diretamente no `test-strategy.md` (seção de exemplos)

6. **Gerar artefato e atualizar `.status`:**
   - `06-quality/test-strategy.md` — documento narrativo com:
     - Resumo da estratégia (1 parágrafo: modelo base, abordagem, ferramentas)
     - Mapa de camadas testáveis (tabela: camada | tipo | foco | exclusões)
     - Ferramentas (tabela: tipo | ferramenta | comando)
     - Cobertura mínima (tabela: camada | target | métrica)
     - Gates de CI (quando bloquear merge)
     - Templates de teste por tipo (exemplos de código)
     - Priorização: quais testes escrever primeiro (ordenado por ROI)
     - Referências cruzadas: links para architecture-overview, tech specs, user flows
   - Atualizar `.status`: artifact `test-strategy` → `draft`

## Artefato Gerado

- `06-quality/test-strategy.md`

## Referências

- Para guia detalhado de Pirâmide de Testes e Testing Trophy, ver [test-pyramid-guide.md](references/test-pyramid-guide.md)

## Validação

Antes de marcar como `draft`, verificar:

- [ ] Todas as camadas da arquitetura estão mapeadas a pelo menos 1 tipo de teste
- [ ] Ferramentas são compatíveis com a stack definida na arquitetura
- [ ] Cobertura mínima definida por camada (não apenas global)
- [ ] Cobertura global ≥ 70% definida como target
- [ ] Templates de teste incluem pelo menos: unit, integration, e2e (API)
- [ ] Templates seguem padrão AAA (Arrange-Act-Assert)
- [ ] Naming de testes segue convenção definida em code-standards
- [ ] Comandos de execução documentados (como rodar cada tipo de teste)
- [ ] Gates de CI definidos (quando bloquear merge por cobertura)
- [ ] E2E cobre os happy paths dos fluxos críticos do MVP
- [ ] Priorização de testes ordenada por ROI (unit em business logic primeiro)
- [ ] Referências cruzadas para architecture-overview e tech specs
