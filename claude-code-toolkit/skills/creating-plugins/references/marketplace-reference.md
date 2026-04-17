# Marketplace Reference

## Contents
- Marketplace schema
- Plugin entries
- Plugin sources
- Distribution methods
- Team configuration
- Version resolution
- Release channels
- Validation

## Marketplace Schema (marketplace.json)

Location: `.claude-plugin/marketplace.json` at repository root.

### Required Fields

| Field     | Type   | Description                                   |
|-----------|--------|-----------------------------------------------|
| `name`    | string | Marketplace ID (kebab-case, no spaces)        |
| `owner`   | object | `{name: string, email?: string}`              |
| `plugins` | array  | List of plugin entries                         |

### Reserved Marketplace Names

Cannot use: `claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`, `anthropic-marketplace`, `anthropic-plugins`, `agent-skills`, `knowledge-work-plugins`, `life-sciences`. Names impersonating official marketplaces (like `official-claude-plugins`, `anthropic-tools-v2`) are also blocked.

### Optional Metadata

| Field                  | Type   | Description                                         |
|------------------------|--------|-----------------------------------------------------|
| `metadata.description` | string | Brief marketplace description                       |
| `metadata.version`     | string | Marketplace version                                 |
| `metadata.pluginRoot`  | string | Base dir prepended to relative plugin source paths  |

## Plugin Entries

### Required

| Field    | Type             | Description                            |
|----------|------------------|----------------------------------------|
| `name`   | string           | Plugin ID (kebab-case)                 |
| `source` | string \| object | Where to fetch the plugin              |

### Optional

| Field         | Type    | Description                                   |
|---------------|---------|-----------------------------------------------|
| `description` | string  | Brief plugin description                      |
| `version`     | string  | Plugin version                                |
| `author`      | object  | `{name, email?}`                              |
| `homepage`    | string  | Plugin docs URL                               |
| `repository`  | string  | Source code URL                               |
| `license`     | string  | SPDX identifier                               |
| `keywords`    | array   | Discovery tags                                |
| `category`    | string  | Plugin category                               |
| `tags`        | array   | Tags for searchability                        |
| `strict`      | boolean | `true` (default): plugin.json is authority    |
| `commands`    | string\|array  | Custom command paths                   |
| `agents`      | string\|array  | Custom agent paths                     |
| `hooks`       | string\|object | Hook config                            |
| `mcpServers`  | string\|object | MCP server config                      |
| `lspServers`  | string\|object | LSP server config                      |

## Plugin Sources

### Relative Path (same repo)
```json
{ "source": "./plugins/my-plugin" }
```
Only works with Git-based marketplaces (not URL-based).

### GitHub
```json
{
  "source": {
    "source": "github",
    "repo": "owner/repo",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4..."
  }
}
```

### Git URL
```json
{
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git",
    "ref": "main",
    "sha": "a1b2c3d4..."
  }
}
```

### Git Subdirectory
Sparse clone of a subdirectory within a git repo. Minimizes bandwidth for monorepos.
```json
{
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/acme-corp/monorepo.git",
    "path": "tools/claude-plugin",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4..."
  }
}
```
`url` accepts GitHub shorthand (`owner/repo`) or SSH URLs.

### npm
```json
{
  "source": {
    "source": "npm",
    "package": "@org/plugin",
    "version": "^2.0.0",
    "registry": "https://npm.example.com"
  }
}
```

## Distribution Methods

| Method          | Command                                          |
|-----------------|--------------------------------------------------|
| GitHub          | `/plugin marketplace add owner/repo`             |
| GitHub @ ref    | `/plugin marketplace add owner/repo@v2.0`        |
| Git URL         | `/plugin marketplace add https://gitlab.com/...` |
| Git URL # ref   | `/plugin marketplace add https://gitlab.com/...git#v1.0` |
| Local path      | `/plugin marketplace add ./my-marketplace`       |
| Remote URL      | `/plugin marketplace add https://example.com/marketplace.json` |

> **Marketplace source vs plugin source** — these pin independently. Marketplace sources support `ref` (branch/tag) but not `sha`. Plugin sources inside a marketplace entry support both `ref` and `sha`.

### CLI equivalents

`claude plugin marketplace` subcommands mirror the interactive `/plugin marketplace` commands:

```bash
claude plugin marketplace add <source> [--scope user|project|local] [--sparse <paths...>]
claude plugin marketplace list [--json]
claude plugin marketplace remove <name>        # alias: rm
claude plugin marketplace update [name]
```

