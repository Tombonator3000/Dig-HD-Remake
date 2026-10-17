import os
"""Reuse exact original RGBA drawings after checking identity and painted references.
The 11 costume171 human matches are excluded: their available HD reference has
clothes that do not match the approved character pilot.
"""
from pathlib import Path
import json,hashlib,shutil,os
import numpy as np
from PIL import Image
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));P=R/'grafikk/rapporter/restgrafikk-r19-20261016';S=R/'testing/source/costumes';B=R/'hd-leveranse/costumes';C=R/'kandidat-r19/costumes';O=P/'mod-tillegg/costumes';rows=json.loads((P/'identical-source-candidates.json').read_text());done=[];rejected=[]
for row in rows:
 target=row['target'];source=row['source_candidates'][0]
 if target.startswith('costume171_'):
  rejected.append(row|dict(reason='Available native reference has brown shirt and beige trousers, not the approved pilot clothing; needs new character art.'));continue
 a=np.array(Image.open(S/(target+'_idx.png')).convert('RGBA'));b=np.array(Image.open(S/(source+'_idx.png')).convert('RGBA'));a[a[:,:,3]==0]=0;b[b[:,:,3]==0]=0;assert np.array_equal(a,b),(source,target)
 src=C/(source+'_hd.png');dest=target+'_hd.png';assert not (B/dest).exists();shutil.copy2(src,O/dest);tmp=C/(dest+'.new');shutil.copy2(src,tmp);os.replace(tmp,C/dest)
 idx=target+'_idx.png'
 if not (B/idx).exists():
  shutil.copy2(S/idx,O/idx);tmp=C/(idx+'.new');shutil.copy2(S/idx,tmp);os.replace(tmp,C/idx)
 done.append(row|dict(source=source,method='byte-identical original RGBA and dimensions; HD image reused unchanged after contact-sheet identity review',source_hd_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),sha256=hashlib.sha256((O/dest).read_bytes()).hexdigest()))
(P/'identical-source-registration.json').write_text(json.dumps(dict(imported=done,rejected=rejected),indent=2)+'\n');print(len(done),'exact HD reuses;',len(rejected),'wrong-clothing references rejected')
