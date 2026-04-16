# Tech Spec — <NOME_DA_FEATURE>

> **Fase:** Specs
> **Skill:** tech-spec-writer
> **Status:** draft
> **Data:** <YYYY-MM-DD>

---

## 1. Referência

<!-- Vincular esta spec aos artefatos de Product que a originam. -->

| Campo | Valor |
|-------|-------|
| Épico | <NOME_EPICO> |
| User Stories | <US-001, US-002, ...> |
| Prioridade | Must Have |
| Fluxo(s) relacionado(s) | <FLOW-001, FLOW-002, ...> |

---

## 2. Descrição

<!-- 1-2 parágrafos: o que a feature faz, do ponto de vista funcional. Contexto suficiente para um desenvolvedor entender o propósito sem ler o PRD inteiro. -->

<DESCRICAO_FUNCIONAL>

---

## 3. Endpoints

<!-- Um bloco por endpoint. Se a feature não expõe endpoints (ex: background job), documentar triggers em vez de rotas. -->

### 3.1 <VERBO> `<ROTA>`

| Campo | Valor |
|-------|-------|
| Método | `<GET / POST / PUT / PATCH / DELETE>` |
| Rota | `<ROTA_COMPLETA>` |
| Autenticação | <pública / autenticada / role: admin, manager, ...> |

**Request:**

<!-- Para GET: documentar query params. Para POST/PUT/PATCH: documentar body. -->

```json
{
  "<CAMPO_1>": "<TIPO — string / number / boolean / object / array>",
  "<CAMPO_2>": "<TIPO>  // obrigatório / opcional"
}
```

**Response — `<STATUS_CODE_SUCESSO>`:**

```json
{
  "<CAMPO_1>": "<TIPO>",
  "<CAMPO_2>": "<TIPO>"
}
```

<!-- Adicionar mais endpoints conforme necessário (3.2, 3.3, ...). -->

---

## 4. Modelo de Dados

<!-- Quais entidades do data-model.md são lidas/escritas por esta feature. Usar os mesmos nomes do data model. -->

| Entidade | Operação | Campos Utilizados |
|----------|----------|-------------------|
| `<ENTIDADE_1>` | <READ / CREATE / UPDATE / DELETE> | `<campo_1>`, `<campo_2>`, ... |
| `<ENTIDADE_2>` | <READ / CREATE / UPDATE / DELETE> | `<campo_1>`, `<campo_2>`, ... |

<!-- Referência: [Data Model](../../03-architecture/data-model.md) -->

---

## 5. Regras de Negócio

<!-- Lógica de domínio que vai além de validação de campo. Cada regra com ID para rastreabilidade. -->

| ID | Regra | Detalhe |
|----|-------|---------|
| RN-01 | <NOME_DA_REGRA> | <DESCRICAO_DETALHADA> |
| RN-02 | <NOME_DA_REGRA> | <DESCRICAO_DETALHADA> |

<!-- Adicionar linhas conforme necessário. -->

---

## 6. Validações

<!-- Validações de campo (input do usuário ou payload de API). -->

| Campo | Regra | Mensagem de Erro |
|-------|-------|------------------|
| `<CAMPO_1>` | <obrigatório / min X / max Y / formato email / regex / enum [a, b, c]> | `"<MENSAGEM_ESPECIFICA>"` |
| `<CAMPO_2>` | <obrigatório / min X / max Y / ...> | `"<MENSAGEM_ESPECIFICA>"` |

<!-- Adicionar linhas conforme necessário. -->

---

## 7. Tratamento de Erros

<!-- Erros esperados e como a API deve responder. -->

| Condição | HTTP Status | Código de Erro | Response |
|----------|-------------|---------------|----------|
| <CONDICAO_1: ex. recurso não encontrado> | `<404>` | `<RESOURCE_NOT_FOUND>` | `{ "error": "<MENSAGEM>" }` |
| <CONDICAO_2: ex. validação falhou> | `<422>` | `<VALIDATION_ERROR>` | `{ "error": "<MENSAGEM>", "fields": [...] }` |
| <CONDICAO_3: ex. não autorizado> | `<401>` | `<UNAUTHORIZED>` | `{ "error": "<MENSAGEM>" }` |
| <CONDICAO_4: ex. sem permissão> | `<403>` | `<FORBIDDEN>` | `{ "error": "<MENSAGEM>" }` |

<!-- Adicionar linhas conforme necessário. -->

---

## 8. Dependências

<!-- Features, serviços ou configurações que esta feature requer para funcionar. -->

### Dependências Internas

<!-- Outras features deste projeto que devem estar implementadas antes. -->

| Feature | Motivo |
|---------|--------|
| <FEATURE_1> | <MOTIVO: ex. autenticação necessária para endpoints protegidos> |

### Dependências Externas

<!-- Serviços de terceiros, APIs externas, ou configurações de infra. -->

| Serviço / Recurso | Motivo | Configuração |
|-------------------|--------|-------------|
| <SERVICO_1> | <MOTIVO> | <ENV_VAR ou config necessária> |

<!-- Se não há dependências externas: "Nenhuma dependência externa." -->

---

## 9. Critérios de Aceite Técnicos

<!-- Checklist verificável. Cada item deve ser objetivo e mensurável. -->

- [ ] <CRITERIO_1: ex. "Endpoint GET /api/v1/users responde em < 200ms para 1000 registros">
- [ ] <CRITERIO_2: ex. "Autenticação JWT validada em todos os endpoints protegidos">
- [ ] <CRITERIO_3: ex. "Dados sensíveis (password) nunca retornados na response">
- [ ] <CRITERIO_4: ex. "Paginação implementada para listagens com > 50 itens">
- [ ] <CRITERIO_5: ex. "Testes unitários cobrem todas as regras de negócio (RN-01 a RN-XX)">

<!-- Adicionar linhas conforme necessário. -->

---

## 10. Notas de Implementação

<!-- Hints, gotchas, decisões de design, referências a ADRs. -->

- <NOTA_1: ex. "Usar bcrypt com cost factor 12 para hashing de passwords — ver ADR-003">
- <NOTA_2: ex. "Rate limiting de 100 req/min por IP nos endpoints públicos">
- <NOTA_3: ex. "Soft-delete para entidade User (campo deleted_at) — ver data model">

---

## Referências

- [PRD](../../01-product/prd.md) — user stories e regras de negócio
- [Data Model](../../03-architecture/data-model.md) — entidades e relacionamentos
- [Architecture Overview](../../03-architecture/architecture-overview.md) — stack e padrões
- [ADRs](../../03-architecture/adrs/) — decisões arquiteturais

---

## Status

- **Criado em:** <YYYY-MM-DD>
- **Última atualização:** <YYYY-MM-DD>
- **Status:** draft
- **Aprovado por:** —
- **Data de aprovação:** —
