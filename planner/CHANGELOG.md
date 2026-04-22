# Changelog

All notable changes to the Planner plugin will be documented in this file.

## [2.1.1] - 2026-04-22

### Fixed · Comandos `/planner sync` e `/planner show` alinhados com skill v2.1.0

Patch de documentaçao — nenhuma mudança de comportamento obrigatoria, mas os dois comandos estavam omissos em relaçao aos elementos novos introduzidos em v2.1.0 (meta-footer, agenda so-eventos, viewport-adaptive, `corpo.*_ref`).

**`/planner sync`:**

- `description` agora cita o layout v2.1.0 (viewport-adaptive + meta-footer + agenda so-eventos).
- Passo 7 do fluxo explicita 4 sub-requisitos do render: agenda so-eventos, `.header__corpo-ref` por KPI, meta-footer com 5 spans, CSS sem `@media`.
- **Regra critica:** o span `gerado:` do meta-footer usa **`generated_at` original do .md**, nao a hora do sync. `generated_at` registra quando o plano foi concebido; ediçoes vao em `edits[]`. Sem essa regra, o sync erode a semantica do metadado.
- 4 regras novas em "Nunca fazer": nao re-carimbar `generated_at`, nao emitir HTML sem meta-footer, nao regenerar agenda com linhas vazias, nao adicionar `@media` no CSS inline.

**`/planner show`:**

- Resumo ampliado: alem de MITs/agenda/tasks/frentes/edits, agora reporta o status de cada KPI do Corpo (`peso`, `sono`, `tss_semana`, `tsb`) indicando se valor e ref estao preenchidos. Sinaliza com `!` quando valor existe mas ref esta ausente (bug tipico de extracao TrainingPeaks parcial) e com `—` quando valor e null.

### Rationale

O sync herda o pipeline de render via referencia a [render-from-md.md](skills/generating-daily-planner/references/render-from-md.md), entao ele ja seguia os padroes v2.1.0 na pratica. Mas decisoes de escopo do proprio sync (ex: "o que `gerado:` significa quando re-renderizado") moram no comando, nao na skill. Esse patch fecha o gap editorial.

## [2.1.0] - 2026-04-22

### Added · Data de referencia por KPI no Corpo

Cada um dos 4 KPIs do Corpo (peso, sono, TSS sem, TSB) agora exibe a data a que o dado se refere — antes ficava implicito ("peso 103 kg" podia ser de ontem ou de 5 dias atras). Novo elemento `.header__corpo-ref` em Inter sans 9px `text-subtle`, alinhado a direita abaixo do valor:

- **peso** e **sono** → ISO serializado no `.md` como `corpo.peso_ref` / `corpo.sono_ref`, formatado no render como `hoje`, `ontem`, `há Nd` (<=7d) ou `DD mes` (>=8d, ex: `14 abr`).
- **TSS sem** → literal `"seg->hoje"` (janela semanal), renderizado como `seg→hoje`.
- **TSB** → literal `"hoje"` (metrica derivada de agora).

Simetria com a tag: se o valor do KPI e null, a ref tambem e omitida — regra "nunca inventar dado".

Novo formatter `format_rel_or_abs(date_iso, today_iso)` documentado em [render-from-md.md §2.1](skills/generating-daily-planner/references/render-from-md.md).

### Changed · HTML viewport-adaptive (fit 100% sem media queries)

O template e o `tokens.css` foram refatorados para caber em qualquer viewport (vertical + horizontal) sem `@media` queries, usando `clamp()` em tipografia/zonas e unidades `vh` em gaps/paddings:

