---
name: planning-the-week
description: Companheira de planejamento semanal do Bruno — CONVERSA para planejar a semana e, no fim da semana, para fazer o review. Mapeia as fontes (Google Calendar + ClickUp), conduz o planejamento aplicando a metodologia executiva (8 regras) como diálogo, sempre invoca o subagente pfeffer-power-analyst para o Insight · cruzamento, e ao final produz um OBJETO CANÔNICO (forma enxuta) que entrega à skill writing-week-to-supabase para persistir no banco. NÃO renderiza HTML (o front na Vercel renderiza) e NÃO escreve no banco diretamente (isso é da writing-week-to-supabase). Use quando o Bruno pedir para planejar/ajustar a semana, preparar a semana N, fazer sunday planning, ou fazer o review/retrospectiva da semana. Escopo estritamente pessoal — não usar em outputs M7/corporativos.
license: Proprietary
---

# Planning the Week — companheira de planejamento

Skill **conversacional** (roda na thread principal). Ela **pensa junto** com o Bruno;
**não persiste** (quem grava é a `writing-week-to-supabase`) e **não renderiza**
(o front Next.js na Vercel renderiza, lendo o Supabase).

**Princípio:** o plano só serve se for executável e fiel às fontes. Metodologia primeiro,
texto depois. A companheira **conversa e ajusta** — não despeja um plano pronto.

## Separação de responsabilidades
- **Esta skill (PENSAR):** mapeia fontes, conduz o planejamento/review em diálogo,
  aciona o Pfeffer, e emite o **objeto canônico** validado.
- **`writing-week-to-supabase` (PERSISTIR):** recebe o objeto canônico e faz upsert no
  Supabase via o MCP `bc-planning_`.
- **`pfeffer-power-analyst` (subagente):** única fonte do Insight · cruzamento.

## Dois modos

### Modo PLANO (planejar a semana)
1. **Ler a semana anterior no Supabase (retrospectiva) — PRIMEIRO, NÃO PERGUNTAR.**
   Via o MCP **`bc-planning_`** (`execute_sql`), ler do dono a `weekly_reviews` da semana
   **N-1** (`lede/learning/wins/frictions/seeds`) e o plano da S-1 (`weeks` + filhas).
   **Isso É a retrospectiva** — não pergunte ao Bruno o que o banco já tem. Carregar os
   `seeds[]` da review da S-1 como sementes a puxar para a nova semana. **Só perguntar**
   o que faltar: se a S-1 **não tiver review** no banco (sugerir rodar o modo REVIEW dela
   antes), ou complementos. Atenção ao **rollover de ano** (planejando a semana 1, a
   anterior é a última semana do ano anterior).
2. **Mapear fontes externas** — ler [references/extracao-dados.md](references/extracao-dados.md).
   Varrer **TODAS** as fontes (não só Calendar/ClickUp):
   - **Agenda** (Google Calendar MCP, seg–sex) e **Tarefas/Workspace M7** (ClickUp MCP).
   - **Fireflies** — transcrições/resumos das **últimas reuniões** → action items, decisões, follow-ups.
   - **Slack** — **conversas recentes** → compromissos, pedidos, threads a acompanhar.
   - **E-mail** — **Outlook M7 + Gmail** → pendências de resposta, pedidos, compromissos.

   Cada pendência vira candidata a tarefa (`src` = CU/CA/FF/SL/EM/GM), risco ou foco —
   **sem duplicar** o que já está no ClickUp. Apresentar um **snapshot** ao Bruno.
   Corpo/TrainingPeaks e Metas Q2 podem ser **discutidos**, mas **não entram no objeto**
   (v1 enxuto). Nunca inventar dado.
3. **Conversar/planejar** — ler [references/metodologia-planejamento.md](references/metodologia-planejamento.md)
   e conduzir como **diálogo** (não one-shot), ajustando com o Bruno. Mapear o método
   para a **forma enxuta** (ver "Mapeamento" abaixo): **Tese** → lede (conectada à
   retrospectiva lida no passo 1); **Foco da semana (3)** (= Três grandes/Big 3);
   **Orquestra dos 5 dias** (tema + **foco do dia** `intention` + entrega + tarefas); **Riscos & fogos**;
   **Preflight (4)**. Manter o tom de [references/regras-texto.md](references/regras-texto.md).
4. **Insight** — despachar o subagente [`pfeffer-power-analyst`](../../agents/pfeffer-power-analyst.md)
   (horizonte=weekly) e aplicar as regras de [references/insight-cruzamento.md](references/insight-cruzamento.md).
   Resultado → `insight.text` + `insight.ref` (ex.: `POWER · Cap 9 × Cap 7`).
