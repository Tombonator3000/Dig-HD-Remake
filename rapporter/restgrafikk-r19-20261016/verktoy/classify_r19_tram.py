import os
"""Separate source tram artwork from palette-effect masks.
Pure masks are NOT new HD art and are not removed from the raw inventory.
Original local scripts explicitly use actor 18 shadow mode 3 for chores 9..11;
ScummVM base-costume.cpp and bomp.cpp apply source values below 8 as tables.
Further native reachability evidence is collected separately.
"""
from pathlib import Path
import sys,json
import numpy as np
from PIL import Image
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));sys.path.insert(0,str(R/'kode/pipeline'));from dighd import gamedata as g
G=Path('/home/tom/Documents/Codex/2026-10-16-the-dig-hd-remake-sp-rsm/testing/linux-release/AppDir/usr/share/the-dig-hd/game');d=(G/'DIG.LA1').read_bytes();ix=g.read_index(G/'DIG.LA0');rooms=g.read_rooms(G/'DIG.LA1');P=R/'grafikk/rapporter/restgrafikk-r19-20261016';S=R/'testing/source/costumes';rows=[]
for cid in [92,122,166,268,270,272,274,276]:
 rn,ofs=ix.costume_dir[cid];off=rooms[rn].offset+ofs;b={t:d[o+8:o+s] for t,o,s in g.children(d,off+8,off+g.be32(d,off+4))};codec=g.le16(b[b'AKHD'],8);pal=np.array(list(b[b'AKPL'])+[0]*(256-len(b[b'AKPL'])),dtype='uint8');cells=[]
 for f in sorted(S.glob(f'costume{cid:03d}_*_idx.png')):
  im=Image.open(f);idx=np.array(im);rgba=np.array(im.convert('RGBA'));mask=rgba[:,:,3]>128;values=pal[idx] if codec==1 else idx;art=mask&(values>=8);n=int(f.stem.split('_')[1]);cells.append(dict(cel=n,size=list(im.size),visible=int(mask.sum()),art_pixels=int(art.sum()),effect_pixels=int((mask&~art).sum()),source_values=sorted(set(int(v) for v in values[mask])),classification='pure palette mask under scripted shadow mode 3' if mask.any() and not art.any() else 'contains artwork or empty'))
 rows.append(dict(costume=cid,home_room=rn,codec=codec,pure_mask_cells=sum(v['visible']>0 and v['art_pixels']==0 for v in cells),art_cells=sum(v['art_pixels']>0 for v in cells),cells=cells))
(P/'tram-mask-classification.json').write_text(json.dumps(dict(source_tools_revision='scummvm/scummvm-tools@8665aa1d3221a6cc884026f5ed7144fac512e0e9',method='original AKPL/raw codes plus original scripted actor shadow mode, no artwork generated',costumes=rows),indent=2)+'\n');print([(v['costume'],v['pure_mask_cells'],v['art_cells']) for v in rows])
# AKOS choices independently confirm every pure mask is confined to the
# scripted effect chores 9..11, with no overlap in painted chores 6..8.
proof=[]
script_map={92:'room029-LSCR-2004',122:'room037-LSCR-2005',166:'room060-LSCR-2002',268:'room095-LSCR-2002',270:'room080-LSCR-2002',272:'room081-LSCR-2001',274:'room083-LSCR-2002',276:'room094-LSCR-2002'}
for costume in rows:
 cid=costume['costume'];rn,ofs=ix.costume_dir[cid];off=rooms[rn].offset+ofs;choices=g.akos_animations(d,off,g.be32(d,off+4));by={}
 for v in choices['animasjoner']:by.setdefault(v['animasjon'],set()).update(v['ruter'])
 masks={v['cel'] for v in costume['cells'] if v['visible']>0 and v['art_pixels']==0};shade=set().union(*(by.get(n,set()) for n in [9,10,11]));art=set().union(*(by.get(n,set()) for n in [6,7,8]));assert masks<=shade and not masks&art,(cid,masks-shade,masks&art)
 text=(R/'testing/r19-original-scripts'/(script_map[cid]+'.txt')).read_text();lines=text.splitlines();shadow=next(i for i,l in enumerate(lines) if 'actorOps.setShadowMode(3)' in l);assert any('actorOps.setCurActor(18)' in l for l in lines[max(0,shadow-4):shadow]);selected=[l for l in lines if 'actorOps.setCostume('+str(cid)+')' in l or 'actorOps.setShadowMode(3)' in l or 'animateActor(18,9)' in l or 'buildPaletteShadow([4,' in l][:8]
 proof.append(dict(costume=cid,pure_masks=len(masks),all_in_effect_chores=True,none_in_art_chores=True,script=script_map[cid],script_commands=selected,mask_cells=sorted(masks),art_cells=sorted(art)))
(P/'tram-chore-classification.json').write_text(json.dumps(proof,indent=2)+'\n')
raw=json.loads((P/'dekning-arbeid.json').read_text());maskkeys={(v['costume'],n) for v in proof for n in v['mask_cells']};technical=[c['name'] for c in raw['cells'] if (c['costume'],c['cel']) in maskkeys];summary=dict(raw_missing=raw['missing'],confirmed_palette_masks_without_bitmaps=len(technical),remaining_after_confirmed_mask_classification=raw['missing']-len(technical),technical_mask_cells=technical,warning='Raw inventory remains unchanged. This classifies engine-rendered effects; it does not count masks as newly painted graphics or prove a full playthrough.')
(P/'semantic-coverage.json').write_text(json.dumps(summary,indent=2)+'\n');print(summary['confirmed_palette_masks_without_bitmaps'],'raw inventory entries are confirmed palette effects')
