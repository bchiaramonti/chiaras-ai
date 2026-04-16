# Claude Code Toolkit

Meta-plugin for creating Claude Code commands, skills, agents, hooks, plugins, and marketplaces following official Anthropic best practices. Includes versioning/release automation and a self-improving research skill that keeps all reference material up-to-date.

## Skills

### `/claude-code-toolkit:creating-commands`
Creates Claude Code slash commands (`.claude/commands/`) with correct frontmatter, argument handling, and directory placement.

### `/claude-code-toolkit:creating-skills`
Creates Agent Skills with proper `SKILL.md`, progressive disclosure, references, templates, and scripts following Anthropic best practices.

### `/claude-code-toolkit:creating-agents`
Creates custom subagents (`.claude/agents/`) with system prompts, tool restrictions, permission modes, hooks, memory, and MCP integration.

### `/claude-code-toolkit:creating-hooks`
Creates hooks (event handlers) for automating workflows around tool events, session lifecycle, and agent coordination. Supports command, prompt, agent, and HTTP hook types across 15+ events.

### `/claude-code-toolkit:creating-plugins`
Creates plugins with `plugin.json` manifest, directory structure, marketplace entries, and all component types (skills, agents, hooks, MCP/LSP servers).

### `/claude-code-toolkit:versioning-artifacts`
Versions and releases Claude Code artifacts. Bumps versions in `plugin.json` and `marketplace.json`, generates changelogs, commits, and pushes changes.

### `/claude-code-toolkit:updating-toolkit`
Researches the latest Anthropic documentation and updates all five creation/versioning skills above. Makes the entire toolkit self-improving.

## Structure

```
claude-code-toolkit/
├── .claude-plugin/
│   └── plugin.json
├── README.md
└── skills/
    ├── creating-commands/
    │   ├── SKILL.md
    │   ├── references/
    │   │   └── command-reference.md
    │   └── templates/
    │       └── COMMAND-TEMPLATE.md
    ├── creating-skills/
    │   ├── SKILL.md
    │   ├── references/
    │   │   ├── skill-reference.md
    │   │   └── best-practices.md
    │   └── templates/
    │       └── SKILL-TEMPLATE.md
    ├── creating-agents/
    │   ├── SKILL.md
    │   ├── references/
    │   │   └── agent-reference.md
    │   └── templates/
    │       └── AGENT-TEMPLATE.md
    ├── creating-hooks/
    │   ├── SKILL.md
    │   └── references/
    │       └── hooks-reference.md
    ├── creating-plugins/
    │   ├── SKILL.md
    │   ├── references/
    │   │   ├── plugin-reference.md
    │   │   └── marketplace-reference.md
    │   └── templates/
    │       ├── plugin-json.template.json
    │       └── marketplace-entry.template.json
    ├── versioning-artifacts/
    │   ├── SKILL.md
    │   └── references/
    │       └── versioning-reference.md
    └── updating-toolkit/
        ├── SKILL.md
        └── references/
            └── sources.md
```

## Self-Improvement Cycle

Run `/claude-code-toolkit:updating-toolkit` periodically to:
1. Fetch the latest official Anthropic docs
2. Compare with current reference material across all 7 skills
3. Update references, templates, and checklists
4. Self-update its own source list and workflow
5. Report what changed
6. Suggest running `versioning-artifacts` to commit updates

Each run makes the toolkit more accurate and complete.

## Usage

```bash
# Test locally
claude --plugin-dir ./claude-code-toolkit

# Create a new command
/claude-code-toolkit:creating-commands

# Create a new skill
/claude-code-toolkit:creating-skills

# Create a new agent
/claude-code-toolkit:creating-agents

# Create a new plugin
/claude-code-toolkit:creating-plugins

# Version, commit, and push changes
/claude-code-toolkit:versioning-artifacts minor

# Update the toolkit with latest docs
/claude-code-toolkit:updating-toolkit
```
