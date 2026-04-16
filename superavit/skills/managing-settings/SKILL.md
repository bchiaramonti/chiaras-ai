---
name: managing-settings
description: >-
  Gerencia configurações do Superavit: categorias (listar, adicionar,
  renomear, desativar, editar keywords), contas bancárias, renda mensal,
  modo de voz, e exportação de dados em CSV/JSON.

  <example>
  Context: Ver categorias
  user: "superavit categorias"
  assistant: Lista categorias ativas com keywords de cada uma
  </example>

  <example>
  Context: Exportar dados
  user: "exportar meus dados"
  assistant: Exporta transações em CSV para brain/2-areas/financas/exports/
  </example>

  <example>
  Context: Atualizar renda
  user: "minha renda mudou pra 15 mil"
  assistant: Atualiza config, mostra impacto nos percentuais
  </example>
user-invocable: true
allowed-tools: mcp__claude_ai_Supabase__execute_sql, Bash, Write
---

# Managing Settings — Superavit

CRUD de categorias, contas bancárias, configurações gerais e exportação de dados.

## Operações de Categorias

### Listar categorias

```sql
SELECT name, keywords, is_active, is_default
FROM categories
ORDER BY is_default DESC, name;
```

Formatar como tabela:
```
| Categoria          | Keywords                              | Default | Ativa |
|:-------------------|:--------------------------------------|:-------:|:-----:|
| Alimentacao/Deliv. | ifood, rappi, uber eats, restaurante… | Sim     | Sim   |
| Transporte         | uber, 99, combustivel, gasolina…      | Sim     | Sim   |
| Viagens            | hotel, airbnb, passagem…              | Não     | Sim   |
```

Truncar keywords longas com `…` e mostrar as 4 primeiras.

### Adicionar categoria

Perguntar: nome e keywords (lista separada por vírgula).

```sql
INSERT INTO categories (name, keywords)
VALUES ('<nome>', '<keywords_json>')
ON CONFLICT (name) DO NOTHING;
```

Exemplo de keywords JSON: `'["hotel", "airbnb", "passagem", "booking"]'`

### Renomear categoria

```sql
UPDATE categories
SET name = '<novo_nome>', updated_at = now()
WHERE name ILIKE '%<nome_atual>%';
```

Confirmar com o usuário se o match ILIKE retornar múltiplos resultados.

### Desativar categoria

```sql
UPDATE categories
SET is_active = false, updated_at = now()
WHERE name ILIKE '%<nome>%';
```

> Nunca deletar categorias — transações históricas ficam com `category_id` orphan. Desativar apenas impede novas categorizações.

### Reativar categoria

```sql
UPDATE categories
SET is_active = true, updated_at = now()
WHERE name ILIKE '%<nome>%';
```

### Adicionar keywords a categoria existente

```sql
UPDATE categories
SET keywords = keywords || '<new_keywords_json>'::jsonb, updated_at = now()
WHERE name ILIKE '%<nome>%';
```

> Se a categoria é default (`is_default = true`): confirmar com o usuário antes de alterar keywords.

### Remover keyword de categoria

```sql
UPDATE categories
SET keywords = keywords - '<keyword_to_remove>', updated_at = now()
WHERE name ILIKE '%<nome>%';
```

## Operações de Contas

### Listar contas

```sql
SELECT name, bank, type, is_active,
    (SELECT COUNT(*) FROM transactions WHERE account_id = accounts.id) AS txn_count
FROM accounts
ORDER BY is_active DESC, bank, name;
```

### Adicionar conta

Perguntar:
1. Nome (ex: "Nubank Conta Corrente")
2. Banco (ex: "nubank")
3. Tipo: `checking`, `savings`, ou `credit_card`

```sql
INSERT INTO accounts (name, bank, type)
VALUES ('<nome>', '<banco>', '<tipo>');
```

### Desativar conta

```sql
UPDATE accounts
SET is_active = false, updated_at = now()
WHERE id = '<account_id>';
```

> Nunca deletar conta que tem transações — a FK com `ON DELETE RESTRICT` impede. Desativar apenas.

Verificar antes:
```sql
SELECT COUNT(*) FROM transactions WHERE account_id = '<account_id>';
```

## Config Geral

### Ver configurações

```sql
SELECT key, value FROM config ORDER BY key;
```

Formatar como tabela legível (sem UUIDs):
```
| Configuração    | Valor                |
|:----------------|:---------------------|
| monthly_income  | R$ 10.000,00         |
| voice_mode      | neutral              |
| setup_completed | true                 |
| schema_version  | 001                  |
```

### Atualizar renda mensal

```sql
UPDATE config
SET value = '{"monthly_income": <valor>}', updated_at = now()
WHERE key = 'monthly_income';
```

Após atualizar, mostrar impacto nos percentuais:
```sql
SELECT * FROM get_category_ranking(
    EXTRACT(YEAR FROM CURRENT_DATE)::int,
    EXTRACT(MONTH FROM CURRENT_DATE)::int
);
```

Mostrar: "Com a nova renda de R$ 15.000, Alimentação agora representa 12,3% (antes era 18,5%)."

### Trocar modo de voz

```sql
INSERT INTO config (key, value)
VALUES ('voice_mode', '{"voice_mode": "<modo>"}')
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = now();
```

Modos válidos: `neutral`, `roast`, `alert`.

## Exportação de Dados

### Exportar CSV

Query com JOINs para dados completos:

```sql
SELECT
    t.date, t.description, t.original_description, t.amount, t.type,
    c.name AS category, a.name AS account, a.bank,
    t.is_internal_transfer, t.is_credit_card_payment,
    t.created_at
FROM transactions t
LEFT JOIN categories c ON t.category_id = c.id
LEFT JOIN accounts a ON t.account_id = a.id
ORDER BY t.date DESC, t.created_at DESC;
```

Gerar CSV e salvar:

```bash
mkdir -p ~/Documents/brain/2-areas/financas/exports
```

Salvar com Write tool em:
```
~/Documents/brain/2-areas/financas/exports/transactions-YYYY-MM-DD.csv
```

Formato CSV: header na primeira linha, valores separados por vírgula, encoding UTF-8.

### Exportar JSON

Mesma query, formato JSON array. Salvar como:
```
~/Documents/brain/2-areas/financas/exports/transactions-YYYY-MM-DD.json
```

### Exportar período específico

Se o usuário pedir "exportar janeiro": adicionar filtro de período na query:
```sql
WHERE EXTRACT(YEAR FROM t.date) = <year> AND EXTRACT(MONTH FROM t.date) = <month>
```

## Anti-Patterns

- Nunca deletar categorias default (`is_default = true`) — apenas desativar
- Nunca deletar contas que têm transações — FK com RESTRICT impede
- Nunca alterar keywords de categorias default sem confirmação do usuário
- Nunca usar paths absolutos para export — sempre `~/Documents/brain/...`
- Nunca mostrar UUIDs ao usuário — usar nomes legíveis
