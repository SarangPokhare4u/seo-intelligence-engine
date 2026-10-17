# Keyword Research Reference

## Contents
- Data sources and labeling
- The 10-step method
- Attribute definitions
- Priority score
- Cannibalization check
- B2B and zero-volume keywords
- Output

## Data sources and labeling

| Source | Gives | Label in output |
|---|---|---|
| Google Search Console | Real queries, impressions, clicks, CTR, avg position (by page/country/device) | `GSC <date range>` |
| Google Keyword Planner | Volume ranges (exact only with active spend), CPC ranges | `GKP <date>` |
| Ahrefs / Semrush / Moz | Modeled volume, KD (tool-specific scale), CPC, SERP snapshot, competitor keywords | `<tool> <date>` |
| Google Trends | Relative interest 0-100, seasonality | `Trends <range, geo>` |
| Autocomplete, People Also Ask, related searches | Phrasing and questions (no volume) | `SERP observed <date, geo>` |
| Bing Webmaster Tools keyword research | Bing volumes | `Bing WMT <date>` |
| Customer language (sales calls, support, CRM, reviews) | Real buyer terms | `customer research` |
| User spreadsheets | Whatever columns exist | `user-supplied` |

Rules: never convert a range into a point value; never average two tools' volumes into a new number; never present KD from one tool as comparable with another tool's scale. If no metric source exists, the volume column is `unavailable` and demand is described qualitatively (e.g. "PAA present, autocomplete suggests multiple variants").

## The 10-step method

1. **Seeds**: products, problems solved, job titles, use cases, industries, competitor category terms, customer language.
2. **Expansion**: modifiers (software, platform, tool, system, vendor, pricing, alternative, vs, best, for <industry>, how to, cost of, template, checklist), questions (who/what/why/how/can/does), long-tail.
3. **Entities and concepts**: related standards, regulations, roles, processes, named methods, adjacent tools. These guide coverage, not keyword stuffing.
4. **Intent classification**: informational / navigational / commercial investigation / transactional, plus funnel TOFU/MOFU/BOFU. Confirm with the SERP for priority terms.
5. **SERP analysis**: see [search-intent-serp-analysis.md](search-intent-serp-analysis.md).
6. **Competitor gap**: keywords competitors rank for that the site does not (tool export or observed SERPs).
7. **Clustering**: group by shared ranking URLs (SERP overlap). Run `scripts/cluster_keywords.py`. Default: 3+ shared URLs in top 10 means one page can target both. Without SERP data, cluster by intent + head-term similarity and label `lexical clustering, unverified by SERP`.
8. **Conversion potential**: does the searcher have budget/authority/need now? Map to an offer.
9. **Keyword-to-page mapping**: one primary cluster per URL; existing URL if it already ranks or fits; otherwise propose a URL.
10. **Prioritize**: score below, then sanity-check by hand.

## Attribute definitions

| Column | Allowed values |
|---|---|
| intent | informational, navigational, commercial, transactional |
| funnel | TOFU, MOFU, BOFU |
| volume | number with source, range with source, or `unavailable` |
| kd | number + tool name, or `low/medium/high (qualitative)` |
| cpc | value + currency + source, or `unavailable` |
| business_relevance | low, medium, high + one-line reason |
| conversion_potential | low, medium, high + reason |
| serp_features | observed features only (AI Overview, PAA, video, local pack, shopping, discussions and forums, images, featured snippet, sitelinks, top stories) |
| competitor_urls | URLs actually observed or tool-reported |
| recommended_url | existing path or `NEW: /proposed-path/` |
| content_format | blog, pillar, landing, product, service, comparison, use-case, industry, glossary, tool, case study, category |
| priority | P0-P3 with score |

## Priority score

Transparent 0-100 score; show the inputs.

```
score = 30*relevance + 25*conversion + 15*opportunity + 15*feasibility + 15*strategic_fit
each input 0.0-1.0
opportunity: demand evidence (volume, impressions, PAA richness) relative to the niche
feasibility: inverse of competitive strength observed (who ranks, page types, site's current position)
strategic_fit: supports a priority product, cluster, or market
P1 >= 70, P2 50-69, P3 < 50. P0 reserved for fixing critical issues (e.g. money page not indexed), not keywords.
```

Lower-volume keywords with strong purchase intent and fit outrank high-volume, weak-fit terms. State this explicitly when it changes the order.

## Cannibalization check

Flag when two URLs on the site: (a) both receive impressions for the same query in GSC, alternating positions; or (b) are mapped to the same cluster. Resolve by: differentiate intent, consolidate with 301, canonicalize, or de-optimize one. Never recommend creating near-duplicate pages for keyword variants.

## B2B and zero-volume keywords

Niche B2B terms often show 0-10 or `unavailable` volume yet represent real buyers. Include them when supported by: customer language, sales call notes, GSC impressions, competitor targeting, or industry terminology. Label `low/zero reported volume; included for commercial relevance (<evidence>)`.

## Output

Use [templates/keyword-map.csv](../templates/keyword-map.csv). Include a header block stating sources, dates, market, and what was unavailable.
