---
name: creating-commands
description: Creates Claude Code slash commands (.claude/commands/) with correct frontmatter, argument handling, and directory placement. Use when the user wants to create a new slash command, custom command, or CLI command for Claude Code.
disable-model-invocation: true
argument-hint: [command-name] [description]
---

# Creating Claude Code Commands

Create slash commands following the official Claude Code specification. Commands are Markdown files with YAML frontmatter that users invoke with `/command-name`.

> **Note:** Custom commands have been merged into skills. A file at `.claude/commands/review.md` and a skill at `.claude/skills/review/SKILL.md` both create `/review`. Skills are recommended for new work — use this skill when the user specifically wants a simple command file.

## Workflow

1. **Gather requirements**: Ask the user for:
   - Command name (lowercase, hyphens only)
   - What the command should do
   - Whether it needs arguments
   - Scope: personal (`~/.claude/commands/`) or project (`.claude/commands/`)

2. **Generate the command file** using the template and reference below

3. **Validate** the generated file against the checklist

4. **Place the file** in the correct directory

## Quick Reference

For complete frontmatter fields and rules, see [command-reference.md](references/command-reference.md).
For the starter template, see [COMMAND-TEMPLATE.md](templates/COMMAND-TEMPLATE.md).

## Command File Format

```yaml
---
description: What this command does and when to use it
disable-model-invocation: true
allowed-tools: Read, Grep, Bash
argument-hint: [issue-number]
---

Your instructions here. Use $ARGUMENTS for user input.
Use $ARGUMENTS[0], $ARGUMENTS[1] or $0, $1 for positional args.
```

## Placement Rules

| Scope    | Path                              | Available in            |
|----------|-----------------------------------|-------------------------|
| Personal | `~/.claude/commands/<name>.md`    | All your projects       |
| Project  | `.claude/commands/<name>.md`      | This project only       |

## Validation Checklist

Before delivering, verify:
- [ ] Name uses only lowercase letters, numbers, and hyphens
- [ ] Name is max 64 characters
- [ ] Description is clear, specific, in third person
- [ ] `$ARGUMENTS` placeholder used if command accepts input
- [ ] `disable-model-invocation: true` set for commands with side effects
- [ ] File placed in correct scope directory
- [ ] No reserved words ("anthropic", "claude") in the name
