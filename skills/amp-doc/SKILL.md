---
name: amp-doc
description: >
  Create and edit native Google Docs in Amplitude's workspace using Google Apps Script. Use this skill whenever Sandhya asks to write a doc, create a document, draft a Google Doc, or produce any long-form written content that should live in Google Docs — even if she just says "write up X" or "make a doc about Y." Also use when she wants to edit, append to, or restyle an existing Google Doc. This skill outputs native Google Docs (NOT .docx files) by generating and running Apps Script code via Chrome.
---

# amp-doc

Create and edit native Google Docs using Apps Script, injected and run via Chrome. All docs use Poppins font throughout.

## When to Use

This skill creates or edits Google Docs in Amplitude's Google Workspace. Use it when:
- The user wants to create a new Google Doc
- The user wants to edit or append to an existing Google Doc (by URL)
- The deliverable is a Google Doc, not a local .docx file

If the user wants a local Word file, use the `docx` skill instead.

## Writing Quality

This is a writing skill first, Apps Script skill second. The quality of the prose matters as much as the formatting.

### Voice Principles
- **Clear and direct.** No filler, no passive voice, no jargon without payoff.
- **Structured for scanning.** Use headings, short paragraphs, and clear transitions.
- **Specific.** Name real things — companies, metrics, people, tools.
- **Concise.** Say it once, say it well. Cut anything that doesn't earn its place.

### Document Structure
1. **Title**: Bold, clear, descriptive — not clever for cleverness's sake
2. **Opening paragraph**: State the purpose and key takeaway upfront. No warm-up.
3. **Body sections**: Each headed section should make one clear point. Use subheadings if a section exceeds ~4 paragraphs.
4. **Closing**: End with next steps, a decision point, or a clear call to action — never a summary of what was just said.

### What to Avoid
- Hedging: "it might be argued," "arguably," "it's worth noting"
- AI tells: "pivotal," "transformative," "delve," "landscape," "notably," "furthermore"
- Walls of text without structure
- Generic closings: "The future looks bright," "only time will tell"

## Quick Reference

Read the detailed reference files as needed:
- `references/apps-script-docs-reference.md` — DocumentApp API patterns, Monaco injection technique, and gotchas
- `scripts/helpers.gs.template` — Reusable helper functions for common formatting operations

## Typography

All Poppins, all the time. No other fonts.

| Element | Font | Weight | Size |
|---------|------|--------|------|
| Title | Poppins | Bold | 24pt |
| Heading 1 | Poppins | Bold | 18pt |
| Heading 2 | Poppins | Bold | 14pt |
| Heading 3 | Poppins | SemiBold | 12pt |
| Body | Poppins | Regular | 11pt |
| Caption / footnote | Poppins | Regular | 9pt |

**Colors**: Body text `#333333`, Headings `#000000`, Accent/links `#1E61F0` (Amplitude Blue).

## First-Time Setup

New users only need to be logged into Google with Claude in Chrome. The skill handles everything else automatically.

### What happens on first run

1. The skill navigates to `https://script.google.com/home` via Chrome
2. Creates a new Apps Script project named "Doc Builder"
3. Injects the full starter code (helpers + placeholder `buildDoc()`)
4. Saves the project
5. Stores the new project URL for future use

### Setup detection

Before injecting code, check whether the user already has a Doc Builder project configured:

1. Check if a project URL is stored in the skill's reference data or conversation context
2. If yes → navigate directly to that project and proceed
3. If no → run the first-time setup flow below

### First-time setup flow

```
Step 1: Navigate to https://script.google.com/home via Chrome
Step 2: Click "New project" (or the + button)
Step 3: Wait for the Monaco editor to load
Step 4: Rename the project to "Doc Builder" (click the title area at top-left)
Step 5: Inject the FULL starter code (see "Code Injection Rule" below)
Step 6: Save with Ctrl+S
Step 7: Store the project URL from the browser address bar for future use
Step 8: Tell the user: "Your Doc Builder is set up. I'll use this project going forward."
```

After first-time setup, the user's project URL replaces the default URL in all subsequent runs.

## End-to-End Workflow

### Step 1: Parse the request

Determine what kind of document is needed. Extract the content, structure, and any specific requirements. If the user wants to edit an existing doc, get the URL.

### Step 2: Write the content

