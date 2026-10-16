import os
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,csv
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));S=R/'testing/source/costumes';P=R/'grafikk/rapporter/restgrafikk-r19-20261016';report=json.loads((P/'dekning-arbeid.json').read_text());names={}
with (R/'kode/docs/rom-oversikt.csv').open() as f:
 reader=csv.DictReader(f)
 for row in reader:
  vals=list(row.values())
  try:names[int(vals[0])]=vals[1]
  except ValueError:pass
groups=[g for g in report['groups'] if g['substantial']];pages=[]
for start in range(0,len(groups),24):
 sheet=Image.new('RGB',(1536,1440),'#4b4c56');draw=ImageDraw.Draw(sheet)
 for i,g in enumerate(groups[start:start+24]):
  cid=g['costume'];x=i%4*384;y=i//4*240;cells=[c for c in report['cells'] if c['costume']==cid and c['pixels']>=40];cells.sort(key=lambda c:c['cel'])
  picks=sorted(set([0,len(cells)//2,len(cells)-1]));draw.text((x+5,y+5),f"{cid:03d}: {g['substantial']} / room {g['room']} {names.get(g['room'],'')}",fill='white')
  for j,index in enumerate(picks):
   c=cells[index];f=S/(c['name']+'.png')
   if f.exists():im=Image.open(f).convert('RGBA')
   else:
    meta=json.loads((R/'grafikk/jobber'/c['job']/'jobb.json').read_text());im=Image.open(R/'grafikk/jobber'/c['job']/'original_1x.png').convert('RGBA');sx,sy,w,h=c['rect'];im=im.crop((sx,sy,sx+w,sy+h));a=np.array(im);a[np.all(a[:,:,:3]==meta['bakgrunn'],2),3]=0;im=Image.fromarray(a)
   im.thumbnail((122,190));sheet.paste(im,(x+j*128+(128-im.width)//2,y+28+(190-im.height)//2),im);draw.text((x+j*128+5,y+218),str(c['cel']),fill='white')
 dest=P/f'restkatalog-{start//24:02d}.png';sheet.save(dest);pages.append(str(dest))
print('\n'.join(pages))
