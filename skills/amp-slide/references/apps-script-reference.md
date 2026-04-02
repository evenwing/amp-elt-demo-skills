# Apps Script Reference for amp-slide

## Project Details

- **Project name**: Slide Builder
- **Project URL**: `` ← Replace with your Apps Script project URL (auto-populated by first-run setup)
- **Reused for every slide**: The `buildSlide()` function gets replaced each time

> **Note**: If the Project URL above is empty or contains a placeholder, the skill will automatically create a new Apps Script project and fill this in during the first run. See the "First-Run Setup" section in SKILL.md.

## SlidesApp API Quick Reference

### Creating / opening presentations

```javascript
// New presentation
var pres = SlidesApp.create('My Presentation');
var slide = pres.getSlides()[0];  // First slide already exists
Logger.log('URL: ' + pres.getUrl());

// Existing presentation (by URL)
var pres = SlidesApp.openByUrl('https://docs.google.com/presentation/d/XXXXX/edit');
var slide = pres.appendSlide(SlidesApp.PredefinedLayout.BLANK);
```

### Setting background color

```javascript
slide.getBackground().setSolidFill('#000000');
```

### Creating shapes

```javascript
// Rectangle
var rect = slide.insertShape(SlidesApp.ShapeType.RECTANGLE, x, y, width, height);
rect.getFill().setSolidFill('#FFFFFF');
rect.getBorder().setTransparent();  // No border

// Rounded rectangle
var card = slide.insertShape(SlidesApp.ShapeType.ROUND_RECTANGLE, x, y, width, height);
card.getFill().setSolidFill('#FFFFFF');
card.getBorder().setTransparent();
// Note: corner radius is automatic for ROUND_RECTANGLE. There's no direct API to set it.
// For tighter control, use multiple shapes.

// With border
card.getBorder().getLineFill().setSolidFill('#E0E0E0');
card.getBorder().setWeight(1);
```

### Adding text

```javascript
// Text box
var tb = slide.insertShape(SlidesApp.ShapeType.TEXT_BOX, x, y, width, height);
tb.getText().setText('Hello World');
tb.getText().getTextStyle()
  .setFontFamily('Poppins')
  .setBold(true)
  .setFontSize(28)
  .setForegroundColor('#FFFFFF');

// Alignment
tb.setContentAlignment(SlidesApp.ContentAlignment.TOP);  // TOP, MIDDLE, BOTTOM

// Text alignment (horizontal)
tb.getText().getParagraphStyle().setParagraphAlignment(SlidesApp.ParagraphAlignment.CENTER);
// Also: START, END, JUSTIFIED
```

### Multi-line text with different styles

```javascript
var tb = slide.insertShape(SlidesApp.ShapeType.TEXT_BOX, x, y, w, h);
var text = tb.getText();
text.setText('→ First item\n→ Second item\n→ Third item');
text.getTextStyle()
  .setFontFamily('Poppins')
  .setFontSize(14)
  .setForegroundColor('#333333');
```

### Removing default elements

When working with an existing slide that has default elements:

```javascript
var elements = slide.getPageElements();
for (var i = elements.length - 1; i >= 0; i--) {
  elements[i].remove();
}
```

## Monaco Injection Technique

The key technique for getting code into Apps Script from Chrome.

> **CRITICAL**: `monaco.editor.getModels()[0].setValue()` only updates the client-side Monaco model — Apps Script's internal change-detection layer does **not** recognize it as a real edit. The Save button stays disabled, and "Run" executes the old server-side code. You **must** use the `editor.trigger('keyboard', ...)` approach described below.

### Step 1: Navigate to the project

```
https://script.google.com/u/0/home/projects/1paYh6v-UNPnBS-MGJ5JpFIhHHrKH1FnD8NhDWi97ePZAYVju57j7jyRn/edit
```

### Step 2: Wait for Monaco to load

The Monaco editor takes a few seconds to initialize. Wait for the page to fully load, then verify Monaco is available by running JavaScript:

