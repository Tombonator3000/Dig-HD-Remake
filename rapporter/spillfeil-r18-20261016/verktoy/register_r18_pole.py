from pathlib import Path
from PIL import Image
import numpy as np,cv2,json,shutil,os
from scipy.ndimage import distance_transform_edt,gaussian_filter
R=Path(__file__).resolve().parent;P=R/'grafikk/rapporter/spillfeil-r18-20261016';O=P/'mod-overrides/costumes';M=R/'kandidat-r18/costumes';B=R/'hd-integrert/costumes';S=R/'testing/source/costumes'
def box(m):
 y,x=np.where(m);return (int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1))
def norm(im):
 a=np.asarray(im);m=(a[:,:,3]>128)&~((a[:,:,0]>180)&(a[:,:,2]>150)&(a[:,:,1]<100));a=a.copy();a[~m,3]=0;t=Image.fromarray(a).crop(box(m)).resize((32,32),Image.Resampling.BILINEAR);q=np.asarray(t).astype(float)/255;return q[:,:,:3]*q[:,:,3,None]
A=json.loads((R/'testing/r17-anims.json').read_text());master=Image.open(R/'grafikk/rapporter/spillfeil-20261016/produksjon/boston-heads.png').convert('RGBA');tiles={};refs={}
for row in range(3):
 for di in range(8):
  t=master.crop((round(di*master.width/8),round(row*master.height/3),round((di+1)*master.width/8),round((row+1)*master.height/3)));tiles[row,di]=t.crop(box(np.asarray(t)[:,:,3]>128))
for a in A['14']['animasjoner']:
 if a['animasjon']==1 and a['lag']==1:refs[a['retning']]=norm(Image.open(B/f"costume014_{a['ruter'][-1]:03d}_idx.png").convert('RGBA'))
def main_component(mask):
 n,labels,stats,_=cv2.connectedComponentsWithStats(mask.astype('uint8'),8)
 if n<2:return mask
 return labels==1+int(stats[1:,cv2.CC_STAT_AREA].argmax())
