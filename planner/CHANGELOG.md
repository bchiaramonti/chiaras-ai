# Changelog

All notable changes to the Planner plugin will be documented in this file.

## [1.5.0] - 2026-04-17

### Added
- **MCP server `trainingpeaks`** via `.mcp.json`. Substitui o Garmin MCP removido em v1.3.0 (garth deprecated por Cloudflare), agora usando `JamsusMaximus/trainingpeaks-mcp` (MIT, 58 tools, v2.0.0). Autenticacao cookie-based do navegador (Production_tpAuth) troca o cookie por OAuth token de 1h, criptografa com AES-256-GCM no macOS Keychain. **Nao e afetado por Cloudflare TLS fingerprinting** porque usa sessao do browser ja validada (nao autentica via HTTP puro).
- **Restaura automacao da zona Corpo** no planner: peso, sono, HRV, TSS semana e TSB (forma) agora saem do TP em vez de serem perguntados ao usuario. Pergunta ao usuario volta a ser apenas fallback quando o MCP falha ou a auth expira.
- **README: secao MCP TrainingPeaks** documentando pre-reqs (`uv tool install --reinstall '...[browser]'`, autenticacao via `tp-mcp auth` ou bypass via `pbpaste | python` quando o getpass trava em IDE), renovacao de cookie e update do binario. Documenta tambem o "bypass getpass" para terminais integrados (VS Code, Cursor, Claude Code) que nao dao TTY completo ao Python.

### Changed
- **`extracao-dados.md` secao 4 · Corpo** reescrita: fonte primaria passa a ser TrainingPeaks MCP, com mapeamento das 5 tools relevantes (weight, sleep, HRV, weekly_summary, fitness_metrics). Adiciona regras de cor para TSB (positivo > body; muito negativo > alert).
- **`extracao-dados.md` matriz de fontes (tabela no topo):** a linha Corpo passa de "*Sem MCP atualmente* — sempre perguntar" para "TrainingPeaks (cookie-based auth)".

### Notes
- Pre-requisito de instalacao inclui o extra `[browser]` para permitir extracao direta do cookie do Chrome. Em maquinas com Arc/Brave/Edge como default, o fluxo manual via DevTools + `pbpaste | python` e documentado no README.
- Token OAuth derivado do cookie expira em 1h e e refresh automatico. O cookie raiz tem vida ~30 dias (tipico para sessao TP).

## [1.4.0] - 2026-04-17

### Changed
- **Skill refactored into 3-pass workflow.** Previously the `generating-daily-planner` skill was 100% rendering instructions (style-guide only) — the HTML got preenchido com texto plausivel mas sem metodo. Agora a skill orquestra tres fases explicitas:
  - **Fase 1 · Extrair** (novo `references/extracao-dados.md`): matriz de fontes para agenda (Google Calendar MCP), tarefas/delegadas (ClickUp MCP), corpo/saude (sempre perguntar — Garmin foi removido em v1.3.0), contexto do insight (filesystem `brain/3-resources/` PARA). Protocolo de fallback: tentar uma vez com parametros frouxos, depois pergunta especifica ao usuario, nunca inventar.
  - **Fase 2 · Planejar** (novo `references/metodologia-planejamento.md`): 6 regras de decisao — Lide como tese argumentativa unica; MITs via Eisenhower Q2 > Eat-the-frog > role balance (>=2 dimensoes); Agenda capacidade 60/40 com bloco >=90min reservado em pico cognitivo; Tarefas ClickUp ABCDE com corte em 5-6 linhas; Delegadas agrupadas por projeto; Amanha como Ancora imperativa + Preparar hoje. Inclui checklist de sanidade com 13 pontos.
  - **Fase 2b · Insight cruzamento** (novo `references/insight-cruzamento.md`): processo em 7 passos para gerar o bloco Insight a partir dos desafios reais do dia — extrair tensionamentos, mapear a dominios de conhecimento, escanear `brain/3-resources/`, extrair perguntas fundadoras, cruzar DUAS (nunca 3+) tensionadas, redigir no formato-canon de 150-250 chars. Com fallback para pares classicos quando 3-resources nao cobre o dominio e regra "nunca inventar autor/livro".
  - **Fase 3 · Renderizar** (preserva style-guide existente): `tokens.css`, `principios.md`, `componentes.md`, `regras-texto.md`, `template-html.html` — nenhum destes foi alterado na logica, so adicoes para suportar os dois ajustes de template abaixo.

### Added
- **Template change (a) · Pre-mortem por MIT.** Nova classe `.inadiaveis__risco` (tokens.css) renderiza em bloco abaixo do meta, em italic `--text-subtle`. Cada MIT obrigatoriamente responde em 1 linha `"o que vai me impedir de terminar isso hoje?"` no formato `risco: <causa> → <plano B>`. Modificador `--delayed` mantem coerencia visual com atraso. Componentes.md secao 8 expandida com 4 exemplos e regras do texto de risco.
- **Template change (b) · Amanha estruturado.** Secao Amanha agora tem duas partes explicitas (antes era prosa unica): `.footer__amanha-ancora` (1 frase imperativa) + `.footer__amanha-preparar` opcional (0-2 bullets de <=15min cada). `.footer__amanha-body` legacy permanece no CSS para retro-compat mas nao deve ser usado em planners novos. Componentes.md secao 12 reescrita com variantes validas.
- **`Checklist pre-render`** na SKILL.md: 13 pontos validados antes do HTML final sair (dados reais, lide com tese, MITs com role balance, pre-mortem, capacidade 60/40, ordenacao ABCDE, etc.).
- **Regra explicita anti-ficcao**: Nunca fazer · "Inventar dados quando extracao falha" e "Pre-mortem ficticio".