```javascript
typeof monaco !== 'undefined' && monaco.editor.getModels().length > 0
```

### Step 3: Inject the code (three-phase approach)

**Phase A — Disable auto-close and clear the editor:**

Monaco's auto-closing brackets/quotes will insert extra `}`, `)`, `'` characters when code is typed in. Disable all auto-insertion features first, then select-all and delete using a keyboard trigger (so Apps Script detects the change):

```javascript
var editor = monaco.editor.getEditors()[0];
editor.updateOptions({
  autoClosingBrackets: 'never',
  autoClosingQuotes: 'never',
  autoIndent: 'none',
  formatOnType: false,
  formatOnPaste: false,
  autoSurround: 'never',
  acceptSuggestionOnEnter: 'off',
  quickSuggestions: false,
  suggestOnTriggerCharacters: false
});
var model = editor.getModel();
editor.setSelection(model.getFullModelRange());
editor.trigger('keyboard', 'deleteAllLeft', null);
```

**Phase B — Type the new code:**

```javascript
editor.trigger('keyboard', 'type', { text: CODE_STRING });
```

**Phase C — Verify length matches:**

```javascript
editor.getModel().getValue().length === CODE_STRING.length
// If they don't match, auto-close was still active — repeat from Phase A
```

**Critical**: The CODE_STRING must be a valid JavaScript string. Use JSON.stringify() on the code string for proper escaping.

### Step 4: Save

Click the Save button via JavaScript:

```javascript
document.querySelector('[aria-label="Save project to Drive"]').click();
```

Then wait 3–4 seconds and verify the save completed by checking the button is disabled:

```javascript
document.querySelector('[aria-label="Save project to Drive"]').disabled
// true = saved successfully, false = still unsaved (possible syntax error)
```

> **Why not Ctrl+S?** Dispatching `KeyboardEvent` for Ctrl+S from JavaScript doesn't reliably trigger Apps Script's save handler. Clicking the button directly is more reliable.

### Step 5: Run

Click the Run button via JavaScript:

```javascript
document.querySelector('[aria-label="Run the selected function"]').click();
```

Wait 8–12 seconds, then check the execution log for success. The function dropdown should show `buildSlide`.

### Step 6: Verify execution

Read the execution log panel. Look for:
- `"Execution started"` + `"Execution completed"` = success
- The `Logger.log()` output confirming the correct presentation URL
- If the log shows output from an *old* function (e.g., `DriveApp.getFilesByName` instead of your new code), the save in Step 4 didn't actually persist — re-run from Step 3.

### Authorization & OAuth Scopes

Different SlidesApp methods require different OAuth scopes:

| Method | Scope | Trigger |
|--------|-------|---------|
| `SlidesApp.create()` | `https://www.googleapis.com/auth/presentations` | First time creating a presentation |
| `SlidesApp.openByUrl()` | `https://www.googleapis.com/auth/presentations` + `https://www.googleapis.com/auth/drive` | First time opening an existing presentation |

When a script requires a new scope that wasn't previously authorized, Google shows an "Authorization required" dialog:

1. "Authorization required" → Click **"Review permissions"**
2. Choose the Google account
3. "This app isn't verified" → Click **"Advanced"** → **"Go to Slide Builder (unsafe)"**
4. Click **"Allow"**

**Important**: If the script was previously authorized only for `create()` (which needs just `presentations` scope), switching to `openByUrl()` will trigger a **new** authorization dialog because it additionally requires the `drive` scope. This is expected — the user needs to grant the additional scope.

After authorization, subsequent runs with the same scope don't need re-authorization.

## Chrome Execution Workflow

The full workflow for programmatically interacting with Apps Script from Claude in Chrome.

### Tab management

Keep two Chrome tabs open throughout a session:
1. **Apps Script editor** — for code injection, save, and run
2. **Google Slides presentation** — for visual verification after each run

Always start with `tabs_context_mcp` to get current tab IDs. Store them so you can switch between the editor (for injection) and the presentation (for screenshots).

