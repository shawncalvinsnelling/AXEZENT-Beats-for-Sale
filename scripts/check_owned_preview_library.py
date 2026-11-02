#!/usr/bin/env python3
"""Before publicly serving AXEZENT, require all 50 private, tagged MP3 reviews.

No third-party packages, web services, API keys, or uploaded audio needed.
This checks file presence/format, NOT composition quality or ownership.
"""
import argparse
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DEFAULT_AUDIO=ROOT.parent/"AXEZENT_PRIVATE_TAGGED_PREVIEWS"

def scan(folder, catalog_path=ROOT/"data"/"catalog.json"):
    songs=json.loads(Path(catalog_path).read_text(encoding="utf-8"))
    chosen=[b for b in songs if isinstance(b.get("releaseRank"),int) and
            1<=b["releaseRank"]<=50]
    if len(chosen)!=50 or len({b["id"] for b in chosen})!=50:
        raise ValueError("The 50 selected catalog tracks must have unique IDs.")
    folder=Path(folder)
    if not folder.is_dir():
        return [], [b["id"] for b in chosen]
    ready,missing=[],[]
    for b in sorted(chosen,key=lambda b:b["releaseRank"]):
        p=folder/(b["id"]+"-tagged.mp3")
        try:
            if p.is_symlink() or not p.is_file() or not (100_000<=p.stat().st_size<=10_000_000):
                raise ValueError("invalid file")
            with p.open("rb") as handle:
                start=handle.read(3)
            if start!=b"ID3" and start[:2] not in (b"\xff\xfb",b"\xff\xf3",b"\xff\xf2"):
                raise ValueError("not an MP3 stream")
            ready.append(b["id"])
        except (OSError, ValueError):
            missing.append(b["id"])
    return ready,missing

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--preview-dir",type=Path,default=DEFAULT_AUDIO)
    args=p.parse_args()
    ready,missing=scan(args.preview_dir)
    print("AXEZENT private listening library: %d/50 MP3s ready"%len(ready))
    if missing:
        print("Unusable previews:",", ".join(missing))
        raise SystemExit(1)
    print("PASS: all 50 preview files pass format/size preflight.")
    print("NOTE: this is not a professional-audio or intellectual-property review.")

if __name__=="__main__":
    main()