rows=[]
for f in sorted(S.glob('costume178_*_idx.png')):
 s=np.asarray(Image.open(f).convert('RGBA')).copy();h,w=s.shape[:2];c=int(f.stem.split('_')[1]);a=s[:,:,:3].astype(float);rr,gg,bb=a.transpose(2,0,1);valid=(s[:,:,3]>128)&~((rr>180)&(bb>150)&(gg<100));pole=valid&(rr>gg*2)&(bb>gg*.62)&(rr>45);actor=valid&~pole
 if not actor.any():continue
 shirt=actor&(bb>rr*.9)&(bb>gg*.9)&(a.max(2)<115)&(a.max(2)>20)
 pants=actor&(rr>gg*1.5)&(gg>bb*1.7)&(gg>25)
 name=f.name.replace('_idx','_hd');old=Image.open(B/name).convert('RGBA');out=Image.new('RGBA',old.size);pad=((old.width//4-w)//2,(old.height//4-h)//2)
 if h<=23 and w<=27:
  sb=box(actor);scores={di:float(((norm(Image.fromarray(s))-q)**2).mean()) for di,q in refs.items()};di=min(scores,key=scores.get);row=1 if c not in [7,13] else 0;t=tiles[row,di].resize(((sb[2]-sb[0])*4,(sb[3]-sb[1])*4),Image.Resampling.LANCZOS);out.alpha_composite(t,((sb[0]+pad[0])*4,(sb[1]+pad[1])*4));kind='independent_head'
 else:
  if not shirt.any():continue
  shirt=main_component(shirt);sy=box(shirt)[1];headless=sy<4;srcbody=actor.copy();srcbody[:sy]=False;sb=box(srcbody)
  hd=np.asarray(old).copy();hr,hg,hb=hd[:,:,:3].astype(float).transpose(2,0,1);hp=(hd[:,:,3]>64)&(hr>hg*1.9)&(hb>hg*.62)&(hr>45)&(hb<hr*.8);hp=main_component(hp);hv=(hd[:,:,3]>128)&~hp;hs=hv&(hb>hr*.9)&(hb>hg*.9)&(hd[:,:,:3].max(2)<115)&(hd[:,:,:3].max(2)>20)
  if not hs.any():continue
  hs=main_component(hs);hy=box(hs)[1];hue=cv2.cvtColor(np.asarray(old)[:,:,:3],cv2.COLOR_RGB2HSV)[:,:,0];bodymask=hv&(((hr>hg*1.12)&(hg>hb*1.1)&(hue>8))|hs);bodymask[:hy]=False;bodymask=main_component(cv2.morphologyEx(bodymask.astype('uint8'),cv2.MORPH_CLOSE,np.ones((9,9),np.uint8))>0);bx,by,br,bbottom=box(bodymask);hbbox=(max(0,bx-3),hy,min(hd.shape[1],br+3),min(hd.shape[0],bbottom+8));hd[hp,3]=0;hd[:hy,:,3]=0;body=Image.fromarray(hd).crop(hbbox).resize(((sb[2]-sb[0])*4,(sb[3]-sb[1])*4),Image.Resampling.LANCZOS)
  # Register the tool separately: the long pole must never control actor scale.
  if pole.sum()>5 and hp.sum()>10:
   pb=box(pole);hpbox=box(hp);tool=np.asarray(old).copy();tool[~hp,3]=0;t=Image.fromarray(tool).crop(hpbox).resize(((pb[2]-pb[0])*4,(pb[3]-pb[1])*4),Image.Resampling.LANCZOS)
   ta=np.asarray(t).copy();good=(ta[:,:,3]>128).astype('uint8');_,lab=cv2.distanceTransformWithLabels(1-good,cv2.DIST_L2,5,labelType=cv2.DIST_LABEL_PIXEL);yy,xx=np.where(good);lut=np.stack([yy,xx],1);near=lut[np.maximum(lab-1,0)];ta[:,:,:3]=ta[near[:,:,0],near[:,:,1],:3]
   # Carry each painted shaft column along the source curve, avoiding
   # sampling transparent corners of the old, differently sloped tool.
   pm=pole[pb[1]:pb[3],pb[0]:pb[2]];targetmask=cv2.resize(pm.astype('float32'),(ta.shape[1],ta.shape[0]),interpolation=cv2.INTER_CUBIC);yygrid,xxgrid=np.mgrid[:ta.shape[0],:ta.shape[1]].astype('float32');weights=good.astype(float);oldcenter=(weights*yygrid).sum(0)/np.maximum(weights.sum(0),1);oldradius=np.maximum(weights.sum(0)/2,1);targetweights=np.clip(targetmask,0,1);targetcenter=(targetweights*yygrid).sum(0)/np.maximum(targetweights.sum(0),1);targetradius=np.maximum(targetweights.sum(0)/2,1);my=(oldcenter[None,:]+(yygrid-targetcenter[None,:])*oldradius[None,:]/targetradius[None,:]).astype('float32');ta[:,:,:3]=cv2.GaussianBlur(cv2.remap(ta[:,:,:3],xxgrid,my,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE),(0,0),1.3)
   pm=pole[pb[1]:pb[3],pb[0]:pb[2]];signed=gaussian_filter(distance_transform_edt(pm)-distance_transform_edt(~pm),.85);al=np.clip(cv2.resize(signed,(ta.shape[1],ta.shape[0]),interpolation=cv2.INTER_CUBIC)*4+1.5,0,1);ta[:,:,3]=np.rint(al*255).astype('uint8');out.alpha_composite(Image.fromarray(ta),((pb[0]+pad[0])*4,(pb[1]+pad[1])*4))
  out.alpha_composite(body,((sb[0]+pad[0])*4,(sb[1]+pad[1])*4))
  if not headless:
   headmask=actor&~((bb>rr*.9)&(bb>gg*.9)&(a.max(2)<115));headmask[sy+1:]=False;headmask=main_component(headmask);hx,hy0,hx2,hy2=box(headmask);ha=s.copy();ha[~headmask,3]=0;head=Image.fromarray(ha).crop((hx,hy0,hx2,hy2));scores={di:float(((norm(head)-q)**2).mean()) for di,q in refs.items()};warm=((rr>gg*1.15)&(gg>bb*1.1)&headmask).sum();grey=((np.abs(rr-gg)<20)&(bb>rr*.8)&headmask).sum();allowed=[2,3,4,5,6] if warm>grey*.75 else [0,1,7];di=min(allowed,key=scores.get);oa=np.asarray(out).copy();or_,og,ob=oa[:,:,:3].astype(float).transpose(2,0,1);oy,ox=np.mgrid[:out.height,:out.width];neck=(or_>og*1.12)&(og>ob*1.1)&(oy>=(sy+pad[1])*4)&(oy<(sy+3+pad[1])*4)&(ox>=(hx-1+pad[0])*4)&(ox<(hx2+1+pad[0])*4);oa[neck,3]=0;out=Image.fromarray(oa);t=tiles[0,di].resize(((hx2-hx)*4,(hy2-hy0+2)*4),Image.Resampling.LANCZOS);split=round(t.height*.7);full=Image.new('RGBA',(t.width,t.height+4));full.alpha_composite(t.crop((0,0,t.width,split)),(0,0));full.alpha_composite(t.crop((0,split,t.width,t.height)).resize((t.width,t.height-split+4),Image.Resampling.BICUBIC),(0,split));out.alpha_composite(full,((hx+pad[0])*4,(hy0+pad[1])*4))
  kind='headless_body' if headless else 'body_with_approved_head'
 out.save(O/name);temp=M/(name+'.new');shutil.copy2(O/name,temp);os.replace(temp,M/name);rows.append({'file':name,'kind':kind,'source_actor_bbox':box(actor),'source_shirt_top':int(sy) if kind!='independent_head' else None,'separate_pole_registration':bool(pole.sum()>5),'approved_head_atlas':'spillfeil-20261016/produksjon/boston-heads.png'})
(P/'POLE-REGISTRATION.json').write_text(json.dumps(rows,indent=2));print(len(rows),'registered')
