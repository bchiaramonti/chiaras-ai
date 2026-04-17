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
| Corpo (peso, TSS, sono) | *Sem MCP atualmente* (Garmin foi removido em v1.3.0) | — | Sempre perguntar ao usuario |
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

**Nao ha MCP de saude disponivel** (Garmin MCP removido em v1.3.0 devido a bloqueio da Garmin por Cloudflare TLS fingerprinting).

### Protocolo atual

Sempre perguntar ao usuario no inicio da extracao:

> Para preencher a zona Corpo, me passa os 3 numeros (se tiver — se faltar, deixo em `—`):
> - peso (kg)
> - TSS da semana ate hoje
> - sono da ultima noite (horas)

Aceitar respostas parciais. Campos nao fornecidos viram `<div class="header__corpo-number header__corpo-number--empty">&mdash;</div>`.

### Regras de cor do numero

Aplicadas apos extracao, antes de renderizar (ver [componentes.md secao 5](componentes.md)):
- peso → default (neutro)
- TSS → `--body` (azul petroleo, dado de performance)
- sono < 7h → `--alert` (terracota escuro)
- sono >= 7h → `--body` (azul petroleo)

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
