import os
"""Enlarge existing source cells for readable drawing references; no new artwork."""
from pathlib import Path
from PIL import Image
import json,numpy as np
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));P=R/'grafikk/rapporter/restgrafikk-r19-20261016';plans=json.loads((P/'boston118-plans.json').read_text())
for batch in plans:
 n=batch['batch'];out=Image.new('RGBA',(1536,1024),(0,0,0,0))
 for c in batch['cells']:
  im=Image.open(R/'testing/source/costumes'/c['file']).convert('RGBA');a=np.array(im);a[(a[:,:,0]>230)&(a[:,:,2]>230)&(a[:,:,1]<120)]=0;im=Image.fromarray(a);im=im.crop(im.getbbox());factor=min(280/im.width,340/im.height);im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.NEAREST);s=c['slot'];out.alpha_composite(im,(s%4*384+(384-im.width)//2,s//4*512+(512-im.height)//2))
 out.save(P/f'boston118-{n}-enlarged-reference.png')
# The last tiny distant standing profile reuses approved pilot artwork.
import sys
sys.path.insert(0,str(R/'kode/pipeline'))
from dighd import myk
source=np.array(Image.open(R/'grafikk/hovedark/boston.png').convert('RGBA'))[:540,400:670]
owner,labels,parts=myk.parts(source[:,:,3]);part=max(parts,key=lambda v:v['areal']);x,y,w,h=part['boks'];cut=source[y:y+h,x:x+w].copy();cut[owner[y:y+h,x:x+w]!=part['nr']]=0
im=Image.fromarray(cut);im.thumbnail((280,400));out=Image.new('RGBA',(1536,1024));out.alpha_composite(im,((384-im.width)//2,(512-im.height)//2));out.save(P/'boston118-18-master.png')
