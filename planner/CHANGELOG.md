# Changelog

All notable changes to the Planner plugin will be documented in this file.

## [1.9.0] - 2026-04-17

### Fixed · Tres bugs de integridade detectados em produ&ccedil;&atilde;o

**Bug 1 · Task `cancelada` entrando no planner como `atrasada`.** A skill confiava cegamente no campo `status` retornado pela ClickUp API, sem cruzar com `date_closed`, `archived` ou `status.type`. Uma task marcada como **cancelada** no ClickUp chegou a ser incluida como MIT #1 no planner diario.

Fix aplicado em `generating-daily-planner/references/extracao-dados.md` e `generating-weekly-planner/references/extracao-dados.md` secao 2 (ClickUp):

- **Whitelist explicita** de status aceitos: `["pendente", "em andamento", "atrasada", "bloqueada", "em revisao", "em aprovacao"]`
- **Blacklist** de status proibidos: `["cancelada", "descartada", "won't do", "concluida", "arquivada", "duplicada", "rejeitada"]`
- **Regra de deteccao em ordem**: (1) `status.status` na blacklist, (2) `status.type == closed`, (3) `date_closed != null`, (4) `archived == true` — qualquer match descarta a task
- **Regra de duvida**: tasks destinadas a MIT/Big 3/Prazos duros com status fora da whitelist sao **confirmadas via `AskUserQuestion`** antes de entrar no topo do planner
- **Descoberta de status customizados**: sugerir chamada a `clickup_get_list(list_id=...)` para inspecionar `statuses[]` e identificar automaticamente status com `type=closed|done`

Checklists pre-render (`SKILL.md` + `metodologia-planejamento.md`) validam explicitamente "nenhuma task em status blacklist" e "tasks em status ambiguo destinadas a MIT foram confirmadas".

**Bug 2 · Coluna 3 do daily ("Delegadas") com escopo errado.** Tratava a secao como "tasks que Bruno delegou" (filtro `assignee != Bruno, created_by = Bruno`), quando o escopo correto do cargo Head of Performance e saude do workspace M7 inteiro — independente de quem assinou ou criou. A coluna entregava vazio ou mostrava apenas o time imediato, escondendo gargalos sistemicos.

Fix aplicado com renome estrutural:

- **Renomeada a coluna** de "Delegadas" para **"Workspace M7"** no template, componentes, label editorial e schema
- **Query trocada** de `assignees=[!Bruno]` por `statuses=["atrasada", "bloqueada"]` no workspace inteiro (sem filtro de assignee)
- **Agrupamento** passa de "por projeto que Bruno delegou" para "por frente (lista/sprint)" com contadores reais do workspace
- **Regra "Bruno e o gargalo"**: tasks com `assignee == Bruno` aparecem destacadas com `.tasks__row--self` e, se >=3, o header ganha meta `<span class="alert">N minhas</span>`. Nao duplicam com a coluna 2 (Tarefas ClickUp)
- **Novas classes CSS**: `.workspace__group`, `.workspace__frente`, `.tasks__row--blocked`, `.tasks__row--self` em `tokens.css`. `.delegadas__group` / `.delegadas__project` mantidas como alias de retrocompatibilidade
- **Weekly**: a extracao Workspace M7 alimenta especificamente a Regra 6 (Riscos & fogos) e informa Big 3 quando ha gargalo pessoal de Bruno em uma frente

Atualizados: `SKILL.md` (tabela da Fase 1 + Regra 5), `metodologia-planejamento.md` (Regra 5 reescrita), `componentes.md` (secao 10 renomeada), `regras-texto.md` (vocabulario de labels), `template-html.html` (Coluna 3 do daily) em ambas skills.

**Bug 3 · Contadores sem rastreabilidade com a fonte.** O planner exibia "42 atrasadas" quando a query real retornava 28. O numero provavelmente somava `status=pendente + due vencido` com `status=atrasada` (dupla contagem, porque o ClickUp automaticamente muda para `atrasada` quando o due passa). Sem mapa metrica→query, impossivel auditar.

Fix aplicado em ambos `extracao-dados.md`:

