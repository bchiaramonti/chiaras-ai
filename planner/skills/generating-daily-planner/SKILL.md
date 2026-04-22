---
name: generating-daily-planner
description: Gera o daily planner pessoal executivo de Bruno seguindo quatro fases. Fase 1 (Extrair) le dados reais via MCPs (Google Calendar, ClickUp) ou pergunta ao usuario; corpo/saude sempre perguntado. Fase 2 (Planejar) aplica boas praticas — Most Important Tasks, Eat-the-frog, time blocking 60/40, pre-mortem, Eisenhower, role balance — e **sempre invoca o agente pfeffer-power-analyst** (v1.11.0) para gerar Insight · cruzamento + Notas do dia atraves do livro POWER de Jeffrey Pfeffer (unica fonte de insight do sistema). Fase 3 (Emitir canonico) serializa o plano em .md canonico (frontmatter YAML + body Markdown) em `~/Documents/brain/0-inbox/plan-review/daily/YYYY/MM/daily-YYYY-MM-DD.md` — fonte de verdade editavel durante o dia. Fase 4 (Renderizar+publicar) le o .md, aplica o design system Planner Editorial Noturno e publica o HTML via `mcp__cowork__update_artifact` no live artifact `daily-planner-live`. Use quando Bruno pedir para criar, editar ou gerar seu planner diario. Nao usar em apresentacoes M7, comunicados corporativos ou outputs para terceiros.
license: Proprietary
---

# Generating Daily Planner

Gera o daily planner pessoal executivo aplicando **quatro fases**: extrair dados reais, planejar usando metodologia, emitir .md canonico, renderizar e publicar no live artifact.

**Principio central:** o planner so serve se o plano for executavel. Design impecavel com conteudo fraco produz artefato bonito e inutil. Metodologia primeiro, estilo depois.

**Principio de arquitetura (v2):** o .md canonico e a **fonte unica de verdade**. O HTML do live artifact e derivado — regenerado pela skill (ou por `/planner sync` apos ediçao manual do .md). Planejamento do dia e estatico por natureza; mutabilidade e explicita, nunca automatica.

## Quando usar esta skill

Invocada quando Bruno pede para gerar ou atualizar o planner do dia — nao para apresentacoes corporativas nem comunicacao com terceiros.

**Triggers tipicos:**
- "Crie meu planner de hoje"
- "Gera o HTML do dia"
- "Atualiza minha pagina de planejamento"
- "Monta um daily dashboard"
- "Quero uma visao executiva do meu dia"

**NAO usar esta skill para:**
- Apresentacoes M7 para diretoria ou XP
- Documentos corporativos
- Comunicados formais
- Outputs que terceiros vao consumir
- Interfaces de produtos SaaS

## Workflow em quatro fases

### Fase 1 · Extrair (dados reais antes de pensar)

Ler [references/extracao-dados.md](references/extracao-dados.md) e reunir dados das 5 fontes:

| Fonte | Rota primaria | Fallback |
|---|---|---|
| Agenda | Google Calendar MCP + Outlook (manual) | Pedir print/lista |
| Tarefas | ClickUp MCP (assignee=Bruno) + filtro de status (whitelist/blacklist) | Pedir lista "Hoje" |
| Workspace M7 | ClickUp MCP (statuses=[atrasada, bloqueada], workspace inteiro) | Pedir resumo por frente |
| Corpo | *Sem MCP* (Garmin removido em v1.3.0) | Sempre perguntar |
| Contexto Pfeffer | Agente `pfeffer-power-analyst` (v1.11.0, fonte unica) | — |

**Regra de ouro:** nunca inventar dado. Se nao conseguir extrair nem obter do usuario, secao vira `—` ou e omitida.

### Fase 2 · Planejar (metodologia antes de texto)

Ler [references/metodologia-planejamento.md](references/metodologia-planejamento.md) e aplicar as 6 regras de decisao:

