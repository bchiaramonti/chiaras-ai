# Subagent Reference

## Frontmatter Fields

Only `name` and `description` are required.

| Field             | Required | Description                                                                           |
|-------------------|----------|---------------------------------------------------------------------------------------|
| `name`            | Yes      | Unique identifier. Lowercase letters and hyphens.                                     |
| `description`     | Yes      | When Claude should delegate to this agent. Include "use proactively" if auto-invoke.  |
| `tools`           | No       | Allowed tools. Inherits all if omitted.                                               |
| `disallowedTools` | No       | Tools to deny. Removed from inherited/specified list.                                 |
| `model`           | No       | `sonnet`, `opus`, `haiku`, `inherit`, or full model ID (e.g., `claude-opus-4-6`). Default: `inherit`. |
| `effort`          | No       | Effort level when active. Overrides session level. Options: `low`, `medium`, `high`, `max` (Opus 4.6 only). |
| `initialPrompt`   | No       | Auto-submitted as first user turn when running as main agent (`--agent`). Commands and skills processed. |
| `permissionMode`  | No       | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan`.                     |
| `maxTurns`        | No       | Maximum agentic turns before stopping.                                                |
| `skills`          | No       | Skills to preload into context at startup. Full content injected, not just available.  |
| `mcpServers`      | No       | MCP servers: name reference or inline definition.                                     |
| `hooks`           | No       | Lifecycle hooks scoped to this agent.                                                 |
| `memory`          | No       | Persistent memory: `user`, `project`, or `local`.                                     |
| `background`      | No       | `true` = always runs as background task. Default: `false`.                            |
| `isolation`       | No       | `worktree` = runs in temporary git worktree.                                          |

## Available Tools

Subagents can use any Claude Code internal tool:

**Read-only:** `Read`, `Grep`, `Glob`
**Write:** `Write`, `Edit`, `NotebookEdit`
**Execution:** `Bash`
**Web:** `WebSearch`, `WebFetch`
**Meta:** `Agent(agent_type)`, `Skill`, `TodoWrite`, `AskUserQuestion`

Use `Agent(worker, researcher)` in `tools` to restrict which subagents can be spawned.

## Permission Modes

| Mode                | Behavior                                           |
|---------------------|----------------------------------------------------|
| `default`           | Standard permission prompts                        |
| `acceptEdits`       | Auto-accept file edits                             |
| `dontAsk`           | Auto-deny prompts (explicitly allowed tools work)  |
| `bypassPermissions` | Skip all checks (use with caution)                 |
| `plan`              | Read-only exploration mode                         |

## Persistent Memory

| Scope     | Location                                      | Use when                          |
|-----------|-----------------------------------------------|-----------------------------------|
| `user`    | `~/.claude/agent-memory/<name>/`              | Learnings across all projects     |
| `project` | `.claude/agent-memory/<name>/`                | Project-specific, shareable       |
| `local`   | `.claude/agent-memory-local/<name>/`          | Project-specific, not committed   |

When enabled:
- System prompt includes memory read/write instructions
- First 200 lines of `MEMORY.md` injected at startup
- Read, Write, Edit tools auto-enabled

## Hooks in Subagents

### In frontmatter (runs while agent is active)

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/lint.sh"
```

### In settings.json (project-level lifecycle events)

```json
{
  "hooks": {
    "SubagentStart": [{ "matcher": "db-agent", "hooks": [{"type": "command", "command": "./setup.sh"}] }],
    "SubagentStop": [{ "hooks": [{"type": "command", "command": "./cleanup.sh"}] }]
  }
}
```

## Built-in Subagents

| Agent              | Model   | Tools     | Purpose                              |
|--------------------|---------|-----------|--------------------------------------|
| Explore            | Haiku   | Read-only | Fast codebase search/analysis        |
| Plan               | Inherit | Read-only | Research for plan mode               |
| general-purpose    | Inherit | All       | Complex multi-step tasks             |
| Bash               | Inherit | Bash      | Running terminal commands separately |
| statusline-setup   | Sonnet  | Read/Edit | Configuring status line (`/statusline`) |
| Claude Code Guide  | Haiku   | Read-only | Answering Claude Code feature questions |

