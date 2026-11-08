#!/usr/bin/env python3
"""AXEZENT A–Z selective original arrangement variation (review mixes, not masters).

Deterministic musical humanisation, phrase and timbre variation for tracks that
showed weak hook contrast, high spectral similarity, or mix compatibility flags.
Modifies generated MIDI, NOT anyone else's source recordings, stems or masters.
No magical 'feel-good frequency' claims or commercially licensed samples.
"""
from __future__ import annotations
import hashlib
import math
from pathlib import Path
import mido
from scripts.render_arranged_review_audio import TPQ,TICKS_BAR,parse_key,scale_note

# Based on independently measured 100-track audible review and MIDI note-grid audits.
WEAK_HOOK_IDS=frozenset("""
AXZ-021 AXZ-185 AXZ-181 AXZ-001 AXZ-089 AXZ-013 AXZ-189 AXZ-005
AXZ-073 AXZ-101 AXZ-172 AXZ-070 AXZ-187 AXZ-110
""".split())
SIMILAR_PAIRS=(
 ("AXZ-129","AXZ-193"),("AXZ-169","AXZ-186"),
 ("AXZ-125","AXZ-161"),("AXZ-033","AXZ-133"),
 ("AXZ-157","AXZ-090"),("AXZ-169","AXZ-015"),
 ("AXZ-089","AXZ-015"),("AXZ-173","AXZ-083"),
 ("AXZ-081","AXZ-025"),("AXZ-077","AXZ-119"),
)
MONO_REVIEW_IDS=frozenset(("AXZ-172","AXZ-010","AXZ-110"))
HOOK_ENERGY_IDS=frozenset(("AXZ-187","AXZ-110"))
PRIORITY_IDS=WEAK_HOOK_IDS | frozenset(x for pair in SIMILAR_PAIRS for x in pair) | MONO_REVIEW_IDS

# Timbral palette expands the previous 10 repeating patch families; 0-based GM
# choices retain compatibility with current FluidR3 renderer and permissions.
LEAD_PATCHES=(4,5,10,11,12,13,14,16,17,18,24,26,28,30,31,44,45,48,
              53,61,62,73,80,81,83,88,89,90,91,92,93,95,98,99,100,101)
ANSWER_PATCHES=(4,7,10,11,12,13,16,19,24,28,42,44,45,48,50,52,53,
                61,62,73,81,89,90,91,93,98,99)
DRUM_ACCENTS=(37,39,40,42,44,46,54,56,62,70,71,73,75,76,82)

def stable_int(*parts):
    return int.from_bytes(hashlib.sha256("|".join(map(str,parts)).encode()).digest()[:8],"big")

def targeted(beat):
    return beat["id"] in PRIORITY_IDS

