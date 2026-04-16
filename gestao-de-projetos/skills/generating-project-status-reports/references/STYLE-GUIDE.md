# M7 Investimentos — PPTX Style Guide (v4 — M7-2026 Brand)

Source: M7 Brandbook 2026 + multi7.com.br

## Fundamental Layout Rule

**Two distinct background modes:**

| Mode | Background | Used for | Text colors |
|------|-----------|----------|-------------|
| **DARK** | `#424135` (Verde Caqui) | Cover, Agenda, Section Divider, Closing | Off-white `#fffdef` text |
| **LIGHT** | `#fffdef` (Off-White) | ALL content slides | Dark text (`#424135` titles, `#4f4e3c` body) |

This is the most critical design decision. Content slides ALWAYS use off-white backgrounds.

## Slide Dimensions

| Property | Value |
|----------|-------|
| Width | 10.00 inches (9,144,000 EMU) |
| Height | 5.625 inches (5,143,500 EMU) |
| Aspect | 16:9 widescreen |

## Color Palette

### Backgrounds & Structure

| Name | Hex | Usage |
|------|-----|-------|
| Verde Caqui | `#424135` | Cover/closing bg, titles on light bg |
| Off-White | `#fffdef` | Content slide bg, text on dark slides |
| White | `#FFFFFF` | Card surfaces |
| Card | `#F6F6F5` | Card/box backgrounds (verde-caqui-50) |
| Separator | `#D0D0CC` | Thin lines, connector dots (verde-caqui-100) |

### Text Colors

| Name | Hex | On Light bg | On Dark bg |
|------|-----|-------------|------------|
| Verde Caqui | `#424135` | Titles (TWK Everett 24pt) | — |
| Verde Medio | `#4F4E3C` | Body text, card titles | — |
| Verde Claro | `#79755C` | Intro paragraphs, secondary | — |
| Verde Caqui 200 | `#AEADA8` | Descriptions, footnotes, arrows | — |
| Off-White | `#fffdef` | — | All text on dark slides |
| Lime | `#EEF77C` | Section labels ("01 — CONTEXTO") | Taglines, accents |

### Accent Colors

| Name | Hex | Usage |
|------|-----|-------|
| Lime | `#EEF77C` | Primary accent, section labels, highlights (DECORATIVE ONLY) |
| Success Green | `#4CAF50` | Positive, done, success callouts |
| Amber | `#F59E0B` | Warning, in-progress |
| Red | `#E46962` | Risk, negative, problem items |
| Blue | `#3B82F6` | Info, sprint accents |
| Purple | `#8B5CF6` | Tertiary accent |
| Teal | `#14B8A6` | Quaternary accent |

### Callout Backgrounds

| Name | Hex | Paired with |
|------|-----|-------------|
| Highlight | `#FFFDF4` | Lime accent (off-white-300) |
| Light Green | `#E8F5E9` | Green accent (success) |
| Light Red | `#FDEDED` | Red accent (warning) |

### Color Progression

Steps, sprints, and sequential items use this progression:
`#424135` → `#EEF77C` → `#F59E0B` → `#4CAF50` → `#3B82F6` → `#8B5CF6` → `#14B8A6`

## Typography

### Font Family

| Font | Role |
|------|------|
| **TWK Everett** | ALL text — headings AND body. Weight differentiates role |

**Fallback**: Arial (for systems without TWK Everett installed)

**Brandbook rule**: Headings use Light weight (NOT Bold). Authority comes from size and color, not weight. Bold is reserved for metrics and emphasis only.

### Font Scale on LIGHT Content Slides

| Role | Font | Size (pt) | Bold | Color |
|------|------|-----------|------|-------|
| Section label | TWK Everett | ~9pt | Yes | `#EEF77C` Lime |
| Title | TWK Everett | ~24pt | **No** | `#424135` |
| Intro paragraph | TWK Everett | ~12pt | No | `#79755C` |
| Card title | TWK Everett | ~11pt | Yes | `#4F4E3C` |
| Card body | TWK Everett | ~10pt | No | `#4F4E3C` |
| Description | TWK Everett | ~10pt | No | `#AEADA8` |
| Footnote | TWK Everett | ~9pt | No | `#AEADA8` |
| Badge label (Nx) | TWK Everett | ~14pt | Yes | `#FFFFFF` on color |
| Step number | TWK Everett | ~18pt | Yes | Accent color |

