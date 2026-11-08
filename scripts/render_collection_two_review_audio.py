#!/usr/bin/env python3
"""Render original 50 regional Collection Two *synthetic review* instrumentals.

These new reviews apply the owner's specific 50 city/BPM/key/voice/song-form
blueprints to the existing deterministic composition engine. They are NOT
the source ZIP's exact MIDI performance or certified sale-ready studio masters.
No copyrighted reference song or sample is loaded.
"""
from __future__ import annotations
import argparse
import json
import hashlib
import os
import shutil
import subprocess
import mido
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.collection_two import ROOT, load_collection_two, make_collection_two_catalog
from scripts.render_arranged_review_audio import Arrangement, KICK_POCKETS, HAT_POCKETS

def region_groove(description):
    d=description.lower()
    if "drill" in d: return "drill"
    if any(x in d for x in ("hyphy","flint","bounce","snap","chopper")): return "bounce"
    if any(x in d for x in ("club","party","jersey")): return "club"
    if "trap" in d or "808" in d: return "trap"
    if any(x in d for x in ("funk","soul","bluegrass","live-band","blues")): return "swing"
    if any(x in d for x in ("boom-bap","lyrical","east coast","punchline","grimy")):
        return "boom_bap"
    if any(x in d for x in ("reflective","melodic","nocturnal","ambient","minimalist")):
        return "ambient"
    return "bounce"

