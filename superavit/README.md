# Superavit

Controle financeiro pessoal conversacional dentro do Claude. Importa extratos bancários de múltiplos bancos, categoriza transações automaticamente, gera relatórios mensais com breakdowns e comparativos, e entrega insights provocativos sobre seus hábitos de gasto.

## Pré-requisitos

- **Supabase** (free tier é suficiente) — projeto configurado com MCP ativo
- **Python 3.11+** com `pandas`, `ofxtools`, `pdfplumber` (apenas para importação de extratos)

## Setup

```
/superavit:setting-up
```

O skill de setup cria o schema no Supabase (7 tabelas + 5 RPCs) e configura categorias padrão.

## Skills

| Skill | Descrição | Scripts? |
|-------|-----------|----------|
| `setting-up` | Inicializa schema Supabase, cria tabelas e categorias padrão | Não |
| `importing-statements` | Importa extratos CSV/OFX/PDF, parseia e categoriza transações | Sim (Python) |
| `querying-finances` | Consulta transações, saldos e agregações via SQL | Não |
| `generating-reports` | Gera relatórios mensais com breakdown por categoria e MoM | Não |
| `generating-insights` | Calcula health score e gera insights provocativos | Não |
| `planning-budget` | Cria e gerencia orçamentos mensais por categoria | Não |
| `managing-settings` | Gerencia contas, categorias e configurações do usuário | Não |

## Commands

| Command | Descrição |
|---------|-----------|
| `/superavit:init` | Onboarding completo — schema, contas, categorias e orçamento |
| `/superavit:importar` | Importa extrato bancário da pasta input/ |
| `/superavit:status` | Visão rápida — saldo, health score, top gastos |
| `/superavit:resumo` | Resumo mensal — receitas, despesas, ranking |
| `/superavit:orcamento` | Orçado vs realizado com barras de progresso |

## Agents

| Agent | Descrição |
|-------|-----------|
| `data-ingestor` | Pipeline de ingestão de extratos com parsing multi-banco |
| `financial-analyst` | Consultas complexas, relatórios, insights e orçamento |

## Bancos Suportados

| Banco | Formatos |
|-------|----------|
| Nubank | CSV, PDF |
| Itaú | CSV, OFX |
| Bradesco | OFX |
| Inter | CSV |

## Schema Supabase

7 tabelas principais:

| Tabela | Descrição |
|--------|-----------|
| `accounts` | Contas bancárias do usuário |
| `categories` | Categorias de transação (sistema + custom) |
| `config` | Configurações do usuário (key-value) |
| `import_batches` | Metadados de cada importação |
| `transactions` | Transações financeiras categorizadas |
| `budgets` | Orçamentos mensais por categoria |
| `_migrations` | Controle de versão do schema |

5 RPCs: `get_monthly_summary`, `get_category_ranking`, `get_monthly_trend`, `get_health_score`, `get_budget_vs_actual`.

## Estrutura de Diretórios

```
superavit/
├── .claude-plugin/
│   └── plugin.json
├── .mcp.json
├── README.md
├── skills/
│   ├── setting-up/
│   │   ├── SKILL.md
│   │   └── references/schema-ddl.md
│   ├── importing-statements/
│   │   ├── SKILL.md
│   │   ├── scripts/parse_statement.py
│   │   ├── scripts/categorize.py
│   │   └── references/bank-formats.md
│   ├── querying-finances/SKILL.md
│   ├── generating-reports/
│   │   ├── SKILL.md
│   │   └── templates/relatorio-mensal.tmpl.md
│   ├── generating-insights/SKILL.md
│   ├── planning-budget/SKILL.md
│   └── managing-settings/SKILL.md
├── agents/
│   ├── data-ingestor.md
│   └── financial-analyst.md
└── commands/
    ├── init.md
    ├── importar.md
    ├── status.md
    ├── resumo.md
    └── orcamento.md
```

## Fluxo de Dados

```
Extrato Bancário (CSV/OFX/PDF)
        │
        ▼
   Parser (Python — parse_statement.py)
   ├── CSV (Nubank, Itaú, Inter)
   ├── OFX (Itaú, Bradesco)
   └── PDF (Nubank)
        │
        ▼
  Categorização (categorize.py)
  ├── Keywords (match determinístico)
  └── Claude fallback (sem match)
        │
        ▼
  Supabase PostgreSQL
  ├── transactions
  ├── import_batches
  └── accounts
        │
        ▼
  Consultas & RPCs
  ├── get_monthly_summary
  ├── get_category_ranking
  └── get_monthly_trend
        │
        ▼
  Relatórios & Insights
  ├── Breakdown mensal
  ├── Comparativo MoM
  ├── Health Score
  └── Insights provocativos
```
