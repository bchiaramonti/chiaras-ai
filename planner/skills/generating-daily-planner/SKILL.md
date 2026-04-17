---
name: generating-daily-planner
description: Gera o daily planner pessoal executivo de Bruno em HTML seguindo tres fases. Fase 1 (Extrair) le dados reais via MCPs (Google Calendar, ClickUp) ou pergunta ao usuario quando indisponivel; corpo/saude e sempre perguntado. Fase 2 (Planejar) aplica boas praticas — Most Important Tasks, Eat-the-frog, time blocking 60/40, pre-mortem, Eisenhower, role balance, planejamento noturno — e gera o Insight cruzando frameworks de brain/3-resources (PARA). Fase 3 (Renderizar) aplica o design system Planner Editorial Noturno (Georgia + Inter, terracota + azul petroleo, header 5-zone + body 3-col + footer 2-col, zero ornamento). Use quando Bruno pedir para criar, editar ou gerar seu planner diario, daily dashboard, pagina de planejamento ou HTML de cron pessoal. Nao usar em apresentacoes M7, comunicados corporativos ou outputs para terceiros.
license: Proprietary
---

# Generating Daily Planner

Gera o daily planner pessoal executivo em HTML aplicando **tres fases**: extrair dados reais, planejar usando metodologia, renderizar no design system Planner Editorial Noturno.

**Principio central:** o planner so serve se o plano for executavel. Design impecavel com conteudo fraco produz artefato bonito e inutil. Metodologia primeiro, estilo depois.

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

## Workflow em tres passadas

### Fase 1 · Extrair (dados reais antes de pensar)

Ler [references/extracao-dados.md](references/extracao-dados.md) e reunir dados das 5 fontes:

| Fonte | Rota primaria | Fallback |
|---|---|---|
| Agenda | Google Calendar MCP + Outlook (manual) | Pedir print/lista |
| Tarefas | ClickUp MCP (assignee=Bruno) | Pedir lista "Hoje" |
| Delegadas | ClickUp MCP (criadas por Bruno, assignee != Bruno) | Pedir resumo |
| Corpo | *Sem MCP* (Garmin removido em v1.3.0) | Sempre perguntar |
| Contexto insight | Filesystem `brain/3-resources/` (PARA) | — |

**Regra de ouro:** nunca inventar dado. Se nao conseguir extrair nem obter do usuario, secao vira `—` ou e omitida.

### Fase 2 · Planejar (metodologia antes de texto)

Ler [references/metodologia-planejamento.md](references/metodologia-planejamento.md) e aplicar as 6 regras de decisao:

1. **Lide do dia** — tese argumentativa unica (nao lista descritiva), 200-400 chars
2. **Tres inadiaveis** — Eisenhower Q2 > Eat-the-frog > balance de papeis (>=2 dimensoes), com pre-mortem de 1 linha cada
3. **Agenda** — capacidade 60/40, bloco >=90min para MIT #1 em 9h-12h (pico cognitivo), almoco obrigatorio
4. **Tarefas ClickUp** — 5-6 visiveis ordenadas ABCDE, "+N" para resto
5. **Delegadas** — agrupadas por projeto, atrasadas no topo, max 4-5 grupos
6. **Amanha** — Ancora (1 frase imperativa) + 0-2 bullets de Preparar hoje (<=15min cada)

Em paralelo, gerar o **Insight · cruzamento** seguindo [references/insight-cruzamento.md](references/insight-cruzamento.md): 2-3 desafios do dia → dominios → scan de `brain/3-resources/` → cruzamento binario de frameworks com tensao explicita.

Antes de avancar para Fase 3, validar o **checklist de sanidade** (final de metodologia-planejamento.md).

### Fase 3 · Renderizar (design system aplicado)

Com o plano validado:

