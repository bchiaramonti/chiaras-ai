# Skill Reference

## Frontmatter Fields

All fields are optional. Only `description` is recommended.

| Field                      | Required    | Description                                                                                     |
|----------------------------|-------------|-------------------------------------------------------------------------------------------------|
| `name`                     | No          | Display name and `/slash-command`. Lowercase, numbers, hyphens (max 64 chars). Default: dir name.|
| `description`              | Recommended | What the skill does and when to use it. Max 1024 chars. No XML tags.                            |
| `argument-hint`            | No          | Hint for autocomplete. Example: `[issue-number]`.                                                |
| `disable-model-invocation` | No          | `true` = only user can invoke. Default: `false`.                                                 |
| `user-invocable`           | No          | `false` = hidden from `/` menu, only Claude invokes. Default: `true`.                            |
| `allowed-tools`            | No          | Tools allowed without permission prompt when skill is active.                                    |
| `model`                    | No          | Model: `sonnet`, `opus`, `haiku`, or `inherit`.                                                  |
| `context`                  | No          | `fork` = runs in isolated subagent context.                                                      |
| `agent`                    | No          | Subagent type when `context: fork`. Built-in: `Explore`, `Plan`, `general-purpose`. Or custom.   |
| `hooks`                    | No          | Lifecycle hooks scoped to this skill. See hooks docs for config format.                          |
| `paths`                    | No          | Glob patterns limiting auto-activation. Comma-separated string or YAML list. Same format as path-specific rules. |
| `effort`                   | No          | Effort level when active. Overrides session level. Options: `low`, `medium`, `high`, `max` (Opus 4.6 only). |
| `shell`                    | No          | Shell for `` !`command` `` blocks: `bash` (default) or `powershell`. Requires `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`. |

## String Substitutions

| Variable               | Description                                              |
|------------------------|----------------------------------------------------------|
| `$ARGUMENTS`           | All arguments. Appended automatically if not present.    |
| `$ARGUMENTS[N]`        | Argument by 0-based index.                               |
| `$N`                   | Shorthand for `$ARGUMENTS[N]`.                           |
| `${CLAUDE_SESSION_ID}` | Current session ID.                                      |
| `${CLAUDE_SKILL_DIR}`  | Directory containing the skill's SKILL.md. Use to reference bundled scripts/files. |

## Dynamic Context Injection

`` !`shell-command` `` executes before sending to Claude. Output replaces the placeholder.

```yaml
---
name: pr-review
context: fork
agent: Explore
---
PR diff: !`gh pr diff`
Files changed: !`gh pr diff --name-only`

Review this pull request.
```

## Invocation Control

| Frontmatter                      | User | Claude | Context loading                               |
|----------------------------------|------|--------|-----------------------------------------------|
| (default)                        | Yes  | Yes    | Description always, full content when invoked  |
| `disable-model-invocation: true` | Yes  | No     | Not in context, loads on user invoke           |
| `user-invocable: false`          | No   | Yes    | Description always, full content when invoked  |

## Scope & Placement

| Scope      | Path                                    | Available in              |
|------------|-----------------------------------------|---------------------------|
| Enterprise | managed settings                        | All org users             |
| Personal   | `~/.claude/skills/<name>/SKILL.md`      | All your projects         |
| Project    | `.claude/skills/<name>/SKILL.md`        | This project only         |
| Plugin     | `<plugin>/skills/<name>/SKILL.md`       | Where plugin is enabled   |

Priority: enterprise > personal > project. Plugin skills use `plugin-name:skill-name` namespace.

## Progressive Disclosure Levels

| Level | When loaded      | Token cost      | Content                              |
|-------|------------------|-----------------|--------------------------------------|
| 1     | Always (startup) | ~100 tokens     | `name` + `description` (frontmatter)|
| 2     | When triggered   | <5k tokens      | SKILL.md body                        |
| 3     | As needed        | Unlimited       | Reference files, scripts (via bash)  |

## Running in Subagent

Add `context: fork` for isolated execution. The SKILL.md content becomes the subagent's task prompt.

| Approach                   | System prompt              | Task             | Also loads         |
|----------------------------|----------------------------|------------------|--------------------|
| Skill + `context: fork`   | From agent type            | SKILL.md content | CLAUDE.md          |
| Subagent + `skills` field | Subagent's markdown body   | Delegation msg   | Preloaded skills   |

## Permission Control

```text
# Allow specific skills
Skill(commit)
Skill(review-pr *)

# Deny specific skills
Skill(deploy *)

# Deny all skills
Skill
```

## Extended Thinking

Include the word "ultrathink" anywhere in skill content to enable extended thinking mode.

## Bundled Skills

These ship with Claude Code and are available in every session:

| Skill        | Purpose                                                                 |
|--------------|-------------------------------------------------------------------------|
| `/simplify`  | Reviews changed files for reuse, quality, efficiency. Spawns 3 review agents in parallel. |
| `/batch`     | Orchestrates large-scale parallel changes (5–30 units, each in isolated git worktree). |
| `/debug`     | Troubleshoots current session by reading debug log.                     |
| `/loop`      | Runs a prompt repeatedly on an interval (e.g., `/loop 5m check deploy`). |
| `/claude-api`| Loads Claude API/SDK reference. Auto-activates on `anthropic` imports.  |

## Automatic Discovery

- **Nested directories**: When editing files in subdirectories, skills from nested `.claude/skills/` are auto-discovered (monorepo support).
- **`--add-dir` directories**: Skills from directories added via `--add-dir` are loaded with live change detection.
- **Commands merged into skills**: `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` both create `/deploy`. If both exist, the skill takes precedence.

## Context Budget

Skill descriptions consume ~1% of the context window (fallback: 8,000 chars). Each entry is capped at 250 characters. If too many skills exceed the budget, descriptions are shortened. Override with `SLASH_COMMAND_TOOL_CHAR_BUDGET` env var.