- **Nova secao "Rastreabilidade de metricas"** exigindo que todo numero exibido tenha entrada em `extracao.metricas` com `{metrica, query, count, fonte}`
- **Regra de unica fonte para "atrasada"**: status customizado `atrasada` e a fonte canonica. Proibido somar com `status=pendente + due vencido`
- **Regra de recalculo na Fase 2**: contadores recalculados a partir das linhas extraidas, nao reusados dos headers da API
- **Validacao antes de renderizar**: Fase 3 recusa renderizar se um numero no HTML nao tem entrada correspondente em `metricas`
- Checklists pre-render (`SKILL.md` + `metodologia-planejamento.md`) incluem explicitamente "cada contador tem entrada rastreavel" e "contador recalculado, nao reusado"

### Added

- Secoes novas em `references/extracao-dados.md` (daily + weekly): "Whitelist e blacklist de status", "Rastreabilidade de metricas"
- Blocos novos no schema YAML: `workspace_m7:` (substitui `delegadas:`) com `is_self` por task, `contadores:`, e `metricas:` global
- Classes CSS novas em `tokens.css` do daily: `.workspace__group`, `.workspace__frente`, `.tasks__row--blocked`, `.tasks__row--self`
- Anti-padroes novos em "Nunca fazer" das duas `SKILL.md`: incluir task em blacklist, tratar coluna 3 como "o que eu deleguei", exibir numero sem rastreabilidade, somar heuristicas redundantes

### Changed

- Label editorial "Delegadas." → "Workspace M7." (daily). Weekly nao tinha label visivel (extracao alimentava Riscos & fogos); agora a conexao esta explicitamente documentada na metodologia
- Coluna 3 do daily passa a exibir contadores do workspace inteiro (ex: "28 atrasadas · 4 bloqueadas · 3 minhas") em vez de contadores do subset delegado (ex: "1 atrasada · 7 abertas")
- Todas tabelas de "Nunca fazer" + checklists pre-render atualizadas

### Notes

- `delegadas__*` CSS classes permanecem como alias para nao quebrar HTMLs gerados antes de v1.9.0 — remover em v2.0.0
- Os tres bugs compartilham raiz comum: **skill tratava a API ClickUp como fonte de verdade sem questionar**. A correcao introduz boundaries de interrogacao em cada ponto de ingestao (status validation, scope validation, count validation)
- Usuario adicionou nota semantica ao `brain/CLAUDE.md` reforcando que Bruno responde pelo workspace M7 inteiro (contexto para coluna 3)

## [1.8.1] - 2026-04-17

### Fixed
- **Quebra de linha do label `sono medio`** na zona Corpo da skill `generating-weekly-planner`. A coluna de label do grid 3-col estava em 48px (herdado da daily, cujos labels sao palavras unicas: `peso`, `sono`, `TSS sem`, `TSB`). No weekly os labels sao compostos (`peso Δ`, `sono medio`, `TSS total`, `TSB`) e "sono medio" (~58px em Georgia italic 11px) quebrava em duas linhas, inflando a altura da row e desalinhando o baseline vertical.
- Fix: `grid-template-columns: 48px 1fr auto` -> `72px 1fr auto` em `.band-1__corpo-row`, acomoda todos os labels compostos sem quebra. Adicionado `white-space: nowrap` em `.band-1__corpo-label` como reforco anti-quebra (belt-and-suspenders).

### Notes
- Diferenca intencional em relacao a daily (que mantem 48px): labels do weekly sao semanticamente diferentes porque sao agregados (Δ, medio, total), e a qualificacao e estruturalmente parte do label. Reduzir para `sono` apenas tornaria ambigua a natureza agregada da metrica.
- Escopo limitado a css: nenhuma outra mudanca de comportamento, metodologia ou template.

## [1.8.0] - 2026-04-17

