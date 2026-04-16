---
name: creating-hooks
description: Creates Claude Code hooks (event handlers) for automating workflows around tool events, session lifecycle, and agent coordination. Use when the user wants to add hooks, automate post-tool actions, enforce quality gates, or respond to Claude Code events.
disable-model-invocation: true
argument-hint: [hook-event] [description]
---

# Creating Claude Code Hooks

Create hooks following the official Claude Code specification. Hooks are event handlers that execute automatically at specific lifecycle points — validating commands, formatting code after edits, enforcing quality gates, or coordinating agent teams.

## Workflow

1. **Gather requirements** — ask the user:
   - What event should trigger the hook? (e.g., after file edits, before bash commands)
   - What action should happen? (shell command, HTTP call, LLM prompt, or agentic verification)
   - Should it match specific tools/agents? (matcher pattern)
   - Scope: project settings, plugin hooks, skill/agent frontmatter?
   - Should it block on failure (exit code 2) or just log?

2. **Choose hook type** based on the action complexity:
   - `command` — Shell script for deterministic validation (fastest, supports `async`, `if`, `once`, `statusMessage`)
   - `http` — POST JSON to an endpoint for external integrations (native type with `url`, `headers`, `allowedEnvVars`)
   - `prompt` — LLM evaluation for subjective quality checks (uses `prompt` field, not `command`)
   - `agent` — Agentic verifier with tools for complex multi-step verification

3. **Design the hook configuration** using the reference below

4. **Generate files**: hook config + any scripts

5. **Validate** against the checklist

## Quick Reference

For all hook events, types, input/output schemas, and patterns, see [hooks-reference.md](references/hooks-reference.md).

## Hook Configuration Format

### In settings.json or settings.local.json

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "./scripts/lint-file.sh"
          }
        ]
      }
    ]
  }
}
```

### In plugin hooks/hooks.json

Same format, but use `${CLAUDE_PLUGIN_ROOT}` for paths:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh"
        }]
      }
    ]
  }
}
```

### In skill/agent frontmatter

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh"
```

## Common Patterns

### Auto-format after edits
```json
{"matcher": "Write|Edit", "hooks": [{"type": "command", "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"}]}
```

### Block dangerous commands
```json
{"matcher": "Bash", "hooks": [{"type": "command", "command": "./scripts/block-destructive.sh"}]}
```
Script exits with code 2 to block + stderr message shown to Claude.

### Quality gate on task completion
```json
{"event": "TaskCompleted", "hooks": [{"type": "agent", "prompt": "review the completed work for quality"}]}
```

### HTTP webhook notification
```json
{"matcher": "Write|Edit", "hooks": [{"type": "http", "url": "http://localhost:8080/hooks/file-changed", "timeout": 10}]}
```

### Session startup with env vars
```json
{"event": "SessionStart", "hooks": [{"type": "command", "command": "echo 'export NODE_ENV=production' >> $CLAUDE_ENV_FILE"}]}
```

### Watch file changes
```json
{"event": "FileChanged", "matcher": ".envrc", "hooks": [{"type": "command", "command": "direnv allow"}]}
```

## Validation Checklist

- [ ] Event name: correct casing (e.g., `PostToolUse`, not `postToolUse`)
- [ ] Matcher: regex pattern matches intended tools/agents
- [ ] Scripts: executable (`chmod +x`)
- [ ] Scripts: shebang line present (`#!/bin/bash` or `#!/usr/bin/env bash`)
- [ ] Scripts: read JSON input from stdin (for command hooks)
- [ ] Exit codes: 0=allow, 1=error (logged), 2=block operation + stderr to Claude
- [ ] Plugin hooks: use `${CLAUDE_PLUGIN_ROOT}` for all paths
- [ ] No Windows-style paths
- [ ] Tested manually before deploying