def enhance_midi(midi:Path,beat:dict,plan:dict)->dict:
    """Mutate a freshly generated temporary MIDI in place; source plan unchanged.

    Phrase changes are deterministic across repeated refrains and keep verse
    first-half foreground clear. Intentional variety is section aware.
    """
    ident=beat["id"]
    if ident not in PRIORITY_IDS:
        return {"id":ident,"enhanced":False,"addedNotePairs":0,"newPrograms":{}}
    mf=mido.MidiFile(midi)
    if len(mf.tracks)<3:
        raise RuntimeError("Unexpected missing MIDI music track "+ident)
    seed=stable_int(ident,beat["key"],beat["bpm"])
    root,scale=parse_key(beat["key"])
    programs={
       1:LEAD_PATCHES[stable_int(ident,"lead")%len(LEAD_PATCHES)],
       3:ANSWER_PATCHES[stable_int(ident,"answer")%len(ANSWER_PATCHES)]
    }
    if programs[1]==programs[3]:
        programs[3]=ANSWER_PATCHES[(stable_int(ident,"answer")+5)%len(ANSWER_PATCHES)]
    for track in mf.tracks:
        for msg in track:
            if msg.type=="program_change" and msg.channel in programs:
                msg.program=programs[msg.channel]
    original=mf.tracks[-1]
    events=[]
    absolute=0
    for msg in original:
        absolute+=msg.time
        if msg.type=="end_of_track":
            continue
        order=0 if msg.type=="note_off" or (msg.type=="note_on" and msg.velocity==0) else 1
        events.append((absolute,order,msg.copy(time=0)))
    song_ticks=plan["totalBars"]*TICKS_BAR
    added=0
    def insert(bar,pos,channel,pitch,vel,length):
        nonlocal added
        start=int(round((bar*4+pos)*TPQ))
        stop=start+int(round(length*TPQ))
        if start<0 or stop>=song_ticks: return
        if stop>(bar+1)*TICKS_BAR:
            stop=(bar+1)*TICKS_BAR-4
        if stop<=start:return
        velocity=max(8,min(105,int(vel)))
        events.append((start,1,mido.Message("note_on",channel=channel,note=int(pitch),
                                           velocity=velocity,time=0)))
        events.append((stop,0,mido.Message("note_off",channel=channel,note=int(pitch),
                                          velocity=0,time=0)))
        added+=1
    for sec in plan["sections"]:
        kind=sec["kind"]
        if kind not in ("intro","verse","hook","pre-hook","breakdown","bridge","outro"):
            continue
        for j in range(sec["bars"]):
            bar=sec["startBar"]+j
            phrase=j%8
            group=j//4
            # Four-bar answer: A1 / response / A2 / variation; every eight
            # bars have intentional pauses, accents and a resolved turnaround.
            degree=(seed//23+group*3+j//2)%7
            n1=scale_note(root,degree,scale,4)
            n2=scale_note(root,(degree+2+((seed//41)%3))%7,scale,4)
            if kind=="hook":
                if ident in WEAK_HOOK_IDS:
                    # Increase audible melodic distinction without eating the
                    # initial two beats in the rap verses.
                    insert(bar,1.5,3,n1,46+(j%3)*6,.26)
                    insert(bar,3.52,3,n2,49+(phrase%4)*4,.29)
                elif phrase in (1,3,5,7):
                    insert(bar,3.52,3,n2,44+(phrase%3)*5,.29)
                if phrase==7:
                    # Only final turnaround of each eight-bar group; hooks
                    # retain an A/B phrase rather than one fixed looping cell.
                    insert(bar,3.75,9,DRUM_ACCENTS[(seed//17+group)%len(DRUM_ACCENTS)],42,.10)
            elif kind=="verse":
                # Ghost-drum pickup every fourth bar; a phrase-level edit
                # instead of a copy-pasted eighth-note hat loop.
                if phrase in (3,7):
                    insert(bar,3.75,9,40,34+(j%5)*3,.12)
                if phrase==5 and ident not in MONO_REVIEW_IDS:
                    insert(bar,3.25,9,46,33,.11)
                # No new lead/counter melody before the second half of a bar.
                if phrase in (3,7) and ident not in WEAK_HOOK_IDS:
                    insert(bar,2.75,3,n1,33,.22)
            elif kind in ("bridge","breakdown"):
                if phrase in (1,5):
                    insert(bar,2.5,3,n1,33,.31)
            elif kind=="pre-hook" and phrase==sec["bars"]%8-1:
                insert(bar,3.5,9,40,39,.11)
    events.sort(key=lambda x:(x[0],x[1],x[2].channel if hasattr(x[2],"channel") else 99,
                               x[2].note if hasattr(x[2],"note") else 0))
    rebuilt=mido.MidiTrack()
    last=0
    for tick,_,message in events:
        if tick<last:raise RuntimeError("Non-monotone MIDI ticks")
        rebuilt.append(message.copy(time=tick-last))
        last=tick
    rebuilt.append(mido.MetaMessage("end_of_track",time=max(0,song_ticks-last)))
    mf.tracks[-1]=rebuilt
    mf.save(midi)
    return {"id":ident,"enhanced":True,"addedNotePairs":added,
            "newPrograms":{str(k):v for k,v in programs.items()},
            "sourceMidiEvents":len(events)}
