# Plugin Reference

## Contents
- Plugin manifest schema
- Component path fields
- Environment variables
- Plugin caching
- Version management
- Strict mode
- Hooks in plugins
- MCP servers in plugins
- LSP servers in plugins
- Settings in plugins
- CLI commands

## Plugin Manifest Schema (plugin.json)

Location: `.claude-plugin/plugin.json`

### Required Fields

| Field  | Type   | Description                               |
|--------|--------|-------------------------------------------|
| `name` | string | Unique identifier (kebab-case, no spaces) |

### Metadata Fields

| Field         | Type   | Description                  | Example                    |
|---------------|--------|------------------------------|----------------------------|
| `version`     | string | Semantic version             | `"2.1.0"`                  |
| `description` | string | Brief explanation             | `"Deployment tools"`       |
| `author`      | object | `{name, email?, url?}`      | `{"name": "Dev Team"}`     |
| `homepage`    | string | Documentation URL             | `"https://docs.example.com"` |
| `repository`  | string | Source code URL               | `"https://github.com/..."`  |
| `license`     | string | SPDX identifier              | `"MIT"`, `"Apache-2.0"`    |
| `keywords`    | array  | Discovery tags                | `["deploy", "ci-cd"]`      |

### Component Path Fields

Custom paths **replace** default directories for `commands`, `agents`, `skills`, and `outputStyles`. To keep the default and add more, include the default in the array: `"commands": ["./commands/", "./extras/deploy.md"]`. Hooks, MCP, and LSP servers have different merge semantics.

| Field          | Type                  | Default Location           |
|----------------|-----------------------|----------------------------|
| `commands`     | string\|array         | `commands/`                |
| `agents`       | string\|array         | `agents/`                  |
| `skills`       | string\|array         | `skills/`                  |
| `hooks`        | string\|array\|object | `hooks/hooks.json`         |
| `mcpServers`   | string\|array\|object | `.mcp.json`                |
| `lspServers`   | string\|array\|object | `.lsp.json`                |
| `outputStyles` | string\|array         | (none)                     |

### Environment Variables

`${CLAUDE_PLUGIN_ROOT}` — absolute path to plugin's installed directory. Changes on plugin update.

`${CLAUDE_PLUGIN_DATA}` — persistent directory for plugin state that survives updates. Use for installed dependencies (`node_modules`, venvs), generated code, caches. Auto-created on first reference. Location: `~/.claude/plugins/data/{id}/`. Deleted when plugin uninstalled from last scope (use `--keep-data` to preserve).

```json
{
  "hooks": {
    "PostToolUse": [{
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/lint.sh"
      }]
    }],
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "diff -q \"${CLAUDE_PLUGIN_ROOT}/package.json\" \"${CLAUDE_PLUGIN_DATA}/package.json\" >/dev/null 2>&1 || (cd \"${CLAUDE_PLUGIN_DATA}\" && cp \"${CLAUDE_PLUGIN_ROOT}/package.json\" . && npm install)"
      }]
    }]
  }
}
```

### User Configuration

The `userConfig` field declares values prompted at plugin enable time:

```json
{
  "userConfig": {
    "api_endpoint": { "description": "Your API endpoint", "sensitive": false },
    "api_token": { "description": "API auth token", "sensitive": true }
  }
}
```

Available as `${user_config.KEY}` in MCP/LSP configs, hook commands, and (non-sensitive only) skill/agent content. Also exported as `CLAUDE_PLUGIN_OPTION_<KEY>` env vars. Sensitive values go to system keychain.

### Channels

Declare message channels that inject content into conversations via an MCP server:

```json
{
  "channels": [
    {
      "server": "telegram",
      "userConfig": {
        "bot_token": { "description": "Telegram bot token", "sensitive": true }
      }
    }
  ]
}
```

`server` must match a key in the plugin's `mcpServers`.

## Plugin Caching

Marketplace plugins are copied to `~/.claude/plugins/cache`. Implications:
- Paths referencing files outside the plugin directory won't work
- Use symlinks for shared dependencies (honored during copy)
- Always use `${CLAUDE_PLUGIN_ROOT}` for paths in hooks/MCP

## Version Management

Format: `MAJOR.MINOR.PATCH` (semantic versioning)

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward-compatible)
- **PATCH**: Bug fixes

