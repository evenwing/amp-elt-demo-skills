---
name: slack-to-social
description: Slack sweep → tweet ideas mapped to your content themes
---

Search my Slack messages at [YOUR COMPANY] from the past 48 hours and give me 5 tweet ideas. Follow the instructions below carefully.

## Step 1: Search the right Slack channels

Focus searches on these channel categories (in priority order):

**Tier 1 — Core product & strategy (highest signal)**
- #your-core-product-channel — the team building your main product
- #your-analytics-channel — observability, evals, quality metrics
- #your-product-usage-channel — live usage, session replays, real customer stories
- DMs with key product/eng leaders

**Tier 2 — Developer experience & engineering practices**
- #devx-channel — debugging stories, tooling friction, AI-assisted development
- #security-channel — access control, governance, enterprise security
- #it-help-channel — tool adoption friction, integration requests

**Tier 3 — Product & go-to-market**
- #product-strategy-channel — product strategy, entitlements, packaging decisions
- #experimentation-channel — experimentation, feature flags, growth mechanics
- CRM bot summaries in deal channels (for customer adoption signals)

**Tier 4 — External links shared in Slack**
- Search for links to relevant industry sites shared by employees — these often spark the best discussions

Use 4-6 targeted searches mixing keyword and semantic queries. Skip pure ops/bot-noise channels.

## Step 2: Map insights to my content themes

Every tweet idea MUST map to one of these themes (these are the topics I write about and my audience expects):

1. **AI Evals & Product Quality** — How evals are becoming the new PM craft. Automated testing of AI products. The gap between benchmark evals and real-world quality. Why "vibes-based" shipping doesn't scale.

2. **Agentic UX & Design Patterns** — How AI agent interfaces actually work. Multi-step workflows. Human-in-the-loop patterns. The UX of autonomy and trust. What separates good agent products from chatbot wrappers.

3. **AI Agents vs. SaaS** — Will agents eat SaaS? How AI-native companies reach $100M ARR faster. The shift from CRUD apps to intelligent workflows. What incumbents should do.

4. **AI Pricing & Business Models** — Consumption vs. seat-based pricing for AI. Margin economics of inference costs. How AI changes the unit economics of software.

5. **Self-Improving Products / Autonomous PDLC** — Products that find and fix their own problems. Growth engineering agents. The product development lifecycle becoming autonomous. AI observability as a competitive advantage.

6. **AI in Practice (Honest Takes)** — What AI actually does well today vs. hype. Real engineering stories. The mundane but valuable uses of AI (debugging, dependency management, code review). Contrarian or surprising observations.

7. **Enterprise AI Adoption & Governance** — Security as the new bottleneck. MCP and managed integrations. How companies actually roll out AI tools. The tension between speed and control.

## Step 3: Draft the tweets

For each of the 5 tweet ideas:

**Tweet:** Write in my voice — confident, specific, data-driven, slightly witty. No hedging. Name real companies and real numbers when possible. Keep under 280 characters OR write a short thread (2-3 tweets max). Avoid AI-writing tells: no "transformative," "landscape," "notably," "delve," "game-changer."

**Inspiration:** Quote the specific Slack message(s) that inspired it — include the channel, who said it, and the key snippet.

**Theme:** Which of the 7 themes above this maps to.

**Why post:** 1-2 sentences on why this will resonate with my audience (AI product leaders, SaaS founders, VCs).

## Step 4: Scrub confidential data from tweets

Before saving, review every **Tweet** section and remove any Amplitude-confidential information. The **Inspiration** sections can keep internal details (they're my private notes), but the tweet text itself must be safe to post publicly. Apply these rules:

- **Customer names** → replace with generic descriptors like "a leading SaaS company," "a major media company," "a Fortune 500 customer"
- **Specific ARR / deal values** → replace with ranges like "7-figure ARR," "6-figure deal," "mid-six-figures"
- **Internal employee names** → remove or replace with role ("our head of engineering," "a senior PM")
- **Internal tool names or codenames** that aren't public → replace with generic terms like "our internal agent," "the eval pipeline"
- **Unreleased product details** — features, pricing, packaging that haven't been publicly announced → generalize or omit
- **Customer email addresses** → never include in tweet text

When in doubt, generalize. The tweet should read as an industry insight, not a leak.

## Output format

Save the output as a markdown file to the workspace folder at /sessions/*/mnt/Social/tweet-ideas-{date}.md