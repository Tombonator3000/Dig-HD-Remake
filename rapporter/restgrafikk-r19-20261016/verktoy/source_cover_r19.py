import os
from pathlib import Path
from PIL import Image
import numpy as np,cv2,json,sys
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));S=R/'testing/source/costumes';P=R/'grafikk/rapporter/restgrafikk-r19-20261016'
cid=int(sys.argv[1]) if len(sys.argv)>1 else 328
files=sorted(S.glob(f'costume{cid:03d}_*_idx.png'));images={f.stem.removesuffix('_idx'):np.array(Image.open(f).convert('RGBA')) for f in files}
cover={};offsets={}
for parent,a in images.items():
 cover[parent]=[]
 for target,b in images.items():
  if b.shape[0]>a.shape[0] or b.shape[1]>a.shape[1]:continue
  valid=b[:,:,3]>128
  if not valid.any():continue
  mask=np.repeat(valid[:,:,None].astype('uint8'),4,2)
  result=cv2.matchTemplate(a,b,cv2.TM_SQDIFF,mask=mask);result=np.nan_to_num(result,nan=1e20,posinf=1e20,neginf=1e20)
  _,_,pos,_=cv2.minMaxLoc(result);x,y=pos
  crop=a[y:y+b.shape[0],x:x+b.shape[1]]
  if np.array_equal(crop[valid],b[valid]):
   cover[parent].append(target);offsets[parent,target]=[x,y]
remaining=set(images);selected=[];mappings={}
while remaining:
 best=max(cover,key=lambda p:len(set(cover[p])&remaining));hits=set(cover[best])&remaining
 if not hits:break
 selected.append(best)
 for target in hits:mappings[target]=dict(parent=best,offset=offsets[best,target])
 remaining-=hits
result=dict(costume=cid,total=len(images),masters=selected,mapping=mappings,empty=sorted(remaining))
(P/f'source-cover-{cid}.json').write_text(json.dumps(result,indent=2));print(cid,len(images),'cells,',len(selected),'masters',selected,'empty',remaining)