- `--sparse`: limit checkout to specific subdirectories via git sparse-checkout (useful for monorepos, e.g., `--sparse .claude-plugin plugins`).
- `remove` also **uninstalls** any plugins installed from that marketplace. Use `update` to refresh without losing installed plugins.
- Seed-managed marketplaces are read-only: `remove` and `update` fail against them.

## Team Configuration

Add to `.claude/settings.json` for auto-prompting:

```json
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "github",
        "repo": "org/claude-plugins"
      }
    }
  },
  "enabledPlugins": {
    "tool-a@team-tools": true,
    "tool-b@team-tools": true
  }
}
```

## Managed Marketplace Restrictions

Admins can restrict which marketplaces users can add via `strictKnownMarketplaces` in managed settings:

| Value               | Behavior                                    |
|---------------------|---------------------------------------------|
| Undefined (default) | No restrictions                             |
| Empty array `[]`    | Complete lockdown                           |
| List of sources     | Only matching marketplaces allowed          |

Supports `hostPattern` (regex on host) and `pathPattern` (regex on filesystem path) for flexible matching:

```json
{
  "strictKnownMarketplaces": [
    {"source": "github", "repo": "acme-corp/approved-plugins"},
    {"source": "hostPattern", "hostPattern": "^github\\.example\\.com$"},
    {"source": "pathPattern", "pathPattern": "^/opt/approved/"}
  ]
}
```

## Release Channels

Create two marketplaces pointing to different refs of the same repo:

**Stable:** `"ref": "stable"` — assign to most users
**Latest:** `"ref": "latest"` — assign to early-access

The plugin's `plugin.json` must declare different `version` at each ref, otherwise updates are skipped.

## Private Repository Auth

For background auto-updates, set tokens in environment:

| Provider  | Environment Variables        |
|-----------|------------------------------|
| GitHub    | `GITHUB_TOKEN` or `GH_TOKEN` |
| GitLab    | `GITLAB_TOKEN` or `GL_TOKEN` |
| Bitbucket | `BITBUCKET_TOKEN`            |

## Auto-Updates

Toggle per-marketplace via `/plugin` > Marketplaces > Enable/Disable auto-update.

To disable all auto-updates: `DISABLE_AUTOUPDATER=true`. To keep plugin auto-updates while disabling CC auto-updates: `FORCE_AUTOUPDATE_PLUGINS=true` + `DISABLE_AUTOUPDATER=true`.

## Pre-Populating for Containers

Set `CLAUDE_CODE_PLUGIN_SEED_DIR` to a directory mirroring `~/.claude/plugins/` structure. Layer multiple: separate with `:` (Unix) or `;` (Windows). Seed is read-only; auto-updates disabled for seed marketplaces.

**Building a seed:** run Claude Code during image build with `CLAUDE_CODE_PLUGIN_CACHE_DIR=/opt/claude-seed` so plugins install directly into your seed path:

```bash
CLAUDE_CODE_PLUGIN_CACHE_DIR=/opt/claude-seed claude plugin marketplace add your-org/plugins
CLAUDE_CODE_PLUGIN_CACHE_DIR=/opt/claude-seed claude plugin install my-tool@your-plugins
# Then at runtime:
export CLAUDE_CODE_PLUGIN_SEED_DIR=/opt/claude-seed
```

**Seed semantics:** seed marketplaces **overwrite** any matching entries in the user's config on each startup. To opt out of a seed plugin, use `/plugin disable` (don't try to remove — that fails for seed-managed marketplaces).

## Offline / Flaky Network Behavior

By default, a failed `git pull` on a marketplace **wipes the cache and re-clones** — which fails again in offline environments, leaving plugins unavailable.

Set `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1` to retain the stale cache on pull failure and continue using the last-known-good state:

```bash
export CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1
```

For fully airgapped deployments, use `CLAUDE_CODE_PLUGIN_SEED_DIR` instead.

## Git Timeout

Default: 120s for all git operations. Override: `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS=300000` (5 min).

## Validation

```bash
claude plugin validate .        # CLI
/plugin validate .              # Interactive
```

Common errors:
- Missing `.claude-plugin/marketplace.json`
- Duplicate plugin names
- Path traversal (`..`) in source paths
- Invalid JSON syntax
- Plugin name not kebab-case (blocked by Claude.ai marketplace sync)
