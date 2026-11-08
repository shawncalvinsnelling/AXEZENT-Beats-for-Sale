#!/usr/bin/env python3
"""Create short PUBLIC review excerpts from already rendered AXEZENT synthetic drafts.

No full-length master or full-length review MP3 is published.  Browser audio can
always be captured: these excerpts deliberately contain only a short segment.
"""
import argparse
import json
import subprocess
from pathlib import Path

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--catalog",default="data/catalog.json")
    parser.add_argument("--source",required=True)
    parser.add_argument("--destination",required=True)
    parser.add_argument("--start",type=int,required=True)
    parser.add_argument("--end",type=int,required=True)
    args=parser.parse_args()
    tracks=json.loads(Path(args.catalog).read_text("utf-8"))
    ranked=sorted((b for b in tracks if isinstance(b.get("releaseRank"),int) and 1<=b["releaseRank"]<=50),key=lambda b:b["releaseRank"])
    if len(ranked)!=50:raise SystemExit("Expected 50 catalog entries")
    output=Path(args.destination);output.mkdir(parents=True,exist_ok=True)
    for b in ranked:
        if not args.start<=b["releaseRank"]<=args.end:continue
        ident=b["id"]
        original=Path(args.source)/(ident+"-tagged.mp3")
        if not original.is_file():raise SystemExit("Missing synthetic review mix: "+str(original))
        # Begin shortly before the first 8-bar hook. 30s samples are sufficiently
        # short to avoid posting the complete 48-bar arrangement.
        bpm=int(b["bpm"])
        excerpt_start=round(max(0.0,3.5*4*60/bpm),2)
        target=output/(ident+"-sample.mp3")
        cmd=["ffmpeg","-hide_banner","-nostdin","-loglevel","error","-y",
             "-ss",str(excerpt_start),"-i",str(original),"-t","30.0",
             "-ac","2","-ar","32000","-c:a","libmp3lame","-b:a","96k",str(target)]
        subprocess.run(cmd,check=True)
        if not (100_000<target.stat().st_size<700_000):
            raise SystemExit("Sample size out of bounds: "+str(target))
        print(f"PUBLIC REVIEW EXCERPT: {ident}, 30 seconds, {target.stat().st_size} bytes",flush=True)
if __name__=="__main__":main()
