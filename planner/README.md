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
| References (style guide) | `tokens.css`, `tokens.json`, `principios.md`, `componentes.md`, `regras-texto.md`, `template-html.html` |
| References (metodologia) | `extracao-dados.md`, `metodologia-planejamento.md`, `insight-cruzamento.md` |
| MCP Servers | `trainingpeaks` (stdio) — zona Corpo (peso, sono, TSS, HRV, fitness) |
| Agents | — |
| Commands | — |

## MCP: TrainingPeaks

O plugin declara um server MCP stdio (`trainingpeaks`) via `.mcp.json` apontando para `tp-mcp` no PATH. Expoe ~58 tools (workouts, calendar, fitness metrics CTL/ATL/TSB, power/running PRs, weekly summaries, health metrics como peso/sono/HRV). Usado pela Fase 1 de extracao para popular a zona Corpo do planner com dados reais.

**Fonte:** https://github.com/JamsusMaximus/trainingpeaks-mcp (MIT license, clonado em `3-resources/ai-mcp/trainingpeaks-mcp/`).

### Pre-requisitos (uma vez por maquina)

```bash
# 1. Instalar o binario tp-mcp no PATH (com extra 'browser' para extracao de cookie)
uv tool install --reinstall '/Users/bchiaramonti/Documents/brain/3-resources/ai-mcp/trainingpeaks-mcp[browser]'

# 2. Autenticar. O TrainingPeaks nao tem API publica aprovada para uso pessoal, entao
#    a autenticacao e feita via cookie do navegador (Production_tpAuth).
#    Rota A · getpass nativo (funciona em Terminal.app, pode falhar em IDEs integradas):
tp-mcp auth
#    Rota B · se o prompt getpass travar (comum em terminal integrado de IDE),
#    usar bypass via stdin:
pbpaste | ~/.local/share/uv/tools/tp-mcp/bin/python -c "
import sys
cookie = sys.stdin.read().strip()
from tp_mcp.auth import store_credential, validate_auth_sync
v = validate_auth_sync(cookie)
if not v.is_valid: sys.exit(f'invalid: {v.message}')
r = store_credential(cookie)
print(f'OK · {r.message}')
"
#    (requer o cookie Production_tpAuth no clipboard: DevTools > Application > Cookies)

# 3. Verificar
tp-mcp auth-status
```

O cookie e criptografado (AES-256-GCM + PBKDF2 600k iteracoes) e salvo no macOS Keychain quando disponivel, com fallback para arquivo encriptado. Token OAuth de 1h e derivado sob demanda — Claude nunca ve o cookie, so bearer token de curta duracao.

**Renovar cookie** quando expirar (tipicamente 30 dias ou apos logout):
```bash
tp-mcp auth-clear
# depois repetir o passo 2 com cookie fresh
```

**Atualizar o binario** quando o repo mudar:
```bash
uv tool install --reinstall '/Users/bchiaramonti/Documents/brain/3-resources/ai-mcp/trainingpeaks-mcp[browser]'
```

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
