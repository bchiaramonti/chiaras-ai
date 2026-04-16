---
name: planning-budget
description: >-
  Elabora e acompanha orçamento mensal por categoria. Define limites,
  sugere valores com base no histórico, mostra realizado vs orçado com
  barras de progresso, e alerta quando categorias estão estourando.

  <example>
  Context: Montar orçamento do zero
  user: "quero montar meu orçamento"
  assistant: Analisa média dos últimos 3 meses, sugere limites por categoria, confirma com usuário
  </example>

  <example>
  Context: Acompanhar execução
  user: "como estou no orçamento?"
  assistant: Mostra barras de progresso por categoria com % consumido e dias restantes
  </example>

  <example>
  Context: Ajustar limite
  user: "aumenta o orçamento de lazer pra 800"
  assistant: Atualiza limite no Supabase, mostra novo estado
  </example>
user-invocable: true
allowed-tools: mcp__claude_ai_Supabase__execute_sql
---

# Planning Budget — Superavit

Definição, sugestão inteligente, acompanhamento e ajuste de orçamento mensal por categoria.

## Pré-requisitos

- Setup concluído (`config.setup_completed = true`)
- Pelo menos 1 mês de transações importadas (para sugestão inteligente)

## Operações

### 1. Definir orçamento (novo)

**Trigger:** "montar orçamento", "criar orçamento", "definir limites"

**Etapa 1 — Buscar categorias ativas:**
```sql
SELECT id, name FROM categories WHERE is_active = true ORDER BY name;
```

**Etapa 2 — Calcular média dos últimos 3 meses por categoria:**
```sql
SELECT
    c.name AS categoria,
    c.id AS category_id,
    ROUND(AVG(monthly_total), 2) AS media_3m,
    ROUND(AVG(monthly_total) * 1.1 / 50) * 50 AS sugestao
FROM categories c
JOIN (
    SELECT
        category_id,
        EXTRACT(YEAR FROM date) AS yr,
        EXTRACT(MONTH FROM date) AS mo,
        ABS(SUM(amount)) AS monthly_total
    FROM transactions
    WHERE type = 'expense'
      AND NOT is_internal_transfer
      AND NOT is_credit_card_payment
      AND date >= (CURRENT_DATE - INTERVAL '3 months')
    GROUP BY category_id, EXTRACT(YEAR FROM date), EXTRACT(MONTH FROM date)
) sub ON c.id = sub.category_id
WHERE c.is_active = true
GROUP BY c.name, c.id
ORDER BY media_3m DESC;
```

> A sugestão é: média + 10% de margem, arredondada para múltiplo de R$ 50.

**Etapa 3 — Buscar renda mensal:**
```sql
SELECT (value->>'monthly_income')::numeric AS renda FROM config WHERE key = 'monthly_income';
```

**Etapa 4 — Apresentar sugestão:**

Perguntar: **"Quanto quer poupar por mês? (sugestão: 20% = R$ X.XXX)"**

Calcular: `disponivel = renda - poupanca`

Mostrar tabela:

```
Renda mensal: R$ 10.000,00
Meta de poupança: 20% = R$ 2.000,00
Disponível para gastos: R$ 8.000,00

| Categoria          | Média 3m    | Sugestão    | Ajustar? |
|:-------------------|------------:|------------:|:---------|
| Alimentacao        | R$ 1.680,00 | R$ 1.850,00 |          |
| Moradia            | R$ 1.450,00 | R$ 1.600,00 |          |
| Transporte         | R$ 480,00   | R$ 550,00   |          |
| Lazer              | R$ 320,00   | R$ 350,00   |          |
| ...                |             |             |          |
| **Total**          |             | **R$ X.XXX**|          |

Diferença vs disponível: R$ XXX (folga / excesso)
```

Permitir o usuário ajustar valores antes de confirmar.

**Etapa 5 — Persistir após confirmação:**
```sql
INSERT INTO budgets (category_id, month, amount_limit)
VALUES
    ('<cat_id_1>', '<YYYY-MM-01>', <valor_1>),
    ('<cat_id_2>', '<YYYY-MM-01>', <valor_2>),
    ...
ON CONFLICT (category_id, month)
DO UPDATE SET amount_limit = EXCLUDED.amount_limit, updated_at = now();
```

### 2. Copiar orçamento do mês anterior

**Trigger:** "copiar orçamento", "mesmo orçamento do mês passado"

