# Design System — <PROJECT_NAME>

> **Fase:** Design
> **Skill:** design-system-bootstrap
> **Status:** draft
> **Data:** <YYYY-MM-DD>

---

## 1. Paleta de Cores

<!-- Definir cores do produto. Verificar contraste WCAG AA: texto >= 4.5:1, elementos grandes >= 3:1. -->

### Primary

<!-- Cor principal da marca e ações primárias. -->

| Variante | Hex | Uso |
|----------|-----|-----|
| Light | `<HEX>` | Backgrounds, hover states |
| Default | `<HEX>` | Botões primários, links, ações principais |
| Dark | `<HEX>` | Texto sobre fundo claro, hover de ações |

### Secondary

<!-- Cor de apoio para ações secundárias. -->

| Variante | Hex | Uso |
|----------|-----|-----|
| Light | `<HEX>` | Backgrounds secundários |
| Default | `<HEX>` | Botões secundários, elementos de apoio |
| Dark | `<HEX>` | Texto secundário, hover |

### Accent

<!-- Destaque pontual: badges, highlights, elementos que precisam chamar atenção. -->

| Variante | Hex | Uso |
|----------|-----|-----|
| Light | `<HEX>` | Background de destaque |
| Default | `<HEX>` | Badges, highlights, notificações |
| Dark | `<HEX>` | Texto de destaque |

### Neutral

<!-- Escala de cinzas para texto, bordas, backgrounds. -->

| Token | Hex | Uso |
|-------|-----|-----|
| 50 | `<HEX>` | Background da página |
| 100 | `<HEX>` | Background de cards |
| 200 | `<HEX>` | Bordas sutis, dividers |
| 300 | `<HEX>` | Bordas padrão, inputs desabilitados |
| 400 | `<HEX>` | Placeholder text |
| 500 | `<HEX>` | Texto secundário |
| 600 | `<HEX>` | Texto de apoio |
| 700 | `<HEX>` | Texto principal |
| 800 | `<HEX>` | Headings |
| 900 | `<HEX>` | Texto enfatizado, alto contraste |

### Semantic

<!-- Cores de feedback: success, warning, error. -->

| Token | Hex | Uso |
|-------|-----|-----|
| Success | `<HEX>` | Confirmações, estados positivos, badges de sucesso |
| Warning | `<HEX>` | Alertas, atenção necessária |
| Error | `<HEX>` | Erros, validação falha, ações destrutivas |

### Contraste WCAG AA

<!-- Documentar pares cor/background e suas razões de contraste. -->

| Texto | Background | Razão | Status |
|-------|-----------|-------|--------|
| <COR_TEXTO> | <COR_BG> | <RAZAO:1> | <PASS / FAIL> |

---

## 2. Tipografia

<!-- Font families e escala tipográfica completa. Base: 1rem = 16px. -->

### Font Families

| Tipo | Font Family | Fallback |
|------|------------|----------|
| Primária | `<FONT_PRIMARY>` | `<FALLBACK_STACK>` |
| Monospace | `<FONT_MONO>` | `<FALLBACK_STACK>` |

### Escala Tipográfica

| Token | Font Size (rem) | Line Height | Font Weight | Uso |
|-------|----------------|-------------|-------------|-----|
| h1 | <SIZE> | <LH> | <WEIGHT> | Título principal da página |
| h2 | <SIZE> | <LH> | <WEIGHT> | Título de seção |
| h3 | <SIZE> | <LH> | <WEIGHT> | Subtítulo de seção |
| h4 | <SIZE> | <LH> | <WEIGHT> | Título de card / grupo |
| h5 | <SIZE> | <LH> | <WEIGHT> | Label de destaque |
| h6 | <SIZE> | <LH> | <WEIGHT> | Label pequeno |
| body | <SIZE> | <LH> | <WEIGHT> | Texto corrido padrão |
| small | <SIZE> | <LH> | <WEIGHT> | Texto auxiliar, captions |
| caption | <SIZE> | <LH> | <WEIGHT> | Metadados, timestamps |

---

## 3. Espaçamentos

<!-- Escala baseada em 4px. Usar nomes semânticos para consistência. -->

| Token | Valor | Uso Típico |
|-------|-------|-----------|
| `xs` | 4px | Gap mínimo, ícone-texto |
| `sm` | 8px | Padding interno de badges, gap entre itens inline |
| `sm-md` | 12px | Padding de pills, compact list items, ícone-label |
| `md` | 16px | Gap padrão entre elementos, padding de inputs |
| `lg` | 24px | Padding de containers, gap entre seções |
| `xl` | 32px | Margem entre blocos |
| `2xl` | 48px | Separação de seções da página |
| `3xl` | 64px | Espaço acima/abaixo do hero, separação de áreas |

---

## 4. Bordas e Sombras

### Border Radius

| Token | Valor | Uso |
|-------|-------|-----|
| `sm` | 4px | Inputs, badges |
| `md` | 8px | Cards, botões |
| `lg` | 12px | Modais, containers |
| `full` | 9999px | Avatares, pills |

### Border Width

| Token | Valor | Uso |
|-------|-------|-----|
| `thin` | 1px | Bordas padrão, dividers |
| `medium` | 2px | Bordas de foco, ênfase |

### Sombras

