from pathlib import Path
from PIL import Image
import numpy as np,io
from scipy.ndimage import gaussian_filter
import json,hashlib,shutil
R=Path(__file__).resolve().parent;P=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk/rapporter/spillfeil-r12-20261013');M=R/'AppDir/usr/share/the-dig-hd/mods/gpt';O=P/'mod-overrides';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();stem='obj187_01';before=sha(M/'objects'/(stem+'.png'));room=M/'rooms/room023.png';art=Image.open(room).convert('RGBA').crop((608*4,112*4,648*4,144*4));candidates={}
atlas=Image.open(P/'produksjon/sparks61-base-master.png').convert('RGBA')
for cel,pos in [(1,(623,126)),(0,(624,128))]:
 source=Image.open(R/'original-all/costumes'/f'costume061_{cel:03d}.png').convert('RGBA');w,h=source.size;tile=atlas.crop((0,cel*atlas.height//2,atlas.width,(cel+1)*atlas.height//2));a=np.asarray(tile);ys,xs=np.where(a[:,:,3]>32);box=(int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1));paint=tile.crop(box).resize((w*4,h*4),Image.Resampling.LANCZOS);arr=np.array(paint)
 support=np.asarray(source.getchannel('A').resize((w*4,h*4),Image.Resampling.LANCZOS))/255;support=np.clip(gaussian_filter(support,.65)*1.35,0,1);arr[:,:,3]=np.rint(arr[:,:,3]*support).astype('uint8');im=Image.new('RGBA',((w+8)*4,(h+8)*4));im.alpha_composite(Image.fromarray(arr),(16,16));stream=io.BytesIO();im.save(stream,format='PNG');candidates[f'costume061_{cel:03d}_hd.png']=hashlib.sha256(stream.getvalue()).hexdigest();art.alpha_composite(im,((pos[0]-608-4)*4,(pos[1]-112-4)*4))
mask=R/'sparks61-source/objects'/(stem+'_mask.png');art.putalpha(Image.open(mask).convert('L').resize(art.size,Image.Resampling.NEAREST));art.save(O/'objects'/(stem+'.png'))
for suff in ['_idx.png','_mask.png']:shutil.copy2(R/'sparks61-source/objects'/(stem+suff),O/'objects'/(stem+suff))
for suff in ['.png','_idx.png','_mask.png']:shutil.copy2(O/'objects'/(stem+suff),M/'objects'/(stem+suff))
(P/'SPARKS187-REGISTRERING.json').write_text(json.dumps({'object':stem,'room':23,'source_rect':[608,112,40,32],'source_sha256':sha(R/'sparks61-source/objects'/(stem+'.png')),'source_idx_sha256':sha(R/'sparks61-source/objects'/(stem+'_idx.png')),'exact_smap_mask_sha256':sha(mask),'hd_background_sha256':sha(room),'background_crop':[608*4,112*4,648*4,144*4],'generated_source_cells':candidates,'source_positions':{'costume061_001':[623,126],'costume061_000':[624,128]},'original_mask_preserved':True,'before_sha256':before,'after_sha256':sha(M/'objects'/(stem+'.png')),'finding':'Visible coarse sparks are baked into object187_01; replacing costumes061_000/001 alone yielded pixel-identical runtime frame120. Generated source-faithful base art is therefore composited into the active object layer. Existing room background and exact SMAP coverage determine all other pixels.'},indent=2)+'\n')
print('staged object187',before,'->',sha(M/'objects'/(stem+'.png')))
