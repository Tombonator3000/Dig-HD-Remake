import os
from pathlib import Path
from PIL import Image
import numpy as np,cv2,json,os,shutil,hashlib
R=Path(os.environ.get("DIGHD_WORKSPACE",Path.cwd()));M=R/'kandidat-mod/costumes';B=Path('/home/tom/Documents/Codex/2026-10-16-the-dig-hd-remake-sp-rsm/testing/linux-release/AppDir/usr/share/the-dig-hd/mods/gpt/costumes');P=R/'grafikk/rapporter/spillfeil-20261016';O=P/'mod-overrides/costumes';atlas=Image.open(P/'produksjon/probe78-master.png').convert('RGBA');tiles=[];refs=[];receipt=[]
def box(m):
 y,x=np.where(m);return (int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1))
def green(a):
 r,g,b=a[:,:,:3].astype(float).transpose(2,0,1);return (a[:,:,3]>128)&(g>r*1.04)&(g>b*1.02)&(g>60)
for j in range(17):
 im=atlas.crop((round(j%5*atlas.width/5),round(j//5*atlas.height/4),round((j%5+1)*atlas.width/5),round((j//5+1)*atlas.height/4)));im=im.crop(box(np.asarray(im)[:,:,3]>128));tiles.append(im)
 src=Image.open(B/f'costume078_{j:03d}_idx.png').convert('RGBA');refs.append(src)
for cid in range(78,84):
 for f in sorted(B.glob(f'costume{cid:03d}_*_idx.png')):
  c=int(f.stem.split('_')[1]);src=Image.open(f).convert('RGBA');a=np.asarray(src);gm=green(a)
  if gm.sum()<12:continue
  if cid==78:
   k=c;target=box(a[:,:,3]>128)
  else:
   num,lab,stats,cent=cv2.connectedComponentsWithStats(gm.astype('uint8'))
   biggest=1+stats[1:,cv2.CC_STAT_AREA].argmax();anchor=cent[biggest];keep=np.zeros(gm.shape,bool)
   for z in range(1,num):
    if np.linalg.norm(cent[z]-anchor)<28:keep|=lab==z
   gb=box(keep);x0,y0,x1,y1=gb
   # Match the light panels' shape to a native original probe orientation.
   def desc(ar,m):
    x,y,r,b=box(m);patch=ar[y:b,x:r,:3].astype('float32');mask=m[y:b,x:r];patch*=mask[:,:,None];return cv2.resize(patch,(24,24))/255
   q=desc(a,keep);scores=[]
   for ref in refs:
    ra=np.asarray(ref);rm=green(ra);scores.append(float(((desc(ra,rm)-q)**2).mean()))
   k=int(np.argmin(scores));ra=np.asarray(refs[k]);rb=box(ra[:,:,3]>128);rg=box(green(ra));sx=(x1-x0)/max(1,rg[2]-rg[0]);sy=(y1-y0)/max(1,rg[3]-rg[1]);scale=np.clip((sx+sy)/2,.4,2)
   target=(round(x0-(rg[0]-rb[0])*scale),round(y0-(rg[1]-rb[1])*scale),round(x1+(rb[2]-rg[2])*scale),round(y1+(rb[3]-rg[3])*scale))
  name=f.name.replace('_idx','_hd');out=Image.open(B/name).convert('RGBA');px=(out.width//4-src.width)//2;py=(out.height//4-src.height)//2;x,y,r,b=target
  # Replace the probe body and its former glow as one opaque painted sprite.
  area=(max(0,(x+px)*4),max(0,(y+py)*4),min(out.width,(r+px)*4),min(out.height,(b+py)*4));out.paste((0,0,0,0),area)
  t=tiles[k].resize((max(1,(r-x)*4),max(1,(b-y)*4)),Image.Resampling.LANCZOS);out.alpha_composite(t,((x+px)*4,(y+py)*4));out.save(O/name);tmp=M/(name+'.new');shutil.copy2(O/name,tmp);os.replace(tmp,M/name)
  receipt.append({'file':name,'master_slot':k,'original_body_bbox':target,'source_indices_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'matching':'exact original cell' if cid==78 else 'original mint-panel shape and bounds'})
(P/'PROBE-REGISTRATION.json').write_text(json.dumps(receipt,indent=2));print(len(receipt),'probe bodies registered')
