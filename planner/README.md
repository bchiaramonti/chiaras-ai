# planner

> Personal plugin — gera planners pessoais executivos usando o sistema de design Editorial Noturno (dark mode, Georgia serif + Inter sans, terracota + azul petroleo).

## O que este plugin faz

Quando o Bruno pede um planner diario, daily dashboard, pagina de planejamento do dia ou HTML de cron matinal, o Claude Code invoca automaticamente a skill `generating-daily-planner` e aplica o sistema de design Editorial Noturno afunilado em 20 rodadas de decisao.

**Escopo estrito:** apenas artefatos pessoais. NAO usar em apresentacoes M7, comunicados para diretoria, documentos corporativos ou interfaces de produto.

## O que entrega

- Dark mode quente nativo (sem light mode)
- Tipografia como hierarquia (Georgia serif + Inter sans, sem caixas decorativas)
- Paleta de 9 cores com significado semantico (terracota = foco, azul petroleo = corpo, etc.)
- Grid de 3 colunas com gap 32px
- Zero ornamento (sem icones decorativos, sombras, gradientes, pills, badges)

## Componentes

| Item | Conteudo |
|---|---|
| Skill | `generating-daily-planner` (auto-invocada por trigger de contexto pessoal) |
| References | `tokens.css`, `tokens.json`, `principios.md`, `componentes.md`, `regras-texto.md`, `template-html.html` |
| MCP Servers | `garmin` (stdio) — dados Garmin Connect (sono, HRV, atividades, Body Battery) para enriquecer a zona Corpo |
| Agents | — |
| Commands | — |

## MCP: Garmin

O plugin declara um server MCP stdio (`garmin`) via `.mcp.json`. Quando instalado e habilitado, expoe ~96 tools da Garmin Connect (activities, sleep, HRV, stress, training load, workouts, devices, body battery, weight). O planner usa esses dados para popular a zona Corpo com numeros reais do dia.

O `.mcp.json` chama simplesmente `garmin-mcp`, que precisa estar no PATH. Isso desacopla o plugin de qualquer path absoluto e garante portabilidade do cache (`~/.claude/plugins/cache/`).

**Pre-requisitos (uma vez):**

```bash
# 1. Instalar o binario garmin-mcp no PATH do usuario
uv tool install /Users/bchiaramonti/Documents/brain/3-resources/ai-mcp/garmin-mcp

# 2. Autenticar na Garmin Connect (salva tokens OAuth em ~/.garminconnect)
garmin-mcp-auth
```

O passo 1 cria os binarios `garmin-mcp` e `garmin-mcp-auth` em `~/.local/bin/`. O passo 2 abre um login interativo (email + senha + MFA). Tokens expiram em ~6 meses; reautenticar com `garmin-mcp-auth --force-reauth`.

**Atualizar o binario** quando o repo `ai-mcp/garmin-mcp` mudar:

```bash
uv tool install --reinstall /Users/bchiaramonti/Documents/brain/3-resources/ai-mcp/garmin-mcp
```

**Fonte:** https://github.com/Taxuspt/garmin_mcp (clonado em `3-resources/ai-mcp/garmin-mcp/`, gerenciado por `uv`).

## Instalacao

Via marketplace `bchiaramonti-plugins`:

```
/plugin install planner@bchiaramonti-plugins
```

## Triggers

A skill e invocada quando o pedido contem qualquer um destes sinais:

- "meu planner", "meu daily", "minha pagina de planejamento"
- "dashboard pessoal", "relatorio do dia", "journal"
- "agenda diaria", "visao executiva do meu dia/semana"
- HTML gerado por cron matinal pessoal

## Nunca fazer

- Light mode
- Cartoes elevados ou bordas decorativas
- Icones (emoji ou SVG)
- Sombras, gradientes, blur
- UPPERCASE exceto em labels de dias da semana
- Formatos de data misturados — sempre "16 abril"

## Autor

Bruno Chiaramonti
