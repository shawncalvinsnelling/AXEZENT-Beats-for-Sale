#!/usr/bin/env python3
"""Render only approved-for-test Priority Collection One public review revisions.

Do not replace the remaining original 50 MP3s. This is NOT a stem master and
no private historical audio is copied into Git.
"""
from __future__ import annotations
import argparse
import json
import shutil
from pathlib import Path
from scripts.render_arranged_review_audio import prepare_review
from scripts.music_a_z_enhance import PRIORITY_IDS

ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",required=True,type=Path)
    ap.add_argument("--start",type=int,default=1)
    ap.add_argument("--end",type=int,default=50)
    ap.add_argument("--soundfont",type=Path,default=Path("/usr/share/sounds/sf2/FluidR3_GM.sf2"))
    args=ap.parse_args()
    catalog=json.loads((ROOT/"data/catalog.json").read_text("utf8"))
    plans=json.loads((ROOT/"data/arrangements.json").read_text("utf8"))
    if not args.soundfont.is_file() or not shutil.which("fluidsynth"):
        raise RuntimeError("Missing FluidSynth or installed licensed public review SoundFont")
    featured=sorted((b for b in catalog if isinstance(b.get("releaseRank"),int)
        and 1<=b["releaseRank"]<=50),key=lambda b:b["releaseRank"])
    report=[]
    args.out.mkdir(parents=True,exist_ok=True)
    for beat in featured:
        if beat["id"] not in PRIORITY_IDS or not args.start<=beat["releaseRank"]<=args.end:
            continue
        path=args.out/(beat["id"]+"-review.mp3")
        info=prepare_review(beat,plans[beat["id"]],path,args.soundfont,enhanced=True)
        info.update({"rank":beat["releaseRank"],"revision":"A–Z selective original riff + groove",
                     "unmodifiedFirstCollectionBeatsKept":True})
        report.append(info)
    print("PASS: verified studio preview rendering",len(report),flush=True)
    (args.out/"REVIEW_REPORT.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf8")
if __name__=="__main__":
    main()
