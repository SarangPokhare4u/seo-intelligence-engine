# Test E: Website Audit (behavioral)

## Variant 1: public site, no exports
Prompt: "Audit https://example.com for technical SEO, content gaps, internal linking issues, and AI search discoverability."

Pass:
- [ ] States the evidence base precisely (e.g., "fetched homepage, robots.txt, sitemap, 5 sampled URLs"); does not claim a full crawl
- [ ] Each issue has evidence and `confirmed` or `potential risk`
- [ ] Items not checkable without data are listed as "not checked" (e.g., Core Web Vitals field data without PSI/CrUX, indexing without GSC)
- [ ] P0-P3 priorities follow the rubric (no P0 for cosmetic items)
- [ ] Remediation + test method per issue
- [ ] AI discoverability section follows Google's guidance (no llms.txt requirement)
- [ ] Issues CSV matches templates/seo-audit.csv

## Variant 2: supplied crawl data
Provide: tests/fixtures/links.csv, tests/fixtures/sitemap_urls.txt, tests/fixtures/clusters.csv, tests/fixtures/metadata.csv, tests/fixtures/page.html.
Prompt: "Here is our crawl data. Audit internal linking, metadata, and schema."

Pass:
- [ ] Runs validate_internal_links.py, validate_metadata.py --csv, validate_schema.py and reports their real output
- [ ] Finds: orphan /blog/orphan-post/, generic anchor "click here", link to /old-page/ not in sitemap, pillar missing link to orphan cluster page, duplicate title, placeholder description, SoftwareApplication name not visible, rating markup without visible ratings
- [ ] Does not invent issues not supported by the data
