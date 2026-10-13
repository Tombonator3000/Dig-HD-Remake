from pathlib import Path
from PIL import Image
import numpy as np,cv2,shutil,json,argparse,hashlib
from scipy.ndimage import gaussian_filter,distance_transform_edt
R=Path('.');G=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk/rapporter/spillfeil-r12-20261013');P=G/'produksjon';O=G/'mod-overrides/costumes';M=R/'AppDir/usr/share/the-dig-hd/mods/gpt/costumes';atlas=Image.open(P/'bryterkrystaller-master.png').convert('RGBA');meta=json.loads((R/'switch-source-metadata.json').read_text());records=[]
args=argparse.ArgumentParser();args.add_argument('--light-miniphases-only',action='store_true');args=args.parse_args()
old=json.loads((G/'BRYTERKRYSTALLER-REGISTRERING.json').read_text()) if args.light_miniphases_only else {}
old_records={(r['costume'],r['cel']):r for r in old.get('cells',[])}
# Explicit audited set of source light phases suppressed by the old width/height rule.
miniphases={120:{0,1,2,3,4,21,27,28,29,31,32,33,35,36,37,42,43,44,45,46,47},146:{0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,27,29,31,32,33,48,49,50},165:{12,13,18,31,32,45,46},185:{26,27,28,29,30},207:{0,1,3,19,22,25,28,35,39}}
light_master=Image.open(P/'energi-enkel-master.png').convert('RGBA').crop((0,0,512,512));phase_records=[]
def light_phase(src,tw,th):
 # The source supplies each light's support, tint and strength; generated light
 # contributes only a restrained soft core inside that support. No new silhouette.
 strength=src[:,:,3]*src[:,:,:3].max(2)
 support=np.clip(gaussian_filter(cv2.resize(np.pad(strength,4),(tw,th),interpolation=cv2.INTER_CUBIC),.7),0,1)
 texture=np.asarray(light_master.resize((tw,th),Image.Resampling.LANCZOS)).astype(np.float32)/255
 alpha=support*(.85+.15*texture[:,:,3])
 rgb=cv2.resize(np.pad(src[:,:,:3]*src[:,:,3,None],((4,4),(4,4),(0,0))),(tw,th),interpolation=cv2.INTER_CUBIC)
 rgb=np.clip(rgb/np.maximum(rgb.max(2,keepdims=True),.002),0,1)
 return Image.fromarray(np.rint(np.clip(np.dstack((rgb,alpha)),0,1)*255).astype(np.uint8))
for col,cid in enumerate([120,146,165,185,207]):
 cells=meta[str(cid)]['cels'];flat=[c for c in cells if 45<c['w']<=80 and 35<c['h']<=70];c0=min(flat,key=lambda c:abs(c['w']/c['h']-1.15));template=np.asarray(Image.open(R/'original/costumes'/f'costume{cid:03d}_{c0["cel"]:03d}.png').convert('RGBA'))[:,:,3].astype(np.float32)/255;fh,fw=template.shape;paints=[]
 for row in range(3):
  x0=round(col*atlas.width/5);x1=round((col+1)*atlas.width/5);y0=round(row*atlas.height/3);y1=round((row+1)*atlas.height/3);im=atlas.crop((x0,y0,x1,y1));a=np.asarray(im);ma=a[:,:,3]>120;ys,xs=np.where(ma);box=(int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1);paints.append(im.crop(box))
 for c in cells:
  if args.light_miniphases_only and c['cel'] not in miniphases[cid]:
   records.append(old_records[cid,c['cel']]);continue
  stem=f'costume{cid:03d}_{c["cel"]:03d}';source=Image.open(R/'original/costumes'/(stem+'.png')).convert('RGBA');src=np.asarray(source).astype(np.float32)/255;h,w=src.shape[:2];tw,th=(w+8)*4,(h+8)*4;out=Image.new('RGBA',(tw,th));technical=not bool(np.any(src[:,:,3]*src[:,:,:3].max(2)>0))
  before=hashlib.sha256((M/(stem+'_hd.png')).read_bytes()).hexdigest() if (M/(stem+'_hd.png')).exists() else None
  if not technical:
   if w<45 or h<30:
    # Thin original optical streaks: emitted light rather than an invented gem.
    out=light_phase(src,tw,th);core=[0,0,w,h]
   else:
    cw,ch=min(fw,w),min(fh,h);tm=cv2.resize(template,(cw,ch),interpolation=cv2.INTER_NEAREST);peak=src[:,:,:3].max(2);score=cv2.matchTemplate((peak*src[:,:,3]-2*(1-src[:,:,3])).astype(np.float32),tm,cv2.TM_CCORR);_,_,_,point=cv2.minMaxLoc(score);cx,cy=point;core=[cx,cy,cw,ch];row=0 if w<=fw+3 and h<=fh+3 else (1 if c['cel']<len(cells)*.68 else 2);paint=paints[row].resize((cw*4,ch*4),Image.Resampling.LANCZOS);a=np.asarray(paint).astype(np.float32)/255
    source_core=src[cy:cy+ch,cx:cx+cw];valid=(source_core[:,:,3]>.5)&(source_core[:,:,:3].max(2)>.035);near=distance_transform_edt(~valid,return_distances=False,return_indices=True);filled=source_core[:,:,:3][tuple(near)];target=cv2.resize(filled,(cw*4,ch*4),interpolation=cv2.INTER_CUBIC);smooth=gaussian_filter(a[:,:,:3],(12,12,0));target_smooth=gaussian_filter(target,(12,12,0));ratio=np.clip((target_smooth+.02)/(smooth+.02),.20,1.5);colour=np.clip(a[:,:,:3]*ratio,0,1);alpha=a[:,:,3];processed=Image.fromarray(np.rint(np.dstack((colour,alpha))*255).astype(np.uint8));out.alpha_composite(processed,((cx+4)*4,(cy+4)*4))
  else:core=None
  out.save(O/(stem+'_hd.png'));shutil.copy2(R/'original/costumes'/(stem+'_idx.png'),O/(stem+'_idx.png'))
  for suf in ['_hd.png','_idx.png']:shutil.copy2(O/(stem+suf),M/(stem+suf))
  records.append({'costume':cid,'cel':c['cel'],'core_rect':core,'technical_only':technical,'source_indices_preserved':True})
  if c['cel'] in miniphases[cid]:phase_records.append({'costume':cid,'cel':c['cel'],'source_size':[w,h],'source_visible_pixels':int((src[:,:,3]>0).sum()),'source_emission_peak':float((src[:,:,3]*src[:,:,:3].max(2)).max()),'hd_visible_pixels':int((np.asarray(out)[:,:,3]>0).sum()),'hd_alpha_max':int(np.asarray(out)[:,:,3].max()),'before_sha256':before,'after_sha256':hashlib.sha256((M/(stem+'_hd.png')).read_bytes()).hexdigest(),'reason':'source light phase, not a technical mask; dimension is not a semantic criterion'})
(G/'BRYTERKRYSTALLER-REGISTRERING.json').write_text(json.dumps({'cells':records,'wall_shadow_not_painted_as_housing':True,'original_timing_unchanged':True},indent=2));print('Switch cells',len(records))
(G/'BRYTER-LYSMINIFASER.json').write_text(json.dumps({'generated_light_master_sha256':hashlib.sha256((P/'energi-enkel-master.png').read_bytes()).hexdigest(),'only_audited_miniphases_changed':args.light_miniphases_only,'cells':phase_records},indent=2))
