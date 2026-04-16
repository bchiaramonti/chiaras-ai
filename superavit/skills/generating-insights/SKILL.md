---
name: generating-insights
description: >-
  Análise de padrões de gasto com tom configurável. Health score 0-100,
  benchmarks contra renda e orçamento, provocações sobre hábitos.
  Três modos: neutral (factual), roast (stand-up comedy), alert (só críticos).

  <example>
  Context: Análise padrão
  user: "superavit insights"
  assistant: Health score, top categorias, padrões detectados, recomendações
  </example>

  <example>
  Context: Modo provocativo
  user: "faz um roast dos meus gastos"
  assistant: Roast completo estilo stand-up sobre os hábitos de gasto
  </example>
user-invocable: true
allowed-tools: mcp__claude_ai_Supabase__execute_sql
---

# Generating Insights — Superavit

Análise de padrões financeiros com health score, detecção de tendências e insights acionáveis. Tom configurável entre neutral, roast e alert.

## Modos de Voz

Verificar modo ativo:
```sql
SELECT value->>'voice_mode' AS mode FROM config WHERE key = 'voice_mode';
```

Se não existir ou `null`: usar `neutral` como default.

| Modo | Tom | Quando usar |
|------|-----|-------------|
| `neutral` | Factual, direto, dados + recomendações objetivas | Default, "insights", "análise" |
| `roast` | Humor ácido, exagera pontos fracos, provocativo | "roast", "detona", "mete o pau" |
| `alert` | Apenas itens críticos, sem contexto ou humor | "alertas", "problemas", "o que preciso saber" |

### Troca de modo

Se o usuário pedir para trocar o modo:
```sql
INSERT INTO config (key, value)
VALUES ('voice_mode', '{"voice_mode": "<novo_modo>"}')
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = now();
```

## Coleta de Dados

Executar via MCP:

**1. Health score:**
```sql
SELECT * FROM get_health_score(<year>, <month>);
```

**2. Ranking de categorias — mês atual:**
```sql
SELECT * FROM get_category_ranking(<year>, <month>);
```

**3. Ranking de categorias — mês anterior:**
```sql
SELECT * FROM get_category_ranking(<prev_year>, <prev_month>);
```

**4. Tendência 6 meses:**
```sql
SELECT * FROM get_monthly_trend(6);
```

**5. Orçado vs realizado (se existir):**
```sql
SELECT * FROM get_budget_vs_actual(<year>, <month>);
```

**6. Gastos recorrentes:**
```sql
SELECT
    description,
    COUNT(*) AS vezes,
    ABS(AVG(amount)) AS valor_medio,
    ABS(SUM(amount)) AS total
FROM transactions
WHERE EXTRACT(YEAR FROM date) = <year>
  AND EXTRACT(MONTH FROM date) = <month>
  AND type = 'expense'
  AND NOT is_internal_transfer
  AND NOT is_credit_card_payment
GROUP BY description
HAVING COUNT(*) >= 3
ORDER BY total DESC;
```

## Análise de Padrões

Após coletar dados, detectar os seguintes padrões:

### Crescimento MoM por categoria

Comparar `get_category_ranking` do mês atual vs anterior:

| Condição | Sinal |
|----------|-------|
| Categoria cresceu > 20% MoM | Alerta — gasto acelerando |
| Categoria encolheu > 20% MoM | Reconhecimento — economia visível |
| Categoria nova (não existia antes) | Atenção — gasto novo surgiu |

### Concentração

| Condição | Sinal |
|----------|-------|
| 1 categoria > 30% da renda | Alta concentração — risco |
| Top 3 categorias > 70% da renda | Pouca diversificação |

### Savings Rate

| Faixa | Avaliação |
|-------|-----------|
| > 30% | Excelente |
| 20-30% | Bom — benchmark ideal |
| 10-20% | Atenção — abaixo do recomendado |
| 0-10% | Alerta — margem mínima |
| < 0% | Crítico — gastando mais do que ganha |

### Tendência de saldo (últimos 3 meses)

| Condição | Sinal |
|----------|-------|
| 3 meses consecutivos caindo | Tendência de queda — precisa agir |
| 3 meses consecutivos subindo | Tendência positiva |
| Oscilando | Instável — sem padrão claro |

### Orçamento

| Condição | Sinal |
|----------|-------|
| `pct_used > 100%` | Estourou o orçamento |
| `pct_used > 80%` e estamos na 1a metade do mês | Em risco de estourar |
| `pct_used < 50%` no fim do mês | Bem controlado |

### Gastos recorrentes

| Condição | Sinal |
|----------|-------|
| Mesmo gasto 3+ vezes no mês | Provável assinatura ou hábito |
| Delivery 10+ vezes | Padrão de delivery frequente |

## Output por Modo

### Modo Neutral

```
## Health Score: 62/100 [======----]

### Destaques
- Savings rate: 12,3% (abaixo do benchmark de 20%)
- Top categoria: Alimentacao/Delivery (R$ 1.850,00 — 18,5% da renda)
- Moradia subiu 15,2% vs mês passado

### Padrões Detectados
- iFood apareceu 12x este mês (total: R$ 480,00)
- Categoria Lazer cresceu 35% MoM — de R$ 320 para R$ 432

### Orçamento
- Alimentacao: 92,5% consumido (R$ 150,00 restantes)
- Transporte: estourou em R$ 120,00 (124% do limite)

### Recomendações
1. Reduzir delivery em 30% economizaria ~R$ 144/mês
2. Rever orçamento de Transporte (3o mês consecutivo acima)
3. Meta: subir savings rate para 15% cortando R$ 270/mês
```

### Modo Roast

```
## Health Score: 62/100 — Nota: "Precisa estudar mais"

Bom, vamos lá. Você torrou R$ 480 em iFood este mês. São 12 pedidos.
Isso é um pedido a cada 2,5 dias. Seu fogão tá bem? Precisa de ajuda?

Sua categoria Lazer cresceu 35% — parabéns por investir no entretenimento
enquanto sua poupança chora no canto com 12,3%.

Ah, e o orçamento de Transporte? Estourou. De novo. Pelo terceiro mês.
Neste ponto não é orçamento, é ficção.

**Mas falando sério:** se você trocar 4 desses iFood por comida em casa
e respeitar o limite de Transporte, são R$ 264/mês que viram poupança.
Em 12 meses são R$ 3.168. Pensa nisso.
```

> Regra do roast: **sempre terminar com um insight construtivo.** Humor sobre hábitos, nunca sobre a pessoa.

### Modo Alert

```
- CRITICO: Savings rate 12,3% (meta: 20%)
- ESTOUROU: Transporte 124% do orçamento (3o mês consecutivo)
- ALERTA: Lazer +35% MoM
- ALERTA: Alimentacao 92,5% do orçamento consumido
```

Apenas itens com severidade alta. Sem contexto, sem humor, sem recomendações detalhadas.

## Anti-Patterns

- Nunca inventar dados para o roast — todo número deve vir das queries
- Nunca ser cruel — humor sobre **hábitos** de gasto, nunca sobre a **pessoa**
- Nunca omitir o lado positivo — reconhecer categorias que encolheram ou orçamentos respeitados
- Nunca misturar modos — se neutral, sem piadas; se roast, sem tabelas secas
- Nunca ignorar orçamento existente — se tem budget, sempre comparar
- Nunca mostrar roast sem o insight construtivo final
