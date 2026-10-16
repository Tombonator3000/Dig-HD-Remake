import os
from pathlib import Path
from PIL import Image
import numpy as np,json
R=Path(os.environ.get("DIGHD_WORKSPACE",Path.cwd()));P=R/'grafikk/rapporter/spillfeil-20261016/produksjon';M=R/'kandidat-mod';plan=[];o=Image.new('RGBA',(1536,1168))
for j,f in enumerate(sorted((M/'costumes').glob('costume103_*_idx.png'))):
 im=Image.open(f).convert('RGBA');a=np.asarray(im).copy();a[(a[:,:,0]>180)&(a[:,:,2]>150)&(a[:,:,1]<100),3]=0;im=Image.fromarray(a);b=im.getbbox()
 if not b or b[3]-b[1]<15:continue
 im=im.crop(b);im=im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST);im.thumbnail((230,270));j=len(plan);o.alpha_composite(im,(j%6*256+(256-im.width)//2,j//6*292+(292-im.height)//2));plan.append({'file':f.name,'bbox':b})
o.save(P/'boston103-reference.png');(P/'boston103-plan.json').write_text(json.dumps(plan,indent=2));print('Boston poses',len(plan))
o=Image.new('RGBA',(1536,512))
for j,oid in enumerate([633,634,636,678]):
 im=Image.open(M/'objects'/f'obj{oid:03d}_01_idx.png').convert('RGBA');im=im.resize((im.width*8,im.height*8),Image.Resampling.NEAREST);im.thumbnail((360,460));o.alpha_composite(im,(j*384+(384-im.width)//2,(512-im.height)//2))
o.save(P/'rod-reference.png')