1. **Lide do dia** — tese argumentativa unica (nao lista descritiva), 200-400 chars
2. **Tres inadiaveis** — Eisenhower Q2 > Eat-the-frog > balance de papeis (>=2 dimensoes), com pre-mortem de 1 linha cada; confirmar status via `AskUserQuestion` se nao estiver na whitelist explicita
3. **Agenda** — capacidade 60/40, bloco >=90min para MIT #1 em 9h-12h (pico cognitivo), almoco obrigatorio
4. **Tarefas ClickUp** — 5-6 visiveis ordenadas ABCDE, "+N" para resto; descartar status na blacklist (cancelada, descartada, etc)
5. **Workspace M7** — agrupadas por frente (lista/sprint), atrasadas + bloqueadas do workspace inteiro, Bruno-as-assignee destacado como gargalo pessoal, max 4-5 grupos
6. **Amanha** — Ancora (1 frase imperativa) + 0-2 bullets de Preparar hoje (<=15min cada)

**Rastreabilidade obrigatoria:** cada numero que aparece no HTML deve ter entrada em `extracao.metricas` com `{metrica, query, count, fonte}`. Contadores sao recalculados a partir das linhas extraidas, nao reusados dos headers da API.

Em paralelo, gerar o **Insight · cruzamento** e as **Notas do dia** invocando sempre o agente [`pfeffer-power-analyst`](../../agents/pfeffer-power-analyst.md) (v1.11.0). O agente e a **unica fonte** de insight e notas do planner — cruza dois capitulos do livro POWER (Pfeffer, Stanford GSB, 2010) em tensao genuina, lendo dias politicos via Cap 1/4/6/7/8/9 e dias operacionais/pessoais via Cap 2/10/11/13. Nao ha mais scan de `brain/3-resources/` — o arquivo [references/insight-cruzamento.md](references/insight-cruzamento.md) agora contem apenas as regras editoriais (formato, tom, anti-padroes) que a saida do agente deve obedecer.

Antes de avancar para Fase 3, validar o **checklist de sanidade** (final de metodologia-planejamento.md).

### Fase 3 · Emitir canonico (.md)

Com o plano validado pelo checklist de sanidade, serializar `extracao` + `plano` em um arquivo .md canonico:

1. Ler [references/schema-md.md](references/schema-md.md) para a especificaçao completa
2. Montar frontmatter YAML com os campos obrigatorios (schema, generated_at, date, weekday, mits, amanha.ancora, pfeffer.chapters) e opcionais (metrics, corpo, agenda, tasks, workspace, amanha.preparar)
3. Escrever body Markdown com os 2 H1 obrigatorios (`# Lide do dia`, `# Insight · cruzamento` com citaçao `> Cap X ↔ Cap Y — POWER (Pfeffer)`) e opcional `# Notas do dia`
4. Aplicar convençao de enfase inline (`*italico*` para enfase narrativa, `**negrito**` para entidades nomeadas) — ver [regras-texto.md](regras-texto.md)
5. Resolver path: `~/Documents/brain/0-inbox/plan-review/daily/YYYY/MM/daily-YYYY-MM-DD.md`
6. Criar diretorios `YYYY/MM/` se nao existirem
7. Escrever o arquivo (sobrescrever se ja existe do dia)
8. Validar o .md recem-emitido contra [schema-md.md §8](references/schema-md.md) antes de avançar

### Fase 4 · Renderizar e publicar

1. Ler o .md recem-criado
2. Parsear frontmatter YAML + body Markdown conforme [references/render-from-md.md](references/render-from-md.md)
3. Ler [references/tokens.css](references/tokens.css) e colar no `<style>` do output
4. Ler [references/principios.md](references/principios.md) antes de decisoes visuais
5. Ler [references/componentes.md](references/componentes.md) para replicar cada componente
6. Usar [references/template-html.html](references/template-html.html) como starter
7. Resolver inlines Markdown (`**strong**` → `<em class="strong">`, `*em*` → `<em>`) conforme [render-from-md.md §3](references/render-from-md.md)
8. Chamar `mcp__cowork__update_artifact({id: 'daily-planner-live', html, mcp_tools: [], update_summary: 'Daily YYYY-MM-DD · N MITs · insight Cap X↔Y'})`
9. Se retornar erro "artifact nao encontrado", chamar `mcp__cowork__create_artifact` com o mesmo id (ver [render-from-md.md §4.2](references/render-from-md.md))
10. **NAO** escrever arquivos .html em `daily/YYYY/MM/` (deprecated em v2)

