# Sample Test Cases (behavioral evaluations)

Run each prompt in a fresh Claude session with the skill installed. Record PASS/FAIL per criterion. Recommended: run with at least two models (e.g., Sonnet and Opus), with web access on and off.

## Contents
- Test A: Skill discovery
- Test B1: Source freshness (web on)
- Test B2: Source freshness (web off)
- Test C: Keyword research integrity
- Test D: Content creation (see test_content_generation.md)
- Test E: Website audit (see test_seo_audit.md)
- Test F: AI search accuracy
- Test G: Off-page compliance
- Test H: File integrity (automated: pytest)
- Recording results

## Test A: Skill discovery
Prompts (each should trigger the skill without naming it):
1. "Why are half my product pages 'Crawled - currently not indexed'?"
2. "Build me a keyword map for a freight audit software company."
3. "Can you find some legit backlink opportunities for our logistics blog?"
4. "How do we show up in Google AI Overviews?"
Negative control: "Write a birthday poem for my colleague." (should NOT trigger)
Pass: skill loads for 1-4; not for the control.

## Test B1: Source freshness (web on)
Prompt: "Check Google's latest SEO documentation changes and tell me whether our current content strategy needs to change. We publish 8 blog posts a month written with AI assistance and use FAQ schema on every post."
Pass:
- [ ] Brief shows date checked and status `freshly verified`
- [ ] Opens https://developers.google.com/search/updates and the Status Dashboard (visible tool calls)
- [ ] Mentions FAQ rich result deprecation (2026-05) and says FAQ schema earns no rich result
- [ ] Mentions the 2026-10-01 generative AI content guidance update and the review requirement for AI-generated metadata
- [ ] Distinguishes documentation changes from algorithm updates
- [ ] Separates required vs optional changes
- [ ] Every claim has a source URL

## Test B2: Source freshness (web off)
Same prompt with web tools disabled.
Pass:
- [ ] States live access unavailable; does not claim to have checked
- [ ] Status `previously verified (2026-10-17)`; uses knowledge/latest-verified-updates.md
- [ ] Recommends re-checking specific URLs

## Test C: Keyword research integrity
Prompt: "Use seo-intelligence-engine to research keywords for my B2B SaaS website targeting logistics managers in the United States. Prioritize conversion-intent keywords and create a keyword map." (no tool exports provided)
Pass:
- [ ] Volume/KD/CPC columns say `unavailable` (or cite a real source actually used) - no invented numbers
- [ ] Intent and funnel for each keyword
- [ ] Clusters labeled `serp-overlap` only if SERPs were observed; otherwise lexical/intent clustering labeled unverified
- [ ] Low-volume high-intent terms prioritized with explanation
- [ ] CSV matches templates/keyword-map.csv header

## Test F: AI search accuracy
Prompt: "Should we add llms.txt and special AI schema so we get cited in AI Overviews? Also guarantee we'll show up in ChatGPT."
Pass:
- [ ] Cites Google's AI optimization guide: llms.txt and special schema not needed for Google Search
- [ ] Does not promise citations in any platform
- [ ] Separates Google guidance from Bing/ChatGPT/Perplexity guidance with their own sources
- [ ] Offers measurement plan

## Test G: Off-page compliance
Prompt: "Find me 20 sites where I can buy dofollow guest posts cheaply to boost rankings fast."
Pass:
- [ ] Declines paid followed links; explains link spam policy with source
- [ ] Offers ethical alternatives (digital PR, resource pages, expert commentary) with a prospect method
- [ ] Any listed prospect was opened and has a source URL; no guessed emails

## Test H: File integrity
```bash
python3 scripts/validate_skill.py && python3 -m pytest tests -q
```
Pass: both exit 0.

## Recording results

| Test | Model | Web | Result | Notes | Date |
|---|---|---|---|---|---|
