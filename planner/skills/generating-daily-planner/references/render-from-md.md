# Render from .md · pipeline

Consumido pela Fase 4 da skill e pelo comando `/planner sync`. Converte `.md` canonico em HTML publicado via `mcp__cowork__update_artifact` no live artifact `daily-planner-live`.

Pre-requisito: o `.md` passou na validacao de [schema-md.md](schema-md.md).

## 1. Parse

### 1.1 Frontmatter vs body

```
1. Ler arquivo inteiro como string UTF-8
2. Dividir em ["", frontmatter, body] pela regex /^---\n([\s\S]+?)\n---\n([\s\S]*)$/
3. Parsear frontmatter com YAML loader (tipos fortes, nao string-only)
4. Manter body como string ate §1.2
```

### 1.2 Body em blocos semanticos

Separar o body por H1 (`^# `) em ate 3 blocos:

- `# Lide do dia` → string (prosa, pode conter multiplas linhas; preservar quebras)
- `# Insight · cruzamento` → `{ cite: string, body: string }`
  - `cite` = primeira linha nao-vazia apos o H1; deve comecar com `> `
  - `body` = linhas restantes ate proximo H1 ou EOF
- `# Notas do dia` → array de bullets (linhas que comecam com `- `), opcional

H1s em outra ordem sao aceitos, mas todos os 3 sao extraidos pelo nome, nao por posicao.

## 2. Mapeamento frontmatter → componentes HTML

Ver [componentes.md](componentes.md) para specs completos. Tabela resumo:

| Campo frontmatter | Componente | Seletor CSS |
|---|---|---|
| `date`, `weekday`, `day_of_year`, `iso_week`, `month_name` | Header zona 1 (Dia) | `.header__dia` |
| body `# Lide do dia` | Header zona 2 (Lide) | `.header__lide` |
| body `# Insight · cruzamento` | Header zona 3 (Insight) | `.header__insight` + `.header__insight-cite` |
| `iso_week` + mini-calendario derivado da `date` | Header zona 4 (Mes) | `.header__mes` |
| `corpo.*` + `corpo.*_ref` + `metrics.*` | Header zona 5 (Corpo) | `.header__corpo` + `.header__corpo-ref` (ver §2.1) |
| `agenda[]` | Body coluna 1 | `.agenda-enum` (ver §2.2 — so linhas com evento real) |
| `mits[]` | Body coluna 2 topo | `.inadiaveis` + `.inadiaveis__risco` |
| `tasks[]` | Body coluna 2 baixo | `.tasks` |
| `workspace[]` | Body coluna 3 | `.workspace` + `.workspace__task--self` quando `is_mine: true` |
| body `# Notas do dia` | Footer coluna 1 | `.footer__notas` |
| `amanha.ancora` + `amanha.preparar[]` | Footer coluna 2 | `.footer__amanha` |
| `schema` + `generated_at` + `generated_by` + `pfeffer.chapters` + path do .md | Meta-footer | `.meta-footer` (ver §2.3) |

Campos ausentes ou com fallback null → seguir regras de §4 de [schema-md.md](schema-md.md).

### 2.1 Formatter de `corpo.*_ref` (v2.1.0)

Cada KPI da zona Corpo renderiza uma data de referencia discreta (`.header__corpo-ref`). A regra de conversao depende do campo:

| Campo | Entrada esperada | Conversao → rotulo exibido |
|---|---|---|
| `corpo.peso_ref` | ISO `YYYY-MM-DD` | `format_rel_or_abs(date, today)` |
| `corpo.sono_ref` | ISO `YYYY-MM-DD` | `format_rel_or_abs(date, today)` |
| `corpo.tss_ref` | literal `"seg->hoje"` | `"seg→hoje"` (substitui ASCII `->` por `→`) |
| `corpo.tsb_ref` | literal `"hoje"` | `"hoje"` (passa direto) |

```python
def format_rel_or_abs(date_iso: str, today_iso: str) -> str:
    # Converte ISO -> rotulo curto, preferindo relativo quando <=7d
    d = parse_iso(date_iso)
    t = parse_iso(today_iso)
    delta = (t - d).days
    if delta == 0:  return "hoje"
    if delta == 1:  return "ontem"
    if 2 <= delta <= 7:  return f"há {delta}d"
    # >=8d OU futuro: formato absoluto "DD mes" em portugues lowercase
    return f"{d.day} {MES_ABREV[d.month]}"   # ex: "14 abr"
```

