---
name: updating-toolkit
description: Researches the latest Anthropic documentation on Claude Code skills, agents, commands, plugins, and marketplaces, then updates all skills in this toolkit. Use when the user wants to update the toolkit, check for documentation changes, or improve the toolkit's reference material.
disable-model-invocation: true
argument-hint: [focus-area]
allowed-tools: Read, Edit, Write, Bash, Grep, Glob, WebSearch, WebFetch
---

# Updating the Claude Code Toolkit

This skill makes the toolkit self-improving. It fetches the latest official Anthropic documentation, compares it with the current reference files, and applies updates to keep the toolkit accurate and current.

## Workflow

### Phase 1: Research Latest Documentation

Fetch the latest docs from these official sources in parallel:

1. **Skills docs**: `https://code.claude.com/docs/en/skills`
2. **Subagents docs**: `https://code.claude.com/docs/en/sub-agents`
3. **Plugins docs**: `https://code.claude.com/docs/en/plugins`
4. **Plugins reference**: `https://code.claude.com/docs/en/plugins-reference`
5. **Plugin marketplaces**: `https://code.claude.com/docs/en/plugin-marketplaces`
6. **Discover plugins**: `https://code.claude.com/docs/en/discover-plugins`
7. **Best practices**: `https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices`
8. **Agent Skills overview**: `https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview`
9. **Hooks docs**: `https://code.claude.com/docs/en/hooks`
10. **Agent teams**: `https://code.claude.com/docs/en/agent-teams`

Also run a web search for recent changes:
```
Anthropic Claude Code skills agents plugins documentation changes {current_year}
```

For additional sources and search queries, see [sources.md](references/sources.md).

If the user provided a `$ARGUMENTS` focus area, prioritize sources related to that area:
- `commands` → focus on skills/commands docs
- `skills` → focus on skills + best practices docs
- `agents` → focus on subagents + agent teams docs
- `hooks` → focus on hooks docs (reference + guide)
- `plugins` → focus on plugins + marketplace docs
- `versioning` → focus on plugins reference (version management section)
- `all` → fetch everything

### Phase 2: Compare with Current References

Read the current reference files across ALL skills in this toolkit:

**creating-commands:**
- `../creating-commands/SKILL.md`
- `../creating-commands/references/command-reference.md`
- `../creating-commands/templates/COMMAND-TEMPLATE.md`

**creating-skills:**
- `../creating-skills/SKILL.md`
- `../creating-skills/references/skill-reference.md`
- `../creating-skills/references/best-practices.md`
- `../creating-skills/templates/SKILL-TEMPLATE.md`

**creating-agents:**
- `../creating-agents/SKILL.md`
- `../creating-agents/references/agent-reference.md`
- `../creating-agents/templates/AGENT-TEMPLATE.md`

**creating-plugins:**
- `../creating-plugins/SKILL.md`
- `../creating-plugins/references/plugin-reference.md`
- `../creating-plugins/references/marketplace-reference.md`
- `../creating-plugins/templates/plugin-json.template.json`
- `../creating-plugins/templates/marketplace-entry.template.json`

**creating-hooks:**
- `../creating-hooks/SKILL.md`
- `../creating-hooks/references/hooks-reference.md`

**versioning-artifacts:**
- `../versioning-artifacts/SKILL.md`
- `../versioning-artifacts/references/versioning-reference.md`

For each file, identify:
- **New fields** added to frontmatter, schemas, or configuration
- **Deprecated fields** or changed defaults
- **New patterns** or recommended practices
- **Changed behavior** or updated specifications
- **New features** not yet documented in the toolkit
- **New hook events**, tool names, or model options

### Phase 3: Apply Updates

For each difference found:

1. **Update reference files** with new/changed information
2. **Update templates** if new fields or patterns emerged
3. **Update SKILL.md files** if workflow steps changed
4. **Update checklists** if new validation rules discovered
5. **Preserve existing structure** — don't reorganize, only update content

### Phase 4: Self-Update

Check if this skill itself needs updates:
- New documentation URLs → add to Phase 1 list and to `sources.md`
- New skills added to toolkit → add their files to Phase 2 comparison list
- New artifact types in Claude Code → suggest new skills for the toolkit

### Phase 5: Report Changes

After updating, produce a summary report:

```markdown
## Toolkit Update Report

### Sources checked
- [list of URLs fetched with dates]

### Changes applied
- **creating-commands**: [list of changes or "no changes needed"]
- **creating-skills**: [list of changes or "no changes needed"]
- **creating-agents**: [list of changes or "no changes needed"]
- **creating-hooks**: [list of changes or "no changes needed"]
- **creating-plugins**: [list of changes or "no changes needed"]
- **versioning-artifacts**: [list of changes or "no changes needed"]
- **updating-toolkit**: [list of self-updates or "no changes needed"]

### New features discovered
- [any new Claude Code features not yet covered]

### Recommendations
- [suggestions for new skills, improvements, or structural changes]
```

### Phase 6: Version and Commit (optional)

If changes were applied, suggest running the `versioning-artifacts` skill:
```
/claude-code-toolkit:versioning-artifacts patch docs: update toolkit references with latest docs
```

## Important Rules

- **Never remove information** unless it's confirmed deprecated in official docs
- **Always preserve the current structure** — add to it, don't reorganize
- **Mark uncertain changes** with `<!-- TODO: verify -->` comments
- **Update the sources.md** file with the date of last check
- **Keep reference files under their size limits** — if growing too large, suggest splitting
- **Cross-reference between skills** — if a new feature affects multiple skills, update all of them

## Self-Improvement Cycle

This skill can update itself and the entire toolkit. If the research reveals:
- New official documentation URLs → update `sources.md` and Phase 1 list
- New toolkit patterns → update this SKILL.md's workflow
- New validation rules → update the checklists in sibling skills
- New artifact types → recommend creating new skills
- New frontmatter fields → update all relevant reference files

This creates a positive feedback loop: each run makes the next run more effective.
