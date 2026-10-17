# Structured Data and Rich Results

Supported list verified 2026-10-17 against the Search Gallery (updated 2026-10-16). Re-check the gallery before recommending any rich result.

## Contents
- Supported vs deprecated
- Rules
- Templates (JSON-LD)
- Validation

## Supported vs deprecated

Supported rich result features: Article, Breadcrumb, Carousel (beta, limited regions), Course list, Dataset, Discussion forum, Education Q&A, Employer aggregate rating, Event, Image metadata, Job posting, Local business, Math solver, Movie, Organization, Product (product snippets + merchant listings), Profile page, Q&A, Recipe, Review snippet, Software app, Speakable (beta), Subscription and paywalled content, Vacation rental, Video.

Not shown / deprecated: FAQ (stopped 2026-05-07), HowTo, Practice problem, Special announcement, Book actions, Course info, Claim review, Estimated salary, Learning video, Vehicle listing. Do not offer these as rich-result opportunities. Existing FAQPage markup can remain; it gives no Google rich result.

Organization markup has no rich result display but informs knowledge panel/logo details; still recommended for the homepage or about page.

Any schema.org type outside this list may be valid vocabulary but earns no Google rich result. Say so if recommending it for other consumers.

## Rules

- Markup must describe content visible on the page. No hidden or misleading data.
- Never fabricate ratings, reviews, authors, prices, addresses, or dates. Self-serving reviews of the business itself on LocalBusiness/Organization are not eligible for review snippets.
- Review snippet: no fake or undisclosed incentivized reviews (2026-07-24); one way of indicating the reviewed item (2025-11-12).
- Product: `offers` with price/currency/availability; `category` and sale-price date properties documented 2026-07-07; `hasAdultConsideration` when relevant.
- VideoObject: `creator` supported (2026-09-24).
- Prefer JSON-LD in `<head>` or body; one entity graph with `@id` references is fine.
- Structured data is not required for AI features; there is no special AI schema.

## Templates

Organization:
```json
{"@context":"https://schema.org","@type":"Organization","@id":"https://example.com/#org","name":"Example Co","url":"https://example.com/","logo":"https://example.com/logo.png","sameAs":["https://www.linkedin.com/company/example"]}
```

Article (blog post):
```json
{"@context":"https://schema.org","@type":"Article","headline":"<H1 or title>","datePublished":"2026-10-17","dateModified":"2026-10-17","author":[{"@type":"Person","name":"<real author>","url":"https://example.com/authors/<slug>/"}],"publisher":{"@id":"https://example.com/#org"},"image":["https://example.com/images/<file>.jpg"]}
```

BreadcrumbList:
```json
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://example.com/"},{"@type":"ListItem","position":2,"name":"Blog","item":"https://example.com/blog/"},{"@type":"ListItem","position":3,"name":"<Post title>"}]}
```

SoftwareApplication (B2B SaaS; review/rating only if real and shown):
```json
{"@context":"https://schema.org","@type":"SoftwareApplication","name":"<Product>","applicationCategory":"BusinessApplication","operatingSystem":"Web","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"}}
```
Note: Google's software app rich result requires `name`, `offers.price`, and either `aggregateRating` or `review` (verify against the current doc at use time). Most B2B SaaS pages without public pricing and real on-page reviews are not eligible; do not invent a price or rating to qualify. Keep the markup only if it accurately describes the page.

LocalBusiness, Product, VideoObject, Event, JobPosting: follow the current Google doc for required/recommended properties at use time.

## Validation

1. `python3 scripts/validate_schema.py <file.json|file.html>`: parses JSON-LD, checks `@context`/`@type`, flags deprecated types, checks Google-required properties for common types (local rule table), and checks that key text values appear in the HTML when an HTML file is given.
2. Google Rich Results Test (https://search.google.com/test/rich-results) for eligibility.
3. Schema Markup Validator (https://validator.schema.org/) for vocabulary.
4. After launch: Search Console enhancement reports.
