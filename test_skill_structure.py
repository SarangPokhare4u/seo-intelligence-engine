"""Test A + H: skill discovery metadata and file integrity."""
import csv
import re
import zipfile
from pathlib import Path

import validate_skill

ROOT = Path(__file__).resolve().parent.parent


def test_validate_skill_passes():
    issues = validate_skill.validate(ROOT)
    errors = [i["message"] for i in issues if i["severity"] == "error"]
    assert errors == []


def test_frontmatter_fields_and_limits():
    fm, body = validate_skill.parse_frontmatter((ROOT / "SKILL.md").read_text(encoding="utf-8"))
    assert fm["name"] == "seo-intelligence-engine"
    assert 0 < len(fm["description"]) <= 1024
    assert "Use when" in fm["description"] or "Use whenever" in fm["description"]
    assert body.count("\n") < 500


def test_description_triggers_cover_core_requests():
    fm, _ = validate_skill.parse_frontmatter((ROOT / "SKILL.md").read_text(encoding="utf-8"))
    d = fm["description"].lower()
    for term in ["keyword", "audit", "content", "backlink", "ai search", "seo"]:
        assert term in d


def test_every_routed_file_exists():
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    for target in re.findall(r"\]\(([^)#]+)\)", text):
        if not target.startswith("http"):
            assert (ROOT / target).exists(), target


def test_all_csv_templates_have_headers():
    for p in (ROOT / "templates").glob("*.csv"):
        header = next(csv.reader(p.open(encoding="utf-8")))
        assert len(header) >= 5 and len(header) == len(set(header)), p.name


def test_reference_files_are_operational_not_placeholders():
    for p in list((ROOT / "references").glob("*.md")) + list((ROOT / "workflows").glob("*.md")):
        text = p.read_text(encoding="utf-8")
        assert len(text) > 800, f"{p.name} looks like a stub"
        assert "TODO" not in text and "lorem ipsum" not in text.lower(), p.name


def test_zip_layout_if_built():
    z = ROOT.parent / "seo-intelligence-engine.zip"
    if not z.exists():
        return
    names = zipfile.ZipFile(z).namelist()
    assert "seo-intelligence-engine/SKILL.md" in names
    assert all(n.startswith("seo-intelligence-engine/") for n in names)


def test_routing_table_reference_names_exist():
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    rows = [l for l in text.splitlines() if l.startswith("| ") and "workflows/" in l]
    assert len(rows) >= 11
    for row in rows:
        refs = row.rstrip(" |").rsplit("|", 1)[-1]
        for name in [n.strip() for n in refs.split(",") if n.strip()]:
            assert (ROOT / "references" / f"{name}.md").exists(), name


def test_every_workflow_is_routed():
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    for p in (ROOT / "workflows").glob("*.md"):
        assert f"workflows/{p.name}" in text, p.name