class CollectionTwoArrangement(Arrangement):
    def __init__(self, beat, spec, blueprint):
        # The base songwriter has 50 instrument slots. Give each new track
        # its own internal slot but retain its actual 51-100 public identity.
        local_rank=blueprint["releaseRank"]-50
        source_beat=dict(beat,releaseRank=local_rank)
        source_spec=dict(spec,releaseRank=local_rank)
        super().__init__(source_beat,source_spec)
        self.beat=beat
        self.spec=spec
        self.instruments=tuple(blueprint["gmPrograms"])
        self.groove=region_groove(blueprint["groove"])
        self.rank=local_rank
        # Deliberately break the old first-50 instrument and drum-pocket
        # assignments; both groove choice and kit accent now follow the
        # separate city blueprint and musical fingerprint.
        salt=int.from_bytes(hashlib.sha256(
            (beat["id"]+"|"+blueprint["groove"]).encode()).digest()[:4],"big")
        self.drum_style=(salt//7+local_rank)%len(KICK_POCKETS)
        self.hat_style=(salt//19+local_rank*3)%len(HAT_POCKETS)
        self.rap_space=salt%4
        self.swing_delay=.085 if self.groove=="swing" else (
            .04 if self.groove=="boom_bap" else 0)

    # A/B ONLY: improve the four measured mix-review flags without touching
    # any first-collection MIDI or all other Collection Two songs. Not a
    # psychoacoustic patent or guarantee of human approval.
    def add(self, beat_tick, channel, note, velocity, length_ticks):
        if os.environ.get("AXEZENT_MIX_AB_BASELINE")!="1" and self.beat["id"] in ("AXZ-187","AXZ-110"):
            bar=int(beat_tick)//(480*4)
            section=next((s for s in self.spec["sections"]
                if s["startBar"]<=bar<s["endBar"]),None)
            if section and section["kind"]=="hook":
                if channel in (0,1,2,3):
                    velocity=min(127,velocity+9)
                elif channel==9 and note in (35,36,38,39,40):
                    velocity=min(127,velocity+5)
        super().add(beat_tick,channel,note,velocity,length_ticks)

    def build_midi(self,outpath):
        count=super().build_midi(outpath)
        if os.environ.get("AXEZENT_MIX_AB_BASELINE")=="1" or self.beat["id"] not in ("AXZ-172","AXZ-010"):
            return count
        # Only newly flagged songs: bring outer melodic voices nearer the
        # center. Bass (channel 2) stays exactly centered at pan 64.
        mid=mido.MidiFile(outpath)
        pan={0:55,1:73,2:64,3:77}
        found=set()
        for track in mid.tracks:
            for msg in track:
                if msg.type=="control_change" and msg.control==10 and msg.channel in pan:
                    msg.value=pan[msg.channel]
                    found.add(msg.channel)
        if found!={0,1,2,3}:
            raise RuntimeError("Cannot locate four expected MIDI pan controllers")
        mid.save(outpath)
        return count

def render(beat,spec,blueprint,outpath,soundfont):
    arranger=CollectionTwoArrangement(beat,spec,blueprint)
    outpath.parent.mkdir(parents=True,exist_ok=True)
    midi=outpath.with_suffix(".mid")
    wave=outpath.with_suffix(".wav")
    midi_events=arranger.build_midi(midi)
    subprocess.run(["fluidsynth","-ni","-F",str(wave),"-r","44100",
                    str(soundfont),str(midi)],check=True,stdout=subprocess.DEVNULL)
    # The original 50's tested sound chain, with conservative codec true peak.
    filters=(
        "highpass=f=28,"
        "bass=g=-5:f=155:w=0.7,"
        "equalizer=f=900:width_type=o:width=1.1:g=2,"
        "equalizer=f=2500:width_type=o:width=1:g=3,"
        "treble=g=5:f=4300:w=0.65,"
        "acompressor=threshold=-23dB:ratio=2.6:attack=12:release=150:makeup=3,"
        "loudnorm=I=-14:TP=-2.5:LRA=8,"
        "alimiter=limit=0.72:level=false"
    )
    subprocess.run(["ffmpeg","-hide_banner","-nostdin","-loglevel","error",
         "-y","-i",str(wave),"-af",filters,
         "-t",str(spec["durationSeconds"]),"-c:a","libmp3lame",
         "-ar","44100","-ac","2","-b:a","160k",str(outpath)],check=True)
    midi.unlink(missing_ok=True)
    wave.unlink(missing_ok=True)
    if outpath.stat().st_size<150_000 or midi_events<200:
        raise RuntimeError("Missing or underdeveloped instrumental preview "+beat["id"])
    meta=json.loads(subprocess.check_output(["ffprobe","-v","error",
        "-show_entries","format=duration:stream=codec_name,channels,sample_rate",
        "-of","json",str(outpath)]))
    if meta["streams"][0]["codec_name"]!="mp3" or meta["streams"][0]["channels"]!=2:
        raise RuntimeError("Not a valid stereo MP3 "+beat["id"])
    if abs(float(meta["format"]["duration"])-spec["durationSeconds"])>1:
        raise RuntimeError("Section duration doesn't match rendered preview "+beat["id"])
    return {"id":beat["id"],"releaseRank":beat["releaseRank"],
            "midiEvents":midi_events,"durationSeconds":round(float(meta["format"]["duration"]),3),
            "bytes":outpath.stat().st_size,"groove":arranger.groove,
            "reviewOnly":True,
            "source":"New deterministic musical rendering of owner-prepared city/arrangement blueprint; not the previously uploaded full MIDI sketch or commercial artist audio"}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--start",type=int,required=True)
    p.add_argument("--end",type=int,required=True)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--soundfont",type=Path,
        default=Path("/usr/share/sounds/sf2/FluidR3_GM.sf2"))
    a=p.parse_args()
    if not a.soundfont.is_file() or not shutil.which("fluidsynth") or not shutil.which("ffmpeg"):
        raise RuntimeError("The tested FluidSynth soundfont and FFmpeg are required")
    if a.start<51 or a.end>100 or a.end<a.start:raise ValueError("Second collection range 51–100 only")
    catalog=json.loads((ROOT/"data"/"catalog.json").read_text("utf-8"))
    arrangements=json.loads((ROOT/"data"/"arrangements.json").read_text("utf-8"))
    rows,plans=make_collection_two_catalog(catalog,arrangements)
    by_rank={row["releaseRank"]:row for row in rows if isinstance(row.get("releaseRank"),int)}
    blueprints={row["releaseRank"]:row for row in load_collection_two()}
    report=[]
    for rank in range(a.start,a.end+1):
        beat=by_rank[rank]
        path=a.out/(beat["id"]+"-review.mp3")
        info=render(beat,plans[beat["id"]],blueprints[rank],path,a.soundfont)
        report.append(info)
        print("COLLECTION_TWO_TRACK:",json.dumps(info),flush=True)
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/"REVIEW_REPORT.json").write_text(json.dumps(report,indent=2)+"\n")
    if len(report)!=(a.end-a.start+1):raise RuntimeError("Incomplete render")
    print("PASS:",len(report),"distinct full-length Collection Two review instrumentals",flush=True)

if __name__=="__main__":
    main()
