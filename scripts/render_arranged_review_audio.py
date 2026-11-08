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
# Individually curated from each release-rank arrangement's soundPalette.
# 0-based General MIDI programs. Keep deliberately different bass techniques
# and instrument families; the old random list reused only five bass programs.
VOICES=(
 (4,81,39,61),(5,10,38,7),(48,98,39,95),(4,80,36,28),
 (89,83,39,10),(19,44,38,2),(42,13,35,4),(90,61,39,11),
 (91,80,39,5),(0,61,33,17),(12,10,39,52),(5,45,38,50),
 (93,62,38,48),(4,28,32,45),(18,29,36,81),(31,4,35,89),
 (7,62,39,28),(0,10,38,61),(19,14,39,0),(24,11,35,88),
 (30,48,39,81),(0,29,33,19),(4,24,33,90),(93,12,39,5),
 (88,12,35,50),(62,28,38,0),(16,7,32,4),(61,83,36,7),
 (4,31,35,89),(92,10,39,61),(61,11,38,45),(81,11,38,16),
 (0,45,34,42),(5,12,33,19),(16,24,32,4),(61,0,38,48),
 (12,48,35,19),(24,61,33,10),(80,11,34,4),(89,45,39,61),
 (11,24,37,90),(19,73,35,95),(4,31,32,89),(48,4,35,19),
 (10,98,39,48),(11,81,39,55),(89,24,34,11),(4,17,32,45),
 (16,5,38,93),(98,5,38,61)
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
# Psychological groove in music means audible pattern, contrast and motion;
# not a claim about hypnosis or a guaranteed audience response.
GROOVE_FAMILIES = ("drill", "trap", "club", "boom_bap", "swing", "ambient", "bounce")
def groove_family(signature):
    name = str(signature).lower()
    if "drill" in name:
        return "drill"
    if "trap" in name or "808" in name:
        return "trap"
    if "club" in name or "kick-triplet" in name:
        return "club"
    if "boom-bap" in name or "head-nod" in name:
        return "boom_bap"
    if "second-line" in name or "swing" in name or "funk" in name or "soul" in name:
        return "swing"
    if any(k in name for k in ("cinematic","atmospheric","downtempo","slow","ambient","half-time","halftime")):
        return "ambient"
    return "bounce"

# Verse-only counter-rhythms: melodies remain subordinate to the rapper.
# Each focus song has its own motif, placement and percussion accent.
VERSE_FOCUS = {
    "AXZ-049": ((0, 4, 2, 5), (.75, 2.25, 3.5), 37),  # Chicago: syncopated keys/rim
    "AXZ-125": ((5, 3, 2, 0), (.5, 2.0, 3.25), 40),   # Bronx: descending drill response
    "AXZ-117": ((0, 2, 5, 3), (1.0, 2.5, 3.5), 39),   # Newark: offbeat organ/clap
    "AXZ-001": ((0, 3, 4, 6), (.5, 2.0, 3.0), 45),    # Alabama: rising cinematic/tom
    "AXZ-021": ((4, 2, 0, 5), (.75, 2.5, 3.25), 54),  # Denver: airy answer/tambourine
    "AXZ-185": ((5, 4, 2, 0), (1.0, 2.75, 3.5), 76),  # Seattle: descending/woodblock
}
VERSE_LIBRARY = (
    ((0, 2, 4, 1), (.75, 2.25), 37),
    ((4, 2, 0, 5), (.5, 2.75), 54),
    ((0, 3, 5, 2), (1.0, 3.25), 39),
    ((5, 3, 1, 0), (.75, 2.5), 45),
    ((2, 4, 0, 3), (1.25, 3.0), 76),
    ((0, 4, 6, 2), (.5, 2.25), 40),
)


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
        self.groove=groove_family(spec.get("signature",""))
        self.rap_space=self.rank % 4
        self.swing_delay=(.075 if self.groove=="swing" else
                          .035 if self.groove=="boom_bap" else 0)
        self.progression=PROGRESSIONS[(self.rank+self.seed)%len(PROGRESSIONS)]
        source=MELODIES[(self.rank+self.seed//7)%len(MELODIES)]
        rot=(self.seed//211)%len(source)
        # Melodic rotation changes the actual MIDI notes, not merely MP3 hashes.
        self.melody=tuple(source[(i+rot)%len(source)] for i in range(len(source)))
        self.drums=DRUM_VARIANTS[(self.rank-1)%len(DRUM_VARIANTS)]
        self.drum_style=(self.rank+self.seed//29)%len(KICK_POCKETS)
        self.hat_style=(self.rank+self.seed//31)%len(HAT_POCKETS)

    def chord_degree(self, kind, local_bar):
        """Section-locked chord loop: a repeated hook must return on the
        same harmony, not drift when the song has different verse lengths."""
        step=(local_bar//4) % len(self.progression)
        return self.progression[step]

    def add(self,beat_tick,channel,note,velocity,length_ticks):
        tick=max(0,int(round(beat_tick)))
        if tick>=self.spec["totalBars"]*TICKS_BAR: return
        length=max(1,int(length_ticks))
        # Pitched GM notes must not hang across the next chord/bar; otherwise
        # the lead, bass and counter-note overlap unrelated harmonic changes.
        if channel in (0,1,2,3):
            length=min(length,max(1,TICKS_BAR-(tick%TICKS_BAR)-6))
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
        # A region-aware performance pocket, with alternate bars and deliberate
        # gaps for rap rather than one global four-on-the-floor recipe.
        if self.groove=="drill":
            kick_positions=[0,.75,2.75] if local_bar%2 else [0,1.75,2.5]
        elif self.groove=="trap":
            kick_positions=[0,1.5,2.75] if local_bar%2 else [0,2.25,3.25]
        elif self.groove=="boom_bap":
            kick_positions=[0,2.5] if local_bar%2 else [0,1.75,2.75]
        elif self.groove=="club":
            kick_positions=[0,.75,1.5,2.75] if local_bar%2 else [0,1.5,2.5,3.25]
        elif self.groove=="swing":
            kick_positions=[0,1.75,2.5] if local_bar%2 else [0,2.25,3.25]
        elif self.groove=="ambient":
            kick_positions=[0,2.5] if local_bar%2 else [0,1.75,3]
        else:
            # Keep the seeded track-specific pocket but vary last beat by phrase.
            if local_bar%4==2:
                kick_positions=kick_positions[:-1]+[3.25]
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
        backbeats=(2,) if self.groove in ("drill","trap","ambient") else (1,3)
        if self.groove=="bounce" and self.drum_style%4==0: backbeats=(2,)
        if intro and local_bar==0: backbeats=()
        for k,pos in enumerate(backbeats):
            self.percussion(bar*4+pos,kit["snare"],88 if hook else 78,.18)
            if hook and (bar+k)%3==0:
                self.percussion(bar*4+pos+.013,39,51,.11)
        # Different texture sources: rim, shaker, ride, tambourine, closed/open
        # hats or almost no top percussion, depending on the selected kit.
        hats=HAT_POCKETS[self.hat_style]
        if self.groove in ("trap","drill") and hook and local_bar%4==3:
            # Twelve sharp hats plus four other drums was a distracting fill
            # in every fourth verse bar. Save one modest roll for the hook.
            hats=(0,.5,1,1.5,2,2.5,3,3.25,3.5,3.75)
        elif self.groove=="ambient":
            hats=(0,1.5,3) if local_bar%2 else (0,2,3.5)
        elif self.groove=="swing":
            hats=(0,.75,1.5,2.25,3)
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
        prog=self.chord_degree(kind,local_bar)
        hook=kind=="hook"
        bridge=kind in ("bridge","breakdown")
        # Root, third, fifth. All chords are diatonic to the assigned mode.
        scale=self.scale
        notes=[scale_note(self.root,prog+d,scale,4) for d in (0,2,4)]
        if kind=="outro" and local_bar%2: return
        if bridge: notes=notes[:2]
        if kind=="intro": notes=notes[-2:]
        if kind=="verse":
            # Vocal space beats stacked synths. Use simple shells for
            # half-time/club; leave the turnaround open rather than sustaining
            # three-note chords through every rapper pickup.
            if self.groove in ("drill","trap","club","ambient"):
                notes=notes[:2] if local_bar%4!=3 else []
            elif local_bar%4==3:
                notes=notes[:2]
        chord_len=(.76 if hook else .85 if self.groove=="ambient"
                   else .57 if kind=="verse" else .8)
        for j,n in enumerate(notes):
            self.add(bar*TICKS_BAR+j*5,0,n,
                     52 if hook else 37 if kind=="verse" else 35,
                     TICKS_BAR*chord_len)
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
        elif kind=="verse":
            bass_pockets=((0,1.75,2.75),(0,.75,2.25,3.25),
                          (0,1.5,2.75),(0,1.25,2.5,3.5))
            bass_positions=bass_pockets[(self.rank+local_bar//4)%len(bass_pockets)]
        else:
            bass_positions=(0,1.75,2.75)
        for pos in bass_positions:
            bnote=bass + (12 if (local_bar%8==7 and pos>2) else 0)
            # Remove a few low-end hits from lyric pickup bars, keeping the
            # downbeat and kick, then answer in the second half of each bar.
            if kind=="verse" and local_bar%8==0 and pos not in (0,2.75):
                continue
            self.add((bar*4+pos)*TPQ,2,bnote,86 if hook else 72,TPQ*.74)

    def musical_phrase(self,bar,kind,local_bar):
        if kind in ("outro","bridge","breakdown"):
            return
        if kind=="intro" and local_bar==0:
            return
        hook=kind=="hook"
        verse=kind=="verse"
        pattern=self.melody
        # Hooks supply the memorable call; verses leave the first two beats
        # open for the rapper and answer only after the vocal pickup.
        if hook:
            note_count=4+(local_bar%4==3)
            positions=(0,1.25,2.25,3.25,3.75)
        elif verse:
            note_count=(1,2,1,2)[local_bar%4]
            positions=(2.0,3.0,3.5)
        else:
            note_count=2
            positions=(.5,2.75)
        prog=self.chord_degree(kind,local_bar)
        # Keep dense rap styles near the middle piano register. The old
        # 75% high-octave synth leads could compete with the vocal.
        lead_oct=(4 if self.groove in ("drill","trap","boom_bap","swing")
                  else 5 if self.rank%3==0 else 4)
        for i in range(note_count):
            idx=(local_bar*2+i+self.rap_space)%len(pattern)
            hook_answer=1 if hook and local_bar%8>=4 else 0
            degree=(prog+pattern[idx]+hook_answer)%7
            n=scale_note(self.root,degree,self.scale,lead_oct)
            pos=positions[i]
            duration=(.51 if hook else .37)*TPQ
            velocity=(70 if hook else 44 if verse else 43)+self.rng.randint(-5,5)
            self.add((bar*4+pos)*TPQ,1,n,velocity,duration)
        if hook and local_bar%2==1:
            # Counter-instrument only at the end of the hook, not over verses.
            n=scale_note(self.root,(prog+4+self.rank%3)%7,self.scale,4)
            self.add((bar*4+3)*TPQ,3,n,41,TPQ*.46)

    def verse_detail(self, bar, local_bar):
        """Vary verses independently of hooks; retain space for lead vocals.

        Sparse answers after the vocal pickup, with a four-bar contour,
        independently selected for all 50 tracks, plus restrained ghost drums.
        The six owner-identified verses receive distinct deterministic motifs.
        """
        motif, pulses, accent = VERSE_FOCUS.get(
            self.beat["id"],
            VERSE_LIBRARY[(self.rank + self.seed // 19) % len(VERSE_LIBRARY)]
        )
        # The remaining 44 verses must not be six near-identical motifs.
        if self.beat["id"] not in VERSE_FOCUS:
            offset=(self.rank+self.seed//37)%7
            motif=tuple((x+offset)%7 for x in motif)
        phrase = local_bar % 4
        cycle = (local_bar // 4) % 3
        chord_degree = self.chord_degree("verse",local_bar)
        # Previously the counter-part always played 2-3 notes per bar, while
        # the lead, bass and chords were already active. In a piano roll this
        # was more notes than an instrumental supporting a full rap verse needs.
        # Four-bar response: rest / one note / one note / two-note answer.
        candidates=[(i,pos) for i,pos in enumerate(pulses) if pos>=2.0]
        candidates=sorted(candidates,key=lambda p:p[1])
        if phrase==0:
            chosen=[]
        elif phrase==3:
            chosen=candidates[-2:]
        else:
            chosen=candidates[-1:]
        for i,pos in chosen:
            degree=(chord_degree+motif[(phrase+cycle+i)%len(motif)])%7
            low_answer=self.beat["id"] in ("AXZ-125","AXZ-001") and i==0
            octave=3 if low_answer else 4
            pitch=scale_note(self.root,degree,self.scale,octave)
            velocity=35+(self.rank%7)+(5 if phrase==3 else 0)
            self.add((bar*4+pos)*TPQ,3,pitch,velocity,TPQ*.27)
        if phrase==3:
            self.percussion(bar*4+3.5,accent,35+self.rank%9,.09)
            self.percussion(bar*4+3.75,self.drums["snare"],38,.10)

    def build_midi(self,outpath):
        mf=mido.MidiFile(type=1,ticks_per_beat=TPQ)
        conductor=mido.MidiTrack()
        conductor.append(mido.MetaMessage("set_tempo",tempo=mido.bpm2tempo(self.bpm),time=0))
        conductor.append(mido.MetaMessage("time_signature",numerator=4,denominator=4,time=0))
        conductor.append(mido.MetaMessage("track_name",name=self.beat["title"]+" - AXEZENT new review draft",time=0))
        mf.tracks.append(conductor)
        setup=mido.MidiTrack()
        # Lift the sampled percussion bus slightly; the earlier default patch
        # balance put kick and snare too far beneath sustained low-end notes.
        setup.append(mido.Message("control_change",channel=9,control=7,value=122,time=0))
        for channel,patch in zip((0,1,2,3),self.instruments):
            setup.append(mido.Message("program_change",channel=channel,program=patch,time=0))
            setup.append(mido.Message("control_change",channel=channel,control=10,value=(44,85,64,100)[channel],time=0))
            setup.append(mido.Message("control_change",channel=channel,control=7,value=(75,96,105,61)[channel],time=0))
        mf.tracks.append(setup)
        for sec in self.spec["sections"]:
            kind=sec["kind"]
            for local_bar in range(sec["bars"]):
                bar=sec["startBar"]+local_bar
                self.harmony(bar,kind,local_bar)
                self.rhythm(bar,kind,local_bar,sec["bars"])
                self.musical_phrase(bar,kind,local_bar)
                if kind=="verse":
                    self.verse_detail(bar,local_bar)
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

def prepare_review(beat,spec,outpath,soundfont,rate=44100):
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
    # The first V2 review output was measured at -30 to -38 LUFS and extremely
    # bass-heavy: not suitable for reliable casual listening. This corrective
    # streaming mix reduces sub/low-mid masking, clarifies hats/snare presence,
    # applies dynamics control, then EBU-R128 normalization with a conservative
    # true-peak ceiling. It is NOT a claim of artist-approved mastering.
    # Cold Cash Season has a sharper codec-reconstructed transient than the
    # other 49 mixes. Lower only this mix's limiter ceiling; do not turn down
    # the whole album or erase its drum transients.
    limiter_ceiling = 0.65 if beat["id"] == "AXZ-133" else 0.76
    filters=(
        "highpass=f=28,"
        "bass=g=-5:f=155:w=0.7,"
        "equalizer=f=900:width_type=o:width=1.1:g=2,"
        "equalizer=f=2500:width_type=o:width=1:g=3,"
        "treble=g=5:f=4300:w=0.65,"
        "acompressor=threshold=-23dB:ratio=2.6:attack=12:release=150:makeup=3,"
        "loudnorm=I=-14:TP=-2.5:LRA=8,"
        f"alimiter=limit={limiter_ceiling:.2f}:level=false"
    )
    subprocess.run(["ffmpeg","-hide_banner","-nostdin","-loglevel","error","-y",
        "-i",str(wave),"-af",filters,
        "-t",str(duration),"-c:a","libmp3lame","-ar",str(rate),"-ac","2","-b:a","160k",str(outpath)],
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
    p.add_argument("--soundfont",default="/usr/share/sounds/sf2/FluidR3_GM.sf2")
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
