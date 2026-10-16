import os
from pathlib import Path
import numpy as np,cv2,json
from PIL import Image
from scipy.ndimage import distance_transform_edt
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));G=R/'grafikk';P=G/'rapporter/restgrafikk-r19-20261016';S=R/'testing/source/costumes';O=P/'mod-tillegg/costumes';receipt=[]
jobs=[('fig214_18',[(30,20,490,465),(485,15,985,475),(940,70,1465,490),(20,480,575,980),(565,470,1130,980)]),('fig214_19',[(20,20,590,465),(590,15,1150,470),(20,470,590,910)]),('fig213_19',[(25,25,330,445),(330,25,655,445)])]
for job,windows in jobs:
 meta=json.loads((G/'jobber'/job/'jobb.json').read_text());art=Image.open(G/'jobber'/job/'resultat-r19.png').convert('RGBA');assert len(meta['ruter'])==len(windows)
 for c,win in zip(meta['ruter'],windows):
  src=Image.open(S/(c['bilde']+'_idx.png')).convert('RGBA');mask=np.asarray(src)[:,:,3]>128;y,x=np.where(mask);sb=(int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1));x0,y0,x1,y1=sb
  t=art.crop(win);a=np.array(t);m=a[:,:,3]>=16;yy,xx=np.where(m);t=t.crop((xx.min(),yy.min(),xx.max()+1,yy.max()+1)).resize(((x1-x0)*4,(y1-y0)*4),Image.Resampling.LANCZOS);a=np.array(t);m=a[:,:,3]>=16
  _,near=distance_transform_edt(~m,return_indices=True);a[:,:,:3]=a[near[0],near[1],:3]
  # The original phase controls every gap and fragment position. Native
  # painted material supplies detail; this registration cannot invent rings.
  sm=mask[y0:y1,x0:x1];signed=distance_transform_edt(sm)-distance_transform_edt(~sm)
  alpha=np.clip(cv2.resize(signed.astype('float32'),(a.shape[1],a.shape[0]),interpolation=cv2.INTER_CUBIC)*2+.5,0,1);a[:,:,3]=np.rint(alpha*255).astype('uint8')
  out=Image.new('RGBA',((src.width+8)*4,(src.height+8)*4));out.alpha_composite(Image.fromarray(a),((x0+4)*4,(y0+4)*4));name=c['bilde']+'_hd.png';out.save(O/name)
  receipt.append(dict(name=name,job=job,window=win,source_bbox=sb,method='native painted material, original source phase fragment registration'))
  if c['kostyme']==214:
   target=name.replace('costume214','costume222');other=Image.open(S/(target.replace('_hd','_idx'))).convert('RGBA');assert np.array_equal(np.asarray(src),np.asarray(other));out.save(O/target);receipt.append(dict(name=target,identical_original_to=name))
(P/'effect-registration.json').write_text(json.dumps(receipt,indent=2)+'\n');print(len(receipt),'registered spiral phases')
