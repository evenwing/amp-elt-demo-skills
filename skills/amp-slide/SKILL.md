---
name: amp-slide
description: >
  Create native Google Slides in Amplitude's brand style using Google Apps Script. Use this skill whenever Sandhya asks to make a slide, add a slide to a deck, create a presentation slide, or build a Google Slide — even if she just says "make me a slide about X" or "add a slide showing Y." Also use when she references the Amplitude pitch deck style, wants branded slides, or asks for stat callouts, bullet slides, or card layouts in Google Slides format. This skill outputs native Google Slides (NOT .pptx files) by generating and running Apps Script code via Chrome. Trigger for any Google Slides creation or editing task.
---

# amp-slide

Create native Google Slides in Amplitude's brand style. This skill generates Apps Script code, injects it into the "Slide Builder" project via Chrome, and runs it to produce slides directly in Google Slides.

## Design Philosophy

Inherited from the diagram skill, adapted for Amplitude:

- **3-second test**: A viewer grasps the core idea within 3 seconds
- **One concept per slide**: Don't pack multiple ideas into a single slide
- **Fill the canvas**: Content should occupy most of the slide. No big empty gaps
- **Purposeful decoration**: Decorative elements are welcome on title slides (constellation networks, geometric patterns) but should reinforce the content theme. On content slides, every element should earn its place.
- **Amplitude brand**: Uses Amplitude's colors, Poppins font, and template patterns

## When to use

This skill creates individual slides or full decks. It can either create a new presentation or add slides to an existing one. If the user wants to add to an existing deck, ask for the presentation URL.

### Full deck builds vs. small edits

When the user asks for a **full deck from scratch** (multiple slides, new presentation), ask them upfront which build mode they prefer:

- **Batch mode (recommended)** — Generate one Apps Script that builds all slides at once. Faster (~30 sec total), but the user waits without visual feedback until the whole deck is done. After execution, immediately navigate to the presentation and show a filmstrip screenshot so the user sees the result quickly.
- **Slide-by-slide mode** — Build one slide at a time: generate → inject → run → screenshot → get feedback → repeat. Slower (15-20 sec per slide) but the user can review and adjust each slide before moving on.

**Do NOT ask this question** for small edits — adding 1-2 slides to an existing deck, modifying content on a slide, or fixing layout issues. Just do the work directly.

### In-place slide editing

To modify an existing slide (fix text, adjust layout, rebuild a chart), use the **clear-and-rebuild** pattern: get the slide by index, remove all elements, then re-draw. This preserves slide position in the deck. See `references/apps-script-reference.md` → "In-Place Slide Editing" for the code pattern.

## Quick Reference

Read the detailed reference files as needed:
- `references/amplitude-brand.md` — Full color palette, typography specs, and brand patterns
- `references/slide-types.md` — Pixel-level layout specs for each of the 8 supported slide types
- `references/apps-script-reference.md` — SlidesApp API patterns, Monaco injection technique, and gotchas

## Supported Slide Types

### 1. Title Slide
Amplitude Blue (`#1E61F0`) background, large white headline, subtitle. No date pill. Use for opening a deck or starting a section. Can include optional concentric arc rings in the bottom-right corner as a subtle geometric decoration (built from native ellipses positioned partially off-slide, no image uploads needed). A "Made by Claude with ❤️" badge pill is a nice touch for AI-generated decks. See `references/apps-script-reference.md` → "Concentric arc rings" for the pattern.

### 2. Content + Bullets
Light or dark background, headline at top, rounded-corner card containing arrow-bulleted items. Use for key points, feature lists, talking points.

### 3. Multi-Column Cards (2–4 columns)
Light background, headline at top, equal-width cards in a row with titles and descriptions. Optional colored pill at bottom of each card. Use for comparisons, initiatives, categories.

### 4. Stat/Metric Callout
Light background, headline at top, 2–4 columns each with a description, colored "VERIFIED OUTCOME" pill, and a large stat number + label. Use for customer results, KPIs, impact metrics.

### 5. Section Divider
Amplitude Blue (or black) background, large centered headline, thin divider line. A simpler variant of the Title Slide used to break a deck into sections. No subtitle or date pill.

