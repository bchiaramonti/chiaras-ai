# Changelog

All notable changes to the gestao-de-projetos plugin will be documented in this file.

## [1.6.2] - 2026-04-06

### Added
- Base64 (.b64) companions for all 5 PNG assets in `generating-project-status-reports/assets/` — enables self-contained HTML generation

## [1.6.0] - 2026-03-02

### Changed
- Migrated `generating-project-status-reports` skill from v3 (generic design) to v4 (M7-2026 Brandbook)
- Updated `m7_pptx_lib.py` color palette: Verde Caqui `#424135`, Off-White `#fffdef`, Lime `#EEF77C`, organic text tones
- Updated typography from Arial/Arial Black to TWK Everett (headings NOT bold, per brandbook)
- Cover slides now use `m7-hero-dark.png` full-bleed background (fallback: solid Verde Caqui)
- Logo selection is now automatic: dark logo on light slides, off-white logo on dark slides
- Updated all 8 D3 chart templates to M7-2026 theme (TWK Everett, off-white bg, organic palette)
- Updated EXECUTIVE-STATUS-LAYOUT.md and CHART-RECIPES.md references to M7-2026 brand

### Added
- `m7-logo-dark.png`, `m7-logo-offwhite.png`, `m7-hero-dark.png`, `m7-logo-favicon.png` assets
- `STYLE-GUIDE.md` reference (M7-2026 full design system spec)
- `M7-D3-THEME.md` reference (D3 chart color mapping)
- `FONT_HEADING`, `FONT_BODY`, `FONT_FALLBACK` constants in m7_pptx_lib.py
- `C.OFF_WHITE`, `C.BG_HIGHLIGHT` color constants with backward-compat aliases
- `_set_hero_bg()` function for cover slide backgrounds
- "M7 Design System" and "Additional Resources" sections in SKILL.md

## [1.5.0] - 2026-02-24

### Added
- `generating-project-status-reports` skill with Executive Status slides, D3 charts, and milestone grids

## [1.4.0] - 2026-02-20

### Added
- `decomposing-goals-into-sprints` skill for sprint planning from strategic goals
