# Topic Clusters and Topical Authority

"Topical authority" is an editorial planning principle here, not a Google metric or a ranking guarantee.

## Building the topic map

1. List the business's products, the problems they solve, buyer roles, industries, and use cases.
2. List buyer questions per journey stage (problem-aware, solution-aware, vendor-aware, decision, post-purchase).
3. Add entities: standards, regulations, processes, metrics, tools, roles.
4. Group into pillars (broad topics the business must be known for) and clusters (specific subtopics).
5. Assign each cluster: one primary keyword group, one URL, one intent, one conversion destination.
6. Remove clusters that would produce near-duplicate pages; merge them.

## Cluster specification

| Field | Content |
|---|---|
| Cluster name | |
| Target audience | role + seniority |
| Primary intent | |
| Business objective | e.g. demo requests for Product X |
| Priority keyword group | from keyword map |
| Pillar page | URL |
| Supporting content | URLs (existing or proposed) with formats |
| Commercial pages | product/solution pages it should feed |
| URL structure | e.g. /resources/<topic>/<subtopic>/ or flat /blog/<slug>/ (choose one and keep it) |
| Linking strategy | pillar <-> cluster; cluster -> commercial page with descriptive anchor; cross-links between siblings only when relevant |
| Journey stage | TOFU/MOFU/BOFU |
| Conversion destination | CTA + URL |

## Linking rules

- Every cluster page links to its pillar and at least one commercial page.
- Pillar links to every cluster page.
- Commercial pages link to the 2-3 most helpful cluster pages for evaluation-stage questions.
- Validate with `scripts/validate_internal_links.py` (orphans, missing pillar links, broken targets).

## Sequencing

Publish order: commercial pages that already have demand first, then the pillar, then the clusters with the highest priority scores. Fill gaps where GSC shows impressions without a matching page.

## Guardrails

No pages created only to target keyword variants; no programmatic location/industry pages without unique, useful content per page (scaled content abuse and doorway policies).