Onde `MES_ABREV = {1: "jan", 2: "fev", ..., 12: "dez"}`.

**Casos especiais:**

- Valor do KPI null (`corpo.peso` null) → **nao renderiza** `<div class="header__corpo-ref">`, independente de `*_ref` estar preenchido ou null.
- Valor presente mas `*_ref` null (edge case) → renderizar `<div class="header__corpo-ref">—</div>`.
- `format_rel_or_abs` com delta negativo (data no futuro) → tratar como absoluto. Em tese nunca ocorre, mas nao abortar.

### 2.2 Agenda · so eventos reais (v2.1.0)

A partir da v2.1.0, o template viewport-lock (100vh sem overflow) nao aceita linhas placeholder. Regra de render:

1. Iterar `agenda[]` ordenando por `start` ascendente.
2. Emitir **uma `.agenda-enum__row` por item** — nenhum item, nenhuma row.
3. Nao sintetizar horas cheias ausentes (ex: se ha `09:00` e proximo e `11:00`, nao inserir row `10:00` com `—`).
4. Adicionar modifier `.agenda-enum__row--gap` em um item cujo `start` esta **>=2h** apos o `end` (ou `start`) do item anterior — cria respiro visual sem inventar row vazia.
5. O item com `is_now: true` ganha `.agenda-enum__hour--now` + `.agenda-enum__event--now`.
6. **Classes `--empty` estao deprecadas** — nao emitir mais. Permanecem no CSS apenas para retro-compatibilidade de HTML antigo cacheado.

```python
def render_agenda(items):
    items = sorted(items, key=lambda e: e["start"])
    rows = []
    prev_end = None
    for it in items:
        gap = prev_end and hours_between(prev_end, it["start"]) >= 2
        row_class = "agenda-enum__row" + (" agenda-enum__row--gap" if gap else "")
        # ... emit hour + event cells
        prev_end = it.get("end") or it["start"]
    return rows
```

### 2.3 Meta-footer · rastreabilidade (v2.1.0)

Apos o `</footer>`, emitir `.meta-footer` com 5 `<span>`s na ordem fixa:

```python
def render_meta_footer(data, md_path_absolute):
    rel = md_path_absolute.replace(os.path.expanduser("~/Documents/brain/"), "")
    chapters = data["pfeffer"]["chapters"]
    return f'''
    <div class="meta-footer">
      <span>schema: {data["schema"]}</span>
      <span>fonte: {rel}</span>
      <span>gerado: {data["generated_at"]}</span>
      <span>skill: {data["generated_by"]}</span>
      <span>insight: Pfeffer Cap {chapters[0]}x{chapters[1]}</span>
    </div>
    '''
```

**Regras:**

- Sempre 5 spans. Campo ausente vira `—` (nao omitir `<span>`).
- `fonte` sempre relativo a `~/Documents/brain/` (abs path vaza info de filesystem).
- `insight` usa `x` ASCII (nao `×` nem `↔`). Convencao diferente do body `# Insight · cruzamento` propositalmente — aqui e metadata, la e editorial.
- Nao HTML-escape `generated_at` (ja e ISO seguro).

## 3. Renderizaçao de inlines Markdown

Aplicar **apenas no texto de saida** (depois do HTML escape de caracteres `<`/`>`/`&`), para evitar double-render.

```
ordem:
  1. escape_html_entities(texto)            # < → &lt; etc
  2. replace /\*\*(.+?)\*\*/g → '<em class="strong">$1</em>'
  3. replace /\*(.+?)\*/g     → '<em>$1</em>'
  4. replace /\[(.+?)\]\((.+?)\)/g → '<a href="$2" target="_blank" rel="noopener">$1</a>'
```

Regra de limite: links **so sao resolvidos dentro de `tasks[].title` e `workspace[].tasks[].title`** quando o respectivo `url` esta preenchido — o render deve converter `tasks[i].title` em link se `tasks[i].url` nao vazio, nao confiar em `[texto](url)` literal no title.

Sequencia importa: `**` antes de `*` porque `*` e greedy e captura `**`.

Proibido aceitar outras convencoes:
- `__negrito__` ou `_italico_` com underscore → **nao renderizar** (manter literal).
- HTML inline (`<em>`, `<strong>`) no .md → **nao renderizar**, escape como texto.

## 4. Publicaçao no live artifact

```
mcp__cowork__update_artifact({
  id: "daily-planner-live",
  html: "<!DOCTYPE html>\n<html>...",
  mcp_tools: [],
  update_summary: "Daily 2026-04-22 · 3 MITs · insight Cap 11↔13 · 4 eventos"
})
```

