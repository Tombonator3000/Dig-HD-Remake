import os
from pathlib import Path
from PIL import Image
import numpy as np,cv2,json
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));S=R/'testing/source/costumes';P=R/'grafikk/rapporter/restgrafikk-r19-20261016';plans={}
for cid,threshold in [(224,12),(225,13),(226,12),(227,10)]:
 fs=[]
 for f in sorted(S.glob(f'costume{cid:03d}_*_idx.png')):
  a=np.asarray(Image.open(f).convert('L')).astype('float32')
  if np.abs(a-cv2.GaussianBlur(a,(0,0),1)).mean()<threshold:fs.append(f)
 data=np.array([np.asarray(Image.open(f).convert('L')).ravel() for f in fs],dtype='float32')
 k=min(12,len(fs));cv2.setRNGSeed(1)
 _,labels,centers=cv2.kmeans(data,k,None,(cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER,100,.01),10,cv2.KMEANS_PP_CENTERS)
 chosen=[int(np.where(labels.ravel()==j)[0][np.argmin(((data[labels.ravel()==j]-centers[j])**2).mean(1))]) for j in range(k)];chosen=sorted(chosen)
 sheet=Image.new('RGBA',(1536,1024));plan=[]
 for j,i in enumerate(chosen):
  f=fs[i];im=Image.open(f).convert('RGBA');im=im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST);im.thumbnail((340,290));x=j%4*384+(384-im.width)//2;y=j//4*341+(341-im.height)//2;sheet.alpha_composite(im,(x,y));plan.append({'file':f.name,'slot':j,'reference_box':[x,y,im.width,im.height]})
 sheet.save(P/f'portrait{cid}-reference.png');plans[str(cid)]=plan
(P/'portrait-plans.json').write_text(json.dumps(plans,indent=2));print({c:len(v) for c,v in plans.items()})
