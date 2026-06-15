# Fase 1 · Extracao de dados (horizonte semanal)

> _Migrado da generating-weekly-planner e alinhado à arquitetura Supabase: o output é o objeto canônico (forma enxuta), gravado pela skill writing-week-to-supabase; o front Next.js/Vercel renderiza._

A primeira passada da skill e **levantamento** do que sera a proxima semana. Antes de planejar a orquestracao dos 5 dias, o Claude reune entradas das fontes abaixo. Para cada fonte ha uma rota primaria (MCP direto) e um fallback (perguntar ao usuario).

**Regra de ouro:** nunca invente dado. Se nao conseguir extrair e o usuario nao forneceu, o campo correspondente do objeto canonico fica vazio (`null`) ou e omitido — nunca preenchido com ficcao.

**Particularidade weekly:** a **Retrospectiva da semana passada** e sempre perguntada — e o que diferencia um weekly preview de um summary descritivo. Sem ela, a Tese da semana vira generica.

## Indice

- [Matriz de fontes](#matriz-de-fontes)
- [Janela temporal alvo](#janela-temporal-alvo)
- [1. Agenda (5 dias)](#1-agenda-5-dias)
- [2. Tarefas ClickUp (semana)](#2-tarefas-clickup-semana)
- [3. Workspace M7 (saude das frentes)](#3-workspace-m7-saude-das-frentes)
- [4. Corpo · semana (TrainingPeaks MCP) — opcional, nao persistido na v1](#4-corpo--semana-trainingpeaks-mcp--opcional-nao-persistido-na-v1)
- [5. Metas Q2 (conexao trimestral) — opcional, nao persistido na v1](#5-metas-q2-conexao-trimestral--opcional-nao-persistido-na-v1)
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
| **Corpo · semana** *(opcional — discutido, nao persistido na v1 enxuta)* | **TrainingPeaks MCP** (v1.5.0+) | `tp-mcp` (weight, sleep, HRV, weekly_summary, fitness_metrics) | Perguntar se MCP falhar |
| **Metas Q2** *(opcional — discutido, nao persistido na v1 enxuta)* | ClickUp goals → `brain/3-resources/` → perguntar | `mcp__claude_ai_ClickUp__clickup_get_workspace_hierarchy` + `clickup_search` | Perguntar confidence por objetivo |
| **Retrospectiva S-1** | *Sempre perguntar ao usuario* | — | — (e a propria fonte) |
| Contexto Pfeffer | Agente `pfeffer-power-analyst` (horizonte=weekly) recebe Tese + Foco da semana + Retrospectiva S-1 + Riscos | Invocacao direta do agente | Agente pede dado especifico se input incompleto |

### Escopo v1 enxuto (o que persiste no objeto canonico)

O objeto canonico gravado no Supabase persiste apenas: **Tese (lede)**, **Insight**, **Foco da semana (3)**, **Orquestra (5 dias + tarefas)**, **Riscos**, **Preflight** e **Review**.

Fontes e secoes marcadas como *opcional* abaixo (Corpo/TSS via TrainingPeaks, Metas Q2, Criterio de vitoria, Prazos duros, energia por dia) sao **discutidas na conversa** para informar as decisoes, mas **nao sao persistidas** na v1. Extraia-as quando ajudarem o raciocinio, mas nao as inclua no objeto que vai ao Supabase.

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

## 4. Corpo · semana (TrainingPeaks MCP) — opcional, nao persistido na v1

> **Opcional na v1 enxuta.** Corpo/TSS e fonte de **discussao** — alimenta o raciocinio (energia da semana, balanco trabalho/recovery, pre-mortem de fadiga) mas **nao e persistido** no objeto canonico. Extraia quando ajudar a calibrar a Orquestra ou os Riscos; nao inclua os KPIs no output do Supabase.

**Fonte primaria: TrainingPeaks MCP** (adicionado na v1.5.0 do plugin). Restaura a automacao que havia sido removida em v1.3.0 quando o Garmin foi descontinuado.

### Ordem dos 4 KPIs (quando discutidos)

Quando os KPIs forem usados na discussao, mante-los nesta ordem para leitura rapida: `peso Δ → sono medio → TSS total → TSB`

Essa ordem reflete a logica "peso e porta de entrada, sono e condicao, TSS e volume, TSB e sintese".

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

### Tags de classificacao por KPI (quando discutidos)

Cada KPI tem uma **tag de 1 palavra** classificando o status. As faixas sao identicas a daily para garantir consistencia de leitura entre os dois planners.

**Peso Δ** — variacao semanal em kg (rule-of-thumb: 1kg ≈ 1% do peso para Bruno ~100kg):

| Faixa | Tag |
|---|---|
| |Δ| <=1kg (~1% em 7 dias) | `estável` |
| Δ < -1kg (queda >1%) | `em queda` |
| Δ > +1kg (alta >1%) | `subindo` |

**Sono medio** — media de horas seg-1 a qui (4 noites que precedem weekdays):

| Faixa | Tag |
|---|---|
| >=7h | `ideal` |
| 6-7h | `ok` |
| <6h | `baixo` |

**TSS total** — TSS acumulado seg-sex:

| Faixa | Tag |
|---|---|
| 0 nos ultimos 3+ dias consecutivos | `crítico` |
| >0 e <150 na semana | `leve` |
| 150-450 na semana | `saudável` |
| >450 na semana | `pesado` (sobrecarga, sinal de overtraining se persistir) |

**TSB** — Training Stress Balance (forma), bandas de Banister:

| Faixa | Tag |
|---|---|
| TSB < -30 | `overreach` |
| -30 <= TSB < -10 | `produtivo` |
| -10 <= TSB <= +5 | `neutro` |
| +5 < TSB <= +25 | `fresco` |
| TSB > +25 | `destreino` |

### Regra de dado ausente

Quando o MCP TrainingPeaks esta indisponivel ou o dado esta ausente:
- O **valor** fica vazio (`null`)
- A **tag** e **totalmente omitida** (nao gerar tag vazia ou "?")
- Nunca inventar classificacao

### Fallback

Se o TP MCP falhar ou auth expirar:

> Nao consegui extrair os dados do TrainingPeaks (MCP pode ter falhado ou cookie expirou). Pra preencher a Corpo · semana, me passa:
> - peso Δ (delta kg entre inicio e fim da semana — pode deixar vazio)
> - TSS total da semana (numero unico)
> - sono medio (horas, media seg a qui)
> - TSB atual (se souber — positivo em forma, negativo fadiga)

Campos nao fornecidos ficam vazios (`null`). Lembrar que Corpo nao e persistido na v1 — serve so a discussao.

### Renovacao de cookie

Se o erro for `auth expired` ou `401`, ligar o usuario para:
```bash
tp-mcp auth
# ou (bypass getpass para IDE terminals):
pbpaste | python ~/.local/bin/tp-mcp auth
```

## 5. Metas Q2 (conexao trimestral) — opcional, nao persistido na v1

> **Opcional na v1 enxuta.** As Metas Q2 sao fonte de **discussao** — informam de onde o Foco da semana deve derivar — mas **nao sao persistidas** como secao do objeto canonico. Use-as para ancorar o raciocinio; o vinculo Foco↔Metas Q2 e discutido, nao gravado no Supabase na v1.

**Principio:** o Foco da semana deve **derivar** de Metas Q2. Sem essa conexao, o Foco vira so tarefas grandes.

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

### Faixas de confidence (para leitura na discussao)

- Confidence >= 60% → `ok`
- Confidence 40-60% → `atencao` (ainda da)
- Confidence < 40% → `em risco` (rever)

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
- **Foco da semana**: o "aprendi" informa o que precisa ser diferente nos 3 focos

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
foco_da_semana:                 # da Fase 2 Regra 4 (3 focos)
  - titulo, criterio_pronto_quando
orquestra:                      # da Fase 2 Regra 3
  por_dia: { seg, ter, qua, qui, sex }
riscos_pre_capturados:          # opcional, da Fase 2 Regra 6 parcial
  - titulo, fonte (retro/workspace/orquestra)
workspace_m7:                   # da secao 3 desta extracao
  atrasadas_bruno, frentes_mais_atrasadas
corpo_semana:                   # opcional (discutido, nao persistido) — da secao 4
  peso_delta_kg, sono_medio_h, tss_total, tsb
```

### Regra

Se qualquer input esta incompleto quando o agente e invocado, o agente pede o dado especifico antes de produzir analise. Pfeffer e empirico — sem dado, sem analise.

Nao ha fallback. Ver [insight-cruzamento.md](insight-cruzamento.md) para regras de formato do output e racional de commitment editorial.

## Protocolo de fallback

Regras gerais quando um MCP falha ou retorna vazio:

1. **Tentar 1 vez com parametros mais frouxos** (ex: ampliar janela temporal)
2. **Se ainda falhar, perguntar ao usuario** com pergunta especifica
3. **Nunca inventar.** Na duvida, o campo fica vazio (`null`) ou e totalmente omitido do objeto canonico
4. **Registrar a origem no metadata do objeto canonico** (campo opcional de proveniencia, ex: `fonte: usuario` na metrica correspondente)

`★ Exemplo de pergunta especifica ───────────────`
Ruim: "me passa os dados da semana"

Bom: "A tool weekly_summary do TP nao respondeu. Me passa o TSS total da semana passada (se lembrar) e a contagem de treinos — default para o TSS e 250-350 numa semana base, 400+ numa semana all-in."
`──────────────────────────────────────────────────`

## Rastreabilidade de metricas

**Problema que esta regra resolve (v1.9.0):** contadores como `X atrasadas` ou `Y bloqueadas` em Riscos & fogos apareciam sem lastro, podendo resultar de soma redundante de heuristicas (`status=pendente + due vencido + status=atrasada`) ou de headers cached da API que nao batem com as linhas exibidas.

### Regra de ouro

**Todo numero que entra no objeto canonico deve ter uma entrada em `extracao.metricas`** com:
1. `metrica` — rotulo (ex: `atrasadas_workspace_semana`, `foco_count`)
2. `query` — string da query com parametros reais
3. `count` — valor numerico
4. `fonte` — `clickup_mcp` | `google_calendar_mcp` | `trainingpeaks_mcp` | `usuario`

Se um numero destinado ao objeto canonico nao tem entrada, a skill **recusa gravar** e volta para a Fase 2 pedindo a origem antes de chamar a writing-week-to-supabase.

### Regra de unica fonte para "atrasada"

Status customizado `atrasada` no workspace M7 e a fonte unica. **Nunca somar** `status=pendente + due_date < hoje` com `status=atrasada`. Se em algum workspace o `atrasada` nao existir como custom status, usar **uma** das duas heuristicas, nunca somadas:

- Preferencia 1: `status == atrasada`
- Preferencia 2: `status.type in ["open", "custom"] AND due_date < hoje AND status NOT IN blacklist`

### Regra de recalculo na Fase 2

Antes de gravar cada contador no objeto canonico, recalcular a partir das linhas extraidas — nao reusar contadores retornados no header da API:

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
  - metrica: "foco_count"
    query: "len(foco_da_semana)"
    count: 3
    fonte: clickup_mcp
```

> `prazos_duros_count` e metricas derivadas de Metas Q2 (ex: confidence media) so entram aqui se a discussao opcional dessas fontes for promovida ao objeto canonico — o que **nao** acontece na v1 enxuta.

### Validacao antes de gravar

Incluso no checklist de sanidade da Fase 2:

```
[ ] Cada numero destinado ao objeto canonico tem entrada em `metricas`
[ ] Contadores recalculados a partir das linhas (nao reusados da API)
[ ] Nenhum numero soma heuristicas redundantes (pendente+due vencido+atrasada)
[ ] "atrasadas_*" usa status=atrasada como fonte unica
```

## Schema da extracao

Saida consolidada apos Fase 1 (estrutura interna de trabalho — **nao** e o objeto canonico). A Fase 2 destila este artefato no objeto canonico enxuto que a writing-week-to-supabase grava. Campos marcados *(opcional · nao persistido)* alimentam so a discussao:

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
  grupo_a_foco_candidatos:
    - id: "PRJ-12"
      title: "Fechar WBR Invest"
      list: "m7-controle"
      tags: [foco]
      due: "2026-04-24"
      priority: urgent
      linked_goal: "Publicar m7-controle em 3 verticais"   # discutido, nao persistido na v1
  grupo_b_semana: [...]
  prazos_duros:               # opcional · discutido, nao persistido na v1
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

corpo:                         # opcional · discutido, nao persistido na v1
  fonte: trainingpeaks_mcp
  # Ordem dos 4 KPIs quando discutidos: peso -> sono -> TSS -> TSB
  peso_delta_kg: -0.6
  peso_classificacao:
    tag: "estável"
  sono_medio_h: 6.4
  sono_classificacao:
    tag: "ok"                 # entre 6 e 7h
  tss_total: 320
  tss_classificacao:
    tag: "saudável"          # 150-450 na semana
  tsb: -12
  tsb_classificacao:
    tag: "produtivo"         # -30 a -10
  hrv_medio: 48              # contexto interno

metas_q2:                      # opcional · discutido, nao persistido na v1
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
  # Nada a extrair aqui na Fase 1 — o agente recebe retrospectiva + tese + foco +
  # orquestra + riscos_pre_capturados + workspace_m7 (+ corpo, opcional) diretamente
  # da Fase 2b e produz Insight + (opcional) Riscos Pfeffer. Bloco mantido apenas
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
  - metrica: "foco_count"
    query: "len(foco_da_semana)"
    count: 3
    fonte: clickup_mcp
```

Essa estrutura e consumida pela Fase 2 (planejamento), que destila o objeto canonico enxuto entregue a writing-week-to-supabase. Nao e exposta ao usuario — e artefato interno da skill.
