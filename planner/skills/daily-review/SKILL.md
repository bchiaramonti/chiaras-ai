---
name: daily-review
description: Fecha e revisa UM dia do planejamento semanal e replaneja o dia seguinte. Lê o dia no Supabase (plano + tarefas com `done` + o `journal_raw` que o Bruno escreveu no front), relê as fontes (Google Calendar, ClickUp, Fireflies, Slack, e-mail), identifica o que foi feito × o que ficou aberto, reescreve o journal enriquecido, carrega os itens abertos para o dia seguinte e persiste via writing-week-to-supabase (modos daily-review + day). Conversacional (pensa); não renderiza e não grava direto. Use quando o Bruno pedir para fechar/revisar o dia, fazer o "daily review", ou ao final do expediente.
license: Proprietary
---

# Daily Review — fechar o dia e replanejar o seguinte

Skill **conversacional** (thread principal). Ela **pensa** (relê fontes, cruza com o
plano, reescreve o journal, replaneja o amanhã) e **persiste via
`writing-week-to-supabase`**. Não renderiza (o front faz) e não escreve direto no banco.

## Separação
- **`daily-review` (PENSAR):** lê o dia, relê fontes, monta feito×aberto, reescreve o
  journal e o replano do dia seguinte; despacha o Pfeffer se útil.
- **`writing-week-to-supabase` (PERSISTIR):** modo `daily-review` (grava
  `daily_reviews.journal/done_summary/open_items` + `tasks.done`) e modo `day` (grava o
  dia seguinte replanejado). Projeto `bc-planning` (ref `fffowcpzrgeoreiffrrb`) via `bc-planning_`.
- **Fronteira do dono:** o `journal_raw` é do Bruno (escrito no front) — **só leio**, nunca
  sobrescrevo. O que escrevo é o `journal` (versão enriquecida).

## Fluxo
1. **Resolver o dia alvo** — hoje em `America/Sao_Paulo` (ou data/weekday informado).
   Achar a semana/dia no Supabase via `bc-planning_` (`execute_sql`):
   ```sql
   select w.week_num, w.year, d.id day_id, d.name, d.date, d.intention, d.entrega,
          coalesce(dr.journal_raw,'') journal_raw,
          (select json_agg(json_build_object('id',t.id,'title',t.title,'prio',t.prio,
              'time',t."time",'src',t.src,'done',t.done) order by t.order_index)
             from public.tasks t where t.day_id = d.id) tasks
   from public.weeks w join public.days d on d.week_id = w.id
     left join public.daily_reviews dr on dr.day_id = d.id
   where w.user_id = (select id from auth.users where email='bchiaramonti@gmail.com')
     and d.date = '{DD}' and w.year = {YEAR};   -- ou por (week_num, name)
   ```
   Ler também o **dia seguinte** (para replanejar).
2. **Reler as fontes do dia** — reusar [../planning-the-week/references/extracao-dados.md](../planning-the-week/references/extracao-dados.md)
   (Google Calendar, ClickUp, **Fireflies**, **Slack**, **e-mail**) restritas ao dia.
3. **Feito × aberto** — cruzar tasks + `done` (marcadas pelo Bruno no front) + evidência
   das fontes. Montar `done_summary` (o que saiu) e `open_items[]` (o que ficou).
   Marcar `done` as tarefas que as fontes confirmam concluídas (mesmo sem check no front).
4. **Reescrever o journal** — partir do `journal_raw` do Bruno **+ as fontes** → `journal`
   factual e enxuto (tom de [../planning-the-week/references/regras-texto.md]). Pfeffer
   opcional para 1 leitura de poder.
5. **Replanejar o dia seguinte** — carregar os `open_items` para o day+1 (ajustar
   `intention`/`entrega`/tarefas), **sem duplicar** o que já está lá. Se o day+1 for de
   outra semana **ainda não planejada** → avisar e sugerir `planning-the-week`.
6. **Confirmar + persistir** — mostrar ao Bruno; ao confirmar, invocar
   **`writing-week-to-supabase`**: modo `daily-review` (dia revisado) e modo `day`
   (dia seguinte replanejado). Reportar o link do front.

## Objetos canônicos (→ writing-week-to-supabase)
```yaml
daily-review:                 # grava o review do dia revisado
  weekNum: "25"; year: 2026; dayName: "Segunda"      # ou date
  journal: "..."             # versão enriquecida (NÃO é o journal_raw)
  doneSummary: "..."
  openItems: ["...", "..."]
  doneTaskIds: ["uuid", ...] # tarefas confirmadas concluídas

day:                          # replano do dia SEGUINTE (futuro)
  weekNum: "25"; year: 2026; dayName: "Terça"
  intention: "..."; entrega: "..."
  tasks: [ { src, title, prio, time, people } ]
```

## Nunca fazer
- **Sobrescrever `journal_raw`** (é do dono) — escrever só `journal`.
- **Inventar conclusão** sem evidência (fonte real ou check do dono).
- Usar o modo `day` no **dia em curso** (apaga tasks/`done`) — replano é só do dia seguinte.
- Replanejar um dia que não existe (avisar p/ planejar a semana).
- Renderizar HTML ou gravar direto sem a `writing-week-to-supabase`.
