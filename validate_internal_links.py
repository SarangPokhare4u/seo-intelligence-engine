#!/usr/bin/env python3
"""Validate an internal link graph.

Usage:
  python3 scripts/validate_internal_links.py --links links.csv
      [--sitemap-urls urls.txt] [--cluster-map clusters.csv] [--json]

links.csv      columns: source,target[,anchor]  (e.g. Screaming Frog "All Inlinks"
               export reduced to these columns, or links planned in a content brief)
urls.txt       one canonical URL per line (sitemap or intended page list)
clusters.csv   columns: url,cluster,role  where role is pillar | cluster | commercial

Checks:
  - orphan pages: in the URL list but receive no internal links (ERROR)
  - links to URLs not in the URL list (WARNING: possibly broken, redirected or non-canonical)
  - generic anchors ("click here", "read more", ...) (WARNING)
  - one anchor text pointing to multiple targets (WARNING)
  - self links (INFO)
  - cluster rules: each cluster page links to its pillar; pillar links to every
    cluster page; each cluster page links to >= 1 commercial page in its cluster (ERROR/WARNING)

No HTTP requests are made; status codes must come from a crawl export.
Exit codes: 0 = no errors, 1 = errors or bad input.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

GENERIC_ANCHORS = {
    "click here", "here", "read more", "learn more", "more", "this", "link", "this page",
    "find out more", "see more", "details", "go", "continue",
}


def norm(u: str) -> str:
    u = (u or "").strip()
    u = re.sub(r"^https?://(www\.)?[^/]+", "", u, flags=re.I) or "/"
    u = u.split("#")[0].split("?")[0]
    if not u.endswith("/") and "." not in u.rsplit("/", 1)[-1]:
        u += "/"
    return u.lower()


def read_csv(path: Path, required: set) -> list[dict]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        cols = {c.lower().strip(): c for c in (reader.fieldnames or [])}
        missing = required - cols.keys()
        if missing:
            raise ValueError(f"{path.name} missing columns: {sorted(missing)}")
        return [{k: (row.get(v) or "").strip() for k, v in cols.items()} for row in reader]


def analyze(links, urls=None, clusters=None) -> list[dict]:
    issues = []
    add = lambda sev, check, msg: issues.append({"severity": sev, "check": check, "message": msg})  # noqa: E731
    inbound = defaultdict(set)
    outbound = defaultdict(set)
    anchors = defaultdict(set)
    for l in links:
        s, t, a = norm(l["source"]), norm(l["target"]), (l.get("anchor") or "").strip()
        if s == t:
            add("info", "self-link", f"{s} links to itself")
            continue
        inbound[t].add(s)
        outbound[s].add(t)
        if a:
            if a.lower() in GENERIC_ANCHORS:
                add("warning", "generic-anchor", f"'{a}' on {s} -> {t}")
            anchors[a.lower()].add(t)
    for a, targets in anchors.items():
        if len(targets) > 1 and a not in GENERIC_ANCHORS:
            add("warning", "anchor-ambiguity", f"anchor '{a}' points to {len(targets)} URLs: {sorted(targets)}")
    if urls is not None:
        url_set = {norm(u) for u in urls}
        homepage = "/"
        for u in sorted(url_set):
            if u != homepage and not inbound.get(u):
                add("error", "orphan", f"{u} has no internal links pointing to it")
        for t in sorted(set(inbound) - url_set):
            add("warning", "unknown-target", f"links point to {t}, which is not in the URL list (check status/canonical)")
    if clusters:
        by_cluster = defaultdict(lambda: defaultdict(list))
        for c in clusters:
            by_cluster[c["cluster"]][c["role"].lower()].append(norm(c["url"]))
        for name, roles in by_cluster.items():
            pillars, members, commercial = roles.get("pillar", []), roles.get("cluster", []), roles.get("commercial", [])
            if not pillars:
                add("warning", "cluster-structure", f"cluster '{name}' has no pillar page")
            for p in pillars:
                for m in members:
                    if m not in outbound.get(p, set()):
                        add("error", "pillar-to-cluster", f"pillar {p} does not link to cluster page {m} ({name})")
            for m in members:
                for p in pillars:
                    if p not in outbound.get(m, set()):
                        add("error", "cluster-to-pillar", f"cluster page {m} does not link to pillar {p} ({name})")
                if commercial and not (outbound.get(m, set()) & set(commercial)):
                    add("warning", "cluster-to-commercial", f"cluster page {m} links to no commercial page in '{name}'")
    return issues


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--links", type=Path, required=True)
    ap.add_argument("--sitemap-urls", type=Path)
    ap.add_argument("--cluster-map", type=Path)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        links = read_csv(args.links, {"source", "target"})
        urls = None
        if args.sitemap_urls:
            urls = [u for u in args.sitemap_urls.read_text(encoding="utf-8").splitlines() if u.strip() and not u.startswith("#")]
        clusters = read_csv(args.cluster_map, {"url", "cluster", "role"}) if args.cluster_map else None
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    issues = analyze(links, urls, clusters)
    errors = sum(i["severity"] == "error" for i in issues)
    warnings = sum(i["severity"] == "warning" for i in issues)
    if args.json:
        print(json.dumps({"errors": errors, "warnings": warnings, "issues": issues}, indent=2))
    else:
        for i in issues:
            print(f"[{i['severity'].upper()}] {i['check']}: {i['message']}")
        print(f"\nSummary: {len(links)} links checked; {errors} error(s), {warnings} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
