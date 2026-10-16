import os
from inspect_assets import R,GAME,g,d,ix,rooms
import json,struct
out={}
for cid in [14,15,16,17,18,58,59,60,67,73,103]:
 rn,ofs=ix.costume_dir[cid];p=rooms[rn].offset+ofs
 bl={t:(o+8,s-8) for t,o,s in g.children(d,p+8,p+g.be32(d,p+4))}
 aksq=d[bl[b'AKSQ'][0]:sum(bl[b'AKSQ'])];rows=[]
 p=0
 while p<len(aksq)-7:
  if aksq[p:p+2] not in [b'\xc0\x20',b'\xc0\x25']:p+=1;continue
  q=p+2+(4 if aksq[p+1]==0x25 else 0);count=aksq[q];q+=1;parts=[]
  try:
   for _ in range(count):
    x,y=struct.unpack_from('<hh',aksq,q);q+=4;c=struct.unpack_from('>H',aksq,q)[0] if aksq[q]&0x80 else aksq[q];q+=2 if aksq[q]&0x80 else 1
    if c&0xc000==0xc000 or c&0xfff>=bl[b'AKOF'][1]//6:raise ValueError()
    parts.append({'cel':c&0xfff,'x':x,'y':y})
   if parts:rows.append({'offset':p,'parts':parts})
   p=q
  except (ValueError,IndexError,struct.error):p+=1
 out[cid]=rows
 print(cid,rows[:4])
(R/'testing/geometry.json').write_text(json.dumps(out,indent=2))
