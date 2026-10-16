import os
from pathlib import Path
import sys,json,shutil,os,hashlib
from PIL import Image
import numpy as np
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));sys.path.insert(0,str(R/'kode/pipeline'))
from dighd import gamedata as g,myk
P=R/'grafikk/rapporter/restgrafikk-r19-20261016';S=R/'testing/source/costumes';O=P/'mod-tillegg/costumes';M=R/'kandidat-r19/costumes';B=R/'hd-leveranse/costumes'
G=Path('/home/tom/Documents/Codex/2026-10-16-the-dig-hd-remake-sp-rsm/testing/linux-release/AppDir/usr/share/the-dig-hd/game');d=(G/'DIG.LA1').read_bytes();ix=g.read_index(G/'DIG.LA0');rooms=g.read_rooms(G/'DIG.LA1');rn,off=ix.costume_dir[103];p=rooms[rn].offset+off;bl={t:d[o+8:o+n] for t,o,n in g.children(d,p+8,p+g.be32(d,p+4))};pal=rooms[32].palettes[0];colors=[]
for i in bl[b'AKPL']:colors+=list(pal[i*3:i*3+3])
colors+=[0]*(768-len(colors));large={v['name'] for v in json.loads((P/'boston103-plan.json').read_text())};records=[]
for f in sorted(S.glob('costume103_*_idx.png')):
 im=Image.open(f);old=np.array(im);im.putpalette(colors);im.save(f);im.convert('RGBA').save(f.with_name(f.name.replace('_idx','')));assert np.array_equal(old,np.array(Image.open(f)))
 hd=f.name.replace('_idx','_hd')
 if not (O/hd).exists():continue
 if f.stem.replace('_idx','') not in large:
  Image.fromarray(myk.from_original(np.array(im.convert('RGBA')))['bilde']).save(O/hd)
  temp=M/(hd+'.new');shutil.copy2(O/hd,temp);os.replace(temp,M/hd)
 if not (B/f.name).exists():
  shutil.copy2(f,O/f.name);temp=M/(f.name+'.new');shutil.copy2(f,temp);os.replace(temp,M/f.name)
 records.append(dict(file=hd,palette='costume103 AKPL mapped through original room32 palette0',source_fragment=f.stem.replace('_idx','') not in large,sha256=hashlib.sha256((O/hd).read_bytes()).hexdigest()))
(P/'boston103-palette-check.json').write_text(json.dumps(records,indent=2)+'\n');print(len(records),'new Boston phases checked; physical indices unchanged')
