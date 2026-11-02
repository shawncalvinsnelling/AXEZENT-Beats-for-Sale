#!/usr/bin/env python3
"""Securely unpack five user-supplied tagged MP3 preview packs.
This NEVER imports a private master, paid ZIP or other sensitive file.
"""
import json
from pathlib import Path
from zipfile import ZipFile, BadZipFile

ROOT=Path(__file__).resolve().parents[1]
IN=ROOT/"incoming"
OUT=ROOT/"previews"
OUT.mkdir(exist_ok=True)
catalog=json.loads((ROOT/"data/catalog.json").read_text("utf-8"))
allowed={b["id"]+"-tagged.mp3" for b in catalog if isinstance(b.get("releaseRank"),int) and 1 <= b["releaseRank"] <= 50}
assert len(allowed)==50
packs=sorted(IN.glob("axezent-previews-??.zip")) if IN.exists() else []
seen=set()
for pack in packs:
    if pack.name not in {f"axezent-previews-{x:02d}.zip" for x in range(1,6)}:
        raise SystemExit(f"Unexpected archive name: {pack}")
    if not 0 < pack.stat().st_size <= 23*1024*1024:
        raise SystemExit(f"Archive exceeds safe GitHub web upload size: {pack}")
    with ZipFile(pack) as z:
        info=z.infolist()
        if len(info)!=10:
            raise SystemExit(f"Exactly 10 tagged audio files expected in {pack.name}")
        for item in info:
            name=item.filename
            if name not in allowed or item.is_dir() or "/" in name or "\\" in name:
                raise SystemExit(f"Unsafe/unexpected entry {name}")
            if name in seen:
                raise SystemExit(f"Duplicate audio file across packs: {name}")
            if not 100_000 < item.file_size < 7_500_000:
                raise SystemExit(f"Unexpected preview size: {name}")
            seen.add(name)
            dest=OUT/name
            content=z.read(item)
            if len(content)!=item.file_size:
                raise SystemExit(f"Invalid audio size: {name}")
            if dest.exists() and dest.read_bytes()!=content:
                raise SystemExit(f"Existing preview differs: {name}")
            dest.write_bytes(content)
print(f"Imported {len(seen)} tagged previews from {len(packs)} ZIP uploads.")
