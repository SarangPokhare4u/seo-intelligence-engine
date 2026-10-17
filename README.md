# seo-intelligence-engine

A Claude Agent Skill for end-to-end SEO: it checks current Google Search Central guidance at the start of each substantive task, routes the request to one of eleven workflows, researches with whatever tools the environment provides, produces the finished deliverable, validates it, and labels every finding by provenance.

Version 1.0.0 | Knowledge snapshot: 2026-10-17

## Contents
- Install
- What it needs (capabilities)
- How to invoke
- Workflows
- Output formats
- Scripts
- Directory structure
- Running tests
- Extending the skill
- Limitations

## Install

**Claude apps (claude.ai / desktop / Cowork)**: Settings > Capabilities (or Features) > Skills > Upload skill > choose `seo-intelligence-engine.zip`. Code execution must be enabled. The ZIP contains the `seo-intelligence-engine/` folder at its root.

**Claude Code**: unzip into `~/.claude/skills/` (personal) or `<project>/.claude/skills/` (project). No upload step.

**Claude API**: upload via the Skills API (`/v1/skills`) and reference the skill_id in the container. Note: API code execution has no network access, so the refresh step will report `previously verified` unless web tools are supplied separately.

## What it needs

| Capability | Required? | Effect if missing |
|---|---|---|
| Web fetch/search (or a browser tool) | Strongly recommended | Refresh falls back to the 2026-10-17 knowledge snapshot and says so; SERPs cannot be observed |
| Code execution (Python 3.9+) | Recommended | Validators and clustering cannot run; checks are done by hand and noted |
| Shell internet access | Optional | Enables `fetch_updates.py --live`; otherwise feed results from web tools via `--input` |
| Search Console / GA4 / Ads / PSI / Bing WMT / Ahrefs / Semrush / Moz | Optional | Metrics marked `unavailable`; qualitative analysis instead |
| File persistence (Claude Code, connected folder, project) | Optional | Needed to keep snapshots between sessions |

No secrets are stored in the skill. Use read-only API scopes.

## How to invoke

Name the skill or just ask an SEO question. Examples:

1. "Use seo-intelligence-engine to research keywords for my B2B SaaS website targeting logistics managers in the United States. Prioritize conversion-intent keywords and create a keyword map."
2. "Audit https://example.com for technical SEO, content gaps, internal linking issues, and AI search discoverability."
3. "Write a comprehensive SEO blog on reducing vehicle inspection delays. Research keywords, analyze competitors, and create publish-ready content."
4. "Create a conversion-focused product landing page for an automotive logistics technology platform targeting fleet operations directors."
5. "Research ethical backlink opportunities for my website and prepare a prospect list with verified publications and outreach angles."
6. "Check Google's latest SEO documentation changes and tell me whether our current content strategy needs to change."

Every substantive answer opens with an **SEO Intelligence Brief** (date checked, verification status, relevant changes, what changed in the recommendations, sources) and closes with a **quality report** (checks passed, issues, corrections, uncertainties, human-review items).

## Workflows

| ID | Workflow | File | Typical output |
|---|---|---|---|
| A | New website strategy | workflows/website-strategy.md | Strategy doc, keyword map, architecture, roadmap |
| B | SEO audit | workflows/seo-audit.md | Audit report, issues CSV, implementation plan |
| C | Keyword research | workflows/keyword-research.md | Keyword map CSV, clusters, page mapping |
| D | Blog creation | workflows/blog-creation.md | Brief, article, metadata, schema, QA |
| E | Landing page | workflows/landing-page-creation.md | Copy deck, metadata, CTAs, schema, dev notes |
| F | Off-page / backlinks | workflows/backlink-prospecting.md | Prospect CSV, PR concept, outreach drafts |
| G | Content refresh | workflows/content-refresh.md | Diagnosis, change list, rewritten copy |
| H | Traffic recovery | workflows/traffic-recovery.md | Root-cause analysis, recovery plan |
| I | AI search visibility | workflows/ai-search-audit.md | Platform guidance, observation table, actions, measurement |
| J | Content calendar | workflows/content-calendar.md | Editorial calendar CSV |
| - | Competitor research | workflows/competitor-research.md | Competitor report, opportunity CSV |

## Output formats

Markdown (reports, copy), CSV (keyword maps, audits, prospects, calendars), JSON-LD (schema), JSON (snapshots, machine-readable audits), HTML (approved page builds), XLSX/DOCX when the environment has those skills and you ask for them.

## Scripts

