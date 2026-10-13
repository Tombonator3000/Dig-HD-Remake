from pathlib import Path
from PIL import Image
import json,hashlib,shutil
R=Path(__file__).resolve().parent; G=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk');P=G/'rapporter/spillfeil-r12-20261013';O=P/'mod-overrides/objects';M=R/'AppDir/usr/share/the-dig-hd/mods/gpt/objects';records=[]
for job in ['lag055_01','lag055_02','lag055_03']:
 j=G/'jobber'/job;meta=json.loads((j/'jobb.json').read_text());im=Image.open(j/'resultat.png').convert('RGBA');ox,oy,sw,sh=meta['bilde_i_lerret'];rx,ry,rw,rh=meta['region'];sx=sw/rw;sy=sh/rh
 for obj in meta['objekter']:
  stem=obj['bilde'];x,y,w,h=obj['rekt'];box=(round(ox+(x-rx)*sx),round(oy+(y-ry)*sy),round(ox+(x-rx+w)*sx),round(oy+(y-ry+h)*sy));art=im.crop(box).resize((w*4,h*4),Image.Resampling.LANCZOS);mask=R/'nearest-extract/objects'/(stem+'_mask.png');art.putalpha(Image.open(mask).resize(art.size,Image.Resampling.NEAREST));art.save(O/(stem+'.png'))
  for suffix in ['_idx.png','_mask.png']:shutil.copy2(R/'nearest-extract/objects'/(stem+suffix),O/(stem+suffix))
  for suffix in ['.png','_idx.png','_mask.png']:shutil.copy2(O/(stem+suffix),M/(stem+suffix))
  records.append({'job':job,'object':stem,'crop':box,'source_sha256':hashlib.file_digest((j/'resultat.png').open('rb'),'sha256').hexdigest(),'exact_smap_coverage':True,'original_indices_preserved':True})
(P/'PLATEAU-REGISTRERING.json').write_text(json.dumps(records,indent=2));print(records)
