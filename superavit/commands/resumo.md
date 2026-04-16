---
description: Resumo mensal — receitas, despesas, saldo e ranking de categorias
argument-hint: "[mês]"
allowed-tools: mcp__claude_ai_Supabase__execute_sql
---

# Superavit — Resumo Mensal

Exibe resumo financeiro de um mês com ranking de categorias. Formatação segue o padrão da skill `querying-finances`.

## Passo 1 — Resolver Período

**Se `$ARGUMENTS` foi fornecido**, resolver o mês:

| Input | Interpretação |
|:------|:--------------|
| `janeiro`, `jan` | mês 1, ano corrente |
| `03` | mês 3, ano corrente |
| `2026-03` | mês 3, ano 2026 |
| `março 2025` | mês 3, ano 2025 |

**Se nenhum argumento:** usar mês e ano correntes (`CURRENT_DATE`).

## Passo 2 — Coletar Dados

Executar via `mcp__claude_ai_Supabase__execute_sql`:

```sql
-- 1. Resumo mensal
SELECT * FROM get_monthly_summary(:year, :month);

-- 2. Ranking de categorias
SELECT * FROM get_category_ranking(:year, :month);
```

## Passo 3 — Formatar Saída

Seguir o padrão de formatação da skill `querying-finances`:

```
## Resumo — <Mês por extenso> <Ano>

| | Valor |
|:--|------:|
| Receitas | R$ X.XXX,XX |
| Despesas | R$ X.XXX,XX |
| **Saldo** | **R$ X.XXX,XX** |

### Ranking de Categorias

| # | Categoria | Valor | % |
|:--|:----------|------:|--:|
| 1 | Moradia | R$ X.XXX | XX% |
| 2 | Alimentação | R$ X.XXX | XX% |
| ... | ... | ... | ... |
```

### Regras

- Valores em pt-BR: `R$ X.XXX,XX` (ponto milhar, vírgula decimal)
- Mês por extenso em português
- Ranking ordenado do maior para menor gasto
- Saldo positivo sem prefixo, negativo com `-`
