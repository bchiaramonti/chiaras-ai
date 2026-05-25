# Dev-Loop

> Loop de desenvolvimento Spec-Driven otimizado para Claude Opus 4.7.

Plugin para [Claude Code](https://claude.ai/code) que estrutura **cada tarefa de desenvolvimento** em um loop curto de 6 fases — Scaffold → Spec → Research → Plan → Implement → Verify — projetado para tirar máximo proveito da execução literal de instruções do Opus 4.7.

Diferente do `forge` (que é um pipeline longo de produto do zero ao deploy), o `dev-loop` é um **loop curto por tarefa** — feature, bug fix, refactor, exploração. Você abre o loop, fecha o loop, repete.

## Por que existe

Pesquisa e prática convergiram em 2026 para 5 princípios de trabalho com Opus 4.7 e Claude Code:

1. **Spec-first, single-turn** — Intent + constraints + acceptance criteria + file locations na primeira mensagem reduz drift e overhead de turnos.
2. **Plan-as-contract** — Subagents devem ler o plano literal como primeira ação. Opus 4.7 segue instruções literalmente; planos vagos viram drift.
3. **Context engineering por isolamento** — Pesquisa em subagent (não polui main thread); fases isoladas para TDD.
4. **Paralelismo onde compensa** — Múltiplos subagents concorrentes para research; sequenciais para implementação dependente.
5. **Verify-against-spec gate** — Acceptance criteria viram checklist verificável; "done" só após cruzar.

Veja [references/opus-4-7-principles.md](references/opus-4-7-principles.md) para o destilamento completo com fontes.

## Pipeline

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│  ⓪ SCAFFOLD   ① SPEC      ② RESEARCH   ③ PLAN     ④ IMPLEMENT ⑤ VERIFY│
│  .dev-loop/   intent +    parallel sub- literal    step-by-step  AC   │
│  + CLAUDE.md  constraints agents →      executable each sub      check│
│               + criteria  CLAUDE.md +   by sub     reads PLAN    +    │
│               + files     research-     executor   first         tests│
│                           notes.md                                    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## Estrutura criada por `scaffolding-project` (estrutura padrão Claude Code 2026)

Quando você roda o loop pela primeira vez num projeto, `scaffolding-project` monta toda a infra:

```
<project root>/
├── CLAUDE.md                              # Memória durável (com seção Project Context auto-curada)
├── CHANGELOG.md                           # Keep a Changelog format
├── .mcp.json                              # Stub para MCP servers
├── .gitignore                             # Com entries Claude Code
├── .claude/
│   ├── settings.json                      # Shared (hooks, permissions, env)
│   ├── settings.local.json                # Overrides locais (gitignored)
│   ├── agents/                            # Vazio inicial
│   ├── commands/                          # Vazio inicial
│   ├── skills/                            # Vazio inicial
│   └── hooks/                             # Vazio inicial
└── .dev-loop/
    └── .status                            # Estado do loop
```

**Idempotência**: roda quantas vezes quiser. Arquivos existentes são preservados; faltantes são criados; seções faltantes em `CLAUDE.md` são anexadas (não sobrescritas).

## Artefatos por tarefa

```
.dev-loop/<task-slug>/
├── SPEC.md           # Intent, constraints, acceptance criteria, file locations
├── research-notes.md # Sumário consolidado dos subagents de pesquisa (task-specific)
├── PLAN.md           # Passos numerados, ordem de dependência, subagent hints
└── VERIFY.md         # Checklist de acceptance criteria + resultados
```

E o `CLAUDE.md` do projeto recebe **findings duráveis** (arquitetura, convenções, gotchas) que persistem entre tarefas.

## Quick Start

```
# 1. Iniciar tarefa
/dev-loop:start adicionar-cache-redis

# 2. Conduzir a fase atual (skills são user-invocable)
/writing-spec

# 3. Ver onde estou
/dev-loop:status

# 4. Avançar fase a fase
/researching-task
/planning-implementation
/implementing-plan
/verifying-against-spec
```

Cada skill é **user-invocable**. Você dirige o loop; o plugin garante artefatos consistentes e gates auditáveis.

## Commands (2)

| Command | O que faz |
|---|---|
| `/dev-loop:start <task>` | Cria `.dev-loop/<task-slug>/`, inicializa `.status`, invoca `scaffolding-project` se for primeira tarefa, depois `writing-spec` |
| `/dev-loop:status` | Mostra fase atual, checklist do SPEC, artefato pendente |

## Skills (6) — todas user-invocable

| Skill | Artefato | Quando |
|---|---|---|
| `scaffolding-project` | `CLAUDE.md`, `CHANGELOG.md`, `.claude/{settings.json, agents/, commands/, skills/, hooks/}`, `.mcp.json`, `.gitignore`, `.dev-loop/.status` | Primeira tarefa de um projeto novo (idempotente — preserva o que já existe) |
| `writing-spec` | `SPEC.md` | Início de cada tarefa |
| `researching-task` | `research-notes.md` + append em `CLAUDE.md` | Após SPEC, antes do PLAN |
| `planning-implementation` | `PLAN.md` | Após research, antes do código |
| `implementing-plan` | commits/diffs | Executar PLAN.md passo-a-passo |
| `verifying-against-spec` | `VERIFY.md` | Após implementation, gate para "done" |

## MCP Servers (1 — bundled via .mcp.json)

O plugin empacota o servidor MCP oficial do Supabase que inicia automaticamente quando habilitado:

| Servidor | Transport | Origem | Auth |
|---|---|---|---|
| `supabase` | HTTP | `https://mcp.supabase.com/mcp` (oficial) | OAuth automático via `/mcp` no primeiro tool call |

**Setup**: nenhuma config inicial necessária. No primeiro uso, Claude Code abre o fluxo OAuth do Supabase no navegador; o token fica armazenado no keychain do macOS (ou em arquivo de credenciais).

Para desabilitar, edite o `.mcp.json` do plugin ou use `claude mcp disable supabase`.

## Agents (2) — auditores read-only

| Agent | Modelo | Justificativa |
|---|---|---|
| `spec-auditor` | sonnet | Valida SPEC.md contra codebase. Grade A-D + gaps. Isolated context. |
| `plan-critic` | opus | Audita PLAN.md por literal-executability (anti-drift de subagent). Raciocínio pesado, isolated context. |

## Por que skills user-invocable (e não /commands para tudo)

Design memo: **commands são thin se só invocam uma skill**. Skills `user-invocable: true` aparecem direto no menu `/`, sem wrapper. Os únicos 2 commands existem porque:
- `/dev-loop:start` faz mais do que uma skill (cria diretórios + status + delega)
- `/dev-loop:status` é puro leitor de estado (nenhuma skill envolvida)

## Por que apenas 2 agents (não mais)

Design memo: **agents adicionam complexidade — justifique cada um**. Ambos são *gates de qualidade entre fases*, com 3 critérios:
- **Isolated context**: precisam ler codebase + artefato sem poluir main thread
- **Read-only audit**: não escrevem, só geram relatório
- **Asymmetric depth**: análise profunda → relatório curto (uso clássico de subagent)

Pesquisa, planning e implementação **NÃO** viraram agents porque são iterativos com o usuário no main thread.

## Estado (.status schema)

`.dev-loop/.status` é um JSON único no nível do projeto:

```json
{
  "schema_version": 1,
  "project_initialized": true,
  "initialized_at": "2026-05-25",
  "current_task": "adicionar-cache-redis",
  "tasks": {
    "adicionar-cache-redis": {
      "phase": "plan",
      "started_at": "2026-05-25",
      "artifacts": {
        "SPEC.md": "approved",
        "research-notes.md": "approved",
        "PLAN.md": "draft",
        "VERIFY.md": null
      }
    }
  }
}
```

## Requisitos

- **Claude Code** versão recente
- **Opus 4.7** recomendado (Sonnet 4.6 funciona, mas execução literal e respeito ao plano são marcantes em Opus)

## Instalação

```json
{
  "enabledPlugins": {
    "dev-loop@chiaras-ai": true
  }
}
```

## Versão

`0.1.0` — release inicial.

## Licença

MIT
