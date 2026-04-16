---
name: creating-plugins
description: Creates Claude Code plugins with proper plugin.json manifest, directory structure, skills, agents, hooks, MCP/LSP servers, and marketplace entries. Use when the user wants to create a new plugin, package skills for distribution, or set up a plugin marketplace.
disable-model-invocation: true
argument-hint: [plugin-name] [description]
---

# Creating Claude Code Plugins

Create plugins and plugin marketplaces following the official Claude Code specification. Plugins package skills, agents, hooks, MCP servers, and LSP servers for distribution across projects and teams.

## Workflow

1. **Gather requirements** — ask the user:
   - Plugin name (kebab-case, no spaces)
   - What the plugin does (description)
   - Which components it needs (skills, agents, hooks, MCP, LSP, output-styles, channels)
   - Whether it needs user configuration (`userConfig` for API keys, endpoints)
   - Whether it will be distributed via a marketplace
   - Target audience: personal, team, or community

2. **Design the plugin structure** based on components needed

3. **Generate the plugin files** using the reference and templates below

4. **If marketplace needed**: create or update the `marketplace.json`

5. **Validate** against the checklist

6. **Test locally**: `claude --plugin-dir ./plugin-name`

## Quick Reference

For the complete plugin.json schema and all component specs, see [plugin-reference.md](references/plugin-reference.md).
For marketplace.json schema and distribution, see [marketplace-reference.md](references/marketplace-reference.md).
For the starter template, see [PLUGIN-TEMPLATE/](templates/).

## Plugin Directory Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json           # Manifest (only file inside .claude-plugin/)
├── skills/                   # Agent Skills (SKILL.md in subdirectories)
│   └── my-skill/
│       └── SKILL.md
├── agents/                   # Custom subagents (Markdown files)
│   └── my-agent.md
├── commands/                 # Legacy commands (simple .md files)
├── hooks/
│   └── hooks.json            # Event handlers
├── output-styles/            # Output style definitions
├── .mcp.json                 # MCP server configurations
├── .lsp.json                 # LSP server configurations
├── settings.json             # Default settings (only "agent" key supported)
├── README.md                 # Documentation
├── CHANGELOG.md              # Version history
└── LICENSE                   # License file
```

**Critical rule:** Only `plugin.json` goes inside `.claude-plugin/`. All other directories (skills/, agents/, hooks/, etc.) MUST be at the plugin root.

## Plugin Manifest (plugin.json)

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Brief plugin description",
  "author": { "name": "Author Name" },
  "homepage": "https://...",
  "repository": "https://...",
  "license": "MIT",
  "keywords": ["tag1", "tag2"]
}
```

`name` is the only required field. It becomes the namespace prefix for all components (e.g., `/my-plugin:skill-name`).

## Marketplace Entry

To add the plugin to a marketplace, add an entry to `.claude-plugin/marketplace.json`:

```json
{
  "name": "my-plugin",
  "source": "./my-plugin",
  "description": "What the plugin does",
  "version": "1.0.0",
  "author": { "name": "Author Name" },
  "category": "productivity",
  "keywords": ["tag1", "tag2"]
}
```

## Plugin Sources (for distribution)

| Source        | Format                                                   |
|---------------|----------------------------------------------------------|
| Relative path | `"source": "./plugins/my-plugin"`                        |
| GitHub        | `"source": {"source": "github", "repo": "owner/repo"}`  |
| Git URL       | `"source": {"source": "url", "url": "https://...git"}`  |
| npm           | `"source": {"source": "npm", "package": "@org/plugin"}`  |

## Environment Variable

Use `${CLAUDE_PLUGIN_ROOT}` in hooks and MCP configs to reference files within the plugin's installation directory. Plugins are copied to cache on install, so absolute paths won't work.

## Validation Checklist

### Plugin structure
- [ ] `plugin.json` is inside `.claude-plugin/` (not at root)
- [ ] All component directories (skills/, agents/, hooks/) are at plugin root
- [ ] `name` is kebab-case, no spaces
- [ ] `name` doesn't use reserved words (anthropic, claude)
- [ ] `version` follows semantic versioning (MAJOR.MINOR.PATCH)
- [ ] All paths are relative and start with `./`

### Components
- [ ] Each skill has `SKILL.md` with frontmatter
- [ ] Each agent has `name` and `description` in frontmatter
- [ ] Hook scripts are executable (`chmod +x`)
- [ ] Hook scripts use `${CLAUDE_PLUGIN_ROOT}` for paths
- [ ] MCP servers use `${CLAUDE_PLUGIN_ROOT}` for paths
- [ ] No files reference paths outside the plugin directory

### Marketplace
- [ ] `marketplace.json` has `name`, `owner`, `plugins` array
- [ ] Marketplace `name` doesn't use reserved names
- [ ] Each plugin entry has `name` and `source`
- [ ] No duplicate plugin names in the marketplace
- [ ] Version bumped when code changes (otherwise users won't get updates)

### Testing
- [ ] Tested with `claude --plugin-dir ./plugin-name`
- [ ] Skills appear with `/plugin-name:skill-name`
- [ ] Agents appear in `/agents`
- [ ] Hooks trigger on expected events
- [ ] Validated with `claude plugin validate .` or `/plugin validate .`
