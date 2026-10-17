# Workflow D: Create an SEO Blog Article (or pillar/cluster article)

**Input**: topic, audience, website; optional brand guidelines, target keyword, internal URLs list, SME notes.
**Output**: research brief + keyword set + competitor/SERP analysis + publish-ready article (templates/blog-template.md) + metadata + links + schema + QA.

Load: references/content-writing.md, references/on-page-seo.md, references/search-intent-serp-analysis.md. Add references/structured-data.md for schema.

## Checklist

```
- [ ] 1. Phase 2 brief (content/AI-content guidance, rich result changes)
- [ ] 2. Reader, goal, conversion; load brand voice rules if available
- [ ] 3. Keyword set: primary, secondary, questions (sources labeled)
- [ ] 4. SERP review of primary keyword: intent, formats, top pages' coverage
- [ ] 5. Gap list + original angle (what this article adds that top results lack)
- [ ] 6. Source collection: primary sources, dated; facts about the user's product from user/site only
- [ ] 7. Content brief (templates/content-brief.md) -> confirm only if user is present and stakes are high; otherwise proceed
- [ ] 8. Draft full article to the outline; direct answers first; real examples
- [ ] 9. Metadata: title, description, URL, H1 -> validate_metadata.py
- [ ] 10. Internal links (3-10 contextual, to pillar/commercial pages) and external citations
- [ ] 11. Images: recommendations with file names and alt text
- [ ] 12. Schema: Article + BreadcrumbList (validate_schema.py). No FAQ rich result claims.
- [ ] 13. Edit pass: banned patterns, brand rules, readability, duplicate ideas
- [ ] 14. Fact-check table (claim, source, date, status)
- [ ] 15. QA checklist + quality report
```

## Output order

1. Intelligence brief (short)
2. Content strategy summary (audience, intent, angle, conversion rationale)
3. Keyword set
4. SERP/competitor notes and differentiation summary
5. Metadata block (title, description, URL, H1)
6. Full article (Markdown, H2/H3)
7. Internal links table; external citations list
8. Images + alt text
9. JSON-LD
10. CTA
11. Fact-check table
12. QA checklist and quality report
