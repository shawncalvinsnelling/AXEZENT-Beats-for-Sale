#!/usr/bin/env python3
"""Update the 50-track public README only when actual tagged MP3s exist.
No WAV/master links and no payment unlocks.
"""
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
readme = ROOT / "README.md"
records = json.loads((ROOT / "data/catalog.json").read_text("utf-8"))
selection = sorted((b for b in records if isinstance(b.get("releaseRank"), int)),
                   key=lambda b: b["releaseRank"])
assert len(selection) == 50
text = readme.read_text("utf-8")
begin = "<!-- BEATS_START -->"
end = "<!-- BEATS_END -->"
assert text.count(begin) == text.count(end) == 1

def clean(value):
    return str(value).replace("|", "\\|").replace("\n", " ").replace("[", "\\[").replace("]", "\\]")

rows = ["| # | Beat | City / state | Preview | Exclusive ownership inquiry |",
        "|---:|---|---|---|---|"]
for b in selection:
    subject = "AXEZENT $100 exclusive beat inquiry — " + b["id"] + " " + b["title"]
    body = ("Hello AXEZENT,\n\nI am interested in the proposed $100 full-ownership rights agreement for "
            + b["title"] + " (" + b["id"] + ").\n\n"
            + "Please confirm availability, transferable rights, and a written agreement before I pay.\n\n"
            + "Artist name:\nContact email:\n")
    mail = "mailto:shawncsnelling@gmail.com?subject=" + quote(subject) + "&body=" + quote(body)
    if b.get("status") == "preview_ready":
        relative = b["previewUrl"]
        assert relative == "previews/" + b["id"] + "-tagged.mp3"
        assert (ROOT / relative).is_file()
        url = "https://raw.githubusercontent.com/shawncalvinsnelling/AXEZENT-Beats-for-Sale/main/" + relative
        listen = "[▶ Listen to tagged MP3](" + url + ")"
    else:
        listen = "⏳ Preview upload pending"
    rows.append("| " + str(b["releaseRank"]).zfill(2) + " | **" + clean(b["title"]) +
                "** · \\x60" + b["id"] + "\\x60 | " + clean(b["city"]) + ", " + clean(b["state"]) +
                " | " + listen + " | [✉ Ask about $100 ownership](" + mail + ") |")
# Replace only the generated table; keep all branding, disclosures, and other editorial content.
before, rest = text.split(begin, 1)
_, after = rest.split(end, 1)
new = before + begin + "\n" + "\n".join(rows) + "\n" + end + after
# Change alert copy in README to avoid displaying the stale 'pending all' statement.
new = new.replace("The 50 tagged MP3 previews are prepared but **not yet present in this GitHub repository**.",
                  "The 50 tagged MP3 previews are being imported in batches; only verified uploaded files show active listening links.")
new = new.replace("The public GitHub repository contains no finished tagged preview MP3s yet, so remote Play buttons are still inactive.",
                  "Only verified published tagged MP3s are linked above. Full-quality WAV downloads remain locked.")
if new != text:
    readme.write_text(new, "utf-8")
print("README: " + str(sum(b.get("status") == "preview_ready" for b in selection)) + "/50 listening links enabled")
