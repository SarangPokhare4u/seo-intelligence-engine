# Technical SEO Reference

## Contents
1. Evidence rules
2. Discovery and crawling
3. Indexing and canonicalization
4. Architecture and internal links
5. Performance and Core Web Vitals
6. JavaScript and rendering
7. International, pagination, e-commerce
8. Security
9. Site migrations
10. Issue record format

## 1. Evidence rules

- `confirmed`: observed in fetched HTML/headers, crawl export, GSC, PSI, or server logs. Cite the evidence.
- `potential risk`: plausible from partial evidence; say what would confirm it.
- A sample of fetched pages is not a crawl. Say "sampled N URLs" when that is what happened.
- Fetch raw HTML with `curl -sSL -A "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" -D - <url>` when the shell has network; otherwise WebFetch (rendered summary, not raw HTML; note the limitation).

## 2. Discovery and crawling

| Check | How | Notes |
|---|---|---|
| robots.txt | fetch /robots.txt | Disallow on important paths or CSS/JS? Sitemap line present? robots.txt controls crawling, not indexing |
| XML sitemaps | fetch, count URLs, sample status codes | Only canonical, indexable, 200 URLs; lastmod accurate; <50k URLs / 50 MB per file |
| HTML sitemap | optional | Useful for large or deep sites |
| Crawlable navigation | `<a href>` links present in HTML | JS click handlers without href are not crawlable links |
| Crawl depth | crawl export | Money pages within ~3 clicks is an [INT] heuristic |
| Orphans | sitemap URLs minus internally linked URLs; `scripts/validate_internal_links.py` | |
| Status codes | crawl export | 4xx on linked URLs; 5xx spikes (GSC Crawl stats) |
| Redirect chains | crawl export | Keep to one hop; update internal links to final URL |
| Crawl budget | only matters for very large or fast-changing sites (Google guidance) | Parameter/facet traps, infinite calendars |
| File size | HTML over 2 MB uncompressed risks truncation for Search (Googlebot doc, 2026-02-03); inline CSS/JS/base64 count toward it | |

## 3. Indexing and canonicalization

- `noindex` (meta or X-Robots-Tag) only works if the URL is crawlable.
- Do not ship `noindex` in initial HTML expecting JS to remove it.
- Canonical: absolute URL, self-referencing on canonical pages, consistent with internal links, sitemaps, redirects, and hreflang. One canonical per page, in `<head>`. Do not canonicalize paginated series to page 1.
- Duplicates: protocol/host/trailing slash/case/parameter variants should 301 or canonicalize to one version.
- Soft 404: thin "no results" or empty pages returning 200 -> return 404/410 or add real content.
- GSC Page indexing report reasons to triage: "Crawled - currently not indexed" (quality/duplication signal), "Discovered - currently not indexed" (crawl capacity or priority), "Duplicate without user-selected canonical", "Alternate page with proper canonical" (expected), "Blocked by robots.txt", "Excluded by noindex".
- URL Inspection (live test) confirms rendered HTML, canonical selection, indexability for a URL.

## 4. Architecture and internal links

- Logical URL hierarchy; readable, lowercase, hyphenated slugs; no session IDs.
- Hub-and-spoke: pillar links to cluster pages and back; cluster pages link to the relevant commercial page with descriptive anchors.
- Breadcrumbs (visible + BreadcrumbList markup; breadcrumb rich display is desktop-only).
- Descriptive anchor text; avoid "click here"; avoid identical anchors pointing to different URLs.
- Semantic HTML: one main H1 is common practice [INT]; headings reflect structure; `<main>`, `<nav>`, `<article>`.

## 5. Performance and Core Web Vitals

| Metric | Good threshold (75th percentile field data) |
|---|---|
| Largest Contentful Paint (LCP) | <= 2.5 s |
| Interaction to Next Paint (INP) | <= 200 ms (replaced FID in March 2024) |
| Cumulative Layout Shift (CLS) | <= 0.1 |

Use CrUX field data (PageSpeed Insights, GSC Core Web Vitals report) for status; Lighthouse lab data for diagnosis. Common fixes: preload/priority hint the LCP image, serve modern formats with explicit dimensions, reduce render-blocking CSS/JS, break up long tasks, defer third-party scripts, reserve space for ads/embeds. Page experience is one consideration among many; do not overstate it as a primary ranking driver.

## 6. JavaScript and rendering

- Prefer SSR/SSG or hydration with server-rendered content for primary content, links, titles, canonicals, and structured data.
- Non-200 pages may not be rendered.
- Check rendered vs raw HTML (URL Inspection or a headless browser); critical content and links must exist after render.
- Avoid fragment (`#`) URLs for distinct content; use the History API.
- Lazy-load below-the-fold content only; ensure content loads without user interaction.
- JS paywalls: follow the paywalled content guidance (2025-08-28 update).

## 7. International, pagination, e-commerce

- Hreflang: see [local-international-seo.md](local-international-seo.md).
- Pagination: crawlable `<a href>` links between pages; each page self-canonical; `rel=next/prev` is not used by Google for indexing.
- Faceted navigation: allow valuable facets, block or noindex low-value combinations, avoid crawl traps.
- E-commerce: Product + merchant listing markup, Merchant Center feeds, out-of-stock handling (keep page if returning; 404/410 or redirect to close match if permanent).

## 8. Security

HTTPS everywhere with 301 from HTTP; HSTS; no mixed content; check for hacked content (GSC Security issues report); avoid deceptive behavior (back button hijacking is a spam policy as of 2026-04-13).

## 9. Site migrations

Checklist: URL mapping (old -> new, 1:1 where possible), 301s, update internal links/canonicals/hreflang/sitemaps, keep old sitemap briefly for discovery, GSC Change of Address for domain moves (now covers subdomain variants), benchmark before, monitor indexing and traffic for 8-12 weeks [INT].

## 10. Issue record format

Use [templates/seo-audit.csv](../templates/seo-audit.csv): id, url_or_pattern, category, issue, evidence, evidence_type (confirmed/potential risk), seo_impact, severity, priority (P0-P3), remediation, implementation, test_method, owner, status.
