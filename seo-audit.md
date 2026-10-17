# Workflow B: SEO Audit

**Input**: domain; optional crawl export (Screaming Frog/Sitebulb CSV), GSC exports (Performance, Page indexing), PSI/CrUX, GA4, server logs.
**Output**: audit report + issues CSV (templates/seo-audit.csv) + implementation plan.

Load: references/technical-seo.md, references/on-page-seo.md, references/structured-data.md, references/compliance-quality-control.md. Add references/ai-search-optimization.md if AI discoverability is in scope.

## Checklist

```
- [ ] 1. Phase 2 brief (12-month window for indexing/crawl/spam/rich results)
- [ ] 2. State audit scope and evidence base: crawl export? GSC? how many URLs sampled?
- [ ] 3. Discovery: robots.txt, sitemaps (count, status sample), navigation links
- [ ] 4. Indexability: status codes, noindex, canonicals, duplicates, soft 404s, GSC Page indexing reasons
- [ ] 5. Architecture: depth, orphans (validate_internal_links.py), breadcrumbs, URL patterns
- [ ] 6. Rendering: raw vs rendered for key templates; JS-dependent links/content
- [ ] 7. Performance: CrUX field data per template (PSI), main LCP/INP/CLS causes
- [ ] 8. On-page per template: titles/descriptions (validate_metadata.py --csv), H1s, content depth vs intent, internal links
- [ ] 9. Structured data: present types, validity (validate_schema.py), deprecated types
- [ ] 10. International/local (if relevant): hreflang, GBP alignment
- [ ] 11. Security/policy: HTTPS, mixed content, spam-policy risks, manual actions (if GSC provided)
- [ ] 12. Content gaps & cannibalization (GSC queries mapped to multiple pages)
- [ ] 13. AI discoverability (snippet controls, crawler access for Googlebot/Bingbot/OAI-SearchBot/PerplexityBot, text in HTML)
- [ ] 14. Prioritize (P0-P3) and write remediation + test method per issue
- [ ] 15. QA + quality report
```

## Rules

- Every issue row: evidence + evidence_type (`confirmed` / `potential risk`).
- Group issues by template/pattern rather than listing thousands of URLs.
- Distinguish "not checked (no data)" from "passed".

## Report structure

Scope & evidence base; intelligence brief; summary scorecard by area (counts of P0-P3, not a "score"); top 10 issues; detailed findings by area; implementation plan (sprint 1/2/3); monitoring and re-test plan; quality report.
