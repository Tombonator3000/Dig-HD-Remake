from pathlib import Path
from PIL import Image
import numpy as np,cv2,json,shutil
from scipy.ndimage import gaussian_filter
R=Path('.');P=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk/rapporter/spillfeil-r12-20261013');O=P/'mod-overrides/costumes';M=R/'AppDir/usr/share/the-dig-hd/mods/gpt/costumes';records=[]
for plan in json.load(open('energy-phase-plan.json')):
 im=Image.open(P/'produksjon'/(plan['name']+'-master.png')).convert('RGBA');cw=im.width/plan['cols'];ch=im.height/plan['rows']
 for j,c in enumerate(plan['cells']):
  cid=plan['costume'];stem=f'costume{cid:03d}_{c["cel"]:03d}';src=Image.open(R/'context'/(stem+'.png')).convert('RGBA');w,h=src.size;tile=im.crop((round(j%plan['cols']*cw),round(j//plan['cols']*ch),round((j%plan['cols']+1)*cw),round((j//plan['cols']+1)*ch)));ar=np.asarray(tile);ys,xs=np.where(ar[:,:,3]>55)
  if not len(xs):raise RuntimeError(stem+' empty')
  box=(int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1);b=c['source_bbox'];cut=tile.crop(box).resize(((b[2]-b[0])*4,(b[3]-b[1])*4),Image.Resampling.LANCZOS)
  # Source geometry bounds all components. Glow is permitted only close to the
  # original contours, preserving gaps and preventing detached components.
  ca=np.asarray(cut).copy();support=np.array(src.getchannel('A').crop(b).resize(cut.size,Image.Resampling.LANCZOS))/255;support=np.clip(gaussian_filter(support,1.0)*1.5,0,1);ca[:,:,3]=(ca[:,:,3]*support*(0.55 if cid==35 else 1.0)).astype(np.uint8)
  out=Image.new('RGBA',((w+8)*4,(h+8)*4));out.alpha_composite(Image.fromarray(ca),((b[0]+4)*4,(b[1]+4)*4));out.save(O/(stem+'_hd.png'));shutil.copy2(R/'original-all/costumes'/(stem+'_idx.png'),O/(stem+'_idx.png'))
  for suff in ['_hd.png','_idx.png']:shutil.copy2(O/(stem+suff),M/(stem+suff))
  records.append({'costume':cid,'cel':c['cel'],'master':plan['name'],'cell':j,'source_bbox':b,'paint_bbox':box,'exact_source_cel':True})
# Never swap random light designs as frame counters change. All earlier tiny
# pulsating orbs and thin rays use one stable master per source animation family.
(P/'ENERGI-FASE-REGISTRERING.json').write_text(json.dumps(records,indent=2));print('phase-specific energy cells',len(records))
