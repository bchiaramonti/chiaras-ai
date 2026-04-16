---
name: versioning-artifacts
description: Versions and releases Claude Code toolkit artifacts (marketplace, plugins, skills, agents, commands) within this plugin. Bumps versions in plugin.json and marketplace.json, generates changelogs, commits, and pushes changes. Use proactively after modifying any skill, agent, or reference file inside the claude-code-toolkit plugin.
argument-hint: [patch|minor|major] [commit-message]
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# Versioning Claude Code Artifacts

Version, commit, and push changes to Claude Code plugins and their components. Ensures all version numbers, changelogs, and marketplace entries stay in sync.

## Workflow

### Phase 1: Detect Changes

1. Run `git status` and `git diff` to identify modified files
2. Categorize changes by artifact type:
   - **marketplace.json** — marketplace-level changes
   - **plugin.json** — plugin metadata changes
   - **SKILL.md** / references / templates — skill changes
   - **agents/*.md** — agent changes
   - **commands/*.md** — command changes
   - **hooks/**, **.mcp.json**, **.lsp.json** — infrastructure changes

3. Identify which plugins were affected

### Phase 2: Determine Version Bump

Use the `$ARGUMENTS` input or infer from changes:

| Change type                          | Bump    |
|--------------------------------------|---------|
| Bug fix, typo, minor reference update | PATCH   |
| New skill, agent, or command          | MINOR   |
| Breaking change, renamed/removed component | MAJOR |

If `$ARGUMENTS` starts with `patch`, `minor`, or `major`, use that explicitly.

### Phase 3: Apply Version Bumps

For each affected plugin:

1. **Read current version** from `plugin.json`
2. **Bump version** according to semantic versioning rules
3. **Update `plugin.json`** with new version
4. **Update `marketplace.json`** entry with matching version (if applicable)
5. **Update/create CHANGELOG.md** in the plugin directory

### Phase 4: Generate Changelog Entry

Append to the plugin's `CHANGELOG.md`:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- [new features/components]

### Changed
- [modified features/behavior]

### Fixed
- [bug fixes/corrections]

### Removed
- [removed features/components]
```

### Phase 5: Commit and Push

1. **Stage** only the relevant files (not unrelated changes)
2. **Commit** with a descriptive message following the pattern:
   ```
   <type>(<scope>): <description>
   ```
   Types: `feat`, `fix`, `docs`, `refactor`, `chore`
   Scope: plugin name or `marketplace`

3. **Push** to the current branch

## Version Sync Rules

- If a plugin's `plugin.json` has `version`, it takes priority over marketplace entry
- For relative-path plugins in a marketplace, prefer setting version in marketplace.json
- **Always bump version when code changes** — users won't get updates without a version bump
- Keep `plugin.json` and `marketplace.json` versions in sync to avoid confusion

## Commit Message Patterns

For the version bump reference, see [versioning-reference.md](references/versioning-reference.md).

### Examples

```
feat(my-plugin): add code-review skill (v1.1.0)
fix(my-plugin): correct agent frontmatter validation (v1.0.1)
feat(marketplace): add new plugin my-tool (v1.2.0)
chore(my-plugin): bump version to 2.0.0
docs(my-plugin): update skill references with latest docs
```

## Validation Before Commit

- [ ] Version follows semantic versioning
- [ ] `plugin.json` and `marketplace.json` versions match (if both set)
- [ ] CHANGELOG.md updated with changes
- [ ] No unrelated files staged
- [ ] Commit message follows `type(scope): description` pattern
- [ ] Plugin validates: `claude plugin validate .`
