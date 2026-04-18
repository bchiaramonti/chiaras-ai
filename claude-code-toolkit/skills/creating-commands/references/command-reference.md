# Command Reference

## Frontmatter Fields

All fields are optional. Only `description` is recommended.

| Field                      | Required    | Description                                                                                 |
|----------------------------|-------------|---------------------------------------------------------------------------------------------|
| `name`                     | No          | Display name. If omitted, uses filename. Lowercase, numbers, hyphens (max 64 chars).        |
| `description`              | Recommended | What the command does and when to use it. Used for discovery by Claude.                      |
| `argument-hint`            | No          | Hint shown during autocomplete. Example: `[issue-number]` or `[filename] [format]`.         |
| `disable-model-invocation` | No          | `true` prevents Claude from auto-triggering. Use for side-effect commands. Default: `false`. |
| `user-invocable`           | No          | `false` hides from `/` menu. Use for background knowledge. Default: `true`.                  |
| `allowed-tools`            | No          | Tools Claude can use without asking permission when command is active.                        |
| `model`                    | No          | Model to use: `sonnet`, `opus`, `haiku`, or `inherit`.                                       |
| `context`                  | No          | `fork` to run in isolated subagent context.                                                  |
| `agent`                    | No          | Subagent type when `context: fork`. Options: `Explore`, `Plan`, `general-purpose`, or custom.|
| `hooks`                    | No          | Hooks scoped to this command's lifecycle.                                                    |
| `paths`                    | No          | Glob patterns limiting auto-activation. Comma-separated string or YAML list.                 |
| `effort`                   | No          | Effort level when active. Overrides session level. Options: `low`, `medium`, `high`, `xhigh`, `max`. Available levels depend on the model. |
| `shell`                    | No          | Shell for `!<cmd>` (backtick-wrapped) blocks: `bash` (default) or `powershell`.              |

## String Substitutions

| Variable               | Description                                              |
|------------------------|----------------------------------------------------------|
| `$ARGUMENTS`           | All arguments passed. Appended automatically if missing. |
| `$ARGUMENTS[N]`        | Specific argument by 0-based index.                      |
| `$N`                   | Shorthand for `$ARGUMENTS[N]`.                           |
| `${CLAUDE_SESSION_ID}` | Current session ID.                                      |
| `${CLAUDE_SKILL_DIR}`  | Directory containing the command/skill file. Use to reference bundled scripts. |

## Dynamic Context Injection

Use `!<cmd>` (shell command wrapped in backticks, prefixed with `!`) to run shell commands before content is sent to Claude:

```yaml
---
name: pr-summary
description: Summarize current PR
context: fork
agent: Explore
---

PR diff: !`gh pr diff`
Changed files: !`gh pr diff --name-only`

Summarize this pull request.
```

The shell output replaces the placeholder. Claude sees the rendered result, not the command.

## Invocation Control Matrix

| Frontmatter                      | User invokes | Claude invokes | Context loading                              |
|----------------------------------|--------------|----------------|----------------------------------------------|
| (default)                        | Yes          | Yes            | Description always, full content when invoked |
| `disable-model-invocation: true` | Yes          | No             | Not in context, loads when user invokes       |
| `user-invocable: false`          | No           | Yes            | Description always, full content when invoked |

## Differences: Commands vs Skills

| Feature            | Commands (`.claude/commands/`) | Skills (`.claude/skills/`)  |
|--------------------|-------------------------------|-----------------------------|
| Format             | Single `.md` file             | Directory with `SKILL.md`   |
| Supporting files   | No                            | Yes (references, scripts)   |
| Namespace in plugin| Same                          | Same                        |
| Priority           | Lower (skill wins on conflict)| Higher                      |

**Recommendation:** Use skills for new work. Commands remain supported for backwards compatibility.