### Added
- **Extensao das tags de classificacao da zona Corpo para a skill `generating-weekly-planner`** (v1.7.0 aplicou apenas no daily; v1.8.0 completa a paridade). Cada um dos 4 KPIs agregados do weekly (peso Δ, sono medio, TSS total, TSB) agora exibe uma tag de 1 palavra a direita do numero, com cor semantica compartilhada entre valor e tag. Faixas identicas a daily: garante consistencia de leitura entre os dois planners.
- **Classes CSS novas em `generating-weekly-planner/references/tokens.css`**: `.band-1__corpo-tag` com 3 modifiers (`--body`, `--alert`, `--warn`) + `.band-1__corpo-number--empty` para dados ausentes. Espelha o padrao introduzido no daily em v1.7.0.
- **Matriz de faixas -> tag** em `generating-weekly-planner/references/extracao-dados.md` secao 4, adaptada para os KPIs agregados semanais: peso Δ por variacao em kg (com rule-of-thumb 1kg ≈ 1% para Bruno ~100kg), sono medio por horas da semana, TSS total por volume seg-sex, TSB por bandas de Banister. Inclui regra de ouro reforcada: dado ausente = valor `&mdash;` + tag OMITIDA.
- **Secao nova em `regras-texto.md`** documentando o vocabulario fixo das tags por KPI e anti-padroes (sem sinonimos livres, sem parentese, sem pontos finais, italic Georgia 10px).

### Changed
- **Ordem fixa dos 4 KPIs** da zona Corpo · semana passa de `peso Δ -> TSS -> sono -> TSB` para **`peso Δ -> sono medio -> TSS total -> TSB`** — paridade com a daily (v1.7.0). Racional semantico: "peso e porta de entrada, sono e condicao, TSS e volume, TSB e sintese".
- **Layout da row** passa de flex 2-col (label / valor) para **grid 3-col** (`48px 1fr auto`): label fixa na esquerda, valor alinhado a direita no centro, tag com largura auto no fim. `white-space: nowrap` na tag impede quebra de linha.
- **`--zone-corpo` de 150px para 240px** em `tokens.css` e `tokens.json` (acomodar tags). Lide continua em `flex:1` absorvendo o espaco restante — o header reparticiona entre as 5 zonas, nao cresce em altura.
- **`generating-weekly-planner/references/componentes.md` secao 5 (Corpo · semana) reescrita** com a estrutura de 3 colunas, exemplos HTML de todos os 4 KPIs com tags na nova ordem, exemplo de fallback (valor `&mdash;` com tag omitida) e mapeamento rapido das tags por KPI.
- **`generating-weekly-planner/references/template-html.html`** atualizado no bloco da Zona 5 com os 4 KPIs na nova ordem, cada um com sua tag-exemplo.
- **`generating-weekly-planner/SKILL.md`** atualizado: Regra 8 descreve a ordem fixa + tags, checklist pre-render valida a ordem e a regra de omissao da tag, secao "Nunca fazer" adiciona "inventar tag" e "usar sinonimos livres".
- **`generating-weekly-planner/references/metodologia-planejamento.md` Regra 8** reescrita com a nova ordem + regra de cor compartilhada entre numero e tag + mapeamento rapido. Checklist final atualizado.
- **Description do plugin e entry do marketplace** mencionam explicitamente que a zona Corpo (daily + weekly) usa tags de classificacao.

### Notes
- Altura do header **continua identica** — tags ocupam a mesma linha do valor via grid horizontal, nao adicionam row.
- Tag tem **no maximo 1 palavra** (exceto `em queda` que e 1 conceito em 2 palavras). Vocabulario fixo por KPI (sem sinonimos livres): `estável`, `em queda`, `subindo`, `ideal`, `ok`, `baixo`, `saudável`, `leve`, `pesado`, `crítico`, `produtivo`, `neutro`, `fresco`, `overreach`, `destreino`.
- Regra de ouro reforcada na v1.8.0: **dado ausente = valor `&mdash;` com classe `--empty` E tag TOTALMENTE OMITIDA** (nunca renderizar tag vazia ou `?`). Nunca inventar classificacao.
- Versao bumpada para 1.8.0 (MINOR) seguindo o padrao do repo: cada enhancement skill-level recebe bump MINOR. 1.7.0 introduziu o conceito no daily; 1.8.0 completa a paridade no weekly.

## [1.7.0] - 2026-04-17

