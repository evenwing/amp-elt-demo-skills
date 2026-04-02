# amp-slide

Create native Google Slides in Amplitude's brand style using Claude + Google Apps Script.

This skill lets you describe a slide in plain English and get a pixel-perfect, branded Google Slide — no manual formatting. It supports 8 slide types (title, bullets, multi-column cards, stat callouts, section dividers, two-column comparisons, quotes, and image+text splits) and works by generating Apps Script code, injecting it into a reusable Apps Script project via Chrome, and running it.

## What you need

- **Claude desktop app** with Cowork mode (or Claude Code with the skill installed)
- **Claude in Chrome** MCP connected (this is how Claude controls the Apps Script editor)
- **A Google account** with access to Google Slides and Apps Script
- **Poppins font** installed on the Google account (it's a Google Font, available by default in Slides)

## Setup guide

### Step 1: Install the skill

**Option A — From .skill file:**
If you have `amp-slide.skill`, install it through the Claude desktop app or drop it into your skills directory.

**Option B — Manual install:**
Copy the `amp-slide/` folder (containing `SKILL.md`, `references/`, and `scripts/`) into your Claude skills directory:
```
~/.claude/skills/amp-slide/
├── SKILL.md
├── references/
│   ├── amplitude-brand.md
│   ├── apps-script-reference.md
│   └── slide-types.md
└── scripts/
    └── helpers.gs.template
```

### Step 2: Connect Claude in Chrome

Make sure the Claude in Chrome MCP extension is installed and connected. Claude needs this to:
- Navigate to the Apps Script editor
- Inject generated code into the Monaco editor
- Save and run the script
- Take screenshots of the resulting slides for visual QA

### Step 3: Ask for your first slide — setup is automatic!

Just ask Claude to make a slide. On the first run, the skill will detect that no Apps Script project is configured yet and will **automatically**:

1. Open [script.google.com](https://script.google.com) in Chrome
2. Create a new project named **"Slide Builder"**
3. Save the project URL into the skill's config
4. Run a test script to trigger Google's authorization flow
5. Walk you through the one-time **"Allow"** permissions dialog

After that, the skill is fully configured and every future slide request skips straight to building.

### Manual setup (optional)

If you prefer to set up the Apps Script project yourself:

1. Go to [script.google.com](https://script.google.com) → **New project** → rename to **"Slide Builder"**
2. Copy the project URL from the address bar
3. Paste it into `references/apps-script-reference.md` on the Project URL line
4. On first run, click through the authorization dialog: **"Review permissions"** → choose account → **"Advanced"** → **"Go to Slide Builder (unsafe)"** → **"Allow"**

## How it works

```
You: "Make a stat callout slide showing Fender's results"
  │
  ▼
Claude reads the skill → picks slide type → reads layout specs
  │
  ▼
Claude generates a buildSlide() function in Apps Script
  │
  ▼
Claude injects code into Apps Script editor via Chrome
  │
  ▼
Claude saves (Ctrl+S) and clicks Run
  │
  ▼
Google Slides API creates the slide in your presentation
  │
  ▼
Claude screenshots the result and checks for issues
```

## Tutorial: Making your first slide

Here's a walkthrough of the complete flow:

**1. Start a conversation with Claude and ask for a slide:**
> "Make me a title slide for a pitch to Spotify. Presenters are Sandhya Hegde and James Park."

**2. Claude will ask for a presentation URL** (or offer to create a new one):
> Provide an existing deck URL, or say "create a new one"

**3. Claude generates the Apps Script code** — you'll see it thinking through the layout, picking colors, and writing the `buildSlide()` function.

**4. Claude opens the Apps Script editor in Chrome**, injects the code, saves it, and runs it. You may see:
- The Apps Script editor tab open
- Code appearing in the editor
- The Run button being clicked
- An authorization dialog (first time only — Claude will walk through it)

**5. Claude switches to your Google Slides presentation**, takes a screenshot, and shows you the result.

**6. Give feedback and iterate:**
> "Make the headline shorter" or "Switch to the dark variant" or "Add another slide with our key metrics"

Claude will regenerate the code and re-run — the whole cycle takes about 10 seconds.

## Supported slide types

| # | Type | Best for | Background |
|---|------|----------|------------|
| 1 | **Title** | Opening a deck, cover slide | Amplitude Blue |
| 2 | **Content + Bullets** | Key points, agendas, feature lists | Black or Light Grey |
| 3 | **Multi-Column Cards** | Comparisons, initiatives, categories (2-4 cols) | Light Grey |
| 4 | **Stat/Metric Callout** | Customer results, KPIs, impact metrics | Light Grey |
| 5 | **Section Divider** | Breaking a deck into sections | Amplitude Blue or Black |
| 6 | **Two-Column Text** | Before/after, challenge/approach | Light Grey |
| 7 | **Quote / Testimonial** | Customer quotes, key insights | Black |
| 8 | **Image + Text** | Product screenshots, feature deep-dives | Light Grey |

## Brand reference

| Element | Spec |
|---------|------|
| Primary font | Poppins (Regular 400, Medium 500, SemiBold 600) |
| Headlines | 28pt bold, left-aligned (42pt centered for section dividers, 36pt for title slides) |
| Amplitude Blue | `#1E61F0` |
| Coral | `#FF6B6B` |
| Purple | `#7B61FF` |
| Light Grey (backgrounds) | `#F0F2F5` |
| Slide size | 720 × 405 points (10" × 5.625") |

## Troubleshooting

**"Unsaved changes" dialog blocks saving:**
If an account selection dialog appears when Claude tries to Ctrl+S, Claude needs to click "OK" on the dialog first, then click in the editor area, then retry Ctrl+S.

**Authorization dialog won't go away:**
Click through all the prompts — "Review permissions" → choose account → "Advanced" → "Go to Slide Builder (unsafe)" → "Allow". This only happens once per scope.

**First-run setup didn't work:**
If the auto-setup fails (e.g. Chrome MCP can't navigate to script.google.com), follow the manual setup steps in the Setup guide above.

**Slides look wrong or elements overlap:**
Tell Claude what's off. It will take a screenshot, diagnose the issue, and re-run with adjusted coordinates.

**Claude can't find the Apps Script editor:**
Make sure Claude in Chrome MCP is connected and the Apps Script project URL in `references/apps-script-reference.md` matches your actual project.

## Packaging

To create a shareable `.skill` file:

```bash
cd /path/to/amp-slide
zip -r /tmp/amp-slide.skill . -x "./evals/*"
```

The `.skill` format requires `SKILL.md` at the top level of the zip — always `cd` into the skill folder first.