- **Reset viewport-lock:** `html, body { height: 100vh; width: 100vw; overflow: hidden }` + `* { min-width: 0; min-height: 0 }` (libera flex children).
- **Tipografia fluida:** `--fs-display`, `--fs-roman`, `--fs-h2`, `--fs-body`, `--fs-body-sm` passam a usar `clamp(min, vw, max)`. Novo token `--fs-tiny: clamp(9px, 0.7vw, 10px)` para metadata.
- **Zonas do header fluidas:** `--zone-dia`, `--zone-insight`, `--zone-mes`, `--zone-corpo`, `--zone-amanha` com `clamp()`.
- **Body absorvente:** `.body { flex: 1 1 auto; min-height: 0; overflow: hidden }` garante que a area central ocupe exatamente o espaco entre header e footer. Colunas com `height: 100%; overflow: hidden`.
- **Espacamentos verticais em vh:** `.agenda-enum { gap: clamp(3px, 0.45vh, 6px) }`, `.footer { padding-top: clamp(8px, 1vh, 14px); flex-shrink: 0 }`.

### Changed · Agenda so renderiza eventos reais

A partir da v2.1.0 a agenda emite **uma `.agenda-enum__row` por item real** de `agenda[]`. Linhas vazias com placeholder `—` (faixa 07:00-19:00 de hora em hora) nao sao mais geradas. Reduz ~50% da altura da coluna e viabiliza o fit 100%. Modifier `.agenda-enum__row--gap` aplicado quando ha pulo >=2h entre eventos consecutivos, para criar respiro visual sem row vazia. Classes `.agenda-enum__hour--empty` e `.agenda-enum__event--empty` ficam no CSS como retro-compatibilidade mas estao deprecadas.

### Added · Meta-footer de rastreabilidade

Nova linha discreta ao final do `<body>` com 5 metadados em Inter sans 9-10px `text-subtle`:

```
schema: daily-planner@1   fonte: 0-inbox/plan-review/daily/2026/04/daily-2026-04-22.md   gerado: 2026-04-22T08:15:00-03:00   skill: planner:generating-daily-planner v2.1.0   insight: Pfeffer Cap 11x13
```

Ordem fixa (`schema → fonte → gerado → skill → insight`). Sempre 5 `<span>`; campo ausente vira `—`, nunca omitir. `fonte` e path relativo a `~/Documents/brain/` (nao vaza abs path). Permite que qualquer leitor do HTML publicado saiba a origem canonica sem abrir o `.md`.

### Changed · Schema `daily-planner@1` ganha campos opcionais

Backward-compatible — nenhum `.md` historico precisa ser migrado:

- `corpo.peso_ref`, `corpo.sono_ref` (ISO `YYYY-MM-DD`), `corpo.tss_ref` (literal `"seg->hoje"`), `corpo.tsb_ref` (literal `"hoje"`).

Regras de valor e validaçao em [schema-md.md §4](skills/generating-daily-planner/references/schema-md.md).

### Changed · SKILL.md checklist + nunca fazer

- 6 itens novos no checklist pre-publish (ref do Corpo, viewport-lock, agenda so-eventos, meta-footer com 5 spans, path relativo).
- 3 regras novas em "Nunca fazer" (media queries no inline CSS, renderizar horas vazias, omitir spans do meta-footer).

### Files touched

- [references/tokens.css](skills/generating-daily-planner/references/tokens.css) — viewport lock, tipografia/zonas fluidas, `.body`/`.body__col` absorventes, novo `.header__corpo-ref`, novo `.meta-footer`.
- [references/template-html.html](skills/generating-daily-planner/references/template-html.html) — 4 rows vazias da agenda removidas, ref adicionada nas 4 rows do Corpo, meta-footer antes do `</body>`.
- [references/componentes.md](skills/generating-daily-planner/references/componentes.md) — §5 Corpo atualizada com ref, §7 Agenda reescrita (so-eventos), nova §13 Meta-footer.
- [references/schema-md.md](skills/generating-daily-planner/references/schema-md.md) — campos `corpo.*_ref` + regras de valor + fallback matrix.
- [references/extracao-dados.md](skills/generating-daily-planner/references/extracao-dados.md) — §4 tabela de rotas TrainingPeaks ganha coluna "Data de referencia".
- [references/render-from-md.md](skills/generating-daily-planner/references/render-from-md.md) — §2.1 formatter `format_rel_or_abs`, §2.2 agenda so-eventos (pseudocodigo), §2.3 meta-footer (pseudocodigo).
- [SKILL.md](skills/generating-daily-planner/SKILL.md) — checklist + nunca fazer.

