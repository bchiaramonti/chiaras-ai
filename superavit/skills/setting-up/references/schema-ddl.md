# Schema DDL — Superavit

DDL completo do schema PostgreSQL para Supabase. Todo SQL é idempotente.

## Índice

- [1. Tabelas](#1-tabelas)
  - [1.1 accounts](#11-accounts)
  - [1.2 categories](#12-categories)
  - [1.3 config](#13-config)
  - [1.4 import_batches](#14-import_batches)
  - [1.5 transactions](#15-transactions)
  - [1.6 budgets](#16-budgets)
  - [1.7 _migrations](#17-_migrations)
- [2. Índices](#2-índices)
- [3. RPCs](#3-rpcs)
  - [3.1 get_monthly_summary](#31-get_monthly_summary)
  - [3.2 get_category_ranking](#32-get_category_ranking)
  - [3.3 get_monthly_trend](#33-get_monthly_trend)
  - [3.4 get_health_score](#34-get_health_score)
  - [3.5 get_budget_vs_actual](#35-get_budget_vs_actual)
- [4. Seed Data](#4-seed-data)
- [5. Migration Record](#5-migration-record)

---

## 1. Tabelas

### 1.1 accounts

```sql
CREATE TABLE IF NOT EXISTS accounts (
    id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name            varchar(100) NOT NULL,
    bank            varchar(50)  NOT NULL,
    type            varchar(20)  NOT NULL CHECK (type IN ('checking', 'savings', 'credit_card')),
    is_active       boolean      NOT NULL DEFAULT true,
    created_at      timestamptz  NOT NULL DEFAULT now(),
    updated_at      timestamptz  NOT NULL DEFAULT now()
);
```

### 1.2 categories

```sql
CREATE TABLE IF NOT EXISTS categories (
    id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name            varchar(100) NOT NULL UNIQUE,
    keywords        jsonb        NOT NULL DEFAULT '[]',
    is_active       boolean      NOT NULL DEFAULT true,
    is_default      boolean      NOT NULL DEFAULT false,
    created_at      timestamptz  NOT NULL DEFAULT now(),
    updated_at      timestamptz  NOT NULL DEFAULT now()
);
```

### 1.3 config

```sql
CREATE TABLE IF NOT EXISTS config (
    id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    key             varchar(100) NOT NULL UNIQUE,
    value           jsonb        NOT NULL,
    created_at      timestamptz  NOT NULL DEFAULT now(),
    updated_at      timestamptz  NOT NULL DEFAULT now()
);
```

### 1.4 import_batches

```sql
CREATE TABLE IF NOT EXISTS import_batches (
    id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id          uuid         NOT NULL REFERENCES accounts(id) ON DELETE RESTRICT,
    filename            varchar(255) NOT NULL,
    format              varchar(10)  NOT NULL CHECK (format IN ('csv', 'ofx', 'pdf')),
    total_rows          integer      NOT NULL,
    imported_rows       integer      NOT NULL,
    duplicates_skipped  integer      NOT NULL DEFAULT 0,
    date_range_start    date,
    date_range_end      date,
    created_at          timestamptz  NOT NULL DEFAULT now()
);
```

### 1.5 transactions

```sql
CREATE TABLE IF NOT EXISTS transactions (
    id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id              uuid         NOT NULL REFERENCES accounts(id) ON DELETE RESTRICT,
    category_id             uuid         REFERENCES categories(id) ON DELETE SET NULL,
    import_batch_id         uuid         NOT NULL REFERENCES import_batches(id) ON DELETE RESTRICT,
    date                    date         NOT NULL,
    description             text         NOT NULL,
    original_description    text         NOT NULL,
    amount                  numeric(12,2) NOT NULL,
    type                    varchar(20)  NOT NULL CHECK (type IN ('income', 'expense', 'transfer')),
    is_internal_transfer    boolean      NOT NULL DEFAULT false,
    is_credit_card_payment  boolean      NOT NULL DEFAULT false,
    reconciled_with_id      uuid         REFERENCES transactions(id) ON DELETE SET NULL,
    hash                    varchar(64)  NOT NULL UNIQUE,
    source_bank             varchar(50),
    source_format           varchar(10),
    created_at              timestamptz  NOT NULL DEFAULT now(),
    updated_at              timestamptz  NOT NULL DEFAULT now()
);
```

### 1.6 budgets

```sql
CREATE TABLE IF NOT EXISTS budgets (
    id            uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    category_id   uuid NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    month         date NOT NULL,
    amount_limit  numeric(12,2) NOT NULL,
    created_at    timestamptz NOT NULL DEFAULT now(),
    updated_at    timestamptz NOT NULL DEFAULT now(),
    UNIQUE(category_id, month)
);
```

### 1.7 _migrations

```sql
CREATE TABLE IF NOT EXISTS _migrations (
    id          serial PRIMARY KEY,
    version     varchar(50) NOT NULL UNIQUE,
    applied_at  timestamptz NOT NULL DEFAULT now()
);
```

---

## 2. Índices

```sql
CREATE INDEX IF NOT EXISTS idx_transactions_account_date  ON transactions(account_id, date);
CREATE INDEX IF NOT EXISTS idx_transactions_category_date ON transactions(category_id, date);
CREATE INDEX IF NOT EXISTS idx_transactions_date          ON transactions(date);
CREATE INDEX IF NOT EXISTS idx_transactions_type          ON transactions(type);
CREATE INDEX IF NOT EXISTS idx_transactions_import_batch  ON transactions(import_batch_id);
CREATE INDEX IF NOT EXISTS idx_import_batches_account     ON import_batches(account_id);
CREATE INDEX IF NOT EXISTS idx_budgets_month              ON budgets(month);
```

---

## 3. RPCs

### 3.1 get_monthly_summary

Retorna totais de receita, despesa, saldo e contagem de transações para um mês.

```sql
CREATE OR REPLACE FUNCTION get_monthly_summary(p_year int, p_month int)
RETURNS TABLE(
    total_income numeric,
    total_expense numeric,
    balance numeric,
    transaction_count bigint,
    categorized_count bigint
) LANGUAGE sql STABLE AS $$
    SELECT
        COALESCE(SUM(CASE WHEN type = 'income' THEN amount END), 0) AS total_income,
        COALESCE(SUM(CASE WHEN type = 'expense' THEN amount END), 0) AS total_expense,
        COALESCE(SUM(CASE WHEN type IN ('income', 'expense')
                          AND NOT is_internal_transfer
                          AND NOT is_credit_card_payment
                     THEN amount END), 0) AS balance,
        COUNT(*) AS transaction_count,
        COUNT(category_id) AS categorized_count
    FROM transactions
    WHERE EXTRACT(YEAR FROM date) = p_year
      AND EXTRACT(MONTH FROM date) = p_month
      AND NOT is_internal_transfer
      AND NOT is_credit_card_payment;
$$;
```

### 3.2 get_category_ranking

Ranking de categorias por gasto, com percentual sobre a renda mensal.

```sql
CREATE OR REPLACE FUNCTION get_category_ranking(p_year int, p_month int)
RETURNS TABLE(
    category_name varchar,
    total_amount numeric,
    transaction_count bigint,
    pct_of_income numeric
) LANGUAGE sql STABLE AS $$
    WITH monthly_income AS (
        SELECT COALESCE((value->>'monthly_income')::numeric, 0) AS income
        FROM config WHERE key = 'monthly_income'
    )
    SELECT
        c.name AS category_name,
        ABS(SUM(t.amount)) AS total_amount,
        COUNT(*) AS transaction_count,
        CASE WHEN mi.income > 0
             THEN ROUND(ABS(SUM(t.amount)) / mi.income * 100, 1)
             ELSE 0
        END AS pct_of_income
    FROM transactions t
    JOIN categories c ON t.category_id = c.id
    CROSS JOIN monthly_income mi
    WHERE EXTRACT(YEAR FROM t.date) = p_year
      AND EXTRACT(MONTH FROM t.date) = p_month
      AND t.type = 'expense'
      AND NOT t.is_internal_transfer
      AND NOT t.is_credit_card_payment
    GROUP BY c.name, mi.income
    ORDER BY total_amount DESC;
$$;
```

### 3.3 get_monthly_trend

Tendência de receita/despesa/saldo dos últimos N meses.

```sql
CREATE OR REPLACE FUNCTION get_monthly_trend(p_months_back int DEFAULT 6)
RETURNS TABLE(
    year int,
    month int,
    total_income numeric,
    total_expense numeric,
    balance numeric
) LANGUAGE sql STABLE AS $$
    SELECT
        EXTRACT(YEAR FROM date)::int AS year,
        EXTRACT(MONTH FROM date)::int AS month,
        COALESCE(SUM(CASE WHEN type = 'income' THEN amount END), 0) AS total_income,
        COALESCE(SUM(CASE WHEN type = 'expense' THEN amount END), 0) AS total_expense,
        COALESCE(SUM(CASE WHEN type IN ('income', 'expense') THEN amount END), 0) AS balance
    FROM transactions
    WHERE date >= (CURRENT_DATE - (p_months_back || ' months')::interval)
      AND NOT is_internal_transfer
      AND NOT is_credit_card_payment
    GROUP BY EXTRACT(YEAR FROM date), EXTRACT(MONTH FROM date)
    ORDER BY year, month;
$$;
```

### 3.4 get_health_score

Score de saúde financeira (0–100) baseado na taxa de poupança.

```sql
CREATE OR REPLACE FUNCTION get_health_score(p_year int, p_month int)
RETURNS TABLE(
    score int,
    savings_rate numeric,
    top_category varchar,
    top_category_pct numeric
) LANGUAGE sql STABLE AS $$
    WITH summary AS (
        SELECT * FROM get_monthly_summary(p_year, p_month)
    ),
    top_cat AS (
        SELECT category_name, pct_of_income
        FROM get_category_ranking(p_year, p_month)
        LIMIT 1
    ),
    income_cfg AS (
        SELECT COALESCE((value->>'monthly_income')::numeric, 0) AS income
        FROM config WHERE key = 'monthly_income'
    )
    SELECT
        GREATEST(0, LEAST(100,
            CASE WHEN ic.income > 0
                 THEN ROUND(s.balance / ic.income * 100)::int
                 ELSE 50
            END
        )) AS score,
        CASE WHEN ic.income > 0
             THEN ROUND(s.balance / ic.income * 100, 1)
             ELSE 0
        END AS savings_rate,
        tc.category_name AS top_category,
        COALESCE(tc.pct_of_income, 0) AS top_category_pct
    FROM summary s
    CROSS JOIN income_cfg ic
    LEFT JOIN top_cat tc ON true;
$$;
```

### 3.5 get_budget_vs_actual

Comparação orçado vs. realizado por categoria para um mês.

```sql
CREATE OR REPLACE FUNCTION get_budget_vs_actual(p_year int, p_month int)
RETURNS TABLE(
    category_name varchar, budget_limit numeric,
    actual_spent numeric, pct_used numeric, remaining numeric
) LANGUAGE sql STABLE AS $$
    SELECT c.name, b.amount_limit,
        COALESCE(ABS(SUM(t.amount)), 0),
        CASE WHEN b.amount_limit > 0
             THEN ROUND(COALESCE(ABS(SUM(t.amount)), 0) / b.amount_limit * 100, 1)
             ELSE 0 END,
        b.amount_limit - COALESCE(ABS(SUM(t.amount)), 0)
    FROM budgets b
    JOIN categories c ON b.category_id = c.id
    LEFT JOIN transactions t ON t.category_id = c.id
        AND EXTRACT(YEAR FROM t.date) = p_year
        AND EXTRACT(MONTH FROM t.date) = p_month
        AND t.type = 'expense'
        AND NOT t.is_internal_transfer AND NOT t.is_credit_card_payment
    WHERE b.month = make_date(p_year, p_month, 1)
    GROUP BY c.name, b.amount_limit;
$$;
```

---

## 4. Seed Data

### 4.1 Categorias default

```sql
INSERT INTO categories (name, keywords, is_default) VALUES
    ('Alimentacao/Delivery',  '["ifood", "rappi", "uber eats", "zé delivery", "restaurante", "padaria", "mercado", "supermercado", "hortifruti"]', true),
    ('Transporte',            '["uber", "99", "combustivel", "gasolina", "estacionamento", "pedagio", "metro", "onibus"]', true),
    ('Moradia',               '["aluguel", "condominio", "iptu", "luz", "energia", "agua", "gas", "internet"]', true),
    ('Saude',                 '["farmacia", "drogaria", "hospital", "clinica", "medico", "dentista", "plano de saude", "unimed"]', true),
    ('Educacao',              '["escola", "faculdade", "curso", "livro", "udemy", "alura"]', true),
    ('Lazer',                 '["cinema", "teatro", "show", "spotify", "netflix", "disney", "hbo", "amazon prime", "steam", "playstation"]', true),
    ('Compras',               '["amazon", "mercado livre", "shopee", "magalu", "americanas", "renner", "zara"]', true),
    ('Servicos/Assinaturas',  '["nubank", "itau", "bradesco", "tarifa", "anuidade", "seguro", "icloud", "google one", "chatgpt"]', true),
    ('Transferencias',        '["pix", "ted", "doc", "transferencia"]', true),
    ('Outros',                '[]', true)
ON CONFLICT (name) DO NOTHING;
```

### 4.2 Config inicial

```sql
INSERT INTO config (key, value) VALUES
    ('setup_completed', '{"completed": false}'),
    ('default_currency', '{"currency": "BRL"}')
ON CONFLICT (key) DO NOTHING;
```

---

## 5. Migration Record

```sql
INSERT INTO _migrations (version) VALUES ('001_initial') ON CONFLICT DO NOTHING;
```
