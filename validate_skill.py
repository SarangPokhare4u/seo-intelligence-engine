#!/usr/bin/env python3
"""Validate the structure of this skill (or any Agent Skill directory).

Usage:
  python3 scripts/validate_skill.py [SKILL_DIR] [--json]

Checks (per Anthropic Agent Skills docs, verified 2026-10-17):
  - SKILL.md exists with YAML frontmatter containing name and description
  - name: <= 64 chars, lowercase letters/digits/hyphens, no 'anthropic'/'claude', no XML tags
  - description: non-empty, <= 1024 chars, no XML tags
  - SKILL.md body < 500 lines
  - every relative Markdown link in every .md file resolves to an existing file
  - no backslash paths in links
  - reference/workflow files over 100 lines have a 'Contents' section
  - every file in the README directory tree exists
  - CSV templates have a non-empty, duplicate-free header row
  - every script compiles
Exit codes: 0 = pass, 1 = errors.
"""
from __future__ import annotations

import argparse
import csv
import json
import py_compile
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
XML_RE = re.compile(r"<[A-Za-z/][^>]*>")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
MAX_BODY_LINES = 500
TOC_THRESHOLD = 100


def parse_frontmatter(text: str):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, text[m.end():]


def tree_paths(readme: str) -> list[str]:
    """Extract file paths from the first ```text tree block in README.md."""
    m = re.search(r"```text\n(.*?)```", readme, re.S)
    if not m:
        return []
    paths, stack = [], []
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        name_match = re.search(r"([A-Za-z0-9_.\-]+/?)\s*(#.*)?$", line)
        if not name_match:
            continue
        name = name_match.group(1)
        prefix = line[: line.find(name)]
        depth = len(prefix.replace("│", " ").replace("├──", "   ").replace("└──", "   ")) // 4
        stack = stack[:depth]
        if name.endswith("/"):
            stack.append(name.rstrip("/"))
        else:
            paths.append("/".join(stack + [name]))
    # first entry is the root folder itself
    return [p.split("/", 1)[1] for p in paths if "/" in p]


def validate(root: Path) -> list[dict]:
    issues = []
    add = lambda sev, msg: issues.append({"severity": sev, "message": msg})  # noqa: E731
    skill = root / "SKILL.md"
    if not skill.exists():
        add("error", "SKILL.md not found")
        return issues
    text = skill.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    if fm is None:
        add("error", "SKILL.md has no YAML frontmatter")
    else:
        name, desc = fm.get("name", ""), fm.get("description", "")
        if not NAME_RE.match(name):
            add("error", f"name '{name}' must be <=64 chars of lowercase letters, digits, hyphens")
        if "anthropic" in name.lower() or "claude" in name.lower():
            add("error", "name contains reserved word")
        if XML_RE.search(name) or XML_RE.search(desc):
            add("error", "name/description contain XML tags")
        if not desc:
            add("error", "description is empty")
        elif len(desc) > 1024:
            add("error", f"description is {len(desc)} chars (> 1024)")
        else:
            add("info", f"description length {len(desc)}/1024")
        extra = set(fm) - {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
        if extra:
            add("warning", f"non-standard frontmatter keys: {sorted(extra)}")
    body_lines = body.count("\n") + 1
    if body_lines >= MAX_BODY_LINES:
        add("error", f"SKILL.md body has {body_lines} lines (limit {MAX_BODY_LINES})")
    else:
        add("info", f"SKILL.md body lines: {body_lines}")

    for md in sorted(root.rglob("*.md")):
        content = md.read_text(encoding="utf-8")
        # ignore links inside fenced code blocks
        stripped = re.sub(r"```.*?```", "", content, flags=re.S)
        for target in LINK_RE.findall(stripped):
            if re.match(r"^(https?:|mailto:|#)", target):
                continue
            if "\\" in target:
                add("error", f"{md.relative_to(root)}: backslash path '{target}'")
                continue
            dest = (md.parent / target.split("#")[0]).resolve()
            if not dest.exists():
                add("error", f"{md.relative_to(root)}: broken link '{target}'")
        rel = md.relative_to(root).as_posix()
        if rel.startswith(("references/", "workflows/", "knowledge/")) and content.count("\n") > TOC_THRESHOLD:
            if not re.search(r"^#+\s*Contents", content, re.M):
                add("warning", f"{rel}: over {TOC_THRESHOLD} lines without a Contents section")

    readme = root / "README.md"
    if readme.exists():
        for p in tree_paths(readme.read_text(encoding="utf-8")):
            if not (root / p).exists():
                add("error", f"README tree lists missing file: {p}")
    else:
        add("warning", "README.md missing")

    for csv_path in sorted((root / "templates").glob("*.csv")):
        with csv_path.open(newline="", encoding="utf-8") as f:
            header = next(csv.reader(f), [])
        if not header or any(not h.strip() for h in header):
            add("error", f"{csv_path.name}: empty header or blank column name")
        elif len(header) != len(set(header)):
            add("error", f"{csv_path.name}: duplicate header names")

    for py in sorted((root / "scripts").glob("*.py")):
        try:
            py_compile.compile(str(py), doraise=True, cfile=str(Path("/tmp") / (py.name + "c")))
        except py_compile.PyCompileError as exc:
            add("error", f"{py.name} does not compile: {exc.msg}")
    return issues


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("skill_dir", nargs="?", type=Path, default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    issues = validate(args.skill_dir.resolve())
    errors = sum(i["severity"] == "error" for i in issues)
    if args.json:
        print(json.dumps({"errors": errors, "issues": issues}, indent=2))
    else:
        for i in issues:
            print(f"[{i['severity'].upper()}] {i['message']}")
        print(f"\nResult: {'PASS' if not errors else 'FAIL'} ({errors} error(s))")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
