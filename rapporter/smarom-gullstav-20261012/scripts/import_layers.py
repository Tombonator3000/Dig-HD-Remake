from pathlib import Path
import json,shutil,sys,hashlib
from PIL import Image,ImageDraw
import numpy as np
Q=Path(__file__).resolve().parent;T=Q.parent;G=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk');R=G/'rapporter/smarom-gullstav-20261012';M=Path('/home/tombonator3000t/Skrivebord/TheDigHD-Linux-20261012-test/usr/share/the-dig-hd/mods/gpt');sys.path[:0]=[str(T/'code/pipeline'),str(T/'deps')];from dighd import gpt
plan=json.loads((R/'PLAN.json').read_text());records=json.loads((R/'GENERATED-SOURCES.json').read_text());entries=[];finished={};sources={};settings={'sigma':6,'strength':1};candidates={}
for d in plan['layer_jobs']:
 j=d['id'];rs=[r for r in records if r['job']==j];sel=[r for r in rs if r.get('selected')];r=sel[-1] if sel else rs[-1];candidates[j]=r;locked=np.load(Q/'evaluation'/f"{j}-forsok{r['attempt']}.npy");job=gpt._load_job(d)
 for p in d['objekter']:
  n=p['bilde'];src=Q/'extract/objects'/f'{n}.png';hd=gpt._cut(tuple(d['rom_storrelse']),[(tuple(d['region']),locked)],p['rekt'],src);base=f"obj{p['objekt']:03d}_01";idx=Q/'extract/objects'/f'{n}_idx.png';bidx=Q/'extract/objects'/f'{base}_idx.png'
  if base!=n:
   bh=finished.get(base)
   if bh is None and (M/'objects'/f'{base}.png').exists():bh=np.array(Image.open(M/'objects'/f'{base}.png').convert('RGB'))
   if bh is not None and bidx.exists():hd=gpt.match_state(hd,bh,idx,bidx)
  finished[n]=hd;dest=M/'objects'/f'{n}.png';di=M/'objects'/f'{n}_idx.png';backup=Q/'layers-before/objects';backup.mkdir(parents=True,exist_ok=True)
  for f in [dest,di]:
   if f.exists() and not (backup/f.name).exists():shutil.copy2(f,backup/f.name)
  gpt._with_alpha(hd,src).save(dest);shutil.copy2(idx,di);e=json.loads((Q/'evaluation'/f"{j}-forsok{r['attempt']}.json").read_text());entries.append({'job':j,'attempt':r['attempt'],'object':n,'room':d['rom'],'rect':p['rekt'],'auto_status':e['status'],'auto_comment':e['kommentar'],'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'idx_sha256':hashlib.sha256(di.read_bytes()).hexdigest(),'native_indices_and_alpha':True,'state_matching_base':base if base!=n else None})
# Evidence: original beside final runtime crop on a contrasting neutral background.
W=1200;H=200*len(entries);sheet=Image.new('RGB',(W,H),(40,40,45));draw=ImageDraw.Draw(sheet)
for i,e in enumerate(entries):
 n=e['object'];o=Image.open(Q/'extract/objects'/f'{n}.png').convert('RGBA');h=Image.open(M/'objects'/f'{n}.png').convert('RGBA');s=min(480/h.width,164/h.height);size=(max(1,round(h.width*s)),max(1,round(h.height*s)));o=o.resize(size,Image.Resampling.NEAREST);h=h.resize(size,Image.Resampling.LANCZOS);sheet.paste(o,(20,i*200+25),o);sheet.paste(h,(600,i*200+25),h);draw.text((20,i*200+5),n+' original | HD, '+e['job'],fill='white')
sheet.save(Q/'objects-review.png');(R/'IMPORT-LAG.json').write_text(json.dumps({'entries':entries,'count':len(entries),'pipeline':'dighd.gpt _cut, lock_colors sigma6 strength1, match_state, _with_alpha; only31 requested objects, no room images replaced','manual_review_pending':[j for j,r in candidates.items() if json.loads((Q/'evaluation'/f"{j}-forsok{r['attempt']}.json").read_text())['status']!='godkjent']},ensure_ascii=False,indent=2)+'\n');print('Imported',len(entries));print('Review',Q/'objects-review.png')
