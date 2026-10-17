# Google Search Guidelines Digest

Verified against Google Search Central on 2026-10-17. Each item is tagged:
- **[REQ]** stated by Google as required for eligibility or as a policy violation
- **[REC]** Google recommendation / best practice
- **[INT]** interpretation or industry practice, not a Google statement

Re-verify any item before stating it as current if the task depends on it (Phase 2).

## Contents
1. Search Essentials: technical requirements
2. Spam policies (current list)
3. Content quality and generative AI content
4. Ranking systems and core updates
5. Crawling, rendering, indexing
6. Search appearance and rich results
7. AI features (AI Overviews, AI Mode)
8. Search Console reporting changes
9. Third-party SEO tools and services
10. Myths to reject

## 1. Search Essentials: technical requirements

- [REQ] Googlebot is not blocked; the page returns HTTP 200; the page has indexable content. These are the minimum technical requirements.
- [REQ] Meeting requirements does not guarantee crawling, indexing, or serving.
- [REC] Key best practices: helpful people-first content, words people search for in prominent places (title, headings, alt text, link text), crawlable links, telling people about the site, following image/video/structured data/JS best practices.

## 2. Spam policies (current list, page updated 2026-08-28)

Cloaking; doorway abuse; expired domain abuse; hacked content; hidden text and link abuse; keyword stuffing; link spam; machine-generated traffic; malicious practices (malware, unwanted software, **back button hijacking**, added 2026-04-13); misleading functionality; scaled content abuse; scraping; site reputation abuse (EEA enforcement approach adjusted 2026-08-28); sneaky redirects; thin affiliation; user-generated spam; other demotion/removal causes (legal, personal info, policy circumvention, scams).

- [REQ] Spam policies apply to attempts to manipulate **generative AI responses in Google Search** (clarified 2026-05-15).
- [REQ] Paid links must carry `rel="sponsored"` or `rel="nofollow"`. Guest posts placed for links are link spam unless qualified.
- [REQ] Spam reports may be used for manual actions (clarified 2026-04-14 and 2026-04-23).
- [REQ] Site reputation abuse fixes for a manual action: rework as first-party, move to new domain, `noindex` (not robots.txt), or remove.
- [REQ] Scaled content abuse applies regardless of how content is produced (human, AI, or mixed).

## 3. Content quality and generative AI content

- [REC] Helpful, reliable, people-first content: original information, substantial and complete description, insight beyond the obvious, no exaggerated titles, expertise evident, satisfying experience. Use the self-assessment questions on the helpful content page.
- [REC] "Who, How, Why": make authorship clear where expected, explain how content was produced (including automation) where readers would expect it, and make the "why" helping people, not ranking.
- [REQ via spam policy] Generating many pages with AI without adding value may violate scaled content abuse.
- [REC] Fact-check and review all AI-generated content; this includes titles, meta descriptions, structured data, and alt text (guidance updated 2026-10-01 to align with the Search Quality Rater Guidelines sections 4.6.5 scaled content abuse and 4.6.6 low-effort/low-originality content).
- [REQ for Merchant Center] AI-generated product images need IPTC `DigitalSourceType` `TrainedAlgorithmicMedia` metadata; AI-generated product titles/descriptions must be labeled.
- [REQ] Rater guidelines do not directly influence ranking and are not a ranking manual.

## 4. Ranking systems and core updates

- [REQ] Core updates are broad; there is no specific fix. Google points to content quality self-assessment. Smaller core updates also happen between announced ones (doc added 2025-12-09).
- Confirmed 2025-2026 ranking updates (Status Dashboard): see [knowledge/latest-verified-updates.md](../knowledge/latest-verified-updates.md).
- [INT] Recovery after a core update is often visible only after a later core update; not a Google guarantee.

## 5. Crawling, rendering, indexing

