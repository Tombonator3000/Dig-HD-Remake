"""Smooth existing tiny source sparks, preserving their original codes and timing."""
from pathlib import Path
from PIL import Image
import numpy as np,json,shutil,os
P=Path('grafikk/rapporter/spillfeil-r18-20261016');O=P/'mod-overrides/costumes';M=Path('kandidat-r18/costumes');records=[]
for f in sorted(Path('testing/source/costumes').glob('costume150_*_idx.png')):
 src=Image.open(f);w,h=src.size
 im=src.convert('RGBA');pad=Image.new('RGBA',(w+16,h+16));pad.alpha_composite(im,(8,8));art=pad.resize(((w+16)*4,(h+16)*4),Image.Resampling.BICUBIC)
 for name,q in [(f.name,src),(f.name.replace('_idx','_hd'),art)]:
  q.save(O/name);tmp=M/(name+'.new');shutil.copy2(O/name,tmp);os.replace(tmp,M/name)
 records.append({'source':f.name,'method':'bicubic premultiplied alpha on padded original; no new motif'})
(P/'SPARK-REGISTRATION.json').write_text(json.dumps(records,indent=2));print(len(records),'original effect cells smoothed')
