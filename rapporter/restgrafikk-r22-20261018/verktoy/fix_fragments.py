"""Re-export small source-only fragments with the actual actor palette.
These are not independently redrawn HD art and are never counted as such.
"""
from pathlib import Path
import json,sys,hashlib,shutil
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[4];P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'kode/pipeline'));from dighd import myk
plans=json.loads((P/'plans.json').read_text());colors=plans['source_palette'];large={c['name'] for b in plans['batches'] for c in b['cells']};O=P/'mod-erstatninger/costumes';O.mkdir(parents=True,exist_ok=True);records=[];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for f in sorted((R/'testing/source/costumes').glob('costume100_*_idx.png')):
 name=f.stem[:-4]
 if name in large:continue
 idx=Image.open(f);codes=np.array(idx);idx.putpalette(colors);a=np.array(idx.convert('RGBA'));a[codes==0]=0
 # The only opaque colours are the native source pixels; no invented art.
 src=Image.fromarray(a);pixels=int((a[:,:,3]>128).sum());assert pixels<=72,(name,pixels)
 assert (R/'hd-leveranse/costumes'/(name+'_hd.png')).exists()
 im=Image.fromarray(myk.from_original(a)['bilde']);hd=O/(name+'_hd.png');im.save(hd);idx.save(O/f.name);assert np.array_equal(codes,np.array(Image.open(O/f.name)))
 records.append(dict(name=name,pixels=pixels,method='existing myk.from_original source fragment export with AKPL->room32 palette0; not new AI artwork',file=hd.name,sha256=sha(hd),old_sha256=sha(R/'hd-leveranse/costumes'/hd.name),index=f.name,index_sha256=sha(O/f.name),old_index_sha256=sha(R/'hd-leveranse/costumes'/f.name),index_values_unchanged=True))
assert len(records)==91
manifest={str(f.relative_to(P/'mod-erstatninger')):sha(f) for f in sorted(O.glob('*.png'))};(P/'REPLACEMENTS.json').write_text(json.dumps(manifest,indent=2)+'\n');(P/'fragments.json').write_text(json.dumps(records,indent=2)+'\n');print(len(records),'small fragments, source palette corrected;182 declared replacement files')
