---
name: creating-skills
description: Creates Claude Code Agent Skills with proper SKILL.md, progressive disclosure, references, templates, and scripts. Use when the user wants to create a new skill, extend Claude's capabilities, or build a reusable workflow.
disable-model-invocation: true
argument-hint: [skill-name] [description]
---

# Creating Claude Code Skills

Create Agent Skills following the official specification and Anthropic best practices. Skills are directories with a `SKILL.md` entrypoint that teach Claude how to perform specific tasks repeatably.

## Workflow

1. **Gather requirements** — ask the user:
   - Skill name (gerund form preferred: `generating-reports`, `reviewing-code`)
   - What the skill does and when Claude should use it
   - Whether user-invoked (`/skill-name`), model-invoked (automatic), or both
   - Scope: personal, project, or plugin
   - Whether it needs supporting files (references, templates, scripts)

2. **Design the skill architecture** using progressive disclosure:
   - Keep `SKILL.md` under 500 lines (overview + navigation)
   - Move detailed reference material to separate files
   - Bundle scripts for deterministic operations
   - Keep references max 1 level deep from SKILL.md

3. **Generate files** using the templates and reference below

4. **Validate** against the quality checklist

5. **Test recommendations**: suggest the Claude A/B method for iteration

## Quick Reference

For complete frontmatter fields and configuration, see [skill-reference.md](references/skill-reference.md).
For authoring best practices, see [best-practices.md](references/best-practices.md).
For a starter template, see [SKILL-TEMPLATE.md](templates/SKILL-TEMPLATE.md).

## Skill Directory Structure

```
my-skill/
├── SKILL.md              # Main instructions (required, <500 lines)
├── references/           # Detailed docs (loaded on demand)
│   ├── api-reference.md
│   └── rules.md
├── templates/            # Output templates for Claude to fill
│   └── OUTPUT-TEMPLATE.md
├── examples/             # Example outputs showing format
│   └── sample-output.md
└── scripts/              # Executable utilities (run, not loaded)
    ├── validate.py
    └── generate.sh
```

## SKILL.md Skeleton

```yaml
---
name: my-skill-name
description: Does X when Y. Use when the user asks about Z or needs to accomplish W.
---

# Skill Title

Brief overview of what this skill does.

## Quick start

Minimal example to get started.

## Workflow

Step-by-step instructions.

## Additional resources

- For detailed API docs, see [api-reference.md](references/api-reference.md)
- For examples, see [examples/](examples/)
```

## Naming Convention

Use **gerund form** (verb + -ing):
- `generating-reports` (not `report-generator`)
- `reviewing-code` (not `code-review`)
- `processing-pdfs` (not `pdf-tools`)

## Description Guidelines

- Always write in **third person**
- Include **what it does** AND **when to use it**
- Include key terms users would naturally say
- Max 1024 characters

**Good:** `"Generates executive status reports from ROADMAP.md and SPRINT files. Use when the user needs project updates, sprint summaries, or stakeholder presentations."`

**Bad:** `"I help you with reports"` or `"Report helper"`

## Validation Checklist

- [ ] Name: lowercase, numbers, hyphens only (max 64 chars)
- [ ] Name: gerund form preferred
- [ ] Name: no reserved words ("anthropic", "claude")
- [ ] Description: third person, specific, includes trigger keywords
- [ ] SKILL.md: under 500 lines
- [ ] Progressive disclosure: details in separate reference files
- [ ] References: max 1 level deep from SKILL.md
- [ ] Long reference files: have table of contents
- [ ] Scripts: handle errors explicitly (don't punt to Claude)
- [ ] Scripts: no magic numbers (all values documented)
- [ ] Templates: match strictness to task fragility
- [ ] Feedback loops: validation steps for critical operations
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
- [ ] Unix-style paths only (forward slashes)