- [REQ] Googlebot fetches the first **2 MB** (uncompressed) of supported text file types and the first **64 MB** of a PDF when crawling for Search; resources (CSS/JS) are fetched separately with their own limit. Google described the 2026-02-03 doc change as documentation, not behavior change. General crawler infrastructure limit stated as 15 MB.
- [REQ] Pages returning non-200 status may not be sent for rendering (2025-12-18). Do not rely on JS to fix error pages.
- [REC] Do not put `noindex` in the initial HTML if you want JS to remove it later; Google may not render (2025-12-15).
- [REC] Set canonical consistently in HTML and JS; avoid JS changing the canonical (2025-12-17).
- [REQ] Robots meta tags outside `<head>` handling documented 2026-03-24; place them in `<head>`.
- [REQ] robots.txt controls crawling, not indexing. A blocked URL can still be indexed without content; use `noindex` (crawlable) to keep it out.
- [REC] Canonicalization is a signal set (redirects, rel=canonical, sitemaps, internal links); re-evaluation timing documented 2026-07-10.
- Crawling documentation moved to the crawling infrastructure site (https://developers.google.com/crawling) in Nov-Dec 2025. Crawler IP range files moved (March 2026).
- [REC] Change of Address now covers subdomain variants (2026-06-17).

## 6. Search appearance and rich results

- Currently supported rich result types (gallery updated 2026-10-16): Article, Breadcrumb, Carousel, Course list, Dataset, Discussion forum, Education Q&A, Employer aggregate rating, Event, Image metadata, Job posting, Local business, Math solver, Movie, Organization, Product (incl. merchant listings), Profile page, Q&A, Recipe, Review snippet, Software app, Speakable, Subscription/paywalled content, Vacation rental, Video.
- **Deprecated / no longer shown**: FAQ rich results (stopped 2026-05-07; docs removed 2026-06-15), HowTo, Practice problem (removed 2026-01-06), Special announcement (2025), Book actions, Course info, Claim review, Estimated salary, Learning video, Vehicle listing and others retired 2025. Do not recommend these as rich-result opportunities. FAQPage markup may stay on pages harmlessly; it earns no rich result.
- [REC] Breadcrumbs appear on desktop results only (2025-01-22).
- [REC] Review snippet: new guideline against fake and undisclosed incentivized reviews (2026-07-24); avoid multiple ways of declaring the reviewed item (2025-11-12).
- [REC] Preferred image: image metadata and `og:image` inform thumbnails (2026-03-02).
- New 2026 features: Preferred sources (docs 2026-01-30; all languages 2026-04-30; AI Mode/AI Overviews 2026-05-27; custom button 2026-08-20), "read more" deep links (2026-04-20), Search profile badge (2026-09-16), regional differences doc (2026-09-08), Product `category` and sale-price dates (2026-07-07), VideoObject `creator` (2026-09-24).

## 7. AI features (AI Overviews, AI Mode)

- [REQ] Eligibility: indexed and eligible to show with a snippet. No additional requirements, no special optimization, no special schema.
- [REQ] Controls: `nosnippet`, `data-nosnippet`, `max-snippet`, `noindex` limit what is shown. Googlebot robots.txt rules govern Search crawling. `Google-Extended` controls training/grounding in some other Google systems, not Search.
- [REC] AI optimization guide (published 2026-05-15, updated 2026-07-10): foundational SEO applies; unique non-commodity content; clear structure; crawlable; semantic HTML; good page experience; keep Merchant Center and Business Profile current.
- [REQ statement] You do **not** need llms.txt, AI text files, special Markdown, chunking, special schema, or inauthentic mentions. Google Search ignores llms.txt (clarified 2026-06-15).
- Systems use retrieval/grounding with query fan-out.
- [REC] Measure with Search Console Generative AI performance reports (introduced June 2026, rolling out) and the Performance report (AI features count under "Web").

## 8. Search Console reporting changes (2025-2026)

Hourly data and 24-hour view; AI Mode counted in totals (2025-06-16); Search Console Insights revamp; Query groups (2025-10); custom annotations and Branded queries filter (2025-11; filter expanded 2026-03); weekly/monthly views, social channels, AI-powered configuration (2025-12); platform properties and social/video performance guide (2026-07); Generative AI performance reports (2026-06); web multimodal Search performance reporting (2026-09). Confirm availability for the property before relying on any of these.

## 9. Third-party SEO tools and services (2026-06-05)

- [REQ statement] Third-party tools do not have access to Google's internal ranking data; their metrics are estimates. No tool or service is "approved" by Google.
- [REC] Evaluate AEO/GEO advice against Google's generative AI guidance. Do not grant write access to an auditor at the audit stage. Search Console is the first-party data source.

## 10. Myths to reject

Keyword density targets; minimum word counts; meta keywords; E-E-A-T as a direct ranking factor or score; "domain authority" as a Google metric; LSI keywords; mandatory FAQ sections; llms.txt for Google; special AI schema; submitting to Google for AI Overviews; disavow as routine hygiene; duplicate content "penalty" for normal duplication; 15 MB HTML limit for Search indexing (the documented Search limit is 2 MB).
