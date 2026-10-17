#!/usr/bin/env python3
"""Cluster keywords by SERP overlap (preferred) or lexical similarity (fallback).

SERP mode (method = "serp-overlap"):
  --serp-csv FILE   CSV with columns keyword,url[,position][,volume]
                    One row per ranking URL per keyword (from observed SERPs or a
                    rank-tracker export). Only rows with position <= --top are used
                    when position is present.
  --threshold N     Minimum shared URLs with a cluster's lead keyword (default 3).

  Algorithm: keywords are ordered by volume (if provided) then by number of URLs;
  each unassigned keyword becomes a cluster lead and pulls in every unassigned
  keyword sharing >= N URLs with it. This mirrors common "hard" SERP clustering.

Lexical mode (method = "lexical (unverified by SERP)"):
  --keywords FILE --lexical   One keyword per line. Groups by token Jaccard
                              similarity >= --jaccard (default 0.5) after stopword
                              removal and light stemming. Output is labeled as not
                              SERP-verified.

Output CSV: cluster_id,cluster_lead,keyword,method,shared_urls_with_lead,volume
No metrics are invented: volume is copied only if present in the input.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

# Industry tools use 3-4 shared URLs in the top 10 as a "hard" match; 3 is the
# looser end of that range and is easy to tighten with --threshold.
DEFAULT_THRESHOLD = 3
DEFAULT_TOP = 10
# 0.5 token overlap groups close variants ("x software" / "x software tools")
# without merging distinct intents.
DEFAULT_JACCARD = 0.5

STOPWORDS = {
    "a", "an", "the", "for", "of", "to", "in", "on", "and", "or", "with", "what", "is",
    "how", "best", "top", "vs", "near", "me", "do", "does", "can", "your", "my", "are",
}


def normalize_url(u: str) -> str:
    u = u.strip().lower()
    u = re.sub(r"^https?://(www\.)?", "", u)
    u = u.split("#")[0]
    return u.rstrip("/")


def read_serp(path: Path, top: int):
    urls = defaultdict(set)
    volume = {}
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        cols = {c.lower().strip(): c for c in (reader.fieldnames or [])}
        if "keyword" not in cols or "url" not in cols:
            raise ValueError("SERP CSV needs 'keyword' and 'url' columns")
        for row in reader:
            kw = (row[cols["keyword"]] or "").strip().lower()
            url = (row[cols["url"]] or "").strip()
            if not kw or not url:
                continue
            if "position" in cols and (row.get(cols["position"]) or "").strip():
                try:
                    if float(row[cols["position"]]) > top:
                        continue
                except ValueError:
                    pass
            urls[kw].add(normalize_url(url))
            if "volume" in cols and (row.get(cols["volume"]) or "").strip():
                volume[kw] = row[cols["volume"]].strip()
    if not urls:
        raise ValueError("no usable keyword,url rows found")
    return urls, volume


def _num(v):
    try:
        return float(str(v).replace(",", ""))
    except (TypeError, ValueError):
        return -1.0


def cluster_serp(urls, volume, threshold):
    order = sorted(urls, key=lambda k: (_num(volume.get(k)), len(urls[k]), k), reverse=True)
    assigned, rows, cid = set(), [], 0
    for lead in order:
        if lead in assigned:
            continue
        cid += 1
        assigned.add(lead)
        rows.append((cid, lead, lead, len(urls[lead])))
        for other in order:
            if other in assigned:
                continue
            shared = len(urls[lead] & urls[other])
            if shared >= threshold:
                assigned.add(other)
                rows.append((cid, lead, other, shared))
    return rows


def stem(tok: str) -> str:
    for suf in ("ing", "ies", "es", "s", "ed"):
        if len(tok) > len(suf) + 2 and tok.endswith(suf):
            return tok[: -len(suf)] + ("y" if suf == "ies" else "")
    return tok


def tokens(kw: str) -> set:
    return {stem(t) for t in re.findall(r"[a-z0-9]+", kw.lower()) if t not in STOPWORDS}


def cluster_lexical(keywords, jaccard):
    toks = {k: tokens(k) for k in keywords}
    order = sorted(keywords, key=lambda k: (len(toks[k]), k))
    assigned, rows, cid = set(), [], 0
    for lead in order:
        if lead in assigned:
            continue
        cid += 1
        assigned.add(lead)
        rows.append((cid, lead, lead, ""))
        for other in order:
            if other in assigned:
                continue
            a, b = toks[lead], toks[other]
            if a and b and len(a & b) / len(a | b) >= jaccard:
                assigned.add(other)
                rows.append((cid, lead, other, ""))
    return rows


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--serp-csv", type=Path)
    ap.add_argument("--keywords", type=Path)
    ap.add_argument("--lexical", action="store_true")
    ap.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD)
    ap.add_argument("--top", type=int, default=DEFAULT_TOP)
    ap.add_argument("--jaccard", type=float, default=DEFAULT_JACCARD)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args(argv)

    try:
        if args.serp_csv:
            urls, volume = read_serp(args.serp_csv, args.top)
            rows = cluster_serp(urls, volume, args.threshold)
            method = f"serp-overlap (>= {args.threshold} shared of top {args.top})"
        elif args.keywords and args.lexical:
            kws = sorted({line.strip().lower() for line in args.keywords.read_text(encoding="utf-8").splitlines() if line.strip()})
            if not kws:
                raise ValueError("keyword file is empty")
            rows = cluster_lexical(kws, args.jaccard)
            volume = {}
            method = "lexical (unverified by SERP)"
        else:
            ap.error("use --serp-csv FILE, or --keywords FILE --lexical")
            return 1
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    out = open(args.out, "w", newline="", encoding="utf-8") if args.out else sys.stdout
    try:
        w = csv.writer(out)
        w.writerow(["cluster_id", "cluster_lead", "keyword", "method", "shared_urls_with_lead", "volume"])
        for cid, lead, kw, shared in rows:
            w.writerow([cid, lead, kw, method, shared, volume.get(kw, "")])
    finally:
        if args.out:
            out.close()
    n_clusters = len({r[0] for r in rows})
    print(f"{len(rows)} keywords -> {n_clusters} clusters ({method})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
