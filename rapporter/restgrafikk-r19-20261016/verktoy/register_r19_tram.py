import os
"""Register painted blue capsule anchors across original phase geometry.
Pure palette masks are classified separately and never painted as red objects.
New phase material comes from generated HD anchor drawings, not old RGB pixels.
"""
from pathlib import Path
import sys,json,hashlib,shutil,os
import numpy as np,cv2
from scipy.ndimage import gaussian_filter1d
from PIL import Image,ImageDraw
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));sys.path.insert(0,str(R/'kode/pipeline'));from dighd import myk
P=R/'grafikk/rapporter/restgrafikk-r19-20261016';S=R/'testing/source/costumes';B=R/'hd-leveranse/costumes';O=P/'mod-tillegg/costumes';M=R/'kandidat-r19/costumes'
plans=json.loads((P/'tram-art-plans.json').read_text());records=[]
def box(mask):
 yy,xx=np.where(mask);return [int(xx.min()),int(yy.min()),int(xx.max()+1-xx.min()),int(yy.max()+1-yy.min())]
def feature(a):
 return cv2.resize(a,(96,96),interpolation=cv2.INTER_AREA).astype('float32')/255

def edges(mask):return np.array([mask[:,0].mean()>.3,mask[:,-1].mean()>.3,mask[0].mean()>.3,mask[-1].mean()>.3])
def coverage(mask):
 h,w=mask.shape;large=np.zeros((h*16,w*16),dtype='uint8');contours,hierarchy=cv2.findContours(mask.astype('uint8'),cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
 if hierarchy is None:return np.zeros((h*4,w*4),'uint8')
 for k,c in enumerate(contours):
  depth=0;parent=int(hierarchy[0,k,3])
  while parent>=0:depth+=1;parent=int(hierarchy[0,parent,3])
  pts=c[:,0,:].astype('float32')
  if len(pts)>4:pts=gaussian_filter1d(pts,sigma=min(1.3,len(pts)/8),axis=0,mode='wrap')
  pts=np.rint((pts+.5)*16).astype('int32');cv2.drawContours(large,[pts[:,None,:]],-1,255 if depth%2==0 else 0,cv2.FILLED)
 large=cv2.dilate(large,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15)))
 return cv2.resize(large,(w*4,h*4),interpolation=cv2.INTER_AREA)
