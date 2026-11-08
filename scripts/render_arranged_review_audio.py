#!/usr/bin/env python3
"""AXEZENT diverse arrangement-aware *review* audio renderer.

Creates NEW original synthetic/multi-instrument DEMO arrangements, not any previously
approved private originals, sold studio masters, or guarantees of professional quality.
Uses a freely distributed GM SoundFont installed separately in the build runner.
The output is intended for owner audition only and may be copied by any listener.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import random
import shutil
import subprocess
from pathlib import Path
import mido

TPQ=480
TICKS_BAR=TPQ*4
NOTE_SCALE_MAJOR=(0,2,4,5,7,9,11)
NOTE_SCALE_MINOR=(0,2,3,5,7,8,10)
ROOTS={"C":0,"C#":1,"Db":1,"D":2,"D#":3,"Eb":3,"E":4,
       "F":5,"F#":6,"Gb":6,"G":7,"G#":8,"Ab":8,"A":9,
       "A#":10,"Bb":10,"B":11}
# GM SoundFont patches are 0-based; use deliberately different instrument families.
VOICES=(
 (4,81,38,48),(5,80,39,11),(48,98,38,89),(25,83,33,62),
 (16,80,39,10),(18,88,38,48),(48,11,33,89),(62,81,38,10),
 (52,90,39,12),(19,61,33,56),(13,80,38,90),(5,98,39,47),
 (55,81,38,11),(4,24,32,90),(17,81,39,62),(24,73,33,88),
 (80,62,39,13),(2,82,38,48),(19,10,39,88),(25,81,38,89),
 (48,82,39,30),(3,16,33,48),(4,12,38,89),(5,81,39,54),
 (89,11,38,48),(62,82,34,11),(4,81,39,48),(56,80,38,10),
 (5,25,39,89),(48,11,38,89),(61,83,38,19),(16,81,39,89),
 (4,52,38,89),(5,12,33,90),(19,25,38,48),(62,11,39,89),
 (48,13,38,62),(25,80,39,89),(5,81,38,48),(88,11,39,62),
 (4,81,38,24),(89,73,33,48),(5,25,38,89),(48,81,39,19),
 (89,98,38,48),(11,81,39,55),(4,24,33,89),(5,11,38,48),
 (19,81,39,62),(62,12,38,89)
)
PROGRESSIONS=(
 (0,5,3,4),(0,6,5,3),(0,3,5,4),(0,5,6,4),(0,4,3,5),
 (0,2,5,4),(0,6,3,4),(0,5,4,3),(0,3,6,5),(0,4,5,3)
)
MELODIES=(
 (0,2,4,2,3,2,0,6),(0,4,5,4,2,1,6,0),(0,3,4,6,4,2,0,1),
 (0,6,4,2,1,2,4,5),(4,3,2,0,2,4,6,5),(0,2,3,5,3,2,1,0),
 (0,1,2,4,6,5,3,2),(0,4,3,1,0,6,4,2),(2,0,4,5,3,2,1,6),
 (0,2,5,3,1,6,4,2)
)
DRUM_VARIANTS=(
 {"kick":35,"snare":38,"hat":42,"alt":54,"open":46},
 {"kick":36,"snare":40,"hat":44,"alt":37,"open":51},
 {"kick":36,"snare":38,"hat":46,"alt":76,"open":49},
 {"kick":35,"snare":39,"hat":42,"alt":82,"open":51},
 {"kick":36,"snare":40,"hat":51,"alt":54,"open":46},
 {"kick":35,"snare":38,"hat":82,"alt":62,"open":49},
 {"kick":36,"snare":39,"hat":42,"alt":56,"open":51},
 {"kick":35,"snare":40,"hat":44,"alt":76,"open":46},
 {"kick":36,"snare":38,"hat":54,"alt":82,"open":49},
 {"kick":35,"snare":39,"hat":42,"alt":37,"open":51}
)
KICK_POCKETS=(
 (0,2.5),(0,1.5,2.75),(0,2.0,3.5),(0,1.75,2.75),
 (0,1.0,2.5,3.5),(0,2.25,3.25),(0,1.5,3.0),
 (0,0.75,2,3.25),(0,2,2.75),(0,1.25,2.5)
)
HAT_POCKETS=((0,1,2,3),(0,.5,1.5,2,3,3.5),
             (0,.5,1,1.5,2,2.5,3,3.5),(0,1.5,2.5,3.5),
             (0,2,3),(0,.75,1.5,2.25,3),(0,1,2,2.5,3.5),
             (0,.5,1,2,2.5,3.5),(0,1,1.75,2.75,3.5),
             (0,.5,1.25,2,2.75,3.5))
SOUNDS=( "no external samples: GM patches and channel-10 kit variation", )

def scale_note(root, degree, scale, octave=4):
    return int(12*(octave+1)+root+scale[degree%7]+12*(degree//7))

def parse_key(key):
    parts=str(key).split()
    root=ROOTS.get(parts[0])
    if root is None or len(parts)<2:
        raise ValueError("Unexpected key: "+str(key))
    mode=parts[1].lower()
    if mode not in ("major","minor"):
        raise ValueError("Unsupported mode")
    return root, NOTE_SCALE_MAJOR if mode=="major" else NOTE_SCALE_MINOR

class Arrangement:
    def __init__(self,beat,spec):
        self.beat=beat;self.spec=spec
        self.bpm=int(beat["bpm"])
        self.rank=int(beat["releaseRank"])
        self.root,self.scale=parse_key(beat["key"])
        self.seed=int.from_bytes(hashlib.sha256(beat["id"].encode()).digest()[:8],"big")
        self.rng=random.Random(self.seed)
        self.events=[]
        self.instruments=VOICES[self.rank-1]
        self.progression=PROGRESSIONS[(self.rank+self.seed)%len(PROGRESSIONS)]
        self.melody=MELODIES[(self.rank+self.seed//7)%len(MELODIES)]
        self.drums=DRUM_VARIANTS[(self.rank-1)%len(DRUM_VARIANTS)]
        self.drum_style=(self.rank+self.seed//29)%len(KICK_POCKETS)
        self.hat_style=(self.rank+self.seed//31)%len(HAT_POCKETS)

    def add(self,beat_tick,channel,note,velocity,length_ticks):
        tick=max(0,int(round(beat_tick)))
        if tick>=self.spec["totalBars"]*TICKS_BAR: return
        length=max(1,int(length_ticks))
        note=max(0,min(127,int(note)))
        velocity=max(1,min(127,int(velocity)))
        self.events.append((tick,1,mido.Message("note_on",channel=channel,note=note,velocity=velocity)))
        self.events.append((tick+length,0,mido.Message("note_off",channel=channel,note=note,velocity=0)))

    def percussion(self,absbeat,note,velocity=75,length=.13):
        # Channel 10 in General MIDI is channel index 9. No pitched instrument here.
        self.add(absbeat*TPQ,9,note,velocity,length*TPQ)

    def rhythm(self,bar,kind,local_bar,total_bars):
        hook=kind=="hook"
        verse=kind=="verse"
        bridge=kind in ("bridge","breakdown","pre-hook")
        intro=kind=="intro"
        outro=kind=="outro"
        # Drum families and subdivisions differ by track and section. Don't
        # stamp the same ticking hi-hat on each beat.
        kit=self.drums
        kick_positions=list(KICK_POCKETS[self.drum_style])
        if hook and local_bar%4==3: kick_positions += [3.75]
        if bridge: kick_positions=[0,2.0]
        if intro and local_bar==0: kick_positions=[0]
        if outro: kick_positions=[0,2.0]
        for j,pos in enumerate(kick_positions):
            if intro and local_bar==0 and j>0:continue
            if verse and (j==len(kick_positions)-1) and local_bar%4==0:continue
            vel=(100 if hook else 88 if verse else 73)
            jitter=self.rng.uniform(-.013,.013)
            self.percussion(bar*4+pos+max(jitter,-pos),kit["kick"],
                            vel+self.rng.randrange(-7,7),.22)
        backbeats=(1,3) if self.drum_style%4 else (2,)
        if intro and local_bar==0: backbeats=()
        for k,pos in enumerate(backbeats):
            self.percussion(bar*4+pos,kit["snare"],88 if hook else 78,.18)
            if hook and (bar+k)%3==0:
                self.percussion(bar*4+pos+.013,39,51,.11)
        # Different texture sources: rim, shaker, ride, tambourine, closed/open
        # hats or almost no top percussion, depending on the selected kit.
        hats=HAT_POCKETS[self.hat_style]
        if bridge: hats=(0,2)
        if intro: hats=(0,2) if local_bar%2==0 else (1,3)
        if outro: hats=(0,2)
        for j,pos in enumerate(hats):
            if verse and j%5==3:continue
            texture=kit["hat"] if j%4 else kit["alt"]
            v=int((47 if hook else 37 if verse else 28) + (j%3)*7 +
                  self.rng.uniform(-8,8))
            self.percussion(bar*4+pos+self.rng.uniform(-.008,.008),
                            texture,v,.07)
        if local_bar%4==3 and hook:
            self.percussion(bar*4+3.5,kit["open"],64,.32)
        if local_bar==total_bars-1 and kind not in ("outro","intro"):
            for i,p in enumerate((3,3.25,3.5,3.75)):
                self.percussion(bar*4+p,kit["snare"] if i%2 else 45,48+i*7,.12)

    def harmony(self,bar,kind,local_bar):
        prog=self.progression[(bar//4)%4]
        hook=kind=="hook"
        bridge=kind in ("bridge","breakdown")
        # Root, third, fifth. All chords are diatonic to the assigned mode.
        scale=self.scale
        notes=[scale_note(self.root,prog+d,scale,4) for d in (0,2,4)]
        if kind=="outro" and local_bar%2: return
        if bridge: notes=notes[:2]
        if kind=="intro": notes=notes[-2:]
        for j,n in enumerate(notes):
            self.add(bar*TICKS_BAR+j*5,0,n,
                     52 if hook else 40 if kind=="verse" else 35,
                     TICKS_BAR*(.76 if hook else .9))
        # Sparse rhythm stabs in hooks, deliberately reduced beneath verses.
        if hook and local_bar%2==0:
            for j,n in enumerate(notes):
                self.add((bar*4+2.5)*TPQ+j*4,0,n,42,TPQ*.45)
        # Low end follows the kick/bass motion instead of one constant keyboard
        # sound. Bass instrument patch and octave vary across the 50 tracks.
        bass=scale_note(self.root,prog,scale,2)
        if kind=="intro":
            bass_positions=(0,2)
        elif hook:
            bass_positions=(0,1.5,2.5,3.25)
        elif bridge:
            bass_positions=(0,2)
        else:
            bass_positions=(0,1.75,2.75)
        for pos in bass_positions:
            bnote=bass + (12 if (local_bar%8==7 and pos>2) else 0)
            self.add((bar*4+pos)*TPQ,2,bnote,89 if hook else 75,TPQ*.82)

    def musical_phrase(self,bar,kind,local_bar):
        if kind in ("outro","bridge","breakdown"):
            return
        if kind=="intro" and local_bar==0:return
        hook=kind=="hook"
        pattern=self.melody
        note_count=(4 if hook else 2)
        if local_bar%4==3:note_count+=1
        prog=self.progression[(bar//4)%4]
        lead_oct=5 if self.rank%4 else 4
        for i in range(note_count):
            idx=(local_bar*2+i)%len(pattern)
            degree=(prog+pattern[idx])%7
            n=scale_note(self.root,degree,self.scale,lead_oct)
            pos=(.0,1.5,2.5,3.25,3.75)[i]
            duration=(.52 if hook else .4)*TPQ
            velocity=(68 if hook else 43)+self.rng.randint(-7,7)
            self.add((bar*4+pos)*TPQ,1,n,velocity,duration)
        if hook and local_bar%2==1:
            # Different complementary patch and phrase: no full keyboard
            # chord pileup during verses.
            n=scale_note(self.root,(prog+4)%7,self.scale,4)
            self.add((bar*4+3)*TPQ,3,n,40,TPQ*.55)

    def build_midi(self,outpath):
        mf=mido.MidiFile(type=1,ticks_per_beat=TPQ)
        conductor=mido.MidiTrack()
        conductor.append(mido.MetaMessage("set_tempo",tempo=mido.bpm2tempo(self.bpm),time=0))
        conductor.append(mido.MetaMessage("time_signature",numerator=4,denominator=4,time=0))
        conductor.append(mido.MetaMessage("track_name",name=self.beat["title"]+" — AXEZENT new review draft",time=0))
        mf.tracks.append(conductor)
        setup=mido.MidiTrack()
        for channel,patch in zip((0,1,2,3),self.instruments):
            setup.append(mido.Message("program_change",channel=channel,program=patch,time=0))
            setup.append(mido.Message("control_change",channel=channel,control=10,value=(44,85,64,100)[channel],time=0))
            setup.append(mido.Message("control_change",channel=channel,control=7,value=(75,96,112,61)[channel],time=0))
        mf.tracks.append(setup)
        for sec in self.spec["sections"]:
            kind=sec["kind"]
            for local_bar in range(sec["bars"]):
                bar=sec["startBar"]+local_bar
                self.harmony(bar,kind,local_bar)
                self.rhythm(bar,kind,local_bar,sec["bars"])
                self.musical_phrase(bar,kind,local_bar)
        # One music track with deterministic, sorted MIDI events.
        target=mido.MidiTrack()
        last=0
        for tick,priority,msg in sorted(self.events,key=lambda e:(e[0],e[1],e[2].channel,e[2].note)):
            target.append(msg.copy(time=tick-last))
            last=tick
        endtick=self.spec["totalBars"]*TICKS_BAR
        target.append(mido.MetaMessage("end_of_track",time=max(0,endtick-last)))
        mf.tracks.append(target)
        mf.save(outpath)
        return len(self.events)

def prepare_review(beat,spec,outpath,soundfont,rate=32000):
    if beat["bpm"]!=spec["bpm"] or beat["releaseRank"]!=spec["releaseRank"]:
        raise ValueError("Arrangement metadata does not match catalog")
    outpath.parent.mkdir(parents=True,exist_ok=True)
    midi=outpath.with_suffix(".mid")
    wave=outpath.with_suffix(".wav")
    arranger=Arrangement(beat,spec)
    events=arranger.build_midi(midi)
    # Low-footprint offline rendering: the 6 MB GM SoundFont is provided by
    # the job environment; no samples or original private recordings enter repo.
    subprocess.run(["fluidsynth","-ni","-F",str(wave),"-r",str(rate),str(soundfont),str(midi)],
                   check=True,stdout=subprocess.DEVNULL)
    duration=float(spec["durationSeconds"])
    # Normalize conservatively; cut the tail to the exact planned duration.
    subprocess.run(["ffmpeg","-hide_banner","-nostdin","-loglevel","error","-y",
        "-i",str(wave),"-af","highpass=f=27,acompressor=threshold=-17dB:ratio=2.2:attack=15:release=120,alimiter=limit=0.91",
        "-t",str(duration),"-c:a","libmp3lame","-ar",str(rate),"-ac","2","-b:a","128k",str(outpath)],
        check=True)
    midi.unlink(missing_ok=True)
    wave.unlink(missing_ok=True)
    if outpath.stat().st_size<150000:
        raise RuntimeError("Silent or empty rendered preview "+str(outpath))
    ff=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries",
             "format=duration,size:stream=codec_name,channels,sample_rate","-of","json",str(outpath)]))
    audio=ff["streams"][0]
    actual=float(ff["format"]["duration"])
    if (audio["codec_name"]!="mp3" or audio["channels"]!=2 or
            abs(actual-duration)>1.0):
        raise RuntimeError("Audio codec/duration mismatch "+str(outpath))
    return {"id":beat["id"],"durationSeconds":round(actual,3),
            "size":outpath.stat().st_size,"midiEvents":events,
            "qualityStatus":"NEW synthetic review mix; requires producer approval; NOT the original private recording or paid master"}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--catalog",default="data/catalog.json")
    p.add_argument("--arrangements",default="data/arrangements.json")
    p.add_argument("--out",required=True)
    p.add_argument("--soundfont",default="/usr/share/sounds/sf2/TimGM6mb.sf2")
    p.add_argument("--start",type=int,default=1)
    p.add_argument("--end",type=int,default=50)
    a=p.parse_args()
    catalogue=json.loads(Path(a.catalog).read_text("utf-8"))
    spec=json.loads(Path(a.arrangements).read_text("utf-8"))
    beats=sorted((b for b in catalogue if isinstance(b.get("releaseRank"),int)
                  and 1<=b["releaseRank"]<=50),key=lambda b:b["releaseRank"])
    if len(beats)!=50 or len(spec)!=50:raise ValueError("Expected 50 beats and plans")
    if not Path(a.soundfont).is_file():raise FileNotFoundError(a.soundfont)
    if not shutil.which("fluidsynth") or not shutil.which("ffmpeg"):
        raise RuntimeError("fluidsynth and ffmpeg are required for rendering")
    report=[]
    for beat in beats:
        if not a.start<=beat["releaseRank"]<=a.end:continue
        output=Path(a.out)/(beat["id"]+"-review.mp3")
        result=prepare_review(beat,spec[beat["id"]],output,a.soundfont)
        report.append(result)
        print(f"{beat['releaseRank']:02}/50 {beat['id']} {beat['title']} {result['durationSeconds']} s {result['size']//1000} KB",flush=True)
    (Path(a.out)/"REVIEW_REPORT.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":main()
