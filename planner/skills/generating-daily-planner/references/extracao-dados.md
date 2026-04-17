# Fase 1 · Extracao de dados

A primeira passada da skill e **levantamento**. Antes de planejar o dia, o Claude reune as entradas de cinco fontes. Para cada fonte ha uma rota primaria (MCP direto) e um fallback (perguntar ao usuario).

**Regra de ouro:** nunca invente dado. Se nao conseguir extrair e o usuario nao forneceu, a secao correspondente no HTML fica com `&mdash;` ou e omitida — nunca preenchida com ficcao.

## Indice

- [Matriz de fontes](#matriz-de-fontes)
- [1. Agenda](#1-agenda)
- [2. Tarefas ClickUp (tres inadiaveis + tarefas do dia)](#2-tarefas-clickup-tres-inadiaveis--tarefas-do-dia)
- [3. Delegadas](#3-delegadas)
- [4. Corpo / saude](#4-corpo--saude)
- [5. Contexto para o insight](#5-contexto-para-o-insight)
- [Protocolo de fallback](#protocolo-de-fallback)
- [Schema da extracao](#schema-da-extracao)

## Matriz de fontes

| Secao do planner | Fonte primaria | MCP / Ferramenta | Fallback |
|---|---|---|---|
| Agenda | Google Calendar + Outlook M7 | `mcp__claude_ai_Google_Calendar__*` (Google) · *Outlook sem MCP* | Pedir print ou texto da agenda |
| Tres inadiaveis | ClickUp (tags `mit`, `hoje`, `inadiavel`) ou usuario | `mcp__claude_ai_ClickUp__clickup_filter_tasks` | Pedir ao usuario os 3 diretamente |
| Tarefas ClickUp | ClickUp (due = hoje/amanha/atrasadas, assignee = Bruno) | `mcp__claude_ai_ClickUp__clickup_filter_tasks` | Pedir print da lista "Hoje" |
| Delegadas | ClickUp (assignee != Bruno, criadas por Bruno, status aberto) | `mcp__claude_ai_ClickUp__clickup_filter_tasks` | Pedir resumo verbal |
| Corpo (peso, TSS, sono, HRV, forma) | TrainingPeaks (cookie-based auth) | `mcp__trainingpeaks__*` | Perguntar ao usuario se o MCP falhar |
| Contexto insight | Filesystem `brain/3-resources/` (PARA) | `Glob`, `Grep`, `Read` | Nao ha fallback — se vazio, pular insight |

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

Filtrar o resultado em dois grupos:

**Grupo A · Candidatos a Tres inadiaveis** (5-10 tasks)
- Tags contem `mit`, `hoje`, `inadiavel`, `urgente`, `critico`, OU
- Due date = hoje, OU
- Prioridade = urgent/high + atrasada
- Lista de origem tem peso estrategico (nao helpdesk)

**Grupo B · Tarefas do dia** (resto, ate 15 linhas)
- Todas as demais due <= amanha ou atrasadas

### Metadata obrigatoria por task

Para cada task retornada, capturar:
- `id` (ex: `TSM-874`)
- `title`
- `list_name` (nome da lista — vira display no planner)
- `tags[]` (vira display junto da lista)
- `due_date` (usado para classificar atraso e formatar "+Nd")
- `priority` (urgent/high/normal/low)
- `status`

O display final no HTML segue a regra de [componentes.md secao 9](componentes.md): `<titulo> · <lista> · <tag(s)>` + `<due>`.

### Fallback

Se ClickUp MCP falhar:

> Nao consegui extrair as tarefas do ClickUp. Voce pode me dar:
> 1. Os 3 inadiaveis de hoje (titulo + lista + SLA)
> 2. Uma lista curta (ate 8) de outras tarefas abertas com due <= amanha

## 3. Delegadas

### Rota primaria

```
mcp__claude_ai_ClickUp__clickup_filter_tasks (
  assignees=[NOT Bruno],  # ClickUp nao suporta NOT — filtrar pos-query
  created_by=Bruno,
  statuses=open
)
```

Agrupar por **projeto/lista** e ordenar cada grupo por atraso (atrasadas no topo). Limite: 4-5 grupos, 2-3 linhas por grupo.

### Metadata obrigatoria

- `title`
- `assignee` (nome) — vira display `· <pessoa>`
- `project` ou `list_name` — vira cabecalho do grupo `.delegadas__project`
- `due_date`
- `status`

### Fallback

> Nao consegui extrair as delegadas. Me passa um resumo em formato:
> - [Projeto] Titulo · [Pessoa] · [SLA]

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

## 5. Contexto para o insight

Fonte unica: **filesystem `/Users/bchiaramonti/Documents/brain/3-resources/`**.

Essa extracao e preguicosa — nao le os arquivos ainda, apenas inventaria. A leitura real acontece na geracao do insight (ver [insight-cruzamento.md](insight-cruzamento.md)).

### Passo 1 · Identificar temas de desafio do dia

A partir dos Tres inadiaveis + Lide (ja planejados na Fase 2), derivar 2-3 **temas** (1-3 palavras cada). Exemplos:
- MIT "Definir KPIs/PPIs do Ritual N2 Investimentos" → tema `rituais-gestao`, `kpis`, `falconi-gpd`
- MIT "Cobrar Pedro nos chamados TI Louro" → tema `lideranca-situacional`, `delegacao`, `follow-up`

### Passo 2 · Inventariar subdiretorios relevantes em 3-resources

```
Glob: brain/3-resources/**/*.md
```

Filtrar por caminhos/nomes que contenham os temas (case-insensitive, stem matching). Limite: ate 10 candidatos.

### Passo 3 · Passar o inventario para a fase de Insight

Saida para a proxima fase:
```yaml
temas: [rituais-gestao, lideranca-situacional]
candidatos:
  - brain/3-resources/livros/deep-work.md
  - brain/3-resources/metodologias/gpd-falconi.md
  - brain/3-resources/lideranca/situational-leadership-hersey.md
  ...
```

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

delegadas:
  grupos:
    - projeto: "PA-Resultado · Seguros"
      tarefas:
        - title: "TSM-1126 Campos de meta Louro"
          assignee: "Pedro"
          due: "2026-04-15"
          urgencia: urgent

corpo:
  peso: null
  tss_semana: null
  sono_horas: null

contexto_insight:
  temas: [rituais-gestao, lideranca-situacional]
  candidatos_3resources:
    - brain/3-resources/...
```

Essa estrutura e consumida pela Fase 2 (planejamento) e pela Fase 3 (renderizacao). Nao e exposta ao usuario — e artefato interno da skill.
