#!/usr/bin/env python3
"""Validate JSON-LD structured data against Google rich-result basics.

Usage:
  python3 scripts/validate_schema.py FILE [FILE ...] [--json]
FILE may be .json/.jsonld (one object, a list, or an @graph) or .html (all
<script type="application/ld+json"> blocks are extracted).

Checks:
  - JSON syntax; @context is schema.org; every node has @type
  - Deprecated / no-longer-shown Google rich result types (WARNING)
  - Google-required properties for common rich result types (ERROR if missing)
  - Recommended properties (INFO)
  - For HTML input: key text values (name/headline) appear in visible page text
    (WARNING if not; markup must describe visible content)
  - Ratings/reviews present: reminder that they must be real and visible (WARNING
    if the HTML has no visible review/rating text)

The rule table reflects Google docs as verified 2026-10-17. It is a pre-check, not
a substitute for the Rich Results Test (https://search.google.com/test/rich-results).
Exit codes: 0 = no errors, 1 = errors or unreadable input.
"""
from __future__ import annotations

import argparse
import html as htmllib
import json
import re
import sys
from pathlib import Path

# type -> (required, recommended). "a|b" means at least one of a or b.
RULES = {
    "Article": ([], ["headline", "image", "datePublished", "author"]),
    "NewsArticle": ([], ["headline", "image", "datePublished", "author"]),
    "BlogPosting": ([], ["headline", "image", "datePublished", "author"]),
    "BreadcrumbList": (["itemListElement"], []),
    "ListItem": (["position"], ["name", "item"]),
    "Product": (["name", "offers|review|aggregateRating"], ["image", "description", "brand"]),
    "Offer": (["price|priceSpecification"], ["priceCurrency", "availability"]),
    "SoftwareApplication": (["name", "offers", "aggregateRating|review"], ["applicationCategory", "operatingSystem"]),
    "Organization": ([], ["name", "url", "logo"]),
    "LocalBusiness": (["name", "address"], ["telephone", "openingHoursSpecification", "geo", "url"]),
    "Event": (["name", "startDate", "location"], ["endDate", "eventStatus", "image", "description"]),
    "JobPosting": (["title", "description", "datePosted", "hiringOrganization", "jobLocation|applicantLocationRequirements"], ["validThrough", "employmentType", "baseSalary"]),
    "VideoObject": (["name", "thumbnailUrl", "uploadDate"], ["description", "contentUrl|embedUrl", "duration"]),
    "Recipe": (["name", "image"], ["author", "recipeIngredient", "recipeInstructions"]),
    "Review": (["author", "reviewRating"], ["itemReviewed", "datePublished"]),
    "AggregateRating": (["ratingValue", "ratingCount|reviewCount"], ["bestRating"]),
    "Dataset": (["name", "description"], ["license", "creator"]),
    "Course": (["name", "description"], ["provider"]),
    "ProfilePage": (["mainEntity"], []),
    "QAPage": (["mainEntity"], []),
    "DiscussionForumPosting": (["author", "datePublished"], ["text", "headline"]),
    "Movie": (["name", "image"], ["dateCreated", "director"]),
}
# LocalBusiness subtypes inherit its rules.
LOCAL_SUBTYPES = {"Restaurant", "Store", "ProfessionalService", "AutoRepair", "Dentist", "MedicalBusiness", "LegalService"}

DEPRECATED = {
    "FAQPage": "FAQ rich results stopped showing 2026-05-07 (docs removed 2026-06-15). Markup is harmless but earns no rich result.",
    "HowTo": "HowTo rich results are no longer shown.",
    "SpecialAnnouncement": "Special announcement feature deprecated (2025).",
    "ClaimReview": "Claim review rich result retired (2025).",
    "Occupation": "Estimated salary rich result retired (2025).",
}


