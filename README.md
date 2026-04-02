# Amplitude ELT Demo Skills

Custom [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills and scheduled tasks built for Amplitude workflows. These are real production examples — use them as templates for your own Claude Code automations.

## Skills

| Skill | Description |
|-------|-------------|
| **[amp-carousel](skills/amp-carousel/)** | Generate LinkedIn carousel slides (1080x1080 PNGs) in Amplitude's brand style. Uses a Python script with PIL to render title, stat, text, grid, checklist, timeline, cards, and CTA slide types. |
| **[amp-slide](skills/amp-slide/)** | Create native Google Slides in Amplitude's brand style via Google Apps Script. Supports 8 slide types with pixel-level layout specs, injected through Chrome's Monaco editor. |
| **[amp-doc](skills/amp-doc/)** | Create and edit native Google Docs in Amplitude's workspace using Apps Script. Includes helper functions for typography, lists, tables, and document structure. |

## Scheduled Tasks

| Task | Schedule | Description |
|------|----------|-------------|
| **[slack-todo-extractor](scheduled-tasks/slack-todo-extractor.md)** | Daily | Scans Slack for action items directed at you — direct requests, commitments you made, assigned tasks, follow-ups needed. Outputs a prioritized markdown checklist grouped by urgency (Overdue/Today, This Week, Later) with 7-day archive retention. |
| **[slack-to-social](scheduled-tasks/slack-to-social.md)** | Daily | Sweeps internal Slack channels for insights, maps them to your content themes, and drafts 5 tweet ideas. Includes built-in confidentiality scrubbing so tweets are safe to post publicly. |

## Brand Assets

`amp-brand.zip` contains Amplitude's brand kit — logos (PNG, SVG, EPS, AI), color palettes (RGB + CMYK), and guidelines for fonts, voice, writing, and graphic elements.

## Setup

### Skills

1. Clone this repo
2. Copy the skill folder(s) you want into your Claude Code project's `.claude/skills/` directory
3. The skills will be available in your next Claude Code session

**amp-carousel** requires Python 3 with PIL/Pillow and the Poppins font installed.

**amp-slide** and **amp-doc** require:
- A Google account with Apps Script access
- A "Slide Builder" or "Doc Builder" Apps Script project (see the README in each skill)
- The Claude in Chrome MCP server for Monaco editor injection

### Scheduled Tasks

1. Copy the `.md` file contents into a new Claude Code scheduled task
2. Replace the placeholder values (`YOUR_SLACK_USER_ID`, `your-username`, `your-email@company.com`) with your own
3. Customize the Slack channels and content themes to match your workflow
4. Requires the Slack MCP server connected to your workspace

## License

These skills are provided as-is for educational and demonstration purposes.
