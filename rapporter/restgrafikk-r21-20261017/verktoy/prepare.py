from pathlib import Path
import json,sys
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[4];P=R/'grafikk/rapporter/restgrafikk-r21-20261017';P.mkdir(exist_ok=True);(P/'originaler').mkdir(exist_ok=True);(P/'verktoy').mkdir(exist_ok=True)
sys.path.insert(0,str(R/'kode/pipeline'));from dighd import gamedata as g
G=R/'testing/distro-r19/AppDir/usr/share/the-dig-hd/game';d=(G/'DIG.LA1').read_bytes();ix=g.read_index(G/'DIG.LA0');rooms=g.read_rooms(G/'DIG.LA1');rn,off=ix.costume_dir[34];p=rooms[rn].offset+off;b={t:d[o+8:o+n] for t,o,n in g.children(d,p+8,p+g.be32(d,p+4))};mapping=np.array(list(b[b'AKPL']));palette=rooms[15].palettes[0];colors=[]
for i in mapping:colors+=list(palette[i*3:i*3+3])
colors+=[0]*(768-len(colors));cells=[]
for f in sorted((R/'hd-leveranse/costumes').glob('costume034_*_hd.png')):
 name=f.stem[:-3];idx=Image.open(R/'testing/source/costumes'/(name+'_idx.png'));codes=np.array(idx);idx.putpalette(colors);a=np.array(idx.convert('RGBA'));a[mapping[codes]==13]=0;im=Image.fromarray(a);im.save(P/'originaler'/(name+'.png'));idx.save(P/'originaler'/(name+'_idx.png'));cells.append(dict(name=name,cel=int(name[-3:]),source_bbox=list(im.getbbox()),source_size=list(im.size)))
preview=Image.new('RGB',(2000,((len(cells)+7)//8)*220),'#424650');draw=ImageDraw.Draw(preview)
for i,c in enumerate(cells):
 x=i%8*250;y=i//8*220;draw.text((x+3,y+3),c['name'],fill='white')
 for j,im in enumerate([Image.open(P/'originaler'/(c['name']+'.png')),Image.open(R/'hd-leveranse/costumes'/(c['name']+'_hd.png'))]):
  im=im.convert('RGBA');im=im.crop(im.getbbox());im.thumbnail((120,185));preview.paste(im,(x+j*125+(120-im.width)//2,y+25+(185-im.height)//2),im)
preview.save(P/'audit-before.png');(P/'audit-cells.json').write_text(json.dumps(cells,indent=2)+'\n');print(P,len(cells))
plans=[]
for batch in range((len(cells)+7)//8):
 group=cells[batch*8:batch*8+8];sheet=Image.new('RGBA',(1536,1024))
 for slot,c in enumerate(group):
  im=Image.open(P/'originaler'/(c['name']+'.png')).crop(c['source_bbox']);factor=min(330/im.width,420/im.height);im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.NEAREST);x=slot%4*384+(384-im.width)//2;y=slot//4*512+(512-im.height)//2;sheet.alpha_composite(im,(x,y));c['slot']=slot;c['reference_bbox']=[x,y,x+im.width,y+im.height]
 stem=f'canyon034-redraw-{batch+1:02d}';sheet.save(P/(stem+'-reference.png'));plans.append(dict(stem=stem,room=15,palette=0,costume=34,grid=[4,2],cells=group))
(P/'canyon-plans.json').write_text(json.dumps(dict(source_palette=colors,batches=plans),indent=2)+'\n')
