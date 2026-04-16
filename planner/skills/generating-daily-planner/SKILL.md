---
name: generating-daily-planner
description: Gera o daily planner pessoal executivo de Bruno Chiaramonti em HTML dark-mode editorial. Use esta skill quando Bruno pedir para criar, editar ou gerar seu planner diario, daily dashboard, pagina de planejamento do dia, ou HTML de cron matinal pessoal. A skill aplica o sistema de design Planner Editorial Noturno (Georgia serif + Inter sans, paleta terracota + azul petroleo, header 5-zone + body 3-col + footer 2-col, zero ornamento) e preenche o template com dados reais do dia (Lide, Insight, Corpo KPIs, Agenda, Tres inadiaveis, Tarefas ClickUp, Delegadas, Notas, Amanha). Triggers incluem "cria meu planner de hoje", "gera o HTML do dia", "atualiza minha pagina de planejamento", "monta um daily dashboard", "quero uma visao executiva do meu dia". Nao usar em apresentacoes M7, comunicados corporativos, documentos para diretoria ou outputs para terceiros.
license: Proprietary
---

# Generating Daily Planner

Gera o daily planner pessoal executivo em HTML aplicando o sistema de design Planner Editorial Noturno. Sistema construido por afunilamento iterativo em 20 rodadas de decisao.

## Quando usar esta skill

Invocada quando Bruno pede para gerar ou atualizar o planner do dia — nao para apresentacoes corporativas nem comunicacao com terceiros.

**Triggers tipicos:**
- "Crie meu planner de hoje"
- "Gera o HTML do dia"
- "Atualiza minha pagina de planejamento"
- "Monta um daily dashboard"
- "Quero uma visao executiva do meu dia"

**NAO usar esta skill para:**
- Apresentacoes M7 para diretoria ou XP
- Documentos corporativos
- Comunicados formais
- Outputs que terceiros vao consumir
- Interfaces de produtos SaaS

## Quick reference

| Aspecto | Decisao |
|---|---|
| Modo | Dark mode quente nativo (nao ha light mode) |
| Fonte principal | Georgia serif (texto, labels, narrativa) |
| Fonte tabular | Inter sans (horas, numeros em grid) |
| Cor primaria | Terracota #D97757 (trabalho, foco) |
| Cor secundaria | Azul petroleo #6B9EB0 (corpo, treino) |
| Cor alerta | Terracota escuro #B8593C (atraso) |
| Fundo | #1A1715 (escuro quente) |
| Estrutura da pagina | Header 5-zone + Body 3 cols + Footer 2 cols |
| Header | Dia (220) \| Lide (flex) \| Insight (240) \| Mes (150) \| Corpo (130) |
| Body | Agenda \| Tres inadiaveis + Tarefas ClickUp \| Delegadas (3 cols iguais) |
| Footer | Notas do dia (flex) \| Amanha (500px) |
| Gaps | Header 24 · Body 32 · Footer 32 · Page 20 |
| Filosofia | Zero ornamento, hierarquia via tipografia |

## Workflow ao aplicar esta skill

1. Leia o arquivo `references/tokens.css` e cole no `<style>` do output
2. Leia o arquivo `references/principios.md` antes de tomar decisoes visuais
3. Leia o arquivo `references/componentes.md` para replicar componentes centrais
4. Leia o arquivo `references/regras-texto.md` para manter o tom correto
5. Consulte `references/template-html.html` como starter e preencha com os dados reais do dia

## Princípios fundadores (leia antes de qualquer output)

1. **Tipografia antes de caixa** — hierarquia por tamanho/peso/italico/cor, nunca por bordas ou cartoes.
2. **Densidade operacional, respiracao editorial** — dados acionaveis densos, narrativa respirada.
3. **Cor e decisao, nao decoracao** — toda cor significa algo (ver tabela de estados).
4. **Dark mode quente nativo** — nunca implementar light mode.
5. **Numero como escultura** — numeros sao protagonistas visuais, nao metadata.
6. **Zero ornamento** — sem icones decorativos, sombras, gradientes, badges ou pills.

## Nunca fazer

- Light mode
- Cartoes elevados ou bordas em torno de secoes
- Icones decorativos (emoji ou SVG) — so texto e italico para enfase
- Sombras, gradientes, blur
- UPPERCASE exceto em labels de dias da semana
- Formatos de data misturados — sempre "16 abril", nunca "16/04" nem "April 16"
- Introduzir cor nova sem redefinir o sistema
- Serif para dados tabulares, sans para texto narrativo

## Arquivos da skill

```
generating-daily-planner/
├── SKILL.md                       # este arquivo
├── README.md                      # instrucoes de instalacao e uso
└── references/
    ├── tokens.css                 # CSS variables prontas para colar
    ├── tokens.json                # Design tokens em formato DTCG
    ├── principios.md              # 6 principios fundadores em detalhe
    ├── componentes.md             # especificacao de cada componente
    ├── regras-texto.md            # tom, labels, metadata de tempo
    └── template-html.html         # starter HTML completo
```

## Output esperado

Ao aplicar esta skill, o Claude Code deve produzir um artefato que:

- Usa apenas as cores definidas em tokens.css
- Usa apenas Georgia (serif) e Inter (sans)
- Segue a estrutura header 5-zone + body 3-col + footer 2-col
- Implementa os 12 componentes centrais conforme spec
- Respeita o tom editorial do texto (ver regras-texto.md)
- Nao introduz elementos visuais fora do sistema

Se o usuario pedir algo que contradiga os principios (ex: "adiciona uns icones legais" ou "faz um modo claro"), o Claude Code deve respeitar a skill e sinalizar o conflito antes de implementar.