### Added
- **Tags de classificacao na zona Corpo do header** (apenas skill `generating-daily-planner`). Cada um dos 4 KPIs agora exibe, a direita do numero, uma tag de 1 palavra classificando o status (ex: `estável`, `baixo`, `produtivo`, `overreach`). Cor da tag segue semantica do design system: `--body` (azul petroleo) para saudavel, `--alert` (terracota escuro) para alerta, `--accent-primary` (warn) para atencao, `--text-secondary` para neutro. Feature validada no planner gerado em 2026-04-17.
- **Classes CSS novas em `references/tokens.css`**: `.header__corpo-tag` com 3 modifiers (`--body`, `--alert`, `--warn`) + `.header__corpo-number--empty` para dados ausentes.
- **Matriz de faixas -> tag** em `references/extracao-dados.md` secao 4. Cada KPI (peso, sono, TSS sem, TSB) tem 3-5 faixas mapeadas para tags especificas, com a classe CSS correspondente. Inclui regra de classificacao de peso por variacao de 7 dias (estavel/em queda/subindo), sono por horas absolutas, TSS por volume semanal + contagem de dias zerados, TSB por 5 bandas do metodo de Banister (overreach/produtivo/neutro/fresco/destreino).

### Changed
- **Ordem fixa dos 4 KPIs** da zona Corpo: `peso -> sono -> TSS sem -> TSB` (antes: peso -> TSS -> sono, com HRV e TSB como "opcionais"). TSB deixa de ser opcional e entra como 4o KPI fixo — metrica de Banister que sintetiza forma do atleta, importante para modulacao de intensidade no dia.
- **Layout da row da zona Corpo** passa de flex 2-col para **grid 3-col** (`48px 1fr auto`): label fixa na esquerda, valor ocupa o meio alinhado a direita, tag no fim com largura auto. `white-space: nowrap` impede quebra de linha da tag.
- **`--zone-corpo` de 130px para 240px** em `tokens.css` para acomodar as tags sem quebrar. Lide continua em `flex:1` absorvendo o espaco restante (o header continua somando 100% da largura, so redistribui entre as 5 zonas).
- **`references/componentes.md` secao 5 (Corpo) reescrita** com a estrutura de 3 colunas, exemplos HTML de todos os 4 KPIs com tags, exemplo de fallback (valor `&mdash;` com tag omitida) e link para matriz de faixas em `extracao-dados.md`.
- **`references/template-html.html`** atualizado no bloco da Zona 5 (Corpo) com os 4 KPIs na nova ordem, cada um com sua tag-exemplo.

### Notes
- **Regra de ouro mantida e reforcada:** quando um KPI nao tem dado (MCP indisponivel, metrica ausente), o valor renderiza como `&mdash;` com classe `--empty` E a tag e **totalmente omitida** do HTML (nao se renderiza uma tag vazia ou "?"). Nunca inventar classificacao.
- Altura do header **nao aumenta** — as tags ocupam a mesma linha do valor via grid horizontal, nao adicionam row.
- Tag tem **no maximo 1 palavra** — sem parenteses, sem pontos finais, sem compostos ligados por hifen se puder ser reformulado. Ex: `em queda` ok (2 palavras mas 1 conceito), `ok` ok, `overreach` ok, `sobrecarga funcional` **ruim** (reformular pra `pesado`).
- A skill `generating-weekly-planner` (v1.6.0) **nao foi alterada** — o weekly tem seu proprio layout de Corpo com 4 KPIs agregados (peso Delta, TSS total, sono medio, TSB) que pode receber o mesmo tratamento de tags em versao futura, mas esta PR esta escopada em daily.

## [1.6.0] - 2026-04-17

