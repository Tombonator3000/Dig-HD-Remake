import os
from pathlib import Path
import numpy as np,json,hashlib
from PIL import Image
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));P=R/'grafikk/rapporter/restgrafikk-r19-20261016';S=R/'testing/source/costumes';M=R/'hd-leveranse/costumes';O=P/'mod-tillegg/costumes'
inventory=json.loads((P/'dekning-for.json').read_text());rows=[]
for cid,base in [(22,3),(23,2)]:
 for c in [x for x in inventory['cells'] if x['costume']==cid]:
  target=c['name'];source=target.replace(f'{cid:03d}',f'{base:03d}',1)
  a=Image.open(S/(source+'_idx.png'));b=Image.open(S/(target+'_idx.png'));aa=np.asarray(a);bb=np.asarray(b)
  assert a.size==b.size
  # Every source code maps to exactly one target code, preserving all shapes.
  pairs=set(zip(aa.ravel(),bb.ravel()));assert len(pairs)==len(np.unique(aa)),target
  pa=np.array(a.getpalette()).reshape(256,3);pb=np.array(b.getpalette()).reshape(256,3)
  rgbpairs={tuple(pa[k]):pb[v] for k,v in pairs if k!=a.info.get('transparency',0)}
  colors=np.array(list(rgbpairs)).astype(float);newcolors=np.array(list(rgbpairs.values())).astype(float)
  src=M/(source+'_hd.png');assert src.exists(),source
  art=np.array(Image.open(src).convert('RGBA'));flat=art[:,:,:3].reshape(-1,3).astype(float)
  # Preserve painted detail, transferring only the original palette differences.
  nearest=((flat[:,None,:]-colors[None,:,:])**2).sum(2).argmin(1)
  delta=(newcolors-colors)[nearest];art[:,:,:3]=np.clip(flat+delta,0,255).reshape(art.shape[:2]+(3,)).astype('uint8')
  dest=O/(target+'_hd.png');Image.fromarray(art).save(dest)
  rows.append(dict(target=target,source=source,method='identical source pixel segmentation, original palette delta; original approved HD geometry and alpha unchanged',source_hd_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),target_hd_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),approved_model='hovedark/'+('brink.png' if cid==22 else 'maggie.png')))
(P/'tunnel-gjenbruk.json').write_text(json.dumps(rows,indent=2)+'\n');print(len(rows),'tunnel cells reused with exact original structure')
