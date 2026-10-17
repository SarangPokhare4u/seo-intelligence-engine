#!/usr/bin/env python3
"""Compare two update snapshots produced by fetch_updates.py.

Usage:
  python3 scripts/compare_updates.py OLD.json NEW.json [--json]

Reports entries added in NEW, entries no longer present (outside window or
removed), and status changes (e.g. 'rolling out' -> 'complete').
Exit codes: 0 = compared (differences or not), 1 = unreadable input.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def load(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"ERROR: snapshot not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"ERROR: {path} is not valid JSON: {exc}")
    if isinstance(data, list):
        data = {"entries": data}
    if not isinstance(data.get("entries"), list):
        raise SystemExit(f"ERROR: {path} has no 'entries' list")
    return data


def key(e: dict) -> tuple:
    title = re.sub(r"\W+", " ", str(e.get("title", "")).lower()).strip()
    return (e.get("source", ""), title, e.get("date", ""))


def compare(old: dict, new: dict) -> dict:
    o = {key(e): e for e in old["entries"]}
    n = {key(e): e for e in new["entries"]}
    added = [n[k] for k in n if k not in o]
    removed = [o[k] for k in o if k not in n]
    changed = []
    for k in n.keys() & o.keys():
        before, after = o[k], n[k]
        diffs = {f: (before.get(f), after.get(f)) for f in ("status", "end_date", "class")
                 if before.get(f) != after.get(f)}
        if diffs:
            changed.append({"title": after.get("title"), "date": after.get("date"), "changes": diffs})
    sort = lambda xs: sorted(xs, key=lambda e: e.get("date") or "", reverse=True)  # noqa: E731
    return {
        "old_as_of": old.get("as_of"),
        "new_as_of": new.get("as_of"),
        "new_partial": new.get("partial", False),
        "added": sort(added),
        "no_longer_present": sort(removed),
        "status_changes": sort(changed),
    }


def render(result: dict) -> str:
    lines = [f"Snapshot diff: {result['old_as_of']} -> {result['new_as_of']}"]
    if result["new_partial"]:
        lines.append("WARNING: newer snapshot is partial (a source failed); absence of an entry is not evidence it was removed.")
    lines.append(f"\nAdded ({len(result['added'])}):")
    lines += [f"  + {e.get('date')} | {e.get('title')} | {e.get('class')} | {e.get('status')}" for e in result["added"]] or ["  (none)"]
    lines.append(f"\nStatus changes ({len(result['status_changes'])}):")
    for c in result["status_changes"]:
        parts = ", ".join(f"{f}: {a!r} -> {b!r}" for f, (a, b) in c["changes"].items())
        lines.append(f"  ~ {c['date']} | {c['title']} | {parts}")
    if not result["status_changes"]:
        lines.append("  (none)")
    lines.append(f"\nNo longer present ({len(result['no_longer_present'])}) - usually aged out of the window:")
    lines += [f"  - {e.get('date')} | {e.get('title')}" for e in result["no_longer_present"]] or ["  (none)"]
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("old", type=Path)
    ap.add_argument("new", type=Path)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)
    result = compare(load(args.old), load(args.new))
    print(json.dumps(result, indent=2) if args.json else render(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
