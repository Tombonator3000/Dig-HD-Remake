import os
from pathlib import Path
import sys,json,hashlib,shutil,os
import numpy as np,cv2
from PIL import Image,ImageDraw
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));sys.path.insert(0,str(R/'kode/pipeline'))
from dighd import myk
P=R/'grafikk/rapporter/restgrafikk-r19-20261016';S=R/'testing/source/costumes';B=R/'hd-leveranse/costumes';O=P/'mod-tillegg/costumes';M=R/'kandidat-r19/costumes'
masters={};receipts=[];CW,CH=320,182
def canonical(file,art=None):
 im=Image.open(S/file);indices=np.array(im);src=np.array(im.convert('RGBA'));h,w=indices.shape
 person=((indices>=186)&(indices<255)).astype('uint8')
 x=160 if w==160 and person.sum()<1000 else 0;y=CH-h
 assert w in [160,320] and y>=0,(file,w,h)
 rgb=np.zeros((CH,CW,4),'uint8');rgb[y:y+h,x:x+w]=src
 pp=np.zeros((CH,CW),'uint8');pp[y:y+h,x:x+w]=person
 # The palette also contains bright stone highlights. Ownership follows
 # Maggie's original region so the yellow top fragment cannot be mistaken
 # for skin and composited twice with two different generated textures.
 yy,xx=np.mgrid[:CH,:CW]
 figure_region=((xx<150)&(yy>25))|((xx>=140)&(xx<260)&(yy>50)&(yy<125))
 pp[~figure_region]=0
 bounds=np.zeros((CH,CW),'uint8');bounds[y:y+h,x:x+w]=1
 if w==160:
  # Original draw-many frames assemble these pairs. Build the same complete
  # source field before motion estimation for either half, so the shared arm
  # and stone cannot receive different displacement at their join.
  pairs={24:25,25:24,30:31,31:30,41:42,42:41};n=int(file.split('_')[1]);other=Image.open(S/f'costume331_{pairs[n]:03d}_idx.png');oi=np.array(other);oa=np.array(other.convert('RGBA'));oh,ow=oi.shape;ox=160-x;oy=CH-oh;assert ow==160
  rgb[oy:oy+oh,ox:ox+ow]=oa
  op=((oi>=186)&(oi<255)).astype('uint8');op_full=np.zeros((CH,CW),'uint8');op_full[oy:oy+oh,ox:ox+ow]=op;op_full[~figure_region]=0;pp|=op_full
 ca=None
 if art is not None:
  ca=np.zeros((CH*4,CW*4,4),'uint8');ca[y*4:(y+h)*4,x*4:(x+w)*4]=art
 return dict(source=rgb,person=pp,bounds=bounds,offset=[x,y],size=[w,h],image=ca)
def ownership(person):
 return cv2.resize(cv2.dilate(person,np.ones((29,29),'uint8')),(CW*4,CH*4),interpolation=cv2.INTER_NEAREST)
def warp(art,source,target,keep_cropped_bottom=False):
 g1=cv2.GaussianBlur(cv2.cvtColor(target[:,:,:3],cv2.COLOR_RGB2GRAY),(0,0),.6)
 g2=cv2.GaussianBlur(cv2.cvtColor(source[:,:,:3],cv2.COLOR_RGB2GRAY),(0,0),.6)
 flow=cv2.calcOpticalFlowFarneback(g1,g2,None,.5,3,19,3,5,1.1,0)
 flow=np.clip(flow,-3,3);flow=cv2.resize(flow,(CW*4,CH*4),interpolation=cv2.INTER_CUBIC)*4
 yy,xx=np.mgrid[:CH*4,:CW*4].astype('float32')
 sy=yy+flow[:,:,1]
 if keep_cropped_bottom:sy=np.minimum(sy,CH*4-1)
 return cv2.remap(art,xx+flow[:,:,0],sy,cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT)
