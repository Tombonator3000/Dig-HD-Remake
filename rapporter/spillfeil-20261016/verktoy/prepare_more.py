import os
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
R=Path(os.environ.get("DIGHD_WORKSPACE",Path.cwd()));P=R/'grafikk/rapporter/spillfeil-20261016/produksjon';M=R/'kandidat-mod'
out=Image.new('RGBA',(1500,1200));d=ImageDraw.Draw(out)
for j,f in enumerate(sorted((M/'costumes').glob('costume078_*_idx.png'))):
 im=Image.open(f).convert('RGBA');im=im.resize((im.width*6,im.height*6),Image.Resampling.NEAREST);im.thumbnail((260,260));out.alpha_composite(im,(j%5*300+(300-im.width)//2,j//5*300+(300-im.height)//2))
out.save(P/'probe78-reference.png')
f=Image.open(R/'testing/icons-map.png');f.crop((0,2800,1400,3800)).save(R/'testing/icon-crop.png')
