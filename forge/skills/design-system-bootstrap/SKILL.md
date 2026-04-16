---
name: design-system-bootstrap
description: >-
  Defines the initial design system: color palette, typography, spacing, borders,
  shadows, and base component catalog with design tokens in JSON. Use after
  wireframes are specified. Produces 02-design/design-system.md and
  02-design/design-tokens.json.
user-invocable: false
---

# Design System Bootstrap

Define sistema de design inicial com tokens programáticos e catálogo de componentes base. Analisa wireframes para identificar necessidades visuais, estabelece paleta de cores com contraste WCAG AA, escala tipográfica, espaçamentos consistentes e componentes reutilizáveis com variantes e estados.

## Pré-requisitos

- `02-design/wireframes/` com pelo menos 1 wireframe com status `draft` ou `approved`

## Processo

1. **Ler wireframes para inventariar componentes:**
   - `02-design/wireframes/*.md` — identificar: componentes usados, padrões visuais, hierarquia de informação
   - `02-design/user-flows.md` — extrair: contextos de uso (quais telas usam quais componentes)
   - `01-product/prd.md` — extrair: tom/personalidade do produto, público-alvo (influencia escolhas visuais)

2. **Definir tokens de cor:**
   - **Primary** — cor principal da marca/ações primárias
   - **Secondary** — cor de apoio/ações secundárias
   - **Accent** — destaque pontual (badges, highlights)
   - **Neutral** — escala de cinzas para texto, bordas, backgrounds (50-900)
   - **Success** — confirmações, estados positivos
   - **Warning** — alertas, atenção necessária
   - **Error** — erros, ações destrutivas
   - Para cada cor: definir variantes (light, default, dark) com valores hex
   - Verificar contraste WCAG AA: texto sobre background >= 4.5:1, elementos grandes >= 3:1

3. **Definir tipografia:**
   - Font family: primária (headings + body) e monospace (code)
   - Escala tipográfica: h1, h2, h3, h4, h5, h6, body, small, caption
   - Para cada nível: font-size (rem), line-height, font-weight
   - Base size: 1rem = 16px

4. **Definir espaçamentos:**
   - Escala baseada em 4px: `4, 8, 12, 16, 24, 32, 48, 64`
   - Nomes semânticos: `xs` (4), `sm` (8), `sm-md` (12), `md` (16), `lg` (24), `xl` (32), `2xl` (48), `3xl` (64)
   - Gap padrão entre elementos: `md` (16px)
   - Padding de containers: `lg` (24px)

5. **Definir bordas e sombras:**
   - Border radius: `sm` (4px), `md` (8px), `lg` (12px), `full` (9999px)
   - Border widths: `thin` (1px), `medium` (2px)
   - Sombras: `sm` (sutil, cards), `md` (elevação, dropdowns), `lg` (modais, overlays)

6. **Catalogar componentes base:**
   - **Button** — variantes: primary, secondary, ghost; tamanhos: sm, md, lg
   - **Input** — tipos: text, select, textarea, checkbox, radio
   - **Card** — com/sem header, com/sem footer, com/sem imagem
   - **Modal** — com título, corpo, ações (confirm/cancel)
   - **Table** — com header, rows, paginação, estados (empty, loading)
   - **Badge** — variantes: info, success, warning, error; tamanhos: sm, md
   - **Alert** — variantes: info, success, warning, error; com/sem ação
   - Para cada componente: documentar estados (default, hover, active, disabled, focus)

7. **Gerar artefatos:**
   - Design tokens via `templates/design-tokens.tmpl.json` → salvar em `02-design/design-tokens.json`
   - Documentação via `templates/design-system.tmpl.md` → salvar em `02-design/design-system.md`
   - Os dois artefatos devem ser consistentes: todo token no JSON deve estar documentado no Markdown e vice-versa

8. **Atualizar `.status`:**
   - Artifact `design-system` → `draft`
   - Artifact `design-tokens` → `draft`

## Artefatos Gerados

- `02-design/design-system.md` (via `templates/design-system.tmpl.md`)
- `02-design/design-tokens.json` (via `templates/design-tokens.tmpl.json`)

## Validação

Antes de marcar como `draft`, verificar:

- [ ] Tokens seguem formato W3C Design Tokens (`$value`, `$type`, `$description`)
- [ ] Paleta de cores com contraste WCAG AA verificado (texto >= 4.5:1, elementos grandes >= 3:1)
- [ ] Escala tipográfica completa (h1 até caption) com font-size, line-height e weight
- [ ] Espaçamentos seguem escala de 4px sem valores fora da escala
- [ ] Todos os componentes dos wireframes estão cobertos no catálogo
- [ ] Cada componente tem pelo menos: variantes, tamanhos e estados (default, hover, disabled)
- [ ] JSON é válido e parseável (sem trailing commas, sem comentários)
- [ ] Documentação Markdown e JSON são consistentes (mesmos valores, mesmos nomes de token)
- [ ] Nenhum valor hardcoded nos componentes — todos referenciam tokens
- [ ] Border radius, sombras e border widths definidos na escala
