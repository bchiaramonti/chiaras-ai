# Schema do .md canônico · daily planner

Ponto unico de verdade da v2. Todo .md que a skill emite e todo .md que `/planner sync` consome precisa passar por este schema.

## 1. Path e nomenclatura

```
~/Documents/brain/0-inbox/plan-review/daily/YYYY/MM/daily-YYYY-MM-DD.md
```

- `YYYY`, `MM` derivados da `date` no frontmatter (nao do clock do sistema).
- `daily-` prefixa o nome do arquivo; data em `YYYY-MM-DD`.
- A skill **cria** os diretorios `YYYY/MM/` se nao existirem.
- Sobrescrever e permitido quando re-rodar a skill no mesmo dia; a Fase 2b (insight Pfeffer) deve ser re-invocada para evitar cache de insight do run anterior.

## 2. Estrutura geral

Frontmatter YAML entre `---` ... `---`, seguido de body Markdown. H1 e o unico nivel semantico usado no body.

```markdown
---
(yaml frontmatter)
---

# Lide do dia
(prosa argumentativa)

# Insight · cruzamento
> Cap X ↔ Cap Y — POWER (Pfeffer)

(prosa do agente pfeffer-power-analyst)

# Notas do dia
- (bullet 1)
- (bullet 2)
```

## 3. Frontmatter · campos obrigatorios

Se qualquer um estiver ausente ou invalido, a skill (ou `/planner sync`) **aborta com erro explicito** antes de renderizar.

```yaml
schema: daily-planner@1
generated_at: 2026-04-22T08:15:00-03:00
generated_by: generating-daily-planner skill v2.0.0
date: 2026-04-22
weekday: quarta
day_of_year: 112
total_days: 365
iso_week: 17
month_name: abril

mits:
  - roman: i
    text: "..."
    meta: "..."
    risco: "..."
    delayed: false
  - roman: ii
    text: "..."
    meta: "..."
    risco: "..."
    delayed: true
  - roman: iii
    text: "..."
    meta: "..."
    risco: "..."
    delayed: false

amanha:
  ancora: "..."

pfeffer:
  chapters: [11, 13]
```

**Regras:**

- `schema` deve ser exatamente `daily-planner@1` (futuras breaking changes incrementam).
- `generated_at` em ISO-8601 com timezone (nao UTC puro — respeitar `-03:00` de SP).
- `date` em `YYYY-MM-DD`; `weekday` em portugues lowercase (`segunda`..`domingo`).
- `day_of_year` int 1..366; `total_days` int (365 ou 366); `iso_week` int 1..53.
- `month_name` em portugues lowercase (`janeiro`..`dezembro`).
- `mits` array de **exatamente 3 itens**. Nao 2, nao 4. Cada item:
  - `roman`: `i` | `ii` | `iii` (lowercase).
  - `text`: string com ate 2-3 entidades em `**negrito**`.
  - `meta`: tag curta (ex: `"Eat-the-frog · meta-entrega"`).
  - `risco`: pre-mortem de 1 linha (`"causa → plano B"`), ou literal `—` se nao houver risco real. **Proibido pre-mortem ficticio.**
  - `delayed`: bool. `true` se a MIT originou de task atrasada.
- `amanha.ancora`: string imperativa unica. 1 frase.
- `pfeffer.chapters`: array de exatamente 2 ints (capitulos cruzados). Ver taxonomia no agente.

## 4. Frontmatter · campos opcionais (com fallback)

Ausencia ou `null` renderiza com fallback; nao aborta.

