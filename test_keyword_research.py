"""Test C: clustering behavior and no fabricated metrics."""
import csv
import io
from pathlib import Path

import cluster_keywords

FIX = Path(__file__).resolve().parent / "fixtures"
ROOT = FIX.parent.parent


def run(args, capsys):
    code = cluster_keywords.main(args)
    out = capsys.readouterr().out
    return code, list(csv.DictReader(io.StringIO(out)))


def test_serp_overlap_clusters(capsys):
    code, rows = run(["--serp-csv", str(FIX / "serp_rows.csv"), "--threshold", "3"], capsys)
    assert code == 0
    clusters = {}
    for r in rows:
        clusters.setdefault(r["cluster_id"], set()).add(r["keyword"])
    groups = sorted(sorted(v) for v in clusters.values())
    assert ["fleet inspection software", "vehicle inspection app", "vehicle inspection software"] in groups
    # dvir pair shares only 2 URLs in top 10 (position 15 excluded) -> separate at threshold 3
    assert ["dvir checklist"] in groups and ["how to do a dvir"] in groups


def test_threshold_two_merges_dvir(capsys):
    _, rows = run(["--serp-csv", str(FIX / "serp_rows.csv"), "--threshold", "2"], capsys)
    ids = {r["keyword"]: r["cluster_id"] for r in rows}
    assert ids["dvir checklist"] == ids["how to do a dvir"]


def test_no_volume_invented(capsys):
    _, rows = run(["--serp-csv", str(FIX / "serp_rows.csv")], capsys)
    assert all(r["volume"] == "" for r in rows)


def test_lexical_fallback_is_labeled(capsys):
    _, rows = run(["--keywords", str(FIX / "keywords.txt"), "--lexical"], capsys)
    assert all("unverified by SERP" in r["method"] for r in rows)
    ids = {r["keyword"]: r["cluster_id"] for r in rows}
    assert ids["vehicle inspection checklist"] == ids["vehicle inspection checklists"]
    assert ids["dvir requirements"] != ids["fleet inspection software"]


def test_bad_input_returns_error(tmp_path, capsys):
    bad = tmp_path / "bad.csv"
    bad.write_text("term,link\nx,y\n")
    assert cluster_keywords.main(["--serp-csv", str(bad)]) == 1


def test_keyword_map_template_has_source_columns():
    header = next(csv.reader((ROOT / "templates" / "keyword-map.csv").open()))
    for col in ["volume_source", "kd_source", "cpc_source", "serp_observed_date"]:
        assert col in header