### Added
- **New skill `generating-weekly-planner`**. Complementar ao `generating-daily-planner`: daily sobre execucao dentro do dia, weekly sobre orquestracao dos 5 dias uteis (seg-sex, sem fim de semana). Mesmo design system Planner Editorial Noturno (Georgia + Inter, terracota + azul petroleo, dark mode quente) mas estrutura radicalmente diferente: 4 bands em fit-screen 1440x1000 (Contexto + Orquestra HERO + Compromissos + Preflight ancorado ao fundo via `flex:1` na Band 2).
- **Metodologias aplicadas** (pesquisadas e validadas):
  - **Hyatt Weekly Preview** → Tese da semana + Weekly Big 3 derivados de Metas Q2 + Criterio de vitoria (4 outcomes binarios)
  - **Cal Newport Time-Block** → Orquestra dos 5 dias com deep work blocks protegidos (pelo menos 1 maker day por semana, MIT #1 com >=4h contiguas)
  - **4DX (McChesney)** → Criterio de vitoria com checks verificaveis
  - **Kahneman/Klein Pre-mortem** → Riscos & fogos com mitigacao concreta ja escrita
  - **Newport Shutdown Ritual (invertido)** → Preflight com 4 perguntas editoriais antes da semana comecar
- **Retrospectiva S-1 obrigatoria**: skill sempre pergunta ao usuario o que destravou/travou/aprendi na semana passada antes de gerar a Tese. Sem isso, a Tese vira generica.
- **Corpo · semana com 4 KPIs agregados** via TrainingPeaks MCP (reusa as tools introduzidas em v1.5.0): peso Δ (weight tool), TSS total (weekly_summary), sono medio (sleep), TSB (fitness_metrics). TSB e o novo KPI exclusivo do weekly — conceito inerentemente semanal que nao cabe num daily.
- **Conexao com Metas Q2**: Weekly Big 3 devem derivar de objetivos trimestrais (ClickUp goals → brain/3-resources → perguntar). Sem essa conexao, Big 3 sao apenas tarefas grandes.
- **8 regras de planejamento semanal** em `generating-weekly-planner/references/metodologia-planejamento.md` (vs 6 regras da daily), cada uma com filtro + teste de sanidade + anti-padroes + exemplos.
- **Layout fit-screen** com Preflight **sempre ancorado ao fundo**: Band 2 (Orquestra) usa `flex:1` para crescer e empurrar Preflight ao limite inferior. Garantia de one-pager report em qualquer densidade de conteudo.

### Changed
- **Marketplace entry** atualizada para refletir os dois planners (daily + weekly) com descricao contextualizando escopos de cada. Keywords expandidas: `weekly-planner`, `weekly-preview`, `sunday-planning`, `trainingpeaks`, `time-blocking`.
- **Plugin description** idem — agora explica que o plugin cobre daily (execucao) e weekly (orquestracao) como artefatos complementares.

### Notes
- Nenhuma mudanca no `generating-daily-planner` existente — daily continua funcionando identicamente.
- O weekly **nao replica** a estrutura do daily x5. Tem hero visual proprio (Orquestra dos 5 dias lado a lado) e camada estrategica adicional (Tese + Criterio + Big 3 com pronto-quando + Riscos com mitigacao + Preflight).
- Tokens de cor e tipografia sao compartilhados entre daily e weekly — a unica excecao e que o weekly acrescenta tokens de layout especificos para o fit-screen (page-height 1000, band-gap 22, band-1-min-height 180, zone-ano 160).
- Design system iterado e validado visualmente no Paper (arquivo `weekly-planner`, artboard v2 "Weekly Planner v2 · Orquestra") antes da implementacao HTML.

## [1.5.1] - 2026-04-17

### Fixed
- **`.mcp.json` compatibility with GUI-spawned Claude apps** (Cowork, Claude Desktop). The v1.5.0 config used `"command": "tp-mcp"`, relying on PATH resolution. That works in terminal-spawned Claude Code (which inherits `~/.zprofile` PATH) but **fails in GUI apps** because macOS `launchd` provides only a minimalist PATH (`/usr/bin:/bin:/usr/sbin:/sbin`) that excludes `~/.local/bin/` where `uv tool install` places binaries. Symptom: Cowork listed the server in Connectors but chats reported "trainingpeaks nao esta instalado" when trying to use it.
- Fix: wrap the command in `/usr/bin/env` with an explicit `PATH` env var that includes `~/.local/bin`, `/opt/homebrew/bin`, `/usr/local/bin`, and the standard system paths. `/usr/bin/env` exists on every Unix-like system at a fixed absolute path and does PATH lookup using the env passed to the child process.

### Notes
- Trade-off: this reintroduces a user-specific absolute path (`/Users/bchiaramonti/.local/bin`) in the plugin config, which technically violates plugin rules P5 ("no paths outside plugin dir") and is less portable than the v1.5.0 approach. Accepted as explicit trade-off for a **personal** plugin: the only consumer is the author's machine, and without this fix the MCP is not reachable from the primary consumer app (Cowork). README section documenting the `uv tool install` prereq makes this explicit.
- README "MCP: TrainingPeaks" updated with a paragraph explaining why the wrapper is needed and what the launchd PATH limitation is.

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
