---
description: Orçado vs realizado por categoria com barras de progresso
argument-hint: "[mês]"
allowed-tools: mcp__claude_ai_Supabase__execute_sql
---

# Superavit — Orçamento

Exibe comparativo orçado vs realizado por categoria com barras de progresso visuais. Formatação segue o padrão da skill `planning-budget`.

## Passo 1 — Resolver Período

**Se `$ARGUMENTS` foi fornecido**, resolver o mês:

| Input | Interpretação |
|:------|:--------------|
| `janeiro`, `jan` | mês 1, ano corrente |
| `03` | mês 3, ano corrente |
| `2026-03` | mês 3, ano 2026 |
| `março 2025` | mês 3, ano 2025 |

**Se nenhum argumento:** usar mês e ano correntes.

## Passo 2 — Verificar Orçamento

```sql
SELECT COUNT(*) FROM budgets WHERE month = make_date(:year, :month, 1);
```

Se resultado for 0: responder **"Nenhum orçamento definido para <mês>. Use a skill `planning-budget` para criar um."** e **PARAR**.

## Passo 3 — Coletar Dados

```sql
SELECT * FROM get_budget_vs_actual(:year, :month);
```

## Passo 4 — Formatar Saída

Apresentar com barras de progresso por categoria:

```
## Orçamento — <Mês por extenso> <Ano>

Alimentação  ▓▓▓▓▓▓▓░░░  72%  R$ 1.080 / R$ 1.500  ✅
Transporte   ▓▓▓▓▓▓▓▓▓▓  105% R$ 525 / R$ 500     ⚠️
Lazer        ▓▓▓░░░░░░░  28%  R$ 224 / R$ 800       ✅

Total: R$ X.XXX / R$ X.XXX (XX%)
```

### Regras de formatação

- **Barra**: 10 caracteres, `▓` para preenchido, `░` para vazio
- **Status**:
  - ✅ até 90% — em dia
  - ⚠️ 90–100% — em risco
  - 🔴 acima de 100% — estourado
- **Alinhamento**: alinhar barras, percentuais e valores em colunas
- **Valores**: pt-BR (`R$ X.XXX,XX`)
- **Total**: soma consolidada de realizado / orçado ao final
- **Ordenação**: do maior % consumido para o menor
