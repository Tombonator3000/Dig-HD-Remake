import os
# SPDX-License-Identifier: GPL-2.0-or-later
# Format reference copyright (C) 2001-2026 The ScummVM Team.
"""Read original MajMin sprite indices; no HD art is synthesized here.

Algorithm reference: ScummVM engines/scumm/gfx.cpp, MajMinCodec, and
engines/scumm/akos.cpp, paintCelMajMin. ScummVM is GPL-2.0-or-later.
This workbench reader follows that bitstream format, including byte wrapping.
"""
from pathlib import Path
import struct,sys,json
import numpy as np
from PIL import Image
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));sys.path.insert(0,str(R/'kode/pipeline'))
from dighd import gamedata as g
from dighd.export import costume_palette,read_costume_colours
G=Path('/home/tom/Documents/Codex/2026-10-16-the-dig-hd-remake-sp-rsm/testing/linux-release/AppDir/usr/share/the-dig-hd/game');d=(G/'DIG.LA1').read_bytes();ix=g.read_index(G/'DIG.LA0');rooms=g.read_rooms(G/'DIG.LA1');S=R/'testing/source/costumes';P=R/'grafikk/rapporter/restgrafikk-r19-20261016';records=[]
def decode(raw,offset,w,h):
 if w*h==1:return np.array([[raw[offset+1]]],'uint8')
 shift=raw[offset];color=raw[offset+1];bits=int(raw[offset+2])|(int(raw[offset+3])<<8);count=16;q=offset+4;repeat=False;remaining=0;out=[]
 def read(n):
  nonlocal bits,count,q
  if count<=8:
   bits|=int(raw[q])<<count;q+=1;count+=8
  v=bits&((1<<n)-1);bits>>=n;count-=n;return v
 for pixel in range(w*h):
  out.append(color)
  # The final state update has no effect on output and can prefetch past
  # an isolated cel's buffer, so omit it after the last emitted pixel.
  if pixel==w*h-1:break
  if repeat:
   remaining-=1
   if remaining==0:repeat=False
  elif read(1):
   if read(1):
    difference=read(3)-4
    if difference:color=(color+difference)&255
    else:repeat=True;remaining=read(8)-1
   else:color=read(shift)
 return np.array(out,'uint8').reshape(h,w)
for cid in [95,118,266,267]:
 rn,ofs=ix.costume_dir[cid];p=rooms[rn].offset+ofs;bl={t:d[o+8:o+n] for t,o,n in g.children(d,p+8,p+g.be32(d,p+4))};assert g.le16(bl[b'AKHD'],8)==16;arrays=[]
 for j in range(len(bl[b'AKOF'])//6):
  do,co=struct.unpack_from('<IH',bl[b'AKOF'],j*6);w,h=struct.unpack_from('<HH',bl[b'AKCI'],co);arrays.append((decode(bl[b'AKCD'],do,w,h),255))
 pal,how=costume_palette(16,bl.get(b'AKPL',b''),bl.get(b'RGBS',b''),rn,rooms,arrays,read_costume_colours(R/'kode/docs/kostymefarger.csv').get(cid))
 for j,(a,t) in enumerate(arrays):
  name=f'costume{cid:03d}_{j:03d}_idx.png';old=R/'hd-leveranse/costumes'/name;match=None
  if old.exists():match=bool(np.array_equal(np.array(Image.open(old)),a));assert match,(name,'published source index mismatch')
  im=Image.fromarray(a,'P');im.putpalette(pal);im.info['transparency']=255;im.save(S/name);im.convert('RGBA').save(S/name.replace('_idx',''))
  records.append(dict(file=name,size=[a.shape[1],a.shape[0]],published_index_verified=match,palette=how))
 print(cid,len(arrays),'source cels decoded',flush=True)
(P/'codec16-source-check.json').write_text(json.dumps(records,indent=2)+'\n');print(len(records),'decoded; every available published index matched')
