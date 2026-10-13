from pathlib import Path
from PIL import Image
import cv2,numpy as np,shutil,json
R=Path('.');P=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk/rapporter/spillfeil-r12-20261013');O=P/'mod-overrides/objects';M=R/'AppDir/usr/share/the-dig-hd/mods/gpt/objects';S=R/'original/objects';atlas=Image.open(P/'produksjon/pda-paneler-master.png').convert('RGBA');ids=[537,542,541,544,543,546,538,539,540];records=[]
def quad(mask):
 ys,xs=np.where(mask);c=np.column_stack((xs,ys)).astype(np.int32);h=cv2.convexHull(c);ap=cv2.approxPolyDP(h,.025*cv2.arcLength(h,True),True).reshape(-1,2)
 if len(ap)!=4:
  rect=cv2.minAreaRect(h);ap=cv2.boxPoints(rect)
 pts=ap.astype(np.float32);sm=pts.sum(1);df=np.diff(pts,axis=1).ravel();return np.array([pts[sm.argmin()],pts[df.argmin()],pts[sm.argmax()],pts[df.argmax()]],np.float32)
for j,oid in enumerate(ids):
 tile=np.asarray(atlas.crop((j%3*512,j//3*341,(j%3+1)*512,(j//3+1)*341)));paintquad=quad(tile[:,:,3]>150)
 for state in ['01','02']:
  stem=f'obj{oid}_{state}';src=S/(stem+'_idx.png')
  if not src.exists():continue
  im=np.asarray(Image.open(src).convert('RGB'));mask=np.asarray(Image.open(S/(stem+'_mask.png')))>127;h,w=mask.shape;target=quad((im.max(2)<120)&mask)*4;matrix=cv2.getPerspectiveTransform(paintquad,target);warped=cv2.warpPerspective(tile,matrix,(w*4,h*4),flags=cv2.INTER_LANCZOS4);a=warped[:,:,3:4].astype(np.float32)/255;rgb=(warped[:,:,:3]*a+237*(1-a));alpha=np.repeat(np.repeat(mask,4,0),4,1).astype(np.uint8)*255;Image.fromarray(np.dstack((np.clip(rgb,0,255).astype(np.uint8),alpha))).save(O/(stem+'.png'))
  shutil.copy2(src,O/src.name);shutil.copy2(S/(stem+'_mask.png'),O/(stem+'_mask.png'))
  for suf in ['.png','_idx.png','_mask.png']:shutil.copy2(O/(stem+suf),M/(stem+suf))
  records.append({'object':stem,'atlas_cell':j,'original_frame_quad4x':target.tolist(),'exact_source_smap_coverage':True})
(P/'PDA-REGISTRERING.json').write_text(json.dumps(records,indent=2));print('PDA states',len(records))
