import os
"""Prepare rat poses with original scripted room palette and without shade code 13."""
from pathlib import Path
import sys,json,numpy as np,cv2
from PIL import Image
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));sys.path.insert(0,str(R/'kode/pipeline'));from dighd import gamedata as g
P=R/'grafikk/rapporter/restgrafikk-r19-20261016';S=R/'testing/source/costumes';B=R/'hd-leveranse/costumes';C=R/'kandidat-r19/costumes'
G=Path('/home/tom/Documents/Codex/2026-10-16-the-dig-hd-remake-sp-rsm/testing/linux-release/AppDir/usr/share/the-dig-hd/game');d=(G/'DIG.LA1').read_bytes();ix=g.read_index(G/'DIG.LA0');rooms=g.read_rooms(G/'DIG.LA1');rn,off=ix.costume_dir[183];p=rooms[rn].offset+off;b={t:d[o+8:o+n] for t,o,n in g.children(d,p+8,p+g.be32(d,p+4))};mapping=np.array(list(b[b'AKPL']));pal=rooms[68].palettes[1];colors=[]
for i in mapping:colors+=list(pal[i*3:i*3+3])
colors+=[0]*(768-len(colors));outdir=R/'testing/rat183-source';outdir.mkdir(exist_ok=True);art=[];technical=[]
for f in sorted(S.glob('costume183_*_idx.png')):
 im=Image.open(f);idx=np.array(im);im.putpalette(colors);a=np.array(im.convert('RGBA'));mask=(a[:,:,3]>128)&(mapping[idx]!=13);a[~mask]=0;Image.fromarray(a).save(outdir/f.name);n=int(f.stem.split('_')[1]);area=int(mask.sum())
 if (C/f.name.replace('_idx','_hd')).exists():continue
 row=dict(file=f.name,cel=n,art_pixels=area,shade_pixels=int(((mapping[idx]==13)&(np.array(im.convert('RGBA'))[:,:,3]>128)).sum()))
 if area<40:technical.append(row);continue
 y,x=np.where(mask);bb=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];crop=a[bb[1]:bb[3],bb[0]:bb[2]];feature=cv2.resize(crop,(48,48),interpolation=cv2.INTER_AREA).astype('float32')/255;row.update(bbox=bb,feature=feature);art.append(row)
# Farthest-point coverage selects different silhouettes, orientations and poses.
picks=[0];features=np.stack([v['feature'] for v in art]);aspect=np.array([(v['bbox'][2]-v['bbox'][0])/(v['bbox'][3]-v['bbox'][1]) for v in art]);distance=np.full(len(art),np.inf)
while len(picks)<min(32,len(art)):
 k=picks[-1];dist=((features-features[k])**2).mean(axis=(1,2,3))+np.minimum(abs(np.log(aspect/aspect[k])),2)*.04;distance=np.minimum(distance,dist);distance[picks]=-1;picks.append(int(np.argmax(distance)))
picked=sorted([art[k] for k in picks],key=lambda v:v['cel']);plans=[]
for batch in range((len(picked)+7)//8):
 out=Image.new('RGBA',(1536,1024));cells=[]
 for slot,row in enumerate(picked[batch*8:batch*8+8]):
  im=Image.open(outdir/row['file']).crop(row['bbox']);factor=min(310/im.width,370/im.height);im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.NEAREST);out.alpha_composite(im,(slot%4*384+(384-im.width)//2,slot//4*512+(512-im.height)//2));cells.append({k:v for k,v in row.items() if k!='feature'}|dict(slot=slot))
 out.save(P/f'rat183-{batch+1:02d}-reference.png');plans.append(dict(batch=batch+1,cells=cells))
(P/'rat183-plan.json').write_text(json.dumps(dict(costume=183,room=68,palette=1,shadow_mode=1,shadow_code=13,batches=plans,art_cells=[{k:v for k,v in r.items() if k!='feature'} for r in art],technical_cells=technical),indent=2)+'\n');print(len(art),'missing rat artwork cells,',len(technical),'technical/empty,',len(picked),'selected anchors')
