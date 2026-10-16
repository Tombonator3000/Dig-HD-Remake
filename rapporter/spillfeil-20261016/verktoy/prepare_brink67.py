import os
from pathlib import Path
from PIL import Image
import numpy as np,json
R=Path(os.environ.get("DIGHD_WORKSPACE",Path.cwd()));P=R/'grafikk/rapporter/spillfeil-20261016/produksjon';M=R/'kandidat-mod';o=Image.new('RGBA',(1800,2100));plan=[]
for f in sorted((M/'costumes').glob('costume067_*_idx.png')):
 im=Image.open(f).convert('RGBA');a=np.asarray(im).copy();a[(a[:,:,0]>180)&(a[:,:,2]>150)&(a[:,:,1]<100),3]=0;im=Image.fromarray(a);b=im.getbbox()
 if not b or im.width<20 or im.height<15:continue
 t=im.crop(b).resize(((b[2]-b[0])*4,(b[3]-b[1])*4),Image.Resampling.NEAREST);t.thumbnail((280,280));j=len(plan);o.alpha_composite(t,(j%6*300+(300-t.width)//2,j//6*300+(300-t.height)//2));plan.append({'file':f.name,'bbox':b,'headless':int(f.stem.split('_')[1]) in [3,39,40,41,42,43,44,64,65,66]})
o.save(P/'brink67-reference.png');(P/'brink67-plan.json').write_text(json.dumps(plan,indent=2));print(len(plan))
