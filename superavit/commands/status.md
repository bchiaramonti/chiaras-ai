---
description: Visão rápida do mês — saldo, health score, top gastos e % orçamento
allowed-tools: mcp__claude_ai_Supabase__execute_sql
---

# Superavit — Status

Exibe um resumo financeiro compacto do mês atual. Output deve ter **menos de 20 linhas**. Toda formatação em pt-BR (R$, vírgula decimal, ponto milhar).

## Passo 1 — Verificar Setup

```sql
SELECT value FROM config WHERE key = 'setup_completed';
```

- Se resultado for `false` ou nenhuma linha retornada: responder **"Execute `/superavit:init` primeiro."** e **PARAR**. Não executar mais nada.

## Passo 2 — Coletar Dados (3 queries)

Executar as 3 RPCs via `mcp__claude_ai_Supabase__execute_sql`, usando ano/mês correntes:

```sql
-- 1. Resumo mensal
SELECT * FROM get_monthly_summary(
  EXTRACT(YEAR FROM CURRENT_DATE)::int,
  EXTRACT(MONTH FROM CURRENT_DATE)::int
);

-- 2. Health score
SELECT * FROM get_health_score(
  EXTRACT(YEAR FROM CURRENT_DATE)::int,
  EXTRACT(MONTH FROM CURRENT_DATE)::int
);

-- 3. Orçamento vs realizado (se orçamento existir)
SELECT * FROM get_budget_vs_actual(
  EXTRACT(YEAR FROM CURRENT_DATE)::int,
  EXTRACT(MONTH FROM CURRENT_DATE)::int
);
```

Se a query 3 retornar vazio (sem orçamento configurado), omitir a linha de orçamento do output.

## Passo 3 — Formatar Saída

Apresentar exatamente neste formato compacto:

```
## Superavit — <Mês por extenso> <Ano>

<HEALTH_SCORE_BAR>

| | Valor |
|:--|------:|
| Receitas | R$ X.XXX |
| Despesas | R$ X.XXX |
| **Saldo** | **R$ X.XXX** |

**Top gastos:** Categoria1 (XX%), Categoria2 (XX%), Categoria3 (XX%)

**Orçamento:** N categorias em dia, N em risco 🟡, N estouradas 🔴
```

### Regras de formatação

- **Health score bar**: barra visual proporcional (ex: `████████░░ 80/100 Saudável`)
  - 80-100: Saudável (verde)
  - 60-79: Atenção (amarelo)
  - < 60: Crítico (vermelho)
- **Top gastos**: 3 maiores categorias de despesa com % do total
- **Mês**: nome por extenso em português (Janeiro, Fevereiro, etc.)
- **Valores**: formato `R$ X.XXX,XX` com ponto milhar e vírgula decimal
- **Orçamento**: omitir linha inteira se não houver budgets configurados
