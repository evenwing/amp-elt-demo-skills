# Apps Script Reference for amp-doc

## Project Details

- **Project name**: Doc Builder
- **Project URL**: `https://script.google.com/u/0/home/projects/11utwLOqqSiVsGuNQIcxIDPAh5qhNR_QKm3DcVAIceO6wW6kG0Yb6GAJY/edit`
- **Dedicated to docs**: The `buildDoc()` function gets replaced each time

## DocumentApp API Quick Reference

### Creating / opening documents

```javascript
// New document
var doc = DocumentApp.create('My Document');
var body = doc.getBody();
Logger.log('URL: ' + doc.getUrl());

// Existing document (by URL)
var doc = DocumentApp.openByUrl('https://docs.google.com/document/d/XXXXX/edit');
var body = doc.getBody();
```

### Adding paragraphs

```javascript
// Simple paragraph
var para = body.appendParagraph('This is body text.');

// With heading style
var h1 = body.appendParagraph('Section Title');
h1.setHeading(DocumentApp.ParagraphHeading.HEADING1);

// Available headings:
// HEADING1, HEADING2, HEADING3, HEADING4, HEADING5, HEADING6, NORMAL, TITLE, SUBTITLE
```

### Text styling

```javascript
var para = body.appendParagraph('Styled text');
var text = para.editAsText();

// Full paragraph styling
text.setFontFamily('Poppins');
text.setFontSize(11);
text.setForegroundColor('#333333');
text.setBold(false);

// Partial styling (by character range)
text.setBold(0, 4, true);  // Bold first 5 characters
text.setForegroundColor(0, 4, '#1E61F0');  // Blue first 5 characters

// Line spacing
para.setLineSpacing(1.15);
para.setSpacingAfter(6);  // Points after paragraph
para.setSpacingBefore(12); // Points before paragraph
```

### Paragraph alignment

```javascript
para.setAlignment(DocumentApp.HorizontalAlignment.LEFT);
// Also: CENTER, RIGHT, JUSTIFY
```

### Lists

```javascript
// Bullet list
var item1 = body.appendListItem('First item');
item1.setGlyphType(DocumentApp.GlyphType.BULLET);
var item2 = body.appendListItem('Second item');
item2.setGlyphType(DocumentApp.GlyphType.BULLET);

// Numbered list
var item1 = body.appendListItem('Step one');
item1.setGlyphType(DocumentApp.GlyphType.NUMBER);
var item2 = body.appendListItem('Step two');
item2.setGlyphType(DocumentApp.GlyphType.NUMBER);

// Nested list (indent level)
item2.setNestingLevel(1);

// Style list items
item1.editAsText().setFontFamily('Poppins').setFontSize(11).setForegroundColor('#333333');
```

### Tables

```javascript
// Create table with data
var data = [
  ['Header 1', 'Header 2', 'Header 3'],
  ['Row 1 Col 1', 'Row 1 Col 2', 'Row 1 Col 3'],
  ['Row 2 Col 1', 'Row 2 Col 2', 'Row 2 Col 3']
];
var table = body.appendTable(data);

// Style header row
var headerRow = table.getRow(0);
for (var i = 0; i < headerRow.getNumCells(); i++) {
  var cell = headerRow.getCell(i);
  cell.setBackgroundColor('#F0F2F5');
  cell.editAsText()
    .setFontFamily('Poppins')
    .setBold(true)
    .setFontSize(11)
    .setForegroundColor('#000000');
}

// Style body rows
for (var r = 1; r < table.getNumRows(); r++) {
  var row = table.getRow(r);
  for (var c = 0; c < row.getNumCells(); c++) {
    row.getCell(c).editAsText()
      .setFontFamily('Poppins')
      .setFontSize(11)
      .setForegroundColor('#333333');
  }
}

// Table borders
table.setBorderWidth(0.5);
table.setBorderColor('#E0E0E0');

// Column widths (approximate — set via cell width)
// Note: DocumentApp doesn't have direct column width API.
// Widths adjust based on content. For control, pad with spaces or use fixed-width content.
```

### Horizontal rules

```javascript
body.appendHorizontalRule();
```

### Page breaks

```javascript
body.appendPageBreak();
```

### Images