## Quick reference

| Aspecto | Decisao |
|---|---|
| Canonico | `.md` em `~/Documents/brain/0-inbox/plan-review/daily/YYYY/MM/daily-YYYY-MM-DD.md` |
| Render | HTML no live artifact `daily-planner-live` via `mcp__cowork__update_artifact` |
| Editabilidade | Bruno edita `.md` durante o dia; `/planner sync` re-renderiza |
| Debug | `/planner show` imprime o `.md` do dia no chat |

## Checklist pre-publish

Antes de emitir o HTML final, confirmar:

```
[ ] Dados extraidos reais ou explicitamente perguntados ao usuario (nenhum inventado)
[ ] Lide tem UMA tese argumentativa com 2-4 entidades em <em>
[ ] 3 MITs cobrem >=2 dimensoes (trabalho/corpo/familia)
[ ] MIT #1 e Eat-the-frog (pior/maior/mais adiado)
[ ] Cada MIT tem inadiaveis__risco de 1 linha (causa → plano B)
[ ] Agenda <=60% ocupada em 9h-18h, almoco presente
[ ] MIT #1 tem bloco >=90min reservado em 9h-12h
[ ] Tarefas ClickUp ordenadas ABCDE, cortadas em 5-6 + "+N"
[ ] Nenhuma task na blacklist (cancelada/descartada/won't do/arquivada) aparece no planner
[ ] Tasks em status fora da whitelist destinadas a MIT foram confirmadas via AskUserQuestion
[ ] Tarefas__title-meta mostra `· <lista> · <tag>` (regra da componentes.md s9)
[ ] Coluna 3 (Workspace M7) usa query de status, nao assignee — agrupa por frente
[ ] Tasks com assignee=Bruno na coluna 3 aparecem com modifier `--self` (gargalo)
[ ] Tasks na coluna 3 NAO duplicam com coluna 2 (Tarefas ClickUp)
[ ] Cada numero exibido tem entrada em `metricas` com query e count rastreaveis
[ ] Contadores recalculados a partir de linhas extraidas (nao reusados da API)
[ ] "atrasadas" usa status unico como fonte (nao soma pendente+due-vencido)
[ ] Insight gerado pelo agente `pfeffer-power-analyst` cruza DUAS (nao 3+) perguntas de capitulos do livro POWER em tensao
[ ] Ancora de Amanha cabe em 1 frase imperativa
[ ] Preparar hoje tem 0-2 bullets, cada <=15min hoje
[ ] .md gerado em ~/Documents/brain/0-inbox/plan-review/daily/YYYY/MM/daily-YYYY-MM-DD.md
[ ] Frontmatter YAML passou validaçao de schema (ver schema-md.md §8)
[ ] Body com H1 "Lide do dia" e H1 "Insight · cruzamento" presentes; citaçao Pfeffer no formato `> Cap X ↔ Cap Y — POWER (Pfeffer)`
[ ] `update_artifact` chamado com `id: daily-planner-live` e `mcp_tools: []`
[ ] HTML publicado reflete fielmente o .md (inlines `*em*` e `**strong**` resolvidos)
[ ] Nenhum arquivo .html novo escrito em daily/YYYY/MM/
[ ] Cada KPI do Corpo com valor presente tem `.header__corpo-ref` renderizado (peso/sono: relativo ou "DD mes"; TSS: "seg→hoje"; TSB: "hoje")
[ ] KPI do Corpo com valor null **nao** renderiza `.header__corpo-ref` (simetrico com a tag)
[ ] HTML publicado e viewport-adaptive: `html, body { height: 100vh; overflow: hidden }` presentes no CSS inline
[ ] Agenda renderiza **apenas eventos reais** (nenhum row com `--empty` ou placeholder `—`)
[ ] Meta-footer renderizado ao final do `<body>` com 5 `<span>`: schema, fonte, gerado, skill, insight (campo ausente vira `—`, nunca omitir span)
[ ] `fonte` no meta-footer e path relativo a `~/Documents/brain/` (sem abs path)
```

