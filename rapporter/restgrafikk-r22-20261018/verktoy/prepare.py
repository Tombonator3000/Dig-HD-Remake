"""Source-only palette reconstruction and drawing-reference layout. No generated art."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[4];P=Path(__file__).resolve().parents[1];(P/'originaler').mkdir(exist_ok=True)
sys.path.insert(0,str(R/'kode/pipeline'));from dighd import gamedata as g
G=R/'testing/distro-r21/AppDir/usr/share/the-dig-hd/game';d=(G/'DIG.LA1').read_bytes();ix=g.read_index(G/'DIG.LA0');rooms=g.read_rooms(G/'DIG.LA1');rn,off=ix.costume_dir[100];p=rooms[rn].offset+off;bl={t:d[o+8:o+n] for t,o,n in g.children(d,p+8,p+g.be32(d,p+4))};mapping=np.array(list(bl[b'AKPL']));pal=rooms[32].palettes[0];colors=[]
for i in mapping:colors+=list(pal[i*3:i*3+3])
colors+=[0]*(768-len(colors));missing=[x for x in json.loads((R/'grafikk/rapporter/restgrafikk-r20-20261017/remaining.json').read_text())['cells'] if x['costume']==100];plans=[]
for batch in range((len(missing)+7)//8):
 group=missing[batch*8:batch*8+8];sheet=Image.new('RGBA',(1536,1024));cells=[]
 for slot,c in enumerate(group):
  name=c['name'];idx=Image.open(R/'testing/source/costumes'/(name+'_idx.png'));codes=np.array(idx);idx.putpalette(colors);idx.save(P/'originaler'/(name+'_idx.png'));a=np.array(idx.convert('RGBA'));a[codes==0]=0;a[mapping[codes]==13]=0;im=Image.fromarray(a);im.save(P/'originaler'/(name+'.png'));bb=im.getbbox();cut=im.crop(bb);factor=min(330/cut.width,420/cut.height);cut=cut.resize((round(cut.width*factor),round(cut.height*factor)),Image.Resampling.NEAREST);x=slot%4*384+(384-cut.width)//2;y=slot//4*512+(512-cut.height)//2;sheet.alpha_composite(cut,(x,y));cells.append(dict(name=name,cel=c['cel'],slot=slot,source_size=list(im.size),source_bbox=list(bb),reference_bbox=[x,y,x+cut.width,y+cut.height],job=c['job']))
 stem=f'boston100-{batch+1:02d}';sheet.save(P/(stem+'-reference.png'));plans.append(dict(stem=stem,costume=100,room=32,palette=0,grid=[4,2],cells=cells))
(P/'plans.json').write_text(json.dumps(dict(source_palette=colors,batches=plans),indent=2)+'\n');print(len(missing),'source cels prepared')
