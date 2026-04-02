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

For each of the 5 tweet ideas, produce these sections:

**Tweet:** Draft the actual tweet text following the voice rules below. Keep to a single tweet (under 280 chars) for a punchy take. Use a 2-3 tweet thread ONLY when there's a real narrative arc — a setup, a surprising turn, and a payoff. Never thread just to fit more words.

**Inspiration:** Quote the specific Slack message(s) that inspired it — include the channel, who said it, and the key snippet.

**Theme:** Which of the 7 themes above this maps to.

**Why post:** 1-2 sentences on why this will resonate with my audience (AI product leaders, SaaS founders, VCs).

### Voice rules — follow these strictly

**Case & grammar:** mostly lowercase. not aggressively so — capitalize proper nouns, product names, acronyms — but default to lowercase for everything else including the start of sentences. imperfect grammar is fine and encouraged. sentence fragments, trailing off with "..." are good. this should read like someone typing fast with a thought they need to get out.

**Emojis:** use a few emojis sparingly but naturally. :( and 😤 for frustration, 🔥 for something exciting, etc. never more than 2-3 per tweet. they should feel like punctuation, not decoration.

**Sentence structure:** mix very short fragments with longer run-on thoughts connected by "..." or "and" or just line breaks. sometimes a sentence is just one word. sometimes it's a whole paragraph stitched together with no periods. match the energy of the thought — tight when making a sharp point, rambling when thinking through an idea.

**Tone:** thinking out loud. like you're texting a smart friend about something you just noticed. not performing for an audience. not trying to sound authoritative. just... saying the thing. sometimes frustrated, sometimes excited, always honest.

**Specificity:** name real companies, real products, real tools. "many companies" is weak. "Cursor" or "Claude Code" or "Stripe" is strong. After drafting, run through the confidentiality filter in Step 4 for internal data.

**Parenthetical asides:** keep the dry, self-aware asides but make them feel more casual. "(remember those?)" still works. "(lol)" works too. don't force them.

**Endings:** can trail off, can land hard, can just... stop. don't wrap things up neatly. definitely never end with "food for thought" or "what do you think?" — but ending mid-thought or with a strong opinion is great.

**What NOT to sound like:** a thought leader crafting a Perfect Tweet. no polished setups. no "here's what I learned" framing. no clean narrative arcs unless the idea genuinely has one. this is not a TED talk, it's a group chat.

**Reference examples — study these closely and match the vibe:**

> getting frustrated when Claude CoWork behaves differently from Code because my entire mental model for AI work is now based on the latter...   :(
> If we are going to lean heavily on GitHub and .md filesystems for everything we need more consistent UX around plugins and authentication flows.

> It makes little sense to be an indie software developer selling subscriptions to point SaaS solutions anymore...Completely out of vogue and not fun to maintain. Too much SaaS tool bloat in the ecosystem and personal software is the future.   But not everyone will build their own. Open source + bring-your-own-key is the way for most use cases that are on-demand tasks. If it's a background agent/always on task, maybe use stripe's new LLM billing method to offer a fully hosted solution with a good open source API.

### AI-writing tells — NEVER use these

**Significance inflation:** "pivotal moment," "transformative potential," "marks a new era," "testament to"
**Vague attributions:** "experts believe," "studies show," "many have noted"
**Superficial -ing analyses:** "symbolizing," "reflecting," "showcasing," "underscoring"
**Promotional language:** "nestled within," "breathtaking," "groundbreaking," "revolutionary," "game-changer"
**Formulaic framing:** "Despite challenges, X continues to thrive"
**AI vocabulary:** "additionally," "furthermore," "notably," "it's worth noting," "landscape," "realm," "delve into"
**Copula avoidance:** "serves as," "functions as," "stands as," "acts as" — just say "is"
**Negative parallelisms:** "It's not just X, it's Y" — state the point directly
**Forced rule of three:** "innovation, inspiration, and impact" — use the natural number of items
**Synonym cycling:** Don't vary word choice just to avoid repetition. Use the clearest word each time.
**Generic conclusions:** "The future looks bright," "exciting times lie ahead," "only time will tell"
**Hedging:** "it might be argued," "arguably," "it's worth noting," "could potentially"
**Corporate buzzwords:** "leverage," "unlock value," "drive impact," "move the needle," "synergy"
**Overly polished tone:** anything that sounds like it was workshopped. if it reads like a LinkedIn post, rewrite it.

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

Save the output as a markdown file to `Social/tweet-ideas-{date}.md` in the workspace root.