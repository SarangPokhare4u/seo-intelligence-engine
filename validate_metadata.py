#!/usr/bin/env python3
"""Validate SEO titles and meta descriptions.

Usage:
  python3 scripts/validate_metadata.py --title "..." --description "..." [--keyword "..."]
  python3 scripts/validate_metadata.py --csv pages.csv   # columns: url,title,description[,keyword]

Checks: empty, character length, approximate rendered pixel width (truncation
risk), keyword presence, duplicates across rows, ALL CAPS, repeated words
(stuffing signal), separator spam, placeholder text, em dashes (optional brand
rule via --no-em-dash).

Pixel widths are an approximation of Google's desktop SERP fonts (Arial-like,
~20px titles, ~14px descriptions). Truncation is reported as a WARNING (risk),
never an error, because Google rewrites and truncates dynamically.

Exit codes: 0 = no errors (warnings allowed), 1 = errors found or bad input.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

# Commonly observed desktop truncation points (industry measurement, not a Google spec).
TITLE_MAX_PX = 600
DESC_MAX_PX = 920
TITLE_MIN_CHARS = 15
DESC_MIN_CHARS = 50

# Approximate Arial advance widths at 20px for titles. Description font is
# ~14px, so description widths are scaled by 14/20.
NARROW = set("iljtfrI.,:;'|!()[] ")
WIDE = set("mwMW@%")
UPPER_WIDE = set("ABCDEFGHKNOPQRSUVXYZ&")
DESC_SCALE = 14 / 20


def char_px(c: str) -> float:
    if c == " ":
        return 5.6
    if c in NARROW:
        return 5.6
    if c in WIDE:
        return 16.7
    if c in UPPER_WIDE:
        return 13.3
    if c.isupper():
        return 12.2
    if c.isdigit():
        return 11.1
    if ord(c) > 0x2E80:  # CJK and similar full-width scripts
        return 20.0
    return 10.0


def px_width(text: str, scale: float = 1.0) -> float:
    return round(sum(char_px(c) for c in text) * scale, 1)


PLACEHOLDER = re.compile(r"lorem ipsum|\[confirm|\btbd\b|\btodo\b|<.*?>|\{\{|xxx", re.I)


def check(title: str | None, desc: str | None, keyword: str | None, no_em_dash: bool) -> list[dict]:
    issues = []

    def add(sev, field, msg):
        issues.append({"severity": sev, "field": field, "message": msg})

    for field, text, max_px, min_chars, scale in (
        ("title", title, TITLE_MAX_PX, TITLE_MIN_CHARS, 1.0),
        ("description", desc, DESC_MAX_PX, DESC_MIN_CHARS, DESC_SCALE),
    ):
        if text is None:
            continue
        t = text.strip()
        if not t:
            add("error", field, "empty")
            continue
        width = px_width(t, scale)
        add("info", field, f"{len(t)} chars, ~{width}px (limit ~{max_px}px)")
        if width > max_px:
            add("warning", field, f"truncation risk: ~{width}px exceeds ~{max_px}px")
        if len(t) < min_chars:
            add("warning", field, f"short ({len(t)} chars); may be rewritten or under-describe the page")
        if PLACEHOLDER.search(t):
            add("error", field, "contains placeholder or markup text")
        letters = [c for c in t if c.isalpha()]
        if letters and sum(c.isupper() for c in letters) / len(letters) > 0.7 and len(letters) > 10:
            add("warning", field, "mostly uppercase")
        words = [w for w in re.findall(r"[a-z0-9]+", t.lower()) if len(w) > 3]
        rep = [w for w, n in Counter(words).items() if n >= 3]
        if rep:
            add("warning", field, f"repeated words {rep} (possible stuffing)")
        # Count spaced separators and pipes only, so hyphenated words don't trigger it.
        if len(re.findall(r"\s[\-–—]\s|\||:\s", t)) >= 3:
            add("warning", field, "many separators (keyword list pattern)")
        if no_em_dash and "—" in t:
            add("error", field, "contains em dash (brand rule)")
        if keyword:
            if keyword.lower() not in t.lower():
                sev = "warning" if field == "title" else "info"
                add(sev, field, f"primary keyword '{keyword}' not present verbatim")
            elif field == "title" and t.lower().find(keyword.lower()) > len(t) / 2:
                add("info", field, "keyword appears in second half of title; consider front-loading")
    return issues


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--title")
    ap.add_argument("--description")
    ap.add_argument("--keyword")
    ap.add_argument("--csv", type=Path)
    ap.add_argument("--no-em-dash", action="store_true", help="treat em dashes as errors (brand rule)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    results = []
    if args.csv:
        try:
            with args.csv.open(newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                cols = {c.lower().strip(): c for c in (reader.fieldnames or [])}
                if "title" not in cols and "description" not in cols:
                    print("ERROR: CSV needs 'title' and/or 'description' columns", file=sys.stderr)
                    return 1
                rows = list(reader)
        except OSError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        get = lambda r, c: r.get(cols[c]) if c in cols else None  # noqa: E731
        titles = Counter((get(r, "title") or "").strip().lower() for r in rows if get(r, "title"))
        descs = Counter((get(r, "description") or "").strip().lower() for r in rows if get(r, "description"))
        for i, r in enumerate(rows, start=2):
            ident = get(r, "url") or f"row {i}"
            issues = check(get(r, "title"), get(r, "description"), get(r, "keyword"), args.no_em_dash)
            t = (get(r, "title") or "").strip().lower()
            d = (get(r, "description") or "").strip().lower()
            if t and titles[t] > 1:
                issues.append({"severity": "error", "field": "title", "message": f"duplicate title ({titles[t]} pages)"})
            if d and descs[d] > 1:
                issues.append({"severity": "warning", "field": "description", "message": f"duplicate description ({descs[d]} pages)"})
            results.append({"page": ident, "issues": issues})
    elif args.title is not None or args.description is not None:
        results.append({"page": "input", "issues": check(args.title, args.description, args.keyword, args.no_em_dash)})
    else:
        ap.error("provide --title/--description or --csv")

    errors = sum(1 for r in results for i in r["issues"] if i["severity"] == "error")
    warnings = sum(1 for r in results for i in r["issues"] if i["severity"] == "warning")
    if args.json:
        print(json.dumps({"errors": errors, "warnings": warnings, "results": results}, indent=2))
    else:
        for r in results:
            print(f"== {r['page']}")
            for i in r["issues"]:
                print(f"  [{i['severity'].upper()}] {i['field']}: {i['message']}")
        print(f"\nSummary: {errors} error(s), {warnings} warning(s). Pixel widths are approximate.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