Draft the full document content first. Think about structure, clarity, and flow. Apply the writing quality principles above. This is the most important step.

### Step 3: Generate Apps Script code

Write a `buildDoc()` function. The function should:

**For a new document:**
```javascript
var doc = DocumentApp.create('Document Title');
var body = doc.getBody();
// ... build the document
Logger.log('Document URL: ' + doc.getUrl());
```

**For an existing document:**
```javascript
var doc = DocumentApp.openByUrl('USER_PROVIDED_URL');
var body = doc.getBody();
// ... edit the document
```

Use the helper patterns from `scripts/helpers.gs.template` for consistent formatting.

### Step 4: Inject + run via Chrome

1. Navigate to the Apps Script project (stored URL, or default: `https://script.google.com/u/0/home/projects/11utwLOqqSiVsGuNQIcxIDPAh5qhNR_QKm3DcVAIceO6wW6kG0Yb6GAJY/edit`)
2. Wait for the Monaco editor to load (check for `monaco.editor.getModels()` to be available)
3. Inject the **FULL file** using the **3-phase keyboard trigger approach**:
   - **Phase A**: Disable auto-closing brackets/quotes, select all, delete via keyboard trigger
   - **Phase B**: Type the new code via `editor.trigger('keyboard', 'type', { text: CODE_STRING })`
   - **Phase C**: Verify `model.getValue().length === CODE_STRING.length`

   > ⚠️ **Do NOT use `monaco.editor.getModels()[0].setValue()`** — it only updates the client-side editor and does not trigger Apps Script's change detection. The Save button stays disabled and "Run" will execute the old server-side code.

   > **Code string construction**: Build CODE_STRING using the `[...].join('\n')` array pattern — each line as a separate single-quoted array element. This avoids apostrophe and escaping issues. See the amp-slide reference for detailed examples.

4. Save: Click `document.querySelector('[aria-label="Save project to Drive"]').click()` and verify `disabled === true` after 2–3 seconds. Do NOT use Ctrl+S — it's unreliable when dispatched from JavaScript.
5. Run: Click `document.querySelector('[aria-label="Run the selected function"]').click()` to run `buildDoc`
6. Read execution log: Query `document.querySelectorAll('[role="listitem"]')` and check for "Execution completed" or "Error"
7. Handle authorization dialog if it appears (first time per new scope)

### Step 5: Verify

Navigate to the created/edited Google Doc and verify:
- Content is correct and complete
- All text uses Poppins font
- Headings are properly styled
- Spacing and structure look clean

Share the doc URL with the user.

## Code Injection Rule

**CRITICAL: Always inject the FULL file — helpers + buildDoc() together.**

Never inject just a `buildDoc()` function or just test functions by themselves. Every injection must include:

1. Constants block (colors, typography)
2. All helper functions (`styleText`, `addTitle`, `addH1`, `addH2`, `addH3`, `addParagraph`, `addBulletList`, `addNumberedList`, `addTable`, `addHorizontalRule`, `addCaption`, `addImage`)
3. Edit helpers (`openDoc`, `clearAndRebuild`, `setPoppinsDefault`, `replaceText`, `findAndStyle`)
4. The `buildDoc()` function (this is the only part that changes per task)

The complete starter code is in `scripts/helpers.gs.template`. When generating code for a task, read that file, copy everything above `buildDoc()`, then append your custom `buildDoc()` at the bottom.

**Why:** The Apps Script project has a single code file. `setValue()` replaces the entire file contents. If you only inject `buildDoc()`, all the helper functions disappear and the script breaks. If you inject test code without helpers, the original Doc Builder is destroyed.

## Content Guidelines

### Maximum lengths (before splitting into multiple docs)
- Single doc should stay under ~3000 words for readability
- If content is longer, consider splitting into sections with a table of contents

### Formatting patterns

**Bullet lists**: Use `ListItem` with `GlyphType.BULLET`. Keep to 5-7 items max per list.

**Numbered lists**: Use `ListItem` with `GlyphType.NUMBER`. Use for sequential steps or ranked items.

**Tables**: Use for structured data. Keep columns to 4 or fewer. Header row should be bold with light grey background.

**Horizontal rules**: Use sparingly to separate major sections.

## Packaging

To create a shareable `.skill` file:

```bash
cd /path/to/amp-doc
zip -r /tmp/amp-doc.skill . -x "./evals/*"
```