```sql
SELECT c.name, b.amount_limit, b.category_id
FROM budgets b
JOIN categories c ON b.category_id = c.id
WHERE b.month = make_date(<prev_year>, <prev_month>, 1)
ORDER BY b.amount_limit DESC;
```

Mostrar valores e perguntar se quer ajustar algum. Após confirmação, inserir para o mês atual com o mesmo INSERT da operação 1.

### 3. Acompanhar execução

**Trigger:** "como estou no orçamento?", "budget", "acompanhar orçamento"

```sql
SELECT * FROM get_budget_vs_actual(<year>, <month>);
```

Formatar com barras de progresso (10 blocos):

```
Alimentação  ▓▓▓▓▓▓▓░░░  72,0%  R$ 1.080 / R$ 1.500  (resta R$ 420)   🟡
Transporte   ▓▓▓▓▓▓▓▓▓▓  105,0% R$ 525 / R$ 500     (- R$ 25)         🔴 ESTOURADO
Lazer        ▓▓▓░░░░░░░  28,0%  R$ 224 / R$ 800      (resta R$ 576)   🟢
Moradia      ▓▓▓▓▓▓▓▓▓░  92,0%  R$ 1.380 / R$ 1.500  (resta R$ 120)   🔴
```

**Semáforo:**

| % Consumido | Cor |
|-------------|-----|
| < 70% | 🟢 |
| 70–90% | 🟡 |
| 90–100% | 🔴 |
| > 100% | 🔴 ESTOURADO |

**Projeção para o resto do mês:**

Calcular: `projecao = (gasto_atual / dias_passados) * dias_no_mes`

```sql
SELECT
    EXTRACT(DAY FROM CURRENT_DATE) AS dias_passados,
    EXTRACT(DAY FROM (make_date(<year>, <month>, 1) + INTERVAL '1 month' - INTERVAL '1 day')) AS dias_no_mes;
```

Para cada categoria, se `projecao > budget_limit`: alertar.

```
⚠️ Projeções de estouro:
- Alimentação: projetado R$ 1.620 (limite R$ 1.500) — reduzir R$ 40/dia restante
- Transporte: já estourado — R$ 25 acima do limite
```

### 4. Ajustar limite

**Trigger:** "aumenta orçamento de X para Y", "muda limite de X"

Identificar categoria (por nome, case-insensitive):
```sql
SELECT id, name FROM categories WHERE name ILIKE '%<categoria>%';
```

Atualizar:
```sql
UPDATE budgets
SET amount_limit = <novo_valor>, updated_at = now()
WHERE category_id = '<cat_id>'
  AND month = make_date(<year>, <month>, 1);
```

Se não existe budget para a categoria/mês: criar com INSERT.

Mostrar estado atualizado (chamar operação 3).

### 5. Remover orçamento

**Trigger:** "remove orçamento de X", "tirar limite de X"

```sql
DELETE FROM budgets
WHERE category_id = '<cat_id>'
  AND month = make_date(<year>, <month>, 1);
```

Confirmar com o usuário antes de deletar. Mostrar estado atualizado.

## Sugestão Inteligente

Quando o usuário não tem histórico suficiente (< 1 mês), usar benchmarks genéricos baseados na renda:

| Categoria | % da Renda (benchmark) |
|-----------|----------------------:|
| Moradia | 30% |
| Alimentacao | 15% |
| Transporte | 10% |
| Saude | 5% |
| Educacao | 5% |
| Lazer | 5% |
| Compras | 5% |
| Servicos/Assinaturas | 5% |
| Poupança (meta) | 20% |

Total: 100%. Ajustar proporcionalmente se o usuário definir savings rate diferente.

## Formatação

- Valores: `R$ X.XXX,XX` (pt-BR)
- Barras: `▓` (preenchido) e `░` (vazio), 10 blocos
- Percentuais: `XX,X%` com vírgula
- Sugestões arredondadas para múltiplo de R$ 50

## Anti-Patterns

- Nunca criar orçamento sem mostrar sugestão primeiro — o usuário deve validar
- Nunca definir orçamento sem considerar renda — total dos limites deve caber na renda
- Nunca ignorar savings rate — sempre perguntar quanto o usuário quer poupar
- Nunca deletar sem confirmação
- Nunca ignorar orçamento existente ao acompanhar — se existe, sempre mostrar
