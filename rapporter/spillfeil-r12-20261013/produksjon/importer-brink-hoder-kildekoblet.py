"""Source-directed Brink heads. No nearest-head or colour-orientation guessing.
Only regular standing/walking/talking directions explicitly declared by AKCH are
imported; ambiguous/shared technical cells and unreviewed special actions retain
the r11 baseline. Fixed per-direction head size prevents speech skull scaling.
"""
from pathlib import Path
from PIL import Image
import numpy as np,json,shutil,hashlib
R=Path(__file__).resolve().parent
P=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk/rapporter/spillfeil-r12-20261013')
O=P/'mod-overrides/costumes';M=R/'AppDir/usr/share/the-dig-hd/mods/gpt/costumes';B=R/'r11-brink-baseline/usr/share/the-dig-hd/mods/gpt/costumes'
meta=json.load(open(R/'original-all/costumes.json'));anims=json.load(open(R/'costume-anims.json'))
old=P/'BRINK-HODER-REGISTRERING.json'
if old.exists():
 records=json.load(open(old));records=records if isinstance(records,list) else records['cells']
 for rec in records:
  stem=f'costume{rec["costume"]:03d}_{rec["cel"]:03d}'
  for suf in ['_hd.png','_idx.png']:
   source=B/(stem+suf)
   if source.exists():shutil.copy2(source,M/source.name)
   (O/(stem+suf)).unlink(missing_ok=True)
# Every tile direction was visually checked against original standing/walking
# sheets: 0 rear,1 rear-right,2 right,3 front-right,4 front,5 front-left,
# 6 left,7 rear-left. This map is not inferred from regenerated images.
tiles={}
for cid,word in [(15,'frisk'),(16,'syk'),(17,'syk')]:
 master=Image.open(P/'produksjon'/f'brink-hoder-{word}-master.png').convert('RGBA')
 for row in range(3):
  for direction in range(8):
   im=master.crop((direction*192,round(row*1024/3),(direction+1)*192,round((row+1)*1024/3)));ar=np.asarray(im);ys,xs=np.where(ar[:,:,3]>100);tiles[cid,row,direction]=im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
records=[];skipped=[]
for cid in [15,16,17]:
 entries=anims[str(cid)]['animasjoner'];cells={};stand={}
 for a in entries:
  if a['animasjon'] in [1,2,4,5]:
   for cel in a['ruter']:cells.setdefault(cel,[]).append(a)
  if a['animasjon']==1 and a['lag']==1:
   valid=[x for x in a['ruter'] if meta[str(cid)]['cels'][x]['w']>=7]
   if valid:stand[a['retning']]=meta[str(cid)]['cels'][valid[-1]]
 for cel,uses in sorted(cells.items()):
  stem=f'costume{cid:03d}_{cel:03d}';source=R/'original-all/costumes'/(stem+'.png');src=Image.open(source).convert('RGBA');ar=np.asarray(src);h,w=ar.shape[:2];directions={a['retning'] for a in uses};walking=any(a['animasjon']==2 and a['lag']==0 for a in uses);standalone=h<=23 and w<=27 and any(a['lag']==1 for a in uses)
  if len(directions)!=1 or not (walking or standalone) or ar[:,:,3].sum()<500 or w<6:
   skipped.append({'costume':cid,'cel':cel,'reason':'shared/technical/body-only'});continue
  direction=next(iter(directions));out=Image.open(B/(stem+'_hd.png')).convert('RGBA');px=(out.width//4-w)//2;py=(out.height//4-h)//2
  if walking:
   # In this explicitly checked walk family, the complete head occupies the
   # first 11 rows. Shoulders, collar and hands are outside this bound.
   real=ar[:,:,3]>0;ys,xs=np.where(real[:min(8,h),:]);x0=int(xs.min());x1=int(xs.max())+1;y0=0;y1=11
   target_w=x1-x0;target_h=11
   # Baseline import can extend beyond the original head by a pixel or two.
   out.paste((0,0,0,0),(max(0,(x0+px-2)*4),max(0,py*4-4),min(out.width,(x1+px+2)*4),(py+y1)*4))
   mouth=0
  else:
   x0=y0=0;x1=w;y1=h;target_w=stand[direction]['w'];target_h=stand[direction]['h']
   out=Image.new('RGBA',out.size)
   # Preserve original expression changes without scaling head dimensions.
   dark=((ar[:,:,:3].max(2)<55)&(ar[:,:,3]>0)).sum();mouth=2 if dark>10 else 1 if dark>5 else 0
  tile=tiles[cid,mouth,direction].resize((target_w*4,target_h*4),Image.Resampling.LANCZOS)
  out.alpha_composite(tile,((x0+px)*4,(y0+py)*4));out.save(O/(stem+'_hd.png'));shutil.copy2(M/(stem+'_idx.png'),O/(stem+'_idx.png'));shutil.copy2(O/(stem+'_hd.png'),M/(stem+'_hd.png'))
  records.append({'costume':cid,'cel':cel,'direction':direction,'mouth':mouth,'sick':cid!=15,'embedded':walking,'head_bbox':[x0,y0,x1,y1],'target_size':[target_w,target_h],'source':'AKCH regular animation direction, manually reviewed eight-direction family'})
old.write_text(json.dumps({'method':'explicit original AKCH direction for regular standing/walking/talking, fixed head size, special actions restored to r11 pending individual review','cells':records,'skipped':skipped},indent=2))
(R/'qa/brink-explicit-map.json').write_text(json.dumps(records,indent=2));print('Imported explicit heads',len(records))
# Costume 16/17 RGBS tables are not their on-screen room palette. Use the
# verified room105 palette through AKPL so HD skin is not recoloured orange.
# Source byte indices and transparency are identical; only palette metadata.
import sys
sys.path.insert(0,str(R/'code/pipeline'))
from dighd import gamedata as g
D=(R/'AppDir/usr/share/the-dig-hd/game/DIG.LA1').read_bytes();game_index=g.read_index(R/'AppDir/usr/share/the-dig-hd/game/DIG.LA0');rooms=g.read_rooms(R/'AppDir/usr/share/the-dig-hd/game/DIG.LA1');palette_records=[]
for cid in [16,17]:
 rn,ofs=game_index.costume_dir[cid];pos=rooms[rn].offset+ofs;ak=g.find_child(D,pos,g.be32(D,pos+4),b'AKPL');akpl=D[ak+8:ak+g.be32(D,ak+4)];pal=np.zeros((256,3),np.uint8);roompal=np.frombuffer(rooms[105].palettes[0],np.uint8).reshape(256,3)
 for code,val in enumerate(akpl):pal[code]=roompal[val]
 for source in sorted(M.glob(f'costume{cid:03d}_*_idx.png')):
  im=Image.open(source);before=np.array(im).copy();im.putpalette(pal.ravel().tolist());im.save(O/source.name,transparency=im.info.get('transparency',255));shutil.copy2(O/source.name,source)
  assert np.array_equal(before,np.asarray(Image.open(source)))
  palette_records.append({'file':source.name,'indices_sha256':hashlib.sha256(before.tobytes()).hexdigest(),'file_sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
(P/'BRINK-PALETT-KONTROLL.json').write_text(json.dumps({'source_room':105,'source_palette':0,'route':'AKPL original costume slot -> original room105 palette0','script_proof':['room038-LSCR-28630785.txt chooses15/16/17 from bitvars18/19, then shadowMode1','room105-LSCR-85186826.txt explicitly uses costume17 in crystal-machine dialogue'],'actual_indices_unchanged':True,'files':palette_records},indent=2));print('Verified contextual palette metadata',len(palette_records))
