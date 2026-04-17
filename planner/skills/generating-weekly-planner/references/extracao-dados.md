# Fase 1 · Extracao de dados (horizonte semanal)

A primeira passada da skill e **levantamento** do que sera a proxima semana. Antes de planejar a orquestracao dos 5 dias, o Claude reune entradas de 7 fontes. Para cada fonte ha uma rota primaria (MCP direto) e um fallback (perguntar ao usuario).

**Regra de ouro:** nunca invente dado. Se nao conseguir extrair e o usuario nao forneceu, a secao correspondente no HTML fica com `&mdash;` ou e omitida — nunca preenchida com ficcao.

**Particularidade weekly:** a **Retrospectiva da semana passada** e sempre perguntada — e o que diferencia um weekly preview de um summary descritivo. Sem ela, a Tese da semana vira generica.

## Indice

- [Matriz de fontes](#matriz-de-fontes)
- [Janela temporal alvo](#janela-temporal-alvo)
- [1. Agenda (5 dias)](#1-agenda-5-dias)
- [2. Tarefas ClickUp (semana)](#2-tarefas-clickup-semana)
- [3. Delegadas (horizonte semanal)](#3-delegadas-horizonte-semanal)
- [4. Corpo · semana (TrainingPeaks MCP)](#4-corpo--semana-trainingpeaks-mcp)
- [5. Metas Q2 (conexao trimestral)](#5-metas-q2-conexao-trimestral)
- [6. Retrospectiva S-1 (sempre perguntar)](#6-retrospectiva-s-1-sempre-perguntar)
- [7. Contexto para o insight](#7-contexto-para-o-insight)
- [Protocolo de fallback](#protocolo-de-fallback)
- [Schema da extracao](#schema-da-extracao)

## Matriz de fontes

| Secao do planner | Fonte primaria | MCP / Ferramenta | Fallback |
|---|---|---|---|
| Agenda (5 dias) | Google Calendar + Outlook M7 | `mcp__claude_ai_Google_Calendar__list_events` · *Outlook sem MCP* | Pedir print ou lista |
| Tarefas da semana | ClickUp (due <= sex, assignee=Bruno) | `mcp__claude_ai_ClickUp__clickup_filter_tasks` | Pedir lista |
| Delegadas | ClickUp (assignee != Bruno, criadas por Bruno, status aberto) | `mcp__claude_ai_ClickUp__clickup_filter_tasks` | Pedir resumo verbal |
| **Corpo · semana** | **TrainingPeaks MCP** (v1.5.0+) | `tp-mcp` (weight, sleep, HRV, weekly_summary, fitness_metrics) | Perguntar se MCP falhar |
| **Metas Q2** | ClickUp goals → `brain/3-resources/` → perguntar | `mcp__claude_ai_ClickUp__clickup_get_workspace_hierarchy` + `clickup_search` | Perguntar confidence por objetivo |
| **Retrospectiva S-1** | *Sempre perguntar ao usuario* | — | — (e a propria fonte) |
| Contexto insight | Filesystem `brain/3-resources/` (PARA) | `Glob`, `Grep`, `Read` | Pular insight se vazio |

## Janela temporal alvo

Antes de extrair, definir a semana alvo:

**Regra de default:**
- Se invocado entre **seg-qui**: semana alvo = semana atual (dias restantes + ja passados como contexto)
- Se invocado **sex a tarde, sabado, domingo**: semana alvo = proxima semana (S+1)
- Se usuario especificar ("weekly da S18"): usar a especificada

**Janela de 5 dias:**
```
ano-ISOweek: segunda 00h → sexta 23h59
```

Usar formato ISO week (semana 1 = primeira semana com 4+ dias em janeiro). Para 2026, semana 16 = 13-17 abril (seg-sex), semana 17 = 20-24 abril.

**Confirmar com usuario antes de extrair:**

> Weekly para qual semana? Default: **S{N} · {dd/mm} a {dd/mm}** (proxima semana util). Me confirma ou me passa outra.

## 1. Agenda (5 dias)

### Rota primaria · Google Calendar

```
mcp__claude_ai_Google_Calendar__list_events (
  timeMin=segunda_00h,
  timeMax=sexta_23h59,
  calendar=primary
)
```

Extrair por evento: `start`, `end`, `summary`, `location`, `attendees` (se relevante).

**Agrupar por dia** apos extracao:
```
agenda_por_dia:
  seg: [evento1, evento2, ...]
  ter: [...]
  qua: [...]
  qui: [...]
  sex: [...]
```

### Rota primaria · Outlook M7

**Nao ha MCP para Outlook.** Pedir ao usuario:

> Nao consigo ler o Outlook M7 direto. Me cola um print/lista da agenda da semana, ou lista os eventos no formato `SEG 13 · HH:MM - titulo` (uma linha por evento).

### Regra de consolidacao

Se os dois calendarios retornam eventos, mesclar por dia+horario. Conflitos (mesmo horario, dois eventos) viram material para o Preflight ("onde vou dizer nao?") ou para os Riscos.

### Regra de densidade por dia

Classificar cada dia pela densidade de meetings:
- **Dia protegido (maker day)**: <=1 meeting de 30min → candidato a deep work bloco 4h+
- **Dia normal**: 2-4 meetings
- **Dia cheio**: 5+ meetings → nao colocar MIT #1 aqui

Essa classificacao informa a Regra 3 da metodologia (Orquestra dos 5 dias).

## 2. Tarefas ClickUp (semana)

### Rota primaria

```
mcp__claude_ai_ClickUp__clickup_filter_tasks (
  assignees=[Bruno],
  statuses=open,
  due_date_lt=sexta_23h59  # alvo + nao passar do fim de semana
)
```

Filtrar o resultado em dois grupos:

**Grupo A · Candidatos a Big 3 / Tres grandes** (5-10 tasks)
- Tags contem `big3`, `mit`, `semana`, `urgente`, `critico`, OU
- Vinculadas a Metas Q2 (se houver linkage), OU
- Lista de origem tem peso estrategico (nao helpdesk), OU
- Prioridade = urgent/high com impacto multi-projeto

**Grupo B · Tarefas com prazo na semana** (resto, ate 20 linhas)
- Todas as demais due <= sexta ou atrasadas

**Grupo C · Prazos duros (subset de A+B)** — tasks com SLA amarrado a data:
- Entregas externas, compromissos com terceiros
- Reunioes com preparo critico
- Marcos de projeto amarrados a dia especifico

### Metadata obrigatoria por task

Para cada task:
- `id` (ex: `TSM-874`)
- `title`
- `list_name` (nome da lista)
- `tags[]`
- `due_date` (usado para ancorar ao dia da semana)
- `priority` (urgent/high/normal/low)
- `status`
- `linked_goal` (Meta Q2 vinculada, se houver)

### Fallback

Se ClickUp MCP falhar:

> Nao consegui extrair as tarefas do ClickUp. Voce pode me dar:
> 1. Os 3 candidatos a **Weekly Big 3** (titulo + lista + conexao com Q2)
> 2. Uma lista de **prazos duros** da semana (task + dia especifico)
> 3. Uma lista curta (ate 10) de outras tarefas com due ate sexta

## 3. Delegadas (horizonte semanal)

### Rota primaria

```
mcp__claude_ai_ClickUp__clickup_filter_tasks (
  assignees=[NOT Bruno],  # filtrar pos-query
  created_by=Bruno,
  statuses=open,
  due_date_lt=sexta_proxima_semana  # horizonte semanal + buffer
)
```

**Agrupar por projeto/lista**. Ordenar cada grupo por atraso (atrasadas no topo). Limite: **4-5 grupos**, 2-3 linhas por grupo.

### Metadata obrigatoria

- `title`
- `assignee` (nome) — vira display `· <pessoa>`
- `project` ou `list_name` — cabecalho do grupo
- `due_date`
- `status`

### Filtro weekly-especifico

Na weekly, incluir apenas delegadas que:
- Tem due date dentro da semana alvo OU atrasadas, OU
- Bloqueiam tarefas da propria semana (dependencia), OU
- Tem SLA de follow-up na semana (ex: "aguardando resposta ha 5d")

Delegadas distantes (due em 3 semanas) ficam fora — nao sao decisao desta weekly.

### Fallback

> Nao consegui extrair as delegadas. Me passa um resumo por projeto:
> - [Projeto X] 2-3 tarefas · pessoa · due
> - [Projeto Y] ...

## 4. Corpo · semana (TrainingPeaks MCP)

**Fonte primaria: TrainingPeaks MCP** (adicionado na v1.5.0 do plugin). Restaura a automacao que havia sido removida em v1.3.0 quando o Garmin foi descontinuado.

### Tools TP mapeadas para os 4 KPIs semanais

| KPI | TP tool | Calculo |
|---|---|---|
| **peso Δ** | `weight` | weight(sex) - weight(seg-1) = delta semanal em kg |
| **TSS total** | `weekly_summary` | TSS acumulado seg-sex (tool ja agrega) |
| **sono medio** | `sleep` | media de horas dormidas seg-1 a qui (noites que precedem cada weekday) |
| **TSB (forma)** | `fitness_metrics` | Training Stress Balance atual (CTL - ATL) |

Opcionalmente tambem capturar:
- `HRV` medio da semana (nao exibido por default, mas util como contexto)

### Chamadas TP sugeridas

```
# Peso inicial e final
weight(date=segunda_semana_anterior_fim)
weight(date=sexta_semana_alvo)  # ou atual se weekly e feito no meio

# Agregados da semana
weekly_summary(week_start=segunda_semana_alvo)
# retorna: total_tss, sessions_count, total_duration, sports_breakdown

# Sono nos 5 dias
sleep(date_range=seg_a_qui_semana_alvo)  # noites antes de cada weekday
# calcular media

# Forma atual
fitness_metrics(date=today)  # retorna CTL, ATL, TSB
```

### Regras de cor do numero (ver [componentes.md](componentes.md) e tokens.css)

Aplicadas apos extracao, antes de renderizar:

- **peso Δ** → default `--text-primary` (neutro) · se delta > 1kg → `--alert`
- **TSS total** → `--body` (azul petroleo, performance)
- **sono medio** < 7h → `--alert` (terracota escuro)
- **sono medio** >= 7h → `--body` (azul petroleo)
- **TSB** positivo → `--body` (em forma / recuperado)
- **TSB** entre -10 e 0 → default (neutro — carga controlada)
- **TSB** < -10 → `--alert` (fadiga, precisa recovery)

### Fallback

Se o TP MCP falhar ou auth expirar:

> Nao consegui extrair os dados do TrainingPeaks (MCP pode ter falhado ou cookie expirou). Pra preencher a Corpo · semana, me passa:
> - peso Δ (delta kg entre inicio e fim da semana — pode deixar vazio)
> - TSS total da semana (numero unico)
> - sono medio (horas, media seg a qui)
> - TSB atual (se souber — positivo em forma, negativo fadiga)

Campos nao fornecidos viram `&mdash;` no HTML.

### Renovacao de cookie

Se o erro for `auth expired` ou `401`, ligar o usuario para:
```bash
tp-mcp auth
# ou (bypass getpass para IDE terminals):
pbpaste | python ~/.local/bin/tp-mcp auth
```

## 5. Metas Q2 (conexao trimestral)

**Principio:** Weekly Big 3 devem **derivar** de Metas Q2. Sem essa conexao, Big 3 sao so tarefas grandes — nao Big 3.

### Rota primaria · ClickUp goals

```
mcp__claude_ai_ClickUp__clickup_get_workspace_hierarchy
# Procurar "Goals" ou "Metas 2026" ou "Q2 2026"

mcp__claude_ai_ClickUp__clickup_search (
  query="Q2 2026 metas"
)
```

Extrair 2-4 objetivos Q2 com:
- Titulo do objetivo
- Key results (se existirem)
- Progresso atual (% ou etapa)
- Confidence (0-100%) — se ClickUp nao tiver, perguntar

### Rota secundaria · Filesystem

Se ClickUp nao retornar, procurar em `brain/3-resources/`:

```
Glob: brain/3-resources/**/metas*2026*.md
Glob: brain/3-resources/**/q2*.md
Glob: brain/3-resources/**/okr*.md
```

Ler ate 2-3 arquivos candidatos. Extrair os 2-4 objetivos Q2.

### Fallback · Perguntar

Se as duas rotas falharem:

> Quais as suas Metas Q2 ativas nesta semana? Me passa 2-4 objetivos no formato:
> - Titulo do objetivo · confidence atual (0-100%) · etapa atual
>
> Exemplo:
> - Publicar m7-controle em 3 verticais · 65% · fase E6
> - Desdobrar metas 2026 · 30% · SQL consorcios parado (em risco)
> - Maratona junho sub-4h · 50% · bloco de volume OK

### Regra de coloracao (ver componentes)

- Confidence >= 60% → default (verde neutro / ok)
- Confidence 40-60% → `--body` (atencao, ainda da)
- Confidence < 40% → `--alert` (em risco, rever)

## 6. Retrospectiva S-1 (sempre perguntar)

**A peca-chave do weekly preview.** Sem saber o que aconteceu na semana que termina, a Tese da proxima vira generica.

### Pergunta padronizada

No inicio da Fase 1 (antes de extrair MCPs), perguntar:

> Antes de preparar a S{N}, retrospectiva rapida da S{N-1} (~2 min):
>
> 1. **Destravou**: o que rolou bem / que vitoria voce teve? (1-3 linhas)
> 2. **Travou**: o que nao saiu ou patinou? (1-3 linhas)
> 3. **Aprendi**: alguma licao que muda como voce encara a proxima? (1 linha, opcional)
>
> Pode responder em prosa livre — vou estruturar depois.

### Uso na Fase 2

- **Tese**: o "destravou" alimenta o argumento de continuidade ("apos fechar X na S-1, a S{N} usa esse destravamento para avancar Y")
- **Riscos**: o "travou" vira entrada para o pre-mortem (se patinou por motivo Z, Z vira risco mapeado)
- **Criterio de vitoria**: o "aprendi" informa o que precisa ser diferente

### Anti-padrao

Nao pular essa pergunta mesmo se o usuario pedir rapidez. Sem retrospectiva, avisar:

> Sem retrospectiva da S-1, o weekly vai ficar generico — a Tese perde ancoragem. Voce pode me passar rapido 1-2 frases de "o que destravou" e "o que travou"? Se nao tiver nada, posso seguir mas a qualidade cai.

## 7. Contexto para o insight

Fonte unica: **filesystem `/Users/bchiaramonti/Documents/brain/3-resources/`**.

Essa extracao e preguicosa — nao le os arquivos ainda, apenas inventaria. A leitura real acontece na geracao do insight (ver [insight-cruzamento.md](insight-cruzamento.md)).

### Passo 1 · Identificar tensionamentos da semana

A partir da **Tese** + **Big 3** + **Riscos** (ja planejados na Fase 2), derivar 2-3 **temas** estrategicos da semana. Nao sao tarefas — sao **dilemas**.

Exemplos:
- Tese "fechar m7-controle com diretoria" → tensionamento `validacao-vs-autonomia` (aprovar para liberar vs continuar iterando)
- Big 3 "desdobrar metas Q2" → tensionamento `rigor-metrico-vs-flexibilidade-estrategica`
- Riscos "SQL consorcios parado no Rafa" → tensionamento `delegacao-vs-fazer-eu-mesmo`

### Passo 2 · Inventariar subdiretorios relevantes em 3-resources

```
Glob: brain/3-resources/**/*.md
```

Filtrar por caminhos/nomes que contenham os tensionamentos (case-insensitive, stem matching). Limite: ate 10 candidatos.

### Passo 3 · Passar o inventario para a fase de Insight

Saida:
```yaml
tensionamentos: [validacao-vs-autonomia, delegacao-vs-fazer-eu-mesmo]
candidatos:
  - brain/3-resources/lideranca/situational-leadership-hersey.md
  - brain/3-resources/metodologias/shape-up-basecamp.md
  - brain/3-resources/livros/radical-candor.md
```

## Protocolo de fallback

Regras gerais quando um MCP falha ou retorna vazio:

1. **Tentar 1 vez com parametros mais frouxos** (ex: ampliar janela temporal)
2. **Se ainda falhar, perguntar ao usuario** com pergunta especifica
3. **Nunca inventar.** Na duvida, secao fica com `&mdash;` ou e totalmente omitida
4. **Sinalizar a origem no rodape do HTML** (comentario opcional): `<!-- TP offline, Corpo perguntado -->`

`★ Exemplo de pergunta especifica ───────────────`
Ruim: "me passa os dados da semana"

Bom: "A tool weekly_summary do TP nao respondeu. Me passa o TSS total da semana passada (se lembrar) e a contagem de treinos — default para o TSS e 250-350 numa semana base, 400+ numa semana all-in."
`──────────────────────────────────────────────────`

## Schema da extracao

Saida consolidada apos Fase 1 (estrutura interna, nao HTML):

```yaml
semana:
  numero: 17
  range_start: "2026-04-20"
  range_end: "2026-04-24"
  quarter: "Q2 2026"
  quarter_week: 4        # semana 4/13 do Q2
  weeks_remaining: 35

weekday: "quinta"        # dia em que o weekly esta sendo gerado
current_date: "2026-04-17"

retrospectiva_s_menos_1:
  destravou: "Pipeline E2-E6 do m7-controle rodou ponta-a-ponta sem intervencao pela primeira vez."
  travou: "SQL consorcios parado no Rafa ha 5d; sono medio 6.4h."
  aprendi: "Tenho que forcar ensaio de apresentacoes na vespera, nao no dia."

agenda:
  fonte: [google, outlook_manual]
  por_dia:
    seg:
      densidade: normal
      eventos:
        - start: "14:00"
          end: "15:00"
          titulo: "Kickoff WBR Invest"
          local: "Teams"
    ter: { ... }
    qua:
      densidade: protegido   # maker day
      eventos: []
    qui: { ... }
    sex: { ... }
  conflitos: []

tarefas:
  grupo_a_big3_candidatos:
    - id: "PRJ-12"
      title: "Fechar WBR Invest"
      list: "m7-controle"
      tags: [big3]
      due: "2026-04-24"
      priority: urgent
      linked_goal: "Publicar m7-controle em 3 verticais"
  grupo_b_semana: [...]
  prazos_duros:
    - dia: seg
      data: "2026-04-20"
      task: "Enviar briefing diretoria"
      sla: "ate 09h"
    - dia: sex
      data: "2026-04-24"
      task: "Apresentacao diretoria"
      sla: "10h"

delegadas:
  grupos:
    - projeto: "Padronizacao Rituais"
      tarefas:
        - title: "Validar fluxograma G2.3"
          assignee: "Ana"
          due: "2026-04-15"
          urgencia: urgent
          aging_dias: 2

corpo:
  fonte: trainingpeaks_mcp
  peso_delta_kg: -0.6
  tss_total: 320
  sono_medio_h: 6.4
  tsb: -12                 # fadiga, ver regra de cor
  hrv_medio: 48            # contexto interno, nao exibido

metas_q2:
  fonte: clickup_goals
  objetivos:
    - titulo: "Publicar m7-controle em 3 verticais"
      confidence: 65
      etapa: "fase E6"
      status: ok
    - titulo: "Desdobrar metas 2026 em 4 verticais"
      confidence: 30
      etapa: "SQL consorcios parado"
      status: risco
    - titulo: "Maratona junho sub-4h"
      confidence: 50
      etapa: "bloco de volume"
      status: ok

contexto_insight:
  tensionamentos: [validacao-vs-autonomia, delegacao-vs-fazer-eu-mesmo]
  candidatos_3resources:
    - brain/3-resources/...
```

Essa estrutura e consumida pela Fase 2 (planejamento) e pela Fase 3 (renderizacao). Nao e exposta ao usuario — e artefato interno da skill.
