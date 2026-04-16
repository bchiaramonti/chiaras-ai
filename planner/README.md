# planner

> Personal plugin — gera planners pessoais executivos usando o sistema de design Editorial Noturno (dark mode, Georgia serif + Inter sans, terracota + azul petroleo).

## O que este plugin faz

Quando o Bruno pede um planner diario, daily dashboard, pagina de planejamento do dia ou HTML de cron matinal, o Claude Code invoca automaticamente a skill `generating-daily-planner` e aplica o sistema de design Editorial Noturno afunilado em 20 rodadas de decisao.

**Escopo estrito:** apenas artefatos pessoais. NAO usar em apresentacoes M7, comunicados para diretoria, documentos corporativos ou interfaces de produto.

## O que entrega

- Dark mode quente nativo (sem light mode)
- Tipografia como hierarquia (Georgia serif + Inter sans, sem caixas decorativas)
- Paleta de 9 cores com significado semantico (terracota = foco, azul petroleo = corpo, etc.)
- Grid de 3 colunas com gap 32px
- Zero ornamento (sem icones decorativos, sombras, gradientes, pills, badges)

## Componentes

| Item | Conteudo |
|---|---|
| Skill | `generating-daily-planner` (auto-invocada por trigger de contexto pessoal) |
| References | `tokens.css`, `tokens.json`, `principios.md`, `componentes.md`, `regras-texto.md`, `template-html.html` |
| Agents | — |
| Commands | — |

## Instalacao

Via marketplace `bchiaramonti-plugins`:

```
/plugin install planner@bchiaramonti-plugins
```

## Triggers

A skill e invocada quando o pedido contem qualquer um destes sinais:

- "meu planner", "meu daily", "minha pagina de planejamento"
- "dashboard pessoal", "relatorio do dia", "journal"
- "agenda diaria", "visao executiva do meu dia/semana"
- HTML gerado por cron matinal pessoal

## Nunca fazer

- Light mode
- Cartoes elevados ou bordas decorativas
- Icones (emoji ou SVG)
- Sombras, gradientes, blur
- UPPERCASE exceto em labels de dias da semana
- Formatos de data misturados — sempre "16 abril"

## Autor

Bruno Chiaramonti