### Migration

Nao-breaking. Proximo run da skill regenera `.md` e artifact ja no novo layout. `.md` historicos sem `corpo.*_ref` continuam validos (campos opcionais). Artifact `daily-planner-live` passa a ter meta-footer a partir do proximo publish.

## [2.0.0] - 2026-04-22

### Changed · Daily planner: `.md` canonico + live artifact (arquitetura dupla)

**BREAKING.** A skill `generating-daily-planner` deixa de emitir `.html` direto na pasta e passa a produzir dois artefatos sincronizados:

1. **Arquivo `.md` canonico** (fonte unica de verdade) em `~/Documents/brain/0-inbox/plan-review/daily/YYYY/MM/daily-YYYY-MM-DD.md` — frontmatter YAML com dados estruturados + body Markdown com narrativa (Lide, Insight, Notas). Editavel durante o dia pelo Bruno.
2. **HTML publicado no live artifact `daily-planner-live`** via `mcp__cowork__update_artifact`, derivado do `.md`. Estatico por natureza — nao chama MCPs em runtime (`mcp_tools: []`).

O workflow passa de **3 fases** (extrair → planejar → renderizar) para **4 fases** (extrair → planejar → emitir `.md` → renderizar+publicar). A mutabilidade do planner agora e **explicita** (editar .md + `/planner sync`), nao automatica.

**Racional:** planejamento do dia e artefato estatico — nao deveria se reescrever sozinho quando o sidebar abre. Separar canonico (editavel) de render (derivado) torna o `.md` pesquisavel, versionavel e editavel em qualquer editor Markdown, mantendo a consistencia visual do live artifact.

**Migraçao (nao automatica):** `.html` antigos em `daily/YYYY/MM/` ficam como historico visual. Proximos dias sao gerados apenas como `.md` + artifact.

### Added · Referencias novas na skill daily

- [references/schema-md.md](skills/generating-daily-planner/references/schema-md.md) — spec completo do `.md` canonico: path, campos obrigatorios (`schema: daily-planner@1`, `mits[]` de 3 itens, `amanha.ancora`, `pfeffer.chapters`), opcionais (`metrics`, `corpo`, `agenda`, `tasks`, `workspace`, `amanha.preparar`), convençao de enfase inline (`*em*` / `**strong**`), algoritmo de validaçao (§8), e o novo campo `edits[]` append-only para historico de ediçoes.
- [references/render-from-md.md](skills/generating-daily-planner/references/render-from-md.md) — pipeline parse → mapeamento YAML→componentes → resolucao de inlines Markdown → publicaçao via `update_artifact`. Documenta erros comuns e o `update_summary` convencionado.

### Added · Campo `edits[]` no frontmatter

Historico append-only de ediçoes manuais registradas pelo `/planner sync`. Cada entrada: `{at: ISO-8601, summary: string}`. Util para retrospectiva semanal (ver quais MITs foram concluidas ao longo do dia vs empurradas). Skill base nao toca esse campo — so o `/sync` anexa.

### Added · Comando `/planner sync`

Novo em [commands/sync.md](commands/sync.md). Re-renderiza o `daily-planner-live` a partir do `.md` editado manualmente, sem re-extrair dados nem re-invocar o agente Pfeffer. Roda em <5s. Detecta diff em relaçao ao snapshot anterior e faz append em `edits[]`. Aborta se o `.md` do dia nao existe (orienta rodar a skill completa) ou se o artifact nao existe (nao cria — so publica).

### Added · Comando `/planner show`

Novo em [commands/show.md](commands/show.md). Imprime o `.md` canonico do dia no chat em code fence + resumo rapido (contagens, ultima ediçao, campos ausentes). Read-only, sem efeitos colaterais. Util para debug e inspeçao.

