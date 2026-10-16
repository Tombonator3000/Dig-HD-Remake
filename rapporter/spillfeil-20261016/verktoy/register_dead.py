import os
from pathlib import Path
from PIL import Image
import numpy as np,json,shutil,os
R=Path(os.environ.get("DIGHD_WORKSPACE",Path.cwd()));P=R/'grafikk/rapporter/spillfeil-20261016';M=R/'kandidat-mod/costumes';O=P/'mod-overrides/costumes'
master=Image.open(P/'produksjon/dead60-master.png').convert('RGBA');plans=json.loads((P/'produksjon/dead60-plan.json').read_text());records=[]
for rec in plans:
 j=rec['cell'];x0=round((j%4)*master.width/4);y0=round((j//4)*master.height/5);x1=round((j%4+1)*master.width/4);y1=round((j//4+1)*master.height/5)
 tile=master.crop((x0,y0,x1,y1));a=np.asarray(tile);ys,xs=np.where(a[:,:,3]>128)
 box=(int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1));tile=tile.crop(box)
 w,h=rec['source_size'];sb=rec['source_bbox'];out=Image.new('RGBA',((w+8)*4,(h+8)*4))
 out.alpha_composite(tile.resize(((sb[2]-sb[0])*4,(sb[3]-sb[1])*4),Image.Resampling.LANCZOS),((sb[0]+4)*4,(sb[1]+4)*4))
 name=rec['stem']+'_hd.png';out.save(O/name);tmp=M/(name+'.new.png');shutil.copy2(O/name,tmp);os.replace(tmp,M/name)
 records.append(dict(rec,generated_bbox=list(box),original_indices_unchanged=True))
(P/'DEAD-REGISTRATION.json').write_text(json.dumps(records,indent=2));print(len(records),'scene cels registered')
