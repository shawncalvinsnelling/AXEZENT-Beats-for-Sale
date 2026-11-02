#!/usr/bin/env python3
"""Only activate audio previews after the named, low-bitrate file is actually in the repo.
Never unlock purchase or WAV download rights here.
"""
from pathlib import Path
import json, subprocess
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'data/catalog.json'
data=json.loads(p.read_text())
changed=0
for b in data:
    if not isinstance(b.get('releaseRank'),int) or not 1<=b['releaseRank']<=50:continue
    path=ROOT/'previews'/f'{b["id"]}-tagged.mp3'
    if path.is_file():
        if path.stat().st_size>7_500_000 or path.stat().st_size<100_000:
            raise SystemExit(f'Unsafe preview size: {path}')
        r=subprocess.run(['ffprobe','-v','error','-show_entries',
         'stream=codec_name,bit_rate','-show_entries','format=duration',
         '-of','json',str(path)],text=True,capture_output=True)
        if r.returncode:raise SystemExit(f'Invalid audio: {path}: {r.stderr}')
        meta=json.loads(r.stdout)
        s=meta['streams'][0]
        if s.get('codec_name')!='mp3' or int(s.get('bit_rate',0))>128000 or float(meta['format']['duration'])<60:
            raise SystemExit(f'Preview must be at least 60s and max 128kbps MP3: {path}')
        new='previews/'+path.name
        if b['status']!='preview_ready' or b['previewUrl']!=new:changed+=1
        b['status']='preview_ready'
        b['previewUrl']=new
    else:
        if b['status']!='mix_review' or b['previewUrl'] is not None:changed+=1
        b['status']='mix_review'
        b['previewUrl']=None
    b['buyEnabled']=False
    b['downloadEnabled']=False
if changed:p.write_text(json.dumps(data,indent=2)+'\n')
print(f'{changed} preview records synchronized. Total available: {sum(x["status"]=="preview_ready" for x in data)}')