| Token | Valor | Uso |
|-------|-------|-----|
| `sm` | `<BOX_SHADOW_SM>` | Cards, elementos sutilmente elevados |
| `md` | `<BOX_SHADOW_MD>` | Dropdowns, popovers |
| `lg` | `<BOX_SHADOW_LG>` | Modais, overlays |

---

## 5. Catálogo de Componentes Base

<!-- Para cada componente: propósito, variantes, tamanhos, estados. Todos os valores devem referenciar tokens definidos acima. -->

### 5.1 Button

<!-- Componente de ação principal. -->

**Variantes:** primary, secondary, ghost
**Tamanhos:** sm, md, lg

| Propriedade | Primary | Secondary | Ghost |
|------------|---------|-----------|-------|
| Background | `<TOKEN_REF>` | `<TOKEN_REF>` | transparent |
| Text color | `<TOKEN_REF>` | `<TOKEN_REF>` | `<TOKEN_REF>` |
| Border | none | `<TOKEN_REF>` | none |
| Border radius | `<TOKEN_REF>` | `<TOKEN_REF>` | `<TOKEN_REF>` |

**Estados:**

| Estado | Comportamento Visual |
|--------|---------------------|
| Default | <DESCRICAO> |
| Hover | <DESCRICAO> |
| Active | <DESCRICAO> |
| Disabled | <DESCRICAO: opacity, cursor, cores> |
| Focus | <DESCRICAO: outline/ring> |

---

### 5.2 Input

<!-- Campos de entrada de dados. -->

**Tipos:** text, select, textarea, checkbox, radio

| Propriedade | Valor |
|------------|-------|
| Background | `<TOKEN_REF>` |
| Border | `<TOKEN_REF>` |
| Border radius | `<TOKEN_REF>` |
| Padding | `<TOKEN_REF>` |
| Font | `<TOKEN_REF>` |
| Placeholder color | `<TOKEN_REF>` |

**Estados:**

| Estado | Comportamento Visual |
|--------|---------------------|
| Default | <DESCRICAO> |
| Focus | <DESCRICAO: border color change, outline/ring> |
| Error | <DESCRICAO: border error color, mensagem abaixo> |
| Disabled | <DESCRICAO: background, cursor> |

---

### 5.3 Card

<!-- Container de conteúdo agrupado. -->

**Variantes:** com header, sem header; com footer, sem footer; com imagem, sem imagem

| Propriedade | Valor |
|------------|-------|
| Background | `<TOKEN_REF>` |
| Border | `<TOKEN_REF>` |
| Border radius | `<TOKEN_REF>` |
| Shadow | `<TOKEN_REF>` |
| Padding | `<TOKEN_REF>` |

---

### 5.4 Modal

<!-- Overlay para ações que exigem atenção. -->

| Propriedade | Valor |
|------------|-------|
| Background | `<TOKEN_REF>` |
| Overlay | `<TOKEN_REF: cor + opacidade>` |
| Border radius | `<TOKEN_REF>` |
| Shadow | `<TOKEN_REF>` |
| Max width | `<VALOR>` |
| Padding | `<TOKEN_REF>` |

**Estrutura:** Título + Corpo + Ações (Confirmar / Cancelar)

---

### 5.5 Table

<!-- Exibição de dados tabulares. -->

| Propriedade | Valor |
|------------|-------|
| Header background | `<TOKEN_REF>` |
| Row background | `<TOKEN_REF>` |
| Row alt background | `<TOKEN_REF>` |
| Border | `<TOKEN_REF>` |
| Cell padding | `<TOKEN_REF>` |

**Estados:**

| Estado | Comportamento Visual |
|--------|---------------------|
| Default | <DESCRICAO> |
| Empty | <DESCRICAO: mensagem, ilustração> |
| Loading | <DESCRICAO: skeleton rows> |
| Row hover | <DESCRICAO: background change> |

---

### 5.6 Badge

<!-- Indicadores visuais compactos. -->

**Variantes:** info, success, warning, error
**Tamanhos:** sm, md

| Variante | Background | Text Color |
|----------|-----------|-----------|
| Info | `<TOKEN_REF>` | `<TOKEN_REF>` |
| Success | `<TOKEN_REF>` | `<TOKEN_REF>` |
| Warning | `<TOKEN_REF>` | `<TOKEN_REF>` |
| Error | `<TOKEN_REF>` | `<TOKEN_REF>` |

---

### 5.7 Alert

<!-- Mensagens de feedback contextuais. -->

**Variantes:** info, success, warning, error
**Com/sem ação** (botão dismiss ou action link)

| Variante | Background | Border Left | Icon | Text Color |
|----------|-----------|-------------|------|-----------|
| Info | `<TOKEN_REF>` | `<TOKEN_REF>` | <ICON> | `<TOKEN_REF>` |
| Success | `<TOKEN_REF>` | `<TOKEN_REF>` | <ICON> | `<TOKEN_REF>` |
| Warning | `<TOKEN_REF>` | `<TOKEN_REF>` | <ICON> | `<TOKEN_REF>` |
| Error | `<TOKEN_REF>` | `<TOKEN_REF>` | <ICON> | `<TOKEN_REF>` |

---

## Status

- **Criado em:** <YYYY-MM-DD>
- **Última atualização:** <YYYY-MM-DD>
- **Status:** draft
- **Aprovado por:** —
- **Data de aprovação:** —
