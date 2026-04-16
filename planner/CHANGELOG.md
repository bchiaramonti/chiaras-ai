# Changelog

All notable changes to the Planner plugin will be documented in this file.

## [1.2.0] - 2026-04-16

### Changed
- **`.mcp.json` portability**: removed the absolute path to `3-resources/ai-mcp/garmin-mcp` (violated plugin rules P5 "no paths outside plugin dir" and P7 "MCP servers use `${CLAUDE_PLUGIN_ROOT}`"). The plugin now calls simply `garmin-mcp` as a PATH binary, installed via `uv tool install`. Makes the plugin portable across machines and cache-safe (`~/.claude/plugins/cache/`).
- **README prerequisite updated**: added step 1 `uv tool install /path/to/garmin-mcp` before the existing auth step. `garmin-mcp-auth` is now a direct command (was `uv run garmin-mcp-auth`).

### Fixed
- Plugin validation grade: **C → A** (two P5/P7 failures resolved).

### Updated skill · generating-daily-planner
- Introduced `--fs-roman: 28px` token for the Tres inadiaveis roman numerals (previously used `--fs-h1: 40px` — too large). `.inadiaveis__item` grid column `36px → 28px`.
- **Tarefas ClickUp** metadata rule: `.tasks__title-meta` now shows `· <lista> · <tag>` (list first, then tag) to preserve ClickUp's hierarchy and avoid ambiguity. Multiple tags separated by comma in the tag segment.
- Documentation cleanup: removed time-sensitive date from `tokens.css` header, added section index, and replaced the `40px` literal in `principios.md` with the stable token reference `--fs-display`.

## [1.1.0] - 2026-04-16

### Added
- **MCP server**: `garmin` via `.mcp.json` — bundles the Taxuspt/garmin_mcp stdio server (~96 tools across activities, sleep, HRV, stress, training load, workouts, devices). Enables the daily planner to enrich the "Corpo" zone with real Garmin Connect data (sleep score, HRV overnight, Body Battery, previous-day activities).
- Source lives at `/Users/bchiaramonti/Documents/brain/3-resources/ai-mcp/garmin-mcp/` (separate Python project managed by `uv`). Plugin declares the server via `.mcp.json`; authentication is one-time via `uv run garmin-mcp-auth` (tokens stored at `~/.garminconnect`, ~6 month lifetime).

## [1.0.0] - 2026-04-16

### Added
- Plugin scaffold: `plugin.json`, `README.md`, `.claude-plugin/`
- **1 skill**: `generating-daily-planner` (auto-invoked when Bruno requests his daily planner)
- **6 references**:
  - `tokens.css` — CSS variables (colors, typography, spacing, layout zones)
  - `tokens.json` — DTCG format tokens for interop (Figma Tokens Studio, Tailwind)
  - `principios.md` — 6 founding design principles (typography over boxes, color as decision, zero ornament, etc.)
  - `componentes.md` — 12 components specified with HTML examples and CSS classes
  - `regras-texto.md` — editorial voice rules (section labels, lide journalistic tone, insight structure, metric formatting)
  - `template-html.html` — standalone HTML starter (header 5-zone + body 3-col + footer 2-col)
- **Design system**: Planner Editorial Noturno
  - Dark mode warm native (bg `#1A1715`)
  - Georgia serif (narrative) + Inter sans (tabular numbers only)
  - Palette: terracota `#D97757` (work/focus) + azul petroleo `#6B9EB0` (body/training) + alert `#B8593C`
  - Layout: header 5-zone (Dia · Lide · Insight · Mes · Corpo) + body 3-col (Agenda · Tres inadiaveis + Tarefas ClickUp · Delegadas) + footer 2-col (Notas · Amanha)
  - Zero ornament philosophy (no cards, shadows, gradients, pills, badges)
- Marketplace entry in `bchiaramonti-plugins/.claude-plugin/marketplace.json`
