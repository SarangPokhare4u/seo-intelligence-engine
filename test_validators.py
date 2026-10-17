"""Tests for metadata, schema and internal link validators."""
from pathlib import Path

import validate_internal_links as vil
import validate_metadata as vm
import validate_schema as vs

FIX = Path(__file__).resolve().parent / "fixtures"


def sev(issues, level):
    return [i for i in issues if i["severity"] == level]


def test_metadata_good_title_passes():
    issues = vm.check("Fleet Inspection Software for Logistics Teams | Example",
                      "Run digital vehicle inspections, flag defects and close repairs faster with one record per vehicle.",
                      "fleet inspection software", False)
    assert not sev(issues, "error")


def test_metadata_long_title_is_warning_not_error():
    issues = vm.check("A" * 10 + " very long title " * 6, None, None, False)
    assert any("truncation risk" in i["message"] for i in sev(issues, "warning"))
    assert not sev(issues, "error")


def test_metadata_csv_detects_duplicates_and_placeholders():
    assert vm.main(["--csv", str(FIX / "metadata.csv"), "--json"]) == 1


def test_metadata_em_dash_rule():
    issues = vm.check("Inspection records — every handoff", None, None, True)
    assert sev(issues, "error")


def test_schema_good_passes():
    nodes, _ = vs.load_nodes(FIX / "good_schema.json")
    assert not sev(vs.validate(nodes), "error")


def test_schema_bad_flags_problems():
    nodes, _ = vs.load_nodes(FIX / "bad_schema.json")
    issues = vs.validate(nodes)
    msgs = " ".join(i["message"] for i in issues)
    assert "FAQ rich results stopped" in msgs
    assert "Product: missing required property 'name'" in msgs
    assert "@context should be" in msgs
    assert "missing @type" in msgs


def test_schema_html_alignment_and_ratings():
    nodes, text = vs.load_nodes(FIX / "page.html")
    issues = vs.validate(nodes, text)
    msgs = " ".join(i["message"] for i in issues)
    assert "Hidden Product Name" in msgs  # name not visible on page
    assert "no visible review or rating text" in msgs


def test_internal_links():
    links = vil.read_csv(FIX / "links.csv", {"source", "target"})
    urls = (FIX / "sitemap_urls.txt").read_text().splitlines()
    clusters = vil.read_csv(FIX / "clusters.csv", {"url", "cluster", "role"})
    issues = vil.analyze(links, urls, clusters)
    msgs = " ".join(i["message"] for i in issues)
    assert "/blog/orphan-post/ has no internal links" in msgs
    assert "'click here'" in msgs
    assert "/old-page/" in msgs
    assert "pillar /blog/ does not link to cluster page /blog/orphan-post/" in msgs
