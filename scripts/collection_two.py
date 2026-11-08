#!/usr/bin/env python3
"""Collection Two: original 50 city specifications without touching Collection One.

The compressed source contains owner-prepared 50-track titles, keys, BPMs,
GM instrument programs, regional production directions and individual forms.
No commercial audio, samples or studio masters are stored here.
"""
from __future__ import annotations
import json
import re
import zlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SEED=ROOT/"data"/"collection-two-blueprints.zlib"
KIND={"i":"intro","h":"hook","v":"verse","b":"bridge",
      "d":"breakdown","p":"pre-hook","o":"outro"}

def load_collection_two():
    entries=json.loads(zlib.decompress(SEED.read_bytes()).decode("utf-8"))
    if len(entries)!=50:
        raise ValueError("Exactly 50 original second-collection blueprints required")
    songs=[]
    ids=set()
    for rank,record in enumerate(entries,51):
        ident,title,bpm,key,groove,programs,form,artist=record
        if ident in ids or not re.fullmatch(r"AXZ-[0-9]{3}",ident):
            raise ValueError("Duplicate or invalid second-collection ID")
        ids.add(ident)
        segments=re.findall(r"([ihvbdpo])(\d+),",form)
        if not segments or "".join(k+n+"," for k,n in segments)!=form:
            raise ValueError("Malformed song structure for "+ident)
        if not 65<=int(bpm)<=210 or len(programs)!=4 or any(not 0<=p<128 for p in programs):
            raise ValueError("Invalid musical parameters "+ident)
        if segments[-1][0]!="o" or sum(k=="v" for k,n in segments)<2:
            raise ValueError("Incomplete song structure "+ident)
        songs.append({"id":ident,"releaseRank":rank,"title":title,
                      "bpm":int(bpm),"key":key,"groove":groove,
                      "gmPrograms":list(programs),"form":segments,
                      "artistContext":artist})
    return songs

def make_collection_two_catalog(base_catalog,base_arrangements):
    """Expand only deployment copy, preserving existing 50 album source rows."""
    if len(base_catalog)!=200 or len(base_arrangements)!=50:
        raise ValueError("Existing 200-song / 50 published original invariant failed")
    rows=json.loads(json.dumps(base_catalog))
    plans=json.loads(json.dumps(base_arrangements))
    index={row["id"]:row for row in rows}
    if len(index)!=200:
        raise ValueError("Duplicate original IDs")
    old=[row for row in rows if isinstance(row.get("releaseRank"),int)]
    if sorted(row["releaseRank"] for row in old)!=list(range(1,51)):
        raise ValueError("Original 50 release ranks unexpectedly changed")
    original_state=json.dumps({i:plans[i] for i in plans},sort_keys=True)
    collection=load_collection_two()
    new_cities=set()
    for song in collection:
        ident=song["id"]
        if ident in plans:
            raise ValueError("Collection Two collides with first 50")
        track=index[ident]
        if track.get("releaseRank"):
            raise ValueError("Previously released source record unexpectedly changed "+ident)
        city=(track["city"],track["state"])
        if city in new_cities or city in {(b["city"],b["state"]) for b in old}:
            raise ValueError("100 distinct cities required "+str(city))
        new_cities.add(city)
        track.update({"title":song["title"],"bpm":song["bpm"],
                      "key":song["key"],"releaseRank":song["releaseRank"],
                      "status":"mix_review"})
        sections=[]
        bar=0
        kinds={k:0 for k in KIND.values()}
        for short,counttext in song["form"]:
            kind=KIND[short];n=int(counttext);kinds[kind]+=1
            label=kind.title().replace("-"," ")
            if kind in ("hook","verse","pre-hook"):
                label+=" "+str(kinds[kind])
            sections.append({"kind":kind,"label":label,"bars":n,
                "startBar":bar,"endBar":bar+n,
                "startSeconds":round(bar*240/song["bpm"],3),
                "endSeconds":round((bar+n)*240/song["bpm"],3)})
            bar+=n
        plans[ident]={
            "releaseRank":song["releaseRank"],
            "form":"hook-first" if sections[0]["kind"]=="hook" else
                   "verse-first" if sections[0]["kind"]=="verse" else "intro-first",
            "signature":song["groove"],
            "soundPalette":"Four individually selected GM instrument voices "+
                           ", ".join(str(p) for p in song["gmPrograms"]),
            "artistContext":song["artistContext"],
            "arrangementStatus":"proposed_not_audio_verified",
            "artisticDirection":"Original regional style plan, not an artist imitation or sample.",
            "bpm":song["bpm"],"key":song["key"],
            "sections":sections,"totalBars":bar,
            "durationSeconds":round(bar*240/song["bpm"],3),
            "recordingVerified":False
        }
    if json.dumps({i:plans[i] for i in base_arrangements},sort_keys=True)!=original_state:
        raise ValueError("Original arrangements must remain bytewise semantically unchanged")
    featured=sorted((r for r in rows if isinstance(r.get("releaseRank"),int)),
                    key=lambda r:r["releaseRank"])
    if len(featured)!=100 or [r["releaseRank"] for r in featured]!=list(range(1,101)):
        raise ValueError("Not 100 contiguous release records")
    if len({(r["city"],r["state"]) for r in featured})!=100:
        raise ValueError("100 distinct cities were not achieved")
    if len(plans)!=100:
        raise ValueError("100 arrangement maps required")
    return rows,plans

def publish_site_data(folder):
    original=json.loads((ROOT/"data"/"catalog.json").read_text("utf-8"))
    arrangements=json.loads((ROOT/"data"/"arrangements.json").read_text("utf-8"))
    tracks,plans=make_collection_two_catalog(original,arrangements)
    dest=Path(folder);dest.mkdir(parents=True,exist_ok=True)
    safe_keys=("id","title","city","state","collection","bpm","key","releaseRank")
    public=[{k:r.get(k) for k in safe_keys} for r in tracks]
    (dest/"catalog.json").write_text(json.dumps(public,ensure_ascii=False),encoding="utf-8")
    (dest/"arrangements.json").write_text(json.dumps(plans,ensure_ascii=False),encoding="utf-8")
    print("PASS: 200 catalog records, 100 featured cities and 100 unique song maps; source originals untouched",flush=True)

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--public-data",required=True)
    args=p.parse_args()
    publish_site_data(args.public_data)