for b in json.loads((P/'maggie331-plans.json').read_text()):
 f=P/f'maggie331-{b["batch"]}-master.png'
 if not f.exists():continue
 a=np.array(Image.open(f).convert('RGBA'));H,W=a.shape[:2]
 for c in b['cells']:
  s=c['slot'];y0=round(s*H/3);y1=round((s+1)*H/3);tile=a[y0:y1].copy();owner,lab,parts=myk.parts(tile[:,:,3]);large=[p for p in parts if p['areal']>500];assert large,(f,s)
  keep=np.isin(owner,[p['nr'] for p in large]);tile[~keep]=0;ys,xs=np.where(tile[:,:,3]>=128);box=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)];crop=tile[box[1]:box[3],box[0]:box[2]]
  src=np.array(Image.open(S/c['file']).convert('RGBA'));assert list(src.shape[1::-1])==c['source_size']
  art=myk._premul_resize(crop,(src.shape[1]*4,src.shape[0]*4));v=canonical(c['file'],art)
  # A taller stone fragment can extend the whole drawing's bounding box
  # below the cropped torso. Fit the attached figure to its original lower
  # edge separately; otherwise a correctly sized whole cel cuts the shirt
  # above the viewport edge. Head and torso receive the same small transform.
  ca=v['image'];yy,xx=np.mgrid[:CH*4,:CW*4];rgb=ca[:,:,:3].astype('int16')
  warm=(rgb[:,:,0]>rgb[:,:,1]*1.25)&(rgb[:,:,2]<rgb[:,:,1]*.85)
  white=(rgb.min(2)>100)&((rgb.max(2)-rgb.min(2))<35)
  clothing=(ca[:,:,3]>128)&(xx<115*4)&(yy>120*4)&(warm|white)
  v['has_figure']=bool(clothing.any());v['figure']=ca.copy();v['figure_vertical_scale']=1.
  if clothing.any():
   bottom=int(np.where(clothing)[0].max());anchor=20*4;factor=(CH*4-1-anchor)/max(1,bottom-anchor)
   assert .96<factor<1.12,(c['file'],factor,bottom)
   transform=np.array([[1,0,0],[0,factor,anchor*(1-factor)]],dtype='float32')
   v['figure']=cv2.warpAffine(ca,transform,(CW*4,CH*4),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT);v['figure_vertical_scale']=factor
  v.update(native_box=[box[0],box[1]+y0,box[2]-box[0],box[3]-box[1]],native=f.name,sha256=hashlib.sha256(f.read_bytes()).hexdigest());masters[c['file']]=v