## Design system snapshot

| Aspecto | Decisao |
|---|---|
| Modo | Dark mode quente nativo (nao ha light mode) |
| Fonte principal | Georgia serif (texto, labels, narrativa) |
| Fonte tabular | Inter sans (horas, numeros em grid) |
| Cor primaria | Terracota #D97757 (trabalho, foco) |
| Cor secundaria | Azul petroleo #6B9EB0 (corpo, treino) |
| Cor alerta | Terracota escuro #B8593C (atraso) |
| Fundo | #1A1715 (escuro quente) |
| Estrutura | Header 5-zone + Body 3-col + Footer 2-col |
| Filosofia | Zero ornamento, hierarquia via tipografia |

## Principios fundadores (leia antes de qualquer output)

1. **Tipografia antes de caixa** — hierarquia por tamanho/peso/italico/cor, nunca por bordas ou cartoes.
2. **Densidade operacional, respiracao editorial** — dados acionaveis densos, narrativa respirada.
3. **Cor e decisao, nao decoracao** — toda cor significa algo (ver tabela de estados).
4. **Dark mode quente nativo** — nunca implementar light mode.
5. **Numero como escultura** — numeros sao protagonistas visuais, nao metadata.
6. **Zero ornamento** — sem icones decorativos, sombras, gradientes, badges ou pills.

## Nunca fazer

