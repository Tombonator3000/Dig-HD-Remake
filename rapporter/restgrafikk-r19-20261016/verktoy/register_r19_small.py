import os
"""Complete tiny source fragments with the existing myk SMALL fallback.
This is technical resampling, not newly painted HD artwork. Both inventory
and decoded alpha must have fewer than 40 visible nontechnical pixels.
Published index mismatches are excluded rather than overwritten.
"""
from pathlib import Path
import sys,json,hashlib,shutil,os
import numpy as np
from PIL import Image
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));sys.path.insert(0,str(R/'kode/pipeline'))
from dighd import myk
P=R/'grafikk/rapporter/restgrafikk-r19-20261016';S=R/'testing/source/costumes';B=R/'hd-leveranse/costumes';O=P/'mod-tillegg/costumes';M=R/'kandidat-r19/costumes'
prior=P/'small-fragment-registration.json';rows=json.loads(prior.read_text())['new_fragments'] if prior.exists() else [];skipped=[]
for c in json.loads((P/'dekning-arbeid.json').read_text())['cells']:
 if not 0<c['pixels']<40:continue
 name=c['name'];hd=name+'_hd.png';idx=name+'_idx.png';f=S/idx
 if (M/hd).exists() or (M/(name+'.png')).exists():continue
 if not f.exists():skipped.append(dict(file=name,reason='missing decoded source'));continue
 im=Image.open(f);src=np.array(im.convert('RGBA'));mask,_=myk.measure_mask(src);area=int(mask.sum())
 if not 0<area<40:skipped.append(dict(file=name,reason='decoded extent not a tiny visible fragment',pixels=area));continue
 old=B/idx
 if old.exists():
  if not np.array_equal(np.array(Image.open(old)),np.array(im)):skipped.append(dict(file=name,reason='published index differs from decoded source'));continue
  src=np.array(Image.open(old).convert('RGBA'));provenance='published index image with verified identical pixel indices'
 else:provenance='decoded original source index image'
 result=myk.from_original(src)['bilde'];Image.fromarray(result).save(O/hd)
 for source,dest in [(O/hd,hd),(f,idx)]:
  if (B/dest).exists():continue
  if source!=O/hd:shutil.copy2(source,O/dest)
  tmp=M/(dest+'.new');shutil.copy2(source,tmp);os.replace(tmp,M/dest)
 rows.append(dict(file=hd,source=idx,pixels=area,inventory_pixels=c['pixels'],method='existing dighd.myk SMALL fallback, premultiplied Lanczos resampling with technical magenta removed',palette_source=provenance,sha256=hashlib.sha256((O/hd).read_bytes()).hexdigest()))
(P/'small-fragment-registration.json').write_text(json.dumps(dict(new_fragments=rows,skipped=skipped),indent=2)+'\n');print(len(rows),'technical tiny fragments;',len(skipped),'excluded')
