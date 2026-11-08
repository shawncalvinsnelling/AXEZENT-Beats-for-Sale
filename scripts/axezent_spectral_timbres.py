#!/usr/bin/env python3
"""Independent mathematically synthesized AXEZENT instrument timbres.

Original additive/FM pluck and harmonic spectra, using no third-party samples.
The layer plays only at curated phrase points, mostly intros/hooks/bridges.
This is an experimental mix component, NOT clinically proven to cause emotions.
"""
from __future__ import annotations
import hashlib
import math
import wave
from pathlib import Path
from scripts.render_arranged_review_audio import parse_key,scale_note

def synthesize(beat:dict,plan:dict,path:Path,rate:int=44100)->dict:
    import numpy as np
    ident=beat["id"]
    seed=int.from_bytes(hashlib.sha256((ident+"|AZ-SPECTRAL-V1").encode()).digest()[:8],"big")
    rng=np.random.default_rng(seed)
    root,scale=parse_key(beat["key"])
    seconds=float(plan["durationSeconds"])
    length=round(seconds*rate)
    if length<=0 or length>rate*480:
        raise ValueError("Unexpected song length "+ident)
    # All harmonics and musical notes remain linked to this track's declared
    # key. Diverse relative ratios are more useful than a 'magic 432Hz'.
    mode=seed%6
    detune=(-4+(seed%9)) / 1200
    base_tone=(0.92,1.0,1.08,1.16)[seed%4]
    events=[]
    for sec in plan["sections"]:
        kind=sec["kind"]
        if kind not in ("intro","hook","bridge","breakdown","pre-hook"):
            continue
        for bar_index in range(sec["bars"]):
            # Sparse *nonrepeated* variations: a different chord degree every
            # four bars, an answering overtone, and a 7/8-bar resolution.
            block=bar_index//4
            degrees=(seed//13+block*2+sec["startBar"])%7
            for j,pos in enumerate(((1.5,3.48) if kind=="hook" else (2.5,))):
                if kind=="hook" and (bar_index%4==0 and j==1): continue
                if kind!="hook" and bar_index%2==1: continue
                note=scale_note(root,(degrees+(j*2)+(bar_index%3))%7,scale,
                      4 if mode in (0,2,5) else 5)
                freq=440*2**((note-69)/12 + detune)
                start=(sec["startBar"]+bar_index)*240/beat["bpm"]+pos*60/beat["bpm"]
                if start>seconds-.6: continue
                duration_scale=(.43,.78,.58,1.05,.34,.68)[seed%6]
                dur=(duration_scale if kind=="hook" else 1.15*duration_scale)
                dur=min(dur,max(.09,(4-pos)*60/beat["bpm"]-.015))
                events.append((max(0,round(start*rate)),round(dur*rate),freq,j))
    path.parent.mkdir(parents=True,exist_ok=True)
    with wave.open(str(path),"wb") as wf:
        wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(rate)
        for pos in range(0,length,rate):
            block=min(rate,length-pos)
            left=np.zeros(block,dtype=np.float64)
            right=np.zeros(block,dtype=np.float64)
            for onset,nframes,freq,phrase in events:
                offset=max(0,onset-pos)
                stop=min(block,onset+nframes-pos)
                if offset>=stop:continue
                age=(np.arange(pos+offset,pos+stop,dtype=np.float64)-onset)/rate
                # FM index and partial ratios vary by track, while chorus
                # width is always phase-safe (no inverse-phase widening).
                modratio=(1.8,2.1,2.6,3.15,4.0,5.2)[mode]
                modindex=(.08,.2,.3,.4,.55,.7)[mode]
                phase=2*np.pi*freq*age+modindex*np.sin(2*np.pi*freq*age/modratio)
                if mode in (0,3):
                    signal=np.sin(phase)+.32*np.sin(2*phase)+.13*np.sin(3*phase)
                elif mode in (1,4):
                    signal=np.sin(phase)+.28*np.sin(2.02*phase)+.19*np.sin(4.03*phase)
                else:
                    signal=np.sin(phase)+.45*np.sin(1.5*phase)+.11*np.sin(5.1*phase)
                decay=(2.4,5.5,3.7,1.9,8.0,3.0)[mode]
                envelope=np.minimum(1,age/.012)*np.exp(-age*decay)
                envelope*=np.minimum(1,np.maximum(0,(nframes/rate-age))/.08)
                base=.11*base_tone*signal*envelope
                width=.05 if phrase%2 else -.05
                left[offset:stop]+=base*(1-width)
                right[offset:stop]+=base*(1+width)
            stereo=np.column_stack([left,right])
            # Sum of layer voices is bounded independently from the base mix.
            stereo=np.clip(stereo,-.8,.8)
            wf.writeframes((stereo*32767).astype("<i2").tobytes())
    return {"id":ident,"source":"original synthesized harmonic/FM notes, no external audio samples",
            "timbreAlgorithm":mode,"synthEvents":len(events),"sampleRateHz":rate,
            "durationSeconds":round(seconds,3)}
