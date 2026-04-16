# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2026-04-06

### Added
- `homepage` and `repository` metadata fields in plugin.json

## [1.0.0] — 2026-03-02

### Added

#### Infrastructure
- Plugin manifest (`plugin.json`) with metadata and keywords
- Shared reference: `pipeline-overview.md` — pipeline diagram, skill→phase→artifact map, `.status` template
- Shared reference: `frameworks-glossary.md` — 17 software engineering frameworks with sources
- Shared reference: `phase-dependency-map.md` — dependency graph between skills with Mermaid diagram

#### Commands (6)
- `forge:init` — project scaffolding with directory structure, `.status`, CLAUDE.md, and git init
- `forge:status` — visual progress dashboard with phase bars and timeline
- `forge:next` — executes the next pending skill/agent in the pipeline
- `forge:phase` — detailed view of a specific phase (skills, artifacts, dependencies)
- `forge:review` — artifact completeness and inter-phase coherence review
- `forge:advance` — phase gate with approval validation and changelog update

#### Skills (17)
- `problem-framing` — Problem Statement Canvas with JTBD (Discovery)
- `competitive-landscape` — market analysis with gap identification (Discovery)
- `product-definition` — PRD with personas, user stories, MoSCoW (Product)
- `user-flow-mapping` — navigation flows with Mermaid diagrams (Design)
- `wireframe-spec` — textual wireframes per screen with states (Design)
- `design-system-bootstrap` — color, typography, spacing, components + JSON tokens (Design)
- `architecture-design` — C4 Model at 3 levels with Mermaid diagrams (Architecture)
- `adr-writer` — Architecture Decision Records in Nygard format (Architecture)
- `data-model-designer` — entities, relationships, ER diagrams (Architecture)
- `tech-spec-writer` — per-feature technical specifications (Specs)
- `code-standards` — linting, formatting, conventions by stack (Implementation)
- `test-strategy` — Test Pyramid + Testing Trophy strategy (Quality)
- `qa-checklist` — 22-check quality checklist across 6 categories (Quality)
- `security-baseline` — OWASP Top 10 applied to project context (Quality)
- `deploy-strategy` — hosting, CI/CD, env vars, rollback (Deploy)
- `observability-setup` — logging, error tracking, health checks (Deploy)
- `changelog-manager` — Keep a Changelog + SemVer maintenance (Cross-phase)

#### Agents (2)
- `scope-shaper` — scope vs. appetite negotiation, Shaped Pitch + MVP Definition (Opus)
- `dev-orchestrator` — implementation sequencing with dependency graph (Opus)

#### Templates (15)
- `problem-statement.tmpl.md`, `landscape-analysis.tmpl.md`
- `prd.tmpl.md`, `user-story-map.tmpl.md`
- `user-flows.tmpl.md`, `wireframe-screen.tmpl.md`
- `design-system.tmpl.md`, `design-tokens.tmpl.json`
- `adr.tmpl.md`, `data-model.tmpl.md`, `tech-spec.tmpl.md`
- `qa-checklist.tmpl.md`, `deploy-strategy.tmpl.md`
- `observability.tmpl.md`, `changelog.tmpl.md`

#### Skill References (4)
- `c4-model-guide.md` — practical C4 Model guide with Mermaid examples
- `conventions-by-stack.md` — code conventions by technology stack
- `test-pyramid-guide.md` — testing layers, tools, and coverage guidance
- `owasp-top10-checklist.md` — OWASP Top 10 checklist with implementation notes

#### Documentation
- `README.md` — overview, installation, quick start, full component catalog
- `CHANGELOG.md` — this file
- `LICENSE` — MIT

[1.0.0]: https://github.com/bchiaramonti/chiaras-ai/releases/tag/forge-v1.0.0
