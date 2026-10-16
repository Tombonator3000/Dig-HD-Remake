import os
from pathlib import Path
from PIL import Image
import numpy as np,json
R=Path(os.environ.get("DIGHD_WORKSPACE",Path.cwd()));M=R/'kandidat-mod/costumes';O=R/'grafikk/rapporter/spillfeil-20261016/produksjon';O.mkdir(parents=True,exist_ok=True)
files=[]
for f in sorted(M.glob('costume060_*_idx.png')):
 im=Image.open(f).convert('RGBA')
 if im.width>30:files.append(f)
sheet=Image.new('RGBA',(1536,1280));records=[]
for j,f in enumerate(files):
 im=Image.open(f).convert('RGBA');a=np.asarray(im).copy();r,g,b=a[:,:,:3].transpose(2,0,1)
 technical=(r>180)&(b>150)&(g<100)
 a[technical,3]=0;im=Image.fromarray(a);box=im.getbbox()
 scale=min(4,352/im.width,224/im.height);w=round(im.width*scale);h=round(im.height*scale)
 x=(j%4)*384+(384-w)//2;y=(j//4)*256+(256-h)//2
 sheet.alpha_composite(im.resize((w,h),Image.Resampling.NEAREST),(x,y))
 records.append({'stem':f.stem.replace('_idx',''),'cell':j,'source_size':im.size,'source_bbox':box,'reference_pos':[x,y]})
sheet.save(O/'dead60-source.png');(O/'dead60-plan.json').write_text(json.dumps(records,indent=2));print(len(records))
