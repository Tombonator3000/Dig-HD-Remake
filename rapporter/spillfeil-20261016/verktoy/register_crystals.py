import os
from pathlib import Path
import cv2,numpy as np,json,os,shutil,hashlib
from PIL import Image
R=Path(os.environ.get("DIGHD_WORKSPACE",Path.cwd()));M=R/'kandidat-mod/costumes';B=Path('/home/tom/Documents/Codex/2026-10-16-the-dig-hd-remake-sp-rsm/testing/linux-release/AppDir/usr/share/the-dig-hd/mods/gpt/costumes');P=R/'grafikk/rapporter/spillfeil-20261016';O=P/'mod-overrides/costumes';rows=[]
for cid in range(286,290):
 for f in sorted(B.glob(f'costume{cid:03d}_*_idx.png')):
  s=np.asarray(Image.open(f).convert('RGBA'));r,g,b=s[:,:,:3].astype(float).transpose(2,0,1);m=((s[:,:,3]>128)&~((r>65)&(g>30)&(g>r*.25)&(b<r*.55))).astype('uint8');cont,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE);hull=cv2.convexHull(max(cont,key=cv2.contourArea));m[:]=0;cv2.fillConvexPoly(m,hull,1)
  art=Image.open(B/f.name.replace('_idx','_hd')).convert('RGBA');a=np.asarray(art).copy();px=(art.width//4-s.shape[1])//2;py=(art.height//4-s.shape[0])//2
  target=np.zeros((art.height*4,art.width*4),dtype='uint8');vertices=np.rint(((hull[:,0,:]+[px,py])*4+2)*4).astype('int32');cv2.fillConvexPoly(target,vertices,255);alpha=cv2.resize(target,(art.width,art.height),interpolation=cv2.INTER_AREA)
  good=(a[:,:,3]>128).astype('uint8');_,lab=cv2.distanceTransformWithLabels(1-good,cv2.DIST_L2,5,labelType=cv2.DIST_LABEL_PIXEL);y,x=np.where(good);lut=np.stack([y,x],1);missing=(a[:,:,3]<128)&(alpha>0);near=lut[np.maximum(lab[missing]-1,0)];a[missing,:3]=a[near[:,0],near[:,1],:3];a[:,:,3]=alpha
  name=f.name.replace('_idx','_hd');Image.fromarray(a).save(O/name);tmp=M/(name+'.new');shutil.copy2(O/name,tmp);os.replace(tmp,M/name)
  rows.append({'file':name,'original_indices_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'source_vertices':hull[:,0,:].tolist(),'source_silhouette_locked':True,'matte_removed':True})
(P/'CRYSTAL-REGISTRATION.json').write_text(json.dumps(rows,indent=2));print(len(rows),'crystal silhouettes locked')
