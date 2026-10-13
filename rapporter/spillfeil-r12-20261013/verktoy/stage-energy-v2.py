from pathlib import Path
from PIL import Image
import numpy as np,cv2,shutil,json
from scipy.ndimage import gaussian_filter
R=Path('.');P=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk/rapporter/spillfeil-r12-20261013');O=P/'mod-overrides/costumes';M=R/'AppDir/usr/share/the-dig-hd/mods/gpt/costumes';atlas=Image.open(P/'produksjon/energi-enkel-master.png').convert('RGBA');meta=json.load(open('original-all/costumes.json'));records=[];tiles=[]
for j in range(6):
 im=atlas.crop((j%3*512,j//3*512,(j%3+1)*512,(j//3+1)*512));ar=np.asarray(im);ys,xs=np.where(ar[:,:,3]>40);box=(int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1);tiles.append(im.crop(box))
for cid in [32,35,96,145,152,168,175,206]:
 for c in meta[str(cid)]['cels']:
  stem=f'costume{cid:03d}_{c["cel"]:03d}';src=np.asarray(Image.open(R/'original-all/costumes'/(stem+'.png')).convert('RGBA')).astype(np.float32)/255;h,w=src.shape[:2];live=src[:,:,3];peak=src[:,:,:3].max(2);technical=(live>0).sum()<3 or (w<=2 and h<=2);out=Image.new('RGBA',((w+8)*4,(h+8)*4))
  if not technical:
   ys,xs=np.where((live>.01)&(peak>.06));
   if len(xs):
    x0,y0,x1,y1=int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1;bw,bh=x1-x0,y1-y0
    if cid==175:j=5
    elif cid==35 and c['cel']>=200:j=4 if bh>bw*1.5 else 0
    elif bw>bh*2:j=3
    elif bh>bw*2:j=4
    else:j=0
    paint=np.asarray(tiles[j].resize((bw*4,bh*4),Image.Resampling.LANCZOS)).astype(np.float32)/255
    # Thin generated light, with the source's position, bounds and timing.
    # Brightness is phase-driven, not an opaque fill over the whole old mask.
    detail=paint[:,:,:3];light=detail.max(2);rgb=np.clip(detail/np.maximum(light[:,:,None],.02),0,1);alpha=paint[:,:,3]*(.35+.55*light)
    if cid not in [35,175]:
     strength=live[y0:y1,x0:x1]*np.clip((peak[y0:y1,x0:x1]-.05)/.45,0,1);support=cv2.resize(strength,(bw*4,bh*4),interpolation=cv2.INTER_CUBIC);support=np.clip(gaussian_filter(support,1.0),0,1);alpha*=support
    else:
     phase=float(np.quantile(peak[live>.1],.85));alpha*=min(1.,.45+phase*.65)
    out.alpha_composite(Image.fromarray(np.rint(np.clip(np.dstack((rgb,alpha)),0,1)*255).astype(np.uint8)),((x0+4)*4,(y0+4)*4))
  out.save(O/(stem+'_hd.png'));shutil.copy2(R/'original-all/costumes'/(stem+'_idx.png'),O/(stem+'_idx.png'))
  for suf in ['_hd.png','_idx.png']:shutil.copy2(O/(stem+suf),M/(stem+suf))
  records.append({'costume':cid,'cel':c['cel'],'technical_only':bool(technical),'original_size':[w,h],'original_position_timing_preserved':True})
(P/'ENERGI-REGISTRERING.json').write_text(json.dumps({'cells':records,'art':'energi-enkel-master.png','user_request':'simple translucent ethereal light and crystal-shaped energy; no people, clothes, UFO or structures'},indent=2));print('energy',len(records))
