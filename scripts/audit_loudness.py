#!/usr/bin/env python3
"""Independent objective QA of the 100 AXEZENT public review MP3 mixes.

Checks file identity, codec, exact duration, PCM true peak and integrated EBU
R128 loudness. Does not claim subjective quality, regional authenticity,
sample rights, or that these mixes equal the owner's earlier private music.
"""
from __future__ import annotations
import argparse
import concurrent.futures
import hashlib
import json
import re
import statistics
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def probe(path: Path) -> dict:
    return json.loads(subprocess.check_output([
        "ffprobe","-v","error","-show_entries",
        "stream=codec_name,channels,sample_rate:format=duration,size,bit_rate",
        "-of","json",str(path)
    ],stderr=subprocess.DEVNULL))

def measure(path: Path) -> tuple[float,float,float]:
    result=subprocess.run([
        "ffmpeg","-hide_banner","-nostdin","-loglevel","info",
        "-i",str(path),"-af","ebur128=peak=true","-vn","-f","null","-"
    ],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True,check=True)
    tail=result.stderr.rsplit("Summary:",1)[-1]
    integrated=re.search(r"Integrated loudness:\s*I:\s*(-?[\d.]+) LUFS",tail)
    peak=re.search(r"True peak:\s*Peak:\s*(-?[\d.]+) dBFS",tail)
    lra=re.search(r"Loudness range:\s*LRA:\s*([\d.]+) LU",tail)
    if not all((integrated,peak,lra)):
        raise ValueError("EBU R128 summary unavailable")
    return float(integrated.group(1)),float(peak.group(1)),float(lra.group(1))

def one(row: dict,folder: Path,arrangements: dict) -> dict:
    ident=row["id"]
    path=folder/(ident+"-review.mp3")
    if not path.is_file():
        raise ValueError("Missing MP3 "+ident)
    if path.stat().st_size<150_000:
        raise ValueError("Suspiciously small audio file "+ident)
    media=probe(path)
    streams=media.get("streams",[])
    if len(streams)!=1 or streams[0].get("codec_name")!="mp3" or streams[0].get("channels")!=2:
        raise ValueError("Invalid stereo MP3 "+ident)
    sr=int(streams[0]["sample_rate"])
    if sr!=44100:
        raise ValueError("Expected 44.1kHz source "+ident)
    duration=float(media["format"]["duration"])
    plan=arrangements[ident]
    if abs(duration-plan["durationSeconds"])>0.6:
        raise ValueError("Arrangement/duration mismatch "+ident)
    lufs,tp,lra=measure(path)
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        "id":ident, "rank":row["releaseRank"],"title":row["title"],
        "durationSeconds":round(duration,3),"sampleRateHz":sr,
        "sizeBytes":path.stat().st_size,"integratedLUFS":lufs,
        "truePeakDbFS":tp,"loudnessRangeLU":lra,"sha256":digest,
        "status":"QA_VERIFIED_WEB_REVIEW_AUDIO_NOT_APPROVED_MASTER"
    }

def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--audio-dir",type=Path,required=True)
    parser.add_argument("--report",type=Path,required=True)
    parser.add_argument("--catalog",type=Path,default=ROOT/"data/catalog.json")
    parser.add_argument("--arrangements",type=Path,default=ROOT/"data/arrangements.json")
    args=parser.parse_args()
    catalog=json.loads(args.catalog.read_text("utf-8"))
    arrangements=json.loads(args.arrangements.read_text("utf-8"))
    featured=sorted((b for b in catalog if isinstance(b.get("releaseRank"),int)
                     and 1<=b["releaseRank"]<=100),key=lambda b:b["releaseRank"])
    if len(featured)!=100 or len(arrangements)!=100:
        raise ValueError("Published catalog or arrangement count is not 100")
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        reports=list(pool.map(lambda x:one(x,args.audio_dir,arrangements),featured))
    if len({r["sha256"] for r in reports})!=100:
        raise ValueError("Some audio files are identical")
    failures=[]
    for r in reports:
        # A practical audible playback band for sampled hip-hop review mixes;
        # not a mandate for final mastered music.
        if not -19.0 <= r["integratedLUFS"] <= -11.5:
            failures.append(f'{r["id"]}: loudness {r["integratedLUFS"]} LUFS is outside -19…-11.5')
        if r["truePeakDbFS"] > -0.8:
            failures.append(f'{r["id"]}: true-peak {r["truePeakDbFS"]} dBFS risks clipping')
        if r["loudnessRangeLU"]<0.2:
            failures.append(f'{r["id"]}: nearly no measured dynamic variation')
    values=[r["integratedLUFS"] for r in reports]
    summary={
        "tracks":100,
        "meanIntegratedLUFS":round(statistics.mean(values),2),
        "minIntegratedLUFS":min(values),
        "maxIntegratedLUFS":max(values),
        "highestTruePeakDbFS":max(r["truePeakDbFS"] for r in reports),
        "failedChecks":failures,
        "provenance":"NEW derived instrumental review MP3s, not certified original or paid masters"
    }
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps({"summary":summary,"tracks":reports},indent=2)+"\n",encoding="utf-8")
    print("AUDIO_QA_SUMMARY:",json.dumps(summary),flush=True)
    for r in reports:
        print(f'{r["rank"]:03d}/100 {r["id"]}: {r["integratedLUFS"]:+.1f} LUFS, TP {r["truePeakDbFS"]:+.1f} dBFS, {r["durationSeconds"]:.1f}s',flush=True)
    if failures:
        raise ValueError("Audio mastering QA failed: "+"; ".join(failures))
    print("PASS: 100 different full-length MP3 files pass loudness, true peak, codec and duration QA")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