1. Ler [references/tokens.css](references/tokens.css) e colar no `<style>` do output
2. Ler [references/principios.md](references/principios.md) antes de decisoes visuais
3. Ler [references/componentes.md](references/componentes.md) para replicar cada componente
4. Ler [references/regras-texto.md](references/regras-texto.md) para manter o tom
5. Usar [references/template-html.html](references/template-html.html) como starter e preencher com o plano

## Checklist pre-render

Antes de emitir o HTML final, confirmar:

```
[ ] Dados extraidos reais ou explicitamente perguntados ao usuario (nenhum inventado)
[ ] Lide tem UMA tese argumentativa com 2-4 entidades em <em>
[ ] 3 MITs cobrem >=2 dimensoes (trabalho/corpo/familia)
[ ] MIT #1 e Eat-the-frog (pior/maior/mais adiado)
[ ] Cada MIT tem inadiaveis__risco de 1 linha (causa → plano B)
[ ] Agenda <=60% ocupada em 9h-18h, almoco presente
[ ] MIT #1 tem bloco >=90min reservado em 9h-12h
[ ] Tarefas ClickUp ordenadas ABCDE, cortadas em 5-6 + "+N"
[ ] Tarefas__title-meta mostra `· <lista> · <tag>` (regra da componentes.md s9)
[ ] Delegadas agrupadas por projeto
[ ] Insight cruza DUAS (nao 3+) perguntas de frameworks distintos
[ ] Ancora de Amanha cabe em 1 frase imperativa
[ ] Preparar hoje tem 0-2 bullets, cada <=15min hoje
```

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
| Estrutura | Header 5-zone + Body 3-col + Footer 2-col |
| Filosofia | Zero ornamento, hierarquia via tipografia |

## Principios fundadores (leia antes de qualquer output)

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
- **Inventar dados** quando a extracao falha (perguntar ao usuario ou omitir)
- **Pre-mortem ficticio** ("risco: tudo pode dar errado") — escrever `risco: —` se nao ha risco real

## Arquivos da skill

```
generating-daily-planner/
├── SKILL.md                       # este arquivo (orquestracao 3 fases)
├── README.md                      # instrucoes de instalacao e uso
└── references/
    ├── extracao-dados.md          # Fase 1 · fontes, MCPs, fallbacks, schema
    ├── metodologia-planejamento.md # Fase 2 · 6 regras + checklist de sanidade
    ├── insight-cruzamento.md      # Fase 2b · gerar insight criativo de 3-resources
    ├── tokens.css                 # Fase 3 · CSS variables + classes
    ├── tokens.json                # Fase 3 · DTCG format tokens (interop)
    ├── principios.md              # Fase 3 · 6 principios fundadores
    ├── componentes.md             # Fase 3 · 12 componentes especificados
    ├── regras-texto.md            # Fase 3 · tom editorial, labels, metadata
    └── template-html.html         # Fase 3 · starter HTML completo
```

## Output esperado

Ao aplicar esta skill, o Claude Code deve produzir um artefato que:

- Foi **planejado** usando as 6 regras de metodologia-planejamento.md (nao so preenchido)
- Foi **extraido** de fontes reais (ou perguntas explicitas ao usuario), sem ficcao
- Usa apenas as cores definidas em tokens.css
- Usa apenas Georgia (serif) e Inter (sans)
- Segue a estrutura header 5-zone + body 3-col + footer 2-col
- Implementa os 12 componentes centrais + a estrutura Ancora+Preparar em Amanha (v1.4.0)
- Implementa pre-mortem por MIT (v1.4.0)
- Respeita o tom editorial (ver regras-texto.md)
- Contem um Insight cruzando dois frameworks tensionados (nao generico)

Se o usuario pedir algo que contradiga os principios (ex: "adiciona uns icones legais" ou "faz um modo claro"), a skill deve respeitar o style guide e sinalizar o conflito antes de implementar. Se o usuario pedir "pule o planejamento, so monta o HTML rapido", a skill deve avisar que o output sera raso e pedir confirmacao antes de pular as Fases 1 e 2.
