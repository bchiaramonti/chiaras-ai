# Hooks Reference

## Contents
- Hook events
- Hook types
- Configuration schema
- Hook action fields
- Input/output format
- Exit codes
- JSON output format
- Matchers
- Hook placement
- Environment variables

## Hook Events

| Event                | Matcher input       | When it fires                                  | Can block? |
|----------------------|---------------------|------------------------------------------------|------------|
| `SessionStart`       | Source (`startup`, `resume`, `clear`, `compact`) | When session begins or resumes | No |
| `UserPromptSubmit`   | (none)              | When user submits a prompt                     | Yes        |
| `PreToolUse`         | Tool name           | Before a tool call executes                    | Yes        |
| `PermissionRequest`  | Tool name           | When a permission dialog appears               | Yes        |
| `PostToolUse`        | Tool name           | After a tool call succeeds                     | No         |
| `PostToolUseFailure` | Tool name           | After a tool call fails                        | No         |
| `Notification`       | Type (`permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`) | When Claude Code sends a notification | No |
| `SubagentStart`      | Agent type name     | When a subagent begins execution               | No         |
| `SubagentStop`       | Agent type name     | When a subagent finishes                       | Yes        |
| `Stop`               | (none)              | When Claude finishes responding                | Yes        |
| `StopFailure`        | Error type (`rate_limit`, `authentication_failed`, `billing_error`, `invalid_request`, `server_error`, `max_output_tokens`, `unknown`) | When turn ends due to API error | No |
| `TaskCreated`        | (none)              | When a task is being created via TaskCreate    | Yes        |
| `TaskCompleted`      | (none)              | When a task is being marked as completed       | Yes        |
| `TeammateIdle`       | (none)              | When agent team teammate about to go idle      | Yes        |
| `InstructionsLoaded` | Load reason (`session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact`) | When CLAUDE.md or rules loaded | No |
| `ConfigChange`       | Config source (`user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills`) | When config file changes | Yes |
| `CwdChanged`         | (none)              | When working directory changes (e.g., `cd`)    | No         |
| `FileChanged`        | Filename (basename)  | When a watched file changes on disk            | No         |
| `WorktreeCreate`     | (none)              | When worktree created via `--worktree` or `isolation: "worktree"` | Yes (prints path) |
| `WorktreeRemove`     | (none)              | When worktree removed at session exit          | No         |
| `PreCompact`         | Trigger (`manual`, `auto`) | Before context compaction              | No         |
| `PostCompact`        | Trigger (`manual`, `auto`) | After context compaction completes     | No         |
| `Elicitation`        | MCP server name     | When MCP server requests user input            | Yes        |
| `ElicitationResult`  | MCP server name     | After user responds to MCP elicitation         | Yes        |
| `SessionEnd`         | End reason (`clear`, `resume`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other`) | When session terminates | No |

## Hook Types

### `command` — Shell command
Fastest option. Input as JSON via stdin. Use for deterministic validation.

```json
{
  "type": "command",
  "command": "./scripts/validate.sh",
  "timeout": 600,
  "shell": "bash",
  "async": false,
  "statusMessage": "Validating...",
  "if": "Bash(git *)",
  "once": false
}
```

### `http` — HTTP POST
Send event JSON as POST request to a URL. Native hook type (not curl workaround).

```json
{
  "type": "http",
  "url": "http://localhost:8080/hooks/pre-tool-use",
  "timeout": 30,
  "headers": {
    "Authorization": "Bearer $MY_TOKEN"
  },
  "allowedEnvVars": ["MY_TOKEN"]
}
```

Response: 2xx with empty body = success. 2xx with plain text = context added. 2xx with JSON = parsed using standard output schema. Non-2xx = non-blocking error.

### `prompt` — LLM evaluation
Evaluates a prompt with a small model. Use `$ARGUMENTS` for hook input JSON context.

```json
{
  "type": "prompt",
  "prompt": "Should this command be allowed? Command: $ARGUMENTS",
  "model": "claude-opus-4-1-mini",
  "timeout": 30
}
```

### `agent` — Agentic verifier
Runs a subagent with tools for complex multi-step verification.

```json
{
  "type": "agent",
  "prompt": "verify the output meets quality standards by running tests",
  "model": "claude-opus-4-1-mini",
  "timeout": 60
}
```

## Configuration Schema

```json
{
  "hooks": {
    "<EventName>": [
      {
        "matcher": "<regex pattern>",
        "hooks": [
          {
            "type": "command|http|prompt|agent",
            "command": "<command string>",
            "url": "<http endpoint>"
          }
        ]
      }
    ]
  }
}
```

## Hook Action Fields

### Common fields (all types)

| Field           | Required | Description                                                                |
|-----------------|----------|----------------------------------------------------------------------------|
| `type`          | Yes      | Hook type: `command`, `http`, `prompt`, or `agent`                         |
| `timeout`       | No       | Seconds before canceling. Defaults: command=600, http=30, prompt=30, agent=60 |

### `command` type fields

| Field           | Required | Description                                                                |
|-----------------|----------|----------------------------------------------------------------------------|
| `command`       | Yes      | Shell command to execute. Receives JSON on stdin.                          |
| `async`         | No       | Run in background without blocking. Default: `false`.                      |
| `shell`         | No       | `bash` (default) or `powershell`.                                          |
| `statusMessage` | No       | Custom spinner message shown during execution.                             |
| `if`            | No       | Permission rule filter for fine-grained matching. Example: `Bash(git *)`.  |
| `once`          | No       | Run only once per session then removed. Skills/agents only. Default: `false`. |

### `http` type fields

| Field           | Required | Description                                                                |
|-----------------|----------|----------------------------------------------------------------------------|
| `url`           | Yes      | URL for POST request.                                                      |
| `headers`       | No       | HTTP headers. Supports `$ENV_VAR` interpolation.                           |
| `allowedEnvVars`| No       | List of env vars permitted in header interpolation.                        |

### `prompt` type fields

| Field           | Required | Description                                                                |
|-----------------|----------|----------------------------------------------------------------------------|
| `prompt`        | Yes      | Prompt text. Use `$ARGUMENTS` for hook input JSON.                         |
| `model`         | No       | Model for evaluation. Defaults to fast model.                              |

### `agent` type fields

| Field           | Required | Description                                                                |
|-----------------|----------|----------------------------------------------------------------------------|
| `prompt`        | Yes      | Task prompt for the agent.                                                 |
| `model`         | No       | Model for the agent. Defaults to configured model.                         |

## Common Hook Input Fields

All hook events receive these JSON fields on stdin (command) or POST body (http):

```json
{
  "session_id": "abc123",
  "transcript_path": "/home/user/.claude/projects/.../transcript.jsonl",
  "cwd": "/home/user/my-project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "agent_id": "optional-agent-id",
  "agent_type": "optional-agent-type"
}
```

### Tool event input (PreToolUse / PostToolUse / PostToolUseFailure)

```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.ts",
    "content": "..."
  },
  "tool_use_id": "toolu_01ABC123...",
  "tool_response": {"success": true},
  "error": "error message (PostToolUseFailure only)"
}
```

Use `jq` to extract fields:
```bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
```

## Exit Codes

| Code | Behavior                                                     |
|------|--------------------------------------------------------------|
| 0    | Success — stdout parsed for JSON output                      |
| 1    | Non-blocking error — stderr in verbose mode, continues       |
| 2    | **Block** — prevents the operation. Stderr fed back to Claude. |

### Exit code 2 behavior per event

| Event             | Exit code 2 effect                              |
|-------------------|-------------------------------------------------|
| `PreToolUse`      | Blocks the tool call; stderr becomes error msg   |
| `PermissionRequest`| Denies permission                               |
| `UserPromptSubmit`| Blocks prompt processing, erases prompt          |
| `Stop`            | Prevents Claude from stopping                    |
| `SubagentStop`    | Prevents subagent from stopping                  |
| `TeammateIdle`    | Sends feedback, keeps teammate working           |
| `TaskCreated`     | Prevents task creation                           |
| `TaskCompleted`   | Prevents task completion, sends feedback         |
| `ConfigChange`    | Blocks config change (except policy_settings)    |
| `Elicitation`     | Denies elicitation                               |
| `ElicitationResult`| Blocks response (becomes decline)               |
| `WorktreeCreate`  | Worktree creation fails                          |
| Other events      | Output/exit code ignored or logged only          |

## JSON Output Format

Return JSON on stdout with exit code 0 for structured control:

```json
{
  "continue": true,
  "stopReason": "message when continue=false",
  "suppressOutput": false,
  "systemMessage": "warning shown to user",
  "decision": "block",
  "reason": "explanation",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "explanation",
    "updatedInput": {"field": "new_value"},
    "additionalContext": "text added to context"
  }
}
```

### Key JSON output patterns

- **PreToolUse**: `permissionDecision` (`allow`/`deny`/`ask`), `updatedInput` to modify tool input before execution
- **PermissionRequest**: `decision.behavior` (`allow`/`deny`), `updatedInput`, `updatedPermissions`
- **UserPromptSubmit/Stop**: `decision: "block"` + `reason`
- **SessionStart**: `additionalContext` added to session context
- **WorktreeCreate**: Return path via stdout (command) or `hookSpecificOutput.worktreePath` (http)

## Matchers

Matchers use regex to filter when hooks fire:

```json
{"matcher": "Write|Edit"}           // File modification tools
{"matcher": "Bash"}                  // Shell commands only
{"matcher": "Agent"}                 // Any subagent invocation
{"matcher": "db-agent"}              // Specific subagent (SubagentStart/Stop)
{"matcher": "Write|Edit|NotebookEdit"}  // All write operations
{"matcher": "mcp__memory__.*"}       // All tools from MCP memory server
{"matcher": "startup"}              // SessionStart on first start only
{"matcher": "rate_limit"}           // StopFailure on rate limits only
{"matcher": ".envrc"}               // FileChanged for .envrc files
```

No matcher (or omitted) = fires for all instances of that event.

### MCP Tool naming pattern

MCP tools follow: `mcp__<server>__<tool>`. Match with: `mcp__memory__.*` (all memory tools) or `mcp__.*__write.*` (any write tool from any server).

## Hook Placement

| Location                    | Scope              | Best for                          |
|-----------------------------|--------------------|-----------------------------------|
| `~/.claude/settings.json`  | User (all projects)| Cross-project preferences         |
| `.claude/settings.json`    | Project (shared)   | Team-wide quality gates           |
| `.claude/settings.local.json` | Project (personal) | Personal workflow automation   |
| Managed policy settings     | Organization       | Enforced org-wide rules           |
| Plugin `hooks/hooks.json`   | Plugin             | Distributable automations         |
| Skill frontmatter `hooks:`  | Skill              | Skill-specific validation         |
| Agent frontmatter `hooks:`  | Agent              | Agent-specific constraints        |

### Skill/Agent frontmatter hooks

- `Stop` hooks in agent frontmatter are auto-converted to `SubagentStop`
- Hooks in frontmatter only fire while that skill/agent is active
- Cleaned up automatically when skill/agent finishes
- `once: true` runs the hook only once per session then removes it (skills only)

## Environment Variables

| Variable              | Description                                            |
|-----------------------|--------------------------------------------------------|
| `$CLAUDE_PROJECT_DIR` | Project root directory                                 |
| `$CLAUDE_ENV_FILE`    | Write `export` statements here in SessionStart/CwdChanged/FileChanged hooks to persist env vars |
| `$CLAUDE_CODE_REMOTE` | `"true"` in remote web environments                    |
| `${CLAUDE_PLUGIN_ROOT}` | Plugin root directory (in plugin hooks only)          |
| `${CLAUDE_PLUGIN_DATA}` | Plugin persistent data directory (survives updates)   |

### Setting environment variables via hooks

In `SessionStart`, `CwdChanged`, or `FileChanged` hooks, write to `$CLAUDE_ENV_FILE` to set environment variables:

```bash
#!/bin/bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
fi
exit 0
```

## Disabling Hooks

Remove individual hooks from settings JSON, or disable all:
```json
{ "disableAllHooks": true }
```

Managed hooks cannot be disabled at user/project level.

## `/hooks` Menu

Type `/hooks` to browse all configured hooks. Shows event counts, matcher details, handler info, and source (User, Project, Local, Plugin, Session, Built-in). Read-only interface.
