# Slide Type Layout Specifications

All coordinates in **points** (1 inch = 72 points). Slide size: 720 × 405 points.

## Global Layout Constants

```
SLIDE_W = 720
SLIDE_H = 405
PAD = 36          // Edge padding
CARD_GAP = 16     // Gap between cards
CONTENT_X = 36    // Content left edge
CONTENT_W = 648   // Content width (720 - 36*2)
FOOTER_Y = 388    // Footer baseline
FOOTER_X = 684    // Footer right edge (720 - 36)
```

## Universal Headline Rule

**All non-title slides** (Types 2–4) follow the same headline pattern:

| Property | Value |
|----------|-------|
| Position | x=36, y=20 |
| Size | width=648, height=70 |
| Font | Poppins SemiBold (bold) 28pt |
| Alignment | **Left-aligned** (ParagraphAlignment.START) |
| Color | Black (#000000) on light backgrounds, White (#FFFFFF) on dark backgrounds |

The headline box is 70pt tall to accommodate 2-line wrapping headlines.

Title slides (Type 1) are the only exception — they use 36pt and have their own vertical positioning.

## Vertical Centering Rule

The main body content (cards, columns, bullet cards) must be **vertically centered** between the headline bottom and the footer top:

```javascript
var headlineBottom = 90;  // y=20 + height=70
var footerTop = 385;      // just above footer at y=388
var availableH = footerTop - headlineBottom;  // 295pt
var contentY = headlineBottom + (availableH - contentH) / 2;
```

This keeps the slide visually balanced regardless of how tall the content block is.

---

## Type 1: Title Slide

```
┌──────────────────────────────────────────────┐  Background: #1E61F0 (Amplitude Blue)
│                                    [DATE]    │  Date pill: top-right
│                                              │
│                                              │
│  Large Headline Text                         │  Poppins SemiBold 36pt white
│  Here on Two Lines                           │
│  ─────────────────────                       │  Divider line: rgba white 40%
│  Subtitle / Author                           │  Poppins Regular 14pt rgba white 70%
│                                              │
│                          © 2026 Amplitude... │  Footer 7pt rgba white 50%
└──────────────────────────────────────────────┘
```

### Element positions

| Element | x | y | width | height | Style |
|---------|---|---|-------|--------|-------|
| Background | 0 | 0 | 720 | 405 | Fill: #1E61F0 (Amplitude Blue) |
| Date pill (optional) | 580 | 28 | 110 | 28 | Fill: #FF6B6B, rx:14, text: white bold 10pt |
| Headline | 36 | 140 | 550 | 100 | Poppins SemiBold 36pt, white, left-aligned, line spacing 1.2 |
| Divider line | 36 | 262 | 200 | 1 | Fill: #FFFFFF (40% opacity — use #8AADFF on blue bg) |
| Subtitle | 36 | 275 | 400 | 24 | Poppins Regular 14pt, #C2D4FA (white 70% on blue) |
| Second subtitle line | 36 | 298 | 400 | 24 | Poppins Regular 14pt, #C2D4FA |
| Footer | FOOTER_X | FOOTER_Y | — | — | Right-aligned, 7pt, #8AADFF (white 50% on blue) |

### Optional decorative elements

Title slides can include decorative graphics on the right side (the area not occupied by headline text). These are built from native Slides shapes — no images needed.

**Constellation network** (good for data/analytics/protocol themes):
- Offset: `ox=420, oy=20` puts the network in the top-right quadrant
- Central hub: large white ELLIPSE (r=10) at center of network
- Primary nodes: medium ellipses (r=6-7) in `#C2D4FA`, connected to hub via `insertLine` in `#C2D4FA`
- Secondary nodes: smaller (r=3-4) in `#A8C4FF`, tertiary dust (r=1.5-2) in `#8AADFF`
- Orbit rings: transparent ELLIPSE shapes with dotted `#8AADFF` borders (`DashStyle.DOT`)
- Lines use lighter colors for thinner weights: `#C2D4FA` (thick), `#A8C4FF` (medium), `#8AADFF` (thin)

**"Made by Claude" badge** (bottom-left pill):

| Element | x | y | width | height | Style |
|---------|---|---|-------|--------|-------|
| Badge pill | 36 | 365 | 160 | 24 | ROUND_RECTANGLE, white fill, no border |
| Badge text | — | — | — | — | Poppins Bold 9pt, #1E61F0, center-aligned, "Made by Claude with ❤️" |

---

## Type 2: Content + Bullets

```
┌──────────────────────────────────────────────┐  Background: #000000 or #F0F2F5
│  Headline Question or Statement?             │  Poppins SemiBold 28pt
│                                              │
│  ┌────────────────────────────────────────┐  │
│  │                                        │  │  Rounded card: white fill
│  │  → Bullet item one                     │  │
│  │  → Bullet item two                     │  │  Poppins Regular 14pt
│  │  → Bullet item three                   │  │  Dark Grey text
│  │  → Bullet item four                    │  │
│  │                                        │  │
│  └────────────────────────────────────────┘  │
│                          © 2026 Amplitude... │
└──────────────────────────────────────────────┘
```

### Element positions

| Element | x | y | width | height | Style |
|---------|---|---|-------|--------|-------|
| Background | 0 | 0 | 720 | 405 | Fill: #000000 (dark) or #F0F2F5 (light) |
| Headline | 36 | 20 | 648 | 70 | Poppins SemiBold 28pt, left-aligned, white (dark) or black (light) |
| Content card | 36 | 100 | 648 | 275 | ROUND_RECTANGLE, fill: white, rx:12, vertically centered (see formula) |
| Bullet items | 60 | 125 | 600 | — | Poppins Regular 14pt, #333333, line spacing ~40pt |
| Footer | FOOTER_X | FOOTER_Y | — | — | 7pt, #666666 (dark) or #999999 (light) |

### Dark variant specifics
- Background: #000000
- Headline: white
- Card: white fill, no border (the white card pops on black)
- Optional: grey inner panel on left side of card (for image placeholder)

### Light variant specifics
- Background: #F0F2F5
- Headline: black
- Card: white fill, optional 1pt #E0E0E0 border

---

## Type 3: Multi-Column Cards

```
┌──────────────────────────────────────────────┐  Background: #F0F2F5
│  Headline Left-Aligned Here                  │  Poppins SemiBold 28pt black
│                                              │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐    │
│  │ Icon │  │ Icon │  │ Icon │  │ Icon │     │  Placeholder area
│  │ area │  │ area │  │ area │  │ area │     │
│  │      │  │      │  │      │  │      │     │
│  │Title │  │Title │  │Title │  │Title │     │  Card title 14pt bold
│  │      │  │      │  │      │  │      │     │
│  │[PILL]│  │[PILL]│  │[PILL]│  │[PILL]│     │  Colored pill
│  │      │  │      │  │      │  │      │     │
│  │Desc  │  │Desc  │  │Desc  │  │Desc  │     │  Description 11pt
│  └──────┘  └──────┘  └──────┘  └──────┘    │
│                          © 2026 Amplitude... │
└──────────────────────────────────────────────┘
```

### Card sizing formulas

```javascript
var numCols = N;  // 2, 3, or 4
var totalGaps = (numCols - 1) * CARD_GAP;
var cardW = (CONTENT_W - totalGaps) / numCols;
var cardH = 280;
// Vertically center: contentY = 90 + (295 - cardH) / 2
var cardY = 90 + Math.round((295 - cardH) / 2);  // ≈ 98

for (var i = 0; i < numCols; i++) {
  var cardX = CONTENT_X + i * (cardW + CARD_GAP);
  // ... create card at (cardX, cardY, cardW, cardH)
}
```

### Element positions (4-column example)

| Element | x | y | width | height | Style |
|---------|---|---|-------|--------|-------|
| Background | 0 | 0 | 720 | 405 | Fill: #F0F2F5 |
| Headline | 36 | 20 | 648 | 70 | Poppins SemiBold 28pt, black, left-aligned |
| Card 1 | 36 | 98 | 148 | 280 | ROUND_RECTANGLE, white, rx:12, vertically centered |
| Card 2 | 200 | 98 | 148 | 280 | Same |
| Card 3 | 364 | 98 | 148 | 280 | Same |
| Card 4 | 528 | 98 | 148 | 280 | Same |

### Inside each card (relative to card top-left)

| Element | dx | dy | width | height | Style |
|---------|----|----|-------|--------|-------|
| Icon placeholder | 16 | 16 | cardW-32 | 80 | ROUND_RECTANGLE, #F0F2F5, rx:8 |
| Title text | 16 | 110 | cardW-32 | 40 | Poppins bold 14pt, black |
| Pill | 16 | 165 | 100 | 24 | ROUND_RECTANGLE, accent color, rx:12, white text 9pt bold |
| Description | 16 | 200 | cardW-32 | 70 | Poppins Regular 11pt, #333333 |

---

## Type 4: Stat/Metric Callout

```
┌──────────────────────────────────────────────┐  Background: #F0F2F5
│  Headline About Customer Results              │  Poppins SemiBold 28pt black, left-aligned
│                                              │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐    │
│  │ Img  │  │ Img  │  │ Img  │  │ Img  │     │  Image placeholder
│  │      │  │      │  │      │  │      │     │
│  │Desc  │  │Desc  │  │Desc  │  │Desc  │     │  Short description
│  │      │  │      │  │      │  │      │     │
│  │[VERI]│  │[VERI]│  │[VERI]│  │[VERI]│     │  "VERIFIED OUTCOME" pill
│  │      │  │      │  │      │  │      │     │
│  │+27%  │  │+5%   │  │+$3M  │  │+40%  │     │  Large stat number
│  │conv. │  │users │  │rev.  │  │spend │     │  Stat label
│  └──────┘  └──────┘  └──────┘  └──────┘    │
│                          © 2026 Amplitude... │
└──────────────────────────────────────────────┘
```

Columns are vertically centered between the headline and footer. The stat content block is ~215pt tall, so `contentY = 90 + (295 - 215) / 2 ≈ 130`. Use the same card width formulas as Type 3.

### Inside each column (relative to column top-left)

| Element | dx | dy | width | height | Style |
|---------|----|----|-------|--------|-------|
| Image placeholder | 8 | 0 | cardW-16 | 70 | ROUND_RECTANGLE, #E0E0E0, rx:8 |
| Description | 8 | 78 | cardW-16 | 45 | Poppins Regular 11pt, #333333, center-aligned |
| Pill | center | 130 | 130 | 22 | ROUND_RECTANGLE, accent color, rx:11 |
| Pill text | center | 130 | — | — | Poppins bold 8pt, white, "VERIFIED OUTCOME" |
| Stat number | center | 158 | cardW-16 | 40 | Poppins SemiBold 36pt, accent color, center-aligned |
| Stat label | center | 195 | cardW-16 | 20 | Poppins Regular 11pt, #333333, center-aligned |

### Accent colors by column position

| Column | Pill bg | Stat text color |
|--------|---------|----------------|
| 1 | #1E61F0 (Blue) | #1E61F0 |
| 2 | #5B7BF0 (Blue-Purple) | #5B7BF0 |
| 3 | #FF6B6B (Coral) | #FF6B6B |
| 4 | #7B61FF (Purple) | #7B61FF |

---

## Type 5: Section Divider

```
┌──────────────────────────────────────────────┐  Background: #1E61F0 (Amplitude Blue)
│                                              │
│                                              │
│                                              │
│            Large Centered                    │  Poppins SemiBold 42pt white
│            Headline                          │
│            ──────────                        │  Thin divider: #8AADFF
│                                              │
│                                              │
│                          © 2026 Amplitude... │  Footer 7pt #8AADFF
└──────────────────────────────────────────────┘
```

A simpler variant of the Title Slide used to break a deck into sections. No subtitle, no date pill. Headline is **centered** (exception to the left-align rule since there's no body content).

### Element positions

| Element | x | y | width | height | Style |
|---------|---|---|-------|--------|-------|
| Background | 0 | 0 | 720 | 405 | Fill: #1E61F0 (Amplitude Blue) or #000000 (dark variant) |
| Headline | 36 | 130 | 648 | 140 | Poppins SemiBold 42pt, white, center-aligned |
| Divider line | 310 | 290 | 100 | 2 | Fill: #8AADFF (on blue) or #666666 (on black) |
| Footer | FOOTER_X | FOOTER_Y | — | — | Right-aligned, 7pt, #8AADFF |

---

## Type 6: Two-Column Text

```
┌──────────────────────────────────────────────┐  Background: #F0F2F5
│  Headline Left-Aligned Here                  │  Poppins SemiBold 28pt black
│                                              │
│  ┌──────────────────┐  ┌──────────────────┐  │
│  │ Column Title     │  │ Column Title     │  │  Poppins bold 16pt, Amplitude Blue
│  │                  │  │                  │  │
│  │ → Bullet one     │  │ → Bullet one     │  │  Poppins Regular 12pt, Dark Grey
│  │ → Bullet two     │  │ → Bullet two     │  │
│  │ → Bullet three   │  │ → Bullet three   │  │
│  │ → Bullet four    │  │ → Bullet four    │  │
│  └──────────────────┘  └──────────────────┘  │
│                          © 2026 Amplitude... │
└──────────────────────────────────────────────┘
```

Two side-by-side white cards with section titles and arrow-bulleted content. Use for before/after, challenge/approach, problem/solution comparisons.

### Element positions

| Element | x | y | width | height | Style |
|---------|---|---|-------|--------|-------|
| Background | 0 | 0 | 720 | 405 | Fill: #F0F2F5 |
| Headline | 36 | 20 | 648 | 70 | Poppins SemiBold 28pt, black, left-aligned |
| Left card | 36 | vcenter | 316 | 260 | ROUND_RECTANGLE, white, rx:12, no border |
| Right card | 368 | vcenter | 316 | 260 | Same |
| Column title (inside card) | +20 | +16 | cardW-40 | 30 | Poppins bold 16pt, #1E61F0 |
| Body text (inside card) | +20 | +56 | cardW-40 | 180 | Poppins Regular 12pt, #333333, arrow bullets |
| Footer | FOOTER_X | FOOTER_Y | — | — | 7pt, #999999 |

```javascript
var colW = (CONTENT_W - CARD_GAP) / 2;  // 316
var contentH = 260;
var colY = centerContentY(contentH);
```

---

## Type 7: Quote / Testimonial

```
┌──────────────────────────────────────────────┐  Background: #000000
│                                              │
│  "                                           │  Open quote: Poppins bold 72pt, #1E61F0
│  │                                           │  Accent line: 3pt wide, #1E61F0
│  │ Quote text goes here spanning             │  Poppins Regular 20pt, white
│  │ multiple lines if needed.                 │
│  │                                           │
│  │ Speaker Name                              │  Poppins bold 14pt, white
│  │ Title, Company                            │  Poppins Regular 12pt, #999999
│  │                                           │
│                          © 2026 Amplitude... │
└──────────────────────────────────────────────┘
```

Full-width pull quote with attribution. Use for customer testimonials, stakeholder quotes, key insights.

### Element positions

| Element | x | y | width | height | Style |
|---------|---|---|-------|--------|-------|
| Background | 0 | 0 | 720 | 405 | Fill: #000000 |
| Open quote mark | 36 | 80 | 80 | 80 | Poppins bold 72pt, #1E61F0 |
| Accent line | 36 | vcenter | 3 | 155 | Fill: #1E61F0 |
| Quote text | 56 | vcenter | 608 | 100 | Poppins Regular 20pt, white |
| Speaker name | 56 | vcenter+110 | 300 | 22 | Poppins bold 14pt, white |
| Speaker title | 56 | vcenter+134 | 300 | 20 | Poppins Regular 12pt, #999999 |
| Footer | FOOTER_X | FOOTER_Y | — | — | 7pt, #666666 |

```javascript
var quoteBlockH = 160;
var quoteY = centerContentY(quoteBlockH);
```

---

## Type 8: Image + Text (Split Layout)

```
┌──────────────────────────────────────────────┐  Background: #F0F2F5
│  Headline Left-Aligned Here                  │  Poppins SemiBold 28pt black
│                                              │
│  ┌──────────────────┐                        │
│  │                  │  Section Title          │  Poppins bold 16pt, #1E61F0
│  │    [Image        │                        │
│  │    Placeholder]  │  → Bullet one           │  Poppins Regular 12pt, #333333
│  │                  │  → Bullet two           │
│  │                  │  → Bullet three         │
│  │                  │  → Bullet four          │
│  └──────────────────┘                        │
│                          © 2026 Amplitude... │
└──────────────────────────────────────────────┘
```

Split layout: left half is an image placeholder, right half is text content. Use for product screenshots, architecture diagrams, feature deep-dives.

### Element positions

| Element | x | y | width | height | Style |
|---------|---|---|-------|--------|-------|
| Background | 0 | 0 | 720 | 405 | Fill: #F0F2F5 |
| Headline | 36 | 20 | 648 | 70 | Poppins SemiBold 28pt, black, left-aligned |
| Image placeholder | 36 | vcenter | 320 | 260 | ROUND_RECTANGLE, #E0E0E0, rx:12 |
| Placeholder label | 116 | vcenter+110 | 160 | 30 | Poppins 12pt, #999999, center-aligned |
| Section title | 372 | vcenter+10 | 312 | 30 | Poppins bold 16pt, #1E61F0 |
| Body text | 372 | vcenter+50 | 312 | 200 | Poppins Regular 12pt, #333333, arrow bullets |
| Footer | FOOTER_X | FOOTER_Y | — | — | 7pt, #999999 |

```javascript
var contentH = 260;
var splitY = centerContentY(contentH);
var imgW = 320;
var textX = PAD + imgW + CARD_GAP;  // 372
var textW = CONTENT_W - imgW - CARD_GAP;  // 312
```
