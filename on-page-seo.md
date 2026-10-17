# On-Page SEO Reference

## Contents
- Element checklist
- Title links and meta descriptions
- Headings and body
- Links, images, CTAs
- Implementation spec format

## Element checklist

| Element | Standard |
|---|---|
| Purpose | One primary purpose and one primary keyword cluster per URL |
| Intent | Page type matches the SERP's dominant intent |
| Title (`<title>`) | Unique, descriptive, front-loads the topic; brand at end if useful |
| Meta description | Unique summary that earns the click; not a ranking factor |
| H1 | Matches the page promise; may differ from the title |
| H2/H3 | Logical outline; secondary terms where they describe sections naturally |
| URL slug | Short, readable, hyphenated; do not change existing ranking URLs without a 301 plan |
| Intro | States what the page delivers in the first 100-150 words |
| Body | Complete for the intent; first-hand evidence, data, examples; no padding |
| Entities | Cover concepts a knowledgeable reader expects; no keyword stuffing |
| Internal links | 3-10 contextual links where relevant [INT]; descriptive anchors; link to the commercial next step |
| External links | Cite primary sources for claims |
| Images | Descriptive file names, alt text describing the image's content/function, dimensions set, modern formats |
| Structured data | Only supported types that match visible content (see structured-data.md) |
| CTA | One primary CTA aligned to funnel stage; secondary CTA for earlier-stage readers |
| Mobile | Readable font size, tap targets, no intrusive interstitials |

No keyword density targets, mandatory word counts, or forced FAQ sections.

## Title links and meta descriptions

- Google may rewrite title links and generate snippets from page content. Write for clarity, not to a pixel quota.
- Practical truncation guidance [INT]: titles often truncate past ~580-600 px on desktop (roughly 50-60 characters); descriptions past ~920 px (roughly 150-160 characters) on desktop, shorter on mobile. `scripts/validate_metadata.py` flags risk using an approximate pixel width model and reports it as risk, not error.
- Avoid boilerplate titles across many pages, keyword lists, all caps, and misleading claims.

## Headings and body

- Write the outline from the reader's questions in the order they arise.
- Use plain language; define jargon once.
- Put direct answers first, then evidence and nuance.
- Prefer tables for comparisons, numbered steps for procedures.

## Links, images, CTAs

- Anchor text describes the destination ("finished vehicle damage claims process"), not "learn more".
- Alt text: describe what is shown and why it matters; empty `alt=""` for decorative images.
- CTA mapping: TOFU -> newsletter, checklist, guide; MOFU -> comparison, case study, webinar; BOFU -> demo, pricing, quote.

## Implementation spec format

For each optimized page deliver:

```
URL: /path/
Primary keyword: ...  | Secondary: ...
Title (n chars): ...
Meta description (n chars): ...
H1: ...
Outline: H2 ... / H3 ...
Internal links to add: anchor -> target (placement)
Schema: type(s) + JSON-LD block
Images: file name | alt text | placement
CTA: primary / secondary
Dev notes: canonical, redirects, rendering, performance
QA: validate_metadata.py result, validate_schema.py result
```
