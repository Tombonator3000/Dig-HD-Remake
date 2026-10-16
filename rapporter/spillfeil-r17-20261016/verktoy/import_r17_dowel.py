from pathlib import Path
from PIL import Image
import numpy as np,shutil,os
R=Path(__file__).resolve().parent;P=R/'grafikk/rapporter/spillfeil-r17-20261016';M=R/'kandidat-r17';O=P/'mod-overrides/objects';master=P/'produksjon/dowel-master.png';shutil.copy2('/home/tom/.codex/generated_images/01a143a5-2c2d-7dc3-9827-943c3e7c6e0e/exec-a1cb5438-0a1b-458c-b9c1-f25ecab55b73.png',master)
t=Image.open(master).convert('RGBA');a=np.asarray(t)[:,:,3];y,x=np.where(a>128);t=t.crop((x.min(),y.min(),x.max()+1,y.max()+1)).resize((72,24),Image.Resampling.LANCZOS)
# Object includes its stair background. Restore the corresponding HD stone
# before placing the removable peg inside the unchanged original rectangle.
bg=Image.open(M/'rooms/room068.png').convert('RGBA').crop((512*4,88*4,536*4,96*4));bg.alpha_composite(t,(12,4));name='obj474_01.png';bg.save(O/name);temp=M/'objects'/(name+'.new');shutil.copy2(O/name,temp);os.replace(temp,M/'objects'/name)
print('dowel registered within original 24x8 object')
