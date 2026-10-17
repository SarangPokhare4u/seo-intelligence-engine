# Workflow C: Keyword Research

**Input**: product/service/topic/domain/market. Optional: GSC queries export, tool exports, seed list, competitor domains.
**Output**: keyword map CSV (templates/keyword-map.csv) + cluster summary + page mapping + priorities.

Load: references/keyword-research.md, references/search-intent-serp-analysis.md.

## Checklist

```
- [ ] 1. Phase 2 brief (short; note SERP feature changes and reporting changes)
- [ ] 2. Business inputs: offers, ICP, conversions, markets, exclusions
- [ ] 3. Data inventory: list available sources and dates; list unavailable ones
- [ ] 4. Seeds (products, problems, roles, industries, use cases, competitor terms, customer language)
- [ ] 5. Expansion: modifiers, questions, long-tail (autocomplete/PAA via WebSearch where possible)
- [ ] 6. Entities and related concepts
- [ ] 7. Intent + funnel classification
- [ ] 8. SERP checks for top 10-30 candidates (observed, dated, market-specific)
- [ ] 9. Competitor gap (tool export or observed SERPs)
- [ ] 10. Cluster: scripts/cluster_keywords.py on SERP rows (keyword,url) or lexical fallback (labeled)
- [ ] 11. Cannibalization check against existing pages (GSC query-page pairs if supplied)
- [ ] 12. Map clusters to URLs (existing or NEW) and content formats
- [ ] 13. Score and prioritize (formula in keyword-research.md); explain where low-volume high-intent outranks high-volume
- [ ] 14. Build CSV; header notes: sources, dates, market, unavailable data
- [ ] 15. QA: no fabricated metrics; every metric has source; CSV opens cleanly
```

## Cluster script usage

```bash
# rows: keyword,url,position (position optional) from SERP observation or tool export
python3 scripts/cluster_keywords.py --serp-csv serp_rows.csv --threshold 3 --out clusters.csv
# no SERP data: lexical fallback, labeled as such in output
python3 scripts/cluster_keywords.py --keywords keywords.txt --lexical --out clusters.csv
```

## Deliverable sections

Summary (top clusters, top 10 priorities); data sources and limitations; keyword map CSV; cluster table (cluster, primary keyword, intent, recommended URL, format, priority); quick wins (if GSC supplied); terms deliberately not targeted and why; quality report.
