---
name: creating-agents
description: Creates Claude Code custom subagents (.claude/agents/) with system prompts, tool restrictions, permission modes, hooks, memory, and MCP integration. Use when the user wants to create a new agent, subagent, or specialized AI assistant.
disable-model-invocation: true
argument-hint: [agent-name] [description]
---

# Creating Claude Code Subagents

Create custom subagents following the official Claude Code specification. Subagents are specialized AI assistants with their own context window, system prompt, tool access, and permissions.

## Workflow

1. **Gather requirements** — ask the user:
   - Agent name (lowercase, hyphens)
   - What the agent specializes in
   - Whether it should be proactively invoked by Claude or only on request
   - Which tools it needs (read-only? full access? specific tools?)
   - Model preference (haiku for speed, sonnet for balance, opus for power)
   - Scope: personal (`~/.claude/agents/`) or project (`.claude/agents/`)
   - Whether it needs persistent memory, hooks, or MCP servers

2. **Design the agent** using the reference and patterns below

3. **Generate the agent file** using the template

4. **Validate** against the checklist

## Quick Reference

For all frontmatter fields and configuration, see [agent-reference.md](references/agent-reference.md).
For the starter template, see [AGENT-TEMPLATE.md](templates/AGENT-TEMPLATE.md).

## Agent File Format

Agents are Markdown files with YAML frontmatter. The body becomes the system prompt.

```yaml
---
name: my-agent
description: What this agent does. Use proactively when X happens.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a specialist in X. When invoked:
1. Do this
2. Then this
3. Report findings
```

## Placement Rules

| Scope   | Path                    | Available in      | Priority |
|---------|-------------------------|-------------------|----------|
| CLI     | `--agents` JSON flag    | Current session   | Highest  |
| Project | `.claude/agents/`       | This project      | 2        |
| User    | `~/.claude/agents/`     | All projects      | 3        |
| Plugin  | `<plugin>/agents/`      | Where enabled     | Lowest   |

## Design Patterns

### Read-Only Reviewer
```yaml
tools: Read, Grep, Glob, Bash
model: sonnet
```
Good for: code review, security audit, codebase exploration.

### Full-Access Worker
```yaml
tools: Read, Edit, Write, Bash, Grep, Glob
model: inherit
```
Good for: bug fixing, implementation, refactoring.

### Research Agent
```yaml
tools: Read, Grep, Glob, Bash, WebSearch, WebFetch
model: haiku
```
Good for: documentation lookup, codebase understanding.

### Agent with Persistent Memory
```yaml
memory: user
```
Gives the agent a `MEMORY.md` file that persists across sessions.

## Proactive vs On-Request

- Include "use proactively" in `description` for agents Claude should auto-delegate to
- Omit for agents that should only run when explicitly requested

## Validation Checklist

- [ ] Name: lowercase, hyphens only
- [ ] Description: clear about WHEN to delegate to this agent
- [ ] Tools: minimal set needed (principle of least privilege)
- [ ] Model: appropriate for task complexity
- [ ] System prompt: focused on ONE specialization
- [ ] System prompt: includes clear workflow steps
- [ ] No nested subagent spawning (subagents can't spawn subagents)