```yaml
metrics:
  tasks_total: 14
  tasks_delayed: 5
  workspace_atrasadas: 38
  workspace_bloqueadas: 3
  workspace_mine: 19
  agenda_events: 4
  agenda_hours_blocked: 5.5

corpo:
  peso: null          # kg ou null → "—"
  sono: null          # horas ou null → "—"
  tss_semana: null    # int ou null → "—"
  tsb: null           # float ou null → "—"
  note: "sem TP"      # tag mostrada quando algum campo e null

pfeffer:
  chapters: [11, 13]
  shuffle_slot: seed   # "seed" | "1de7"..."7de7" | null (reservado futuro)

agenda:
  - start: "09:00"
    end: "10:30"
    title: "Foco · live artifact"
    is_now: false

tasks:
  - title: "Customizar POP para Investimentos"
    list: "Padronizacao Rituais"
    tag: ""
    due: "hoje"
    status: atrasada
    url: "https://app.clickup.com/t/xyz"

workspace:
  - frente: "s3-universo"
    count: 19
    tasks:
      - title: "Follow-up deal Alpha"
        assignee: "Bruno"
        due: "-7d"
        type: atrasada
        is_mine: true
        url: "https://app.clickup.com/t/abc"

amanha:
  preparar:
    - "Rodar coleta G2.2 E2 Investimentos S16"
    - "Alinhar com Pedro as metricas finais"
```

**Fallback por campo:**

| Campo ausente | Render |
|---|---|
| `metrics.*` | Omite o numero ou usa `—` |
| `corpo.peso\|sono\|tss_semana\|tsb` null | Mostra `—` + tag `corpo.note` (`"sem TP"` tipico) |
| `agenda` vazio | "agenda vazia hoje" |
| `tasks` vazio | "nenhuma task aberta no radar" |
| `workspace` vazio | "nenhuma atrasada ou bloqueada" |
| `amanha.preparar` vazio ou ausente | Omite o bloco "Preparar hoje" |

**Regras de valor:**

- `agenda[].start/end`: `HH:MM` em 24h.
- `agenda[].is_now`: bool, `true` se o evento inclui `generated_at.time`.
- `tasks[].status`: `aberta` | `atrasada` | `bloqueada` | `em-andamento`. Valores fora disso devem ter passado pela whitelist via `AskUserQuestion` (ver regra 4 de metodologia-planejamento.md).
- `tasks[].due`: `"hoje"` | `"amanha"` | `"+Nd"` | `"-Nd"` | data BR `"DD mes"`.
- `workspace[].type`: `atrasada` | `bloqueada`.
- `workspace[].is_mine`: bool. `true` quando Bruno e assignee (destaca como gargalo pessoal).

## 5. Body · blocos canonicos

### 5.1 `# Lide do dia` (obrigatorio)

Uma unica tese argumentativa em prosa, 200-400 chars. Usa `*italico*` para enfase narrativa e `**negrito**` para entidades nomeadas (projetos, pessoas, deals, metricas).

### 5.2 `# Insight · cruzamento` (obrigatorio)

Primeira linha apos o H1 deve ser uma `blockquote` com a citacao:

```markdown
> Cap 11 ↔ Cap 13 — POWER (Pfeffer)
```

Formato rigido: `> Cap N ↔ Cap M — POWER (Pfeffer)` com caractere `↔` (nao `<->`). Capitulos batem com `pfeffer.chapters` do frontmatter.

Linhas seguintes: prosa do agente `pfeffer-power-analyst`, 2-4 linhas tipicas. Mesma convencao `*italico*` / `**negrito**`.

### 5.3 `# Notas do dia` (opcional)

0-3 bullets tacticos. Cada bullet max 2 linhas. Bullets usam `**negrito**` para enfase acionavel:

```markdown
- **Pre-decisao:** listar os 5 deals mais antigos de s3-universo antes das 12h, sem meio termo.
```

Omitir o H1 inteiro se nao ha notas.

### 5.4 Blocos proibidos

