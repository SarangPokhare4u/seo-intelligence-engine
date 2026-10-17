# Local, International, and Multilingual SEO

## Local SEO

- Google Business Profile: accurate category, hours, service areas, address (or hidden for service-area businesses), photos, products/services, Q&A, reviews responded to. Keep consistent with the site (AI features also draw on Business Profile data).
- Location pages: only for real locations or service areas with unique content (team, address, directions, local proof, services offered there). Templated city-swap pages risk doorway abuse.
- NAP consistency across site, GBP, major directories, industry associations.
- LocalBusiness markup on location pages with real data.
- Reviews: never gate, buy, or fabricate; follow GBP review policies.
- Local citations: industry and regional directories with editorial standards.

## International and multilingual

URL structures: ccTLD (example.de), subdirectory (example.com/de/), subdomain (de.example.com). Subdirectories are simplest to maintain [INT]; any can work.

Hreflang rules:
- Each page lists itself and all alternates (return tags are required).
- Language code ISO 639-1, optional region ISO 3166-1 alpha-2 (`en-GB`, `es-MX`, `pt-BR`); `x-default` for selector/fallback.
- Hreflang targets must be canonical, indexable, 200 URLs.
- Implement in HTML head, HTTP headers, or XML sitemap (one method consistently).
- Do not auto-redirect by IP/language without a way to switch; Googlebot crawls mostly from the US.

Canonicalization: localized pages self-canonicalize; never canonicalize all languages to one language.

## Localization, not translation

- Research keywords natively in each market (local tools, local SERPs, native speakers). Literal translation often misses the real term.
- Examples to check: Indian English vs US English vocabulary and spelling (e.g. "lakh/crore" units, "programme"); Spanish differs by country (es-ES vs es-MX); Japanese uses mixed scripts (kanji/katakana/hiragana) and English loanwords in katakana, so check which form searchers use; Hindi searchers frequently type Hindi in Latin script (Hinglish) as well as Devanagari.
- Keep product facts and positioning identical; adapt examples, units, currency, regulations, date formats.
- Regional competitors differ; run competitor analysis per market.
- Google feature availability varies by country (Google "regional differences" doc, 2026-09-08). Check before recommending a feature.