All standard-library Python; none call paid APIs; none invent data.

| Script | Purpose |
|---|---|
| scripts/fetch_updates.py | Build a dated snapshot from the live RSS + Status Dashboard JSON (`--live`), saved files, or entries gathered with web tools (`--input`) |
| scripts/compare_updates.py | Diff two snapshots: added, status changes, aged out |
| scripts/cluster_keywords.py | SERP-overlap clustering; lexical fallback clearly labeled |
| scripts/validate_metadata.py | Title/description length, approximate pixel truncation risk, duplicates, stuffing signals |
| scripts/validate_internal_links.py | Orphans, unknown targets, generic/ambiguous anchors, pillar-cluster linking rules |
| scripts/validate_schema.py | JSON-LD syntax, deprecated types, required properties, visible-content alignment |
| scripts/validate_skill.py | Skill structure, frontmatter limits, links, templates, script compilation |

## Directory structure

```text
seo-intelligence-engine/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── references/
│   ├── official-source-registry.md
│   ├── google-search-guidelines.md
│   ├── seo-update-protocol.md
│   ├── keyword-research.md
│   ├── search-intent-serp-analysis.md
│   ├── technical-seo.md
│   ├── on-page-seo.md
│   ├── off-page-seo.md
│   ├── content-writing.md
│   ├── topical-authority.md
│   ├── competitor-analysis.md
│   ├── ai-search-optimization.md
│   ├── structured-data.md
│   ├── local-international-seo.md
│   ├── multimodal-search.md
│   ├── analytics-measurement.md
│   └── compliance-quality-control.md
├── workflows/
│   ├── website-strategy.md
│   ├── seo-audit.md
│   ├── keyword-research.md
│   ├── blog-creation.md
│   ├── landing-page-creation.md
│   ├── content-refresh.md
│   ├── competitor-research.md
│   ├── backlink-prospecting.md
│   ├── ai-search-audit.md
│   ├── traffic-recovery.md
│   └── content-calendar.md
├── templates/
│   ├── keyword-map.csv
│   ├── seo-audit.csv
│   ├── content-brief.md
│   ├── blog-template.md
│   ├── landing-page-template.md
│   ├── backlink-prospects.csv
│   ├── editorial-calendar.csv
│   ├── seo-report.md
│   └── update-log.md
├── scripts/
│   ├── fetch_updates.py
│   ├── compare_updates.py
│   ├── cluster_keywords.py
│   ├── validate_metadata.py
│   ├── validate_internal_links.py
│   ├── validate_schema.py
│   └── validate_skill.py
├── tests/
│   ├── test_skill_structure.py
│   ├── test_source_refresh.py
│   ├── test_keyword_research.py
│   ├── test_validators.py
│   ├── test_content_generation.md
│   ├── test_seo_audit.md
│   └── sample_test_cases.md
└── knowledge/
    ├── latest-verified-updates.md
    ├── research-sources.md
    ├── research-methodology.md
    └── snapshots/
        └── 2026-10-17.json
```

`tests/fixtures/` holds clearly labeled sample inputs for the unit tests.

## Running tests

```bash
cd seo-intelligence-engine
python3 scripts/validate_skill.py
python3 -m pytest tests -q          # requires: pip install pytest
```

Behavioral tests (`tests/*.md`) are prompts plus pass criteria to run in a Claude session.

## Extending the skill

- **New workflow**: add `workflows/<name>.md` with Input/Output/Load/Checklist, then add one row to the routing table in SKILL.md (keep SKILL.md under 500 lines).
- **New reference**: add `references/<name>.md`; include a Contents section if over 100 lines; link it from SKILL.md directly (references stay one level deep).
- **Update knowledge**: after a verified refresh, add entries to `knowledge/latest-verified-updates.md` and save a new snapshot in `knowledge/snapshots/`; bump CHANGELOG.
- **Brand voice**: keep brand rules in a separate brand skill or file; content workflows load it when present.
- **Tool integration**: document it in references/analytics-measurement.md section 7 (data, auth, fields, errors, fallback, freshness).
- Re-run `python3 scripts/validate_skill.py` and the tests before re-packaging.

## Limitations

- The update check runs only when the skill runs; it is not a background monitor.
- "Freshly verified" requires live web access in that session.
- Web search tools do not expose full SERP features; the skill marks features unverified instead of guessing.
- Third-party metrics (volume, KD, DR/DA) are vendor estimates.
- The skill drafts outreach and page changes; it does not send or publish without explicit approval.
