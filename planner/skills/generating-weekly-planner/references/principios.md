# Principios fundadores

Os seis principios abaixo guiam toda decisao de design. Quando houver duvida entre duas opcoes, reveja-os.

## i. Tipografia antes de caixa

Hierarquia e diferenciacao acontecem por tamanho, peso, italico e cor, nunca por bordas, cartoes ou fundos coloridos. Um numero em `--fs-display` (56px, a data) ja e hierarquia. Um italico em terracota ja e destaque.

**Implicacoes praticas:**
- Nao use `border`, `box-shadow` ou `background-color` para delimitar secoes
- Use `font-size`, `font-weight`, `font-style` e `color` como unica ferramenta de hierarquia
- A unica excecao e o bloco do dia atual no calendario (background `#2A2320`)

## ii. Densidade operacional, respiracao editorial

Onde ha dado acionavel (tarefas, agenda, metricas), a informacao vem densa, colada, direta. Onde ha narrativa (lide do dia, contexto, notas), o texto respira.

**Regra pratica:**
- Listas operacionais: `line-height: 1.45` (compact)
- Texto narrativo: `line-height: 1.6` (normal)
- Agenda timeline: `line-height: 1.9` (loose)

## iii. Cor e decisao, nao decoracao

Terracota `#D97757` marca foco pessoal e trabalho. Azul petroleo `#6B9EB0` marca corpo e treino. Terracota escuro `#B8593C` marca atraso e alerta. Nenhuma cor aparece por estetica — toda cor significa algo.

**Mapa de significados:**
| Cor | Hex | Significa |
|-----|-----|-----------|
| Terracota | `#D97757` | Trabalho, foco, pessoal, entidade destacada, proximo compromisso, dia atual |
| Azul petroleo | `#6B9EB0` | Corpo, treino, saude, metricas de triathlon |
| Terracota escuro | `#B8593C` | Atraso, alerta, prazo critico |

Se um dado nao cabe em um desses tres significados, ele fica em `#F5F0E6` (primario) ou `#8A8178` (secundario).

## iv. Dark mode quente nativo

O fundo `#1A1715` nao e neutro. E quente, terroso, proximo do couro. Funciona em madrugadas longas de trabalho e em sessoes noturnas de planejamento. **Nao existe versao light mode deste sistema.** Se o usuario pedir light mode, sinalize o conflito.

**Test visual rapido:** se o fundo parece "preto neutro" ou "cinza azulado", esta errado. Deve parecer "couro escuro".

## v. Numero como escultura

Numeros nao sao metadata — sao protagonistas. A data do dia em 64px, os romanos (i, ii, iii) em 28-40px em italico, as horas em Inter sans tabular. Os numeros carregam o sistema.

**Implicacao:**
- Data do dia: `font-size: 64px; font-weight: 300; letter-spacing: -0.04em`
- Romanos: `font-size: 40px; font-style: italic; opacity: 0.5`
- Horas: `font-family: Inter; font-variant-numeric: tabular-nums`

## vi. Zero ornamento

Sem icones decorativos. Sem sombras. Sem gradientes. Sem badges pill-shaped. Sem bordas arredondadas generosas. A unica forma nao-textual permitida e a linha divisoria horizontal em `#2E2823`.

**Checklist de rejeicao:**
- `box-shadow` → rejeitar
- `linear-gradient` ou `radial-gradient` → rejeitar
- `border-radius > 6px` → rejeitar (exceto no dia atual do calendario)
- Emoji ou icone SVG decorativo → rejeitar
- Badge com fundo colorido → rejeitar (use texto em italico colorido no lugar)
