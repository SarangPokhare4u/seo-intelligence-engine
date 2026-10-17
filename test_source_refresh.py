"""Test B: update refresh parsing, offline fallback, and snapshot diffing."""
import json
import socket
import urllib.request
from pathlib import Path

import compare_updates
import fetch_updates

FIX = Path(__file__).resolve().parent / "fixtures"
ROOT = FIX.parent.parent


def test_rss_parsing_and_classification():
    entries = fetch_updates.parse_feed((FIX / "sample_rss.xml").read_bytes())
    by_title = {e["title"]: e for e in entries}
    assert len(entries) == 4
    assert by_title["Deprecating the FAQ rich result feature"]["class"] == "feature deprecation"
    assert by_title['Introducing a new spam policy for "back button hijacking"']["class"] == "policy change"
    assert by_title["Updating the Indexing API quota page"]["date"] == "2026-10-16"
    # a documentation page about core updates must not be labeled an algorithm update
    assert by_title["Adding a section on smaller core updates"]["class"] == "documentation change"


def test_atom_parsing():
    entries = fetch_updates.parse_feed((FIX / "sample_atom.xml").read_bytes())
    assert entries[0]["date"] == "2026-06-15"


def test_incidents_parsing_status():
    entries = fetch_updates.parse_incidents((FIX / "sample_incidents.json").read_bytes())
    spam = next(e for e in entries if "spam" in e["title"])
    assert spam["class"] == "algorithm update" and spam["status"] == "complete"
    assert spam["date"] == "2026-09-24" and spam["end_date"] == "2026-10-08"
    rolling = next(e for e in entries if "FIXTURE" in e["title"])
    assert rolling["class"] == "incident" and rolling["status"] == "rolling out"


def test_window_filter(tmp_path):
    out = tmp_path / "snap.json"
    code = fetch_updates.main(["--rss-file", str(FIX / "sample_rss.xml"), "--days", "90",
                               "--today", "2026-10-17", "--out", str(out)])
    assert code == 0
    titles = [e["title"] for e in json.loads(out.read_text())["entries"]]
    assert titles == ["Updating the Indexing API quota page"]


def test_malformed_feed_is_reported_not_invented(tmp_path):
    bad = tmp_path / "bad.xml"
    bad.write_text("<html>not a feed")
    out = tmp_path / "snap.json"
    code = fetch_updates.main(["--rss-file", str(bad), "--out", str(out)])
    assert code == 1 and not out.exists()


def test_live_mode_without_network_fails_cleanly(tmp_path, monkeypatch):
    def boom(*a, **k):
        raise socket.gaierror("network disabled for test")
    monkeypatch.setattr(urllib.request, "urlopen", boom)
    out = tmp_path / "snap.json"
    code = fetch_updates.main(["--live", "--out", str(out)])
    assert code == 1 and not out.exists()


def test_partial_when_one_source_fails(tmp_path, monkeypatch):
    def boom(*a, **k):
        raise socket.gaierror("offline")
    monkeypatch.setattr(urllib.request, "urlopen", boom)
    out = tmp_path / "snap.json"
    code = fetch_updates.main(["--live", "--incidents-file", str(FIX / "sample_incidents.json"),
                               "--days", "0", "--out", str(out)])
    snap = json.loads(out.read_text())
    assert code == 2 and snap["partial"] is True
    assert snap["sources"]["docs_updates_rss"]["ok"] is False


def test_manual_input_rejects_undated_entries(tmp_path):
    src = tmp_path / "found.json"
    src.write_text(json.dumps([{"title": "No date"}, {"title": "Deprecating X", "date": "2026-05-08"}]))
    out = tmp_path / "snap.json"
    assert fetch_updates.main(["--input", str(src), "--days", "0", "--out", str(out)]) == 0
    entries = json.loads(out.read_text())["entries"]
    assert [e["title"] for e in entries] == ["Deprecating X"]
    assert entries[0]["class"] == "feature deprecation"


def test_compare_snapshots():
    old = compare_updates.load(FIX / "snapshot_old.json")
    new = compare_updates.load(FIX / "snapshot_new.json")
    r = compare_updates.compare(old, new)
    assert [e["title"] for e in r["added"]] == ["Updating the Indexing API quota page"]
    assert r["status_changes"][0]["changes"]["status"] == ("rolling out", "complete")
    assert [e["title"] for e in r["no_longer_present"]] == ["Old entry aging out"]


def test_baseline_snapshot_is_valid():
    snap = json.loads((ROOT / "knowledge" / "snapshots" / "2026-10-17.json").read_text())
    assert snap["entries"] and all(e["date"] and e["title"] for e in snap["entries"])
    assert all(e["class"] in fetch_updates.VALID_CLASSES for e in snap["entries"])