- H2 (`##`) ou niveis menores.
- Tabelas Markdown (dados estruturados vivem no frontmatter).
- Code fences (` ``` `) — o planner nao e documentacao tecnica.
- HTML inline (use apenas inlines MD, veja §6).

## 6. Convencao de enfase inline

| Sintaxe MD | Render HTML | Uso |
|---|---|---|
| `*italico*` | `<em>` (accent-primary, italic) | Enfase narrativa suave (verbos, qualificadores) |
| `**negrito**` | `<em class="strong">` (accent-primary, italic, semibold) | Entidades nomeadas (projetos, pessoas, deals, metricas) |
| `[texto](url)` | `<a href="url" target="_blank">` | Apenas em `tasks[].url` e `workspace[].tasks[].url` dentro do frontmatter; nao usar links no body |
| `` `code` `` | — | **Proibido** (tom editorial, nao tecnico) |

Essa convencao substitui a abordagem v1.x de escrever `<em>` direto no texto planejado.

## 7. Campo `edits` (historico de ediçoes manuais)

Quando o usuario edita o .md durante o dia e roda `/planner sync`, o comando **append**a uma entrada em `edits[]` no frontmatter registrando o que mudou:

```yaml
edits:
  - at: 2026-04-22T14:30:00-03:00
    summary: "MIT ii marcada como concluida (delayed: false)"
  - at: 2026-04-22T16:15:00-03:00
    summary: "Adicionado bullet em amanha.preparar"
  - at: 2026-04-22T18:00:00-03:00
    summary: "Reescrito # Insight · cruzamento"
```

**Regras:**

- `edits` e array, ordem cronologica crescente (mais antigo primeiro).
- Ausente ou `[]` significa "nunca editado apos geracao inicial".
- `at`: ISO-8601 com timezone, mesmo formato de `generated_at`.
- `summary`: string curta (max ~80 chars) descrevendo **o que** mudou, nao **por que**.
- O `/planner sync` e o unico emissor de entradas em `edits[]`. A skill base nao escreve nesse campo (gera .md com `edits: []` ou campo ausente).
- Deteccao de diff: comparar o .md pre-edit (snapshot em memoria do ultimo `generated_at` ou do ultimo `edits[].at`) com o estado atual. Gerar 1-3 linhas de summary descrevendo as maiores mudancas.
- Util para retrospectiva semanal: ver quais MITs foram concluidas ao longo do dia vs empurradas.

## 8. Validaçao (pseudo-algoritmo)

```
1. Parse frontmatter YAML. Se falha → abort("YAML invalido em {path}: {error}")
2. Verificar schema == "daily-planner@1". Se diferente → abort("schema {x} incompativel com v2.0.0")
3. Verificar campos obrigatorios do §3. Se algum ausente → abort("campo obrigatorio ausente: {field}")
4. Verificar mits.length == 3. Se diferente → abort("mits precisa ter exatamente 3 itens")
5. Verificar pfeffer.chapters.length == 2 e ambos int. Se diferente → abort
6. Parse body. Extrair H1 "Lide do dia" (obrigatorio). Se ausente → abort
7. Extrair H1 "Insight · cruzamento" (obrigatorio). Primeira linha apos H1 deve match regex `^> Cap \d+ ↔ Cap \d+ — POWER \(Pfeffer\)$`. Se nao → abort
8. Extrair H1 "Notas do dia" (opcional). Se presente, conteudo = bullets.
9. Ok → prosseguir para render
```

## 9. Exemplo minimal valido

```markdown
---
schema: daily-planner@1
generated_at: 2026-04-22T08:00:00-03:00
generated_by: generating-daily-planner skill v2.0.0
date: 2026-04-22
weekday: quarta
day_of_year: 112
total_days: 365
iso_week: 17
month_name: abril
mits:
  - roman: i
    text: "Entregar **WBR Investimentos** do S16"
    meta: "Eat-the-frog · compromisso publico"
    risco: "—"
    delayed: false
  - roman: ii
    text: "Revisar **POP Seguros** com Filipe"
    meta: "90min bloqueio 14h"
    risco: "Filipe atrasar → reagendar para 16h"
    delayed: false
  - roman: iii
    text: "Treino Z2 45min"
    meta: "corpo · balance"
    risco: "—"
    delayed: false
amanha:
  ancora: "validar pipeline G3 com Pedro antes da 1:1"
pfeffer:
  chapters: [6, 11]
---

# Lide do dia

Bruno entrega o *WBR Investimentos* enquanto fecha a janela de revisao do **POP Seguros** com Filipe.

# Insight · cruzamento

> Cap 6 ↔ Cap 11 — POWER (Pfeffer)

Construir reputacao (Cap 6) exige mostrar resultados publicos; *perder poder* (Cap 11) vem de acumular entregas incompletas.
```

Esse exemplo passa em toda validacao mesmo sem `metrics`, `corpo`, `agenda`, `tasks`, `workspace`, `amanha.preparar` ou `# Notas do dia`.
