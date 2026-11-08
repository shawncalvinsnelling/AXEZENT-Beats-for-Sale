#!/usr/bin/env python3
"""All-50 original AXEZENT MIDI-grid audit; creates FL-style piano roll SVGs.
No copyrighted/reference-note transcription and no private audio exposure.
"""
from __future__ import annotations
import argparse
import json
import tempfile
from pathlib import Path
from xml.sax.saxutils import escape
from render_arranged_review_audio import Arrangement, TPQ, TICKS_BAR, parse_key

ROOT=Path(__file__).resolve().parents[1]
COLORS={0:"#85a0ed",1:"#4fd0d0",2:"#f4c15d",3:"#d3a2fd",9:"#eb8181"}

def events(a):
    active={};notes=[]
    for tick,_,m in sorted(a.events,key=lambda r:(r[0],r[1])):
        key=(m.channel,m.note)
        if m.type=="note_on" and m.velocity:
            active.setdefault(key,[]).append((tick,m.velocity))
        elif m.type=="note_off":
            if not active.get(key):raise AssertionError(f"Unpaired note off {key}")
            start,v=active[key].pop(0)
            if tick<=start:raise AssertionError("Nonpositive note duration")
            notes.append((start,tick-start,m.channel,m.note,v))
    if any(active.values()):raise AssertionError("Stuck note on event")
    return notes

def metrics(notes,section):
    first=section["startBar"]*TICKS_BAR
    last=section["endBar"]*TICKS_BAR
    values=[n for n in notes if first<=n[0]<last]
    return (round(sum(n[2]!=9 for n in values)/section["bars"],3),
            round(sum(n[2]==9 for n in values)/section["bars"],3))

def hook(notes,sec):
    base=sec["startBar"]*TICKS_BAR
    return tuple(sorted((t-base,d,ch,n) for t,d,ch,n,v in notes if
           ch in (0,1,2,3) and base<=t<base+2*TICKS_BAR))

def render(beat,notes,plan,target):
    sections={k:next(s for s in plan["sections"] if s["kind"]==k)
              for k in ("verse","hook")}
    pitches=[n[3] for n in notes if n[2]!=9 and
             any(s["startBar"]*TICKS_BAR<=n[0]<
                 (s["startBar"]+4)*TICKS_BAR for s in sections.values())]
    if not pitches:raise ValueError("No pitched notes")
    lo=max(24,min(pitches)-1);hi=min(103,max(pitches)+1)
    step=7.5;gridh=(hi-lo+1)*step
    width=1040;x0=135;panelh=gridh+110
    height=int(80+2*panelh+40)
    lines=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}">',
           f'<rect width="1200" height="{height}" fill="#101a2a"/>',
           f'<text x="20" y="27" fill="#ffffff" font-size="20" font-family="Arial" font-weight="bold">{escape(beat["title"])} — {escape(beat["city"])}</text>',
           f'<text x="20" y="49" fill="#b8c9d8" font-size="13" font-family="Arial">{beat["id"]} · {beat["bpm"]} BPM · {escape(beat["key"])} · original generated MIDI roll, not an FL Studio screenshot</text>']
    for index,kind in enumerate(("verse","hook")):
        sec=sections[kind];base=sec["startBar"]*TICKS_BAR
        end=min(sec["endBar"]*TICKS_BAR,base+4*TICKS_BAR)
        ybase=85+index*panelh
        lines.append(f'<text x="20" y="{ybase-8:.1f}" fill="#ffffff" font-size="16" font-family="Arial">{kind.upper()} — first four bars</text>')
        for n in range(lo,hi+1):
            y=ybase+(hi-n)*step
            if n%12 in (1,3,6,8,10):
                lines.append(f'<rect x="{x0}" y="{y:.1f}" width="{width}" height="{step}" fill="#253147"/>')
            elif n%12==0:
                lines.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x0+width}" y2="{y:.1f}" stroke="#5b6376" stroke-width=".7"/>')
                lines.append(f'<text x="25" y="{y+7:.1f}" fill="#d9e3ee" font-family="Arial" font-size="10">C{n//12-1}</text>')
        for i in range(65):
            x=x0+width*i/64
            if i%4==0:
                lines.append(f'<line x1="{x:.1f}" y1="{ybase}" x2="{x:.1f}" y2="{ybase+gridh+66:.1f}" stroke="#516176" stroke-width="{1.6 if i%16==0 else .45}"/>')
        for t,d,ch,n,vel in notes:
            if not base<=t<end:continue
            x=x0+width*(t-base)/(4*TICKS_BAR)
            w=max(3,width*min(d,end-t)/(4*TICKS_BAR))
            if ch==9:
                drumrow=(0 if n in (35,36) else 1 if n in (38,39,40) else
                         2 if n in (42,44,46,51,54,82) else 3)
                y=ybase+gridh+4+drumrow*15
                lines.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="10" rx="2" fill="{COLORS[ch]}" opacity=".8"/>')
            elif lo<=n<=hi:
                y=ybase+(hi-n)*step
                lines.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="7" rx="1.5" fill="{COLORS[ch]}"/>')
        for j,label in enumerate(("KICK","SNARE","HAT","OTHER")):
            lines.append(f'<text x="25" y="{ybase+gridh+13+j*15:.1f}" fill="#f3a6a6" font-size="10" font-family="Arial">{label}</text>')
    lines.append(f'<text x="20" y="{height-11}" fill="#c1cad5" font-size="11" font-family="Arial">Blue chords • Cyan lead • Yellow bass • Purple counter • Red drums. Precise note-on times and durations.</text>')
    lines.append("</svg>")
    target.write_text("\n".join(lines),encoding="utf-8")

