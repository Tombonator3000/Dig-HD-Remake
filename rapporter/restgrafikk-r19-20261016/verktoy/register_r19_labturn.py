import os
from pathlib import Path
import sys,json,hashlib,shutil,os
import numpy as np,cv2
from PIL import Image,ImageDraw
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));sys.path.insert(0,str(R/'kode/pipeline'))
from dighd import myk
P=R/'grafikk/rapporter/restgrafikk-r19-20261016';S=R/'testing/source/costumes';B=R/'hd-leveranse/costumes';O=P/'mod-tillegg/costumes';M=R/'kandidat-r19/costumes'
masters={};receipts=[]
for b in json.loads((P/'maggie330-plans.json').read_text()):
 f=P/f'maggie330-{b["batch"]}-master.png'
 if not f.exists():continue
 a=np.array(Image.open(f).convert('RGBA'));H,W=a.shape[:2]
 for c in b['cells']:
  s=c['slot'];y0=round(s*H/3);y1=round((s+1)*H/3);tile=a[y0:y1].copy();owner,lab,parts=myk.parts(tile[:,:,3]);large=[p for p in parts if p['areal']>500];assert large,(f,s)
  keep=np.isin(owner,[p['nr'] for p in large]);tile[~keep]=0;ys,xs=np.where(tile[:,:,3]>=128);box=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)];crop=tile[box[1]:box[3],box[0]:box[2]]
  src=np.array(Image.open(S/c['file']).convert('RGBA'));assert src.shape[:2]==(180,320)
  art=myk._premul_resize(crop,(1280,720));masters[c['file']]=dict(image=art,source=src,native_box=[box[0],box[1]+y0,box[2]-box[0],box[3]-box[1]],native=f.name,sha256=hashlib.sha256(f.read_bytes()).hexdigest())
for n in range(2,59):
 file=f'costume330_{n:03d}_idx.png';target=file.replace('_idx','_hd')
 if (B/target).exists():continue
 key='costume330_006_idx.png' if n<=39 else file
 if key not in masters:continue
 v=masters[key];art=v['image'].copy();src=np.array(Image.open(S/file).convert('RGBA'));flow_used=n<=39 and n!=6
 if flow_used:
  # The rear-view figure does not turn in these phases. Transfer only the
  # original animated stone-surface displacement, keeping head and torso fixed.
  g1=cv2.cvtColor(src[:,:,:3],cv2.COLOR_RGB2GRAY);g2=cv2.cvtColor(v['source'][:,:,:3],cv2.COLOR_RGB2GRAY)
  flow=cv2.calcOpticalFlowFarneback(g1,g2,None,.5,3,21,3,5,1.1,0);flow[40:,:124]=0
  flow=cv2.resize(flow,(1280,720),interpolation=cv2.INTER_CUBIC)*4
  yy,xx=np.mgrid[:720,:1280].astype('float32');art=cv2.remap(art,xx+flow[:,:,0],yy+flow[:,:,1],cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT)
 # Source coverage is an animation layer, including the stone's changing
 # transparency. Smooth its original dither without painting over the gaps.
 mask=(src[:,:,3]>128).astype('float32');coverage=cv2.GaussianBlur(mask,(0,0),.65)
 # Palette entries 186..254 belong to Maggie in this codec-5 sequence.
 # The old pixel silhouette must not clip the newly drawn cheek, nose or
 # fingers. Keep native figure alpha in a padded foreground ownership area;
 # only the animated stone surface uses the source transparency guide.
 indices=np.asarray(Image.open(S/file));person=((indices>=186)&(indices<255)).astype('uint8')
 person=cv2.dilate(person,np.ones((29,29),'uint8'))
 coverage[person>0]=1
 coverage=cv2.resize(coverage,(1280,720),interpolation=cv2.INTER_CUBIC);coverage=np.clip((coverage-.12)/.65,0,1)
 # A narrow source guide prevents cutout drift while retaining native edges.
 guide=cv2.dilate((coverage>.1).astype('uint8'),np.ones((9,9),'uint8'))
 art[:,:,3]=np.minimum(art[:,:,3],np.rint(coverage*255).astype('uint8'));art[guide==0]=0
 canvas=np.zeros((752,1312,4),'uint8');canvas[16:736,16:1296]=art;Image.fromarray(canvas).save(O/target)
 for source,name in [(O/target,target),(S/file,file)]:
  if (B/name).exists():continue
  if source!=O/target:shutil.copy2(source,O/name)
  tmp=M/(name+'.new');shutil.copy2(source,tmp);os.replace(tmp,M/name)
 source_area=int((mask>0).sum()*16);native_coverage=float(((art[:,:,3]>128)&(coverage>.5)).sum()/max(1,(coverage>.5).sum()))
 receipts.append(dict(file=target,representative=key,native=v['native'],native_sha256=v['sha256'],native_box=v['native_box'],source_surface_motion=flow_used,source_coverage=native_coverage,visually_approved_by_tom=False,sha256=hashlib.sha256((O/target).read_bytes()).hexdigest()))
(P/'labturn-registration.json').write_text(json.dumps(receipts,indent=2)+'\n');print(len(receipts),'laboratory turning phases registered')
preview=Image.new('RGB',(1600,1000),(36,45,56));d=ImageDraw.Draw(preview)
for j,n in enumerate([6,14,40,41,42,43,44,47,50,53,56,58]):
 f=O/f'costume330_{n:03d}_hd.png'
 if not f.exists():continue
 im=Image.open(f).convert('RGBA');im.thumbnail((390,290));x=j%4*400;y=j//4*330;preview.paste(im,(x,y+25),im);d.text((x+5,y+5),str(n),fill='white')
preview.save(P/'labturn-registration-preview.png')