for plan in plans:
 cid=plan['costume'];master=P/f'tram{cid:03d}-master.png'
 anchors=[]
 if not master.exists():
  for n in plan['art_cells']:
   old=B/f'costume{cid:03d}_{n:03d}_hd.png'
   if not old.exists():continue
   source=f'costume{cid:03d}_{n:03d}_idx.png';im=np.array(Image.open(S/source).convert('RGBA'));mask=im[:,:,3]>128;x,y,w,h=box(mask);src=im[y:y+h,x:x+w].copy();a=np.array(Image.open(old).convert('RGBA'));nx,ny,nw,nh=box(a[:,:,3]>128);anchors.append(dict(source=source,source_crop=src,feature=feature(src),edges=edges(mask[y:y+h,x:x+w]),native=a[ny:ny+nh,nx:nx+nw].copy(),native_bbox=[nx,ny,nw,nh],master=old))
  assert anchors,cid
 else:
  native=np.array(Image.open(master).convert('RGBA'));HH,WW=native.shape[:2]
 if master.exists():
  for c in plan['cells']:
   im=np.array(Image.open(S/c['file']).convert('RGBA'));mask=im[:,:,3]>128;x,y,w,h=box(mask);src=im[y:y+h,x:x+w].copy();slot=c['slot'];tile=native[round(slot//4*HH/2):round((slot//4+1)*HH/2),round(slot%4*WW/4):round((slot%4+1)*WW/4)].copy();owner,labels,parts=myk.parts(tile[:,:,3]);keep=np.isin(owner,[p['nr'] for p in parts if p['areal']>=8]);tile[~keep]=0;nx,ny,nw,nh=box(tile[:,:,3]>128);tile=tile[ny:ny+nh,nx:nx+nw].copy();anchors.append(dict(source=c['file'],source_crop=src,feature=feature(src),edges=edges(mask[y:y+h,x:x+w]),native=tile,native_bbox=[nx,ny,nw,nh],master=master))
 for n in plan['art_cells']:
  name=f'costume{cid:03d}_{n:03d}';f=S/(name+'_idx.png');hd=name+'_hd.png'
  if (B/hd).exists() or (B/(name+'.png')).exists():continue
  im=np.array(Image.open(f).convert('RGBA'));H,W=im.shape[:2];mask=im[:,:,3]>128;x,y,w,h=box(mask);crop=im[y:y+h,x:x+w].copy();q=feature(crop);qe=edges(mask[y:y+h,x:x+w]);scores=[]
  for a in anchors:
   fa=a['feature'];intersection=(fa[:,:,3]>.5)&(q[:,:,3]>.5);rgb=float(((fa[:,:,:3]-q[:,:,:3])**2)[intersection].mean()) if intersection.any() else 1.;shape=float(((fa[:,:,3]-q[:,:,3])**2).mean());scores.append(rgb+shape*2+float((a['edges']!=qe).sum())*.2)
  k=int(np.argmin(scores));a=anchors[k];fit=myk._premul_resize(a['native'],(w*4,h*4));alpha=fit[:,:,3:4].astype('float32')/255;premul=fit[:,:,:3].astype('float32')*alpha
  targetgray=cv2.cvtColor((q[:,:,:3]*255).astype('uint8'),cv2.COLOR_RGB2GRAY);refgray=cv2.cvtColor((a['feature'][:,:,:3]*255).astype('uint8'),cv2.COLOR_RGB2GRAY);flow=cv2.calcOpticalFlowFarneback(targetgray,refgray,None,.5,3,17,4,7,1.3,0);flow=cv2.GaussianBlur(np.clip(flow,-4,4),(0,0),8);flow=np.clip(flow,-1.5,1.5);full=cv2.resize(flow,(w*4,h*4),interpolation=cv2.INTER_CUBIC);yy,xx=np.mgrid[:h*4,:w*4].astype('float32');mx=xx+full[:,:,0]*(w*4/96);my=yy+full[:,:,1]*(h*4/96);warped=cv2.remap(premul,mx,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT);al=cv2.remap(alpha,mx,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT);al=al[:,:,None] if al.ndim==2 else al;rgb=warped/np.maximum(al,.0001);good=al[:,:,0]>.5;targetalpha=coverage(mask[y:y+h,x:x+w])
  if not good.all():
   _,labels=cv2.distanceTransformWithLabels((~good).astype('uint8'),cv2.DIST_L2,5,labelType=cv2.DIST_LABEL_PIXEL);gy,gx=np.where(good);lut=np.stack([gy,gx],1);bad=~good;near=lut[np.maximum(labels[bad]-1,0)];rgb[bad]=rgb[near[:,0],near[:,1]]
  # Straight crop boundaries are technical cuts, not physical black rims.
  # Extend adjacent HD material through the generated outline there.
  sx=max(1,min(12,round(3*w*4/a['native'].shape[1])));sy=max(1,min(12,round(3*h*4/a['native'].shape[0])))
  if qe[0] and sx<rgb.shape[1]:rgb[:,:sx]=rgb[:,sx:sx+1]
  if qe[1] and sx<rgb.shape[1]:rgb[:,-sx:]=rgb[:,-sx-1:-sx]
  if qe[2] and sy<rgb.shape[0]:rgb[:sy]=rgb[sy:sy+1]
  if qe[3] and sy<rgb.shape[0]:rgb[-sy:]=rgb[-sy-1:-sy]
  art=np.dstack([np.clip(rgb,0,255).astype('uint8'),targetalpha]);out=Image.new('RGBA',((W+8)*4,(H+8)*4));out.alpha_composite(Image.fromarray(art),((x+4)*4,(y+4)*4));out.save(O/hd)
  for source,dest in [(O/hd,hd),(f,f.name)]:
   if (B/dest).exists():continue
   if source!=O/hd:shutil.copy2(source,O/dest)
   tmp=M/(dest+'.new');shutil.copy2(source,tmp);os.replace(tmp,M/dest)
  originalmask=cv2.resize(mask[y:y+h,x:x+w].astype('uint8'),(w*4,h*4),interpolation=cv2.INTER_NEAREST)>0;newmask=targetalpha>128;iou=float((originalmask&newmask).sum()/max(1,(originalmask|newmask).sum()));records.append(dict(file=hd,anchor=a['source'],master=str(a['master'].relative_to(R)),master_sha256=hashlib.sha256(a['master'].read_bytes()).hexdigest(),anchor_score=float(scores[k]),source_bbox=[x,y,w,h],alpha_iou=iou,flow_limit_normalized=1.5,method='painted anchor reuse with bounded original phase flow and smoothed antialiased original contour; no source RGB pasted',sha256=hashlib.sha256((O/hd).read_bytes()).hexdigest()))
(P/'tram-art-registration.json').write_text(json.dumps(records,indent=2)+'\n');print(len(records),'new painted capsule phases; lowest alpha IoU',min(r['alpha_iou'] for r in records))
# Original/HD pairs, including closed, open and clipped capsule phases.
preview=Image.new('RGB',(1600,1200),(43,48,58));draw=ImageDraw.Draw(preview)
selection=[]
for cid in [268,270,272,274,276]:
 members=[r for r in records if r['file'].startswith(f'costume{cid:03d}_')]
 if members:selection.extend([members[0],members[len(members)//2]])
for j,r in enumerate(selection):
 px=j%4*400;py=j//4*400;old=Image.open(S/r['file'].replace('_hd','_idx')).convert('RGBA');new=Image.open(O/r['file']).convert('RGBA');old.thumbnail((180,350));new.thumbnail((180,350));preview.paste(old,(px,py+30),old);preview.paste(new,(px+195,py+30),new);draw.text((px+5,py+5),r['file'],fill='white')
preview.save(P/'tram-art-preview.png')
