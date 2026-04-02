# Amplitude Brand System for Slides

## Color Palette

| Role | Name | Hex | When to use |
|------|------|-----|-------------|
| Dark backgrounds | Black | `#000000` | Title slides, section dividers, dark-theme content slides |
| Light backgrounds | Light Grey | `#F0F2F5` | Content slides, card-layout slides |
| Primary text (dark bg) | White | `#FFFFFF` | Headlines and body on black backgrounds |
| Primary text (light bg) | Black | `#000000` | Headlines on light grey backgrounds |
| Body text (light bg) | Dark Grey | `#333333` | Descriptions, bullet text on light backgrounds |
| Secondary text | Mid Grey | `#666666` | Subtitles, footer, secondary labels |
| Primary accent | Amplitude Blue | `#1E61F0` | First pill color, active indicators, links |
| Warm accent | Coral | `#FF6B6B` | Warm-tone pills, alert/challenge indicators |
| Cool accent | Purple | `#7B61FF` | Cool-tone pills, step indicators |
| Card fill | White | `#FFFFFF` | Content cards on light grey backgrounds |
| Card border | Card Grey | `#E0E0E0` | Subtle borders on white cards (optional) |

### Accent color usage across columns

When a slide has 2–4 columns with colored pills, use this gradient pattern left to right:

| Columns | Colors (left → right) |
|---------|----------------------|
| 2 | Blue, Purple |
| 3 | Blue, Coral, Purple |
| 4 | Blue, Blue, Coral, Purple |

## Typography

All text uses **Poppins** from Google Fonts (natively available in Google Slides).

| Weight | SlidesApp method | Usage | Size range |
|--------|-----------------|-------|------------|
| SemiBold (600) | `.setBold(true)` | Headlines, large stat numbers | 28–42pt |
| Medium (500) | `.setBold(false)` with manual weight | Sub-headings, card titles, pill labels | 14–20pt |
| Regular (400) | `.setBold(false)` | Body text, descriptions, bullets, footer | 7–14pt |

Note: SlidesApp doesn't have a direct `setFontWeight()` method. Use `.setBold(true)` for SemiBold, and `.setBold(false)` for Medium/Regular. The visual difference between Medium and Regular is subtle at slide sizes, so this approximation works well.

### Size guidelines by slide type

| Element | Title Slide | Content Slide | Stat Slide |
|---------|------------|---------------|------------|
| Headline | 36pt bold | 28pt bold | 28pt bold |
| Subtitle | 14pt regular | — | — |
| Card title | — | 16pt bold | 14pt bold |
| Body text | — | 12pt regular | 11pt regular |
| Stat number | — | — | 36pt bold |
| Stat label | — | — | 11pt regular |
| Pill text | — | 10pt bold | 9pt bold |
| Footer | 7pt regular | 7pt regular | 7pt regular |

## Common Patterns

### Rounded-corner cards
- White fill on light grey background
- Corner radius: 12pt (use `SlidesApp.ShapeType.ROUND_RECTANGLE`)
- Optional light border: 1pt `#E0E0E0`
- Internal padding: 16pt from card edges

### Colored pills / badges
- Small rounded rectangles: height ~24pt, width sized to text + 24pt padding
- Corner radius: 12pt (fully rounded ends)
- White text, colored background (Blue, Coral, or Purple)
- Poppins bold, 9–10pt
- Text centered vertically and horizontally

### Large stat numbers
- Poppins SemiBold, 36pt
- Color matches the pill above it (Blue, Coral, or Purple)
- Positioned directly below the pill
- Descriptor label below in 11pt regular, Dark Grey

### Arrow bullets
- Use the `→` character followed by a space before each bullet item
- Or use regular bullet formatting via SlidesApp paragraph styles

### Footer
- Text: `© 2026 Amplitude, Inc. Confidential. All Rights Reserved.`
- Font: Poppins Regular, 7pt, Mid Grey (`#666666`)
- Position: bottom-right of slide, right-aligned
- Present on every slide

### Horizontal divider
- Thin line (`SlidesApp.ShapeType.RECTANGLE`, height 1pt)
- Color: `#E0E0E0`
- Spans most of the slide width
- Used to separate headline from content on some slides
