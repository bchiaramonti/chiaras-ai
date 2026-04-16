# Validation Rules

Consolidated rule index for validating Claude Code artifacts. Each rule points to its source reference — load the source only when explaining FAILs or WARNINGs.

## Contents

- [Universal Rules](#universal-rules)
- [Skill-Specific Rules](#skill-specific-rules)
- [Agent-Specific Rules](#agent-specific-rules)
- [Command-Specific Rules](#command-specific-rules)
- [Hook-Specific Rules](#hook-specific-rules)
- [Plugin-Specific Rules](#plugin-specific-rules)
- [Marketplace-Specific Rules](#marketplace-specific-rules)
- [Grading Scale](#grading-scale)

---

## Universal Rules

Apply to ALL artifact types.

| ID | Rule | Severity | Source |
|----|------|----------|--------|
| U1 | Name: lowercase, numbers, hyphens only (max 64 chars) | FAIL | creating-skills/references/skill-reference.md |
| U2 | Name: no reserved words ("anthropic", "claude") | FAIL | creating-plugins/references/plugin-reference.md |
| U3 | Description: written in third person | WARNING | creating-skills/references/best-practices.md |
| U4 | Description: includes what it does AND when to use it | FAIL | creating-skills/references/best-practices.md |
| U5 | Description: max 1024 characters | FAIL | creating-skills/references/skill-reference.md |
| U6 | Description: no XML tags | FAIL | creating-skills/references/skill-reference.md |
| U7 | Unix-style paths only (forward slashes) | FAIL | creating-skills/references/best-practices.md |
| U8 | No time-sensitive information (dates, versions that expire) | WARNING | creating-skills/references/best-practices.md |
| U9 | Consistent terminology throughout (no synonym drift) | WARNING | creating-skills/references/best-practices.md |

---

## Skill-Specific Rules

| ID | Rule | Severity | Source |
|----|------|----------|--------|
| S1 | Name uses gerund form (verb + -ing) | WARNING | creating-skills/references/best-practices.md |
| S2 | SKILL.md exists at skill root | FAIL | creating-skills/references/skill-reference.md |
| S3 | SKILL.md under 500 lines | FAIL | creating-skills/references/best-practices.md |
| S4 | Progressive disclosure: detailed material in separate reference files | WARNING | creating-skills/references/best-practices.md |
| S5 | References max 1 level deep from SKILL.md | FAIL | creating-skills/references/best-practices.md |
| S6 | Long reference files (>100 lines) have table of contents | WARNING | creating-skills/references/best-practices.md |
| S7 | Scripts handle errors explicitly (don't punt to Claude) | FAIL | creating-skills/references/best-practices.md |
| S8 | Scripts have no undocumented magic numbers | WARNING | creating-skills/references/best-practices.md |
| S9 | Templates match strictness to task fragility | WARNING | creating-skills/references/best-practices.md |
| S10 | Workflows have clear sequential steps | WARNING | creating-skills/references/best-practices.md |
| S11 | Feedback loops present for critical operations | WARNING | creating-skills/references/best-practices.md |
| S12 | Frontmatter has required fields: name, description | FAIL | creating-skills/references/skill-reference.md |

---

## Agent-Specific Rules

| ID | Rule | Severity | Source |
|----|------|----------|--------|
| A1 | Description: clear about WHEN to delegate to this agent | FAIL | creating-agents/references/agent-reference.md |
| A2 | Tools: minimal set specified (principle of least privilege) | WARNING | creating-agents/references/agent-reference.md |
| A3 | Model: explicitly set and appropriate for task complexity | WARNING | creating-agents/references/agent-reference.md |
| A4 | System prompt: focused on ONE specialization | FAIL | creating-agents/references/agent-reference.md |
| A5 | System prompt: includes clear workflow steps | WARNING | creating-agents/references/agent-reference.md |
| A6 | Does not spawn subagents (no Agent tool in tools list) | FAIL | creating-agents/references/agent-reference.md |
| A7 | Proactive agents include "use proactively" or "use PROACTIVELY" in description | WARNING | creating-agents/references/agent-reference.md |
| A8 | Frontmatter has required fields: name, description | FAIL | creating-agents/references/agent-reference.md |

---

## Command-Specific Rules

| ID | Rule | Severity | Source |
|----|------|----------|--------|
| C1 | Single .md file (not a directory with SKILL.md) | WARNING | creating-commands/references/command-reference.md |
| C2 | Side-effect commands set `disable-model-invocation: true` | WARNING | creating-commands/references/command-reference.md |
| C3 | Uses `$ARGUMENTS` placeholder if command accepts input | WARNING | creating-commands/references/command-reference.md |
| C4 | Frontmatter has required fields: description | FAIL | creating-commands/references/command-reference.md |
| C5 | Consider migrating to skill (commands merged into skills) | WARNING | creating-commands/references/command-reference.md |

---

## Hook-Specific Rules

| ID | Rule | Severity | Source |
|----|------|----------|--------|
| H1 | Event name: correct PascalCase (e.g., PostToolUse, not postToolUse) | FAIL | creating-hooks/references/hooks-reference.md |
| H2 | Event name: exists in the official event list | FAIL | creating-hooks/references/hooks-reference.md |
| H3 | Matcher: valid regex pattern | FAIL | creating-hooks/references/hooks-reference.md |
| H4 | Command scripts: executable permissions (chmod +x) | FAIL | creating-hooks/references/hooks-reference.md |
| H5 | Command scripts: shebang line present (#!/bin/bash or #!/usr/bin/env bash) | FAIL | creating-hooks/references/hooks-reference.md |
| H6 | Command scripts: read JSON input from stdin | WARNING | creating-hooks/references/hooks-reference.md |
| H7 | Exit codes: uses only 0 (allow), 1 (error), 2 (block) | FAIL | creating-hooks/references/hooks-reference.md |
| H8 | Plugin hooks: use ${CLAUDE_PLUGIN_ROOT} for all paths | FAIL | creating-hooks/references/hooks-reference.md |
| H9 | Hook type has required fields (command needs `command`, http needs `url`) | FAIL | creating-hooks/references/hooks-reference.md |

---

## Plugin-Specific Rules

| ID | Rule | Severity | Source |
|----|------|----------|--------|
| P1 | plugin.json located inside .claude-plugin/ directory (not at root) | FAIL | creating-plugins/references/plugin-reference.md |
| P2 | Component dirs (skills/, agents/, hooks/) at plugin root (not inside .claude-plugin/) | FAIL | creating-plugins/references/plugin-reference.md |
| P3 | Version follows semantic versioning (MAJOR.MINOR.PATCH) | FAIL | creating-plugins/references/plugin-reference.md |
| P4 | All paths are relative, starting with ./ | FAIL | creating-plugins/references/plugin-reference.md |
| P5 | No files reference paths outside the plugin directory | FAIL | creating-plugins/references/plugin-reference.md |
| P6 | Hook scripts use ${CLAUDE_PLUGIN_ROOT} for paths | FAIL | creating-plugins/references/plugin-reference.md |
| P7 | MCP servers use ${CLAUDE_PLUGIN_ROOT} for paths | FAIL | creating-plugins/references/plugin-reference.md |
| P8 | Has README.md at plugin root | WARNING | creating-plugins/references/plugin-reference.md |
| P9 | plugin.json has required fields: name, description, version | FAIL | creating-plugins/references/plugin-reference.md |
| P10 | Plugin name matches directory name | WARNING | creating-plugins/references/plugin-reference.md |

---

## Marketplace-Specific Rules

| ID | Rule | Severity | Source |
|----|------|----------|--------|
| M1 | marketplace.json has required fields: name, owner, plugins array | FAIL | creating-plugins/references/marketplace-reference.md |
| M2 | Marketplace name: not a reserved name | FAIL | creating-plugins/references/marketplace-reference.md |
| M3 | Each plugin entry has name and source | FAIL | creating-plugins/references/marketplace-reference.md |
| M4 | No duplicate plugin names in plugins array | FAIL | creating-plugins/references/marketplace-reference.md |
| M5 | Version bumped when code changes (stale version = users don't get updates) | WARNING | creating-plugins/references/marketplace-reference.md |
| M6 | Plugin names are kebab-case | WARNING | creating-plugins/references/marketplace-reference.md |

---

## Grading Scale

| Grade | Criteria | Meaning |
|-------|----------|---------|
| **A** | 0 fails, 0 warnings | Production-ready, follows all best practices |
| **B** | 0 fails, 1-3 warnings | Functional, minor improvements recommended |
| **C** | 1-2 fails OR 4+ warnings | Needs fixes before publishing |
| **D** | 3+ fails | Significant issues, review creation skill references |