## Disabling Subagents

In permissions settings:
```json
{ "permissions": { "deny": ["Agent(Explore)", "Agent(my-agent)"] } }
```

Or via CLI: `claude --disallowedTools "Agent(Explore)"`

## Managing Subagents

### `/agents` command
Interactive interface to view, create, edit, and delete subagents. Create via guided setup or Claude generation. Available scopes: user-level or project-level.

### `claude agents` CLI
List all configured subagents from command line (non-interactive).

### `--agents` CLI flag
Pass JSON subagent definitions for a single session:
```bash
claude --agents '{"reviewer": {"description": "Code reviewer", "prompt": "...", "tools": ["Read"], "model": "sonnet"}}'
```
JSON accepts same fields as frontmatter: `description`, `prompt`, `tools`, `disallowedTools`, `model`, `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, `initialPrompt`, `memory`, `effort`, `background`, `isolation`.

### Running as main session agent

Use `--agent <name>` to start a session where the main thread uses that agent's system prompt, tool restrictions, and model:
```bash
claude --agent code-reviewer
```

Make it the default via `.claude/settings.json`: `{"agent": "code-reviewer"}`. CLI flag overrides setting.

### Invoking via @-mention

Type `@` and select the agent from typeahead. Plugin agents: `@agent-<plugin>:<name>`. This guarantees the specific agent runs for one task.

### Model resolution order

1. `CLAUDE_CODE_SUBAGENT_MODEL` env var (if set)
2. Per-invocation `model` parameter
3. Agent definition's `model` frontmatter
4. Main conversation's model

### Resuming subagents
Each invocation returns an agent ID. Resume with full context preserved by passing the ID. Transcripts stored at `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl`.

### Backgrounding
- Press **Ctrl+B** to background a running subagent
- Set `background: true` in frontmatter to always run in background
- Disable with `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` env var

### Auto-compaction
Subagents auto-compact at ~95% capacity. Override with `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` (e.g., `50`).

## Key Constraints

- Subagents **cannot spawn other subagents** (no nesting)
- Subagents receive only their system prompt + environment details, **not** the full Claude Code system prompt
- Background subagents auto-deny non-pre-approved permissions
- `context: fork` in skills creates temporary subagents
- Agents loaded at session start; restart or use `/agents` to reload
- **Task → Agent rename** (v2.1.63): The Task tool was renamed to Agent. `Task(...)` still works as alias.
- **`model` parameter on Agent tool**: Per-invocation model overrides restored in v2.1.72.

## Agent Teams (Experimental)

> Enable with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in settings.json or environment.

Agent teams coordinate multiple Claude Code instances working together. Unlike subagents (which run within one session), teammates are independent sessions with shared task lists and inter-agent messaging.

### Architecture

| Component     | Role                                              |
|---------------|---------------------------------------------------|
| **Team lead** | Main session that creates team and coordinates     |
| **Teammates** | Separate Claude Code instances on assigned tasks   |
| **Task list** | Shared work items teammates claim and complete     |
| **Mailbox**   | Messaging system between agents                    |

### Display modes

Set `teammateMode` in settings.json: `"auto"` (default), `"in-process"`, or `"tmux"`.

- **In-process**: All in one terminal. Shift+Down cycles teammates.
- **Split panes**: Each teammate in own pane (requires tmux or iTerm2).

### Best use cases

- Research and review (parallel investigation)
- New modules/features (each teammate owns separate piece)
- Debugging with competing hypotheses
- Cross-layer changes (frontend + backend + tests)

### When NOT to use

- Sequential tasks with many dependencies
- Same-file edits (risk of overwrites)
- Simple tasks (coordination overhead not worth it)
- Use subagents instead for focused tasks reporting back.

### Hooks for quality gates

- `TeammateIdle`: Exit code 2 sends feedback, keeps teammate working
- `TaskCompleted`: Exit code 2 prevents completion, sends feedback

### Key limitations

- No session resumption with in-process teammates
- One team per session
- No nested teams (teammates can't spawn teams)
- Lead is fixed for team lifetime
- Config stored at `~/.claude/teams/{team-name}/config.json`
