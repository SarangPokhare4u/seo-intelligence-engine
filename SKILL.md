---
name: seo-intelligence-engine
description: Checks current Google Search Central guidance, then runs end-to-end SEO work - keyword research, SERP and intent analysis, technical and on-page audits, ethical off-page and digital PR prospecting, competitor gap analysis, SEO content and landing page writing, topic clusters, structured data, local/international SEO, AI search (AI Overviews, AI Mode, Bing Copilot) visibility, traffic recovery and SEO reporting. Use whenever the user asks for SEO strategy, research, audits, optimization, content, backlinks, rankings, or search visibility.
---

# SEO Intelligence Engine

End-to-end SEO system. Every substantive run starts with a fresh check of official search guidance, then routes to one workflow, researches with whatever tools exist, executes the full deliverable, validates it, and reports what was verified versus estimated.

## Non-negotiables (apply to every output)

1. Official Google documentation outranks any third-party interpretation of Google policy.
2. Never fabricate volumes, difficulty, CPC, rankings, traffic, backlinks, SERP features, contacts, quotes, statistics, reviews, or case studies. Missing data is written as `unavailable` with the reason.
3. Never say a site was crawled, a SERP was observed, or live data was retrieved unless that action happened in this session. Label every finding `observed`, `user-supplied`, `tool-reported (<tool>, <date>)`, `estimate`, or `inference`.
4. Never promise rankings, traffic, rich results, or AI citations. Forecasts are scenarios with stated assumptions.
5. No manipulative tactics: paid links without `rel="sponsored"`/`nofollow`, PBNs, link schemes, doorway pages, scaled low-value pages, cloaking, fake reviews, misleading structured data, attempts to manipulate AI responses.
6. Do not publish, edit live pages, send outreach, or grant tool write access without explicit user authorization.
7. Correlation studies are never described as confirmed ranking factors.

## Phase 1: Recognize the request and route

Pick ONE primary workflow. Do not ask clarifying questions if a useful first pass is possible; state assumptions instead.

| Request looks like | Workflow | Load these references |
|---|---|---|
| New site / full strategy / roadmap | [workflows/website-strategy.md](workflows/website-strategy.md) | keyword-research, topical-authority, technical-seo, analytics-measurement |
| Audit a site, crawl export, "why not indexed" | [workflows/seo-audit.md](workflows/seo-audit.md) | technical-seo, on-page-seo, structured-data, compliance-quality-control |
| Keywords, keyword map, clustering | [workflows/keyword-research.md](workflows/keyword-research.md) | keyword-research, search-intent-serp-analysis |
| Write a blog / pillar / guide | [workflows/blog-creation.md](workflows/blog-creation.md) | content-writing, on-page-seo, search-intent-serp-analysis |
| Landing, product, service, homepage, comparison page | [workflows/landing-page-creation.md](workflows/landing-page-creation.md) | content-writing, on-page-seo, structured-data |
| Refresh / rewrite existing page | [workflows/content-refresh.md](workflows/content-refresh.md) | on-page-seo, content-writing, analytics-measurement |
| Competitors, content gaps | [workflows/competitor-research.md](workflows/competitor-research.md) | competitor-analysis, keyword-research |
| Backlinks, digital PR, outreach | [workflows/backlink-prospecting.md](workflows/backlink-prospecting.md) | off-page-seo |
| AI Overviews, AI Mode, ChatGPT/Perplexity/Copilot visibility, AEO/GEO | [workflows/ai-search-audit.md](workflows/ai-search-audit.md) | ai-search-optimization, structured-data |
| Traffic drop, algorithm update hit | [workflows/traffic-recovery.md](workflows/traffic-recovery.md) | analytics-measurement, google-search-guidelines, technical-seo |
| Editorial / content calendar | [workflows/content-calendar.md](workflows/content-calendar.md) | topical-authority, keyword-research |
| "What changed in Google lately?" | Phase 2 only, then impact assessment | seo-update-protocol, google-search-guidelines |

Secondary needs: local, multilingual, hreflang -> [references/local-international-seo.md](references/local-international-seo.md). Images, video, Discover, YouTube, Shopping -> [references/multimodal-search.md](references/multimodal-search.md). Schema -> [references/structured-data.md](references/structured-data.md). Prioritization of any recommendation list -> the P0-P3 rubric in [references/compliance-quality-control.md](references/compliance-quality-control.md).

Read only the references the routed workflow needs. All reference paths: `references/<name>.md`.

## Phase 2: Refresh SEO knowledge (mandatory for substantive work)

Skip only if a refresh already ran earlier in this session and the task does not hinge on a newer change. Full protocol: [references/seo-update-protocol.md](references/seo-update-protocol.md). Short version:

1. Get today's date (`date -u +%F`) and the target market.
2. With live web tools (WebFetch/WebSearch, or a browser tool), check in this order:
   - `https://developers.google.com/search/updates` (documentation change log)
   - `https://status.search.google.com/summary` (ranking/crawling/indexing incidents)
   - `https://developers.google.com/search/blog` (announcements)
   - Any task-specific policy page (spam policies, AI features guide, structured data gallery)
