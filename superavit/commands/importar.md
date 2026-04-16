---
description: Importar extrato bancário da pasta input/ ou de um arquivo específico
argument-hint: "[arquivo]"
allowed-tools: mcp__claude_ai_Supabase__execute_sql, Bash, Read, Write, Glob
---

# Superavit — Importar

Atalho para importar extratos bancários. Delega todo o processamento para a skill `importing-statements`.

## Passo 1 — Resolver arquivo(s)

**Se `$ARGUMENTS` foi fornecido:**
- Usar o path informado como arquivo-alvo
- Se path relativo, resolver a partir do diretório atual

**Se nenhum argumento:**
- Listar arquivos disponíveis em `~/Documents/brain/2-areas/financas/input/`:

```bash
ls -1 ~/Documents/brain/2-areas/financas/input/
```

- Se vazio: informar **"Nenhum arquivo em `~/Documents/brain/2-areas/financas/input/`. Coloque seus extratos lá e tente novamente."** e **PARAR**.
- Se múltiplos: listar e perguntar qual importar (ou "todos")

## Passo 2 — Delegar para skill

Seguir o pipeline completo da skill `importing-statements` com o(s) arquivo(s) resolvido(s). **Não duplicar lógica** — a skill contém todas as regras de parsing, categorização e persistência.
