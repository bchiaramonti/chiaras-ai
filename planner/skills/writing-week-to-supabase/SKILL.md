---
name: writing-week-to-supabase
description: Persiste no Supabase (projeto bc-planning) o objeto canônico de uma semana — modo "plano" (weeks + focus_items + days + tasks + risks + preflight_items) ou modo "review" (weekly_reviews). Upsert idempotente por (user_id, year, week_num) via delete-then-insert. Escreve via o MCP bc-planning_ (service_role, ignora RLS), setando user_id do dono, last_sync_at e order_index. Determinística: NÃO planeja nem conversa (isso é da planning-the-week) e NÃO renderiza (o front faz). Use quando já existir um objeto canônico de plano/review pronto para gravar.
license: Proprietary
---

# Writing Week to Supabase — persistência

Skill **determinística** de escrita. Recebe o **objeto canônico** (emitido pela
`planning-the-week`) e grava no Postgres do Supabase. Não pensa, não conversa, não renderiza.

## Alvo e canal
- Projeto **bc-planning** · ref `fffowcpzrgeoreiffrrb` · URL `https://bc-planning.vercel.app`.
- Canal: MCP **`bc-planning_`** → `execute_sql`. (Fallback: `plugin:supabase:supabase`
  `execute_sql` com `project_id=fffowcpzrgeoreiffrrb`.) Ambos usam service_role → **ignoram
  RLS**, por isso o `user_id` do dono é setado explicitamente em cada linha.
- Contrato do objeto: ver `planning-the-week/SKILL.md` (forma enxuta) e o schema em
  `0-inbox/plan-review/supabase/migrations/0001_init.sql` (+ `seed.sql` como modelo do upsert).

## Regras de dados (CRÍTICAS — evitam SQL quebrado / dados sujos)
- **Escapar aspas simples**: todo texto vai em literal SQL com `'` → `''`.
- **`prio`**: `''` (vazio) vira **`NULL`** (CHECK aceita só `P1|P2|P3` ou NULL).
- **Coluna `"time"`**: sempre entre aspas duplas (palavra reservada). Ausente → `NULL`.
- **`people`/`wins`/`frictions`/`seeds`**: `text[]` → `array['a','b']` (vazio = `'{}'`).
- **`stats`/`delivered`**: `jsonb` → `'[...]'::jsonb`. `color` ∈
  `success|warning|accent|accent-2|ink|muted`; `status` ∈ `Feito|Parcial|Movido`.
- **`order_index`** denso (0..n) na ordem do objeto (focus, days, tasks, risks, preflight).
- **`last_sync_at`**: `now()` no upsert do plano (é o carimbo "Claude Cowork" do header).
- **Idempotência**: re-rodar a mesma semana **substitui** (delete-then-insert), nunca duplica.

## Resolução do dono
`user_id` = `select id from auth.users where email = 'bchiaramonti@gmail.com'`. Se nulo,
**abortar** (o usuário Auth precisa existir). Multi-user futuro: receber o e-mail/uid como parâmetro.

## Modo PLANO — `execute_sql` (um do-block, transacional)
```sql
do $$
declare
  v_email text := 'bchiaramonti@gmail.com';
  v_uid uuid; v_week uuid; v_day uuid;
begin
  select id into v_uid from auth.users where email = v_email;
  if v_uid is null then raise exception 'dono % inexistente em auth.users', v_email; end if;

  -- idempotência: limpa a semana (cascade remove filhas)
  delete from public.weeks where user_id = v_uid and year = {YEAR} and week_num = {WEEK_NUM};

  insert into public.weeks (user_id, week_num, year, range, sub,
      lede_a, lede_accent, lede_b, insight_text, insight_ref, created_by, last_sync_at)
    values (v_uid, {WEEK_NUM}, {YEAR}, '{RANGE}', '{SUB}',
      '{LEDE_A}', '{LEDE_ACCENT}', '{LEDE_B}', '{INSIGHT_TEXT}', '{INSIGHT_REF}',
      'claude-skill', now())
    returning id into v_week;

  insert into public.focus_items (week_id, user_id, number, text, order_index) values
    (v_week, v_uid, '01', '{FOCO_1}', 0),
    (v_week, v_uid, '02', '{FOCO_2}', 1),
    (v_week, v_uid, '03', '{FOCO_3}', 2);

  -- por dia (repetir para os 5; order_index 0..4):
  insert into public.days (week_id, user_id, name, short, date, theme, entrega, order_index)
    values (v_week, v_uid, '{NAME}', '{SHORT}', '{DATE}', '{THEME}', '{ENTREGA}', {DAY_IDX})
    returning id into v_day;
  insert into public.tasks (day_id, week_id, user_id, src, title, prio, "time", people, order_index) values
    (v_day, v_week, v_uid, '{SRC}', '{TITLE}', {PRIO_OR_NULL}, {TIME_OR_NULL}, {PEOPLE_ARR}, {TASK_IDX});
  -- ... demais tasks do dia ...

  insert into public.risks (week_id, user_id, title, mitig, order_index) values
    (v_week, v_uid, '{R_TITLE}', '{R_MITIG}', {R_IDX});

  insert into public.preflight_items (week_id, user_id, q, a, order_index) values
    (v_week, v_uid, '{Q}', '{A}', {P_IDX});
end $$;
```
(`{TIME_OR_NULL}` = `'18:00'` ou `null`; `{PRIO_OR_NULL}` = `'P1'` ou `null`;
`{PEOPLE_ARR}` = `array['Ana','Léo']` ou `'{}'`.)

## Modo REVIEW — `execute_sql`
```sql
do $$
declare
  v_email text := 'bchiaramonti@gmail.com';
  v_uid uuid; v_week uuid;
begin
  select id into v_uid from auth.users where email = v_email;
  select id into v_week from public.weeks where user_id = v_uid and year = {YEAR} and week_num = {WEEK_NUM};
  if v_week is null then raise exception 'semana %/% não existe — grave o plano antes do review', {WEEK_NUM}, {YEAR}; end if;

  delete from public.weekly_reviews where week_id = v_week;          -- idempotente (1:1)
  insert into public.weekly_reviews (week_id, user_id, lede, learning, learning_ref,
      stats, delivered, wins, frictions, seeds)
    values (v_week, v_uid, '{LEDE}', '{LEARNING}', '{LEARNING_REF}',
      '{STATS_JSON}'::jsonb, '{DELIVERED_JSON}'::jsonb,
      {WINS_ARR}, {FRICTIONS_ARR}, {SEEDS_ARR});
end $$;
```

## Depois de gravar
1. Conferir (`execute_sql`): contagens da semana (1 week, N focus/days/tasks/risks/preflight; review = 1).
2. Reportar: `id` da semana + link `https://bc-planning.vercel.app` (logar como o dono mostra a semana).

## Nunca fazer
- Planejar/conversar (é da `planning-the-week`) ou renderizar HTML (é do front).
- Escrever sem setar `user_id` do dono (service_role ignora RLS → sem dono = órfão).
- Esquecer de escapar `'`, ou inserir `prio=''` (deve ser `NULL`).
- Inserir review de uma semana cujo plano não existe.
- Persistir campos fora do schema enxuto (Corpo/Prazos/Critério/etc. — v1 não tem coluna).
