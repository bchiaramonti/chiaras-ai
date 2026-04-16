# Pirâmide de Testes & Testing Trophy — Guia Prático

> Referência para a skill `test-strategy`.
> Baseado em: Mike Cohn — *Succeeding with Agile* (2009) e Kent C. Dodds — *The Testing Trophy* (2018).

---

## Sumário

1. [Pirâmide de Testes (Mike Cohn)](#1-pirâmide-de-testes-mike-cohn)
2. [Testing Trophy (Kent C. Dodds)](#2-testing-trophy-kent-c-dodds)
3. [Quando Usar Cada Modelo](#3-quando-usar-cada-modelo)
4. [Tipos de Teste — Detalhamento](#4-tipos-de-teste--detalhamento)
5. [Métricas de Cobertura](#5-métricas-de-cobertura)
6. [Anti-patterns de Teste](#6-anti-patterns-de-teste)
7. [Decisão Rápida por Stack/Contexto](#7-decisão-rápida-por-stackcontexto)

---

## 1. Pirâmide de Testes (Mike Cohn)

### O Modelo

```
        /\
       /  \        E2E (poucos)
      /----\       Lentos, frágeis, caros
     /      \
    /--------\     Integration (médio)
   /          \    Moderados em velocidade e custo
  /------------\
 /              \  Unit (muitos)
/________________\ Rápidos, baratos, isolados
```

### Princípio

A base larga (unit tests) sustenta o sistema. Quanto mais alto na pirâmide, mais lento, frágil e caro o teste. A pirâmide sugere uma **proporção**: muitos unit tests, número moderado de integration tests, poucos E2E tests.

### Proporção Típica

| Tipo | % do Total | Velocidade | Custo de Manutenção | Confiança |
|------|-----------|-----------|---------------------|-----------|
| Unit | ~70% | Milissegundos | Baixo | Baixa (testa isolado) |
| Integration | ~20% | Segundos | Médio | Média (testa interação) |
| E2E | ~10% | Minutos | Alto | Alta (testa o todo) |

### Quando a Pirâmide Funciona Bem

- Backends com lógica de negócio complexa (muitas regras, cálculos, transformações)
- Sistemas com camadas bem definidas (controller → service → repository)
- Equipes que precisam de feedback rápido no CI
- Projetos onde a maioria do valor está na lógica de domínio

---

## 2. Testing Trophy (Kent C. Dodds)

### O Modelo

```
        ___
       | E2E |       E2E (poucos)
       |_____|
      /       \
     /  Integ. \     Integration (MUITOS) ← foco
    /___________\
   /             \
  /    Unit       \  Unit (alguns)
 /_________________\
|   Static Types   |  TypeScript, ESLint, etc.
|__________________|
```

### Princípio

O trophy inverte a ênfase: **integration tests são o ponto de maior ROI** porque testam como os componentes trabalham juntos, que é onde a maioria dos bugs realmente aparece. A base não é unit tests, mas **análise estática** (TypeScript, linting, formatting).

### Proporção Típica

| Tipo | % do Total | Velocidade | Custo de Manutenção | Confiança |
|------|-----------|-----------|---------------------|-----------|
| Static | (não conta) | Instantâneo | Mínimo | Previne erros triviais |
| Unit | ~20% | Milissegundos | Baixo | Baixa |
| Integration | ~60% | Segundos | Médio | **Alta** |
| E2E | ~20% | Minutos | Alto | Muito alta |

### Quando o Trophy Funciona Bem

- Frontends e aplicações UI-heavy (React, Vue, Angular)
- Backends com pouca lógica própria (CRUD, orchestração de serviços)
- Projetos que já usam TypeScript / análise estática
- Equipes que querem maximizar confiança com menos testes

---

## 3. Quando Usar Cada Modelo

| Critério | Pirâmide | Trophy |
|----------|----------|--------|
| **Lógica de negócio** | Complexa (cálculos, regras, transformações) | Simples (CRUD, orchestração) |
| **Tipo de aplicação** | API/backend, sistemas distribuídos | Frontend, full-stack com UI dominante |
| **Stack** | Python, Go, Java, backends em geral | TypeScript/JavaScript, React, Next.js |
| **Análise estática** | Opcional (pode não ter tipos) | Forte (TypeScript, ESLint rigoroso) |
| **Prioridade** | Feedback rápido no CI | Confiança de que "funciona de verdade" |
| **Custo de E2E** | Alto (evitar) | Tolerável (investir mais) |

### Modelo Híbrido (Recomendação Padrão do Forge)

Na prática, a maioria dos projetos se beneficia de um **híbrido**:

1. **Base:** análise estática (TypeScript, linter, formatter) — prevenir erros triviais
2. **Core:** unit tests em business logic (services, utils, regras de negócio) — feedback rápido
3. **Meio:** integration tests em handlers/controllers + banco — confiança real
4. **Topo:** E2E nos happy paths dos fluxos críticos do MVP — validação end-to-end

---

## 4. Tipos de Teste — Detalhamento

### 4.1 Unit Tests

**O que são:** Testam uma unidade isolada de código (função, método, classe) sem dependências externas.

**O que testar:**
- Funções puras (input → output previsível)
- Regras de negócio em services (ex: cálculo de desconto, validação de elegibilidade)
- Transformações de dados (mappers, serializers, formatters)
- Validações de input (schemas, parsers)
- Edge cases e condições de contorno

**O que NÃO testar:**
- Getters/setters triviais sem lógica
- Código gerado por ORM/framework
- Configurações e constantes
- Implementações de interface (testar via integration)

**Padrão AAA:**
```
Arrange  → Preparar dados de entrada e mocks
Act      → Executar a função/método sob teste
Assert   → Verificar o resultado esperado
```

**Mocking:**
- Mockar dependências externas (banco, APIs, filesystem)
- **Não** mockar a unidade sob teste
- Preferir injeção de dependência para facilitar mocks

### 4.2 Integration Tests

**O que são:** Testam a interação entre 2+ componentes reais (não mockados).

**O que testar:**
- Controller/handler → service → repository → banco real (test database)
- Endpoints HTTP completos (request → middleware → handler → response)
- Comunicação com filas e caches (usando containers de teste)
- Queries SQL/NoSQL complexas (verificar que o ORM gera o SQL correto)
- Autenticação/autorização end-to-end (JWT validation, RBAC)

**O que NÃO testar:**
- Lógica que já está coberta por unit tests (não duplicar)
- Serviços externos reais (usar mocks ou containers)
- UI/browser (isso é E2E)

**Setup/Teardown:**
- Test database separado (nunca usar banco de produção ou desenvolvimento)
- Migrations automáticas antes do test suite
- Cada teste isola seus dados (transação com rollback ou truncate)
- Fixtures para dados comuns (users, configs)

### 4.3 End-to-End Tests (E2E)

**O que são:** Testam o sistema completo da perspectiva do usuário.

**O que testar:**
- Happy paths dos fluxos críticos do MVP (derivados de `user-flows.md`)
- Fluxo de registro/login completo
- Fluxo principal de cada épico Must Have
- Cenários de pagamento/transação (se aplicável)

**O que NÃO testar:**
- Todos os edge cases (custoso demais — cobrir com unit/integration)
- Variações visuais (usar snapshot/visual regression testing separado)
- Performance (usar ferramentas de load testing separadas)

**Boas Práticas:**
- Selectors resilientes: `data-testid` (não classes CSS ou xpaths frágeis)
- Aguardar estados (never `sleep`, always wait for condition)
- Dados de teste independentes (cada E2E cria seus próprios dados)
- Screenshots/vídeos automáticos em falhas (debugging)

### 4.4 Análise Estática

**O que é:** Detecção de erros em tempo de desenvolvimento, sem executar código.

| Ferramenta | O que detecta |
|-----------|--------------|
| TypeScript | Erros de tipo, null safety, interfaces incompatíveis |
| ESLint / Ruff | Padrões problemáticos, imports incorretos, código morto |
| Prettier / Ruff format | Inconsistências de formatação |
| Husky + lint-staged | Validação automática no pre-commit |

---

## 5. Métricas de Cobertura

### Tipos de Cobertura

| Métrica | O que mede | Target Recomendado |
|---------|-----------|-------------------|
| **Line coverage** | % de linhas executadas | ≥ 70% global |
| **Branch coverage** | % de caminhos lógicos (if/else, switch) | ≥ 60% |
| **Function coverage** | % de funções chamadas | ≥ 80% |
| **Statement coverage** | % de statements executados | ≥ 70% |

### Targets por Camada

| Camada | Line Coverage | Justificativa |
|--------|-------------|---------------|
| Services / Business Logic | ≥ 80% | Onde estão as regras de negócio — maior risco |
| Controllers / Handlers | ≥ 60% | Cobertura via integration tests |
| Repositories / DAOs | ≥ 50% | Grande parte é código ORM/query builder |
| Utils / Helpers | ≥ 90% | Funções puras — fáceis de testar |
| Config / Constants | Não medir | Sem lógica testável |

### Quando NÃO Perseguir Cobertura

- **100% é quase sempre um desperdício** — os últimos 10-20% custam mais que valem
- Focar cobertura em **business logic**, não em boilerplate
- Cobertura alta com testes triviais (testar `1 + 1 === 2`) dá falsa segurança
- **Mutation testing** é melhor indicador de qualidade dos testes do que line coverage

### Ferramentas de Cobertura

| Stack | Ferramenta | Comando |
|-------|-----------|---------|
| TypeScript/JS (Vitest) | v8 ou istanbul (built-in) | `vitest run --coverage` |
| TypeScript/JS (Jest) | istanbul (built-in) | `jest --coverage` |
| Python | coverage.py + pytest-cov | `pytest --cov=src --cov-report=html` |
| Go | go tool cover (built-in) | `go test -coverprofile=cover.out ./...` |

---

## 6. Anti-patterns de Teste

### Testes Frágeis

| Anti-pattern | Problema | Solução |
|-------------|----------|---------|
| Testar implementação (não comportamento) | Quebra ao refatorar sem mudar comportamento | Testar input → output, não como funciona internamente |
| Mocks excessivos | Teste não verifica nada real | Mockar apenas I/O externo (banco, API, filesystem) |
| Fixtures globais compartilhadas | Um teste afeta outro | Cada teste cria seus próprios dados |
| Assertions genéricas (`toBeTruthy`) | Não identifica o que falhou | Assertions específicas (`toEqual`, `toContain`) |
| `sleep()` em E2E | Flaky tests, CI lento | Wait for condition / polling |
| Testar código de terceiros | Desperdiça tempo, não garante nada | Confiar na biblioteca, testar a integração |

### Inversão da Pirâmide (Ice Cream Cone)

```
  ________________
 /                \  E2E (muitos) ← PROBLEMA
/------------------\
|   Integration    |
|   (poucos)       |
|__________________|
|   Unit (poucos)  |
|__________________|
```

**Resultado:** CI lento, testes flaky, custo de manutenção alto, feedback tardio.
**Solução:** Mover lógica testável para funções puras e testar com unit tests.

---

## 7. Decisão Rápida por Stack/Contexto

### Tabela de Decisão

| Se o projeto é... | Modelo base | Foco principal |
|-------------------|------------|---------------|
| API REST backend com lógica complexa | Pirâmide | Unit tests em services |
| Frontend React/Next.js | Trophy | Integration tests em componentes |
| Full-stack (frontend + API) | Híbrido | Unit (backend logic) + Integration (API handlers + React components) |
| Microservices | Pirâmide + Contract tests | Unit (cada service) + Contract (entre services) |
| Serverless (Lambda/Functions) | Trophy adaptado | Integration tests em handlers (cada function) |
| CLI tool | Pirâmide | Unit tests em commands + Integration em I/O |

### Checklist de Priorização (O Que Testar Primeiro)

Ordenado por ROI (retorno sobre investimento):

1. **Unit tests nas regras de negócio** — maior valor, menor custo
2. **Integration tests nos endpoints/handlers da API** — valida o contrato
3. **E2E no happy path do fluxo principal** — valida que "funciona de ponta a ponta"
4. **Unit tests em validações e transformações** — previne bugs de dados
5. **Integration tests de autenticação/autorização** — previne falhas de segurança
6. **E2E em fluxos secundários** — expandir cobertura gradualmente
7. **Snapshot/visual regression** — apenas se UI é crítica
8. **Performance/load tests** — apenas se escalabilidade é requisito