### 6. Two-Column Text
Light background, headline at top, two side-by-side white cards each with a blue section title and arrow-bulleted body text. Use for before/after, challenge/approach, problem/solution comparisons.

### 7. Quote / Testimonial
Black background, large pull quote in white text with a blue accent line on the left, bold speaker name and grey title below. Use for customer testimonials, stakeholder quotes, key insights.

### 8. Image + Text (Split Layout)
Light background, headline at top, left half is an image placeholder, right half has a blue section title and arrow-bulleted text. Use for product screenshots, architecture diagrams, feature deep-dives.

## Universal Headline Rule

All non-title slides (Types 2–4, 6, 8) use the **same headline style**. Types 1, 5, and 7 have custom layouts:
- **28pt bold, left-aligned** (ParagraphAlignment.START)
- Headline box: x=36, y=20, width=648, height=70 (supports 2-line wrapping)
- **Body content is vertically centered** between headline bottom (y=90) and footer top (y=385). Use `centerContentY(contentH)` helper.
- Title slides (Type 1) are the only exception — they use 36pt, Amplitude Blue background, and custom vertical positioning.

## Brand Summary (read `references/amplitude-brand.md` for full details)

**Colors**: Amplitude Blue `#1E61F0` (title slide bg), White `#FFFFFF`, Light Grey `#F0F2F5` (content slide bgs), Black `#000000` (dark variant bg), Coral `#FF6B6B`, Purple `#7B61FF`, Dark Grey `#333333`, Mid Grey `#666666`

**Typography**: All Poppins. SemiBold for headlines (28–36pt), Medium for sub-headings and labels (14–20pt), Regular for body (11–14pt).

**Footer**: `© 2026 Amplitude, Inc. Confidential. All Rights Reserved.` — Poppins Regular 7pt, Mid Grey, bottom-right.

## First-Run Setup (auto-setup via Chrome)

Before building any slide, check whether an Apps Script project URL is configured in `references/apps-script-reference.md`. If the **Project URL** field is empty, contains a placeholder, or the file doesn't exist yet, run the first-run setup flow below. **Skip this section entirely if a valid project URL is already configured.**

### Setup Step 1: Create the Apps Script project

1. Use Claude in Chrome to navigate to `https://script.google.com`
2. Click **"New project"**
3. Click on "Untitled project" at the top-left and rename it to **"Slide Builder"**
4. The editor will show a default `Code.gs` with `myFunction()` — leave it as-is

### Setup Step 2: Capture and save the project URL

1. Read the URL from the browser address bar — it will look like:
   `https://script.google.com/u/0/home/projects/XXXXXX/edit`
2. Write that URL into `references/apps-script-reference.md` on the Project URL line
3. Also update the URL in this file (SKILL.md) under "Step 4: Inject + run via Chrome" below

### Setup Step 3: Test run to trigger authorization

1. Inject a minimal test function via Monaco:
   ```javascript
   function buildSlide() {
     var pres = SlidesApp.create('amp-slide Setup Test');
     var slide = pres.getSlides()[0];
     slide.getBackground().setSolidFill('#1E61F0');
     var tb = slide.insertShape(SlidesApp.ShapeType.TEXT_BOX, 36, 160, 648, 80);
     tb.getText().setText('Setup complete!');
     tb.getText().getTextStyle().setFontFamily('Poppins').setBold(true).setFontSize(36).setForegroundColor('#FFFFFF');
     tb.getText().getParagraphStyle().setParagraphAlignment(SlidesApp.ParagraphAlignment.CENTER);
     Logger.log('Test presentation: ' + pres.getUrl());
   }
   ```
2. Save (Ctrl+S) and click Run
3. Google will show an authorization dialog — walk the user through it:
   - Click **"Review permissions"**
   - Choose the Google account
   - Click **"Advanced"** → **"Go to Slide Builder (unsafe)"**
   - Click **"Allow"**
4. After authorization completes, the script will create a test presentation. Confirm it worked by checking the execution log for the URL.
5. Let the user know setup is complete and they can delete the test presentation if they want.

