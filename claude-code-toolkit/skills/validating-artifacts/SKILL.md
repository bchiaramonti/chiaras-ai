---
name: validating-artifacts
description: >-
  Validates Claude Code artifacts (skills, agents, commands, hooks, plugins)
  against best practices and official specifications. Use when the user wants
  to check, validate, audit, review, or lint an artifact before publishing
  or committing.

  <example>
  Context: user just created a new skill
  user: "validate this skill"
  assistant: reads the skill, applies validation rules, produces graded report
  </example>
argument-hint: [path-to-artifact]
---

# Validating Claude Code Artifacts

Validate any artifact against official specifications and best practices.
Produces a structured report with pass/fail/warning for each rule and an overall grade (A–D).

## Workflow

### Phase 1: Detect Artifact Type

Given `$ARGUMENTS` (a path), determine the artifact type using these signals:

| Signal | Type |
|--------|------|
| Directory contains `SKILL.md` | **skill** |
| `.md` file inside `agents/` or frontmatter has `tools`/`permissionMode`/`maxTurns` | **agent** |
| `.md` file inside `commands/` (no SKILL.md sibling) | **command** |
| JSON with hook event keys (`PreToolUse`, `PostToolUse`, etc.) or hooks array in settings | **hook** |
| Directory contains `.claude-plugin/plugin.json` | **plugin** |
| JSON file with `plugins` array and `owner` field | **marketplace** |

If the path is ambiguous, check multiple signals. If no `$ARGUMENTS` provided, ask the user for a path.

### Phase 2: Load Artifact Content

1. Read the target file(s)
2. Parse YAML frontmatter (between `---` markers) if present
3. For plugins: inventory all contained artifacts (skills, agents, hooks)
4. Note file counts, line counts, and directory structure

### Phase 3: Validate Against Rules

Load rules from [validation-rules.md](references/validation-rules.md).

Apply in order:
1. **Universal rules** (U1–U9) — apply to all artifact types
2. **Type-specific rules** — only the section matching the detected type

For each rule, determine:
- **PASS** — rule is satisfied
- **FAIL** — rule is violated (must fix)
- **WARNING** — technically met but could be improved
- **SKIP** — rule does not apply (e.g., no scripts to check S7)

### Phase 4: Cross-Reference Source Specs

For any FAIL or WARNING, load the relevant source reference to provide specific fix guidance. Source references are in sibling creation skills:

| Type | Source references |
|------|-----------------|
| skill | `../creating-skills/references/skill-reference.md`, `../creating-skills/references/best-practices.md` |
| agent | `../creating-agents/references/agent-reference.md` |
| command | `../creating-commands/references/command-reference.md` |
| hook | `../creating-hooks/references/hooks-reference.md` |
| plugin | `../creating-plugins/references/plugin-reference.md` |
| marketplace | `../creating-plugins/references/marketplace-reference.md` |

Only load a reference when needed — do not preload all references.

### Phase 5: Generate Report

Output the report in this format:

```markdown
## Validation Report

**Artifact:** `{path}`
**Type:** {detected type}
**Date:** {current date}

### Universal Rules

| # | Rule | Result | Notes |
|---|------|--------|-------|
| U1 | Name: lowercase, hyphens, max 64 chars | ✅ PASS | |
| U4 | Description: includes what + when | ❌ FAIL | Missing "when to use" clause |
| ... | ... | ... | ... |

### {Type}-Specific Rules

| # | Rule | Result | Notes |
|---|------|--------|-------|
| S1 | Name uses gerund form | ⚠️ WARNING | "report-generator" → consider "generating-reports" |
| ... | ... | ... | ... |

### Summary

| Category | ✅ Pass | ❌ Fail | ⚠️ Warning | ⏭️ Skip |
|----------|---------|---------|------------|---------|
| Universal | X | X | X | X |
| {Type}-specific | X | X | X | X |
| **Total** | **X** | **X** | **X** | **X** |

**Grade: {A|B|C|D}**

### Fixes Required

1. **{Rule ID}**: {what is wrong} — **Fix:** {specific action}.
   See: `../creating-{type}/references/{file}.md`, section "{section name}"

### Improvements Suggested

1. **{Rule ID}**: {what could be better} — **Consider:** {suggestion}.
```

## Recursive Plugin Validation

When validating a **plugin** directory:

1. Validate the plugin itself (P1–P10 rules)
2. Validate each skill in `skills/*/SKILL.md`
3. Validate each agent in `agents/*.md`
4. Validate hook configs if present
5. Check marketplace entry sync if marketplace.json exists nearby

Produce a **per-artifact mini-report** (type, grade, fail count), then a **plugin rollup**:

```markdown
### Plugin Rollup: {plugin-name}

| Artifact | Type | Grade | Fails | Warnings |
|----------|------|-------|-------|----------|
| plugin root | plugin | B | 0 | 2 |
| skills/creating-agents | skill | A | 0 | 0 |
| agents/scope-shaper.md | agent | C | 1 | 1 |
| ... | ... | ... | ... | ... |

**Overall Plugin Grade: {worst grade among all artifacts}**
```

## Important

- Do NOT duplicate rule definitions — always reference [validation-rules.md](references/validation-rules.md) as the checklist
- Do NOT fabricate rules that aren't in the validation-rules reference
- When a rule requires reading file contents (e.g., checking line count, parsing frontmatter), actually read the file — do not guess
- For hook validation, check executable permissions with `ls -la`
- Grade honestly — an artifact with issues should get C or D, not be inflated
