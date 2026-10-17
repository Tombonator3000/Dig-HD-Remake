import os
"""Find exact same RGBA source drawings that already have HD, without importing candidates."""
from pathlib import Path
import numpy as np,json,hashlib,collections
from PIL import Image
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));P=R/'grafikk/rapporter/restgrafikk-r19-20261016';S=R/'testing/source/costumes';C=R/'kandidat-r19/costumes';missing=json.loads((P/'dekning-arbeid.json').read_text());sources=collections.defaultdict(list)
def key(f):
 im=Image.open(f).convert('RGBA');a=np.array(im);a[a[:,:,3]==0]=0
 if (a[:,:,3]>128).sum()<40:return None
 return hashlib.sha256(np.array(a.shape,dtype='int32').tobytes()+a.tobytes()).hexdigest()
for f in S.glob('*_idx.png'):
 name=f.stem.removesuffix('_idx');hd=C/(name+'_hd.png')
 if not hd.exists():continue
 k=key(f)
 if k:sources[k].append(name)
rows=[]
for row in missing['cells']:
 f=S/(row['name']+'_idx.png')
 if not f.exists():continue
 k=key(f)
 if k in sources:rows.append(dict(target=row['name'],source_candidates=sources[k],source_sha256=k,pixels=row['pixels']))
(P/'identical-source-candidates.json').write_text(json.dumps(rows,indent=2)+'\n');print(len(rows),'exact source matches; not yet imported');print(collections.Counter((v['target'][7:10],v['source_candidates'][0][7:10]) for v in rows))
