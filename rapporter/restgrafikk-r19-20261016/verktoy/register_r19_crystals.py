import os
from pathlib import Path
import sys,cv2,numpy as np,json,shutil,os
from PIL import Image
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));sys.path.insert(0,str(R/'kode/tools'))
from register_crystal_atlas import core
sys.path.insert(0,str(R/'kode/pipeline'))
from dighd import myk
S=R/'testing/source/costumes';B=R/'hd-leveranse/costumes';P=R/'grafikk/rapporter/restgrafikk-r19-20261016';O=P/'mod-tillegg/costumes';M=R/'kandidat-r19/costumes';refs=[];arts=[]
for i in range(90):
 f=B/f'costume286_{i:03d}_idx.png';im,box,crop=core(f);refs.append(cv2.resize(crop,(64,64),interpolation=cv2.INTER_AREA).astype(float)/255)
 art=Image.open(B/f'costume286_{i:03d}_hd.png').convert('RGBA');a=np.asarray(art);yy,xx=np.where(a[:,:,3]>128);arts.append(art.crop((xx.min(),yy.min(),xx.max()+1,yy.max()+1)))
ref=np.array(refs);rows=[]
for cid in range(278,286):
 for f in sorted(S.glob(f'costume{cid:03d}_*_idx.png')):
  if (B/f.name.replace('_idx','_hd')).exists() or (B/f.name.replace('_idx','')).exists():continue
  raw=np.asarray(Image.open(f).convert('RGBA'))
  if myk.measure_mask(raw)[0].sum()<40:
   result=myk.from_original(raw);name=f.name.replace('_idx','_hd');Image.fromarray(result['bilde']).save(O/name)
   for source,name2 in [(O/name,name),(f,f.name)]:
    if (B/name2).exists():continue
    if source!=O/name:shutil.copy2(source,O/name2)
    temp=M/(name2+'.new');shutil.copy2(source,temp);os.replace(temp,M/name2)
   rows.append({'file':name,'source_fragment':True,'source_pixels':int(myk.measure_mask(raw)[0].sum())});continue
  im,box,crop=core(f);x,y,w,h=box;H,W=im.shape[:2];q=cv2.resize(crop,(64,64),interpolation=cv2.INTER_AREA).astype(float)/255;delta=((ref[:,:,:,:3]-q[:,:,:3])**2).mean((1,2,3))+((ref[:,:,:,3]-q[:,:,3])**2).mean((1,2))*.5;k=int(delta.argmin())
  art=np.asarray(arts[k].resize((w*4,h*4),Image.Resampling.LANCZOS)).copy();cc,_=cv2.findContours((crop[:,:,3]>0).astype('uint8'),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE);hull=cv2.convexHull(max(cc,key=cv2.contourArea));large=np.zeros((h*16,w*16),np.uint8);v=np.rint((hull[:,0,:]*4+2)*4).astype('int32');cv2.fillConvexPoly(large,v,255);alpha=cv2.resize(large,(w*4,h*4),interpolation=cv2.INTER_AREA)
  good=(art[:,:,3]>128).astype('uint8');_,labels=cv2.distanceTransformWithLabels(1-good,cv2.DIST_L2,5,labelType=cv2.DIST_LABEL_PIXEL);yy,xx=np.where(good);lut=np.stack([yy,xx],1);missing=(art[:,:,3]<128)&(alpha>0);near=lut[np.maximum(labels[missing]-1,0)];art[missing,:3]=art[near[:,0],near[:,1],:3]
  # Preserve each door's actual source crystal intensity and hue, rather than its orange matte.
  original=crop[:,:,:3][crop[:,:,3]>128].astype(float).mean(0);paint=art[:,:,:3][alpha>128].astype(float).mean(0);factor=np.clip(original/max(paint.max(),1),.1,1.5);factor*=max(paint.max(),1)/np.maximum(paint,3);factor=np.clip(factor,.3,1.6);art[:,:,:3]=np.clip(art[:,:,:3]*factor,0,255).astype('uint8');art[:,:,3]=alpha
  out=Image.new('RGBA',((W+4)*4,(H+4)*4));out.alpha_composite(Image.fromarray(art),((x+2)*4,(y+2)*4));name=f.name.replace('_idx','_hd');out.save(O/name)
  for source,name2 in [(O/name,name),(f,f.name)]:
   if (B/name2).exists():continue
   if source!=O/name:shutil.copy2(source,O/name2)
   temp=M/(name2+'.new');shutil.copy2(source,temp);os.replace(temp,M/name2)
  rows.append({'file':name,'reference':k,'mse':float(delta[k]),'source_bbox':box,'matte_removed':True})
(P/'crystal-registration.json').write_text(json.dumps(rows,indent=2));print(len(rows))
