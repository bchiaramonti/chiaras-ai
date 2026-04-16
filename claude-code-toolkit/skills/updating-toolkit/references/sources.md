# Documentation Sources

Last updated: 2026-03-30

## Primary Sources (Official Anthropic Documentation)

### Claude Code Docs (code.claude.com)

| Topic              | URL                                                    | Priority | Covers skills |
|--------------------|--------------------------------------------------------|----------|---------------|
| Skills             | https://code.claude.com/docs/en/skills                 | High     | commands, skills |
| Subagents          | https://code.claude.com/docs/en/sub-agents             | High     | agents |
| Plugins            | https://code.claude.com/docs/en/plugins                | High     | plugins |
| Plugins reference  | https://code.claude.com/docs/en/plugins-reference      | High     | plugins, versioning |
| Plugin marketplaces| https://code.claude.com/docs/en/plugin-marketplaces    | High     | plugins |
| Discover plugins   | https://code.claude.com/docs/en/discover-plugins       | Medium   | plugins |
| Hooks reference    | https://code.claude.com/docs/en/hooks                  | Medium   | plugins, agents |
| Hooks guide        | https://code.claude.com/docs/en/hooks-guide            | Medium   | plugins, agents |
| Memory             | https://code.claude.com/docs/en/memory                 | Medium   | agents |
| Permissions        | https://code.claude.com/docs/en/permissions            | Medium   | skills, agents |
| MCP                | https://code.claude.com/docs/en/mcp                    | Medium   | plugins |
| Settings           | https://code.claude.com/docs/en/settings               | Low      | plugins |
| CLI reference      | https://code.claude.com/docs/en/cli-reference          | Low      | plugins, versioning |
| Agent teams        | https://code.claude.com/docs/en/agent-teams            | Medium   | agents |
| Full docs index    | https://code.claude.com/docs/llms.txt                  | Low      | all |

### Anthropic Platform Docs (platform.claude.com)

| Topic                | URL                                                                              | Priority | Covers skills |
|----------------------|----------------------------------------------------------------------------------|----------|---------------|
| Agent Skills overview| https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview       | High     | skills |
| Best practices       | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | High     | skills |
| Skills quickstart    | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/quickstart     | Medium   | skills |
| Skills API guide     | https://platform.claude.com/docs/en/build-with-claude/skills-guide               | Medium   | skills |
| Agent SDK skills     | https://platform.claude.com/docs/en/agent-sdk/skills                             | Medium   | skills |

## Secondary Sources (Community & Engineering Blog)

| Source                           | URL                                                                                  | Type        |
|----------------------------------|--------------------------------------------------------------------------------------|-------------|
| Anthropic Engineering Blog       | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | Blog     |
| Official Skills Repository       | https://github.com/anthropics/skills                                                 | Repository  |
| Official Plugins Directory       | https://github.com/anthropics/claude-plugins-official                                | Repository  |
| Claude Code CHANGELOG            | https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md                     | Changelog   |
| Claude Code Release Notes        | https://releasebot.io/updates/anthropic/claude-code                                  | Tracker     |
| Awesome Claude Code              | https://github.com/hesreallyhim/awesome-claude-code                                  | Community   |
| Agent Skills Standard            | https://agentskills.io                                                               | Specification|
| Claude Code Demo Plugins         | https://github.com/anthropics/claude-code/tree/main/plugins                          | Demo        |

## Web Search Queries for Updates

When researching, use these queries to find the latest information:

```
Anthropic Claude Code skills documentation {year}
Claude Code subagents custom agents configuration {year}
Claude Code plugins marketplace creation {year}
Claude Code plugin-marketplaces distribution {year}
Claude Code hooks lifecycle events {year}
Agent Skills SKILL.md best practices {year}
Claude Code slash commands frontmatter {year}
Claude Code plugin.json manifest schema {year}
Claude Code marketplace.json schema {year}
Claude Code semantic versioning plugins {year}
```

Replace `{year}` with the current year for the most relevant results.

## Update Log

| Date       | Scope              | Changes                                                    |
|------------|--------------------|------------------------------------------------------------|
| 2026-03-01 | Initial creation   | All reference files created from official docs             |
| 2026-03-01 | v2.0.0 expansion   | Added creating-plugins, versioning-artifacts, marketplace/plugin-marketplaces sources |
| 2026-03-10 | Skills 2.0 update  | Added ${CLAUDE_SKILL_DIR}, bundled skills, auto-discovery, context budget, Skills 2.0 categories, eval-driven dev, MCP tool refs, managing subagents section, Task→Agent rename, built-in agents expanded, hook types (prompt/agent/HTTP), InstructionsLoaded event, /reload-plugins, official marketplace submission, sources updated |
| 2026-03-30 | Major docs sync    | Skills: added `effort`, `paths`, `shell` frontmatter fields; fixed context budget (1%/8k). Commands: added `effort`, `paths`, `shell`, `${CLAUDE_SKILL_DIR}`. Agents: added `effort`, `initialPrompt`, full model IDs, `--agent` flag, @-mention, model resolution order. Hooks: added 12 new events (StopFailure, TaskCreated, ConfigChange, CwdChanged, FileChanged, WorktreeCreate/Remove, PostCompact, Elicitation/ElicitationResult, SessionEnd matchers), native `http` hook type, `async`/`if`/`once`/`statusMessage`/`shell` fields, JSON output format, `$CLAUDE_ENV_FILE`/`$CLAUDE_PROJECT_DIR`, detailed matchers per event. Plugins: added `userConfig`, `channels`, `${CLAUDE_PLUGIN_DATA}`, `output-styles/`, fixed component path behavior (replace not supplement), `--keep-data` flag. Marketplace: added `git-subdir` source, removed incorrect `pip` source, `pathPattern`/`hostPattern`, auto-update env vars, seed dirs, git timeout config. |
