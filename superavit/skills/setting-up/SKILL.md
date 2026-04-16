---
name: setting-up
description: >-
  Inicializa o Superavit: cria schema no Supabase (7 tabelas, 5 RPCs),
  seed de categorias default, configura renda mensal. Idempotente.
  Use quando o usuário diz "superavit setup" ou na primeira execução.

  <example>
  Context: Primeiro uso do plugin
  user: "superavit setup"
  assistant: Verifica conexão Supabase, cria tabelas via MCP, pede renda mensal, confirma
  </example>
user-invocable: true
allowed-tools: mcp__claude_ai_Supabase__execute_sql, mcp__claude_ai_Supabase__apply_migration, mcp__claude_ai_Supabase__list_projects, mcp__claude_ai_Supabase__get_project, mcp__claude_ai_Supabase__list_tables, Bash, Write
---

# Setting Up — Superavit

Inicializa toda a infraestrutura do Superavit: schema PostgreSQL no Supabase, categorias default, renda mensal e diretórios locais.

## Pré-requisitos

- Projeto Supabase criado (free tier é suficiente)
- MCP Supabase acessível (`mcp__claude_ai_Supabase__*`)

## Processo

### Etapa 1 — Verificar conexão Supabase

1. Chamar `mcp__claude_ai_Supabase__list_projects`
2. Se múltiplos projetos: perguntar ao usuário qual usar
3. Se nenhum projeto: orientar a criar um em supabase.com
4. Guardar o `project_id` para as chamadas seguintes

### Etapa 2 — Verificar schema existente

Executar via `mcp__claude_ai_Supabase__execute_sql`:

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN ('accounts', 'categories', 'config', 'import_batches', 'transactions', 'budgets', '_migrations');
```

- Se todas as 7 tabelas existem: informar que setup já foi executado
- Se parcial: informar quais faltam e prosseguir (DDL é idempotente)
- Se nenhuma: prosseguir com setup completo

### Etapa 3 — Criar schema

Executar o DDL completo de [schema-ddl.md](references/schema-ddl.md), na seguinte ordem:

1. **Tabelas** (respeitar ordem de foreign keys):
   - `accounts`
   - `categories`
   - `config`
   - `import_batches` (depende de `accounts`)
   - `transactions` (depende de `accounts`, `categories`, `import_batches`)
   - `budgets` (depende de `categories`)
   - `_migrations`

2. **Índices** — todos com `IF NOT EXISTS`

3. **RPCs** — todas com `CREATE OR REPLACE`

Usar `mcp__claude_ai_Supabase__execute_sql` para cada bloco. Agrupar tabelas sem dependências mútuas quando possível.

### Etapa 4 — Seed de dados

Executar seed de categorias e config inicial do [schema-ddl.md](references/schema-ddl.md) seção "Seed Data". Todos os INSERTs usam `ON CONFLICT DO NOTHING`.

### Etapa 5 — Configurar renda mensal

1. Perguntar ao usuário: **"Qual é sua renda mensal líquida (após impostos)?"**
2. Aceitar valor numérico (R$ ou sem prefixo)
3. Salvar:

```sql
INSERT INTO config (key, value)
VALUES ('monthly_income', '{"monthly_income": <VALOR>}')
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = now();
```

> **Não pular esta etapa.** A renda é usada nos RPCs `get_category_ranking` e `get_health_score` para calcular percentuais.

### Etapa 6 — Criar diretórios locais

```bash
mkdir -p ~/brain/2-areas/financas/{input,extratos,relatorios,exports}
```

Propósito de cada diretório:
- `input/` — extratos bancários brutos (CSV, OFX, PDF) para importação
- `extratos/` — extratos processados e arquivados por mês
- `relatorios/` — relatórios mensais gerados
- `exports/` — dados exportados (CSV, JSON)

> **Nunca usar caminhos absolutos.** Sempre `~/brain/...` ou path relativo.

### Etapa 7 — Criar CLAUDE.md do workflow

Criar `~/brain/2-areas/financas/CLAUDE.md` com instruções para o Claude sobre o workflow financeiro. Este arquivo é carregado automaticamente quando o usuário abre o diretório `financas/` no Claude Code.

Conteúdo do arquivo:

```markdown
# CLAUDE.md — Finanças Pessoais (Superavit)

