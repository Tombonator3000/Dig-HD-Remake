import os
"""Identify combined trap/rat cels by the original mechanism palette, not silhouette guesses."""
from pathlib import Path
import sys,json,numpy as np
from PIL import Image
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));sys.path.insert(0,str(R/'kode/pipeline'));from dighd import gamedata as g
P=R/'grafikk/rapporter/restgrafikk-r19-20261016';S=R/'testing/source/costumes';A=R/'testing/rat183-source';G=Path('/home/tom/Documents/Codex/2026-10-16-the-dig-hd-remake-sp-rsm/testing/linux-release/AppDir/usr/share/the-dig-hd/game');d=(G/'DIG.LA1').read_bytes();ix=g.read_index(G/'DIG.LA0');rooms=g.read_rooms(G/'DIG.LA1');rn,off=ix.costume_dir[183];p=rooms[rn].offset+off;b={t:d[o+8:o+n] for t,o,n in g.children(d,p+8,p+g.be32(d,p+4))};mapping=np.array(list(b[b'AKPL']));plan=json.loads((P/'rat183-plan.json').read_text());combined=[]
for row in plan['art_cells']:
 idx=np.array(Image.open(S/row['file']));vals=mapping[idx];n=int(((vals>=46)&(vals<=103)).sum())
 if n>=40:combined.append(row)
selected=[combined[round(i*(len(combined)-1)/7)] for i in range(8)];out=Image.new('RGBA',(1536,1024));cells=[]
for slot,row in enumerate(selected):
 im=Image.open(A/row['file']).convert('RGBA');bb=im.getbbox();im=im.crop(bb);factor=min(330/im.width,400/im.height);im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.NEAREST);out.alpha_composite(im,(slot%4*384+(384-im.width)//2,slot//4*512+(512-im.height)//2));cells.append(row|dict(slot=slot))
out.save(P/'rat183-trap-reference.png');(P/'rat183-trap-plan.json').write_text(json.dumps(dict(cells=cells,combined_cells=[v['cel'] for v in combined]),indent=2)+'\n');print(len(combined),'combined trap/rat cells', [v['cel'] for v in selected])
