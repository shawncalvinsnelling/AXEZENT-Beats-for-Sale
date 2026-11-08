#!/usr/bin/env python3
"""Preserve existing AXEZENT MP3s and encode full-length compact streams.
The source MP3s are preserved byte-for-byte. No new instruments or composition edits are claimed.
"""
from __future__ import annotations
import argparse,concurrent.futures,hashlib,json,subprocess,time,urllib.request,shutil
from pathlib import Path
from urllib.parse import urljoin

BASE='https://shawncalvinsnelling.github.io/AXEZENT-Beats-for-Sale/'
TONE_CORRECTIONS={
 'AXZ-097':['equalizer=f=4900:width_type=o:width=0.8:g=-0.8'],
 'AXZ-142':['equalizer=f=48:width_type=o:width=1:g=-0.5'],
 'AXZ-020':['equalizer=f=96:width_type=o:width=1:g=-0.5'],
}
WIDTH_CORRECTIONS={
 'AXZ-061':0.90,
 'AXZ-019':0.93,
 'AXZ-038':0.94,
 'AXZ-017':0.95,
 'AXZ-018':0.95,
}

def command(args):
 p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 if p.returncode:
  raise RuntimeError('Audio operation failed '+str(args[:3])+': '+p.stderr[-600:])
 return p.stdout

def download(url,dest):
 error=None
 for attempt in range(4):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'AXEZENT-Source-Preservation/1.0'}),timeout=50) as response,open(dest,'wb') as out:
    if response.status!=200:
     raise RuntimeError('Unexpected HTTP status '+str(response.status))
    count=0
    while True:
     data=response.read(262144)
     if not data:break
     count+=len(data)
     if count>12000000:raise RuntimeError('Unexpected oversized MP3')
     out.write(data)
   if not 150000<dest.stat().st_size<12000000:
    raise RuntimeError('Unexpected MP3 size')
   return
  except Exception as exc:
   error=exc
   dest.unlink(missing_ok=True)
   time.sleep(3*(attempt+1))
 raise RuntimeError('Failed to preserve '+url+': '+str(error))

def one(beat,source_root,public_manifest,output):
 ident=beat['id']
 mp3=ident+'-review.mp3'
 directory=output/'review-audio'
 original=directory/mp3
 if source_root:
  source=source_root/mp3
  if not source.is_file():raise ValueError('Local source missing '+str(source))
  shutil.copyfile(source,original)
 else:
  expected='./review-audio/'+mp3
  if public_manifest.get(ident)!=expected:
   raise ValueError('Missing authentic live MP3 for '+ident)
  download(urljoin(BASE,expected),original)
 if not 150000<original.stat().st_size<12000000:
  raise ValueError('Source audio invalid '+ident)
 probe=json.loads(command(['ffprobe','-v','error','-show_entries',
   'format=duration:stream=codec_name,channels,sample_rate','-of','json',str(original)]))
 if not probe.get('streams') or probe['streams'][0]['codec_name']!='mp3' or probe['streams'][0]['channels']!=2:
  raise ValueError('Invalid source stereo MP3 '+ident)
 duration=float(probe['format']['duration'])
 if not 55<duration<480:raise ValueError('Not a full-length track '+ident)
 filters=TONE_CORRECTIONS.get(ident,[]).copy()
 if ident in WIDTH_CORRECTIONS:
  filters.append('stereotools=mlev=1:slev='+str(WIDTH_CORRECTIONS[ident]))
 compact=directory/(ident+'-listen.m4a')
 command(['ffmpeg','-hide_banner','-nostdin','-v','error','-y','-threads','1',
  '-i',str(original),'-vn','-af',','.join(filters) if filters else 'anull',
  '-c:a','aac','-b:a','96k','-ar','44100','-ac','2','-movflags','+faststart',
  '-map_metadata','-1','-metadata','artist=AXEZENT',
  '-metadata','title='+beat['title'],str(compact)])
 check=json.loads(command(['ffprobe','-v','error','-show_entries',
  'format=duration:stream=codec_name,channels','-of','json',str(compact)]))
 if check['streams'][0]['codec_name']!='aac' or check['streams'][0]['channels']!=2:
  raise ValueError('Invalid compact AAC '+ident)
 discrepancy=abs(float(check['format']['duration'])-duration)
 if discrepancy>.18 or compact.stat().st_size<250000:
  raise ValueError('Compact stream length or duration mismatch '+ident)
 return {'releaseRank':beat['releaseRank'],'id':ident,'sourceBytes':original.stat().st_size,
  'compactBytes':compact.stat().st_size,'duration':round(duration,3),
  'durationDeltaSeconds':round(discrepancy,3),
  'sourceSHA256':hashlib.sha256(original.read_bytes()).hexdigest(),
  'compactSHA256':hashlib.sha256(compact.read_bytes()).hexdigest(),
  'auditionTonalReviewApplied':bool(filters),
  'disclosure':'AAC from MP3 origin; not lossless'}

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('--catalog',type=Path,required=True)
 parser.add_argument('--out',type=Path,required=True)
 parser.add_argument('--source-dir',type=Path)
 parser.add_argument('--qa-report',type=Path)
 args=parser.parse_args()
 catalog=json.loads(args.catalog.read_text('utf8'))
 songs=sorted((b for b in catalog if isinstance(b.get('releaseRank'),int) and
  1<=b['releaseRank']<=100),key=lambda b:b['releaseRank'])
 if len(songs)!=100 or len({b['id'] for b in songs})!=100:
  raise ValueError('Exactly 100 distinct ranked songs required')
 manifest={}
 if args.source_dir is None:
  with urllib.request.urlopen(urljoin(BASE,'data/public-preview-manifest.json'),timeout=35) as response:
   manifest=json.load(response)
  if len(manifest)!=100:
   raise ValueError('100 complete published sources required, never synthesize substitutes')
 args.out.joinpath('review-audio').mkdir(parents=True,exist_ok=True)
 rows=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  for row in pool.map(lambda b:one(b,args.source_dir,manifest,args.out),songs):
   rows.append(row)
   if len(rows)%10==0:print('PRESERVED '+str(len(rows))+'/100 full songs',flush=True)
 if len({r['sourceSHA256'] for r in rows})!=100 or len({r['compactSHA256'] for r in rows})!=100:
  raise ValueError('Duplicate audio, aborting release')
 if len(list((args.out/'review-audio').glob('*.mp3')))!=100 or len(list((args.out/'review-audio').glob('*.m4a')))!=100:
  raise ValueError('Missing audio, aborting release')
 report={'songs':100,'distinctSourceFingerprints':100,'originalMP3FilesUnmodified':True,
  'totalOriginalMB':round(sum(r['sourceBytes'] for r in rows)/1e6,1),
  'totalCompactMB':round(sum(r['compactBytes'] for r in rows)/1e6,1),
  'maxDurationDeltaSeconds':max(r['durationDeltaSeconds'] for r in rows),
  'tracks':rows,
  'disclosure':'96kbps AAC full-song auditions from existing MP3 originals. Human listening and independent instrument editing remain unverified.'}
 if args.qa_report:
  args.qa_report.parent.mkdir(parents=True,exist_ok=True)
  args.qa_report.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
 print('PASS: 100 full-length MP3 preserved, 100 compact M4A; total AAC MB',report['totalCompactMB'])

if __name__=='__main__':
 main()