```javascript
// From URL (must be publicly accessible or in same Drive)
var blob = UrlFetchApp.fetch('https://example.com/image.png').getBlob();
body.appendImage(blob);

// From Drive
var file = DriveApp.getFileById('FILE_ID');
body.appendImage(file.getBlob());

// Resize
var img = body.appendImage(blob);
img.setWidth(400);
img.setHeight(300);
```

### Setting document-wide defaults

```javascript
// Unfortunately, DocumentApp doesn't support setting default font globally.
// You must set font on each element individually.
// The helpers.gs.template provides wrapper functions to do this consistently.
```

### Clearing an existing document

```javascript
body.clear();
```

### Moving the cursor / inserting at specific positions

```javascript
// Insert paragraph at index
var para = body.insertParagraph(0, 'Inserted at top');

// Get child count
var numChildren = body.getNumChildren();
```

## Monaco Injection Technique

Same 3-phase approach as amp-slide. The only difference is the function name: use `buildDoc` instead of `buildSlide`.

> **CRITICAL**: `monaco.editor.getModels()[0].setValue()` does NOT work — it only updates the client-side Monaco model. Apps Script's change-detection layer does not recognize it as a real edit. The Save button stays disabled, and "Run" executes the old server-side code. You **must** use the keyboard trigger approach below.

### Quick summary:

1. Navigate to: `https://script.google.com/u/0/home/projects/11utwLOqqSiVsGuNQIcxIDPAh5qhNR_QKm3DcVAIceO6wW6kG0Yb6GAJY/edit`
2. Wait for Monaco: `typeof monaco !== 'undefined' && monaco.editor.getModels().length > 0`
3. **Phase A** — Disable auto-close and clear:
   ```javascript
   var editor = monaco.editor.getEditors()[0];
   editor.updateOptions({
     autoClosingBrackets: 'never', autoClosingQuotes: 'never',
     autoIndent: 'none', formatOnType: false, formatOnPaste: false,
     autoSurround: 'never', acceptSuggestionOnEnter: 'off',
     quickSuggestions: false, suggestOnTriggerCharacters: false
   });
   var model = editor.getModel();
   editor.setSelection(model.getFullModelRange());
   editor.trigger('keyboard', 'deleteAllLeft', null);
   ```
4. **Phase B** — Type the code: `editor.trigger('keyboard', 'type', { text: CODE_STRING });`
5. **Phase C** — Verify: `editor.getModel().getValue().length === CODE_STRING.length`
6. Save: `document.querySelector('[aria-label="Save project to Drive"]').click()` — verify `disabled === true` after 2-3 sec
7. Run: `document.querySelector('[aria-label="Run the selected function"]').click()`
8. Read log: check `document.querySelectorAll('[role="listitem"]')` for "Execution completed" or errors

### Code string construction

Use the `[...].join('\n')` array pattern for CODE_STRING — each line as a separate single-quoted element. This avoids apostrophe escaping issues that frequently break single-string approaches.

### Chrome extension disconnects

The extension occasionally disconnects mid-operation. Wait 3-5 seconds, check `model.getValue().length`, and retry Phase B if the content is empty or partial.

## Gotchas and Tips

### Font availability
- Poppins is a Google Font and is available in Google Docs by default
- `setFontFamily('Poppins')` works without any additional setup
- Always set font on every element — there's no "default font" setting in DocumentApp

### Heading styles
- `setHeading()` applies Google Docs' built-in heading styles
- These have their own default font/size which you must override with explicit styling
- Always call `setHeading()` FIRST, then apply font/size/color overrides

### List continuity
- Consecutive `appendListItem()` calls with the same glyph type automatically form a single list
- To start a separate list, insert a paragraph between them
- List items inherit styling independently — style each one

### Text ranges
- `editAsText()` returns the full text of an element as a `Text` object
- Range-based methods use (startOffset, endOffsetInclusive) — both are inclusive character indices
- `getText()` returns the plain string content

### Whitespace and spacing
- `setSpacingBefore()` and `setSpacingAfter()` are in points
- `setLineSpacing()` is a multiplier (1.0, 1.15, 1.5, 2.0)
- Default Google Docs spacing is 1.15 line spacing with 0pt before and 0pt after

### Authorization
- First run may require authorization for `DocumentApp` scope
- Same flow as amp-slide: Review permissions → Advanced → Go to project (unsafe) → Allow
- If the script already has Slides scope, Docs scope is an additional authorization
