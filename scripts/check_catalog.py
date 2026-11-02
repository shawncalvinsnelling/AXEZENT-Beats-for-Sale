#!/usr/bin/env python3
"""Strict, standard-library catalog gate; never treats a proposed track as audio."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
records = json.loads((ROOT / "data" / "catalog.json").read_text(encoding="utf-8"))
assert isinstance(records, list) and len(records) == 200, "200 catalog entries required"
assert len({b["id"] for b in records}) == 200, "Duplicate ID"
assert len({b["title"].casefold() for b in records}) == 200, "Duplicate title"
assert len({b["state"] for b in records}) == 50, "Exactly 50 states required"
assert set(Counter(b["state"] for b in records).values()) == {4}, "Four tracks per state required"
for i, b in enumerate(records, 1):
    assert b["id"] == f"AXZ-{i:03d}", f"Unstable catalog ID at {i}"
    assert b["title"].strip() and b["city"].strip(), "Missing music or city"
    assert b["status"] in ("planned", "mix_review", "preview_ready"), "Unsupported track state"
    assert b["priceUsd"] == 100, "Proposed base license mismatch"
    if b["status"] in ("planned", "mix_review"):
        assert b["previewUrl"] is None, "Planned audio cannot advertise playback"
    else:
        preview = b["previewUrl"]
        assert isinstance(preview, str), "Published preview missing URL"
        assert preview.startswith("previews/") and preview.endswith("-tagged.mp3"), "Unexpected preview path"
        assert ".." not in preview and "\\" not in preview, "Unsafe preview path"
        assert (ROOT / preview).is_file(), f"Missing preview: {preview}"
        assert (ROOT / preview).stat().st_size > 0, f"Empty preview: {preview}"

bad = list(ROOT.rglob("*.wav")) + list(ROOT.rglob("*.flac")) + list(ROOT.rglob("*.sqlite3"))
assert not bad, "Private studio masters or database accidentally included"
review = [b for b in records if b["status"] == "mix_review"]
assert len(review) == 50, "The first 50 mixes must remain tracked"
assert len(set(b["releaseRank"] for b in review)) == 50, "Release order must be unique"
assert set(b["releaseRank"] for b in review) == set(range(1, 51)), "Release order must cover 1 through 50"
assert all(b.get("buyEnabled") is False and b.get("downloadEnabled") is False for b in review), "Unverified checkout must stay disabled"
print("PASS: 200 titles / 50 states / 50 review mixes; public masters not present; unverified sales disabled")