### Splitting injection across tool calls

Run Phase A (disable auto-close + clear) as one `javascript_tool` call, then Phase B + C (type + verify) as a separate call. This is safer than combining all three — if the Chrome extension disconnects mid-operation during a large type, you can check `model.getValue().length` and retry just Phase B.

### Code string construction

**Use the `[...].join('\n')` array pattern** instead of a single escaped string. Each line is a separate array element in single quotes. This avoids problems with:
- Apostrophes in comments (e.g., `Can't` breaks single-quote strings)
- Nested quote escaping
- Unicode escapes being interpreted at the wrong level

```javascript
var code = [
'function buildSlide() {',
'  var pres = SlidesApp.openByUrl("...");',
'  var slide = pres.appendSlide(SlidesApp.PredefinedLayout.BLANK);',
'  // ... build the slide',
'  Logger.log("Done: " + pres.getUrl());',
'}'
].join('\n');

var editor = monaco.editor.getEditors()[0];
editor.trigger('keyboard', 'type', { text: code });
[code.length, editor.getModel().getValue().length];
```

### Reading the execution log

After clicking Run and waiting 5–8 seconds, read the log with:

```javascript
var items = document.querySelectorAll('[role="listitem"]');
var result = [];
items.forEach(function(el) {
  var t = el.textContent.trim();
  if (t.includes('Notice') || t.includes('Info') || t.includes('Error'))
    result.push(t);
});
result.slice(-3).join(' | ');
```

A successful run shows three entries: `Execution started`, your `Logger.log` output, and `Execution completed`. If you see `Error`, read the message for the stack trace.

### Chrome extension disconnects

The Claude in Chrome extension occasionally disconnects mid-operation (Chrome service worker restart). When this happens:
1. Wait 3–5 seconds for auto-reconnect
2. Check `model.getValue().length` — if 0 or partial, the type command didn't complete
3. Re-run from Phase A (disable + clear + type)
4. If the length matches your code length, the injection succeeded despite the disconnect — proceed to save

### Visual verification

After execution completes, switch to the Slides tab and:
1. Click the target slide in the filmstrip
2. Take a `screenshot` to check overall layout
3. Use `zoom` on specific regions to check small text or alignment
4. Fix any issues by editing the Apps Script and re-running

## Lines and Connectors

### insertLine (for connecting lines, decorative elements)

```javascript
var line = slide.insertLine(
  SlidesApp.LineCategory.STRAIGHT,
  startLeft,  // x1
  startTop,   // y1
  endLeft,    // x2
  endTop      // y2
);
line.getLineFill().setSolidFill('#FFFFFF');
line.setWeight(1.5);  // in points
```

> **Important**: The signature is `(LineCategory, x1, y1, x2, y2)` with five numeric arguments. Do NOT use `{left, top}` objects — that signature does not exist and throws a parameter mismatch error.

### Line styling

```javascript
line.getLineFill().setSolidFill('#8AADFF');  // color
line.setWeight(0.75);  // thickness in points

// Dashed borders on shapes (not lines)
shape.getBorder().setDashStyle(SlidesApp.DashStyle.DOT);
// Also: DASH, DASH_DOT, LONG_DASH, LONG_DASH_DOT, SOLID
```

### Decorative network graphics

Complex decorative elements (constellation networks, node graphs) can be built entirely from native Slides shapes — no image uploads needed. The pattern:

1. Define nodes as `[x, y, radius]` arrays
2. Define connections as `[fromIdx, toIdx, weight]` arrays
3. Draw lines first (they render behind shapes)
4. Draw ellipses on top as nodes
5. Use color hierarchy: white for central hub, lighter blues (`#C2D4FA`, `#A8C4FF`, `#8AADFF`) for progressively smaller/distant nodes

