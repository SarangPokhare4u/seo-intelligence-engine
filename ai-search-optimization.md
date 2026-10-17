# AI Search, AEO, and GEO

AEO/GEO are not separate Google ranking systems. Google states AI Overviews and AI Mode are built on core Search ranking and quality systems, and that foundational SEO applies (AI optimization guide, published 2026-05-15, updated 2026-07-10). Other platforms differ and must be researched individually.

## Contents
- Platform facts (verify at use time)
- What to do
- What not to do
- Audit procedure
- Measurement
- Disagreements to handle honestly

## Platform facts

| Platform | Eligibility / controls | Reporting | Source |
|---|---|---|---|
| Google AI Overviews / AI Mode | Indexed + snippet-eligible; no extra requirements; controls: nosnippet, data-nosnippet, max-snippet, noindex; Google-Extended does not control Search | Performance report ("Web" totals); Generative AI performance reports (June 2026, rolling out) | developers.google.com/search/docs/appearance/ai-features; ai-optimization-guide |
| Bing / Copilot | Bing Webmaster Guidelines include a GEO section (Feb 2026); NOARCHIVE blocks Copilot/grounding use, NOCACHE limits to URL/title/snippet; `data-nosnippet` respected; IndexNow for freshness | Bing WMT AI Performance report (public preview, Feb 2026): citations, cited pages, grounding queries; no clicks | blogs.bing.com/webmaster; bing.com/webmasters/help/webmaster-guidelines-30fba23a |
| ChatGPT search | OAI-SearchBot controls inclusion in search answers; GPTBot is training | Referral traffic in analytics (utm/source `chatgpt.com`) | platform.openai.com/docs/bots |
| Perplexity | PerplexityBot (index), Perplexity-User (user fetches) | Referrals in analytics | docs.perplexity.ai/guides/bots |

## What to do

1. Pass technical eligibility: crawlable, indexable, 200, snippet allowed, important text in HTML (not only images/PDF/tabs requiring interaction).
2. Answer-focused content gap analysis: list real user questions (PAA, sales calls, support, forums) and check whether the site answers each clearly.
3. Lead sections with a direct answer, then evidence, examples, and nuance (good for readers; not a Google requirement).
4. Provide information others would reference: original data, first-hand testing, clear comparisons, definitions, step-by-step processes, pricing transparency where possible.
5. Entity consistency: same company/product names, descriptions, and facts across site, Google Business Profile, Merchant Center, LinkedIn, directories, Wikipedia/Wikidata where legitimately applicable.
6. Credible citations to primary sources.
7. Multimodal: relevant original images and video with good metadata (see multimodal-search.md).
8. Structured data only for supported features and matching content.
9. Earn genuine mentions through digital PR and expertise (no inauthentic mention campaigns).

## What not to do

- Do not present llms.txt, special AI schema, chunking, or "AI-friendly rewriting" as Google requirements. Google's guide says they are not needed and Google Search ignores llms.txt. If a user wants llms.txt for other agents, say it is optional, unproven for retrieval (Ahrefs log data, June 2026: most llms.txt files received no requests), and harmless.
- Do not promise inclusion or citation.
- Do not create pages for each fan-out query variant (scaled content abuse).
- Do not attempt prompt injection, hidden text for AI, or manipulation of AI responses (spam policy for Google since 2026-05-15; Bing "Prompt Injection and AI Manipulation" section).

## Audit procedure

1. Pick 10-30 target queries (mix of informational and commercial).
2. For each: observe Google results (and AI features if visible), Bing/Copilot, and optionally ChatGPT/Perplexity answers if the user has access or the tools are available. Record date, market, cited sources. If a platform cannot be observed, write `not observed`.
3. Score each query: brand cited (Y/N/not observed), site URL cited, competitors cited, accuracy of brand facts in answers.
4. Map gaps to actions: missing answer content, weak evidence, entity inconsistency, technical blocks, lack of third-party mentions.
5. Measurement plan (below).

## Measurement

- Google: Search Console Performance (AI features included in Web totals), Generative AI performance reports where available, GA4 landing-page conversions for organic.
- Bing: AI Performance report (citations).
- AI referrals: GA4 session source contains `chatgpt.com`, `perplexity.ai`, `copilot.microsoft.com`, `gemini.google.com`, `claude.ai`. Build a custom channel group. Many AI clicks arrive without referrer; treat as undercounted.
- Do not compute "AI CTR" from reports that expose impressions or citations without clicks.

## Disagreements to handle honestly

- Click impact of AI Overviews: third-party studies range widely (Ahrefs Feb 2026: ~58% lower position-1 CTR; Seer Nov 2025: -61% organic CTR on informational AIO queries; Semrush Dec 2025: zero-click rate slightly lower after AIO appears; Pew Jul 2025: 8% vs 15% click rate). Google says organic click volume is relatively stable. Present as a range with methods, not a fact.
- Structure advice: Bing/Microsoft recommends Q&A blocks, tables, and schema; Google says no special structure or schema is needed. Apply per platform; good structure helps readers on all of them.