5. **Emitir + confirmar** — montar o **objeto canônico (plano)**, mostrar ao Bruno para
   confirmação e, ao confirmar, **invocar a skill `writing-week-to-supabase` (modo plano)**
   passando o objeto. Reportar o link do front (`https://bc-planning.vercel.app`).

### Modo REVIEW (fim da semana)
1. **Retrospectiva** — perguntar ao Bruno: o que **destravou** (vitórias), o que
   **travou** (atritos), o que **aprendi** (lição + ref, ex.: capítulo POWER).
2. **Planejado × entregue** — cruzar o plano da semana (no Supabase / ClickUp) e montar
   `delivered[]` (`{title, status: Feito|Parcial|Movido}`) e `stats[]`
   (`{k, v, color}` — ex.: Entregue 11/13, Reuniões, Foco protegido).
3. **Sementes** — `seeds[]` (itens que migram para a próxima semana).
4. **Emitir + confirmar** — montar o **objeto canônico (review)** e invocar
   `writing-week-to-supabase` (modo review).

## Objeto canônico (contrato com a skill de escrita)
Forma **enxuta** = o que o front renderiza (`lib/types.ts` de `0-inbox/plan-review/`).

```yaml
# modo PLANO
weekNum: "26"          # ISO week
year: "2026"
range: "23–27 jun"     # dd–dd mes
sub: "Semana atual"    # rótulo da sidebar
lede:    { a: "...", accent: "...", b: "..." }   # Tese, com 1 trecho de acento no meio
insight: { text: "...", ref: "POWER · Cap X × Cap Y" }
focus:                  # Foco da semana = Três grandes (exatamente 3)
  - { n: "01", text: "..." }
  - { n: "02", text: "..." }
  - { n: "03", text: "..." }
days:                   # Orquestra (exatamente 5: seg–sex)
  - name: "Segunda"; short: "Seg"; date: "23"; theme: "..."; intention: "foco do dia (1 frase)"; entrega: "..."
    tasks:
      - { src: "CA", title: "...", prio: "P1", time: "09:00–10:00", people: ["..."] }
      - { src: "CU", title: "...", prio: "P2" }     # prio "" e time/people opcionais
risks:     [ { title: "...", mitig: "..." } ]
preflight: [ { q: "...", a: "..." } ]               # 4 perguntas

# modo REVIEW
weekNum: "26"; year: "2026"
lede: "..."; learning: "..."; learningRef: "POWER · Cap 13 Showing up"
stats:     [ { k: "Entregue", v: "11/13", color: "success" } ]
delivered: [ { title: "...", status: "Feito" } ]    # Feito | Parcial | Movido
wins: [ "..." ]; frictions: [ "..." ]; seeds: [ "..." ]
```

**`src`** (origem da tarefa): `CU` ClickUp · `SL` Slack · `EM` Outlook/e-mail ·
`CA` Outlook Calendar · `GM` Gmail · `GC` Google Calendar · `FF` Fireflies.
**`prio`**: `P1|P2|P3` ou `""`. **`color`** (stats): `success|warning|accent|accent-2|ink|muted`.

## Mapeamento método → enxuto
- **Persistir:** Tese→`lede`; Insight→`insight`; **Foco/Big 3 (3)**→`focus`;
  Orquestra→`days`+`tasks`; Riscos→`risks`; Preflight→`preflight`; Retrospectiva→review.
- **Discutir mas NÃO persistir (v1):** Critério de vitória, Prazos duros, Corpo/TSS,
  "pronto quando" + link Metas Q2, energia por dia, capítulo Pfeffer do risco.
  (Entram só se o schema/front forem estendidos numa v2.)

## Nunca fazer
- **Escrever no banco diretamente** — sempre via `writing-week-to-supabase`.
- **Renderizar HTML / tokens / template** — o front é dono do visual.
- **Inventar dados** quando a extração falha — perguntar ao Bruno ou omitir.
- **Pular a conversa** e despejar um plano pronto — a companheira ajusta em diálogo.
- **Persistir os campos "discutir mas não persistir"** na v1.

## Nota sobre as references migradas
`extracao-dados`, `metodologia-planejamento`, `insight-cruzamento` e `regras-texto` vêm
da antiga `generating-weekly-planner`. **Ignore** nelas qualquer menção a Fase de
**render**, HTML, `tokens.css`/`template-html`, `.md` canônico, `/sync` ou Cowork —
isso foi aposentado. O **único output** desta skill é o **objeto canônico** acima,
entregue à `writing-week-to-supabase`. A fonte de verdade é o **Supabase**.
