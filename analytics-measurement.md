# Analytics, Measurement, and Tool Integrations

## Contents
1. Metric layers
2. Search Console essentials and caveats
3. GA4 essentials
4. B2B KPI framework
5. Traffic-drop diagnosis
6. Reporting cadence
7. Tool integrations (auth, fields, fallbacks, freshness)

## 1. Metric layers

Keep separate in every report:
- **Visibility**: impressions, average position, queries ranking, AI citations (Bing), Generative AI report impressions.
- **Acquisition**: GSC clicks, GA4 organic sessions/users, referral sessions from AI platforms.
- **Conversion**: GA4 key events (demo request, contact), CRM leads/SQLs/opportunities/pipeline.

GSC clicks are not GA4 sessions (consent mode, bot filtering, attribution, redirects, cross-domain, and different counting rules). Never equate them.

## 2. Search Console essentials and caveats

- Average position is impression-weighted and query-dependent; compare like-for-like segments.
- Anonymized queries are omitted from query tables; page totals exceed query totals.
- AI Mode and AI Overviews count under "Web" totals; each AI Mode follow-up is a new query.
- Data is available for 16 months; export regularly for longer history.
- Useful features: branded query filter (AI-assisted, may misclassify), query groups (high-volume properties), annotations, hourly/weekly/monthly views, Generative AI performance reports (rolling out), Page indexing, Crawl stats, Core Web Vitals, Enhancements, Manual actions, Security issues.
- API: Search Analytics API (supports hourly data since 2025-04), URL Inspection API (2,000/day/property quota) [verify current quotas].

## 3. GA4 essentials

Landing page report filtered to Organic Search; key events; engagement rate; custom channel group for AI referrers (regex on source: `chatgpt\.com|perplexity\.ai|copilot\.microsoft\.com|gemini\.google\.com|claude\.ai|edgeservices\.bing\.com`). Link GA4 to Search Console for the combined reports.

## 4. B2B KPI framework

| Layer | KPI | Source |
|---|---|---|
| Visibility | Non-branded impressions for priority clusters | GSC (branded filter) |
| Acquisition | Non-branded organic clicks to commercial + cluster pages | GSC |
| Engagement | Organic sessions reaching product/demo pages | GA4 path exploration |
| Conversion | Organic demo/contact submissions; conversion rate by landing page | GA4 key events |
| Pipeline | Organic-sourced and organic-influenced SQLs, opportunities, pipeline value | CRM (state attribution model) |

Other models: e-commerce (revenue, AOV, product page CTR), publishers (pageviews, subscriptions, Discover traffic), local (calls, direction requests, GBP actions).

## 5. Traffic-drop diagnosis (investigate before concluding)

Order: (1) tracking/reporting change (GA4 tag, consent, GSC property, filters); (2) technical change (deploy, robots, noindex, canonicals, redirects, rendering, server errors) by matching dates in GSC Crawl stats and release logs; (3) seasonality and demand (Trends, YoY); (4) SERP changes (new features, AI Overviews, competitors) for top lost queries; (5) algorithm updates overlapping the window (Status Dashboard dates); (6) competitor gains; (7) manual actions/security. Segment by page type, query type (branded/non-branded), device, country. Label each cause `confirmed`, `likely`, `possible`, `ruled out`.

## 6. Reporting cadence

- Weekly: indexing/crawl anomalies, top page click deltas, conversions, launches.
- Monthly: KPI table by layer, cluster performance, wins/losses with causes, next actions.
- Quarterly: strategy review, roadmap re-prioritization, content audit, competitor shifts.
Template: [templates/seo-report.md](../templates/seo-report.md).

## 7. Tool integrations

| Integration | Provides | Required? | Auth | Key fields | Errors / fallback | Freshness check |
|---|---|---|---|---|---|---|
| Live web (WebFetch/WebSearch/browser) | Official doc refresh, SERP observation, page fetch | Required for "freshly verified" | none | page text | Fall back to knowledge snapshot; mark previously verified | Page "Last updated" date |
| Google Search Console API | Queries, pages, clicks, impressions, CTR, position; URL inspection | Optional (user CSV export works) | OAuth 2.0 or service account added as user; scope `webmasters.readonly` | date, query, page, country, device, searchAppearance | 403 -> property access; 429 -> back off; else ask for export | Data lags ~2-3 days; note last date |
| GA4 Data API | Sessions, users, key events by landing page/channel | Optional | OAuth/service account with Viewer; scope `analytics.readonly` | sessionDefaultChannelGroup, landingPage, keyEvents | Ask for export | Note property timezone and date range |
| Google Ads API / Keyword Planner | Volume ranges, CPC | Optional | Developer token + OAuth + customer ID | keyword, avg monthly searches, competition, bid ranges | Use other tool or label unavailable | Note month of data |
| PageSpeed Insights API | CrUX field data + Lighthouse | Optional (key recommended) | API key | LCP, INP, CLS (p75), lab audits | Run PSI web UI or ask for report | CrUX = rolling 28 days |
| Google Trends (API alpha since 2025-07, or UI) | Relative interest, seasonality | Optional | Alpha access / none for UI | interest over time, related queries | Describe qualitatively | Note range and geo |
| Bing Webmaster Tools | Queries, backlinks, AI Performance (citations), keyword research | Optional | API key | query stats, citations | Ask for export | Note date |
| Ahrefs / Semrush / Moz | Volume, KD, backlinks, competitor keywords | Optional | API key or MCP connector | tool-specific | Use CSV export; label vendor | Note export date; metrics are estimates |
| Screaming Frog / Sitebulb | Crawl data | Optional | none (export) | address, status, indexability, canonical, title, meta, H1, inlinks, depth | Sample with fetches | Note crawl date and config |
| Sitemap/page fetch utilities | URL lists, raw HTML | Optional | none | | WebFetch summary | Note fetch date |
| Spreadsheets (CSV/XLSX) | User data | Optional | none | any | Ask for CSV | Ask for export date |
| Site source code | Templates, rendering, schema | Optional | repo access | | Inspect rendered HTML | Commit date |

Security: never print, store, or include credentials or tokens in reports. Read-only scopes only. Do not request write access (Google's 2026-06-05 guidance).
