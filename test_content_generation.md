# Test D: Content Generation (behavioral)

## Prompt
"Write a comprehensive SEO blog on reducing vehicle inspection delays. Research keywords, analyze competitors, and create publish-ready content. Audience: operations managers at automotive logistics companies in the US."

## Pass criteria

Process
- [ ] SEO Intelligence Brief first (date, status, relevant changes only)
- [ ] Keyword set with labeled sources (`unavailable` where no metric source)
- [ ] SERP observed for the primary keyword with date/market, or explicitly marked unverified
- [ ] Gap list and stated original angle
- [ ] Content brief produced before the article

Article
- [ ] Single H1; logical H2/H3; answer-first sections
- [ ] No banned openers/filler (see references/content-writing.md)
- [ ] Every statistic has a source URL and date, or is flagged `needs confirmation`
- [ ] No invented customers, quotes, testimonials, or results
- [ ] Product claims limited to user-supplied/site facts or `[CONFIRM]` placeholders
- [ ] Internal link suggestions with descriptive anchors and a commercial next step
- [ ] CTA appropriate to stage

Packaging
- [ ] Title and description validated with scripts/validate_metadata.py (output shown)
- [ ] Article + BreadcrumbList JSON-LD validated with scripts/validate_schema.py; no FAQ rich result claims
- [ ] Image recommendations with alt text
- [ ] Fact-check table
- [ ] Quality report with human-review items

## Scoring
PASS if all Process and Article boxes pass and at most one Packaging box fails with a stated reason.
