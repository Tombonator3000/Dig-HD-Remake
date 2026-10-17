import os
"""Original Brink shovel sequence: global174 explicitly assigns costume46 to actor5.
Use room15 palette (the scripted scene), not the job's fallback room19.
"""
from pathlib import Path
import sys,json,numpy as np
from PIL import Image
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));sys.path.insert(0,str(R/'kode/pipeline'));from dighd import gamedata as g
P=R/'grafikk/rapporter/restgrafikk-r19-20261016';S=R/'testing/source/costumes';A=R/'testing/brink46-source';A.mkdir(exist_ok=True);G=Path('/home/tom/Documents/Codex/2026-10-16-the-dig-hd-remake-sp-rsm/testing/linux-release/AppDir/usr/share/the-dig-hd/game');d=(G/'DIG.LA1').read_bytes();ix=g.read_index(G/'DIG.LA0');rooms=g.read_rooms(G/'DIG.LA1');rn,off=ix.costume_dir[46];p=rooms[rn].offset+off;b={t:d[o+8:o+n] for t,o,n in g.children(d,p+8,p+g.be32(d,p+4))};mapping=np.array(list(b[b'AKPL']));pal=rooms[15].palettes[0];colors=[]
for i in mapping:colors+=list(pal[i*3:i*3+3])
colors+=[0]*(768-len(colors));cells=[]
for f in sorted(S.glob('costume046_*_idx.png')):
 im=Image.open(f);idx=np.array(im);im.putpalette(colors);a=np.array(im.convert('RGBA'));a[mapping[idx]==13]=0;im=Image.fromarray(a);bb=im.getbbox();im.save(A/f.name);cells.append(dict(file=f.name,cel=int(f.stem.split('_')[1]),bbox=list(bb)))
used=set().union(*(set(mapping[np.array(Image.open(f))].ravel()) for f in S.glob('costume046_*_idx.png')))-{0,13}
qa_palette_equal=all(rooms[15].palettes[0][int(i)*3:int(i)*3+3]==rooms[23].palettes[0][int(i)*3:int(i)*3+3] for i in used);assert qa_palette_equal
plans=[]
for batch in range(2):
 out=Image.new('RGBA',(1536,1024));rows=[]
 for slot,row in enumerate(cells[batch*8:batch*8+8]):
  im=Image.open(A/row['file']).crop(row['bbox']);factor=min(280/im.width,420/im.height);im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.NEAREST);out.alpha_composite(im,(slot%4*384+(384-im.width)//2,slot//4*512+(512-im.height)//2));rows.append(row|dict(slot=slot))
 out.save(P/f'brink46-{batch+1:02d}-reference.png');plans.append(dict(batch=batch+1,cells=rows))
(P/'brink46-plan.json').write_text(json.dumps(dict(costume=46,script='global174 actor5 costume46 in room15',room=15,palette=0,reference='hovedark/brink.png',source_palette=colors,qa_room=23,qa_used_palette_codes=sorted(int(i) for i in used),qa_character_palette_identical_to_room15=qa_palette_equal,batches=plans),indent=2)+'\n');print(len(cells),'original Brink shovel poses')
