# Fase 1 · Extracao de dados

A primeira passada da skill e **levantamento**. Antes de planejar o dia, o Claude reune as entradas de cinco fontes. Para cada fonte ha uma rota primaria (MCP direto) e um fallback (perguntar ao usuario).

**Regra de ouro:** nunca invente dado. Se nao conseguir extrair e o usuario nao forneceu, a secao correspondente no HTML fica com `&mdash;` ou e omitida — nunca preenchida com ficcao.

## Indice

- [Matriz de fontes](#matriz-de-fontes)
- [1. Agenda](#1-agenda)
- [2. Tarefas ClickUp (tres inadiaveis + tarefas do dia)](#2-tarefas-clickup-tres-inadiaveis--tarefas-do-dia)
- [3. Workspace M7 (saude das frentes)](#3-workspace-m7-saude-das-frentes)
- [4. Corpo / saude](#4-corpo--saude)
- [5. Contexto para o agente Pfeffer](#5-contexto-para-o-agente-pfeffer)
- [Protocolo de fallback](#protocolo-de-fallback)
- [Rastreabilidade de metricas](#rastreabilidade-de-metricas)
- [Schema da extracao](#schema-da-extracao)

## Matriz de fontes

| Secao do planner | Fonte primaria | MCP / Ferramenta | Fallback |
|---|---|---|---|
| Agenda | Google Calendar + Outlook M7 | `mcp__claude_ai_Google_Calendar__*` (Google) · *Outlook sem MCP* | Pedir print ou texto da agenda |
| Tres inadiaveis | ClickUp (tags `mit`, `hoje`, `inadiavel`) ou usuario | `mcp__claude_ai_ClickUp__clickup_filter_tasks` | Pedir ao usuario os 3 diretamente |
| Tarefas ClickUp | ClickUp (due = hoje/amanha/atrasadas, assignee = Bruno) | `mcp__claude_ai_ClickUp__clickup_filter_tasks` | Pedir print da lista "Hoje" |
| Workspace M7 | ClickUp (statuses=[atrasada, bloqueada], workspace inteiro) | `mcp__claude_ai_ClickUp__clickup_filter_tasks` | Pedir resumo por frente |
| Corpo (peso, TSS, sono, HRV, forma) | TrainingPeaks (cookie-based auth) | `mcp__trainingpeaks__*` | Perguntar ao usuario se o MCP falhar |
| Contexto Pfeffer | Agente `pfeffer-power-analyst` recebe agenda + MITs + workspace M7 + Lide | Invocacao direta do agente | Se input incompleto, agente pede dado especifico |

## 1. Agenda

### Rota primaria · Google Calendar

```
mcp__claude_ai_Google_Calendar__list_events (timeMin=hoje 00h, timeMax=hoje 23h59, calendar=primary)
```

Extrair por evento: `start`, `end`, `summary`, `location` (inline ou virtual), `attendees` (se relevante para o display).

### Rota primaria · Outlook M7

**Nao ha MCP para Outlook.** Pedir ao usuario:

> Nao consigo ler o Outlook M7 direto. Me cola um print da agenda do dia, ou lista os eventos no formato `HH:MM - titulo` (uma linha por evento).

### Regra de consolidacao

Se os dois calendarios retornam eventos, mesclar por horario. Se conflito (mesmo horario, dois eventos), usar o do Google como primario e anotar o conflito no campo `conflitos[]` do schema de saida — o conflito vira material para o Lide ou para a nota de agenda no HTML.

## 2. Tarefas ClickUp (tres inadiaveis + tarefas do dia)

### Rota primaria

```
mcp__claude_ai_ClickUp__clickup_filter_tasks (
  assignees=[Bruno],
  statuses=open,
  due_date_lt=amanha_00h
)
```

### Whitelist e blacklist de status (v1.9.0)

O ClickUp retorna qualquer task que nao esteja em `closed`, **mesmo quando o status customizado e cancelada, descartada ou won't do**. O campo `status` da API e a fonte da verdade visual do card no ClickUp, mas nao e a fonte da verdade executiva — uma task `cancelada` nao deve entrar no planner nem mesmo no Grupo B.

**Status aceitos (whitelist)** — aparecem no planner:

```
["pendente", "em andamento", "atrasada", "bloqueada", "em revisao", "em aprovacao"]
```

**Status proibidos (blacklist)** — filtrar ANTES de classificar em grupos:

```
["cancelada", "descartada", "won't do", "concluida", "arquivada", "duplicada", "rejeitada"]
```

**Regra de detec&ccedil;&atilde;o de blacklist** (aplicar em ordem):

1. `status.status` (case-insensitive) esta na blacklist → descartar
2. `status.type == "closed"` → descartar (captura status customizados fechados)
3. `date_closed != null` → descartar (task foi fechada mesmo com status estranho)
4. `archived == true` → descartar

Para workspaces com status customizados que nao aparecem nas listas acima, chamar **uma vez** no inicio da sessao:

```
mcp__claude_ai_ClickUp__clickup_get_list (list_id=<id da lista>)
```

e inspecionar `statuses[]` para descobrir o mapa (ordem, tipo `open|custom|closed|done`). Status com `type=closed` ou `type=done` sao blacklist automatica. Status customizados novos que nao batem com a whitelist sao **ambiguos** — tratar como Regra de duvida (abaixo).

### Regra de duvida (tasks candidatas a MIT ou ao Destaque do dia)

Se uma task esta destinada ao **topo do planner** (candidata a MIT ou destaque) e seu status NAO esta na whitelist explicita, confirmar com o usuario via `AskUserQuestion` antes de incluir:

> A task TSM-874 "Executar primeiro ciclo do Ritual" esta com status **<status exato retornado>**. Isso aparece para mim como aberta, mas quero confirmar antes de colocar como MIT #1. Ela deve entrar no planner de hoje?

Para tasks do Grupo B (tarefas do dia, nao-destacadas), aplicar a blacklist sem perguntar — se nao passar, descartar silenciosamente.

### Anti-padr&atilde;o

| Ruim | Melhor |
|---|---|
| Confiar cegamente no `status.status` retornado | Cruzar com `date_closed`, `archived`, `status.type` |
| Usar `statuses=open` sem filtrar cancelada pos-query | Aplicar blacklist manual apos extracao |
| Incluir task `cancelada` porque o ClickUp retornou | Blacklist antes de grupo A/B |

### Filtragem em grupos

Apos aplicar whitelist/blacklist, separar em:

**Grupo A · Candidatos a Tres inadiaveis** (5-10 tasks)
- Tags contem `mit`, `hoje`, `inadiavel`, `urgente`, `critico`, OU
- Due date = hoje, OU
- Prioridade = urgent/high + status `atrasada`
- Lista de origem tem peso estrategico (nao helpdesk)

**Grupo B · Tarefas do dia** (resto, ate 15 linhas)
- Todas as demais due <= amanha ou atrasadas (status na whitelist)

### Metadata obrigatoria por task

Para cada task retornada, capturar:
- `id` (ex: `TSM-874`)
- `title`
- `list_name` (nome da lista — vira display no planner)
- `tags[]` (vira display junto da lista)
- `due_date` (usado para classificar atraso e formatar "+Nd")
- `priority` (urgent/high/normal/low)
- `status` (status.status + status.type)
- `date_closed` (validacao anti-cancelada)
- `archived`

O display final no HTML segue a regra de [componentes.md secao 9](componentes.md): `<titulo> · <lista> · <tag(s)>` + `<due>`.

### Fallback

Se ClickUp MCP falhar:

> Nao consegui extrair as tarefas do ClickUp. Voce pode me dar:
> 1. Os 3 inadiaveis de hoje (titulo + lista + SLA)
> 2. Uma lista curta (ate 8) de outras tarefas abertas com due <= amanha

## 3. Workspace M7 (saude das frentes)

**Escopo (reformulado em v1.9.0):** esta coluna **nao** e sobre "tasks que Bruno delegou". O papel de Bruno como Head of Performance e responder pela saude de **todo o workspace M7**, nao so pelo subset que ele criou ou assignou. O filtro correto e *onde o trabalho esta travando*, nao *quem Bruno delegou para*.

### Rota primaria

```
mcp__claude_ai_ClickUp__clickup_filter_tasks (
  statuses=["atrasada", "bloqueada"],   # custom statuses M7
  # sem filtro de assignee — escopo e workspace inteiro
  # sem filtro de created_by — escopo e workspace inteiro
)
```

Depois aplicar a mesma blacklist da secao 2 (cancelada, descartada, etc — `status.type == closed`, `date_closed`, `archived`).

### Regra de agrupamento

Agrupar por **lista/sprint/projeto** (a dimensao do ClickUp que melhor representa a frente). Ordenar:
1. Lista com mais atrasadas no topo
2. Dentro da lista, atrasadas antes de bloqueadas
3. Dentro de cada classe, mais antigas primeiro

Limite: 4-5 grupos visiveis, 2-3 linhas por grupo. O contador do section-header mostra o **total real** no workspace (nao o truncado).

### Regra de responsavel visivel

Cada linha mostra o **assignee** da task, mesmo que seja gente fora do time direto de Bruno. Se multiplos assignees, separar por vírgula. Sem assignee, escrever `· sem responsavel` (sinal forte de tarefa orfa).

### Regra "Bruno e o gargalo"

Se uma task retornada tiver `assignee == Bruno`, ela vira candidata a **sinal de gargalo**, nao item de acompanhamento:

- Aparece com marca visual `.tasks__row--self` (ver componentes.md)
- Nao duplicar com a coluna 2 (Tarefas ClickUp): se ja apareceu la, omitir daqui e logar internamente "ja em coluna 2"
- Se Bruno tem >=3 atrasadas proprias no workspace, gerar nota no section-header `.section-header__meta`: `<span class="alert">N minhas</span>` — sinaliza gargalo pessoal

### Metadata obrigatoria

- `id`
- `title`
- `assignee` (nome ou lista de nomes) — display `· <pessoa>`
- `list_name` ou `project` — cabecalho do grupo
- `due_date`
- `status.status` + `status.type`
- `date_closed`, `archived`
- `is_self` (booleano: assignee inclui Bruno)

### Fallback

Se ClickUp MCP falhar:

> Nao consegui extrair o estado do workspace M7. Me passa um resumo das tarefas atrasadas ou bloqueadas por frente (lista/sprint), no formato:
> - [Frente] Titulo · [Responsavel] · [SLA ou dias de atraso]
>
> Nao preciso das suas tasks pessoais aqui — essa coluna e sobre saude do workspace inteiro.

## 4. Corpo / saude

**Fonte:** TrainingPeaks MCP (`mcp__trainingpeaks__*`) via autenticacao cookie-based — bypassa aprovacao de API e nao e afetado por Cloudflare TLS fingerprinting (diferente do Garmin, removido em v1.3.0).

### Ordem fixa dos KPIs (v1.7.0)

A zona Corpo tem **4 rows em ordem fixa**:

```
1. peso       (kg)
2. sono       (h)
3. TSS sem    (pontos de training stress, semana ate hoje)
4. TSB        (training stress balance)
```

A ordem e parte do design — peso abre (dado estavel, diario), sono vem logo em seguida (dado cognitivo imediato), TSS mostra volume de treino da semana, TSB fecha com a sintese (forma). Nao reordenar.

### Rota primaria · TrainingPeaks MCP

Quatro chamadas independentes (paralelizar quando possivel):

| # | KPI do planner | Tool MCP | Observacao |
|---|---|---|---|
| 1 | **peso (kg)** | health-metrics (weight, last + -7d) | Ultimo valor + comparar com ha 7 dias para calcular variacao e tag |
| 2 | **sono (h)** | health-metrics (sleep, last night) | Noite mais recente. Se vazio, valor vira `&mdash;` e tag e omitida |
| 3 | **TSS sem** | `mcp__trainingpeaks__weekly_summary` | Total de TSS seg-hoje. Tambem retornar contagem de dias sem treino para aplicar tag "critico" |
| 4 | **TSB** | `mcp__trainingpeaks__fitness_metrics` | TSB atual (signed integer, pode ser negativo) |

Consultar a lista completa de 58 tools do TrainingPeaks MCP via `claude mcp list-tools trainingpeaks` ou pela documentacao do repo em `3-resources/ai-mcp/trainingpeaks-mcp/README.md`.

### Matriz de faixas → tag classificatoria (v1.7.0)

Cada KPI renderiza no HTML com uma **tag de 1 palavra** a direita do valor, com cor semantica. A tag e derivada automaticamente da faixa em que o valor cai. Se o valor e `&mdash;` (MCP indisponivel), a tag e omitida — regra de ouro: **nunca inventar classificacao**.

**Peso** — comparar valor atual com valor de 7 dias atras:

| Faixa | Tag | Classe CSS do numero + tag |
|---|---|---|
| variacao absoluta <=1% em 7 dias | `estável` | default (sem modifier) |
| queda >1% em 7 dias | `em queda` | `--body` (azul petroleo) |
| alta >1% em 7 dias | `subindo` | (warn · `--accent-primary`) |

**Sono** — horas da ultima noite:

| Faixa | Tag | Classe CSS |
|---|---|---|
| >=7h | `ideal` | `--body` (azul petroleo) |
| 6-7h | `ok` | default (neutro) |
| <6h | `baixo` | `--alert` (terracota escuro) |

**TSS sem** — total semanal (seg → hoje):

| Faixa | Tag | Classe CSS |
|---|---|---|
| 0 TSS nos ultimos 3+ dias consecutivos | `crítico` | `--alert` |
| TSS >0 e <150 na semana | `leve` | (warn · `--accent-primary`) |
| TSS 150-450 na semana | `saudável` | `--body` |
| TSS >450 na semana | `pesado` | `--alert` (sobrecarga, sinal de overtraining se persistir) |

**TSB** — training stress balance atual:

| Faixa | Tag | Classe CSS |
|---|---|---|
| TSB < -30 | `overreach` | `--alert` |
| -30 <= TSB < -10 | `produtivo` | `--body` |
| -10 <= TSB <= +5 | `neutro` | default |
| +5 < TSB <= +25 | `fresco` | (warn · `--accent-primary`) |
| TSB > +25 | `destreino` | `--alert` |

**Mapeamento de classe CSS:** a tag usa os mesmos modifiers do numero para coerencia visual. Ver [componentes.md secao 5](componentes.md#5-corpo--stack-vertical) para o HTML completo. Quando o texto indica "(warn · `--accent-primary`)", a classe e `header__corpo-tag--warn` e o numero pode levar classe correspondente se o status o justificar.

### Regras de cor do numero (complementares a tag)

O numero segue a mesma classe CSS que a tag:
- default primary (neutro) → peso estavel, sono ok, TSB neutro
- `--body` (azul petroleo) → peso em queda, sono ideal, TSS saudavel, TSB produtivo
- `--alert` (terracota escuro) → sono baixo, TSS critico/pesado, TSB overreach/destreino
- `--empty` (`--text-subtle`) → valor ausente (`&mdash;`), tag omitida

### Fallback

Se o TrainingPeaks MCP falhar parcial ou totalmente (cookie expirado, API fora do ar, tool indisponivel, metrica faltando):

- Os campos que nao chegarem ficam com `&mdash;` (classe `header__corpo-number--empty`)
- A tag daqueles campos e **omitida** do HTML (nao renderiza `<div class="header__corpo-tag">`)
- Perguntar ao usuario:

> TrainingPeaks MCP nao respondeu para [lista dos KPIs faltantes]. Voce quer:
> (a) Deixar em `—` sem tag (recomendado se o dia for curto)
> (b) Me passar manualmente os numeros

Se a autenticacao expirou, sugerir:
```bash
tp-mcp auth-status  # confirma se o problema e auth
```
E se necessario, renovar o cookie com o metodo documentado no README do plugin.

## 5. Contexto para o agente Pfeffer

Desde **v1.11.0**, o Insight · cruzamento e as Notas do dia sao sempre geradas pelo agente [`pfeffer-power-analyst`](../../../agents/pfeffer-power-analyst.md). Nao ha mais scan de `brain/3-resources/` — o agente le a agenda atraves das lentes do livro POWER (Pfeffer, 2010).

Esta secao documenta **o que a Fase 1 deve montar** para a Fase 2b conseguir invocar o agente com inputs completos.

### Inputs que o agente espera

```yaml
horizonte: daily
data: "2026-04-20"
agenda:                      # da secao 1 desta extracao
  - start, end, titulo, local, calendar
mits:                        # derivados da Fase 2 Regra 2
  - titulo, projeto
workspace_m7:                # da secao 3 desta extracao
  atrasadas_bruno: <int>
  frentes_mais_atrasadas: [<nomes>]
lide_rascunho: "<texto>"     # rascunho da Fase 2 Regra 1
```

### Regra

Se qualquer input esta incompleto quando o agente e invocado, o agente pede o dado especifico que falta antes de produzir analise — nao inventa. **Jamais** substitua a invocacao do agente por "improviso de insight".

Nao ha fallback. Pfeffer e a fonte unica por decisao editorial — ver [insight-cruzamento.md](insight-cruzamento.md) para regras de formato do output e racional de commitment.

## Protocolo de fallback

Regras gerais quando um MCP falha ou retorna vazio:

1. **Tentar 1 vez com parametros mais frouxos** (ex: remover filtro de data, ampliar range)
2. **Se ainda falhar, perguntar ao usuario** com pergunta especifica (nao `"me da os dados"` generico)
3. **Nunca inventar.** Na duvida, secao fica com `—` ou e totalmente omitida
4. **Anotar no log qual fonte faltou.** A nota de agenda no HTML (classe `.agenda-note`) e o lugar natural para sinalizar "Outlook offline, Google capturado"

`★ Exemplo de pergunta especifica ───────────────`
Ruim: "me passa os dados do dia"
Bom: "A agenda do Outlook M7 nao respondeu. Voce pode me colar os eventos de hoje no formato `HH:MM - titulo · local`? Se nao tiver nada no Outlook, responde so `vazio`."
`──────────────────────────────────────────────────`

## Rastreabilidade de metricas

**Problema que esta regra resolve (v1.9.0):** contadores como `42 atrasadas` no section-header apareciam sem lastro — nao batiam com a soma das linhas exibidas, porque eram derivados de queries legacy ou somavam `status=pendente + due vencido` (duplicando com `status=atrasada`).

### Regra de ouro

**Todo numero que aparece no HTML final deve ter uma entrada em `extracao.metricas`** com:
1. `metrica` — rotulo que aparece no HTML (ex: `atrasadas_workspace`)
2. `query` — string da query que gerou o numero (parametros reais)
3. `count` — valor numerico
4. `fonte` — `clickup_mcp` | `google_calendar_mcp` | `trainingpeaks_mcp` | `usuario`

Se um numero no HTML nao tem entrada no bloco `metricas`, a Fase 3 deve **recusar renderizar** e voltar pra Fase 2 pedindo a origem.

### Regra de unica fonte da verdade para "atrasada"

Status customizado `atrasada` no workspace M7 ja e a fonte de verdade unica. **Nunca somar** `status=pendente + due_date < hoje` com `status=atrasada` — isso duplica (porque o ClickUp automaticamente muda o status para `atrasada` quando o due passa). Se em algum workspace o `atrasada` nao existir como status custom, usar **uma** das duas heuristicas, nunca as duas somadas:

- Preferencia 1: `status == atrasada` (se custom status existe)
- Preferencia 2: `status.type in ["open", "custom"] AND due_date < hoje AND status NOT IN blacklist`

### Regra de recalculo na Fase 2

Antes de renderizar um contador, a Fase 2 **recalcula a partir dos dados extraidos**, nao reusa o numero que veio do section-header do ClickUp. Ou seja:

```
# ERRADO (reusa numero da API)
total_atrasadas = response["header"]["count"]

# CERTO (recalcula a partir das linhas)
total_atrasadas = len([t for t in tasks if t["status.status"] == "atrasada"
                        and t["archived"] is False and t["date_closed"] is None])
```

### Schema do bloco `metricas`

```yaml
metricas:
  - metrica: "atrasadas_workspace"
    query: "clickup_filter_tasks(statuses=[atrasada], archived=False) | len"
    count: 28
    fonte: clickup_mcp
  - metrica: "atrasadas_bruno"
    query: "atrasadas_workspace AND assignee==bruno | len"
    count: 18
    fonte: clickup_mcp
  - metrica: "bloqueadas_workspace"
    query: "clickup_filter_tasks(statuses=[bloqueada]) | len"
    count: 4
    fonte: clickup_mcp
  - metrica: "tarefas_dia_visiveis"
    query: "grupo_b_dia sorted ABCDE | head(6)"
    count: 6
    fonte: clickup_mcp
  - metrica: "tarefas_dia_cortadas"
    query: "len(grupo_b_dia) - tarefas_dia_visiveis"
    count: 12
    fonte: clickup_mcp
```

### Validacao antes de renderizar

Ultimo passo da Fase 2 (checklist de sanidade):

```
[ ] Cada numero no HTML planejado tem entrada em `metricas`
[ ] Cada contador foi recalculado a partir das linhas extraidas (nao reusado)
[ ] Nenhum numero vem de soma de duas heuristicas redundantes (pendente + due vencido + atrasada)
[ ] Se um numero e "atrasadas", a query usa status=atrasada como unica fonte
```

## Schema da extracao

Saida consolidada apos Fase 1 (estrutura interna, nao HTML):

```yaml
data: "2026-04-17"
weekday: "Sexta-feira"

agenda:
  fonte: [google, outlook_manual]
  eventos:
    - start: "10:00"
      end: "11:00"
      titulo: "6a Mentoria Viva Lideranca"
      local: "Teams"
      calendar: google
  conflitos: []
  notas: "Outlook capturado via print as 07:12"

tarefas:
  grupo_a_candidatos_mit:
    - id: "TSM-874"
      title: "Views Cubo ClickHouse Gold"
      list: "Chamados TI"
      tags: [captacao-receita]
      due: "2026-02-01"
      priority: high
      aging_dias: 75
  grupo_b_dia: [...]

workspace_m7:
  escopo: "statuses=[atrasada, bloqueada] no workspace inteiro"
  grupos:
    - frente: "PA-Resultado · Seguros"
      tarefas:
        - id: "TSM-1126"
          title: "Campos de meta Louro"
          assignee: "Pedro"
          due: "2026-04-15"
          status: "atrasada"
          is_self: false
        - id: "TSM-1130"
          title: "Validar calculo comissao seguros"
          assignee: "Bruno"
          due: "2026-04-10"
          status: "atrasada"
          is_self: true                # destacar como gargalo pessoal
  contadores:
    atrasadas_total: 28
    bloqueadas_total: 4
    atrasadas_bruno: 3                 # se >=3, meta gargalo vai pro header

metricas:
  - metrica: "atrasadas_workspace"
    query: "clickup_filter_tasks(statuses=[atrasada], archived=False) | len"
    count: 28
    fonte: clickup_mcp
  - metrica: "atrasadas_bruno"
    query: "atrasadas_workspace AND assignee==bruno | len"
    count: 3
    fonte: clickup_mcp
  - metrica: "tarefas_dia_visiveis"
    query: "grupo_b_dia sorted ABCDE | head(6)"
    count: 6
    fonte: clickup_mcp
  - metrica: "tarefas_dia_total"
    query: "len(grupo_b_dia)"
    count: 18
    fonte: clickup_mcp

corpo:
  peso: null
  tss_semana: null
  sono_horas: null

contexto_pfeffer:                        # v1.11.0 · substitui contexto_insight
  # Nada a extrair aqui na Fase 1 — o agente recebe agenda + mits + workspace_m7 + lide
  # diretamente da Fase 2b e produz Insight + Notas. Bloco mantido apenas para
  # documentar a ausencia de scan em brain/3-resources/.
  fonte: agents/pfeffer-power-analyst.md
```

Essa estrutura e consumida pela Fase 2 (planejamento) e pela Fase 3 (renderizacao). Nao e exposta ao usuario — e artefato interno da skill.
