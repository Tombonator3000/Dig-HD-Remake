"""Source phase175 consists of adjacent 256px and25px strips, not two forms.

Run after stage-energy-phases.py. Preserve exact cel offsets and source index
maps; normalize one newly generated full-width master then split at source256.
"""
from pathlib import Path
from PIL import Image
import numpy as np
import json, hashlib, shutil

R=Path(__file__).resolve().parent
P=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk/rapporter/spillfeil-r12-20261013')
O=P/'mod-overrides/costumes'
M=R/'AppDir/usr/share/the-dig-hd/mods/gpt/costumes'
master=P/'produksjon/energy175-samlet-master.png'
paint=Image.open(master).convert('RGBA')
# Full canvas aspect1746:901 equals the source281:145, within rounding. Do not
# crop or stretch the old partial256px painting. The new complete master was
# explicitly generated from the reconstructed281px source and actual room65.
assert abs(paint.width/paint.height-281/145)<0.002
full=paint.resize((281*4,145*4),Image.Resampling.LANCZOS)
registration=[]
def save(cel,out,method,master_path=master):
    stem=f'costume175_{cel:03d}'
    out.save(O/(stem+'_hd.png'))
    shutil.copy2(R/'original-all/costumes'/(stem+'_idx.png'),O/(stem+'_idx.png'))
    for suffix in ['_hd.png','_idx.png']:
        shutil.copy2(O/(stem+suffix),M/(stem+suffix))
    registration.append({'costume':175,'cel':cel,'method':method,'master':str(master_path),'hd_sha256':hashlib.sha256((O/(stem+'_hd.png')).read_bytes()).hexdigest(),'source_cel':str(R/'context'/(stem+'.png'))})

for cel,left,width in [(0,0,256),(1,256,25)]:
    out=Image.new('RGBA',((width+8)*4,(145+8)*4))
    out.alpha_composite(full.crop((left*4,0,(left+width)*4,145*4)),(16,16))
    save(cel,out,'new full281x145 source-phase master; exact split x256; preserve source placement')

# Pulse13 shares the outline of3 but has a broader/brighter central core.
# Use a dedicated master generated from13, not an unrelated generic diamond.
orbmaster=P/'produksjon/energy175-013-master.png'
orb=Image.open(orbmaster).convert('RGBA').resize((60,44),Image.Resampling.LANCZOS)
out=Image.new('RGBA',(92,76));out.alpha_composite(orb,(16,16))
save(13,out,'new master from source13, preserving brighter broader core and rightward halo',orbmaster)
for cel in [2,14]:
    assert Image.open(R/'context'/f'costume175_{cel:03d}.png').size==(1,1)
    save(cel,Image.new('RGBA',(36,36)),'original1x1 technical blank; transparent HD marker')

info={'source_dimensions':[281,145],'source_runtime_positions':{'0':[24,0],'1':[280,0]},'split_x':256,'generated_master_dimensions':list(paint.size),'master_sha256':hashlib.sha256(master.read_bytes()).hexdigest(),'original_source3_equals13':False,'source3_and13_same_alpha_but_different_core':True,'cells':registration}
(P/'ENERGI175-SAMLET-REGISTRERING.json').write_text(json.dumps(info,indent=2))
rp=P/'ENERGI-FASE-REGISTRERING.json'
records=json.loads(rp.read_text())
ids={0,1,2,13,14}
records=[r for r in records if not (r['costume']==175 and r['cel'] in ids)]
records+=registration
rp.write_text(json.dumps(records,indent=2))
print(json.dumps({'staged':len(registration),'source_dimensions':[281,145],'split_x':256}))
