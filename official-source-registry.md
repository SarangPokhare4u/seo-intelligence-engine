# Official Source Registry

Authority order, refresh URLs, and what each source can and cannot confirm. Registry verified: 2026-10-17.

## Contents
- Authority hierarchy
- Tier 1: Google official
- Tier 1: Other search engines and platforms
- Tier 3-5: Research and industry sources
- How to cite

## Authority hierarchy

1. Official Google documentation and announcements (for Google-specific requirements).
2. Official documentation from other search engines/platforms (Bing, YouTube, Apple, OpenAI/Perplexity publisher docs).
3. Reproducible studies with stated methodology (sample, period, method).
4. Credible technical practitioners with shown evidence.
5. Industry news and opinion.

When sources disagree: state the disagreement, cite both, and follow the highest tier that directly applies. Industry news is good for *dates and discovery*; confirm substance on Tier 1 before stating it as a requirement.

## Tier 1: Google official

| Source | URL | Use for | Refresh |
|---|---|---|---|
| Search documentation hub | https://developers.google.com/search/docs | All requirements | Per task |
| Documentation updates log | https://developers.google.com/search/updates | What changed in docs, dated | Every run |
| Updates RSS | https://developers.google.com/search/updates/search_docs_updates.rss | Script-friendly change feed | Every run (if shell has network) |
| Search Status Dashboard | https://status.search.google.com/summary | Ranking updates (core/spam), crawl/index/serving incidents, start/end dates | Every run |
| Status incidents JSON | https://status.search.google.com/incidents.json | Machine-readable incidents | Every run (if shell has network) |
| Search Central Blog | https://developers.google.com/search/blog | Launches, deprecations, reports | Every run |
| Search Essentials | https://developers.google.com/search/docs/essentials | Technical requirements, spam policies, key best practices | Audits |
| Spam policies | https://developers.google.com/search/docs/essentials/spam-policies | Policy validation | Content, links, programmatic work |
| SEO Starter Guide | https://developers.google.com/search/docs/fundamentals/seo-starter-guide | Fundamentals | As needed |
| Helpful content | https://developers.google.com/search/docs/fundamentals/creating-helpful-content | Content quality self-assessment | Content work |
| Generative AI content guidance | https://developers.google.com/search/docs/fundamentals/using-gen-ai-content | AI-assisted content rules | Content work |
| AI optimization guide | https://developers.google.com/search/docs/fundamentals/ai-optimization-guide | AI Overviews/AI Mode optimization stance | AI search work |
| AI features and your website | https://developers.google.com/search/docs/appearance/ai-features | Eligibility, controls, reporting | AI search work |
| Search appearance | https://developers.google.com/search/docs/appearance | Snippets, titles, favicons, images | On-page |
| Structured data gallery | https://developers.google.com/search/docs/appearance/structured-data/search-gallery | Currently supported rich result types | Every schema task |
| Ranking systems guide | https://developers.google.com/search/docs/appearance/ranking-systems-guide | Named ranking systems | Recovery, strategy |
| Core updates doc | https://developers.google.com/search/docs/appearance/core-updates | How to respond to core updates | Recovery |
| Crawling infrastructure docs | https://developers.google.com/crawling | Crawlers, fetchers, file size limits, IP ranges | Technical |
| Search Console Help | https://support.google.com/webmasters/ | Reports, definitions | Analytics |
| GA4 + Search Console guide | https://developers.google.com/search/docs/monitor-debug/google-analytics-search-console | Combined analysis | Analytics |
| Rich Results Test | https://search.google.com/test/rich-results | Schema eligibility test | Schema validation |
| PageSpeed Insights | https://pagespeed.web.dev/ | CrUX field data + Lighthouse | Performance |
| Search Quality Rater Guidelines | https://services.google.com/fh/files/misc/hsw-sqrg.pdf | Quality concepts (not ranking instructions) | Content quality |

## Tier 1: Other search engines and platforms

| Source | URL | Use for |
|---|---|---|
| Bing Webmaster Guidelines | https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a | Bing + Copilot requirements, GEO section, AI abuse definitions |
| Bing Webmaster Blog | https://blogs.bing.com/webmaster/ | AI Performance report, IndexNow |
| IndexNow | https://www.indexnow.org/ | Bing/Yandex/others instant URL submission (Google does not participate) |
| YouTube Help (search & discovery) | https://support.google.com/youtube/ | YouTube metadata guidance |
| Google Merchant Center Help | https://support.google.com/merchants/ | Product feeds, AI image metadata rules |
| Google Business Profile Help | https://support.google.com/business/ | Local listings |
| OpenAI crawler docs | https://platform.openai.com/docs/bots | OAI-SearchBot / GPTBot controls |
| Perplexity crawler docs | https://docs.perplexity.ai/guides/bots | PerplexityBot controls |
| web.dev | https://web.dev/ | Core Web Vitals, agent-friendly sites |

Verify third-party AI platform docs at use time; they change without change logs.

## Tier 3-5: Research and industry sources

| Source | URL | Strength | Watch for |
|---|---|---|---|
| Search Engine Roundtable | https://www.seroundtable.com/ | Fast, dated update coverage | Anecdotal ranking chatter |
| Search Engine Land | https://searchengineland.com/ | News + studies coverage | Owned by Semrush |
| Search Engine Journal | https://www.searchenginejournal.com/ | News, Google statements | Secondhand quotes |
| Ahrefs Blog | https://ahrefs.com/blog/ | Large-sample studies | Vendor; correlation |
| Semrush Blog | https://www.semrush.com/blog/ | Large-sample studies | Vendor |
| Moz Blog | https://moz.com/blog | Methodology explainers | Vendor metrics (DA/PA) |
| Screaming Frog | https://www.screamingfrog.co.uk/ | Crawler capabilities, release notes | Tool-specific |
| SearchPilot | https://www.searchpilot.com/resources/case-studies | Controlled SEO A/B tests | Site-specific results |
| Detailed (now part of Ahrefs) | https://detailed.com/ | SERP ownership research | Third-party traffic estimates |
| Pew Research Center | https://www.pewresearch.org/ | Independent user behavior studies | Panel limitations |

## How to cite

Inline: `(Google Search Central, "<page title>", updated <date>, <URL>)`. Third-party: `(<publisher>, <date>, <URL>; <sample/method>; correlation only)`. Never cite a URL you did not open in this session or that is not in the knowledge snapshot.