Este diretório é o workspace do Superavit, plugin de controle financeiro pessoal.

## Estrutura

- `input/` — Depositar extratos bancários aqui para importação
- `extratos/` — Extratos processados, organizados por YYYY-MM/
- `relatorios/` — Relatórios mensais gerados (YYYY-MM-relatorio.md)
- `exports/` — Dados exportados (CSV, JSON)

## Workflow

1. **Importar**: colocar extrato em `input/`, rodar `/superavit:importar`
2. **Consultar**: perguntar em linguagem natural ("quanto gastei com delivery?")
3. **Relatório**: `/superavit:resumo` (rápido) ou `/superavit:generating-reports` (completo)
4. **Orçamento**: `/superavit:orcamento` para acompanhar, `/superavit:planning-budget` para criar
5. **Insights**: `/superavit:generating-insights` para análise com health score

## Persistência

Dados ficam no **Supabase PostgreSQL** (7 tabelas, 5 RPCs). Queries via `mcp__claude_ai_Supabase__execute_sql`.

Tabelas: accounts, categories, config, import_batches, transactions, budgets, _migrations.

## Bancos Suportados

Nubank (CSV, PDF), Itaú (CSV, OFX), Bradesco (OFX), Inter (CSV).

## Regras

- Nunca usar caminhos absolutos — sempre `~/brain/2-areas/financas/...`
- Nunca incluir transferências internas ou pagamentos CC nos totais
- Valores sempre em pt-BR: `R$ X.XXX,XX`
- Extratos processados vão para `extratos/YYYY-MM/`, nunca ficam em `input/`
```

> Se o arquivo já existe: não sobrescrever. Informar que já existe.

### Etapa 8 — Marcar setup como completo

```sql
INSERT INTO config (key, value)
VALUES ('setup_completed', '{"completed": true, "completed_at": "<ISO_TIMESTAMP>"}')
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = now();
```

```sql
INSERT INTO _migrations (version) VALUES ('001_initial') ON CONFLICT DO NOTHING;
```

## Confirmação

Após completar todas as etapas, apresentar tabela resumo:

| Item | Status |
|------|--------|
| Projeto Supabase | ✅ `<nome do projeto>` |
| Tabelas criadas | ✅ 7/7 |
| Índices | ✅ 7 |
| RPCs | ✅ 5 |
| Categorias default | ✅ 10 |
| Renda mensal | ✅ R$ X.XXX,XX |
| Diretórios locais | ✅ 4 criados |
| CLAUDE.md | ✅ criado em financas/ |
| Migration | ✅ 001_initial |

**Próximos passos:**
1. Coloque um extrato bancário em `~/brain/2-areas/financas/input/`
2. Use `/superavit:importing-statements` para importar

## Idempotência

Todas as operações são seguras para re-execução:
- Tabelas: `CREATE TABLE IF NOT EXISTS`
- Índices: `CREATE INDEX IF NOT EXISTS`
- RPCs: `CREATE OR REPLACE FUNCTION`
- Seeds: `INSERT ... ON CONFLICT DO NOTHING`
- Config: `INSERT ... ON CONFLICT (key) DO UPDATE`

## Anti-Patterns

- ❌ Caminhos absolutos (`/Users/...`) — sempre usar `~/brain/...`
- ❌ Pular a pergunta de renda mensal — RPCs dependem dela
- ❌ DDL sem `IF NOT EXISTS` — quebra idempotência
- ❌ Executar todo SQL em uma única chamada — dividir por bloco lógico
- ❌ Criar tabelas fora de ordem — respeitar foreign keys