### Notes
- Nenhuma mudanca em `principios.md`, `regras-texto.md`, `template-html.html` (estrutura) nem em tokens existentes — apenas adicoes.
- `tokens.css` cresceu de 712 para ~760 linhas com as duas novas secoes de classes.
- Referencias cruzadas entre os 3 novos arquivos e os existentes mantem o principio de progressive disclosure (SKILL.md orquestra, references detalham).

## [1.3.0] - 2026-04-16

### Removed
- **MCP server `garmin`** and the `.mcp.json` declaration. The upstream `Taxuspt/garmin_mcp` depends on the `garth` library, which was officially deprecated after Garmin deployed Cloudflare TLS fingerprinting in March 2026 — all non-browser HTTP clients are blocked with `429 Too Many Requests` on first SSO auth. See Taxuspt/garmin_mcp issues #58, #63, #79. Two open PRs (#70 user-agent spoof, #77 `curl_cffi` upgrade) attempt to fix it but none are merged.
- README section "MCP: Garmin" and the related row in Componentes table.

### Notes
- Source repo (`3-resources/ai-mcp/garmin-mcp/`), `uv tool` install (`~/.local/bin/garmin-mcp`, `~/.local/bin/garmin-mcp-auth`), and `~/.local/share/uv/tools/garmin-mcp/` have all been removed.
- Future direction: evaluate Playwright-based alternatives (`etweisberg/garmin-connect-mcp` or `nrvim/garmin-givemydata`) that are immune to TLS fingerprinting because they use a real browser.

## [1.2.0] - 2026-04-16

### Changed
- **`.mcp.json` portability**: removed the absolute path to `3-resources/ai-mcp/garmin-mcp` (violated plugin rules P5 "no paths outside plugin dir" and P7 "MCP servers use `${CLAUDE_PLUGIN_ROOT}`"). The plugin now calls simply `garmin-mcp` as a PATH binary, installed via `uv tool install`. Makes the plugin portable across machines and cache-safe (`~/.claude/plugins/cache/`).
- **README prerequisite updated**: added step 1 `uv tool install /path/to/garmin-mcp` before the existing auth step. `garmin-mcp-auth` is now a direct command (was `uv run garmin-mcp-auth`).

### Fixed
- Plugin validation grade: **C → A** (two P5/P7 failures resolved).

### Updated skill · generating-daily-planner
- Introduced `--fs-roman: 28px` token for the Tres inadiaveis roman numerals (previously used `--fs-h1: 40px` — too large). `.inadiaveis__item` grid column `36px → 28px`.
- **Tarefas ClickUp** metadata rule: `.tasks__title-meta` now shows `· <lista> · <tag>` (list first, then tag) to preserve ClickUp's hierarchy and avoid ambiguity. Multiple tags separated by comma in the tag segment.
- Documentation cleanup: removed time-sensitive date from `tokens.css` header, added section index, and replaced the `40px` literal in `principios.md` with the stable token reference `--fs-display`.

## [1.1.0] - 2026-04-16

### Added
- **MCP server**: `garmin` via `.mcp.json` — bundles the Taxuspt/garmin_mcp stdio server (~96 tools across activities, sleep, HRV, stress, training load, workouts, devices). Enables the daily planner to enrich the "Corpo" zone with real Garmin Connect data (sleep score, HRV overnight, Body Battery, previous-day activities).
- Source lives at `/Users/bchiaramonti/Documents/brain/3-resources/ai-mcp/garmin-mcp/` (separate Python project managed by `uv`). Plugin declares the server via `.mcp.json`; authentication is one-time via `uv run garmin-mcp-auth` (tokens stored at `~/.garminconnect`, ~6 month lifetime).

## [1.0.0] - 2026-04-16

### Added
- Plugin scaffold: `plugin.json`, `README.md`, `.claude-plugin/`
- **1 skill**: `generating-daily-planner` (auto-invoked when Bruno requests his daily planner)
- **6 references**:
  - `tokens.css` — CSS variables (colors, typography, spacing, layout zones)
  - `tokens.json` — DTCG format tokens for interop (Figma Tokens Studio, Tailwind)
  - `principios.md` — 6 founding design principles (typography over boxes, color as decision, zero ornament, etc.)
  - `componentes.md` — 12 components specified with HTML examples and CSS classes
  - `regras-texto.md` — editorial voice rules (section labels, lide journalistic tone, insight structure, metric formatting)
  - `template-html.html` — standalone HTML starter (header 5-zone + body 3-col + footer 2-col)
- **Design system**: Planner Editorial Noturno
  - Dark mode warm native (bg `#1A1715`)
  - Georgia serif (narrative) + Inter sans (tabular numbers only)
  - Palette: terracota `#D97757` (work/focus) + azul petroleo `#6B9EB0` (body/training) + alert `#B8593C`
  - Layout: header 5-zone (Dia · Lide · Insight · Mes · Corpo) + body 3-col (Agenda · Tres inadiaveis + Tarefas ClickUp · Delegadas) + footer 2-col (Notas · Amanha)
  - Zero ornament philosophy (no cards, shadows, gradients, pills, badges)
- Marketplace entry in `bchiaramonti-plugins/.claude-plugin/marketplace.json`