**After setup, proceed to the normal workflow below for the user's actual slide request.**

## End-to-End Workflow

### Step 1: Parse the request

Determine which slide type fits the user's content. Extract headlines, bullet points, stats, labels, etc. If the user wants to add to an existing deck, get the presentation URL.

**For full deck builds:** After parsing the content into slides, ask the user which build mode they want (batch vs. slide-by-slide) — see "Full deck builds vs. small edits" above. Then either generate one script for all slides (batch) or proceed one slide at a time.

### Step 2: Read the slide type spec

Read `references/slide-types.md` for the exact layout coordinates and spacing for the chosen slide type. Read `references/apps-script-reference.md` for API patterns.

### Step 3: Generate Apps Script code

Write a `buildSlide()` function. The function should:

**For a new presentation:**
```javascript
var pres = SlidesApp.create('Presentation Name');
var slide = pres.getSlides()[0];
// ... build the slide
Logger.log('Presentation URL: ' + pres.getUrl());
```

**For an existing presentation:**
```javascript
var pres = SlidesApp.openByUrl('USER_PROVIDED_URL');
var slide = pres.appendSlide(SlidesApp.PredefinedLayout.BLANK);
// ... build the slide
```

Use the helper patterns from `scripts/helpers.gs.template` for common elements (cards, pills, stat blocks, footers).

### Step 4: Inject + run via Chrome

1. Navigate to the Apps Script project URL (read from `references/apps-script-reference.md`)
2. Wait for the Monaco editor to load (check for `monaco.editor.getModels()` to be available)
3. Inject code using the **3-phase keyboard trigger approach** (see `references/apps-script-reference.md` → "Monaco Injection Technique"):
   - **Phase A**: Disable auto-closing brackets/quotes, select all, delete via keyboard trigger
   - **Phase B**: Type the new code via `editor.trigger('keyboard', 'type', { text: CODE_STRING })`
   - **Phase C**: Verify `model.getValue().length === CODE_STRING.length`

   > ⚠️ **Do NOT use `monaco.editor.getModels()[0].setValue()`** — it only updates the client-side editor and does not trigger Apps Script's change detection. The Save button stays disabled and "Run" will execute the old server-side code.

   > **Code string construction**: Build CODE_STRING using the `[...].join('\n')` array pattern, not a single escaped string. Each line as a separate single-quoted array element avoids apostrophe/escaping issues. See `references/apps-script-reference.md` → "Code string construction".

4. Save: Click `document.querySelector('[aria-label="Save project to Drive"]').click()` and verify `disabled === true` after 3–4 seconds
5. Run: Click `document.querySelector('[aria-label="Run the selected function"]').click()`
6. Handle authorization dialog if it appears — note that switching from `SlidesApp.create()` to `SlidesApp.openByUrl()` requires an additional Drive scope and will trigger a new auth dialog even if the project was previously authorized

### Step 5: Visual QA

Navigate to the target presentation, take a screenshot, and verify:
- Correct slide type layout
- Text is readable and properly positioned
- Colors match the brand
- No overlapping elements
- Footer is present

Fix any issues by editing the Apps Script and re-running.

## Content Guidelines

These limits keep slides readable. If content exceeds them, split into multiple slides.

| Slide Type | Max Content |
|------------|-------------|
| Title | 2 lines headline + 1 subtitle |
| Content + Bullets | 5 bullet items, each 1–2 lines |
| Multi-Column Cards | 4 cards, each with title + 2-line description |
| Stat Callout | 4 stat columns |

## Coordinate System

Google Slides default: **720 × 405 points** (10" × 5.625").

Standard margins and positions are defined in `references/slide-types.md`. The key principle: use consistent padding (36pt from edges) and consistent gaps (16pt between cards).

## Packaging

To create a shareable `.skill` file, **always `cd` into the skill folder first** so that `SKILL.md` is at the zip root (not nested inside subdirectories):

```bash
cd /path/to/amp-slide
zip -r /tmp/amp-slide.skill . -x "./evals/*"
```

The `.skill` format requires `SKILL.md` at the top level of the zip — not inside a subfolder.
