# M7 D3.js Theme Mapping (v4 — M7-2026 Brand)

Color and typography mapping from the M7-2026 design system to D3.js chart elements.

## Color Mapping

| Chart Element | M7 Token | Hex | CSS/D3 Usage |
|--------------|----------|-----|-------------|
| Series 1 (primary) | Verde Caqui | `#424135` | `fill`, `stroke` for main data |
| Series 2 | Lime | `#EEF77C` | Second series (DECORATIVE — not on text) |
| Series 3 | Verde Claro | `#79755C` | Third series |
| Series 4 | Green | `#4CAF50` | Fourth series or positive values |
| Series 5 | Blue | `#3B82F6` | Fifth series |
| Series 6 | Teal | `#14B8A6` | Sixth series |
| Positive values | Green | `#4CAF50` | Growth, success, above target |
| Negative values | Red | `#E46962` | Decline, risk, below target |
| Axis lines | Separator | `#D0D0CC` | `.axis path`, `.axis line` |
| Axis text | Text Light | `#AEADA8` | `.axis text` |
| Grid lines | Card | `#F6F6F5` | `.grid line` |
| Data labels | Text Body | `#4F4E3C` | `.data-label` |
| Annotations | Text Med | `#79755C` | `.annotation` |
| Chart title | Verde Caqui | `#424135` | `.chart-title` |
| Background | Off-White | `#fffdef` | `body`, SVG background |
| Font family | TWK Everett | — | `font-family: "twkEverett", Arial, sans-serif` |

## JavaScript Theme Object

Every D3 template includes this standard object:

```javascript
const M7 = {
  // Series colors (ordered by usage priority)
  series: ['#424135', '#EEF77C', '#79755C', '#4CAF50', '#3B82F6', '#14B8A6'],

  // Named colors
  verdeCaqui: '#424135',
  lime: '#EEF77C',
  verdeClaro: '#79755C',
  blue: '#3B82F6',
  purple: '#8B5CF6',
  teal: '#14B8A6',

  // Status colors
  positive: '#4CAF50',
  negative: '#E46962',
  amber: '#F59E0B',

  // Structural colors
  dark: '#424135',
  offWhite: '#fffdef',
  text: '#4F4E3C',
  textMed: '#79755C',
  textLight: '#AEADA8',
  axis: '#AEADA8',
  grid: '#F6F6F5',
  separator: '#D0D0CC',
  card: '#F6F6F5',
  white: '#FFFFFF',
};
```

## CSS Base Styles

```css
@font-face {
  font-family: twkEverett;
  src: url("https://multi7.com.br/_next/static/media/TWKEverett_Regular-s.p.4411e19a.otf") format("opentype");
  font-weight: 400; font-display: swap;
}
body { margin: 0; padding: 0; background: #fffdef; font-family: "twkEverett", Arial, sans-serif; }
.axis text { font-family: "twkEverett", Arial, sans-serif; font-size: 11px; fill: #AEADA8; }
.axis path, .axis line { stroke: #D0D0CC; }
.grid line { stroke: #F6F6F5; stroke-width: 1; }
.grid .domain { display: none; }
.annotation { font-family: "twkEverett", Arial, sans-serif; font-size: 12px; fill: #79755C; }
.data-label { font-family: "twkEverett", Arial, sans-serif; font-size: 10px; fill: #4F4E3C; }
.chart-title { font-family: "twkEverett", Arial, sans-serif; font-size: 14px; font-weight: 400; fill: #424135; }
.chart-subtitle { font-family: "twkEverett", Arial, sans-serif; font-size: 11px; fill: #79755C; }
```

## Chart Dimensions

| Property | Value | Notes |
|----------|-------|-------|
| SVG width | 880px | Matches PPTX content width (~8.8") |
| SVG height | 350px | Content area below header |
| Render width | 1760px | 2x for crisp PNG |
| Render height | 700px | 2x for crisp PNG |
| Margin top | 20-40px | Space for title/legend |
| Margin right | 30-80px | Space for end labels |
| Margin bottom | 40-50px | Space for axis + label |
| Margin left | 60-160px | Axis labels (wider for horizontal bars) |

## Color Usage Rules

1. **Max 6 series** — Beyond 6, humans can't distinguish colors
2. **Highlight sparingly** — Use Verde Caqui for the primary data series; gray out secondary
3. **Status colors are semantic** — Green = positive, Red = negative. Don't use them for arbitrary series
4. **Background off-white** — Use `#fffdef` (warm), not pure white, to match PPTX slides
5. **No gradients** — Solid fills only
6. **Accent the insight** — The most important data point should have the strongest color
7. **Lime is decorative** — Never use `#EEF77C` for text (fails WCAG on any light bg)
8. **Font weight 400** — Chart titles use Regular weight, not Bold (M7-2026 rule)
