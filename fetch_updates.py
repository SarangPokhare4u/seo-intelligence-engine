#!/usr/bin/env python3
"""Build a normalized snapshot of Google Search updates.

Modes (combine as needed):
  --live                 Fetch the Search Central docs-updates RSS feed and the
                         Search Status Dashboard incidents JSON over HTTP.
  --rss-file PATH        Parse a saved copy of the RSS/Atom feed.
  --incidents-file PATH  Parse a saved copy of incidents.json.
  --input PATH           Normalize entries Claude gathered with web tools
                         (JSON list, or {"entries": [...]}).

Output: JSON snapshot {generated_at, mode, partial, window_days, sources, entries}.
Never invents entries. If a source fails, it is recorded in `sources` with the
error and the snapshot is flagged partial. If every requested source fails the
script exits 1 and writes nothing.

Exit codes: 0 = all requested sources OK, 2 = partial, 1 = nothing usable / bad input.
Standard library only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import email.utils
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

RSS_URL = "https://developers.google.com/search/updates/search_docs_updates.rss"
INCIDENTS_URL = "https://status.search.google.com/incidents.json"
# Official pages usually answer within a few seconds; 20 s tolerates slow proxies.
REQUEST_TIMEOUT_S = 20
# Default look-back window used by the update protocol (references/seo-update-protocol.md).
DEFAULT_WINDOW_DAYS = 90
USER_AGENT = "seo-intelligence-engine/1.0 (+update-check)"

VALID_CLASSES = {
    "algorithm update",
    "documentation change",
    "policy change",
    "feature launch",
    "feature deprecation",
    "reporting change",
    "incident",
}
VALID_STATUS = {"announced", "rolling out", "complete", "deprecated", "unknown"}

# Ordered keyword rules for classifying documentation titles. First match wins.
CLASS_RULES = [
    (r"deprecat|removing documentation|no longer (shown|available|supported)|retir", "feature deprecation"),
    (r"spam polic|new spam|site reputation|policy|guideline", "policy change"),
    (r"search console|report|analytics", "reporting change"),
    # No title rule ever yields "algorithm update": only Status Dashboard ranking
    # incidents (or an explicit class in --input) may carry that label, so a doc
    # page that merely mentions "core updates" stays a documentation change.
    (r"^(introducing|launching|adding (a )?new|new )|now available|is available|expanding", "feature launch"),
]


def classify_title(title: str) -> str:
    t = title.lower().strip()
    for pattern, cls in CLASS_RULES:
        if re.search(pattern, t):
            return cls
    return "documentation change"


def parse_date(value) -> str | None:
    """Return YYYY-MM-DD for RFC 822, ISO 8601, or YYYY-MM-DD strings; None if unparseable."""
    if value is None:
        return None
    s = str(value).strip()
    if not s:
        return None
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        try:
            dt.date.fromisoformat(s)
            return s
        except ValueError:
            return None
    try:
        parsed = email.utils.parsedate_to_datetime(s)
        if parsed is not None:
            return parsed.date().isoformat()
    except (TypeError, ValueError, IndexError):
        pass
    try:
        return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return None


def http_get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_S) as resp:  # noqa: S310 (fixed https URLs)
        if resp.status != 200:
            raise urllib.error.HTTPError(url, resp.status, "non-200 response", resp.headers, None)
        return resp.read()


def _text(el, names):
    for n in names:
        found = el.find(n)
        if found is not None:
            if found.text and found.text.strip():
                return found.text.strip()
            href = found.get("href")
            if href:
                return href.strip()
    return None


def parse_feed(data: bytes) -> list[dict]:
    """Parse RSS 2.0 or Atom bytes into entries. Raises ValueError on malformed XML."""
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise ValueError(f"feed is not valid XML: {exc}") from exc
    atom = "{http://www.w3.org/2005/Atom}"
    items = root.findall(".//item")
    entries = []
    if items:
        for it in items:
            title = _text(it, ["title"])
            if not title:
                continue
            entries.append({
                "date": parse_date(_text(it, ["pubDate", "{http://purl.org/dc/elements/1.1/}date"])),
                "title": title,
                "url": _text(it, ["link", "guid"]),
                "summary": _strip_html(_text(it, ["description"]) or "")[:300],
            })
    else:
        for it in root.findall(f".//{atom}entry"):
            title = _text(it, [f"{atom}title"])
            if not title:
                continue
            entries.append({
                "date": parse_date(_text(it, [f"{atom}updated", f"{atom}published"])),
                "title": title,
                "url": _text(it, [f"{atom}link", f"{atom}id"]),
                "summary": _strip_html(_text(it, [f"{atom}summary", f"{atom}content"]) or "")[:300],
            })
    if not entries and root.tag not in ("rss", f"{atom}feed"):
        raise ValueError(f"unrecognized feed root element: {root.tag}")
    for e in entries:
        e["source"] = "docs_updates"
        e["class"] = classify_title(e["title"])
        e["status"] = "deprecated" if e["class"] == "feature deprecation" else "complete"
    return entries


def _strip_html(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def parse_incidents(data: bytes) -> list[dict]:
    try:
        payload = json.loads(data)
    except json.JSONDecodeError as exc:
        raise ValueError(f"incidents payload is not JSON: {exc}") from exc
    if not isinstance(payload, list):
        raise ValueError("incidents payload is not a JSON array")
    entries = []
    for inc in payload:
        if not isinstance(inc, dict):
            continue
        title = (inc.get("external_desc") or "").strip()
        if not title:
            continue
        service = (inc.get("service_name") or "").strip()
        end = parse_date(inc.get("end"))
        latest = inc.get("most_recent_update") or {}
        entries.append({
            "date": parse_date(inc.get("begin")),
            "end_date": end,
            "title": title,
            "service": service,
            "source": "status_dashboard",
            "class": "algorithm update" if service.lower() == "ranking" else "incident",
            "status": "complete" if end else "rolling out",
            "url": "https://status.search.google.com/" + str(inc.get("uri", "")).lstrip("/"),
            "summary": _strip_html(str(latest.get("text", "")))[:300],
        })
    return entries


def normalize_input(path: Path) -> list[dict]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"input file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"input file is not valid JSON: {exc}") from exc
    if isinstance(payload, dict):
        payload = payload.get("entries", [])
    if not isinstance(payload, list):
        raise ValueError("input must be a JSON list of entries or {'entries': [...]}")
    out, problems = [], []
    for i, raw in enumerate(payload):
        if not isinstance(raw, dict):
            problems.append(f"entry {i}: not an object")
            continue
        title = str(raw.get("title", "")).strip()
        date = parse_date(raw.get("date"))
        if not title:
            problems.append(f"entry {i}: missing title")
            continue
        if not date:
            problems.append(f"entry {i} ('{title[:40]}'): missing or unparseable date")
            continue
        cls = str(raw.get("class") or classify_title(title)).lower()
        if cls not in VALID_CLASSES:
            problems.append(f"entry {i}: unknown class '{cls}', reclassified")
            cls = classify_title(title)
        status = str(raw.get("status") or "unknown").lower()
        if status not in VALID_STATUS:
            status = "unknown"
        entry = {
            "date": date,
            "title": title,
            "source": str(raw.get("source") or "manual"),
            "class": cls,
            "status": status,
            "url": raw.get("url"),
            "summary": str(raw.get("summary", ""))[:300],
        }
        if raw.get("end_date"):
            entry["end_date"] = parse_date(raw.get("end_date"))
        out.append(entry)
    for p in problems:
        print(f"WARNING: {p}", file=sys.stderr)
    return out


def within_window(entries, days, today):
    if days is None:
        return entries
    cutoff = today - dt.timedelta(days=days)
    kept = []
    for e in entries:
        d = e.get("date")
        end = e.get("end_date")
        try:
            if (d and dt.date.fromisoformat(d) >= cutoff) or (end and dt.date.fromisoformat(end) >= cutoff):
                kept.append(e)
        except ValueError:
            continue
    return kept


def dedupe(entries):
    seen, out = set(), []
    for e in entries:
        key = (e.get("source"), re.sub(r"\W+", " ", e["title"].lower()).strip(), e.get("date"))
        if key in seen:
            continue
        seen.add(key)
        out.append(e)
    return sorted(out, key=lambda e: (e.get("date") or "", e["title"]), reverse=True)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--live", action="store_true", help="fetch RSS + incidents over HTTP")
    ap.add_argument("--rss-file", type=Path)
    ap.add_argument("--incidents-file", type=Path)
    ap.add_argument("--input", type=Path, help="JSON entries gathered with web tools")
    ap.add_argument("--days", type=int, default=DEFAULT_WINDOW_DAYS, help="look-back window; 0 = no filter")
    ap.add_argument("--today", help="override today's date (YYYY-MM-DD), for reproducible tests")
    ap.add_argument("--out", type=Path, help="write snapshot JSON here (default: stdout)")
    args = ap.parse_args(argv)

    if not (args.live or args.rss_file or args.incidents_file or args.input):
        ap.error("choose at least one of --live, --rss-file, --incidents-file, --input")

    today = dt.date.fromisoformat(args.today) if args.today else dt.datetime.now(dt.timezone.utc).date()
    sources, entries = {}, []

    def run(name, loader):
        try:
            got = loader()
            sources[name] = {"ok": True, "count": len(got)}
            entries.extend(got)
        except (urllib.error.URLError, OSError, ValueError, TimeoutError) as exc:
            sources[name] = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
            print(f"ERROR: {name} failed: {exc}", file=sys.stderr)

    if args.live:
        run("docs_updates_rss", lambda: parse_feed(http_get(RSS_URL)))
        run("status_dashboard", lambda: parse_incidents(http_get(INCIDENTS_URL)))
    if args.rss_file:
        run("docs_updates_rss_file", lambda: parse_feed(args.rss_file.read_bytes()))
    if args.incidents_file:
        run("status_dashboard_file", lambda: parse_incidents(args.incidents_file.read_bytes()))
    if args.input:
        run("manual_input", lambda: normalize_input(args.input))

    ok = [n for n, s in sources.items() if s["ok"]]
    if not ok:
        print("FAILED: no source could be read. Nothing written. Fall back to "
              "knowledge/latest-verified-updates.md and mark guidance 'previously verified'.", file=sys.stderr)
        return 1

    days = None if args.days == 0 else args.days
    final = dedupe(within_window(entries, days, today))
    partial = len(ok) < len(sources)
    snapshot = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "as_of": today.isoformat(),
        "mode": "live" if args.live else "offline",
        "partial": partial,
        "window_days": days,
        "sources": sources,
        "entries": final,
    }
    text = json.dumps(snapshot, indent=2, ensure_ascii=False)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
        print(f"Wrote {len(final)} entries to {args.out} (partial={partial})", file=sys.stderr)
    else:
        print(text)
    return 2 if partial else 0


if __name__ == "__main__":
    sys.exit(main())
