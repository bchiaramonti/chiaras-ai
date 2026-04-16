# Versioning Reference

## Semantic Versioning

Format: `MAJOR.MINOR.PATCH`

| Component | When to bump | Examples |
|-----------|-------------|----------|
| MAJOR     | Breaking changes, removed components, incompatible API changes | Renamed skill, changed required args, removed agent |
| MINOR     | New features, new components, backward-compatible additions | New skill, new agent, new hook, new MCP server |
| PATCH     | Bug fixes, typo corrections, documentation updates | Fixed reference, corrected template, updated checklist |

Pre-release: `2.0.0-beta.1`, `1.5.0-rc.2`

### Version Bump Decision Tree

```
Is a component removed or renamed?
  → YES → MAJOR
  → NO  → Is a new component added?
            → YES → MINOR
            → NO  → PATCH
```

## Artifact Types and Files to Update

### When a skill changes

Files to update:
- `skills/<name>/SKILL.md` — the skill itself
- `<plugin>/.claude-plugin/plugin.json` — bump plugin version
- `<marketplace>/.claude-plugin/marketplace.json` — bump marketplace plugin entry version
- `<plugin>/CHANGELOG.md` — document the change

### When an agent changes

Files to update:
- `agents/<name>.md` — the agent itself
- `<plugin>/.claude-plugin/plugin.json` — bump plugin version
- `<marketplace>/.claude-plugin/marketplace.json` — bump marketplace plugin entry version
- `<plugin>/CHANGELOG.md` — document the change

### When a command changes

Files to update:
- `commands/<name>.md` — the command itself
- `<plugin>/.claude-plugin/plugin.json` — bump plugin version
- `<marketplace>/.claude-plugin/marketplace.json` — bump marketplace plugin entry version
- `<plugin>/CHANGELOG.md` — document the change

### When hooks/MCP/LSP change

Files to update:
- `hooks/hooks.json` or `.mcp.json` or `.lsp.json` — the config
- `<plugin>/.claude-plugin/plugin.json` — bump plugin version
- `<marketplace>/.claude-plugin/marketplace.json` — bump marketplace plugin entry version
- `<plugin>/CHANGELOG.md` — document the change

### When only plugin.json metadata changes

Files to update:
- `<plugin>/.claude-plugin/plugin.json` — the change itself (no version bump needed for metadata-only)
- `<marketplace>/.claude-plugin/marketplace.json` — sync metadata

### When a new plugin is added to marketplace

Files to update:
- `<marketplace>/.claude-plugin/marketplace.json` — add plugin entry
- All plugin files — create from scratch

## Commit Message Convention

### Format
```
<type>(<scope>): <description>
```

### Types

| Type       | When to use                              |
|------------|------------------------------------------|
| `feat`     | New feature, skill, agent, or component  |
| `fix`      | Bug fix, correction                      |
| `docs`     | Documentation-only changes               |
| `refactor` | Restructuring without behavior change    |
| `chore`    | Version bumps, dependency updates        |
| `style`    | Formatting, whitespace                   |
| `test`     | Test additions or corrections            |

### Scopes

Use the plugin name as scope. For marketplace-level changes, use `marketplace`.

```
feat(apresentacoes): add audience-adapter agent (v2.1.0)
fix(design-system-m7): correct color token for M7-2026 (v2.2.1)
chore(marketplace): add claude-code-toolkit plugin
docs(normativos-m7): update normative-standards reference
```

## CHANGELOG.md Format

```markdown
# Changelog

All notable changes to this plugin will be documented in this file.

## [Unreleased]

## [1.1.0] - 2026-03-01

### Added
- New `reviewing-code` skill for automated code review

### Changed
- Updated `generating-reports` skill with new chart types

### Fixed
- Corrected template path in `creating-documents` skill

## [1.0.0] - 2026-02-15

### Added
- Initial release with 3 skills and 2 agents
```

## Git Workflow

1. `git status` — check what changed
2. `git diff` — review changes
3. `git add <specific-files>` — stage only relevant files
4. `git commit -m "type(scope): description"` — commit with conventional message
5. `git push -u origin <branch>` — push to remote

**Never** use `git add -A` or `git add .` — always stage specific files to avoid including secrets or unrelated changes.
