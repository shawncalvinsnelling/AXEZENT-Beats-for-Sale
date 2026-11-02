#!/usr/bin/env python3
"""AXEZENT public preview renderer: deterministic original synthesized REVIEW mixes.
No samples, paid masters, AI-authorship claims or proprietary NODESS internals.
Uses measured ms timing, sectional dynamics, frequency-conscious stereo routing.
Not a substitute for producer listening/approval. Requires numpy + ffmpeg.
"""
import json, math, hashlib, argparse, os, subprocess, tempfile
from pathlib import Path
import numpy as np
SR=32000
TAU=2*math.pi
PITCH={'C':0,'C#':1,'DB':1,'D':2,'D#':3,'EB':3,'E':4,'F':5,'F#':6,'GB':6,
       'G':7,'G#':8,'AB':8,'A':9,'A#':10,'BB':10,'B':11}
SCALE=(0,2,3,5,7,8,10)
STYLES=('Southern half-time','Detroit bounce','New York drill','West Coast synth-funk',
        'Atlanta trap','Memphis dark','cinematic hip-hop','club bounce','soulful boom bap',
        'gospel synth','desert atmosphere','cold melodic')
def midi(root,degree,octave=4):
    return 12*(octave+1)+root+SCALE[degree%7]+12*(degree//7)
def freq(note):return 440*2**((note-69)/12)
def insert(out,w,time,pan=0,gain=1):
    st=round(time*SR);a=max(0,st);b=min(len(out),st+len(w))
    if b<=a:return
    q=(max(-1,min(1,pan))+1)*math.pi/4
    z=w[a-st:b-st]*gain
    out[a:b,0]+=z*math.cos(q)
    out[a:b,1]+=z*math.sin(q)
def note(n,dur,kind,seed):
    t=np.arange(max(1,round(SR*dur)),dtype=np.float32)/SR
    f=freq(n)
    if kind=='sub':
        ph=TAU*(f*t+4*(1-np.exp(-t*20))/20)
        y=np.sin(ph)+.16*np.sin(2*ph)
        e=np.minimum(1,t*110)*np.exp(-t/(.55+.13*(seed%4)))
    elif kind=='pad':
        y=np.sin(TAU*f*t)+.28*np.sin(TAU*f*1.004*t)+.19*np.sin(TAU*2*f*t)
        e=np.minimum(1,t*5)*np.minimum(1,(dur-t)*5)
    elif kind=='bell':
        y=np.sin(TAU*f*t)+.34*np.sin(TAU*2.02*f*t)+.15*np.sin(TAU*3.95*f*t)
        e=np.minimum(1,t*300)*np.exp(-t/(.25+.1*(seed%4)))
    elif kind=='keys':
        y=np.sin(TAU*f*t)+.23*np.sin(TAU*2*f*t+.3)+.12*np.sin(TAU*3*f*t+.9)
        e=np.minimum(1,t*150)*np.exp(-t/(.3+.11*(seed%4)))
    elif kind=='lead':
        vib=.04*np.sin(TAU*5*t)
        y=np.sin(TAU*f*t+vib)+.22*np.sin(TAU*2*f*t+vib)
        e=np.minimum(1,t*35)*np.minimum(1,(dur-t)*8)
    else:
        y=np.sin(TAU*f*t)+.27*np.sin(TAU*2*f*t)+.1*np.sin(TAU*3*f*t)
        e=np.minimum(1,t*100)*np.exp(-t/(.12+.05*(seed%3)))
    result=(y*e).astype(np.float32)
    fade=min(len(result)//8,round(SR*.01))
    if fade:result[-fade:]*=np.linspace(1,0,fade,dtype=np.float32)
    return result
def drums(rng,rank):
    t=np.arange(round(SR*.5),dtype=np.float32)/SR
    phase=TAU*((42+rank%5*3)*t+50*(1-np.exp(-t*40))/40)
    kick=(np.sin(phase)*np.exp(-t*13)+rng.normal(0,.065,len(t))*np.exp(-t*80))*.42
    t=np.arange(round(SR*.24),dtype=np.float32)/SR
    white=rng.normal(size=len(t)).astype(np.float32)
    noise=white-np.convolve(white,np.ones(9)/9,'same')
    snare=(noise*.14*np.exp(-t*29)+np.sin(TAU*170*t)*.08*np.exp(-t*22))
    t=np.arange(round(SR*.09),dtype=np.float32)/SR
    white=rng.normal(size=len(t)).astype(np.float32)
    hat=(white-np.convolve(white,np.ones(7)/7,'same'))*.055*np.exp(-t*60)
    t=np.arange(round(SR*.18),dtype=np.float32)/SR
    white=rng.normal(size=len(t)).astype(np.float32)
    clap=white*.044*np.exp(-t*21)
    return [a.astype(np.float32) for a in (kick,snare,hat,clap)]
def render(track,rank,outpath):
    seed=int.from_bytes(hashlib.sha256(track['id'].encode()).digest()[:8],'big') & 0xffffffff
    rng=np.random.default_rng(seed)
    bpm=int(track.get('bpm') or (80+rank%50))
    root=PITCH.get(str(track.get('key') or 'D minor').split()[0].upper(),2)
    beat=60/bpm;bar=4*beat;bars=48;length=bars*bar+1
    out=np.zeros((math.ceil(length*SR),2),dtype=np.float32)
    profile=(rank-1)%len(STYLES)
    progressions=((0,5,3,4),(0,3,5,4),(0,6,5,3),(0,4,3,5),(0,5,6,3))
    progression=progressions[(rank+seed)%len(progressions)]
    patterns=((0,2,4,6,4,2),(0,3,4,2,1,0),(0,4,2,5,3,1),(2,4,6,5,3,1))
    melody=patterns[(rank+seed)%len(patterns)]
    kit=drums(rng,rank)
    pan=.12+(seed%13)/100
    for bi in range(bars):
        section=('intro' if bi<4 else 'verse' if bi<20 else 'hook' if bi<28 else
                 'verse' if bi<40 else 'hook' if bi<46 else 'outro')
        t0=bi*bar;rootstep=progression[(bi//4)%4]
        hook=section=='hook'
        if bi>=2:
            beat_positions=({0,2.5} if profile in (0,5,10) else
                           {0,1.5,2.75} if profile in (1,7) else
                           {0,2,3.5} if profile in (2,8) else {0,2,2.75})
            if hook:beat_positions|={3.5}
            for j,k in enumerate(sorted(beat_positions)):
                t=t0+k*beat+(.0025*((j+seed)%4) if j else 0)
                insert(out,kit[0],t,gain=1 if hook else .8)
                insert(out,note(midi(root,rootstep+(7 if j%3==0 else 0),2),
                                min(1.3,beat*1.1),'sub',seed),t+.009,gain=.19 if hook else .15)
        for k in (1,3):
            insert(out,kit[1],t0+k*beat+.005,pan=(-.06 if k==1 else .06),gain=.73 if hook else .56)
            if hook or profile in (1,6,8):insert(out,kit[3],t0+k*beat+.002,gain=.63)
        n=16 if profile in (1,2,4,7) or hook else 8
        for h in range(n):
            if section=='intro' and h%3:continue
            sw=.035*beat if h%2 and profile in (1,8) else 0
            jit=float(rng.uniform(-.006,.006))
            vel=.4+.31*(h%4==0)+float(rng.uniform(-.05,.05))
            insert(out,kit[2],t0+h*(4/n)*beat+sw+jit,pan=(-.25 if h%2 else .18),gain=.7*vel)
        if section not in ('intro','outro') or bi%2==0:
            for j,step in enumerate((0,2,4)):
                insert(out,note(midi(root,rootstep+step,4),bar*.92,'pad',seed),
                       t0+.013*j,pan=(-pan,0,pan)[j],gain=.037 if hook else .026)
        if section in ('hook','verse'):
            for j in range(6 if hook else 3):
                step=melody[(j+(bi%4)*2)%6]
                nm=midi(root,rootstep+step,4+(int(hook and j==5)))
                kind=('bell','pluck','keys','lead')[profile%4] if not hook else ('bell','lead','pluck')[profile%3]
                pos=(j+(.5 if j%2 else 0))*bar/(7 if hook else 4)
                insert(out,note(nm,min(beat*1.5,bar*.46),kind,seed+j),
                       t0+pos+(.004 if j%2 else 0),pan=(-1)**j*pan,gain=.034 if hook else .025)
        if bi in (19,39):
            a=int((t0+3.7*beat)*SR);b=int((t0+4*beat)*SR)
            out[a:b]*=np.linspace(1,.3,b-a,dtype=np.float32)[:,None]
    # Audio-routing QA: centered bass by low-frequency summing, high-band crossfeed
    # at 2.5-5.3 ms, hook-only and low gain. Not neural or medical effects.
    smooth_window=round(SR/520)
    kernel=np.ones(smooth_window,dtype=np.float32)/smooth_window
    smooth=lambda a:np.convolve(a,kernel,'same').astype(np.float32)
    bass=(smooth(out[:,0])+smooth(out[:,1]))*.5
    for k in range(2):out[:,k]+=.8*(bass-smooth(out[:,k]))
    delta=round(SR*(.0025+.0004*(rank%8)))
    for first,last in ((20,28),(40,46)):
        a=int(first*bar*SR);b=min(len(out),int(last*bar*SR))
        if b>a+delta:
            l=out[a:b-delta,0].copy();r=out[a:b-delta,1].copy()
            out[a+delta:b,0]+=.034*(r-smooth(r))
            out[a+delta:b,1]+=.034*(l-smooth(l))
    # Producer-tone marker; streamable MP3 remains capturable by design.
    for sec in range(8,int(length),24):
        for j,n in enumerate((77,81,84)):
            insert(out,note(n,.14,'bell',seed),sec+j*.19,pan=(-.12,0,.12)[j],gain=.034)
    fade=round(SR*.45)
    out[:fade]*=np.linspace(0,1,fade,dtype=np.float32)[:,None]
    out[-fade:]*=np.linspace(1,0,fade,dtype=np.float32)[:,None]
    peak=float(np.max(np.abs(out)))
    if peak<.005:raise ValueError('silent audio')
    out=np.tanh(out*(.88/peak)*1.14)/1.14
    outpath.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(suffix='.f32')
    try:
        with os.fdopen(fd,'wb') as f:f.write(out.astype('<f4').tobytes())
        p=subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-f','f32le',
           '-ar',str(SR),'-ac','2','-i',tmp,'-c:a','libmp3lame','-b:a','96k',
           str(outpath)],capture_output=True,text=True)
        if p.returncode:raise RuntimeError(p.stderr[-900:])
    finally:os.unlink(tmp)
    return {'id':track['id'],'title':track['title'],'releaseRank':rank,'bpm':bpm,
            'lengthSeconds':round(bars*bar,2),'styleSketch':STYLES[profile],
            'highbandDelayMs':round(1000*delta/SR,2),
            'status':'reproducible synthetic PREVIEW DRAFT; not approved for $100 sale'}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--catalog',default='data/catalog.json')
    ap.add_argument('--out',default='previews')
    ap.add_argument('--start',type=int,default=1)
    ap.add_argument('--end',type=int,default=50)
    p=ap.parse_args()
    data=json.loads(Path(p.catalog).read_text('utf-8'))
    ranked=sorted((b for b in data if b.get('releaseRank')),key=lambda b:b['releaseRank'])
    assert len(ranked)==50
    manifest=[]
    for b in ranked:
        i=b['releaseRank']
        if not p.start<=i<=p.end:continue
        file=Path(p.out)/(b['id']+'-tagged.mp3')
        info=render(b,i,file)
        manifest.append(info)
        print(f"{i:02d}/50 {b['id']} {b['title']} {file.stat().st_size/1e6:.2f} MB",flush=True)
    if p.start==1 and p.end==50:
        (Path(p.out)/'PUBLIC_RENDER_REPORT.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':main()