**Important:** If you change code but don't bump version, users won't get updates due to caching. If version is set in both `plugin.json` and `marketplace.json`, `plugin.json` wins silently.

**Recommendation:** For relative-path plugins in a marketplace, set version in marketplace.json. For all other sources, set it in plugin.json.

## Strict Mode

Set in marketplace entry's `strict` field:

| Value            | Behavior                                                          |
|------------------|-------------------------------------------------------------------|
| `true` (default) | `plugin.json` is authority. Marketplace can supplement.           |
| `false`          | Marketplace entry is entire definition. No `plugin.json` needed.  |

## Hooks in Plugins

Location: `hooks/hooks.json` or inline in `plugin.json`

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh"
      }]
    }]
  }
}
```

Available hook events: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PostToolUseFailure`, `Notification`, `SubagentStart`, `SubagentStop`, `TaskCreated`, `TaskCompleted`, `Stop`, `StopFailure`, `TeammateIdle`, `InstructionsLoaded`, `ConfigChange`, `CwdChanged`, `FileChanged`, `WorktreeCreate`, `WorktreeRemove`, `PreCompact`, `PostCompact`, `Elicitation`, `ElicitationResult`, `SessionEnd`

Hook types:
- `command` — Execute shell commands/scripts (input as JSON via stdin)
- `prompt` — Evaluate a prompt with an LLM (uses `$ARGUMENTS` for context)
- `agent` — Run an agentic verifier with tools for complex verification
- **HTTP hooks** — POST JSON to an endpoint (added v2.1.63)

Hook context includes `agent_id` and `agent_type` fields (added v2.1.69).

Hook input is passed as JSON via stdin for command hooks, or as POST body for HTTP hooks. Use `jq` to extract fields.

## MCP Servers in Plugins

Location: `.mcp.json` or inline in `plugin.json`

```json
{
  "mcpServers": {
    "my-server": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": { "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data" }
    }
  }
}
```

## LSP Servers in Plugins

Location: `.lsp.json` or inline in `plugin.json`

```json
{
  "my-lang": {
    "command": "lang-server",
    "args": ["serve"],
    "extensionToLanguage": { ".ext": "lang" }
  }
}
```

Required: `command`, `extensionToLanguage`. Optional: `args`, `transport`, `env`, `initializationOptions`, `settings`, `workspaceFolder`, `startupTimeout`, `shutdownTimeout`, `restartOnCrash`, `maxRestarts`.

**Note:** The language server binary must be installed separately.

## Settings in Plugins

Location: `settings.json` at plugin root. Only `agent` key is currently supported.

```json
{ "agent": "my-default-agent" }
```

Activates a plugin agent as the main thread when the plugin is enabled.

## CLI Commands

| Command                              | Description                    |
|--------------------------------------|--------------------------------|
| `claude plugin install <p> [-s scope]` | Install plugin               |
| `claude plugin uninstall <p> [-s scope] [--keep-data]`| Remove plugin (--keep-data preserves ${CLAUDE_PLUGIN_DATA}) |
| `claude plugin enable <p> [-s scope]`  | Enable disabled plugin       |
| `claude plugin disable <p> [-s scope]` | Disable without uninstalling |
| `claude plugin update <p> [-s scope]`  | Update to latest version     |
| `claude plugin validate .`            | Validate plugin/marketplace   |
| `/reload-plugins`                      | Activate plugin changes without restart (v2.1.69) |

Scopes: `user` (default), `project`, `local`, `managed`

## Official Marketplace Submission

Submit plugins to the official Anthropic marketplace via:
- **Claude.ai**: `claude.ai/settings/plugins/submit`
- **Console**: `platform.claude.com/plugins/submit`

Official plugin directory: `github.com/anthropics/claude-plugins-official`

## Installation Scopes

| Scope     | Settings file                     | Use case                          |
|-----------|-----------------------------------|-----------------------------------|
| `user`    | `~/.claude/settings.json`         | Personal, all projects (default)  |
| `project` | `.claude/settings.json`           | Team, via version control         |
| `local`   | `.claude/settings.local.json`     | Project-specific, gitignored      |
| `managed` | Managed settings                  | Admin-controlled (read-only)      |
