import os
"""Register native cave-rat poses against original artwork, leaving palette shadows to the engine."""
from pathlib import Path
import sys,json,hashlib,shutil,os
import numpy as np,cv2
from scipy.ndimage import gaussian_filter1d
from PIL import Image,ImageDraw
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));sys.path.insert(0,str(R/'kode/pipeline'));from dighd import myk
P=R/'grafikk/rapporter/restgrafikk-r19-20261016';S=R/'testing/source/costumes';A=R/'testing/rat183-source';B=R/'hd-leveranse/costumes';O=P/'mod-tillegg/costumes';M=R/'kandidat-r19/costumes'
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
plan=json.loads((P/'rat183-plan.json').read_text());anchors=[];records=[]
trap=json.loads((P/'rat183-trap-plan.json').read_text());combined=set(trap['combined_cells'])
for batch in plan['batches']:
 master=P/f'rat183-{batch["batch"]:02d}-master.png';native=np.array(Image.open(master).convert('RGBA'));HH,WW=native.shape[:2]
 for c in batch['cells']:
  if c['cel'] in combined:continue
  im=np.array(Image.open(A/c['file']).convert('RGBA'));mask=im[:,:,3]>128;x,y,w,h=box(mask);src=im[y:y+h,x:x+w];slot=c['slot'];tile=native[round(slot//4*HH/2):round((slot//4+1)*HH/2),round(slot%4*WW/4):round((slot%4+1)*WW/4)].copy();owner,labels,parts=myk.parts(tile[:,:,3]);keep=np.isin(owner,[p['nr'] for p in parts if p['areal']>=8]);tile[~keep]=0;nx,ny,nw,nh=box(tile[:,:,3]>128);anchors.append(dict(source=c['file'],feature=feature(src),aspect=w/h,native=tile[ny:ny+nh,nx:nx+nw].copy(),master=master))
for c in plan['art_cells']:
 if c['cel'] in combined:continue
 f=S/c['file'];hd=f.name.replace('_idx','_hd');assert not (B/hd).exists();im=np.array(Image.open(A/c['file']).convert('RGBA'));H,W=im.shape[:2];mask=im[:,:,3]>128;x,y,w,h=box(mask);crop=im[y:y+h,x:x+w].copy();q=feature(crop);scores=[]
 for a in anchors:
  fa=a['feature'];intersection=(fa[:,:,3]>.5)&(q[:,:,3]>.5);rgb=float(((fa[:,:,:3]-q[:,:,:3])**2)[intersection].mean()) if intersection.any() else 1.;shape=float(((fa[:,:,3]-q[:,:,3])**2).mean());scores.append(rgb+shape*2+min(abs(np.log((w/h)/a['aspect'])),2)*.04)
 k=int(np.argmin(scores));a=anchors[k];fit=myk._premul_resize(a['native'],(w*4,h*4));alpha=fit[:,:,3:4].astype('float32')/255;premul=fit[:,:,:3].astype('float32')*alpha
 targetgray=cv2.cvtColor((q[:,:,:3]*255).astype('uint8'),cv2.COLOR_RGB2GRAY);refgray=cv2.cvtColor((a['feature'][:,:,:3]*255).astype('uint8'),cv2.COLOR_RGB2GRAY);flow=cv2.calcOpticalFlowFarneback(targetgray,refgray,None,.5,3,17,4,7,1.3,0);flow=cv2.GaussianBlur(np.clip(flow,-4,4),(0,0),6);flow=np.clip(flow,-3,3);full=cv2.resize(flow,(w*4,h*4),interpolation=cv2.INTER_CUBIC);yy,xx=np.mgrid[:h*4,:w*4].astype('float32');mx=xx+full[:,:,0]*(w*4/96);my=yy+full[:,:,1]*(h*4/96);warped=cv2.remap(premul,mx,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT);al=cv2.remap(alpha,mx,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT);al=al[:,:,None] if al.ndim==2 else al;rgb=warped/np.maximum(al,.0001);good=al[:,:,0]>.5;targetalpha=np.rint(np.clip(al[:,:,0],0,1)*255).astype('uint8')
 if not good.all():
  _,labels=cv2.distanceTransformWithLabels((~good).astype('uint8'),cv2.DIST_L2,5,labelType=cv2.DIST_LABEL_PIXEL);gy,gx=np.where(good);lut=np.stack([gy,gx],1);bad=~good;near=lut[np.maximum(labels[bad]-1,0)];rgb[bad]=rgb[near[:,0],near[:,1]]
 art=np.dstack([np.clip(rgb,0,255).astype('uint8'),targetalpha]);out=Image.new('RGBA',((W+8)*4,(H+8)*4));out.alpha_composite(Image.fromarray(art),((x+4)*4,(y+4)*4));out.save(O/hd)
 for source,dest in [(O/hd,hd),(f,f.name)]:
  if (B/dest).exists():continue
  if source!=O/hd:shutil.copy2(source,O/dest)
  tmp=M/(dest+'.new');shutil.copy2(source,tmp);os.replace(tmp,M/dest)
 records.append(dict(file=hd,anchor=a['source'],master=str(a['master'].relative_to(R)),master_sha256=hashlib.sha256(a['master'].read_bytes()).hexdigest(),anchor_score=float(scores[k]),source_bbox=[x,y,w,h],palette='original room68 palette1 through AKPL; technical shadow code13 excluded',method='native painted pose reuse with bounded original phase flow and native painted alpha and bounded whole-pose transform; no source RGB pasted',sha256=hashlib.sha256((O/hd).read_bytes()).hexdigest()))
(P/'rat183-registration.json').write_text(json.dumps(records,indent=2)+'\n');print(len(records),'rat artwork phases registered; trap composites handled separately')
preview=Image.new('RGB',(1536,1024),(44,47,55));draw=ImageDraw.Draw(preview)
for j,r in enumerate(records[::max(1,len(records)//16)][:16]):
 px=j%4*384;py=j//4*256;old=Image.open(A/r['file'].replace('_hd','_idx')).convert('RGBA');bb=old.getbbox();old=old.crop(bb);old=old.resize((old.width*4,old.height*4),Image.Resampling.NEAREST);old.thumbnail((180,210));new=Image.open(O/r['file']).convert('RGBA');new=new.crop(new.getbbox());new.thumbnail((180,210));preview.paste(old,(px,py+30),old);preview.paste(new,(px+192,py+30),new);draw.text((px+5,py+5),r['file'],fill='white')
preview.save(P/'rat183-preview.png')
