#!/usr/bin/env python3
"""AXEZENT original studio MIDI performance pass."""
from __future__ import annotations
import collections
import pathlib
import mido

TICKS_PER_BAR=1920
PITCH_PROFILES={
  "AXZ-189":"warm",
  "AXZ-049":"percussive",
  "AXZ-089":"sustained",
  "AXZ-037":"club",
}

def refine_midi(filename:pathlib.Path,beat:dict,plan:dict)->dict:
    ident=beat["id"]
    if ident not in PITCH_PROFILES:
        return {"processed":False,"notes":0,"tuningChanges":0,"articulations":0}
    mf=mido.MidiFile(filename)
    if len(mf.tracks)<3: raise RuntimeError("Missing song events")
    section_map=[(s["startBar"],s["endBar"],s["kind"]) for s in plan["sections"]]
    duration=plan["totalBars"]*TICKS_PER_BAR
    active=collections.defaultdict(collections.deque)
    notes=[]
    other=[]
    time=0
    for msg in mf.tracks[-1]:
        time+=msg.time
        if msg.type=="end_of_track":continue
        if msg.type=="note_on" and msg.velocity>0:
            active[(msg.channel,msg.note)].append((time,msg.velocity))
        elif msg.type=="note_off" or (msg.type=="note_on" and msg.velocity==0):
            key=(msg.channel,msg.note)
            if not active[key]:raise ValueError("Unmatched MIDI release")
            start,vel=active[key].popleft()
            if time<=start:raise ValueError("Invalid note length")
            notes.append([start,time,msg.channel,msg.note,vel])
        else:
            other.append((time,msg))
    if any(active.values()):raise ValueError("Unreleased MIDI note")
    source_count=len(notes)
    profile=PITCH_PROFILES[ident]
    kicks=collections.defaultdict(list)
    for on,off,ch,pitch,vel in notes:
        if ch==9 and pitch in (35,36):
            kicks[on//TICKS_PER_BAR].append(on)
    tuning_changes=0
    articulation_changes=0
    for note in notes:
        on,off,ch,pitch,velocity=note
        bar=on//TICKS_PER_BAR
        kind=None
        local=0
        for start,end,name in section_map:
            if start<=bar<end:
                kind=name;local=bar-start;break
        if kind is None:raise ValueError("Song event outside arrangement")
        tick_in_bar=on%TICKS_PER_BAR
        length=off-on
        new_pitch=pitch
        if ch==1 and kind in ("hook","verse"):
            if profile=="warm" and kind=="hook" and pitch>=76 and local%4 in (1,3):
                new_pitch=pitch-12
            elif profile=="percussive" and kind=="verse" and pitch<=67 and local%4==3:
                new_pitch=pitch+12
            elif profile=="sustained" and kind=="hook" and pitch<=71 and local%4 in (0,2):
                new_pitch=pitch+12
            elif profile=="club" and kind=="hook" and pitch<=69 and local%4==2:
                new_pitch=pitch+12
            if new_pitch<58 or new_pitch>90:new_pitch=pitch
            # Section-sensitive articulation, not a universal quantized loop.
            if kind=="hook":
                factor=1.48 if local%4 in (2,3) else (.80 if local%4==1 else 1.2)
            else:
                factor=.83 if local%4 in (0,2) else 1.27
            new_length=min(round(length*factor),TICKS_PER_BAR-tick_in_bar-8)
            new_length=max(20,new_length)
            if new_length!=length:
                note[1]=on+new_length
                articulation_changes+=1
        elif ch==3 and kind=="hook":
            factor=1.38 if local%4==3 else .87
            new_length=max(16,min(round(length*factor),TICKS_PER_BAR-tick_in_bar-8))
            if new_length!=length:
                note[1]=on+new_length
                articulation_changes+=1
        elif ch==2:
            # Keep the low-frequency attack aligned with the actual kick
            # when both notes already occupy the same deliberate pocket.
            nearest=min(kicks[bar],key=lambda k:abs(k-on),default=None)
            if nearest is not None and 4<abs(nearest-on)<=27:
                new_on=max(bar*TICKS_PER_BAR,nearest+2)
                delta=new_on-on
                if 0<=new_on%TICKS_PER_BAR<TICKS_PER_BAR-12:
                    note[0]=new_on
                    note[1]=off+delta
                    articulation_changes+=1
            if kind=="verse" and local%4==3:
                target=max(20,round((note[1]-note[0])*.76))
                if target<note[1]-note[0]:
                    note[1]=note[0]+target
                    articulation_changes+=1
        if new_pitch!=pitch:
            note[3]=new_pitch
            tuning_changes+=1
        if ch==1 and kind=="hook" and local%4==3:
            note[4]=min(115,velocity+5)
        elif ch==1 and kind=="verse" and local%4==0:
            note[4]=max(30,velocity-4)
    # Prevent same-pitch voices colliding when shifted by an octave or extended.
    notes.sort(key=lambda n:(n[0],n[2],n[3],n[1]))
    future=collections.defaultdict(list)
    for n in notes:future[(n[2],n[3])].append(n)
    for rows in future.values():
        for a,b in zip(rows,rows[1:]):
            if a[1]>=b[0]:
                a[1]=max(a[0]+1,b[0]-2)
    ordered=[]
    for on,off,ch,pitch,vel in notes:
        if not (0<=on<off<=duration):
            raise ValueError("Out-of-range MIDI note")
        if ch!=9 and (on//TICKS_PER_BAR)!=((off-1)//TICKS_PER_BAR):
            raise ValueError("Pitched note crosses chord boundary")
        ordered.append((on,1,mido.Message("note_on",note=pitch,velocity=vel,channel=ch,time=0)))
        ordered.append((off,0,mido.Message("note_off",note=pitch,velocity=0,channel=ch,time=0)))
    for on,msg in other:
        ordered.append((on,2,msg.copy(time=0)))
    ordered.sort(key=lambda row:(row[0],row[1],row[2].channel if hasattr(row[2],"channel") else 99))
    track=mido.MidiTrack()
    prev=0
    for tick,order,msg in ordered:
        track.append(msg.copy(time=tick-prev))
        prev=tick
    track.append(mido.MetaMessage("end_of_track",time=max(0,duration-prev)))
    mf.tracks[-1]=track
    mf.save(filename)
    check=mido.MidiFile(filename)
    if len(check.tracks[-1])!=2*source_count+1+len(other):
        raise ValueError("MIDI source events unexpectedly changed")
    return {"processed":True,"notes":source_count,
       "tuningChanges":tuning_changes,"articulations":articulation_changes}