def main():
    p=argparse.ArgumentParser();p.add_argument("--out",type=Path,required=True)
    dest=p.parse_args().out;svgs=dest/"piano-roll-svg";svgs.mkdir(parents=True,exist_ok=True)
    cat=json.loads((ROOT/"data/catalog.json").read_text("utf-8"))
    arrangements=json.loads((ROOT/"data/arrangements.json").read_text("utf-8"))
    beats=sorted((x for x in cat if isinstance(x.get("releaseRank"),int)
                 and 1<=x["releaseRank"]<=50),key=lambda x:x["releaseRank"])
    if len(beats)!=50:raise ValueError("50 song catalog required")
    allrows=[];fail=[];hooksigs=set();drumsigs=set()
    with tempfile.TemporaryDirectory() as tmp:
        for b in beats:
            plan=arrangements[b["id"]];a=Arrangement(b,plan)
            a.build_midi(Path(tmp)/"piano.mid")
            n=events(a);hooks=[s for s in plan["sections"] if s["kind"]=="hook"]
            verses=[s for s in plan["sections"] if s["kind"]=="verse"]
            if len(hooks)<2 or not verses:raise ValueError("Missing song form")
            identical=all(hook(n,s)==hook(n,hooks[0]) for s in hooks[1:])
            vd=metrics(n,verses[0]);hd=metrics(n,hooks[0])
            root,scale=parse_key(b["key"]);allowed={(root+i)%12 for i in scale}
            outofkey=sorted({e[3]%12 for e in n if e[2]!=9}-allowed)
            warnings=[]
            if not identical:warnings.append("Repeat hook harmonic/lead grid drift")
            if vd[0]>=hd[0]:warnings.append("Verse pitched attack density >= hook")
            if vd[0]>8.5:warnings.append("Excessive verse notes")
            if outofkey:warnings.append("Pitches outside declared diatonic key")
            hookbase=hooks[0]["startBar"]*TICKS_BAR
            drumsigs.add(tuple(sorted((t-hookbase,p) for t,d,ch,p,v in n if ch==9 and
                       hookbase<=t<hookbase+4*TICKS_BAR)))
            hooksigs.add(hook(n,hooks[0]))
            path=svgs/f'{b["releaseRank"]:02d}-{b["id"]}.svg'
            render(b,n,plan,path)
            row={"rank":b["releaseRank"],"id":b["id"],"title":b["title"],
                 "city":b["city"],"groove":a.groove,
                 "hookReturnsIdentically":identical,"versePitchedNotesPerBar":vd[0],
                 "hookPitchedNotesPerBar":hd[0],
                 "versePercussionNotesPerBar":vd[1],
                 "hookPercussionNotesPerBar":hd[1],"midiNotes":len(n),
                 "pitchClassErrors":outofkey,"flags":warnings,
                 "pianoRoll":str(path.relative_to(dest))}
            allrows.append(row)
            if warnings:fail.append(row)
            print("PIANO_ROLL_TRACK:",json.dumps(row),flush=True)
    summary={
        "tracks":len(allrows),"returningHooksIdentical":sum(x["hookReturnsIdentically"] for x in allrows),
        "uniqueHookPianoRolls":len(hooksigs),"distinctDrumGridPatterns":len(drumsigs),
        "meanVersePitchedPerBar":round(sum(x["versePitchedNotesPerBar"] for x in allrows)/50,2),
        "meanHookPitchedPerBar":round(sum(x["hookPitchedNotesPerBar"] for x in allrows)/50,2),
        "flagCount":len(fail),"originalReferenceAudioUsed":False,
        "scope":"exact generated MIDI, not screenshots of commercial FL Studio projects"
    }
    (dest/"AXEZENT_50_PIANO_ROLL_AUDIT.json").write_text(json.dumps(
        {"summary":summary,"tracks":allrows},indent=2)+"\n",encoding="utf-8")
    print("PIANO_ROLL_SUMMARY:",json.dumps(summary),flush=True)
    if fail:raise ValueError(f"{len(fail)} piano-roll arrangement failures")
    print("PASS: 50 original MIDI grids and 50 piano-roll SVGs validated")

if __name__=="__main__":main()
