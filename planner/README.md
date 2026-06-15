# planner

> Personal plugin — planejamento semanal executivo do Bruno, separando **pensar** de
> **persistir**: uma companheira conversacional planeja a semana e uma skill
> determinística grava no Supabase. O **front Next.js na Vercel** renderiza.

## Arquitetura

```
planning-the-week (skill, conversa) ── despacha ──▶ pfeffer-power-analyst (agente)
        │  mapeia fontes (Calendar + ClickUp), planeja em diálogo, emite o OBJETO canônico
        ▼
writing-week-to-supabase (skill, grava) ──▶ Supabase (bc-planning, via MCP bc-planning_)
                                                  ▲
                                   front Next.js/Vercel LÊ e renderiza (bc-planning.vercel.app)
```

## Componentes

| Item | Papel |
|---|---|
| `planning-the-week` (skill) | **Pensar.** Mapeia fontes, conduz o planejamento/review em diálogo (8 regras), aciona o Pfeffer e emite o objeto canônico (forma enxuta). Não grava, não renderiza. |
| `writing-week-to-supabase` (skill) | **Persistir.** Upsert idempotente do plano/review no Supabase (`bc-planning`) via MCP `bc-planning_`. Modos `plano` e `review`. |
| `pfeffer-power-analyst` (agente) | Fonte única do Insight · cruzamento (2 capítulos do POWER, Pfeffer). |

## Dependências de MCP (não bundladas — vêm do ambiente)
- `planning-the-week`: **Google Calendar** + **ClickUp** (mapear fontes).
- `writing-week-to-supabase`: **`bc-planning_`** (Supabase do projeto; service_role).

## Triggers
- Planejar: "planeja minha semana", "prepara a semana N", "sunday planning".
- Review: "fazer o review da semana", "retrospectiva da semana".

## Escopo
Estritamente pessoal. Não usar em apresentações M7, comunicados ou documentos corporativos.

## v1 enxuto
Persiste só o que o front renderiza hoje (Tese, Insight, Foco da semana, Orquestra dos
5 dias + tarefas, Riscos, Preflight, Review). A metodologia rica (Critério de vitória,
Prazos duros, Corpo/TSS, Big 3 ↔ Metas Q2) é **discutida na conversa**, mas só será
persistida se o schema/front forem estendidos numa v2. **Fonte de verdade = Supabase**
(sem `.md` local, sem `/sync`, sem Cowork). Ver `0-inbox/plan-review/CLAUDE.md`.

## Instalação
```
/plugin install planner@bchiaramonti-plugins
```

## Autor
Bruno Chiaramonti
