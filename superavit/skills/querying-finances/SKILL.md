---
name: querying-finances
description: >-
  Consultas conversacionais sobre finanças pessoais. Interpreta linguagem
  natural e traduz para queries SQL via Supabase MCP. Resumo mensal,
  gastos por categoria, comparativos, orçamento vs realizado.

  <example>
  Context: Pergunta sobre gastos
  user: "quanto gastei com alimentação esse mês?"
  assistant: Busca via RPC, formata tabela com valor e % da renda
  </example>

  <example>
  Context: Orçamento
  user: "como estou no orçamento?"
  assistant: Busca via get_budget_vs_actual, mostra barras de progresso por categoria
  </example>
user-invocable: true
allowed-tools: mcp__claude_ai_Supabase__execute_sql
---

# Querying Finances — Superavit

Consultas conversacionais sobre finanças pessoais. Interpreta linguagem natural, traduz para SQL via Supabase MCP e formata a resposta em pt-BR.

## Pré-requisitos

- Setup concluído (`config.setup_completed = true`)
- Transações importadas (pelo menos 1 import_batch)

Verificar rapidamente:
```sql
SELECT
    (SELECT value->>'completed' FROM config WHERE key = 'setup_completed') AS setup_ok,
    (SELECT COUNT(*) FROM transactions) AS txn_count;
```

Se `setup_ok` não é `true`: orientar `/superavit:setting-up`.
Se `txn_count = 0`: orientar `/superavit:importing-statements`.

## Mapa de Intenções

| O usuário diz... | RPC / Query |
|-------------------|-------------|
| "como estou?", "resumo", "visão geral" | `get_monthly_summary(year, month)` |
| "gastos por categoria", "ranking", "onde gasto mais" | `get_category_ranking(year, month)` |
| "tendência", "últimos meses", "evolução" | `get_monthly_trend(months_back)` |
| "saúde financeira", "score", "nota" | `get_health_score(year, month)` |
| "quanto gastei com X?" | Query filtrada por categoria |
| "compara mês A e mês B" | Dois `get_monthly_summary` + diff |
| "como estou no orçamento?", "budget" | `get_budget_vs_actual(year, month)` |
| "últimas transações", "extrato" | Query em `transactions` com LIMIT |

## Resolução de Período

Quando o usuário menciona um período, resolver para `year` e `month`:

| Expressão | Resolução |
|-----------|-----------|
| "esse mês", "mês atual" | `EXTRACT(YEAR FROM CURRENT_DATE)`, `EXTRACT(MONTH FROM CURRENT_DATE)` |
| "mês passado" | Mês anterior ao atual |
| "janeiro", "fevereiro", ... | Mês nomeado do ano corrente (se futuro, assume ano anterior) |
| "janeiro 2025" | Mês e ano explícitos |
| "últimos 3 meses" | `get_monthly_trend(3)` |
| "últimos 6 meses" | `get_monthly_trend(6)` |
| "esse ano" | Iterar `get_monthly_summary` para cada mês do ano |

Se o período é ambíguo: **perguntar ao usuário** antes de assumir.

## Queries SQL

### Resumo mensal

```sql
SELECT * FROM get_monthly_summary(<year>, <month>);
```

Retorna: `total_income`, `total_expense`, `balance`, `transaction_count`, `categorized_count`.

### Ranking de categorias

```sql
SELECT * FROM get_category_ranking(<year>, <month>);
```

Retorna: `category_name`, `total_amount`, `transaction_count`, `pct_of_income`.

### Tendência mensal

```sql
SELECT * FROM get_monthly_trend(<months_back>);
```

Retorna por mês: `year`, `month`, `total_income`, `total_expense`, `balance`.

### Health score

```sql
SELECT * FROM get_health_score(<year>, <month>);
```

Retorna: `score` (0–100), `savings_rate`, `top_category`, `top_category_pct`.

### Orçamento vs realizado

```sql
SELECT * FROM get_budget_vs_actual(<year>, <month>);
```

Retorna por categoria: `category_name`, `budget_limit`, `actual_spent`, `pct_used`, `remaining`.

### Gasto por categoria específica

```sql
SELECT
    c.name AS categoria,
    ABS(SUM(t.amount)) AS total,
    COUNT(*) AS transacoes
FROM transactions t
JOIN categories c ON t.category_id = c.id
WHERE c.name ILIKE '%<categoria>%'
  AND EXTRACT(YEAR FROM t.date) = <year>
  AND EXTRACT(MONTH FROM t.date) = <month>
  AND t.type = 'expense'
  AND NOT t.is_internal_transfer
  AND NOT t.is_credit_card_payment
GROUP BY c.name;
```

### Comparativo entre meses

Executar `get_monthly_summary` para cada mês e calcular diff:

```sql
SELECT * FROM get_monthly_summary(<year_a>, <month_a>);
SELECT * FROM get_monthly_summary(<year_b>, <month_b>);
```

Calcular: `delta_income = B.income - A.income`, `delta_expense = B.expense - A.expense`, etc.

### Últimas transações

```sql
SELECT
    t.date, t.description, t.amount, t.type,
    c.name AS categoria
FROM transactions t
LEFT JOIN categories c ON t.category_id = c.id
WHERE NOT t.is_internal_transfer
  AND NOT t.is_credit_card_payment
ORDER BY t.date DESC, t.created_at DESC
LIMIT <n>;
```

## Formatação de Resposta

### Valores monetários

Sempre formatar como `R$ X.XXX,XX`:
- `1234.56` → `R$ 1.234,56`
- `-1234.56` → `- R$ 1.234,56`
- `0` → `R$ 0,00`

### Percentuais

Formatar com vírgula decimal: `XX,X%`
- `23.5` → `23,5%`
- `100.0` → `100,0%`

### Deltas (comparativos)

| Condição | Indicador |
|----------|-----------|
| Valor subiu (positivo) | `+XX,X%` |
| Valor caiu (negativo) | `-XX,X%` |
| Sem variação | `0,0%` |

### Health Score

Formatar como barra visual:

| Faixa | Emoji | Barra |
|-------|-------|-------|
| 80–100 | Excelente | `[=========-] 85` |
| 60–79 | Bom | `[======----] 65` |
| 40–59 | Atenção | `[====------] 45` |
| 20–39 | Alerta | `[==--------] 25` |
| 0–19 | Crítico | `[=---------] 10` |

### Orçamento por categoria

Formatar como tabela com barra de progresso:

```
| Categoria          | Limite      | Gasto       | Uso   | Restante    |
|--------------------|-------------|-------------|-------|-------------|
| Alimentacao        | R$ 1.500,00 | R$ 1.200,00 | 80,0% | R$ 300,00   |
| Transporte         | R$ 500,00   | R$ 620,00   | 124,0%| - R$ 120,00 |
```

Categorias acima de 100%: destacar que estourou o orçamento.

### Tabelas gerais

- Headers em português
- Alinhar valores numéricos à direita
- Ordenar por valor absoluto (maior primeiro) quando ranking

## Anti-Patterns

- Nunca inventar dados — se a query retorna vazio, informar que não há dados para o período
- Nunca incluir transferências internas (`is_internal_transfer = true`) nos totais de receita/despesa
- Nunca incluir pagamentos de cartão (`is_credit_card_payment = true`) nos totais — é dupla contagem
- Nunca assumir mês sem confirmar quando a expressão é ambígua
- Nunca mostrar UUIDs ao usuário — usar nomes de categorias e contas
- Nunca formatar valores com ponto decimal (padrão americano) — sempre vírgula (pt-BR)
