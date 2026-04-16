---
name: generating-reports
description: >-
  Gera relatório mensal detalhado em Markdown: resumo executivo, breakdown
  por categoria, orçado vs realizado, comparativo MoM, tendência 6 meses,
  top 10 gastos e recomendações. Salva em brain/2-areas/financas/relatorios/.

  <example>
  Context: Relatório de um mês específico
  user: "superavit relatório janeiro"
  assistant: Coleta dados via MCP, gera relatório completo, salva como 2026-01-relatorio.md
  </example>
user-invocable: true
allowed-tools: mcp__claude_ai_Supabase__execute_sql, Write, Bash
---

# Generating Reports — Superavit

Gera relatórios mensais detalhados em Markdown, preenchendo o template com dados reais do Supabase.

## Pré-requisitos

- Setup concluído (`config.setup_completed = true`)
- Transações importadas no período solicitado
- Template disponível em `templates/relatorio-mensal.tmpl.md`

## Processo

### Etapa 1 — Resolver período

Usar mesma lógica de `querying-finances`:
- "relatório janeiro" → year = ano corrente, month = 1
- "relatório mês passado" → mês anterior
- "relatório" (sem mês) → perguntar qual mês

Guardar `year`, `month`, `MES_NOME` (ex: "Janeiro"), `MES_ANTERIOR` (ex: "Dezembro").

### Etapa 2 — Coletar dados via MCP

Executar as seguintes queries em sequência:

**1. Resumo do mês atual:**
```sql
SELECT * FROM get_monthly_summary(<year>, <month>);
```

**2. Resumo do mês anterior (para comparativo):**
```sql
SELECT * FROM get_monthly_summary(<prev_year>, <prev_month>);
```

**3. Ranking de categorias:**
```sql
SELECT * FROM get_category_ranking(<year>, <month>);
```

**4. Tendência 6 meses:**
```sql
SELECT * FROM get_monthly_trend(6);
```

**5. Health score:**
```sql
SELECT * FROM get_health_score(<year>, <month>);
```

**6. Orçado vs realizado:**
```sql
SELECT * FROM get_budget_vs_actual(<year>, <month>);
```

**7. Top 10 maiores gastos:**
```sql
SELECT
    t.date, t.description, ABS(t.amount) AS valor,
    c.name AS categoria
FROM transactions t
LEFT JOIN categories c ON t.category_id = c.id
WHERE EXTRACT(YEAR FROM t.date) = <year>
  AND EXTRACT(MONTH FROM t.date) = <month>
  AND t.type = 'expense'
  AND NOT t.is_internal_transfer
  AND NOT t.is_credit_card_payment
ORDER BY ABS(t.amount) DESC
LIMIT 10;
```

**8. Transações sem categoria:**
```sql
SELECT COUNT(*) AS sem_categoria
FROM transactions
WHERE EXTRACT(YEAR FROM date) = <year>
  AND EXTRACT(MONTH FROM date) = <month>
  AND category_id IS NULL
  AND NOT is_internal_transfer
  AND NOT is_credit_card_payment;
```

### Etapa 3 — Ler template

Ler o template de [relatorio-mensal.tmpl.md](templates/relatorio-mensal.tmpl.md).

### Etapa 4 — Preencher placeholders

Substituir cada `{{VARIAVEL}}` com dados formatados:

| Placeholder | Fonte | Formatação |
|-------------|-------|------------|
| `{{MES_NOME}}` | Resolução de período | "Janeiro", "Fevereiro", ... |
| `{{ANO}}` | Resolução de período | "2026" |
| `{{DATA_GERACAO}}` | Data atual | "DD/MM/YYYY HH:MM" |
| `{{HEALTH_SCORE_BAR}}` | `get_health_score` | Barra visual + score numérico |
| `{{TOTAL_RECEITAS}}` | `get_monthly_summary.total_income` | `R$ X.XXX,XX` |
| `{{TOTAL_DESPESAS}}` | `get_monthly_summary.total_expense` | `R$ X.XXX,XX` (valor absoluto) |
| `{{SALDO}}` | `get_monthly_summary.balance` | `R$ X.XXX,XX` |
| `{{SAVINGS_RATE}}` | `get_health_score.savings_rate` | `XX,X%` |
| `{{CATEGORIAS_TABLE}}` | `get_category_ranking` | Tabela Markdown |
| `{{ORCAMENTO_TABLE}}` | `get_budget_vs_actual` | Tabela Markdown (se houver orçamento) |
| `{{TOP_GASTOS_TABLE}}` | Query top 10 | Tabela Markdown |
| `{{MES_ANTERIOR}}` | Resolução de período | Nome do mês anterior |
| `{{COMPARATIVO_TABLE}}` | Dois `get_monthly_summary` | Tabela com deltas |
| `{{TENDENCIA_TABLE}}` | `get_monthly_trend` | Tabela 6 meses |
| `{{RECOMENDACOES}}` | Análise dos dados | 2-3 recomendações |

