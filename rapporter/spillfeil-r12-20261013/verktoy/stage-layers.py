from pathlib import Path
from PIL import Image
import json,shutil,hashlib
from dighd import export
R=Path('.');G=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk/rapporter/spillfeil-r12-20261013');O=G/'mod-overrides/objects';O.mkdir(parents=True,exist_ok=True);M=R/'AppDir/usr/share/the-dig-hd/mods/gpt/objects';export.export_la1(R/'AppDir/usr/share/the-dig-hd/game',R/'original',{15,49,75})
records=[]
for a in json.loads((R/'layer-candidates.json').read_text()):
 o=a['object'];stem=o['bilde']
 if o['objekt']==238:continue
 src=R/'original/objects'/(stem+'.png');idx=R/'original/objects'/(stem+'_idx.png')
 if not src.exists():continue
 x,y,w,h=o['rekt'];im=Image.open(a['result']).convert('RGBA').crop(a['crop']).resize((w*4,h*4),Image.Resampling.LANCZOS);alpha=Image.open(src).convert('RGBA').getchannel('A').resize(im.size,Image.Resampling.NEAREST);im.putalpha(alpha);im.save(O/(stem+'.png'));shutil.copy2(idx,O/idx.name)
 for suffix in ['.png','_idx.png']:shutil.copy2(O/(stem+suffix),M/(stem+suffix))
 records.append({'object':stem,'job':a['job'],'source_result_sha256':hashlib.file_digest(Path(a['result']).open('rb'),'sha256').hexdigest(),'source_indices_preserved':True,'output_size':list(im.size)})
(G/'HULL-LINSER-IMPORT.json').write_text(json.dumps(records,indent=2));print('HD layers imported',len(records))
