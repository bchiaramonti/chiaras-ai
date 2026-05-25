---
name: scaffolding-project
description: Inicializa um projeto para uso do dev-loop com a estrutura padrão Claude Code 2026 — cria CLAUDE.md, CHANGELOG.md, .claude/{agents,commands,skills,hooks,settings.json}, .mcp.json stub, .gitignore e .dev-loop/.status. Idempotente — preserva arquivos existentes e apenas anexa seções faltantes. Use na primeira tarefa de um projeto novo ou quando precisar trazer um projeto pré-existente para a estrutura padrão.
user-invocable: true
---

# Scaffolding Project

Inicializa a infraestrutura completa de um projeto Claude Code seguindo as melhores práticas 2026, incluindo a infraestrutura do dev-loop.

## Pré-requisitos

- Estar no diretório raiz do projeto-alvo
- **Idempotente**: se um arquivo/diretório já existe, **preservar** (não sobrescrever). Apenas ANEXAR seções faltantes onde aplicável.

## Estrutura final esperada

```
<project root>/
├── CLAUDE.md                              # Memória durável do projeto
├── CHANGELOG.md                           # Histórico de releases (Keep a Changelog)
├── .mcp.json                              # MCP servers do projeto (stub se não existir)
├── .gitignore                             # com entries Claude Code
├── .claude/
│   ├── settings.json                      # Hooks, permissions, env do projeto
│   ├── settings.local.json                # Overrides locais (gitignored)
│   ├── agents/                            # Custom subagents (vazio inicial)
│   ├── commands/                          # Custom slash commands (vazio inicial)
│   ├── skills/                            # Custom skills (vazio inicial)
│   └── hooks/                             # Hook scripts (vazio inicial)
└── .dev-loop/
    └── .status                            # Estado do loop
```

## Processo

1. **Detectar estado atual** — para cada arquivo/diretório do alvo, marcar `exists | missing`.
2. **Tratar `CLAUDE.md`**:
   - Se **missing**: criar a partir de `templates/CLAUDE.tmpl.md`.
   - Se **exists**: ler. Se NÃO contém a seção `## Project Context (auto-curated by dev-loop)`, ANEXAR ao final. Não modificar o resto.
3. **Tratar `CHANGELOG.md`**:
   - Se **missing**: criar a partir de `templates/CHANGELOG.tmpl.md` (formato Keep a Changelog).
   - Se **exists**: não modificar.
4. **Tratar `.mcp.json`**:
   - Se **missing**: criar a partir de `templates/mcp.tmpl.json` (objeto vazio `{"mcpServers": {}}` — pronto pra adicionar servers).
   - Se **exists**: não modificar.
5. **Tratar `.claude/`**:
   - Se **missing**: criar diretório.
   - Criar subdiretórios faltantes: `agents/`, `commands/`, `skills/`, `hooks/`. Cada um com um `.gitkeep` para garantir tracking quando vazios.
6. **Tratar `.claude/settings.json`**:
   - Se **missing**: criar a partir de `templates/settings.tmpl.json` (stub mínimo: `{"permissions": {"allow": [], "deny": []}, "env": {}, "hooks": {}}`).
   - Se **exists**: não modificar.
7. **Tratar `.claude/settings.local.json`**:
   - Se **missing**: criar com `{}` (será populado pelo usuário). **Garantir está no .gitignore**.
8. **Tratar `.gitignore`**:
   - Se **missing**: criar com `templates/gitignore.tmpl` (inclui Claude Code patterns padrão).
   - Se **exists**: ler. ANEXAR seção dev-loop ao final se ainda não tem:
     ```
     # Claude Code
     .claude/settings.local.json
     .claude/projects/
     ```
   - **NÃO** ignorar `.dev-loop/` (artefatos são memória útil pro time) — mas perguntar ao usuário; se ele optar por ignorar, adicionar `.dev-loop/`.
9. **Tratar `.dev-loop/`**:
   - Criar diretório se missing.
   - Criar `.dev-loop/.status` a partir de `templates/status.tmpl.json` (substituir `YYYY-MM-DD` por data atual).
10. **Reportar**:
    - Listar TODOS os arquivos criados (e quais foram preservados intactos).
    - Próximo passo: `/dev-loop:start <task>` para iniciar a primeira tarefa.

## Decisão pro usuário (perguntar 1 vez)

Antes de tocar no `.gitignore`, perguntar via `AskUserQuestion`:

> "Trackear `.dev-loop/` no git? Recomendado: SIM — artefatos viram memória do time. NÃO se você quer manter privado."

Default: trackear (sim).

## Pós-condição

- Todos os arquivos listados em "Estrutura final esperada" existem
- `.status` parseia como JSON válido com `project_initialized: true`
- `CLAUDE.md` contém a seção `## Project Context (auto-curated by dev-loop)`
- `.gitignore` cobre `settings.local.json` e (opcionalmente) `.dev-loop/`
- Nenhum arquivo pré-existente foi sobrescrito

## Validação interna

- [ ] `CLAUDE.md` tem seção sentinela
- [ ] `CHANGELOG.md` segue Keep a Changelog
- [ ] `.claude/settings.json` parseia como JSON válido
- [ ] `.claude/settings.local.json` está no `.gitignore`
- [ ] `.dev-loop/.status` parseia, `project_initialized: true`
- [ ] Idempotência verificada: rodar duas vezes não muda o output da segunda
