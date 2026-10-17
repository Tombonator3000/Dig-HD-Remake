"""Original combined cast cels, costume 34, canyon room 15 palette 0."""
from pathlib import Path
import os,sys,json,hashlib
import numpy as np
from PIL import Image
R=Path(os.environ.get('DIGHD_WORKSPACE',Path(__file__).resolve().parents[4]))
P=R/'grafikk/rapporter/restgrafikk-r20-20261017';sys.path.insert(0,str(R/'kode/pipeline'))
from dighd import gamedata as g
G=R/'testing/distro-r19/AppDir/usr/share/the-dig-hd/game';d=(G/'DIG.LA1').read_bytes();ix=g.read_index(G/'DIG.LA0');rooms=g.read_rooms(G/'DIG.LA1')
rn,off=ix.costume_dir[34];p=rooms[rn].offset+off;b={t:d[o+8:o+n] for t,o,n in g.children(d,p+8,p+g.be32(d,p+4))}
assert g.le16(b[b'AKHD'],8)==1
mapping=np.array(list(b[b'AKPL']));palette=rooms[15].palettes[0];colors=[]
for i in mapping:colors+=list(palette[i*3:i*3+3])
colors+=[0]*(768-len(colors))
old=json.loads((R/'grafikk/rapporter/restgrafikk-r19-20261016/dekning-arbeid.json').read_text());cells=sorted([c for c in old['cells'] if c['costume']==34],key=lambda c:c['cel']);plans=[]
for c in cells:
    f=R/'testing/source/costumes'/(c['name']+'_idx.png');idx=Image.open(f);codes=np.array(idx).copy();idx.putpalette(colors);assert np.array_equal(np.array(idx),codes)
    a=np.array(idx.convert('RGBA'));a[mapping[codes]==13]=0
    art=Image.fromarray(a);c['source_bbox']=list(art.getbbox());c['source_size']=list(art.size);c['source_sha256']=hashlib.sha256(f.read_bytes()).hexdigest()
    art.save(P/'originaler'/(c['name']+'.png'));idx.save(P/'originaler'/f.name)
for batch in range((len(cells)+7)//8):
    group=cells[batch*8:batch*8+8];sheet=Image.new('RGBA',(1536,1024))
    for slot,c in enumerate(group):
        art=Image.open(P/'originaler'/(c['name']+'.png')).crop(c['source_bbox']);factor=min(330/art.width,420/art.height);art=art.resize((round(art.width*factor),round(art.height*factor)),Image.Resampling.NEAREST)
        x=slot%4*384+(384-art.width)//2;y=slot//4*512+(512-art.height)//2;sheet.alpha_composite(art,(x,y));c['slot']=slot;c['reference_bbox']=[x,y,x+art.width,y+art.height]
    stem=f'canyon034-{batch+1:02d}';sheet.save(P/(stem+'-reference.png'));plans.append(dict(stem=stem,room=15,palette=0,costume=34,grid=[4,2],cells=group))
(P/'canyon-plans.json').write_text(json.dumps(dict(script='room015-LSCR-2010, actor3 composite cast animation6/7/8/9',source_palette=colors,batches=plans),indent=2)+'\n')
print(len(cells),'whole-unit cast cels in',len(plans),'sheets')
