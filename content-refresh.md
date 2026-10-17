# Workflow G: SEO Content Refresh

**Input**: existing page URL or text; performance data (GSC queries/pages for 3-16 months, GA4 landing page); target keywords.
**Output**: diagnosis, gap analysis, updated research, change list, improved copy (full or section-level), implementation checklist.

Load: references/on-page-seo.md, references/content-writing.md, references/analytics-measurement.md.

## Checklist

```
- [ ] 1. Phase 2 brief
- [ ] 2. Baseline: clicks, impressions, CTR, position by query (period-over-period, YoY), conversions
- [ ] 3. Diagnose: decay (lost positions), CTR problem (good position, low CTR), intent drift (SERP changed), cannibalization, outdated facts, thin sections, technical (indexing/rendering)
- [ ] 4. SERP re-check for top queries: what ranks now and why
- [ ] 5. Gap analysis: queries with impressions not addressed on page; competitor coverage; new subtopics
- [ ] 6. Fact update: every stat and claim re-verified; replace stale data with dated sources
- [ ] 7. Change list: keep / rewrite / add / remove / merge, with reason
- [ ] 8. Rewrite: preserve product meaning, facts, URL, and what already ranks; improve intro, structure, depth, examples, internal links
- [ ] 9. Metadata update only if it addresses a diagnosed CTR or intent problem (validate_metadata.py)
- [ ] 10. Update dateModified only for substantive changes
- [ ] 11. Implementation checklist + measurement plan (compare 28-day windows post-reindex)
- [ ] 12. QA + quality report
```

Rule: do not change the URL of a ranking page. If consolidating, 301 the weaker page into the stronger and merge unique content.