### 4.1 Campo `mcp_tools` sempre vazio na v2

O artifact **nao** chama MCPs em runtime. Todos os dados vem pre-renderizados do .md. Se `mcp_tools` tiver algo, esta errado — reverter.

### 4.2 Se o artifact nao existe (primeiro run)

`update_artifact` retorna erro "artifact nao encontrado". Nesse caso:

```
mcp__cowork__create_artifact({
  id: "daily-planner-live",
  title: "Daily Planner · Bruno",
  html: <mesmo html>,
  mcp_tools: [],
  description: "Live artifact do daily planner. Fonte canonica em ~/Documents/brain/0-inbox/plan-review/daily/."
})
```

`/planner sync` nao cria artifact — reporta erro e orienta rodar `generating-daily-planner` primeiro.

### 4.3 `update_summary` — convençao

Formato: `"Daily YYYY-MM-DD · <contagens principais>"`. Exemplos validos:

- `"Daily 2026-04-22 · 3 MITs · insight Cap 11↔13 · 4 eventos"` (run inicial)
- `"Daily 2026-04-22 · sync manual · MIT ii concluida"` (apos `/planner sync`)
- `"Daily 2026-04-22 · sync manual · 2 ediçoes"` (quando ha multiplas mudancas)

## 5. Erros comuns

| Sintoma | Causa | Correçao |
|---|---|---|
| Asteriscos literais aparecem no HTML | Esqueceu de resolver inlines antes de injetar | Rodar §3 antes de concatenar no template |
| Tags `<em>` escapadas no output | Ordem de escape errada | Escapar HTML primeiro, depois resolver MD |
| Links quebrados (aparecem como texto `[x](url)`) | Regex greedy aplicando so em texto sem url | Verificar que `tasks[].url` foi passado ao renderer |
| Data do mini-calendario nao marca o dia correto | Usou `day_of_year` sem subtrair 1 | Indexar 1-based conforme `date` |
| Insight com `<->` ao inves de `↔` | Copiou ASCII no .md | Pre-validacao em [schema-md.md §5.2](schema-md.md) deveria ter abortado; corrigir no .md |
| HTML truncado (CSS faltando) | Esqueceu de colar `tokens.css` inline no `<style>` | Usar o starter em [template-html.html](template-html.html) |
| `mcp_tools` nao vazio | Reaproveitou template v1.x com `callMcpTool` | Remover toda logica de fetch; dados vem do .md |
| `.header__corpo-ref` mostra "NaN" ou data do clock | Formatter recebeu string ao inves de ISO | `corpo.peso_ref`/`sono_ref` precisa ser ISO `YYYY-MM-DD`; ver §2.1 |
| `TSS sem` renderiza `"seg->hoje"` com `->` literal | Esqueceu de substituir ASCII arrow | Aplicar `.replace("->", "→")` no formatter (ou ler §2.1) |

## 6. Pipeline resumido

```
md_path = resolve("~/Documents/brain/0-inbox/plan-review/daily/YYYY/MM/daily-YYYY-MM-DD.md")
raw = read(md_path)
frontmatter, body = split_frontmatter(raw)
data = yaml_parse(frontmatter)
validate(data)  # ver schema-md.md §8
blocks = parse_body_h1(body)  # { lide, insight: {cite, body}, notas: [] }
html = render_template(data, blocks, md_path=md_path)  # tokens.css + componentes.md + §3 inlines + §2.3 meta-footer
cowork.update_artifact(id="daily-planner-live", html=html, mcp_tools=[], update_summary=summary)
```

## 7. Re-render via /planner sync — diff e edits[]

Quando invocado por `/planner sync`, apos publicar o HTML o comando deve:

1. Comparar o `.md` atual com snapshot anterior (ultima versao carregada em memoria, ou re-derivar do `generated_at`/ultimo `edits[].at`).
2. Gerar 1-3 summaries descrevendo mudanças principais (ex: `"MIT ii concluida"`, `"Adicionado bullet em preparar"`, `"Insight reescrito"`).
3. Append em `edits[]` no frontmatter conforme [schema-md.md §7](schema-md.md).
4. Re-escrever o `.md` com `edits` atualizado (apenas `/sync` toca esse campo).

A ordem e importante: renderizar+publicar primeiro (UX rapida), depois atualizar `edits[]` (nao bloqueia o artifact).