def load_nodes(path: Path) -> tuple[list, str | None]:
    text = path.read_text(encoding="utf-8")
    page_text = None
    if path.suffix.lower() in {".html", ".htm"}:
        blocks = re.findall(r"<script[^>]*type=[\"']application/ld\+json[\"'][^>]*>(.*?)</script>", text, re.S | re.I)
        if not blocks:
            raise ValueError("no application/ld+json blocks found in HTML")
        visible = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", text, flags=re.S | re.I)
        page_text = re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", visible))).lower()
        payloads = []
        for i, b in enumerate(blocks, 1):
            try:
                payloads.append(json.loads(b))
            except json.JSONDecodeError as exc:
                raise ValueError(f"JSON-LD block {i} invalid: {exc}") from exc
    else:
        try:
            payloads = [json.loads(text)]
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON: {exc}") from exc
    nodes = []
    for p in payloads:
        items = p if isinstance(p, list) else [p]
        for it in items:
            if isinstance(it, dict) and "@graph" in it:
                ctx = it.get("@context")
                for g in it["@graph"]:
                    if isinstance(g, dict):
                        g.setdefault("@context", ctx)
                        nodes.append(g)
            elif isinstance(it, dict):
                nodes.append(it)
    return nodes, page_text


def types_of(node) -> list[str]:
    t = node.get("@type", [])
    return [x.split("/")[-1] for x in (t if isinstance(t, list) else [t]) if isinstance(x, str)]


def has(node, spec: str) -> bool:
    return any(node.get(k) not in (None, "", [], {}) for k in spec.split("|"))


def walk(node, path="$"):
    """Yield (path, node) for the node and every nested dict that has @type."""
    yield path, node
    for k, v in node.items():
        if isinstance(v, dict) and "@type" in v:
            yield from walk(v, f"{path}.{k}")
        elif isinstance(v, list):
            for i, x in enumerate(v):
                if isinstance(x, dict) and "@type" in x:
                    yield from walk(x, f"{path}.{k}[{i}]")


def validate(nodes, page_text=None) -> list[dict]:
    issues = []
    add = lambda sev, where, msg: issues.append({"severity": sev, "where": where, "message": msg})  # noqa: E731
    if not nodes:
        add("error", "$", "no JSON-LD objects found")
    for idx, top in enumerate(nodes):
        ctx = str(top.get("@context", ""))
        if "schema.org" not in ctx:
            add("error", f"node[{idx}]", f"@context should be https://schema.org (got '{ctx}')")
        for path, node in walk(top, f"node[{idx}]"):
            ts = types_of(node)
            if not ts:
                add("error", path, "missing @type")
                continue
            parent_is_review_target = ".review" in path or ".aggregateRating" in path
            for t in ts:
                if t in DEPRECATED:
                    add("warning", path, f"{t}: {DEPRECATED[t]}")
                rule = RULES.get("LocalBusiness" if t in LOCAL_SUBTYPES else t)
                if not rule:
                    continue
                required, recommended = rule
                for spec in required:
                    if t in ("Review", "AggregateRating") and spec == "itemReviewed":
                        continue
                    if not has(node, spec):
                        add("error", path, f"{t}: missing required property '{spec.replace('|', ' or ')}'")
                for spec in recommended:
                    if spec == "itemReviewed" and parent_is_review_target:
                        continue
                    if not has(node, spec):
                        add("info", path, f"{t}: recommended property '{spec.replace('|', ' or ')}' not set")
                if t == "ListItem" and not has(node, "name") and not has(node, "item"):
                    add("error", path, "ListItem needs name or item")
                if page_text is not None:
                    for key in ("headline", "name"):
                        val = node.get(key)
                        if isinstance(val, str) and len(val) > 3 and t not in ("ListItem", "Organization", "Person", "Brand"):
                            if htmllib.unescape(val).lower().strip() not in page_text:
                                add("warning", path, f"{t}.{key} '{val[:60]}' not found in visible page text")
            if any(t in ("Review", "AggregateRating") for t in ts) and page_text is not None:
                if not re.search(r"review|rating|stars?|out of 5", page_text):
                    add("warning", path, "rating/review markup but no visible review or rating text on the page")
    return issues


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    report, total_errors = [], 0
    for f in args.files:
        try:
            nodes, page_text = load_nodes(f)
            issues = validate(nodes, page_text)
        except (OSError, ValueError) as exc:
            issues = [{"severity": "error", "where": "$", "message": str(exc)}]
        total_errors += sum(i["severity"] == "error" for i in issues)
        report.append({"file": str(f), "issues": issues})
    if args.json:
        print(json.dumps({"errors": total_errors, "files": report}, indent=2))
    else:
        for r in report:
            print(f"== {r['file']}")
            for i in r["issues"] or [{"severity": "ok", "where": "", "message": "no issues"}]:
                print(f"  [{i['severity'].upper()}] {i['where']} {i['message']}")
        print(f"\nSummary: {total_errors} error(s). Confirm eligibility with the Rich Results Test.")
    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main())
