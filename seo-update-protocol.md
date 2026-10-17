# SEO Update Protocol (seo-update-monitor)

Runs at the start of every substantive invocation. It is not a background service: it runs only when the skill runs.

## Contents
- Step 1: Date and market
- Step 2: Check official sources
- Step 3: Analyze each update
- Step 4: Apply to the current task
- Step 5: Intelligence Brief
- Snapshots and diffs (scripts)
- Failure handling
- Classification rules

## Step 1: Date and market

```bash
date -u +%F
```
Record target country/language. Some features are regional (see Google's "regional differences" doc, 2026-09-08).

## Step 2: Check official sources

Order and what to extract:

| # | Source | Extract |
|---|---|---|
| 1 | https://developers.google.com/search/updates | Every entry in the window: date, title, one-line change |
| 2 | https://status.search.google.com/summary | Ranking incidents (name, start, end/duration, status); crawling/indexing/serving incidents |
| 3 | https://developers.google.com/search/blog | Posts in the window (launches, deprecations, reporting) |
| 4 | Task-specific page(s) | e.g. spam policies, AI features, structured data gallery, the doc for any feature being recommended |
| 5 | Optional cross-check | Search Engine Roundtable / Search Engine Land for exact rollout completion dates |

Window: 90 days by default. Extend to 12 months for ranking updates, indexing/crawling behavior, spam policy, or rich-result support whenever the task touches those areas.

Tooling: use WebFetch (ask for "every entry with date and title"), WebSearch, or a browser tool. If a page summarization truncates, fetch again with an offset. Do not rely on memory for dates.

## Step 3: Analyze each relevant update

Record per item (use [templates/update-log.md](../templates/update-log.md) fields):

- announcement date; source URL; title
- class (see rules below)
- what changed (one sentence, Google's wording where possible)
- effective / rollout dates; rollout status: `announced`, `rolling out`, `complete`, `deprecated`
- affected site types
- impact area: technical / on-page / off-page / content / measurement / AI search
- action: `required`, `recommended`, `monitor`, `none`
- verification: `verified on Tier 1`, `Tier 1 page not loaded (secondary only)`, `unverified`

## Step 4: Apply to the current task

Examples of mandatory adjustments:
- Rich result deprecated -> remove from opportunities; keep markup only if harmless and still useful for other consumers.
- Gen-AI content guidance changed -> update content QA checklist.
- Crawl/index doc changed -> update audit checks.
- Core or spam update overlaps a traffic change window -> add as a hypothesis in recovery work (never as a conclusion without evidence).
- New Search Console report -> add to measurement plan if available for the property.

## Step 5: SEO Intelligence Brief

Five lines maximum per item; omit unrelated updates.

```
SEO Intelligence Brief
Checked: 2026-10-17 (UTC) | Market: US | Status: freshly verified
Relevant changes:
- 2026-05-08 | FAQ rich result deprecated | feature deprecation | do not propose FAQ rich results | developers.google.com/search/updates
Applied to this task: removed FAQ rich-result recommendation; FAQ content kept only where users need it.
Sources consulted: <URLs>
```

Status values: `freshly verified` (Tier 1 pages loaded this session), `previously verified (<date>)` (from knowledge snapshot), `unverified` (nothing loaded and no snapshot covers it).

## Snapshots and diffs (scripts)

Normalize what was found into JSON (list of objects with `date`, `title`, `source`, `class`, `url`, optional `summary`, `status`):

```bash
python3 scripts/fetch_updates.py --input found.json --out knowledge/snapshots/$(date -u +%F).json
python3 scripts/compare_updates.py knowledge/snapshots/<previous>.json knowledge/snapshots/<today>.json
```

If the shell has internet:
```bash
python3 scripts/fetch_updates.py --live --days 90 --out knowledge/snapshots/$(date -u +%F).json
```
`--live` pulls the docs-updates RSS and the Status Dashboard incidents JSON. On any network error it exits non-zero, prints the failing source, and writes nothing (or writes only sources that succeeded, flagged `partial: true`).

## Failure handling

- WebFetch blocked or empty: try WebSearch with `site:developers.google.com/search` and the month; then a browser tool; then the snapshot.
- Say exactly which sources failed. Never write "I checked" for a source that did not load.
- Persisted snapshots only exist if the environment keeps files (Claude Code, a connected folder, a project). In ephemeral environments, include the brief in the deliverable instead.

## Classification rules

| Class | Definition | Example |
|---|---|---|
| algorithm update | Ranking system change announced on Status Dashboard | March 2026 core update |
| documentation change | Docs clarified/moved without stated behavior change | Googlebot 2 MB limit doc (2026-02-03) |
| policy change | Spam/content policy added or altered | Back button hijacking policy (2026-04-13) |
| feature launch | New search feature or markup support | Preferred sources |
| feature deprecation | Feature removed from results | FAQ rich results (2026-05-07) |
| reporting change | Search Console/analytics change | Generative AI performance reports |
| incident | Crawling/indexing/serving outage | 2026-02-24 serving issue (15 min) |

Never relabel a documentation change as an algorithm update, and never name an update that is not on the Status Dashboard or Search Central blog.
