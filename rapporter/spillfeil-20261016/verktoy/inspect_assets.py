import os
from pathlib import Path
import json,sys
from PIL import Image,ImageDraw
R=Path(os.environ.get("DIGHD_WORKSPACE",Path.cwd()))
sys.path.insert(0,str(R/'kode/pipeline'))
from dighd import gamedata as g
GAME=Path('/home/tom/Documents/Codex/2026-10-16-the-dig-hd-remake-sp-rsm/testing/linux-release/AppDir/usr/share/the-dig-hd/game')
d=(GAME/'DIG.LA1').read_bytes(); ix=g.read_index(GAME/'DIG.LA0');rooms=g.read_rooms(GAME/'DIG.LA1')
anims={};cellmeta={}
for cid in [14,15,16,17,18,58,59,60,67,69,73,78,79,80,81,82,83,103,104,107,114,119,121,286,287,288,289]:
 rn,ofs=ix.costume_dir[cid];p=rooms[rn].offset+ofs
 anims[cid]=g.akos_animations(d,p,g.be32(d,p+4))
 blocks={t:(o+8,s-8) for t,o,s in g.children(d,p+8,p+g.be32(d,p+4))}
 if b'AKOF' in blocks and b'AKCI' in blocks:
  import struct
  akof=blocks[b'AKOF'];ci=blocks[b'AKCI'][0]
  cellmeta[cid]=[struct.unpack_from('<HHhhhh',d,ci+g.le16(d,akof[0]+j*6+4)) for j in range(akof[1]//6)]
(R/'testing/anims.json').write_text(json.dumps(anims,indent=2))
(R/'testing/cell-metadata.json').write_text(json.dumps(cellmeta,indent=2))
dest=R/'testing/assets';dest.mkdir(exist_ok=True)
for cid in [14,15,18,58,59,60,286]:
 files=sorted((R/'kandidat-mod/costumes').glob(f'costume{cid:03d}_*_idx.png'))
 if cid in [14,15,18]:files=[f for f in files if int(f.stem.split('_')[1])<65]
 if cid==286:files=files[:30]
 cw,ch=240,220;sheet=Image.new('RGB',(cw*6,ch*((len(files)+5)//6)),'#696979');draw=ImageDraw.Draw(sheet)
 for j,f in enumerate(files):
  im=Image.open(f).convert('RGBA');hd=f.with_name(f.name.replace('_idx','_hd'));x=(j%6)*cw;y=(j//6)*ch
  im=im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST);im.thumbnail((110,190));sheet.paste(im,(x,y+22),im)
  if hd.exists():
   art=Image.open(hd).convert('RGBA');art.thumbnail((120,190));sheet.paste(art,(x+115,y+22),art)
  draw.text((x+5,y+3),f.stem,fill='white')
 sheet.save(dest/f'costume{cid:03d}.png')
print('metadata and contact sheets exported')
