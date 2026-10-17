import os
"""Select and display original blue tram art anchors, excluding shade masks."""
from pathlib import Path
import json,numpy as np
from PIL import Image
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));P=R/'grafikk/rapporter/restgrafikk-r19-20261016';S=R/'testing/source/costumes';C=R/'kandidat-r19/costumes';data=json.loads((P/'tram-mask-classification.json').read_text());plans=[]
for costume in data['costumes']:
 cid=costume['costume'];art=[c for c in costume['cells'] if c['art_pixels']>=40];missing=[c for c in art if not (C/f'costume{cid:03d}_{c["cel"]:03d}_hd.png').exists()]
 if not missing:continue
 # Eight spread anchors include the first genuine art, largest core,
 # smallest fragment and phases from the entire source sequence.
 candidates=sorted(art,key=lambda c:c['cel']);picked=[]
 for c in [candidates[0],max(art,key=lambda c:c['art_pixels']),min(missing,key=lambda c:c['art_pixels'])]+[candidates[round(i*(len(candidates)-1)/4)] for i in range(1,5)]:
  if c['cel'] not in [v['cel'] for v in picked]:picked.append(c)
 for c in candidates:
  if len(picked)>=8:break
  if c['cel'] not in [v['cel'] for v in picked]:picked.append(c)
 picked=sorted(picked[:8],key=lambda c:c['cel']);out=Image.new('RGBA',(1536,1024));cells=[]
 for slot,c in enumerate(picked):
  f=S/f'costume{cid:03d}_{c["cel"]:03d}_idx.png';im=Image.open(f).convert('RGBA');bb=im.getbbox();im=im.crop(bb);scale=min(300/im.width,360/im.height);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST);out.alpha_composite(im,(slot%4*384+(384-im.width)//2,slot//4*512+(512-im.height)//2));cells.append(dict(file=f.name,slot=slot,source_bbox=list(bb),source_size=c['size']))
 out.save(P/f'tram{cid:03d}-anchor-reference.png');plans.append(dict(costume=cid,cells=cells,missing_art_cells=len(missing),art_cells=[c['cel'] for c in art]))
(P/'tram-art-plans.json').write_text(json.dumps(plans,indent=2)+'\n');print([(v['costume'],v['missing_art_cells']) for v in plans])
