# Changelog

All notable changes to the Superavit plugin will be documented in this file.

## [1.0.0] - 2026-03-10

### Added
- Plugin scaffold: plugin.json, .mcp.json (Supabase dependency), README.md
- **7 skills**: setting-up, importing-statements, querying-finances, generating-reports, generating-insights, planning-budget, managing-settings
- **2 agents**: data-ingestor (parsing pipeline), financial-analyst (queries, reports, insights)
- **5 commands**: init, importar, status, resumo, orcamento
- **2 Python scripts**: parse_statement.py (multi-bank parser), categorize.py (keyword matcher)
- **Schema DDL**: 7 tables (accounts, categories, config, import_batches, transactions, budgets, _migrations), 7 indexes, 5 RPCs
- **Report template**: relatorio-mensal.tmpl.md with 14 placeholders
- **Bank format reference**: Nubank (CSV/PDF), Itaú (CSV/OFX), Bradesco (OFX), Inter (CSV)
- CLAUDE.md generation step in setting-up for workflow orientation
- Marketplace entry in .claude-plugin/marketplace.json
