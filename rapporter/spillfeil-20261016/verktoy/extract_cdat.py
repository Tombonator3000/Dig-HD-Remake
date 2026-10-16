import os
from pathlib import Path
import sys,struct,json
import numpy as np
from PIL import Image
R=Path(os.environ.get("DIGHD_WORKSPACE",Path.cwd()));sys.path.insert(0,str(R/'kode/pipeline'))
from dighd import gamedata as g
from dighd.export import costume_palette,read_costume_colours
G=Path('/home/tom/Documents/Codex/2026-10-16-the-dig-hd-remake-sp-rsm/testing/linux-release/AppDir/usr/share/the-dig-hd/game');d=(G/'DIG.LA1').read_bytes();ix=g.read_index(G/'DIG.LA0');rooms=g.read_rooms(G/'DIG.LA1');O=R/'testing/source/costumes';O.mkdir(parents=True,exist_ok=True)
for cid in [58,115]:
 rn,ofs=ix.costume_dir[cid];p=rooms[rn].offset+ofs;b={t:d[o+8:o+s] for t,o,s in g.children(d,p+8,p+g.be32(d,p+4))};arrays=[]
 assert g.le16(b[b'AKHD'],8)==5
 for j in range(len(b[b'AKOF'])//6):
  do,co=struct.unpack_from('<IH',b[b'AKOF'],j*6);w,h=struct.unpack_from('<HH',b[b'AKCI'],co);raw=b[b'AKCD'];q=do;pixels=[]
  for y in range(h):
   n=struct.unpack_from('<H',raw,q)[0];k=q+2;line=[]
   while len(line)<w:
    code=raw[k];k+=1;count=min((code>>1)+1,w-len(line))
    if code&1:line.extend([raw[k]]*count);k+=1
    else:line.extend(raw[k:k+count]);k+=count
   pixels.extend(line);q+=n+2
  arrays.append((np.array(pixels,dtype=np.uint8).reshape(h,w),255))
 pal,how=costume_palette(5,b.get(b'AKPL',b''),b.get(b'RGBS',b''),rn,rooms,arrays,read_costume_colours(R/'kode/docs/kostymefarger.csv').get(cid))
 for j,(a,t) in enumerate(arrays):
  im=Image.fromarray(a,'P');im.putpalette(pal);im.info['transparency']=255;im.save(O/f'costume{cid:03d}_{j:03d}_idx.png');im.convert('RGBA').save(O/f'costume{cid:03d}_{j:03d}.png')
  old=R/'kandidat-mod/costumes'/f'costume{cid:03d}_{j:03d}_idx.png'
  if old.exists():assert np.array_equal(np.asarray(Image.open(old)),a),(cid,j)
 print(cid,len(arrays),how,'original indexed data verified when available')
