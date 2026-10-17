"""R20 references from original physical cels and scripted Nexus palettes.

Workbench only. Does not change job originals, published assets or engine code.
"""
from pathlib import Path
import os, sys, json, hashlib, subprocess
import numpy as np
from PIL import Image

R = Path(os.environ.get('DIGHD_WORKSPACE', Path(__file__).resolve().parents[4]))
P = R / 'grafikk/rapporter/restgrafikk-r20-20261017'
sys.path.insert(0, str(R / 'kode/pipeline'))
from dighd import gamedata as g

G = R / 'testing/distro-r19/AppDir/usr/share/the-dig-hd/game'
rooms = g.read_rooms(G / 'DIG.LA1')
old = json.loads((R / 'grafikk/rapporter/restgrafikk-r19-20261016/dekning-arbeid.json').read_text())
base = subprocess.check_output(['git','-C',str(R/'hd-leveranse'),'rev-parse','HEAD'], text=True).strip()
assert base == '630cadb3ebb398ac8ade1f4e1ea759f8a783cd5a'
out = P / 'originaler'
out.mkdir(parents=True, exist_ok=True)
plans = []
scripts = {62: (280,1,'museum'),63: (283,0,'map'),64: (289,2,'tomb'),65: (286,3,'planetarium'),66: (262,0,'cathedral')}
for cid, (script, palnum, meaning) in scripts.items():
    cells = sorted([c for c in old['cells'] if c['costume']==cid], key=lambda c:c['cel'])
    for cell in cells:
        source = R / 'testing/source/costumes' / (cell['name']+'_idx.png')
        idx = Image.open(source)
        pixels = np.array(idx).copy()
        # Codec 5 feeds direct room-palette codes to ScummVM, not AKPL.
        idx.putpalette(rooms[23].palettes[palnum])
        idx.info['transparency'] = 255
        assert np.array_equal(np.array(idx),pixels)
        idx.save(out/source.name)
        art = idx.convert('RGBA')
        assert art.getbbox()
        cell['source_bbox'] = list(art.getbbox())
        cell['source_size'] = list(art.size)
        cell['source_sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
        art.save(out/(cell['name']+'.png'))
        assert not (R/'hd-leveranse/costumes'/(cell['name']+'_hd.png')).exists()
        assert not (R/'hd-leveranse/costumes'/(cell['name']+'.png')).exists()
    for batch in range((len(cells)+11)//12):
        group = cells[batch*12:batch*12+12]
        sheet = Image.new('RGBA',(1536,1536))
        for slot, c in enumerate(group):
            art = Image.open(out/(c['name']+'.png')).crop(c['source_bbox'])
            scale = min(320/art.width, 430/art.height)
            art = art.resize((round(art.width*scale),round(art.height*scale)),Image.Resampling.NEAREST)
            x=slot%4*384+(384-art.width)//2
            y=slot//4*512+(512-art.height)//2
            sheet.alpha_composite(art,(x,y))
            c['slot']=slot
            c['reference_bbox']=[x,y,x+art.width,y+art.height]
        stem=f'nexus{cid:03d}-{batch+1:02d}'
        sheet.save(P/(stem+'-reference.png'))
        plans.append(dict(stem=stem,costume=cid,room=23,palette=palnum,script=f'global{script}',meaning=meaning,grid=[4,3],cells=group))
(P/'plans.json').write_text(json.dumps(dict(base=base,batches=plans),ensure_ascii=False,indent=2)+'\n')
print([(p['stem'],len(p['cells'])) for p in plans])
