from pathlib import Path
from PIL import Image
from dighd import export
import numpy as np,shutil,json
R=Path('.');P=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk/rapporter/spillfeil-r12-20261013');M=R/'AppDir/usr/share/the-dig-hd/mods/gpt';O=P/'mod-overrides/objects';export.export_la1(R/'AppDir/usr/share/the-dig-hd/game',R/'lens-source',{27});S=R/'lens-source/objects';stem='obj238_01';src=Image.open(S/(stem+'.png')).convert('RGBA');a=np.array(src);obj=(a[:,:,2]>a[:,:,0])&(a[:,:,0]>75)&(a[:,:,3]>0);ys,xs=np.where(obj);box=(int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1)
# Refine by all neutral rim pixels touching the documented glass, x7..14/y6..11.
box=(7,6,14,11)
f=Path('/home/tombonator3000t/.codex/generated_images/01a1348c-93eb-7bc3-83cf-edfb9bc273c8/exec-d6bf5e3f-c1c8-49e7-aa39-08518c38c0d6.png');shutil.copy2(f,P/'produksjon/lens238-master.png');art=Image.open(f).convert('RGBA');aa=np.array(art);yy,xx=np.where(aa[:,:,3]>50);cut=art.crop((xx.min(),yy.min(),xx.max()+1,yy.max()+1)).resize(((box[2]-box[0])*4,(box[3]-box[1])*4),Image.Resampling.LANCZOS);back=Image.open(M/'rooms/room027.png').convert('RGBA').crop((168*4,736*4,192*4,752*4));back.alpha_composite(cut,(box[0]*4,box[1]*4));back.putalpha(Image.open(S/(stem+'_mask.png')).resize(back.size,Image.Resampling.NEAREST));back.save(O/(stem+'.png'))
for suff in ['_idx.png','_mask.png']:shutil.copy2(S/(stem+suff),O/(stem+suff))
for suff in ['.png','_idx.png','_mask.png']:shutil.copy2(O/(stem+suff),M/'objects'/(stem+suff))
(P/'LENS238-REGISTRERING.json').write_text(json.dumps({'identity':'optical lens at bottom of power room27, POWERRM.043','object':stem,'source_bbox':box,'exact_smap_coverage':True,'source_indices_preserved':True,'attempts':2,'first_rejected':'pixelated, no HD smooth edges'},indent=2));print(box)
