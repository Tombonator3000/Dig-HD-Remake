from pathlib import Path
from PIL import Image
import numpy as np,json,shutil
from dighd.myk import technical
R=Path('.');P=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk/rapporter/spillfeil-r12-20261013');O=P/'mod-overrides/costumes';M=R/'AppDir/usr/share/the-dig-hd/mods/gpt/costumes';plans=json.load(open('action-plans.json'));meta=json.load(open('original-all/costumes.json'));records=[]
for label,entries in plans.items():
 for e in entries:
  atlas=Image.open(P/'produksjon'/f'{label}-{e["batch"]}-master.png').convert('RGBA');j=e['cell'];tile=atlas.crop(((j%6)*256,(j//6)*256,(j%6+1)*256,(j//6+1)*256));a=np.asarray(tile);ys,xs=np.where(a[:,:,3]>100);assert len(xs)>50,(label,j);box=(int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1);cut=tile.crop(box)
  for name in e['members']:
   src=Image.open(R/'context'/(name+'.png')).convert('RGBA');ar=np.asarray(src);mask=(ar[:,:,3]>0)&~technical(ar);ys,xs=np.where(mask);sb=(int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1);w,h=src.size;out=Image.new('RGBA',((w+8)*4,(h+8)*4));out.alpha_composite(cut.resize(((sb[2]-sb[0])*4,(sb[3]-sb[1])*4),Image.Resampling.LANCZOS),((sb[0]+4)*4,(sb[1]+4)*4));out.save(O/(name+'_hd.png'));shutil.copy2(R/'context'/(name+'_idx.png'),O/(name+'_idx.png'))
   for suf in ['_hd.png','_idx.png']:shutil.copy2(O/(name+suf),M/(name+suf))
   records.append({'costume_cel':name,'master':f'{label}-{e["batch"]}-master.png','cell':j,'source_box':sb,'atlas_box':box,'source_indices_preserved':True})
# Remaining Boston cels are optical masks or one-pixel timing markers. The
# decoder now preserves their actual shading; never paint them as solid blobs.
for c in meta['158']['cels']:
 name=f'costume158_{c["cel"]:03d}'
 if any(r['costume_cel']==name for r in records):continue
 w,h=c['w'],c['h'];Image.new('RGBA',((w+8)*4,(h+8)*4)).save(O/(name+'_hd.png'));shutil.copy2(R/'context'/(name+'_idx.png'),O/(name+'_idx.png'))
 for suf in ['_hd.png','_idx.png']:shutil.copy2(O/(name+suf),M/(name+suf))
 records.append({'costume_cel':name,'optical_mask_or_marker':True,'source_indices_preserved':True})
(P/'HANDLINGER-REGISTRERING.json').write_text(json.dumps(records,indent=2));print('Staged',len(records),'action cels')