### Changed · SKILL.md e referencias auxiliares

- [SKILL.md](skills/generating-daily-planner/SKILL.md) — renomeada seçao "Workflow em tres passadas" → "Workflow em quatro fases". Nova Fase 3 (emitir `.md`) e Fase 4 (renderizar+publicar) substituem a antiga Fase 3 (renderizar HTML direto). Checklist "pre-render" virou "pre-publish" com 5 items novos (path do .md, validaçao de schema, blocos obrigatorios do body, update_artifact com `mcp_tools: []`, nenhum .html novo). "Nunca fazer" ganhou 5 regras sobre a nova arquitetura.
- [references/extracao-dados.md](skills/generating-daily-planner/references/extracao-dados.md) — adicionada seçao "Output final da Fase 1 (v2)" mapeando `extracao.*` → campos YAML.
- [references/metodologia-planejamento.md](skills/generating-daily-planner/references/metodologia-planejamento.md) — adicionada seçao "Output final da Fase 2 (v2)" mapeando `plano.*` → frontmatter + body.
- [references/regras-texto.md](skills/generating-daily-planner/references/regras-texto.md) — adicionada seçao "Convençao de enfase no .md canonico" com tabela `*em*` / `**strong**`, exemplos e anti-patterns.

### Changed · Weekly planner nao migrou ainda

O weekly planner (`generating-weekly-planner`) mantem a arquitetura v1.x de emitir HTML direto. Migraçao analoga planejada para v2.1+.

### Removed

- Nenhum arquivo deletado. `.html` antigos em `~/Documents/brain/0-inbox/plan-review/daily/2026/04/` (16, 17, 20) permanecem como historico visual.

### Validation

- Exemplo de validaçao em `~/Documents/brain/0-inbox/plan-review/daily/2026/04/daily-2026-04-22.md` criado antes da skill (fonte: brief do usuario) — passa nas regras de [schema-md.md §8](skills/generating-daily-planner/references/schema-md.md).
- Artifact `daily-planner-live` ja publicado no Cowork com HTML simplificado (sem `callMcpTool`, sem loaders) na sessao de 2026-04-22 que originou este brief.

### Open questions (deferidas para v2.1+)

- Imagens/screenshots em `# Notas do dia` via `![alt](path)` (fora do escopo v2).
- Script de validaçao standalone para conferir schema de qualquer `.md` historico.
- Migraçao do weekly planner para o mesmo modelo `.md` + artifact.
- Exportaçao para PDF via pandoc ou vault Obsidian com backlinks.

## [1.11.0] - 2026-04-17

### Changed · Pfeffer como **fonte unica** de Insight e Notas (simplificacao editorial)

Consolidacao do agente `pfeffer-power-analyst` (introduzido em v1.10.0 como **alternativa** condicional para dias com sinais politicos fortes) como **fonte unica** de Insight · cruzamento e Notas do dia em ambos os planners (daily e weekly). O caminho dual do v1.10 — "Pfeffer para dias politicos, scan de `brain/3-resources/` para dias operacionais" — foi descontinuado.

**Racional editorial (commitment):**

- O planner ja e committed a um design system nao-configuravel (Editorial Noturno — dark mode quente, Georgia + Inter, tokens fixos). A partir de v1.11.0, o Insight passa a ter o mesmo nivel de commitment — Pfeffer nao e "framework do dia que Bruno escolhe"; e **a** lente.
- Consistencia diaria cria leitura acumulada. 90 dias lendo o trabalho atraves do mesmo livro ensina mais que 90 frameworks diferentes. Ao ler Pfeffer aplicado a uma reuniao real na segunda e outra na terca, Bruno nao esta estudando Pfeffer — esta **usando**.
- A lente cobre dias politicos **e** operacionais/pessoais — ver atualizacoes no agente abaixo.
- Evita a armadilha "qualquer tarefa vira justificativa para invocar qualquer framework". O planner nao e biblioteca rotativa — e diario editorial.

