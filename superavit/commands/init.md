---
description: Onboarding completo do Superavit — schema, contas, categorias e orçamento em uma sessão
allowed-tools: mcp__claude_ai_Supabase__execute_sql, mcp__claude_ai_Supabase__apply_migration, mcp__claude_ai_Supabase__list_projects, mcp__claude_ai_Supabase__get_project, mcp__claude_ai_Supabase__list_tables, Bash, Write
---

# Superavit — Init (Onboarding Completo)

Orquestra o setup inicial do Superavit em 7 fases conversacionais. Cada fase pergunta ao usuário e espera confirmação antes de avançar. **Nunca executar tudo silenciosamente.**

Rastrear o progresso interno com este checklist:

- [ ] Fase 1: Schema
- [ ] Fase 2: Renda
- [ ] Fase 3: Contas
- [ ] Fase 4: Categorias
- [ ] Fase 5: Orçamento
- [ ] Fase 6: Diretório local
- [ ] Fase 7: Confirmação

---

## Fase 1 — Schema (skill: setting-up)

Seguir o processo da skill `setting-up`:

1. Verificar conexão Supabase (`mcp__claude_ai_Supabase__list_projects`)
2. Se múltiplos projetos: perguntar qual usar
3. Verificar se schema já existe (7 tabelas, 5 RPCs)
4. Se já existe: informar e pular. Se parcial ou ausente: criar via DDL
5. Executar seed de categorias default

Informar resultado ao usuário antes de avançar.

---

## Fase 2 — Renda (skill: setting-up)

1. Perguntar: **"Qual é sua renda mensal líquida (o que cai na conta)?"**
2. Aceitar valor numérico (com ou sem R$, pontos, vírgulas)
3. Salvar na tabela `config`:

```sql
INSERT INTO config (key, value, updated_at)
VALUES ('monthly_income', '$VALOR', NOW())
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = NOW();
```

4. Confirmar: "Renda configurada: R$ X.XXX,XX"

---

## Fase 3 — Contas (skill: managing-settings)

1. Perguntar: **"Quais contas bancárias e cartões você usa no dia a dia?"**
2. Dar exemplos para guiar:
   ```
   Exemplos:
   - Nubank CC → nubank / credit_card
   - Itaú Conta → itau / checking
   - BTG Invest → btg / investment
   ```
3. Para cada conta informada, cadastrar na tabela `accounts`:
   - `name`: nome amigável
   - `bank`: identificador do banco
   - `type`: checking, savings, credit_card, investment
4. Listar contas cadastradas em tabela e perguntar: **"Ficou certo? Quer adicionar ou ajustar alguma?"**

---

## Fase 4 — Categorias (skill: managing-settings)

1. Mostrar as 10 categorias default (já inseridas pelo seed na Fase 1):

   | # | Categoria | Tipo |
   |---|-----------|------|
   | 1 | Moradia | essencial |
   | 2 | Alimentação | essencial |
   | 3 | Transporte | essencial |
   | 4 | Saúde | essencial |
   | 5 | Educação | essencial |
   | 6 | Lazer | lifestyle |
   | 7 | Vestuário | lifestyle |
   | 8 | Assinaturas | lifestyle |
   | 9 | Investimentos | savings |
   | 10 | Outros | variable |

2. Perguntar: **"Quer adicionar, remover ou renomear alguma categoria?"**
3. Aplicar alterações via SQL (INSERT/UPDATE/DELETE na tabela `categories`)
4. Listar categorias finais e confirmar

---

## Fase 5 — Orçamento (skill: planning-budget)

1. Com base na renda (Fase 2) e categorias ativas (Fase 4), sugerir alocação seguindo a regra 50/30/20:
   - 50% necessidades (essencial)
   - 30% desejos (lifestyle)
   - 20% poupança/investimentos (savings)

2. Apresentar tabela de sugestão:

   ```
   Renda: R$ XX.XXX

   | Categoria      | Sugestão   | % Renda |
   |:---------------|:-----------|:--------|
   | Moradia        | R$ X.XXX   | XX%     |
   | Alimentação    | R$ X.XXX   | XX%     |
   | ...            | ...        | ...     |
   | **Total**      | **R$ XX.XXX** | **100%** |
   ```

3. Perguntar: **"Quer ajustar algum valor antes de salvar?"**
4. Após confirmação, salvar na tabela `budgets`:

```sql
INSERT INTO budgets (category_id, monthly_limit, updated_at)
VALUES ($CATEGORY_ID, $VALOR, NOW())
ON CONFLICT (category_id) DO UPDATE SET monthly_limit = EXCLUDED.monthly_limit, updated_at = NOW();
```

---

## Fase 6 — Diretório local (skill: setting-up)

1. Criar estrutura de diretórios para extratos e relatórios:

```bash
mkdir -p ~/brain/2-areas/financas/{input,extratos,relatorios,exports}
```

2. Confirmar: "Diretórios criados em `~/brain/2-areas/financas/`"

> **Nota:** usar `~` para path dinâmico. Expandir via `$HOME` no Bash.

---

## Fase 7 — Confirmação Final

Ao completar todas as fases, apresentar resumo consolidado:

```
Superavit configurado!

| Item        | Status                        |
|:------------|:------------------------------|
| Schema      | ✅ 7 tabelas, 5 RPCs          |
| Renda       | ✅ R$ XX.XXX                  |
| Contas      | ✅ N contas cadastradas        |
| Categorias  | ✅ N categorias ativas         |
| Orçamento   | ✅ N categorias com limite     |
| Diretório   | ✅ brain/2-areas/financas/     |

Próximos passos:
1. Coloque extratos em brain/2-areas/financas/input/
2. Execute /superavit:importar
```

Substituir XX.XXX e N pelos valores reais coletados durante o onboarding.