background_key=json.loads((P/'maggie331-plans.json').read_text())[5]['cells'][0]['file']
background=masters[background_key];stone=background['image'].copy()
for n in range(52):
 file=f'costume331_{n:03d}_idx.png';target=file.replace('_idx','_hd')
 if (B/target).exists():continue
 current=canonical(file);src=current['source'];bounds=current['bounds'];person=current['person'];scores={}
 for key,v in masters.items():
  if not v['has_figure']:continue
  # Original mouth and eye poses select an already drawn expression.
  # Evaluate only the target part's bounds; a cropped arm is never completed.
  weights=(np.maximum(person,v['person'])*3+.1)*bounds
  weights[76:130,65:135]*=6
  delta=(src[:,:,:3].astype('float32')-v['source'][:,:,:3])**2
  scores[key]=float((delta.mean(2)*weights).sum()/max(weights.sum(),1))
 key=min(scores,key=scores.get);v=masters[key]
 foreground=warp(v['figure'],v['source'],src,keep_cropped_bottom=True)
 # The same painted stone material is used throughout the dialogue. Only
 # source displacement and coverage vary, so its texture cannot jump between
 # independently generated frames. No original face pixels are composited.
 backdrop=warp(stone,background['source'],src)
 # The right arm keeps the same pointing pose throughout this dialogue.
 # Keep it and the stone from one painted state; blend the expression and
 # attached torso in a short shoulder seam. Both halves then share one arm
 # and one background at the engine's 160-pixel assembly boundary.
 own=ownership(person).astype('float32')
 feather=np.clip((152-np.arange(CW*4)/4)/10,0,1).astype('float32')
 blend=own*feather[None,:];fa=foreground[:,:,3].astype('float32')/255;ba=backdrop[:,:,3].astype('float32')/255
 alpha=fa*blend+ba*(1-blend)
 premul=foreground[:,:,:3]*fa[:,:,None]*blend[:,:,None]+backdrop[:,:,:3]*ba[:,:,None]*(1-blend[:,:,None])
 art=np.zeros_like(foreground);art[:,:,:3]=np.clip(premul/np.maximum(alpha[:,:,None],1e-6),0,255).astype('uint8');art[:,:,3]=np.rint(alpha*255).astype('uint8');flow_used=True
 # Source coverage is an animation layer, including the stone's changing
 # transparency. Smooth its original dither without painting over the gaps.
 mask=(src[:,:,3]>128).astype('float32');coverage=cv2.GaussianBlur(mask,(0,0),.65)
 # Palette entries 186..254 belong to Maggie in this codec-5 sequence.
 # The old pixel silhouette must not clip the newly drawn cheek, nose or
 # fingers. Keep native figure alpha in a padded foreground ownership area;
 # only the animated stone surface uses the source transparency guide.
 person=cv2.dilate(person,np.ones((29,29),'uint8'))
 coverage[person>0]=1
 coverage=cv2.resize(coverage,(src.shape[1]*4,src.shape[0]*4),interpolation=cv2.INTER_CUBIC);coverage=np.clip((coverage-.12)/.65,0,1)
 # A narrow source guide prevents cutout drift while retaining native edges.
 guide=cv2.dilate((coverage>.1).astype('uint8'),np.ones((9,9),'uint8'))
 art[:,:,3]=np.minimum(art[:,:,3],np.rint(coverage*255).astype('uint8'));art[guide==0]=0
 x,y=current['offset'];w,h=current['size'];art=art[y*4:(y+h)*4,x*4:(x+w)*4];coverage=coverage[y*4:(y+h)*4,x*4:(x+w)*4]
 canvas=np.zeros(((h+8)*4,(w+8)*4,4),'uint8');canvas[16:-16,16:-16]=art;Image.fromarray(canvas).save(O/target)
 for source,name in [(O/target,target),(S/file,file)]:
  if (B/name).exists():continue
  if source!=O/target:shutil.copy2(source,O/name)
  tmp=M/(name+'.new');shutil.copy2(source,tmp);os.replace(tmp,M/name)
 source_area=int((mask>0).sum()*16);native_coverage=float(((art[:,:,3]>128)&(coverage>.5)).sum()/max(1,(coverage>.5).sum()))
 receipts.append(dict(file=target,representative=key,native=v['native'],native_sha256=v['sha256'],native_box=v['native_box'],figure_vertical_scale=v['figure_vertical_scale'],shared_stone=background_key,canonical_offset=current['offset'],source_motion_limit_pixels=3,expression_source_score=scores[key],source_surface_motion=flow_used,source_coverage=native_coverage,visually_approved_by_tom=False,sha256=hashlib.sha256((O/target).read_bytes()).hexdigest()))
(P/'labtalk-registration.json').write_text(json.dumps(receipts,indent=2)+'\n');print(len(receipts),'laboratory dialogue parts registered')
preview=Image.new('RGB',(1600,1000),(36,45,56));d=ImageDraw.Draw(preview)
for j,n in enumerate([0,42,41,40,39,38,35,33,11,14,32,51]):
 f=O/f'costume331_{n:03d}_hd.png'
 if not f.exists():continue
 im=Image.open(f).convert('RGBA');im.thumbnail((390,290));x=j%4*400;y=j//4*330;preview.paste(im,(x,y+25),im);d.text((x+5,y+5),str(n),fill='white')
preview.save(P/'labtalk-registration-preview.png')
