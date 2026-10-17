# Compliance, Prioritization, and Quality Control

Run before finalizing any deliverable. Fix, re-check, and only then deliver.

## Contents
- Prioritization engine (P0-P3)
- QA checklist: technical
- QA checklist: content
- QA checklist: policy
- QA checklist: AI search
- Final quality report format

## Prioritization engine

Score each recommendation 1-5 on: business value (V), search opportunity (O), severity (S), evidence strength (E), effort (F, 5 = easy), dependency-freedom (D, 5 = no blockers), risk if ignored (R), time sensitivity (T), confidence (C).

```
impact = (V + O + S + R + T) / 5
ease   = (F + D) / 2
trust  = (E + C) / 2
priority_score = impact * 0.5 + ease * 0.25 + trust * 0.25   (range 1-5)
```

Labels (then sanity-check by hand):
- **P0 Critical**: confirmed issue blocking access, indexing, or core functionality of important pages, or a severe policy risk (manual action, hacked content, spam pattern). Severity overrides score.
- **P1 High**: priority_score >= 3.8, strong business case.
- **P2 Medium**: 3.0-3.79.
- **P3 Low**: < 3.0 or optional.

Never label something P0 only because a checklist mentions it (e.g., a missing meta description is not P0). Forecasts: give conservative/expected/optimistic scenarios with assumptions, never guarantees.

## QA checklist: technical

- [ ] No claim that a site was crawled/audited beyond what was fetched; sample size stated.
- [ ] Indexing advice correct (robots.txt vs noindex; crawlable noindex; canonical consistency).
- [ ] No contradictory canonicals/redirects/hreflang.
- [ ] Schema types are currently supported; deprecated types not offered as rich results; `validate_schema.py` passes.
- [ ] Code examples valid (JSON parses, HTML well-formed, regex tested).
- [ ] Links in deliverable were opened or are flagged `unverified`.
- [ ] Search feature recommendations re-checked against Phase 2 findings.

## QA checklist: content

- [ ] Matches dominant search intent; page has one purpose.
- [ ] Primary keyword in title/H1/intro naturally; no stuffing.
- [ ] Original value stated (data, experience, framework, example) and present.
- [ ] Every statistic/claim has a source or is flagged `needs confirmation`.
- [ ] No invented testimonials, customers, quotes, numbers, awards.
- [ ] No duplicate sections; heading hierarchy logical (one H1, nested H2/H3).
- [ ] Brand voice rules applied (list them).
- [ ] CTA matches funnel stage.
- [ ] Banned patterns absent (see content-writing.md).
- [ ] `validate_metadata.py` run on title/description.

## QA checklist: policy

Flag and remove: keyword stuffing; scaled content abuse (many low-value near-duplicates, templated programmatic pages without unique value); doorway pages; cloaking; link spam (paid/exchanged/guest links without qualification); site reputation abuse (third-party content riding host signals); fake or incentivized undisclosed reviews; misleading structured data; back button hijacking or deceptive UX; manipulation of AI responses; thin affiliate content.

## QA checklist: AI search

- [ ] Platform-specific claims cite that platform's own documentation.
- [ ] No promised AI inclusion or citations.
- [ ] No llms.txt/special schema/chunking presented as Google requirements.
- [ ] Recommendations help users, not only machines.
- [ ] Study figures presented with publisher, date, method, and "correlation" caveats.

## Final quality report format

```
Quality report
Checks passed: <list>
Issues found: <list>
Corrections applied: <list>
Remaining uncertainties: <data unavailable, unverified sources, assumptions>
Human review required: <product facts, legal/regulatory claims, stats to confirm, brand approval>
Data provenance: <sources + dates>
```

Do not assign scores that imply Google endorsement (no "Google SEO score 92/100").