- Light mode
- Cartoes elevados ou bordas em torno de secoes
- Icones decorativos (emoji ou SVG) — so texto e italico para enfase
- Sombras, gradientes, blur
- UPPERCASE exceto em labels de dias da semana
- Formatos de data misturados — sempre "16 abril", nunca "16/04" nem "April 16"
- Introduzir cor nova sem redefinir o sistema
- Serif para dados tabulares, sans para texto narrativo
- **Inventar dados** quando a extracao falha (perguntar ao usuario ou omitir)
- **Pre-mortem ficticio** ("risco: tudo pode dar errado") — escrever `risco: —` se nao ha risco real
- **Incluir task em status blacklist** (cancelada, descartada, won't do, arquivada, rejeitada) — mesmo que o ClickUp retorne com `status=aberta`, validar via `date_closed`/`archived`/`status.type`
- **Tratar coluna 3 como "o que eu deleguei"** — o escopo e workspace inteiro; Bruno responde pela saude das frentes, nao so pelo que assinou
- **Usar numero sem rastreabilidade** — todo contador precisa de entrada em `extracao.metricas`. Se nao tem, recalcular ou nao exibir
- **Somar `status=pendente+due-vencido` com `status=atrasada`** — duplica. Usar uma fonte unica (preferencia: status customizado `atrasada`)
- **Emitir .html direto na pasta `daily/YYYY/MM/`** — deprecated em v2. Os `.html` antigos (abril/2026) ficam como historico visual; a v2 nao gera novos
- **Pular a Fase 3 (emissao do .md) e ir direto para o HTML do artifact** — o .md e fonte de verdade, o HTML e derivado. Publicar sem .md viola a arquitetura
- **Chamar `update_artifact` com HTML que nao foi gerado a partir do .md que acabou de ser emitido** — garante fidelidade canonico ↔ render
- **Popular `mcp_tools` no `update_artifact`** — na v2 o artifact e estatico, nao chama MCPs em runtime. `mcp_tools: []` sempre
- **Escrever no campo `edits[]` do frontmatter na Fase 3** — `edits[]` e append-only e emitido apenas por `/planner sync`. A skill base gera `edits: []` ou omite o campo
- **Usar media queries no CSS inline** — a partir da v2.1.0 o template e viewport-adaptive via `clamp()` e unidades `vh`/`vw`. Nenhuma `@media` no `<style>`. Se precisar ajustar para uma resolucao especifica, refinar os ranges do `clamp()` em tokens.css
- **Renderizar horas vazias na agenda** — v2.1.0 emite so eventos reais. Classes `.agenda-enum__hour--empty` e `.agenda-enum__event--empty` estao deprecadas
- **Omitir spans do meta-footer** — sempre 5 spans fixos. Campo ausente vira `—`, nunca `<span>` a menos. A ordem e fixa: schema → fonte → gerado → skill → insight

## Arquivos da skill

```
generating-daily-planner/
├── SKILL.md                       # este arquivo (orquestracao 4 fases)
├── README.md                      # instrucoes de instalacao e uso
└── references/
    ├── extracao-dados.md          # Fase 1 · fontes, MCPs, fallbacks, schema
    ├── metodologia-planejamento.md # Fase 2 · 6 regras + checklist de sanidade
    ├── insight-cruzamento.md      # Fase 2b · regras editoriais do output do agente Pfeffer (v1.11.0)
    ├── schema-md.md               # Fase 3 · spec do .md canonico (frontmatter + body)
    ├── render-from-md.md          # Fase 4 · pipeline parse → render → publish no live artifact
    ├── tokens.css                 # Fase 4 · CSS variables + classes
    ├── tokens.json                # Fase 4 · DTCG format tokens (interop)
    ├── principios.md              # Fase 4 · 6 principios fundadores
    ├── componentes.md             # Fase 4 · 12 componentes especificados
    ├── regras-texto.md            # Fase 4 · tom editorial, labels, convencao de enfase inline
    └── template-html.html         # Fase 4 · starter HTML completo

Agente (pasta `agents/` do plugin):
└── pfeffer-power-analyst.md       # Fonte UNICA de Insight · cruzamento e Notas do
                                    dia (v1.11.0). Sempre invocado na Fase 2b.
                                    Cruza 2 capitulos do livro POWER (Pfeffer, 2010)
                                    em tensao genuina. Cap 1/4/6/7/8/9 para dias
                                    politicos, Cap 2/10/11/13 para dias operacionais
                                    ou pessoais.

Comandos (pasta `commands/` do plugin):
├── sync.md                        # /planner sync — re-renderiza o artifact a partir
│                                    do .md editado manualmente; append em edits[]
└── show.md                        # /planner show — imprime o .md do dia no chat (debug)
```

## Output esperado

Ao aplicar esta skill, o Claude Code deve produzir **dois artefatos sincronizados**:

**1. `.md` canonico** em `~/Documents/brain/0-inbox/plan-review/daily/YYYY/MM/daily-YYYY-MM-DD.md` que:

- Passa na validaçao do schema `daily-planner@1` (ver [schema-md.md §8](references/schema-md.md))
- Foi **planejado** usando as 6 regras de metodologia-planejamento.md (nao so preenchido)
- Foi **extraido** de fontes reais (ou perguntas explicitas ao usuario), sem ficçao
- Serializa `mits[]`, `amanha`, `pfeffer.chapters` como campos obrigatorios no frontmatter
- Inclui body com H1 `# Lide do dia` e H1 `# Insight · cruzamento` (citaçao `> Cap X ↔ Cap Y — POWER (Pfeffer)`)
- Respeita o tom editorial e a convençao inline (`*italico*` para enfase narrativa, `**negrito**` para entidades)

**2. HTML publicado** no live artifact `daily-planner-live` via `mcp__cowork__update_artifact` que:

- Usa apenas as cores definidas em tokens.css
- Usa apenas Georgia (serif) e Inter (sans)
- Segue a estrutura header 5-zone + body 3-col + footer 2-col
- Implementa os 12 componentes + Ancora+Preparar em Amanha + pre-mortem por MIT
- E **fielmente derivado** do .md recem-emitido (inlines Markdown resolvidos, nenhum dado extra)
- Tem `mcp_tools: []` (artifact nao chama MCPs em runtime na v2)

Se o usuario pedir algo que contradiga os principios (ex: "adiciona uns icones legais" ou "faz um modo claro"), a skill deve respeitar o style guide e sinalizar o conflito antes de implementar. Se o usuario pedir "pule o planejamento, so monta o HTML rapido", a skill deve avisar que o output sera raso e pedir confirmaçao antes de pular as Fases 1 e 2. Se o usuario pedir "so regenera o HTML sem mexer em nada", orientar o uso de `/planner sync` (mais rapido, nao re-extrai, nao re-invoca Pfeffer).