### Changed · Agente `pfeffer-power-analyst` expandido para cobrir qualquer dia

Description e body do agente atualizados para remover o conceito de "quando NAO usar este agente". O agente agora cobre qualquer horizonte:

- **Dias politicos** (reuniao com superior, oposicao, apresentacao, posicionamento) — leitura via Cap 1/4/6/7/8/9
- **Dias de price-of-power** (sobrecarga, gargalo pessoal, overcommitment) — leitura via Cap 10/11 cruzado com Cap 2
- **Dias de recovery ou pessoais** (fim de semana, familia, treino, leitura) — leitura via Cap 2 (energia/ambicao) × Cap 10 (autonomia recuperada) × Cap 13 (showing up)
- **Dias pos-setback** (reuniao anterior deu ruim, projeto foi rejeitado) — Cap 9 × Cap 11 (nao desistir × nao sobrecompensar)

**Novo mapa de cruzamentos** na secao "Passo 2" do agente inclui 16 combinacoes agenda-tipo → 2 capitulos com tensao, cobrindo desde "apresentacao para superior" ate "almoco com familia" e "dia de treino longo".

**Unico limite restante:** input incompleto. Se a agenda, MITs ou retrospectiva nao foram extraidos, o agente pede o dado especifico em vez de produzir analise fictícia. Pfeffer e empirico — sem dado, sem analise.

### Changed · Documentos de referencia reescritos

**`references/insight-cruzamento.md` (daily + weekly):** nao descreve mais um processo de geracao (os antigos 7 passos de scan em `brain/3-resources/` foram removidos). Agora contem apenas:

- Racional do commitment editorial (por que Pfeffer como fonte unica)
- Formato do Insight (estrutura gramatical, linha de citacao `POWER · Cap X × Cap Y`, extensao 150-250 chars daily / 200-350 chars weekly)
- Formato das Notas do dia (componente `.note`, 30-80 chars, acionavel, com hora quando ancorado a evento)
- Formato do bloco opcional `## Riscos Pfeffer` (weekly) que alimenta Regra 6
- Regras editoriais (2 capitulos, tensao, rotacao, pt-BR com vocabulario Pfeffer em ingles quando natural)
- Anti-padroes
- 4 exemplos validados cobrindo dia politico, dia operacional, dia familia, dia pos-setback (+ 3 exemplos para weekly)

**`references/extracao-dados.md` (daily secao 5, weekly secao 7):** reescritas. Nao ha mais scan de `brain/3-resources/`. Documentam apenas **quais inputs a Fase 1 deve montar** para o agente Pfeffer conseguir rodar na Fase 2b.

**`SKILL.md` (daily + weekly):** descricoes, tabelas da Fase 1, workflow Fase 2b, checklists pre-render, lista de arquivos e sumario "Output esperado" atualizados para refletir invocacao sempre do agente.

### Removed

- Processo de 7 passos para gerar Insight via scan de `brain/3-resources/` (descontinuado; regras de formato preservadas)
- Conceito de "Atalho Pfeffer" (v1.10.0) — Pfeffer agora e o caminho unico, nao um atalho
- Secao "Quando NAO usar este agente" da description e body do agente (substituida por "Limite unico: dados insuficientes")
- Campo `contexto_insight` (com `temas` + `candidatos_3resources`) do schema de extracao — substituido por `contexto_pfeffer` documental

### Notes

- Esta versao e **minor** (1.10 → 1.11) porque nao remove capacidades publicas: todo HTML gerado continua valido, todas as classes CSS continuam intactas, o fluxo de 3 fases se mantem. O que muda e a fonte de conteudo do Insight + Notas — uma escolha editorial, nao uma mudanca de API.
- Semanas/dias que anteriormente teriam insight de `brain/3-resources/` agora tem insight de Pfeffer Cap 2/10/11/13 (dias operacionais). Nada fica vazio. Nada invent.
- Se em algum dia especifico Bruno quiser insight de outro framework, deve pedir fora da skill (ex: "gera so o insight de hoje usando Shape Up"). A skill nao suporta mais essa opcao como caminho oficial.

