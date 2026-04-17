# Fase 1 · Extracao de dados (horizonte semanal)

A primeira passada da skill e **levantamento** do que sera a proxima semana. Antes de planejar a orquestracao dos 5 dias, o Claude reune entradas de 7 fontes. Para cada fonte ha uma rota primaria (MCP direto) e um fallback (perguntar ao usuario).

**Regra de ouro:** nunca invente dado. Se nao conseguir extrair e o usuario nao forneceu, a secao correspondente no HTML fica com `&mdash;` ou e omitida — nunca preenchida com ficcao.

**Particularidade weekly:** a **Retrospectiva da semana passada** e sempre perguntada — e o que diferencia um weekly preview de um summary descritivo. Sem ela, a Tese da semana vira generica.

## Indice

- [Matriz de fontes](#matriz-de-fontes)
- [Janela temporal alvo](#janela-temporal-alvo)
- [1. Agenda (5 dias)](#1-agenda-5-dias)
- [2. Tarefas ClickUp (semana)](#2-tarefas-clickup-semana)
- [3. Workspace M7 (saude das frentes)](#3-workspace-m7-saude-das-frentes)
- [4. Corpo · semana (TrainingPeaks MCP)](#4-corpo--semana-trainingpeaks-mcp)
- [5. Metas Q2 (conexao trimestral)](#5-metas-q2-conexao-trimestral)
- [6. Retrospectiva S-1 (sempre perguntar)](#6-retrospectiva-s-1-sempre-perguntar)
- [7. Contexto para o agente Pfeffer](#7-contexto-para-o-agente-pfeffer)
- [Protocolo de fallback](#protocolo-de-fallback)
- [Rastreabilidade de metricas](#rastreabilidade-de-metricas)
- [Schema da extracao](#schema-da-extracao)

## Matriz de fontes

| Secao do planner | Fonte primaria | MCP / Ferramenta | Fallback |
|---|---|---|---|
| Agenda (5 dias) | Google Calendar + Outlook M7 | `mcp__claude_ai_Google_Calendar__list_events` · *Outlook sem MCP* | Pedir print ou lista |
| Tarefas da semana | ClickUp (due <= sex, assignee=Bruno) | `mcp__claude_ai_ClickUp__clickup_filter_tasks` | Pedir lista |
| **Workspace M7** | ClickUp (statuses=[atrasada, bloqueada] workspace inteiro) | `mcp__claude_ai_ClickUp__clickup_filter_tasks` | Pedir resumo por frente |
| **Corpo · semana** | **TrainingPeaks MCP** (v1.5.0+) | `tp-mcp` (weight, sleep, HRV, weekly_summary, fitness_metrics) | Perguntar se MCP falhar |
| **Metas Q2** | ClickUp goals → `brain/3-resources/` → perguntar | `mcp__claude_ai_ClickUp__clickup_get_workspace_hierarchy` + `clickup_search` | Perguntar confidence por objetivo |
| **Retrospectiva S-1** | *Sempre perguntar ao usuario* | — | — (e a propria fonte) |
| Contexto Pfeffer | Agente `pfeffer-power-analyst` (horizonte=weekly) recebe Tese + Big 3 + Retrospectiva S-1 + Riscos + Corpo | Invocacao direta do agente | Agente pede dado especifico se input incompleto |

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

### Whitelist e blacklist de status (v1.9.0)

Identica ao daily. O ClickUp retorna tasks com status `cancelada`, `descartada`, `won't do` quando `statuses=open` — filtrar pos-query:

**Whitelist:** `["pendente", "em andamento", "atrasada", "bloqueada", "em revisao", "em aprovacao"]`

**Blacklist:** `["cancelada", "descartada", "won't do", "concluida", "arquivada", "duplicada", "rejeitada"]`

**Regra de deteccao:** aplicar em ordem — (1) `status.status` na blacklist, (2) `status.type == closed`, (3) `date_closed != null`, (4) `archived == true`. Se qualquer regra bate, descartar. Tasks destinadas ao topo do weekly (candidatas a **Big 3**, **Prazos duros** ou **Riscos**) com status fora da whitelist explicita devem ser confirmadas via `AskUserQuestion` antes de entrar.

Para descobrir status customizados M7, chamar `clickup_get_list(list_id=...)` uma vez por sessao e inspecionar `statuses[]`.

### Filtragem em grupos

Apos aplicar whitelist/blacklist, separar em:

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

## 3. Workspace M7 (saude das frentes)

**Escopo (reformulado em v1.9.0):** no horizonte semanal, esta secao alimenta principalmente **Riscos & fogos** (Band 3) e informa os **Prazos duros**. O escopo e saude do workspace M7 inteiro (todas as frentes, todos os assignees), nao "tasks delegadas por Bruno". Bruno como Head of Performance responde pela execucao de todas as frentes — o weekly usa essa extracao pra detectar gargalos sistemicos na semana e informar pre-mortem.

### Rota primaria

```
mcp__claude_ai_ClickUp__clickup_filter_tasks (
  statuses=["atrasada", "bloqueada"],     # custom statuses M7
  due_date_lt=sexta_proxima_semana,       # horizonte semanal + buffer
  # sem filtro de assignee — escopo e workspace inteiro
  # sem filtro de created_by — escopo e workspace inteiro
)
```

Apos query, aplicar a mesma blacklist da secao 2 (cancelada/descartada/closed/archived/date_closed).

### Regra de agrupamento

Agrupar por **frente** (lista/sprint/projeto). Ordenar:
1. Frentes com mais atrasadas no topo
2. Dentro da frente, atrasadas antes de bloqueadas
3. Dentro de cada classe, mais antigas primeiro

Limite: **4-5 grupos visiveis** para alimentar Riscos, 2-3 linhas por grupo.

### Regra "Bruno e o gargalo"

Tasks com `assignee == Bruno` aparecem com marca `is_self: true` no schema. No weekly elas sao insumo para:

- **Pre-mortem (Riscos)**: gargalo pessoal vira risco explicito
- **Big 3**: se Bruno tem 3+ atrasadas proprias numa frente, essa frente pode virar Big 3 ("Desafogar fila de X")
- **Preflight ("onde vou dizer nao?")**: contagem de atrasadas proprias informa essa resposta

### Metadata obrigatoria

- `id`, `title`
- `assignee` (ou lista) — display `· <pessoa>`
- `list_name` ou `project` — cabecalho do grupo
- `due_date`
- `status.status` + `status.type`
- `date_closed`, `archived`
- `is_self` (booleano: assignee inclui Bruno)

### Filtro weekly-especifico

Incluir apenas tasks `atrasada` ou `bloqueada` que:
- Tem due date dentro da semana alvo OU ja atrasadas, OU
- Bloqueiam tarefas da propria semana (dependencia), OU
- Tem SLA de follow-up que estoura na semana

Tasks atrasadas ha muito tempo e sem bloqueio ativo ficam fora — nao sao decisao desta weekly.

### Fallback

Se ClickUp MCP falhar:

> Nao consegui extrair o estado do workspace M7. Me passa um resumo por frente das tarefas atrasadas ou bloqueadas:
> - [Frente X] 2-3 tarefas · responsavel · dias de atraso
> - [Frente Y] ...
>
> Nao preciso das suas tasks pessoais aqui — essa secao alimenta Riscos & fogos, escopo e workspace inteiro.

## 4. Corpo · semana (TrainingPeaks MCP)

**Fonte primaria: TrainingPeaks MCP** (adicionado na v1.5.0 do plugin). Restaura a automacao que havia sido removida em v1.3.0 quando o Garmin foi descontinuado.

### Ordem fixa dos 4 KPIs (v1.8.0)

**Renderizar sempre nesta ordem**: `peso Δ → sono medio → TSS total → TSB`

Essa ordem e compartilhada com a daily (v1.7.0) — "peso e porta de entrada, sono e condicao, TSS e volume, TSB e sintese". Trocar a ordem quebra a leitura rapida.

### Tools TP mapeadas para os 4 KPIs semanais

| KPI | TP tool | Calculo |
|---|---|---|
| **peso Δ** | `weight` | weight(sex) - weight(seg-1) = delta semanal em kg |
| **sono medio** | `sleep` | media de horas dormidas seg-1 a qui (noites que precedem cada weekday) |
| **TSS total** | `weekly_summary` | TSS acumulado seg-sex (tool ja agrega) |
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

### Tags de classificacao por KPI (v1.8.0)

Cada KPI renderiza uma **tag de 1 palavra** a direita do valor, classificando o status. As faixas sao identicas a daily (v1.7.0) para garantir consistencia entre os dois planners.

**Peso Δ** — variacao semanal em kg (rule-of-thumb: 1kg ≈ 1% do peso para Bruno ~100kg):

| Faixa | Tag | Classe CSS |
|---|---|---|
| |Δ| <=1kg (~1% em 7 dias) | `estável` | default (sem modifier) |
| Δ < -1kg (queda >1%) | `em queda` | `--body` (azul petroleo) |
| Δ > +1kg (alta >1%) | `subindo` | `--warn` (`--accent-primary`) |

**Sono medio** — media de horas seg-1 a qui (4 noites que precedem weekdays):

| Faixa | Tag | Classe CSS |
|---|---|---|
| >=7h | `ideal` | `--body` (azul petroleo) |
| 6-7h | `ok` | default (neutro) |
| <6h | `baixo` | `--alert` (terracota escuro) |

**TSS total** — TSS acumulado seg-sex:

| Faixa | Tag | Classe CSS |
|---|---|---|
| 0 nos ultimos 3+ dias consecutivos | `crítico` | `--alert` |
| >0 e <150 na semana | `leve` | `--warn` (`--accent-primary`) |
| 150-450 na semana | `saudável` | `--body` (azul petroleo) |
| >450 na semana | `pesado` | `--alert` (sobrecarga, sinal de overtraining se persistir) |

**TSB** — Training Stress Balance (forma) no momento da geracao do weekly, bandas de Banister:

| Faixa | Tag | Classe CSS |
|---|---|---|
| TSB < -30 | `overreach` | `--alert` |
| -30 <= TSB < -10 | `produtivo` | `--body` |
| -10 <= TSB <= +5 | `neutro` | default |
| +5 < TSB <= +25 | `fresco` | `--warn` (`--accent-primary`) |
| TSB > +25 | `destreino` | `--alert` |

### Regra de cor do numero + tag (consistencia)

O numero segue a **mesma classe CSS** que a tag. Assim valor e classificacao compartilham a mesma cor semantica:

- default primary (neutro) → peso estavel, sono ok, TSB neutro
- `--body` (azul petroleo) → peso em queda, sono ideal, TSS saudavel, TSB produtivo
- `--warn` (`--accent-primary` / terracota) → peso subindo, TSS leve, TSB fresco
- `--alert` (terracota escuro) → sono baixo, TSS critico/pesado, TSB overreach/destreino

### Regra de ouro (v1.8.0)

Quando o MCP TrainingPeaks esta indisponivel ou o dado esta ausente:
- O **valor** renderiza como `&mdash;` com classe `--empty`
- A **tag** e **totalmente omitida** do HTML (nao renderiza tag vazia ou "?")
- Nunca inventar classificacao

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

## 7. Contexto para o agente Pfeffer

Desde **v1.11.0**, o Insight · cruzamento do weekly e sempre gerado pelo agente [`pfeffer-power-analyst`](../../../agents/pfeffer-power-analyst.md) com horizonte=weekly. Alem do Insight, o agente pode alimentar a Regra 6 (Riscos & fogos) com bloco opcional `## Riscos Pfeffer`. Nao ha mais scan de `brain/3-resources/`.

### Inputs que o agente espera (horizonte=weekly)

```yaml
horizonte: weekly
semana_numero: 17
semana_range: "2026-04-20 a 2026-04-24"
retrospectiva_s_menos_1:       # da secao 6 desta extracao
  destravou, travou, aprendi
tese_rascunho: "<texto>"       # rascunho da Fase 2 Regra 1
big3:                           # da Fase 2 Regra 4
  - titulo, confidence, criterio_pronto_quando
orquestra:                      # da Fase 2 Regra 3
  por_dia: { seg, ter, qua, qui, sex }
riscos_pre_capturados:          # opcional, da Fase 2 Regra 6 parcial
  - titulo, fonte (retro/workspace/orquestra)
workspace_m7:                   # da secao 3 desta extracao
  atrasadas_bruno, frentes_mais_atrasadas
corpo_semana:                   # da secao 4 desta extracao
  peso_delta_kg, sono_medio_h, tss_total, tsb
```

### Regra

Se qualquer input esta incompleto quando o agente e invocado, o agente pede o dado especifico antes de produzir analise. Pfeffer e empirico — sem dado, sem analise.

Nao ha fallback. Ver [insight-cruzamento.md](insight-cruzamento.md) para regras de formato do output e racional de commitment editorial.

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

## Rastreabilidade de metricas

**Problema que esta regra resolve (v1.9.0):** contadores como `X atrasadas` ou `Y bloqueadas` em Riscos & fogos e no section-header apareciam sem lastro, podendo resultar de soma redundante de heuristicas (`status=pendente + due vencido + status=atrasada`) ou de headers cached da API que nao batem com as linhas exibidas.

### Regra de ouro

**Todo numero que aparece no HTML final deve ter uma entrada em `extracao.metricas`** com:
1. `metrica` — rotulo (ex: `atrasadas_workspace_semana`, `big3_count`)
2. `query` — string da query com parametros reais
3. `count` — valor numerico
4. `fonte` — `clickup_mcp` | `google_calendar_mcp` | `trainingpeaks_mcp` | `usuario`

Se um numero no HTML nao tem entrada, a Fase 3 **recusa renderizar** e volta para Fase 2 pedindo a origem.

### Regra de unica fonte para "atrasada"

Status customizado `atrasada` no workspace M7 e a fonte unica. **Nunca somar** `status=pendente + due_date < hoje` com `status=atrasada`. Se em algum workspace o `atrasada` nao existir como custom status, usar **uma** das duas heuristicas, nunca somadas:

- Preferencia 1: `status == atrasada`
- Preferencia 2: `status.type in ["open", "custom"] AND due_date < hoje AND status NOT IN blacklist`

### Regra de recalculo na Fase 2

Antes de renderizar cada contador, recalcular a partir das linhas extraidas — nao reusar contadores retornados no header da API:

```
# CERTO
total_atrasadas_semana = len([
    t for t in workspace_tasks
    if t["status.status"] == "atrasada"
    and t["due_date"] <= sexta_semana_alvo
    and not t["archived"] and not t["date_closed"]
])
```

### Schema do bloco `metricas` (weekly)

```yaml
metricas:
  - metrica: "atrasadas_workspace_semana"
    query: "clickup_filter_tasks(statuses=[atrasada], due_lt=sex_semana) | len"
    count: 14
    fonte: clickup_mcp
  - metrica: "bloqueadas_workspace_semana"
    query: "clickup_filter_tasks(statuses=[bloqueada], due_lt=sex_semana) | len"
    count: 3
    fonte: clickup_mcp
  - metrica: "atrasadas_bruno_semana"
    query: "atrasadas_workspace_semana AND assignee==bruno | len"
    count: 2
    fonte: clickup_mcp
  - metrica: "prazos_duros_count"
    query: "grupo_c_prazos_duros | len"
    count: 5
    fonte: clickup_mcp
  - metrica: "big3_confidence_media"
    query: "avg(objetivos_q2[i].confidence)"
    count: 48
    fonte: clickup_goals
```

### Validacao antes de renderizar

Incluso no checklist de sanidade da Fase 2:

```
[ ] Cada numero planejado tem entrada em `metricas`
[ ] Contadores recalculados a partir das linhas (nao reusados da API)
[ ] Nenhum numero soma heuristicas redundantes (pendente+due vencido+atrasada)
[ ] "atrasadas_*" usa status=atrasada como fonte unica
```

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

workspace_m7:
  escopo: "statuses=[atrasada, bloqueada] no workspace inteiro, due_lt=sex_semana"
  grupos:
    - frente: "Padronizacao Rituais"
      tarefas:
        - id: "TSM-1140"
          title: "Validar fluxograma G2.3"
          assignee: "Ana"
          due: "2026-04-15"
          status: "atrasada"
          is_self: false
          aging_dias: 2
    - frente: "Desdobramento Metas 2026"
      tarefas:
        - id: "TSM-1155"
          title: "SQL consorcios"
          assignee: "Rafa"
          due: "2026-04-12"
          status: "bloqueada"
          is_self: false
          aging_dias: 5
  contadores:
    atrasadas_total: 14
    bloqueadas_total: 3
    atrasadas_bruno: 2           # se >=3, alimenta Pre-mortem como gargalo

corpo:
  fonte: trainingpeaks_mcp
  # Ordem fixa dos 4 KPIs (v1.8.0): peso -> sono -> TSS -> TSB
  peso_delta_kg: -0.6
  peso_classificacao:
    tag: "estável"
    modifier: null           # default (neutro)
  sono_medio_h: 6.4
  sono_classificacao:
    tag: "ok"
    modifier: null           # default (neutro) — entre 6 e 7h
  tss_total: 320
  tss_classificacao:
    tag: "saudável"
    modifier: "--body"       # 150-450 na semana
  tsb: -12
  tsb_classificacao:
    tag: "produtivo"
    modifier: "--body"       # -30 a -10
  hrv_medio: 48              # contexto interno, nao exibido

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

contexto_pfeffer:                        # v1.11.0 · substitui contexto_insight
  # Nada a extrair aqui na Fase 1 — o agente recebe retrospectiva + tese + big3 +
  # orquestra + riscos_pre_capturados + workspace_m7 + corpo_semana diretamente da
  # Fase 2b e produz Insight + (opcional) Riscos Pfeffer. Bloco mantido apenas
  # para documentar a ausencia de scan em brain/3-resources/.
  fonte: agents/pfeffer-power-analyst.md
  horizonte: weekly

metricas:
  - metrica: "atrasadas_workspace_semana"
    query: "clickup_filter_tasks(statuses=[atrasada], due_lt=sex_semana) | len"
    count: 14
    fonte: clickup_mcp
  - metrica: "bloqueadas_workspace_semana"
    query: "clickup_filter_tasks(statuses=[bloqueada], due_lt=sex_semana) | len"
    count: 3
    fonte: clickup_mcp
  - metrica: "atrasadas_bruno_semana"
    query: "atrasadas_workspace_semana AND assignee==bruno | len"
    count: 2
    fonte: clickup_mcp
  - metrica: "prazos_duros_count"
    query: "grupo_c_prazos_duros | len"
    count: 5
    fonte: clickup_mcp
```

Essa estrutura e consumida pela Fase 2 (planejamento) e pela Fase 3 (renderizacao). Nao e exposta ao usuario — e artefato interno da skill.
