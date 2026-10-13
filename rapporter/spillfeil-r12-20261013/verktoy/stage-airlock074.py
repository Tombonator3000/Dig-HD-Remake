from pathlib import Path
from PIL import Image
import numpy as np, json, hashlib, shutil
R=Path(__file__).resolve().parent
P=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk/rapporter/spillfeil-r12-20261013')
source=R/'original-all/costumes/costume074_004.png'
idx=source.with_name('costume074_004_idx.png')
master=P/'produksjon/airlock074-004-master.png'
if not master.exists():
    shutil.copy2('/home/tombonator3000t/.codex/generated_images/01a136b7-4ca2-7bf3-b336-fe7005243b88/exec-f94ab81c-6d13-4cdc-91ec-53dea18d4696.png',master)
src=Image.open(source).convert('RGBA'); paint=Image.open(master).convert('RGBA')
# Register the complete generated sprite canvas to the complete original cel.
# Only resize and add transparent runtime margins; do not repaint missing art.
w,h=src.size
hd=Image.new('RGBA',((w+8)*4,(h+8)*4))
hd.alpha_composite(paint.resize((w*4,h*4),Image.Resampling.LANCZOS),(16,16))
for out in (P/'mod-overrides/costumes',R/'AppDir/usr/share/the-dig-hd/mods/gpt/costumes'):
    out.mkdir(parents=True,exist_ok=True)
    hd.save(out/'costume074_004_hd.png')
    shutil.copy2(idx,out/idx.name)
a=np.asarray(src.getchannel('A'))>127
b=np.asarray(paint.getchannel('A').resize(src.size,Image.Resampling.BOX))>127
report={'costume':74,'cel':4,'source_size':[w,h],'hd_size':list(hd.size),'registration':'full canvas, scale4, transparent margin4 original pixels each side','source_alpha_iou':float((a&b).sum()/(a|b).sum()),'source_indices_preserved':True,'only_cel4_added':True,'other_mask_cels_unchanged':True,'sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (source,idx,master,P/'mod-overrides/costumes/costume074_004_hd.png')}}
(P/'AIRLOCK074-REGISTRERING.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
