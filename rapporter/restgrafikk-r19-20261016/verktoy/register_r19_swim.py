import os
"""Register painted swimming poses as whole bodies, with bubbles kept separate.
The source body palette is 192..219. Water dither and magenta marks do not
control head/body scale. No old face pixels are overlaid on new drawings.
"""
from pathlib import Path
import sys,json,hashlib,shutil,os
import numpy as np,cv2
from PIL import Image
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));sys.path.insert(0,str(R/'kode/pipeline'))
from dighd import myk
P=R/'grafikk/rapporter/restgrafikk-r19-20261016';S=R/'testing/source/costumes';B=R/'hd-leveranse/costumes';O=P/'mod-tillegg/costumes';M=R/'kandidat-r19/costumes'
plans=json.loads((P/'boston118-plans.json').read_text());records=[];selected={};batch_of={c['file']:b['batch'] for b in plans for c in b['cells']}
def bbox(mask):
 ys,xs=np.where(mask);return [int(xs.min()),int(ys.min()),int(xs.max()+1-xs.min()),int(ys.max()+1-ys.min())] if len(xs) else None
for batch in plans:
 num=batch['batch'];f=P/('boston118-pilot-master.png' if num==0 else f'boston118-{num}-master.png')
 if not f.exists():continue
 a=np.array(Image.open(f).convert('RGBA'));H,W=a.shape[:2]
 for cell in batch['cells']:
  s=cell['slot']
  if num==0 and s==7:continue
  tile=a[round(s//4*H/2):round((s//4+1)*H/2),round(s%4*W/4):round((s%4+1)*W/4)].copy();owner,lab,parts=myk.parts(tile[:,:,3]);parts=sorted([v for v in parts if v['areal']>=10],key=lambda v:-v['areal']);assert parts,(num,s)
  selected[cell['file']]=(tile,owner,parts,f)
if 'costume118_062_idx.png' in selected:
 selected['costume118_001_idx.png']=selected['costume118_062_idx.png']
for f in sorted(S.glob('costume118_*_idx.png')):
 src=np.array(Image.open(f).convert('RGBA'));idx=np.array(Image.open(f));h,w=src.shape[:2];mask,_=myk.measure_mask(src);hd=f.name.replace('_idx','_hd');area=int(mask.sum())
 if f.name not in selected and area>=40:continue
 if area<40:
  result=myk.from_original(src)['bilde'];notes=dict(method='small original water/bubble fragment, soft source-preserving resampling')
 else:
  tile,owner,parts,native=selected[f.name];out=Image.new('RGBA',((w+8)*4,(h+8)*4));body=(idx>=192)&(idx<=219)&mask;target=bbox(body)
  if target is None or int(body.sum())<20:
   target=bbox(mask);method='painted surface splash, complete original extent'
  else:method='whole painted body fit to source body palette extent; head and torso transformed together'
  combined=int(body.sum())<20 or batch_of[f.name] in [1,2] or int(((src[:,:,0]>140)&(src[:,:,1]>190)&(src[:,:,2]>190)&mask).sum())>20
  bb=None
  if combined:
   # Water and the tiny partly submerged man form one original composition.
   # Keep every native component, not only the largest foam/bubble piece.
   target=bbox(mask);nb=bbox(tile[:,:,3]>128);x,y,pw,ph=nb;cut=tile[y:y+ph,x:x+pw].copy();tx,ty,tw,th=target
   out.alpha_composite(Image.fromarray(myk._premul_resize(cut,(tw*4,th*4))),((tx+4)*4,(ty+4)*4));p=dict(boks=nb);method='complete painted water/figure or bubble composition fit to full original extent'
  else:
   p=parts[0];x,y,pw,ph=p['boks'];cut=tile[y:y+ph,x:x+pw].copy();cut[owner[y:y+ph,x:x+pw]!=p['nr']]=0
   tx,ty,tw,th=target;fit=myk._premul_resize(cut,(tw*4,th*4));out.alpha_composite(Image.fromarray(fit),((tx+4)*4,(ty+4)*4))
   # The detached painted bubbles keep the original bubble-core placement.
   bubbles=(idx>=220)&(idx<=223)&mask;bb=bbox(bubbles)
   # Bubble cores are only one or two original pixels. Fitting a whole
   # plume stretched the individual bubbles into large floating balls.
   # Register separate bubbles around their original cores instead.
   dist=cv2.distanceTransform((~body).astype('uint8'),cv2.DIST_L2,5)
   count,labels,stats,centers=cv2.connectedComponentsWithStats(bubbles.astype('uint8'),8)
   bubbleparts=parts[1:]
   for j in range(1,count):
    bx,by,bw,bh,ba=map(int,stats[j]);cx,cy=centers[j]
    if not bubbleparts or dist[round(cy),round(cx)]<2:continue
    part=bubbleparts[(j-1)%len(bubbleparts)];x,y,pw,ph=part['boks'];cut=tile[y:y+ph,x:x+pw].copy();cut[owner[y:y+ph,x:x+pw]!=part['nr']]=0
    diameter=min(4,max(bw,bh)+2)*4;fit=myk._premul_resize(cut,(diameter,diameter));out.alpha_composite(Image.fromarray(fit),(round((cx+4)*4-diameter/2),round((cy+4)*4-diameter/2)))
  result=np.array(out);method=('painted splash reuse from costume118_062, fit to original water fragment' if f.name=='costume118_001_idx.png' else method);method=('approved Boston pilot side-view reuse, fit to original distant profile' if f.name=='costume118_180_idx.png' else method);notes=dict(method=method,native=native.name,native_sha256=hashlib.sha256(native.read_bytes()).hexdigest(),source_body_bbox=target,native_body_bbox=p['boks'],source_bubbles_bbox=bb)
 Image.fromarray(result).save(O/hd)
 for source,name in [(O/hd,hd),(f,f.name)]:
  if (B/name).exists():continue
  if source!=O/hd:shutil.copy2(source,O/name)
  tmp=M/(name+'.new');shutil.copy2(source,tmp);os.replace(tmp,M/name)
 records.append(dict(file=hd,pixels=area,**notes,sha256=hashlib.sha256((O/hd).read_bytes()).hexdigest()))
(P/'swim-registration.json').write_text(json.dumps(records,indent=2)+'\n');print(len(records),'swim cells,',len(selected),'painted poses, rest tiny source fragments')