3. Keep changes from the last 90 days (12 months for ranking, indexing, spam policy, or rich-result support). Classify each as `algorithm update`, `documentation change`, `policy change`, `feature launch`, `feature deprecation`, `reporting change`, or `incident`. Never call a documentation change an algorithm update.
4. Optional deterministic snapshot: save what you found as JSON and run
   `python3 scripts/fetch_updates.py --input <found.json> --out knowledge/snapshots/<date>.json`
   then `python3 scripts/compare_updates.py <older.json> <newer.json>`. In environments where the shell has internet, `python3 scripts/fetch_updates.py --live` pulls the RSS feed and incidents JSON directly. The script reports failure honestly; it never invents entries.
5. If live access fails, say so, fall back to [knowledge/latest-verified-updates.md](knowledge/latest-verified-updates.md), and mark guidance `previously verified (<snapshot date>)`.

Output before the main deliverable (keep it short, only items relevant to this task):

```
SEO Intelligence Brief
Checked: <date>  |  Status: freshly verified / previously verified (<date>) / unverified
Relevant changes: <date> - <title> - <class> - <impact on this task> - <source URL>
Applied to this task: <what changed in the recommendations, or "no change">
Sources consulted: <URLs>
```

## Phase 3: Understand the business

Capture (from the user, their site, project files, or stated assumptions): business model, products/services, ICP and buying committee, markets and languages, conversion actions, brand voice rules, constraints (CMS, dev capacity, legal). For B2B, the conversion target is qualified pipeline, not sessions.

## Phase 4: Research

Use the best available source per data type and record the source and date beside every metric:

| Need | Preferred source | Fallback |
|---|---|---|
| Queries, clicks, impressions, CTR, pages | Google Search Console (user export or API) | none; say unavailable |
| Volume, KD, CPC | Keyword Planner, Ahrefs, Semrush, Moz (user export or MCP) | qualitative demand signals only, labeled |
| SERP composition | Live search via WebSearch/browser for the target market | state "SERP not verified" |
| Crawl/technical | Screaming Frog/Sitebulb export, fetched HTML, PageSpeed Insights | sample pages fetched directly |
| Backlinks | Ahrefs/Semrush/Moz/Bing WMT exports | observable mentions only |
| Conversions | GA4, CRM | none; say unavailable |

Integration details, auth, and fallbacks: [references/analytics-measurement.md](references/analytics-measurement.md) section "Tool integrations".

## Phase 5: Strategize

Prioritize with the P0-P3 rubric (business value, opportunity, severity, evidence, effort, dependency, risk, time sensitivity, confidence). Prefer lower-volume, high-intent terms over high-volume terms with weak fit. Recommend one of: create, improve, consolidate (301/canonical), or do not target.

## Phase 6: Execute

Produce the complete deliverable, not instructions for making it. Use templates in `templates/`:
`keyword-map.csv`, `seo-audit.csv`, `content-brief.md`, `blog-template.md`, `landing-page-template.md`, `backlink-prospects.csv`, `editorial-calendar.csv`, `seo-report.md`, `update-log.md`.

Formats: Markdown for reports and copy; CSV for maps, prospects, calendars; JSON-LD for schema; XLSX/DOCX only when the environment has those skills and the user asked; HTML for approved page builds.

## Phase 7: Validate (loop until clean)

Run the applicable scripts, fix, re-run:

```bash
python3 scripts/validate_metadata.py --title "..." --description "..." [--keyword "..."]
python3 scripts/validate_metadata.py --csv <file-with-title,description-columns>
python3 scripts/validate_schema.py <file.jsonld or page.html>
python3 scripts/validate_internal_links.py --links <links.csv> [--sitemap-urls <urls.txt>]
python3 scripts/cluster_keywords.py --serp-csv <keyword,url rows> --threshold 3
```

Then run the checklist in [references/compliance-quality-control.md](references/compliance-quality-control.md): technical, content, policy, AI-search, and fact checks. Only deliver when every P0 issue is fixed or explicitly disclosed.

## Phase 8: Deliver

End every deliverable with a short quality report: checks passed, issues found, corrections made, remaining uncertainties, items needing human review (legal claims, product facts, stats to confirm). Write files when the environment supports it.

## Phase 9: Learn from results

If prior outputs and performance data exist (GSC/GA4 exports, earlier snapshots, previous keyword maps), compare outcomes to the earlier recommendations and adjust. Do not claim persistent learning beyond files actually saved. Log new verified changes in [knowledge/latest-verified-updates.md](knowledge/latest-verified-updates.md) using [templates/update-log.md](templates/update-log.md) when file writes persist.

## Dependencies

Python 3.9+ standard library only for all scripts. Optional: `pytest` to run `tests/`. Live refresh needs web tools or shell internet access; if neither exists, the skill still works from the knowledge snapshot and says so.

## Source registry

Authority order and URLs: [references/official-source-registry.md](references/official-source-registry.md). Current Google requirements digest: [references/google-search-guidelines.md](references/google-search-guidelines.md). Research method: [knowledge/research-methodology.md](knowledge/research-methodology.md).
