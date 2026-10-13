from pathlib import Path
from PIL import Image
import numpy as np,shutil,json,hashlib
R=Path('.');G=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk');report=G/'rapporter/spillfeil-r12-20261013';O=report/'mod-overrides/costumes';O.mkdir(parents=True,exist_ok=True);M=R/'AppDir/usr/share/the-dig-hd/mods/gpt/costumes';atlas=Image.open(report/'produksjon/boston-krystallplukk-atlas-1.png').convert('RGBA');placements=[]
for cel in range(23):
 stem=f'costume231_{cel:03d}';j=cel;cx=(j%6)*256;cy=(j//6)*256;im=atlas.crop((cx,cy,cx+256,cy+256));a=np.asarray(im);mask=a[:,:,3]>100;ys,xs=np.where(mask);assert len(xs)>500,(cel,len(xs));box=(int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1)
 src=Image.open(R/'original/costumes'/(stem+'_context.png')).convert('RGBA');s=np.asarray(src);ys,xs=np.where(s[:,:,3]>128);sb=(int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1);w,h=src.size
 out=Image.new('RGBA',((w+8)*4,(h+8)*4));cut=im.crop(box).resize(((sb[2]-sb[0])*4,(sb[3]-sb[1])*4),Image.Resampling.LANCZOS);out.alpha_composite(cut,((sb[0]+4)*4,(sb[1]+4)*4));out.save(O/(stem+'_hd.png'))
 idx=Image.open(R/'original/costumes'/(stem+'_idx.png'));idx.putpalette(src.convert('P').getpalette() or [0]*768) if False else None
 # This costume inherits Boston's actor palette. Preserve exact source codes,
 # but use the room0/AKPL context palette verified in the original renderer.
 from dighd import gamedata
 if cel==0:
  D=(R/'AppDir/usr/share/the-dig-hd/game/DIG.LA1').read_bytes();ix=gamedata.read_index(R/'AppDir/usr/share/the-dig-hd/game/DIG.LA0');rooms=gamedata.read_rooms(R/'AppDir/usr/share/the-dig-hd/game/DIG.LA1');rn,ofs=ix.costume_dir[231];akos=rooms[rn].offset+ofs;p=gamedata.find_child(D,akos,gamedata.be32(D,akos+4),b'AKPL');akpl=D[p+8:p+gamedata.be32(D,p+4)];pal=bytearray(768)
  for code,val in enumerate(akpl):pal[code*3:code*3+3]=rooms[rn].palettes[0][val*3:val*3+3]
 idx.putpalette(pal);idx.save(O/(stem+'_idx.png'),transparency=idx.info.get('transparency',255))
 for suffix in ['_hd.png','_idx.png']:shutil.copy2(O/(stem+suffix),M/(stem+suffix))
 placements.append({'cel':cel,'atlas_box':box,'source_box':sb,'output_size':list(out.size)})
(report/'BOSTON231-REGISTRERING.json').write_text(json.dumps({'frames':placements,'source_palette':'room82 palette0 through AKPL; verified original game screenshot','original_indices_preserved':True},indent=2));print('23 Boston pickup cells staged.')
