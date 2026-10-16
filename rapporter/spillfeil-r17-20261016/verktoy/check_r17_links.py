from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
from scipy.ndimage import distance_transform_edt
R=Path(__file__).resolve().parent;M=R/'kandidat-r17/costumes';P=R/'grafikk/rapporter/spillfeil-r17-20261016';geo=json.loads((R/'testing/r17-geometry.json').read_text())['178'];parts={row['parts'][0]['cel']:row['parts'][0] for row in geo if len(row['parts'])==1};anim=json.loads((R/'testing/r17-anims.json').read_text())['178']['animasjoner'];pairs=set()
for a in [4,5]:
 for di in range(8):
  body=next(z['ruter'] for z in anim if z['animasjon']==a and z['retning']==di and z['lag']==0);head=next(z['ruter'] for z in anim if z['animasjon']==a and z['retning']==di and z['lag']==1)
  pairs.update((b,h) for b in body for h in head)
rows=[];sheet=Image.new('RGB',(1400,((len(pairs)+6)//7)*210),'#777788');d=ImageDraw.Draw(sheet)
for j,(b,h) in enumerate(sorted(pairs)):
 layers=[]
 for c in [b,h]:
  p=parts[c];stem=f'costume178_{c:03d}';idx=Image.open(M/(stem+'_idx.png'));im=Image.open(M/(stem+'_hd.png')).convert('RGBA');px=(im.width//4-idx.width)//2;py=(im.height//4-idx.height)//2;layers.append((im,(p['x']-px)*4,(p['y']-py)*4))
 x0=min(x for im,x,y in layers);y0=min(y for im,x,y in layers);x1=max(x+im.width for im,x,y in layers);y1=max(y+im.height for im,x,y in layers);out=Image.new('RGBA',(x1-x0+8,y1-y0+8));ms=[]
 for im,x,y in layers:
  out.alpha_composite(im,(x-x0+4,y-y0+4));mask=Image.new('L',out.size);mask.paste(im.getchannel('A'),(x-x0+4,y-y0+4));ms.append(np.asarray(mask)>128)
 gap=float(distance_transform_edt(~ms[0])[ms[1]].min());rows.append({'body':b,'head':h,'gap_hd':gap,'needs_review':gap>4});out.thumbnail((195,190));x=j%7*200;y=j//7*210;sheet.paste(out,(x,y+20),out);d.text((x,y),f'{b}+{h}, gap {gap:.1f}',fill='white')
(P/'HEAD-BODY-CHECK.json').write_text(json.dumps(rows,indent=2));sheet.save(R/'testing/r17-head-links.png');print(len(rows),'pairs, max gap',max(r['gap_hd'] for r in rows));assert not any(r['needs_review'] for r in rows)
