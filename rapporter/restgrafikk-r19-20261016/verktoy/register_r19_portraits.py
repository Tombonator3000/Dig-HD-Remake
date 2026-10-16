import os
from pathlib import Path
from PIL import Image
import numpy as np,cv2,json,hashlib
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));P=R/'grafikk/rapporter/restgrafikk-r19-20261016';S=R/'testing/source/costumes';O=P/'mod-tillegg/costumes';M=R/'hd-leveranse/costumes'
plans=json.loads((P/'portrait-plans.json').read_text());receipts=[]
def quad(mask):
 contours,_=cv2.findContours(mask.astype('uint8'),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
 contour=max(contours,key=cv2.contourArea);hull=cv2.convexHull(contour)
 for eps in [.01,.015,.02,.025,.03,.04,.05]:
  q=cv2.approxPolyDP(hull,eps*cv2.arcLength(hull,True),True).reshape(-1,2).astype('float32')
  if len(q)==4:break
 assert len(q)==4
 total=q.sum(1);diff=q[:,1]-q[:,0]
 return np.array([q[total.argmin()],q[diff.argmin()],q[total.argmax()],q[diff.argmax()]],dtype='float32')
for cid,threshold in [(224,12),(225,13),(226,12),(227,10)]:
 atlas=np.array(Image.open(P/f'portrait{cid}-master.png').convert('RGBA'));n,labels,stats,centers=cv2.connectedComponentsWithStats((atlas[:,:,3]>128).astype('uint8'),8)
 ids=[i for i in range(1,n) if stats[i,4]>10000];ids.sort(key=lambda i:(int(centers[i,1]//341),centers[i,0]))
 plan=plans[str(cid)];assert len(plan)==len(ids),(cid,len(ids),len(plan))
 masters=[];reference=[]
 for i,c in zip(ids,plan):
  x,y,w,h=map(int,stats[i,:4]);tile=atlas[max(0,y-4):y+h+4,max(0,x-4):x+w+4].copy();src=np.array(Image.open(S/c['file']).convert('RGBA'))
  q1=quad(tile[:,:,3]>128);q2=quad(src[:,:,3]>128)*4+16
  transform=cv2.getPerspectiveTransform(q1,q2);warped=cv2.warpPerspective(tile,transform,((src.shape[1]+8)*4,(src.shape[0]+8)*4),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT)
  # Lock monochrome display values, preserving native drawn shading.
  gray=cv2.cvtColor(warped[:,:,:3],cv2.COLOR_RGB2GRAY);warped[:,:,:3]=gray[:,:,None];masters.append(warped);reference.append(cv2.cvtColor(src[:,:,:3],cv2.COLOR_RGB2GRAY).astype('float32'))
 cleanfiles=[];cleanarrays=[]
 for f in sorted(S.glob(f'costume{cid:03d}_*_idx.png')):
  a=np.array(Image.open(f).convert('L')).astype('float32')
  if np.abs(a-cv2.GaussianBlur(a,(0,0),1)).mean()<threshold:cleanfiles.append(f);cleanarrays.append(a)
 cleanarrays=np.array(cleanarrays);reference=np.array(reference)
 for f in sorted(S.glob(f'costume{cid:03d}_*_idx.png')):
  name=f.name.replace('_idx','_hd')
  if (M/name).exists() or (M/f.name.replace('_idx','')).exists():continue
  src=np.array(Image.open(f).convert('RGBA'));gray=cv2.cvtColor(src[:,:,:3],cv2.COLOR_RGB2GRAY).astype('float32');noisy=float(np.abs(gray-cv2.GaussianBlur(gray,(0,0),1)).mean())>=threshold
  # Select the exact original clean expression closest to the transmitted
  # phase, then its native representative; distortion is a separate layer.
  h,w=gray.shape
  canonical=cv2.resize(gray,(reference.shape[2],reference.shape[1]),interpolation=cv2.INTER_LINEAR)
  blurred=cv2.GaussianBlur(canonical,(0,0),1)
  scores=np.array([np.mean(np.abs(cv2.GaussianBlur(a,(0,0),1)-blurred)) for a in cleanarrays]);best=int(scores.argmin());base=cleanarrays[best]
  weights=np.ones_like(base);bh,bw=base.shape;weights[int(bh*.55):int(bh*.9),int(bw*.25):int(bw*.8)]=3
  slot=int((((reference-base)**2)*weights).mean((1,2)).argmin())
  tile=Image.fromarray(masters[slot][16:-16,16:-16]).resize((w*4,h*4),Image.Resampling.LANCZOS)
  out=np.zeros(((h+8)*4,(w+8)*4,4),dtype='uint8');out[16:16+h*4,16:16+w*4]=np.asarray(tile)
  base=cv2.resize(base,(w,h),interpolation=cv2.INTER_LINEAR)
  if noisy:
   # Original line jitter and noise remain intentional transmission effects.
   # Only the residual is transferred, never an original portrait overlay.
   shifts=[]
   for row in range(h):
    costs=[np.mean(np.minimum(np.abs(gray[row]-np.roll(base[row],dx)),50)) for dx in range(-8,9)]
    shifts.append(int(np.argmin(costs))-8)
   shifts=cv2.GaussianBlur(np.array(shifts,dtype='float32')[:,None],(1,5),0).ravel()
   yy,xx=np.mgrid[:h,:w].astype('float32');warpedbase=cv2.remap(base,xx-shifts[:,None],yy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
   residual=gray-warpedbase
   gy,gx=np.mgrid[:out.shape[0],:out.shape[1]].astype('float32');line=np.interp((gy[:,0]-16)/4,np.arange(h),shifts)*4
   shifted=cv2.remap(out,(gx-line[:,None]).astype('float32'),gy,cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT)
   r=cv2.resize(residual,(w*4,h*4),interpolation=cv2.INTER_CUBIC)
   shifted[16:16+h*4,16:16+w*4,:3]=np.clip(shifted[16:16+h*4,16:16+w*4,:3].astype(float)+r[:,:,None],0,255).astype('uint8')
   # Signal distortion affects the screen content, never the frame boundary.
   mask=cv2.resize((src[:,:,3]>128).astype('uint8'),(w*4,h*4),interpolation=cv2.INTER_NEAREST);inner=cv2.erode(mask,np.ones((9,9),'uint8'));region=out[16:16+h*4,16:16+w*4];region[inner>0]=shifted[16:16+h*4,16:16+w*4][inner>0]
  # Every phase retains its original transmitted screen coverage, including
  # cropped or broken signal frames. No frame is completed by the importer.
  coverage=cv2.resize(src[:,:,3],(w*4,h*4),interpolation=cv2.INTER_CUBIC)
  out[16:16+h*4,16:16+w*4,3]=np.minimum(out[16:16+h*4,16:16+w*4,3],coverage)
  dest=O/name;Image.fromarray(out).save(dest)
  receipts.append(dict(file=name,native_slot=slot,original_representative=plan[slot]['file'],closest_clean_original=cleanfiles[best].name,signal_distortion=noisy,sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
(P/'portrait-registration.json').write_text(json.dumps(receipts,indent=2)+'\n');print(len(receipts),'portrait phases registered')
