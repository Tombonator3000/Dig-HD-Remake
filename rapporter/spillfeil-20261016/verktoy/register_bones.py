import os
"""Fit HD bone paint to the source puzzle's geometry and local bone palette."""
from pathlib import Path
import json,os,shutil,hashlib
import cv2,numpy as np
from PIL import Image
R=Path(os.environ.get("DIGHD_WORKSPACE",Path.cwd()));M=R/'kandidat-mod/costumes';B=Path('/home/tom/Documents/Codex/2026-10-16-the-dig-hd-remake-sp-rsm/testing/linux-release/AppDir/usr/share/the-dig-hd/mods/gpt/costumes');P=R/'grafikk/rapporter/spillfeil-20261016';O=P/'mod-overrides/costumes';records=[]
for f in sorted(B.glob('costume121_*_idx.png')):
 src=Image.open(f).convert('RGBA');s=np.asarray(src);mask=(s[:,:,3]>128)&~((s[:,:,0]>180)&(s[:,:,2]>150)&(s[:,:,1]<100));y,x=np.where(mask)
 if len(y)<4:continue
 art=Image.open(B/f.name.replace('_idx','_hd')).convert('RGBA');a=np.asarray(art).copy();px=(art.width//4-src.width)//2;py=(art.height//4-src.height)//2
 target=np.pad(mask,((py,py),(px,px))).astype('uint8')
 target=cv2.resize(target,None,fx=4,fy=4,interpolation=cv2.INTER_NEAREST)
 # Preserve the source outline while removing its 4x4 stair steps.
 target=cv2.GaussianBlur(target.astype('float32'),(0,0),.9)
 destmask=(target>.5).astype('uint8');oldmask=(a[:,:,3]>128).astype('uint8')
 def distance(m):return cv2.distanceTransform(m,cv2.DIST_L2,5)-cv2.distanceTransform(1-m,cv2.DIST_L2,5)
 sd=distance(destmask);ad=distance(oldmask)
 # Backward dense correspondence solves source silhouette -> current art.
 flow=cv2.calcOpticalFlowFarneback(np.clip(sd*4+128,0,255).astype('uint8'),np.clip(ad*4+128,0,255).astype('uint8'),None,.5,5,35,7,7,1.5,0)
 yy,xx=np.indices(sd.shape,dtype='float32');mapped=cv2.remap(a,xx+flow[:,:,0],yy+flow[:,:,1],cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
 # Every target point must sample actual bone paint, not an old hole.
 missing=(mapped[:,:,3]<128)&(target>.05)
 good=(mapped[:,:,3]>=128).astype('uint8');_,labels=cv2.distanceTransformWithLabels(1-good,cv2.DIST_L2,5,labelType=cv2.DIST_LABEL_PIXEL);gy,gx=np.where(good);lookup=np.stack([gy,gx],1)
 if missing.any() and len(lookup):
  near=lookup[np.maximum(labels[missing]-1,0)];mapped[missing,:3]=mapped[near[:,0],near[:,1],:3]
 # Original bones are cool lavender/white. Keep current paint's luminance,
 # but use source local chroma; green shell lighting must stay off bones.
 color=s[:,:,:3].astype('float32');col=np.pad(color,((py,py),(px,px),(0,0)));col=cv2.resize(col,(art.width,art.height),interpolation=cv2.INTER_NEAREST)
 sm=np.pad(mask.astype('uint8'),((py,py),(px,px)));sm=cv2.resize(sm,(art.width,art.height),interpolation=cv2.INTER_NEAREST)
 _,lab=cv2.distanceTransformWithLabels(1-sm,cv2.DIST_L2,5,labelType=cv2.DIST_LABEL_PIXEL);sy,sx=np.where(sm);lut=np.stack([sy,sx],1);ny,nx=lut[np.maximum(lab-1,0)].transpose(2,0,1);col=col[ny,nx]
 lum=mapped[:,:,:3].astype('float32').mean(2);base=col.mean(2);new=col/np.maximum(base[:,:,None],1)*lum[:,:,None]
 mapped[:,:,:3]=np.clip(new,0,255);mapped[:,:,3]=np.clip((target-.12)/.76,0,1)*255
 name=f.name.replace('_idx','_hd');Image.fromarray(mapped).save(O/name);tmp=M/(name+'.new');shutil.copy2(O/name,tmp);os.replace(tmp,M/name)
 records.append({'file':name,'source_indices_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'original_silhouette_iou':float(((mapped[:,:,3]>128)&destmask).sum()/((mapped[:,:,3]>128)|destmask).sum()),'max_registration_flow_hd':float(np.abs(flow).max()),'colour':'source local bone chroma, HD paint luminance'})
(P/'BONES-REGISTRATION.json').write_text(json.dumps(records,indent=2));print(len(records),'bones registered')