```javascript
// Dotted orbit rings
var ring = slide.insertShape(SlidesApp.ShapeType.ELLIPSE, cx-r, cy-r, r*2, r*2);
ring.getFill().setTransparent();
ring.getBorder().getLineFill().setSolidFill('#8AADFF');
ring.getBorder().setWeight(0.75);
ring.getBorder().setDashStyle(SlidesApp.DashStyle.DOT);
```

## In-Place Slide Editing

To modify an existing slide without deleting and re-appending it:

```javascript
var slide = pres.getSlides()[4];  // 0-indexed

// Remove all elements
var elements = slide.getPageElements();
for (var i = elements.length - 1; i >= 0; i--) {
  elements[i].remove();
}

// Re-draw from scratch
slide.getBackground().setSolidFill('#1E61F0');
// ... add new shapes
```

This preserves the slide's position in the deck and avoids reordering issues.

## Gotchas and Tips

### Coordinate system
- Origin (0,0) is top-left of the slide
- Units are points (72 points = 1 inch)
- Default slide: 720 × 405 points (10" × 5.625")
- Shapes positioned with (left, top, width, height)

### Text in shapes
- Text added to any shape (not just TEXT_BOX) appears centered by default
- Use `setContentAlignment()` for vertical positioning
- Use `getParagraphStyle().setParagraphAlignment()` for horizontal

### Shape borders
- New shapes have a default border — always set `.getBorder().setTransparent()` explicitly if you don't want one
- For colored borders: `.getBorder().getLineFill().setSolidFill(color)` + `.getBorder().setWeight(pts)`

### No gradient fills in SlidesApp
- `setSolidFill()` is the only fill type available
- For gradient effects, use adjacent shapes with different colors

### No corner radius control
- `ROUND_RECTANGLE` has an automatic corner radius that scales with shape size
- For small shapes (pills), this works well — ends up looking fully rounded
- For large shapes, the radius is proportionally subtle

### Image insertion
- `slide.insertImage(imageUrl)` requires a publicly accessible URL
- Can also use `slide.insertImage(blob)` with a Blob from DriveApp
- Out of scope for v1 but worth noting for future

### Line shapes for dividers
```javascript
var line = slide.insertShape(SlidesApp.ShapeType.RECTANGLE, x, y, width, 1);
line.getFill().setSolidFill('#666666');
line.getBorder().setTransparent();
```

### Monaco setValue() does NOT save (critical!)
- `monaco.editor.getModels()[0].setValue()` updates the editor UI but does NOT trigger Apps Script's internal change-detection layer
- The Save button remains disabled after `setValue()` — meaning the server-side code is unchanged
- When you click "Run", Apps Script executes the **server-side** version, not what's visible in the editor
- **Always use** `editor.trigger('keyboard', 'type', { text: code })` instead — this simulates real keyboard input and triggers change detection
- See the "Monaco Injection Technique" section above for the full 3-phase injection approach

### Monaco auto-closing brackets
- Monaco automatically inserts matching `}`, `)`, `'`, `"` when you type an opening bracket/quote
- When using `editor.trigger('keyboard', 'type', ...)` to inject code, this results in **duplicate closing characters** throughout the code, causing syntax errors
- **Always disable** auto-closing features before injecting: `editor.updateOptions({ autoClosingBrackets: 'never', autoClosingQuotes: 'never', ... })`
- After typing, verify `model.getValue().length === code.length` to confirm no extra characters were inserted

### Bar chart overflow

When building horizontal bar charts inside a card, calculate layout bounds before choosing the max bar width:

```
barX + maxBarW + gap + valueLabelW < cardRight
```

The longest bar (100%) must leave room for its value label (e.g., "599K (60%)"). A common safe setup inside a 648-wide card: `labelX=52, barX=210, maxBarW=250, valueLabelW=130` — keeps everything within bounds.

### Performance
- Each SlidesApp call is a remote API call, so scripts with many shapes take a few seconds
- A typical slide with 15–25 shapes runs in 1–3 seconds
- Scripts with many decorative elements (50+ shapes for a constellation network) still run in 1–2 seconds
- Logging with `Logger.log()` helps debug positioning issues
