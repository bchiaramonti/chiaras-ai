# Changelog

All notable changes to the claude-code-toolkit plugin are documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.1] - 2026-04-06

### Added
- `keywords` metadata field in plugin.json for marketplace discoverability

## [2.2.0] - 2026-03-30

### Added
- **validating-artifacts** skill: Universal validator that checks any Claude Code artifact (skill, agent, command, hook, plugin, marketplace) against best practices from all creation skills. Produces graded reports (A–D) with pass/fail/warning per rule. Includes 51 rules across 7 categories, recursive plugin validation, and cross-references to source specifications. Files: SKILL.md + references/validation-rules.md.

### Changed
- Plugin description updated to mention validation capability.

## [2.1.1] - 2026-03-30

### Changed
- **skill-reference.md**: Added `effort`, `paths`, `shell` frontmatter fields; fixed context budget from ~2%/16k to ~1%/8k with 250-char per-entry cap.
- **command-reference.md**: Added `effort`, `paths`, `shell` frontmatter fields; added `${CLAUDE_SKILL_DIR}` to string substitutions.
- **agent-reference.md**: Added `effort`, `initialPrompt` fields; full model ID support (e.g., `claude-opus-4-6`); `--agent` CLI flag; @-mention syntax; model resolution order (4-tier hierarchy).
- **hooks-reference.md**: Major rewrite — added 12 new events (StopFailure, TaskCreated, ConfigChange, CwdChanged, FileChanged, WorktreeCreate/Remove, PostCompact, Elicitation/ElicitationResult); native `http` hook type; `async`/`if`/`once`/`statusMessage`/`shell` fields; JSON output format; `$CLAUDE_ENV_FILE`/`$CLAUDE_PROJECT_DIR` env vars; detailed matchers per event.
- **plugin-reference.md**: Added `userConfig`, `channels`, `${CLAUDE_PLUGIN_DATA}`; fixed component path behavior (replace not supplement); expanded hook events from 15 to 25; added `--keep-data` flag.
- **marketplace-reference.md**: Added `git-subdir` source type; removed incorrect `pip` source; expanded `strictKnownMarketplaces` with `pathPattern`; added auto-update, seed dirs, git timeout sections.
- **creating-hooks SKILL.md**: Updated hook types list with native `http`; corrected `agent` type field; added HTTP/FileChanged/env var patterns.
- **creating-plugins SKILL.md**: Added `channels`, `userConfig`, `output-styles/` to structure and workflow.
- **sources.md**: Updated last-checked date and added comprehensive update log entry.

## [2.1.0] - 2026-03-10

### Added
- **creating-hooks** skill: New skill for creating Claude Code hooks (event handlers) with SKILL.md and hooks-reference.md covering all 15 hook events, 4 hook types (command, prompt, agent, HTTP), exit code behavior, matchers, and placement options.
- **Agent Teams** section in agent-reference.md: Experimental feature documentation covering architecture, display modes, use cases, hooks for quality gates, and limitations.
- **skill-reference.md**: `${CLAUDE_SKILL_DIR}` string substitution, Bundled Skills table (`/simplify`, `/batch`, `/debug`, `/loop`, `/claude-api`), Automatic Discovery section (nested dirs, `--add-dir`, commands merged into skills), Context Budget section (`SLASH_COMMAND_TOOL_CHAR_BUDGET`).
- **agent-reference.md**: Built-in agents expanded (Bash, statusline-setup, Claude Code Guide), Managing Subagents section (`/agents`, `claude agents`, `--agents` CLI flag), Resuming subagents, Backgrounding (Ctrl+B), Auto-compaction, Task→Agent rename note, model parameter note.
- **plugin-reference.md**: `InstructionsLoaded` hook event, HTTP hooks type, `agent_id`/`agent_type` hook context fields, `/reload-plugins` command, Official Marketplace Submission section.
- **best-practices.md**: Skills 2.0 Skill Categories (Capability Uplift vs Workflow/Preference), Evaluation-Driven Development workflow, MCP Tool References pattern, Table of Contents guidance.
- **sources.md**: 3 new secondary sources (Official Plugins Directory, CHANGELOG, Release Notes tracker), Hooks guide URL.
- **updating-toolkit SKILL.md**: hooks focus area, creating-hooks in comparison list and report template.

## [2.0.0] - 2026-03-01

### Added
- **creating-plugins** skill: Full plugin creation workflow with plugin-reference.md and marketplace-reference.md, plus plugin.json and marketplace entry templates.
- **versioning-artifacts** skill: Automated version bumping, changelog generation, commit/push workflow with versioning-reference.md.
- **updating-toolkit** skill: Self-improving research skill that fetches latest Anthropic docs and updates all toolkit references, with sources.md tracking.
- All reference files created from official Anthropic documentation.

### Changed
- Expanded from 3 skills (commands, skills, agents) to 6 skills (added plugins, versioning, updating).

## [1.0.0] - 2026-02-15

### Added
- Initial release with 3 creation skills: creating-commands, creating-skills, creating-agents.
- Reference files: command-reference.md, skill-reference.md, best-practices.md, agent-reference.md.
- Templates: COMMAND-TEMPLATE.md, SKILL-TEMPLATE.md, AGENT-TEMPLATE.md.
