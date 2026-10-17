# Test fixtures

Synthetic or structure-only samples for offline unit tests. They are NOT live data
and must never be cited as Google announcements or real SERP results.

- sample_rss.xml: RSS 2.0 sample shaped like the Search Central docs-updates feed (titles copied from the public updates page, 2026-10-17).
- sample_atom.xml: Atom variant to test the fallback parser.
- sample_incidents.json: two incidents in the documented Status Dashboard JSON structure (keys verified 2026-10-17).
- serp_rows.csv: synthetic keyword,url rows on example.* domains.
- keywords.txt: keyword list for lexical clustering.
- metadata.csv: titles/descriptions with deliberate problems.
- links.csv, sitemap_urls.txt, clusters.csv: synthetic internal link graph.
- good_schema.json, bad_schema.json, page.html: schema validation samples.
- snapshot_old.json, snapshot_new.json: snapshot diff samples.
