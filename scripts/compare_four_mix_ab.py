#!/usr/bin/env python3
"""Four-track reversible mix A/B; no public media changes."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
from scripts.collection_two import load_collection_two,make_collection_two_catalog,ROOT
from scripts.render_collection_two_review_audio import render
from scripts.audit_audio_depth import one as inspect
from scripts.audit_loudness import measure

STEREO=("AXZ-172","AXZ-010")
HOOK=("AXZ-187","AXZ-110")

def report(beat,plan,directory):
    f=directory/(beat["id"]+"-review.mp3")
    depth=inspect(beat,plan,directory)
    lufs,tp,lra=measure(f)
    v=depth["excerpts"]["verse"]
    h=depth["excerpts"]["hook"]
    return {"id":beat["id"],
       "hookMinusVerseDb":depth["hookMinusVerseDb"],
       "minMonoRetention":min(v["monoRetention"],h["monoRetention"]),
       "minStereoCorrelation":min(v["stereoCorrelation"],h["stereoCorrelation"]),
       "verseMono":v["monoRetention"],"hookMono":h["monoRetention"],
       "verseCorrelation":v["stereoCorrelation"],"hookCorrelation":h["stereoCorrelation"],
       "reviewFlags":depth["producerReviewFlags"],"hardFlags":depth["hardFailures"],
       "LUFS":lufs,"truePeak":tp,"LRA":lra,
       "sha256":hashlib.sha256(f.read_bytes()).hexdigest()}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True,type=Path)
    args=p.parse_args()
    original=json.loads((ROOT/"data/catalog.json").read_text("utf-8"))
    plans0=json.loads((ROOT/"data/arrangements.json").read_text("utf-8"))
    allcatalog,plans=make_collection_two_catalog(original,plans0)
    byid={x["id"]:x for x in allcatalog}
    blueprints={x["id"]:x for x in load_collection_two()}
    sf=Path("/usr/share/sounds/sf2/FluidR3_GM.sf2")
    rows=[]
    for ident in (*STEREO,*HOOK):
        beat=byid[ident]
        baseline=args.out/"baseline"
        candidate=args.out/"candidate"
        try:
            os.environ["AXEZENT_MIX_AB_BASELINE"]="1"
            render(beat,plans[ident],blueprints[ident],baseline/(ident+"-review.mp3"),sf)
        finally:
            os.environ.pop("AXEZENT_MIX_AB_BASELINE",None)
        render(beat,plans[ident],blueprints[ident],candidate/(ident+"-review.mp3"),sf)
        old=report(beat,plans[ident],baseline)
        new=report(beat,plans[ident],candidate)
        if old["sha256"]==new["sha256"]:
            raise RuntimeError("A/B outputs identical for "+ident)
        if ident in STEREO:
            improved=(new["minMonoRetention"]>=old["minMonoRetention"]+.01
                      and new["minStereoCorrelation"]>=old["minStereoCorrelation"])
        else:
            improved=new["hookMinusVerseDb"]>=old["hookMinusVerseDb"]+.2
        valid=(not new["hardFlags"] and -19<=new["LUFS"]<=-11.5
               and new["truePeak"]<=-.8)
        row={"id":ident,"rank":beat["releaseRank"],"title":beat["title"],
             "improved":improved,"valid":valid,"baseline":old,"candidate":new}
        rows.append(row)
        print("MIX_AB_TRACK:",json.dumps(row),flush=True)
    summary={"tested":len(rows),"improved":sum(x["improved"] for x in rows),
             "valid":sum(x["valid"] for x in rows),"publicBeatsChanged":False}
    output=args.out/"results"
    output.mkdir(parents=True,exist_ok=True)
    (output/"AB_AUDIO_COMPARISON.json").write_text(json.dumps(
         {"summary":summary,"tracks":rows},indent=2)+"\n")
    print("MIX_AB_SUMMARY:",json.dumps(summary),flush=True)
    if summary["improved"]<4 or summary["valid"]<4:
        raise ValueError("Failed A/B acceptance; preserve current released mixes")

if __name__=="__main__":
    main()
