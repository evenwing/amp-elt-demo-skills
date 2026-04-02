---
name: amp-carousel
description: >
  Create LinkedIn carousel slides as individual PNG images in Amplitude's brand style
  (black background, Amplitude Blue #0052F2, Poppins font, gradient accent bar).
  Use this skill whenever Sandhya asks for a LinkedIn carousel, social media slides,
  a slide deck for LinkedIn, or any request like "make a carousel about X" or
  "turn this into LinkedIn slides." Also use when she says "create slides" or
  "make this shareable" in the context of LinkedIn content. Always use this skill —
  never try to generate carousels ad-hoc without it.
---

# Amplitude LinkedIn Carousel Skill

Generates professional 1080×1080 PNG carousel slides for LinkedIn using Amplitude's brand.

## Brand Spec

- **Background**: Black `#000000`
- **Primary**: Amplitude Blue `#0052F2`
- **Accent colors**: Lilac `#6980FF`, Violet `#A373FF`, Pink `#FF7D78`
- **Darks**: Dark Blue `#001A4F`, Gray100 `#13171A`, Gray90 `#242A2E`
- **Text grays**: Gray40 `#9FA5AD`, Gray50 `#868D95`, Gray60 `#697077`, Gray20 `#D5D9E0`
- **Font**: Poppins (Bold, Medium, Regular) — installed at `/usr/share/fonts/truetype/google-fonts/`
- **Top bar**: 8px horizontal gradient from `#0052F2` → `#6980FF` → `#A373FF`
- **Logo**: Real Amplitude logo PNG when `--logo-dir` is provided; falls back to drawn blue rounded-rect + "Amplitude" text
- **Title slide motif**: Abstract wave ribbon (blue→violet gradient) inspired by Amplitude's brand graphic elements

## Workflow

### Step 1 — Understand the content

Parse the user's input:
- If they give a **topic** (e.g. "MCP adoption"), research it yourself before writing slides
- If they give a **data summary or bullet points**, use those directly as slide content
- If they give a **document or article**, extract the key insights

### Step 2 — Plan the carousel

Decide on a slide count based on content depth:
- **5–7 slides**: tight topic, single stat or concept
- **8–10 slides**: medium topic with multiple angles
- **11–14 slides**: data-rich or multi-part narrative

Always include:
1. **Title slide** — bold hook, subtitle, "SWIPE →" at bottom
2. **Content slides** — 1 clear idea per slide (stat, concept, list, timeline, etc.)
3. **CTA slide** — closing statement + follow prompt + author name

**Before generating, tell the user your planned slide count and outline, and ask for a quick thumbs up or any changes.** Keep the ask concise — just the count and a 1-line summary per slide.

### Step 3 — Generate the PNGs

Use the bundled script at `scripts/generate_carousel.py`. Call it like this:

```bash
python3 <skill_dir>/scripts/generate_carousel.py \
  --slides '<JSON>' \
  --output './carousel/'
```

Where:
- `--slides` is a JSON array of slide objects (see schema below), or use `--slides-file path/to/slides.json`
- `--output` is the directory to save PNGs to (e.g. `./carousel/`)

**Logo resolution**: The script automatically finds the Amplitude logo by checking:
1. `amp-carousel/assets/` (bundled in skill) — takes priority if present
2. `amp brand/Amplitude Logo/Full/PNG (RGB)/` (workspace fallback)
3. Drawn "A" fallback if neither is found

No `--logo-dir` flag needed — logos are resolved automatically.

### Step 4 — Review and present

Read back the generated PNGs using the Read tool to visually verify each slide looks correct — check for text overflow, missing content, or layout issues. Fix any problems by adjusting the slides JSON and re-running. Then present the files.

---

## Slide JSON Schema

Each slide is an object with a `type` and content fields.

```json
[
  {
    "type": "title",
    "hook": "THE PROTOCOL SHIFT",
    "headline": ["MCP Adoption", "Is Exploding.", "Here's Why."],
    "headline_highlight": [false, true, false],
    "subtitle": "How the Model Context Protocol went from experiment to industry standard in 16 months",
    "swipe": true
  },
  {
    "type": "stat",
    "label": "THE SCALE",
    "big_number": "97M",
    "big_unit": "monthly SDK downloads",
    "date": "as of March 2026",
    "context": ["For comparison: React's npm package took ~3 years to reach 100M monthly downloads.", "MCP got there in 16 months."]
  },
  {
    "type": "text",
    "label": "WHAT IS MCP?",
    "headline": ["One protocol to connect", "any AI to any tool"],
    "headline_highlight": [false, true],
    "body": "The Model Context Protocol (MCP) is an open standard that lets AI agents securely access data sources, APIs, and tools through a single, universal interface.",
    "callout": "Think of it as USB-C for AI — one connector that works everywhere."
  },
  {
    "type": "grid",
    "label": "BY THE NUMBERS",
    "headline": ["The ecosystem is", "massive"],
    "headline_highlight": [false, true],
    "items": [
      {"number": "10,000+", "label": "Active public\nMCP servers", "color": "blue"},
      {"number": "6,400+", "label": "Servers in the\nofficial registry", "color": "lilac"},
      {"number": "4x", "label": "Growth in remote\nservers since May '25", "color": "violet"},
      {"number": "16 mo.", "label": "From launch to\nindustry standard", "color": "pink"}
    ]
  },
  {
    "type": "checklist",
    "label": "WHO'S IN",
    "headline": ["Every major AI player", "now ships MCP"],
    "headline_highlight": [false, true],
    "items": [
      {"name": "Claude", "detail": "Native MCP support across all products"},
      {"name": "ChatGPT", "detail": "MCP integration in agents & plugins"},
      {"name": "Gemini", "detail": "MCP-compatible tool framework"}
    ]
  },
  {
    "type": "timeline",
    "label": "THE TIMELINE",
    "headline": ["From experiment to", "industry standard"],
    "headline_highlight": [false, true],
    "subtitle": "MCP's adoption curve has been remarkably fast:",
    "events": [
      {"date": "Nov 2024", "title": "Anthropic launches MCP", "desc": "as an open protocol for AI-tool connectivity"},
      {"date": "Mid 2025", "title": "OpenAI, Google, Microsoft adopt MCP", "desc": "in their agent frameworks"},
      {"date": "Dec 2025", "title": "Donated to Linux Foundation", "desc": "Agentic AI Foundation (AAIF) formed"},
      {"date": "Mar 2026", "title": "97M monthly downloads", "desc": "de facto standard for agentic AI"}
    ]
  },
  {
    "type": "cards",
    "label": "GROWING PAINS",
    "headline": ["What's still", "unsolved"],
    "headline_highlight": [false, true],
    "headline_color": "pink",
    "items": [
      {"number": "1", "title": "Authentication & security", "desc": "Enterprise-grade auth across remote MCP servers is still maturing."},
      {"number": "2", "title": "Discovery & trust", "desc": "With 10K+ servers, finding reliable, well-maintained ones is a real problem."},
      {"number": "3", "title": "Production observability", "desc": "Monitoring and debugging agent-to-tool interactions at scale needs better tooling."}
    ]
  },
  {
    "type": "cta",
    "headline": ["The agent era", "needs better data."],
    "headline_highlight": [false, true],
    "taglines": [
      "MCP makes agents powerful.",
      "Amplitude makes them measurable.",
      "Together, they close the loop."
    ],
    "cta_button": "Follow for more on AI product analytics",
    "author": "Sandhya Hegde  ·  Amplitude"
  }
]
```

### Slide types

| Type | Use for |
|---|---|
| `title` | Cover slide with hook + headline + subtitle |
| `stat` | Big number stat with context |
| `text` | Concept explanation with optional callout box |
| `grid` | 2×2 grid of stats/metrics |
| `checklist` | List of items with checkmarks |
| `timeline` | Chronological events |
| `cards` | Numbered cards (3–4 items) |
| `cta` | Closing slide with CTA button |

### Color names for highlight/accent fields

| Name | Hex |
|---|---|
| `blue` | `#0052F2` |
| `lilac` | `#6980FF` |
| `violet` | `#A373FF` |
| `pink` | `#FF7D78` |
| `white` | `#FFFFFF` |

---

## Typography rules

All text is center-aligned. Font size guidelines — these are intentionally large for mobile readability:

| Element | Size | Weight |
|---|---|---|
| Slide label (e.g. "THE SCALE") | 18px | Bold |
| H1 headline (title slide) | 72px | Bold |
| H2 headline (content slides) | 48px | Bold |
| Big stat number | 160px | Bold |
| Body text | 26px | Regular |
| Callout / card detail | 22px | Medium |
| Small caption | 18px | Regular |
| CTA button | 24px | Bold |

Poppins Bold at these sizes renders cleanly on mobile at carousel thumbnail size. Do not go below 18px for any text.

---

## Notes

- Each slide is exactly 1080×1080px (LinkedIn square carousel format)
- All content is horizontally centered
- Padding: 80px on left/right, 120px top (to clear logo), 80px bottom
- The generator script handles all layout — just populate the JSON correctly
- If a slide has too much text to fit, split it across two slides

## Layout behavior

- **Vertical centering**: `text`, `stat`, `checklist`, and `cards` slide types all vertically center their content block within the available space (between logo area and bottom padding). This keeps content visually balanced rather than anchored to the top.
- **Stat context text**: Uses `draw_wrapped_centered` return values to track actual rendered height, preventing overlap when context paragraphs wrap to multiple lines.
- **Title slide**: Includes a subtle wave motif in the lower portion (blue→violet gradient ribbon) inspired by Amplitude's brand graphic elements. Text is positioned above it.
- **Real logo**: When `--logo-dir` is provided, the script loads and caches the official Amplitude full logo PNG (scaled to 44px height) and composites it onto every slide.
