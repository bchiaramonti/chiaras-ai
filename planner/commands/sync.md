---
description: Re-renderiza o live artifact daily-planner-live a partir do .md canonico do dia (layout viewport-adaptive v2.1.0 com meta-footer e agenda so-eventos), sem re-extrair dados nem re-invocar o agente Pfeffer.
---

Le o .md do dia atual em `~/Documents/brain/0-inbox/plan-review/daily/YYYY/MM/daily-YYYY-MM-DD.md`, parseia frontmatter YAML + body Markdown, re-renderiza o HTML seguindo [render-from-md.md](../skills/generating-daily-planner/references/render-from-md.md) da skill `generating-daily-planner`, e publica via `mcp__cowork__update_artifact({id: 'daily-planner-live', html, mcp_tools: [], update_summary})`.

A partir da v2.1.0, o HTML regenerado deve manter o layout viewport-adaptive (`html, body { height: 100vh; overflow: hidden }` via [tokens.css](../skills/generating-daily-planner/references/tokens.css)), emitir apenas as linhas reais da agenda (ver [render-from-md.md §2.2](../skills/generating-daily-planner/references/render-from-md.md)) e incluir o meta-footer de rastreabilidade com os 5 spans fixos (ver §2.3).

Depois da publicaçao, detecta o diff em relaçao ao snapshot anterior e faz append em `edits[]` no frontmatter do .md — ver [schema-md.md §7](../skills/generating-daily-planner/references/schema-md.md).

## Quando usar

Apos editar manualmente o .md durante o dia. Exemplos:

- Concluiu uma MIT → trocar `delayed: false` + ajustar `text` com anotaçao de conclusao
- Adicionou uma nota nova ao `# Notas do dia`
- Reescreveu a `# Lide do dia` com enfoque mais afiado
- Reescreveu o `# Insight · cruzamento` (mantendo a citaçao no formato canonico)
- Adicionou/removeu bullet em `amanha.preparar`
- Corrigiu uma metrica numerica ou um status de task

## Fluxo

1. Resolver data atual em `YYYY-MM-DD` (America/Sao_Paulo)
2. Construir path: `~/Documents/brain/0-inbox/plan-review/daily/YYYY/MM/daily-YYYY-MM-DD.md`
3. Se arquivo nao existe → abortar com mensagem: `"O daily de {data} ainda nao foi gerado. Rode a skill generating-daily-planner primeiro."`
4. Ler o arquivo (UTF-8)
5. Parsear frontmatter + body; validar contra [schema-md.md §8](../skills/generating-daily-planner/references/schema-md.md)
6. Se schema incompativel → abortar com versao detectada vs esperada (`daily-planner@1`)
7. Renderizar HTML seguindo [render-from-md.md](../skills/generating-daily-planner/references/render-from-md.md), incluindo:
   - Agenda **so com eventos reais** (sem linhas vazias) conforme [§2.2](../skills/generating-daily-planner/references/render-from-md.md)
   - `.header__corpo-ref` em cada KPI com valor preenchido conforme [§2.1](../skills/generating-daily-planner/references/render-from-md.md)
   - **Meta-footer** com 5 spans fixos (schema/fonte/gerado/skill/insight) conforme [§2.3](../skills/generating-daily-planner/references/render-from-md.md) — usar **`generated_at` original do .md** no span `gerado:`, nao a hora do sync
   - Layout viewport-adaptive (CSS inline de [tokens.css](../skills/generating-daily-planner/references/tokens.css), sem `@media`)
8. Publicar: `mcp__cowork__update_artifact({id: 'daily-planner-live', html, mcp_tools: [], update_summary: 'Daily YYYY-MM-DD · sync manual · <resumo>'})`
9. Se retornar "artifact nao encontrado" → abortar com mensagem orientando rodar a skill primeiro (`/sync` nao cria artifact)
10. Detectar diff em relaçao ao snapshot anterior do .md. Gerar 1-3 summaries curtos (`"MIT ii concluida"`, `"Insight reescrito"`, `"Adicionado bullet em preparar"`)
11. Append em `edits[]` no frontmatter: `{at: <now ISO-8601>, summary: <string>}`
12. Reescrever o .md com `edits` atualizado (unica escrita do `/sync`)
13. Reportar: `"Artifact atualizado. N ediçoes registradas: <lista>"`

## Nunca fazer

- Chamar o agente `pfeffer-power-analyst` — o insight vive no .md, nao e regenerado
- Chamar MCPs de extraçao (ClickUp, Google Calendar) — dados canonicos vivem no .md
- Sobrescrever qualquer campo do .md que nao seja `edits[]` — o `/sync` so le e anexa historico
- **Re-carimbar `generated_at` com a hora do sync** — esse campo registra quando o plano foi concebido, nao quando foi re-renderizado. Edicoes vao em `edits[]`; o meta-footer do HTML sempre mostra o `generated_at` original
- **Emitir HTML sem meta-footer** ou com menos de 5 spans — a v2.1.0 exige os 5 metadados fixos (schema/fonte/gerado/skill/insight). Campo ausente vira `—`, nunca omitir `<span>`
- **Regenerar linhas vazias na agenda** (placeholders `—` em faixa horaria fixa) — a v2.1.0 emite so eventos reais. Se o render antigo for reaproveitado, a agenda regride
- **Adicionar `@media` queries no CSS inline** — o layout e viewport-adaptive via `clamp()` + `vh` (ver [tokens.css](../skills/generating-daily-planner/references/tokens.css))
- Criar artifact novo quando ele nao existe — reportar erro e orientar rodar a skill
- Popular `mcp_tools` no `update_artifact` — artifact da v2 e estatico, nao chama MCPs em runtime
- Rodar `/sync` quando o .md nao foi editado manualmente — sem diff para registrar, e redundante com a skill completa

## Tempo esperado

<5s em uso tipico. Sem chamadas de MCP alem do `update_artifact` final, sem subagents, sem extraçao.