## [1.10.0] - 2026-04-17

### Added · Novo agente `pfeffer-power-analyst`

Primeiro agente do plugin planner. Especializado em analise de dinamicas de poder organizacional baseado no livro **POWER: Why Some People Have It — and Others Don't** (Jeffrey Pfeffer, Stanford GSB, 2010). Localizado em `agents/pfeffer-power-analyst.md`.

**Funcao:** analisar a agenda do dia ou semana atraves das lentes do livro de Pfeffer e retornar Markdown estruturado pronto para os campos **Insight · cruzamento** e **Notas do dia** dos planners (daily e weekly).

**Design:**
- Ferramentas read-only (Read, Grep, Glob) — principio do menor privilegio. O agente nao escreve no HTML; retorna Markdown que a skill do planner incorpora.
- Modelo: `opus`. Analise de dinamicas de poder exige nuance e cruzamento de frameworks.
- System prompt carrega inventario completo dos 13 capitulos do livro com conceitos-chave, mapa de cruzamentos frequentemente uteis (agenda-tipo → 2 capitulos com tensao), exemplo completo de entrada e saida, e anti-padroes.
- Voz descritiva nao-prescritiva. Pfeffer e explicito: *"the world is not a just place — don't wish it were different, understand it"*. O tom do agente carrega essa disposicao.

**Quando e invocado:**
- Daily: quando agenda contem reuniao com superior, 1:1 com subordinado em oposicao, apresentacao para audiencia externa, decisao de posicionamento, ou gargalo pessoal no workspace M7 (>=3 atrasadas de Bruno).
- Weekly: quando retro S-1 menciona oposicao, semana tem >=3 reunioes com superiores, apresentacao externa de alto risco, ou decisao consequente de posicionamento politico.

**Output estruturado (Markdown):**
- `## Insight · cruzamento` — tese argumentativa cruzando 2 capitulos em tensao
- `## Notas do dia` — 1-3 notas taticas em bullets compativeis com componente `.note`
- `## Riscos Pfeffer` (weekly, opcional) — pre-mortem tatico alimenta Regra 6 da metodologia
- `## Rastro` — auditoria dos sinais lidos e capitulos descartados

**Integracao com as skills existentes:**
- `generating-daily-planner/SKILL.md`: Fase 2b ganha **atalho Pfeffer** como alternativa ao `insight-cruzamento.md` padrao quando agenda tem sinais politicos fortes.
- `generating-daily-planner/references/insight-cruzamento.md`: nova secao "Atalho Pfeffer" com criterios de invocacao e anti-padroes (quando NAO usar).
- `generating-weekly-planner/SKILL.md`: Fase 2 ganha trigger equivalente para horizonte semanal.
- `generating-weekly-planner/references/insight-cruzamento.md`: nova secao "Atalho Pfeffer" especifica para horizonte semanal.
- `generating-weekly-planner/references/metodologia-planejamento.md` Regra 6 (Riscos & fogos): agente alimenta pre-mortem com leituras Pfeffer quando relevante.

### Notes

- O agente nao substitui o `insight-cruzamento.md` padrao — coexiste como alternativa especializada para dias/semanas com conteudo politico dominante. Dias puramente operacionais continuam usando scan de `brain/3-resources/`.
- System prompt e extenso (~300 linhas) por design: agentes rodam em contexto isolado sem acesso ao livro; o inventario dos 13 capitulos no prompt garante aplicacao especifica (capitulo + conceito) em vez de conselho generico.
- Memoria do agente nao foi ativada nesta versao. Pode ser adicionada em v2.0.0 se o uso indicar valor em lembrar padroes recorrentes de Bruno (rede, opositores conhecidos, tolerancia a conflito).

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