### Formatação das tabelas

**Categorias (ranking):**
```markdown
| # | Categoria | Valor | % Renda | Txns |
|--:|:----------|------:|--------:|-----:|
| 1 | Alimentacao/Delivery | R$ 1.850,00 | 18,5% | 34 |
| 2 | Moradia | R$ 1.500,00 | 15,0% | 4 |
```

**Orçado vs Realizado:**
```markdown
| Categoria | Limite | Gasto | Uso | Restante |
|:----------|-------:|------:|----:|---------:|
| Alimentacao | R$ 2.000,00 | R$ 1.850,00 | 92,5% | R$ 150,00 |
| Transporte | R$ 500,00 | R$ 620,00 | 124,0% | - R$ 120,00 |
```

Se não houver orçamentos definidos: substituir `{{ORCAMENTO_TABLE}}` por:
> _Nenhum orçamento definido. Use `/superavit:planning-budget` para criar._

**Comparativo MoM:**
```markdown
| Métrica | {{MES_ANTERIOR}} | {{MES_NOME}} | Delta |
|:--------|------------------:|-------------:|------:|
| Receitas | R$ 10.000,00 | R$ 10.500,00 | +5,0% |
| Despesas | R$ 7.500,00 | R$ 8.200,00 | +9,3% |
| Saldo | R$ 2.500,00 | R$ 2.300,00 | -8,0% |
```

**Tendência 6 meses:**
```markdown
| Mês | Receitas | Despesas | Saldo |
|:----|--------:|---------:|------:|
| Out/25 | R$ 10.000,00 | R$ 7.200,00 | R$ 2.800,00 |
| Nov/25 | R$ 10.000,00 | R$ 8.100,00 | R$ 1.900,00 |
```

**Top 10 gastos:**
```markdown
| # | Data | Descrição | Valor | Categoria |
|--:|:-----|:----------|------:|:----------|
| 1 | 15/01 | ALUGUEL APTO | R$ 2.500,00 | Moradia |
```

### Recomendações

Gerar 2-3 recomendações baseadas nos dados reais:
- Categoria que mais cresceu MoM → sugerir atenção
- Categoria acima do orçamento → sugerir ajuste
- Health score baixo → sugerir meta de poupança
- Sem categoria em transações → sugerir categorizar

Usar tom direto, não genérico. Referenciar números reais.

### Etapa 5 — Salvar relatório

```bash
mkdir -p ~/Documents/brain/2-areas/financas/relatorios
```

Salvar com Write tool em:
```
~/Documents/brain/2-areas/financas/relatorios/YYYY-MM-relatorio.md
```

Confirmar ao usuário: caminho do arquivo salvo + resumo do health score.

## Formatação

Mesmas regras de `querying-finances`:
- Valores: `R$ X.XXX,XX` (ponto milhar, vírgula decimal)
- Percentuais: `XX,X%` com vírgula
- Datas: `DD/MM/YYYY` ou `Mmm/AA` (tabelas compactas)
- Nunca incluir transferências internas ou pagamentos CC nos totais

## Anti-Patterns

- Nunca gerar relatório com dados inventados — se query retorna vazio, informar
- Nunca usar path absoluto — sempre `~/Documents/brain/...`
- Nunca omitir comparativo MoM — é a seção mais útil
- Nunca incluir transferências internas nos totais
- Nunca deixar placeholder `{{VAR}}` não substituído no output
