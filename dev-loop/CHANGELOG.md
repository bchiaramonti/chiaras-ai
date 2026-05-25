# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] — 2026-05-25

Initial release.

### Added

#### Infrastructure
- Plugin manifest (`plugin.json`) with metadata, keywords, and homepage/repository
- `README.md` documenting the 5-fase loop, components, and design rationale
- Shared reference: `references/opus-4-7-principles.md` — 5 princípios destilados de 8 fontes (Anthropic blog, Tembo, CloudZero, claudefa.st, etc.)
- Shared reference: `references/dev-loop-overview.md` — state machine diagram, file layout, phase gates, `.status` schema
- `.mcp.json` — empacota o MCP oficial do Supabase (HTTP com OAuth automático)

#### Commands (2)
- `dev-loop:start <task>` — inicializa diretório, status, e invoca `writing-spec` (com `disable-model-invocation: true` por ser side-effect command)
- `dev-loop:status` — leitor puro de estado: mostra fase atual, artefatos pendentes e próxima skill recomendada

#### Skills (6, todas user-invocable)
- `scaffolding-project` — bootstraps estrutura padrão Claude Code 2026 (CLAUDE.md, CHANGELOG.md, `.claude/{agents,commands,skills,hooks,settings.json}`, `.mcp.json`, `.gitignore`, `.dev-loop/.status`); idempotente
- `writing-spec` — estrutura SPEC.md com 4 campos do single-turn pattern (intent, constraints, acceptance criteria, file locations)
- `researching-task` — dispatcha subagents Explore em paralelo; consolida findings em `research-notes.md` (task-specific) + apêndice em `CLAUDE.md` (durável entre sessões)
- `planning-implementation` — sintetiza SPEC + research em `PLAN.md` literal-executável com passos numerados, dependências, e hints de subagent dispatch
- `implementing-plan` — executa PLAN.md passo a passo; cada subagent recebe prompt `mandatory-first-read` (anti-drift)
- `verifying-against-spec` — cruza cada Acceptance Criteria 1-para-1 em `VERIFY.md`; gate final para fechar tarefa

#### Agents (2, read-only, isolated context)
- `spec-auditor` (sonnet) — audita SPEC.md contra codebase; rubrica A-D × 4 dimensões + gaps
- `plan-critic` (opus) — audita PLAN.md por literal-executability (anti-drift); issues priorizadas 🔴🟡🟢

#### Templates (7)
- SPEC, PLAN, VERIFY, research-notes, CLAUDE, CHANGELOG, settings, status, mcp, gitignore — todos com placeholders e estrutura fixa

#### Skill references (2)
- `researching-task/references/parallel-dispatch.md` — padrão de fan-out de subagents Explore com prompt template
- `implementing-plan/references/subagent-dispatch.md` — critérios subagent vs main thread + prompt mandatory-first-read literal

### Design notes
- 5 princípios Opus 4.7 (Spec-first single-turn, Plan-as-contract, Context engineering por isolamento, Paralelismo onde compensa, Verify-against-spec gate) incorporados no fluxo das skills
- Findings duráveis da fase research são persistidos em `CLAUDE.md` do projeto consumidor (memória entre sessões)
- 0 fails / 0 warnings em validação pelo `claude-code-toolkit:validating-artifacts` (Grade A em todos os 11 artefatos)
