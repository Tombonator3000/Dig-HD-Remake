import os
"""Check the original MajMin decoder against protected source job images."""
from pathlib import Path
import json,numpy as np
from PIL import Image
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));S=R/'testing/source/costumes';P=R/'grafikk/rapporter/restgrafikk-r19-20261016';seen=set();rows=[]
for folder in sorted((R/'grafikk/jobber').glob('fig*')):
 meta=json.loads((folder/'jobb.json').read_text())
 if meta.get('kostyme') not in [95,118,266,267]:continue
 ref=Image.open(folder/'original_1x.png').convert('RGB')
 for c in meta['ruter']:
  n=c['bilde']
  if n in seen:continue
  seen.add(n);x,y,w,h=c['rekt'];orig=np.array(ref.crop((x,y,x+w,y+h)));im=Image.open(S/(n+'_idx.png'));raw=np.array(im);rgba=np.array(im.convert('RGBA'));assert raw.shape==(h,w),(n,raw.shape,(h,w))
  mark=(orig[:,:,0]>180)&(orig[:,:,2]>150)&(orig[:,:,1]<100);valid=(raw!=255)&~mark;mis=np.any(orig!=rgba[:,:,:3],axis=2)&valid;nonbg=np.any(orig!=np.array(meta['bakgrunn']),axis=2)&~mark;mask_mis=int(((raw!=255)!=nonbg)[~mark].sum())
  rows.append(dict(name=n,pixels_checked=int(valid.sum()),rgb_mismatch=int(mis.sum()),mask_mismatch=mask_mis))
(P/'codec16-job-reference-check.json').write_text(json.dumps(rows,indent=2)+'\n')
assert len(rows)==872 and all(not v['rgb_mismatch'] and not v['mask_mismatch'] for v in rows)
print('872 original source cells: exact RGB and coverage match')