### Font Scale on DARK Slides

| Role | Font | Size | Bold | Color |
|------|------|------|------|-------|
| Cover title | TWK Everett | 36pt | **No** | `#fffdef` |
| Cover label | TWK Everett | 10pt | Yes | `#fffdef` |
| Cover tagline | TWK Everett | 16pt | No | `#EEF77C` |
| Agenda title | TWK Everett | 26pt | **No** | `#fffdef` |
| Agenda item | TWK Everett | 14pt | No | `#fffdef` |
| Footer | TWK Everett | 12pt | No | `#fffdef` |

## Logo

| Property | Value |
|----------|-------|
| Dark logo | `assets/m7-logo-dark.png` (verde caqui #424135) → light bg |
| Off-white logo | `assets/m7-logo-offwhite.png` (#fffdef) → dark bg |
| Favicon | `assets/m7-logo-favicon.png` (64x64) |
| Size | 502,920 x 251,460 EMU (~0.55" × 0.275") — 2:1 ratio |
| Position | Top-right corner |
| Left | 8,321,040 EMU |
| Top | 137,160 EMU |
| Presence | Every slide |
| Min size | 15px digital (brandbook rule) |
| Protection area | Half logo width in each direction |

**Logo selection rule**: Use off-white logo on DARK slides, dark logo on LIGHT slides.

## Hero Image

| Property | Value |
|----------|-------|
| Original | `assets/m7-hero.png` (3840x1760, M7 brand photo) |
| Darkened | `assets/m7-hero-dark.png` (40% brightness, for overlay use) |
| Usage | **Cover slide background** (hero-dark, full-bleed). Also for section dividers and atmospheric backgrounds |

## Content Slide Header (Universal)

Every content slide has the same header structure:

| Element | Position (left, top) | Size (w, h) |
|---------|---------------------|-------------|
| Logo | 8,321,040 / 137,160 | 502,920 x 502,920 |
| Section label | 548,640 / 365,760 | 5,486,400 x 274,320 |
| Title | 548,640 / 640,080 | 8,046,720 x 548,640 |
| Intro paragraph | 548,640 / 1,371,600 | 7,772,400 x 731,520 |
| Footnote | 548,640 / 4,617,720 | 7,772,400 x 274,320 |

Left margin: 548,640 EMU (~0.6 inches) consistently.

## Visual Patterns from Reference

### Problem Items
- Red accent bar (54,864 wide) + x icon in red + bold title + gray description
- Rows spaced ~548,640 EMU apart

### Step Cards
- Horizontal cards with colored top accent bar (54,864 high)
- Number in accent color, title below
- Arrow connectors between cards in gray

### Metric Cards
- Cards with left accent bar (54,864 wide), big number, description
- Grouped in rows of 3

### Numbered Steps
- Colored circles (365,760 diameter) with off-white number
- Title + description + right-aligned label in matching color
- Circle colors follow progression

### Flow Columns
- Colored header bars (640,080 high) with off-white text
- Bullet items below using triangle marker
- Arrow connectors between columns

### Hierarchy Levels
- Badge (Nx) with colored fill, progressively indented
- Content bar in #F6F6F5 with title + description + colored example
- Connector dots between levels

### Sprint Cards
- Tall cards (2,011,680 high) with top accent bar
- Sprint code, name, detail, divider line, date range
- Arrow connectors between cards

### Callout Boxes
- Tinted background + colored left accent bar (54,864 wide) + bold text
- Variants: highlight/lime, green (success), amber (warning)

## Numbering Pattern

- Section labels: "01 — CONTEXTO", "02 — ABORDAGEM"
- Always zero-padded: 01, 02, ... 09, 10
- Agenda items: numbers in lime circles

## Graphic Elements (Brandbook)

Angular forms derived from the negative space between "M" and "7" in the logo:
- Used as layers, frames, and crop masks over photographs
- Color: verde caqui `#424135` or lime `#EEF77C` (semi-transparent)
- Icons inspired by the angle of the "7" — linear, geometric, minimal

## Photographic Style (Brandbook)

| Aspect | Guideline |
|--------|-----------|
| Casting | Diverse, inclusive, representative |
| Lighting | Solar, natural, warmth |
| Acting | Natural, neutral, sophisticated |
| Focus | Human figure as central element |
| Treatment | Warm tones, moderate contrast |
