import os
from pathlib import Path
from PIL import Image,ImageFilter
import numpy as np,cv2,json,os,shutil,hashlib
R=Path(os.environ.get("DIGHD_WORKSPACE",Path.cwd()));M=R/'kandidat-mod';P=R/'grafikk/rapporter/spillfeil-20261016';S=P/'produksjon';O=P/'mod-overrides';records=[]
def maskbox(im):
 a=np.asarray(im);y,x=np.where(a[:,:,3]>128);return int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)
def save(im,kind,name,info):
 dest=O/kind/name;dest.parent.mkdir(exist_ok=True,parents=True);im.save(dest);tmp=M/kind/(name+'.new');shutil.copy2(dest,tmp);os.replace(tmp,M/kind/name);records.append({'file':str(Path(kind)/name),**info})
for label,cols,rows in [('boston103',6,4),('brink67',6,7)]:
 master=S/(label+'-master.png')
 if not master.exists():continue
 plan=json.loads((S/(label+'-plan.json')).read_text());atlas=Image.open(master).convert('RGBA')
 for j,p in enumerate(plan):
  f=M/'costumes'/p['file'];src=Image.open(f);name=f.name.replace('_idx','_hd');old=Image.open(M/'costumes'/name);px=(old.width//4-src.width)//2;py=(old.height//4-src.height)//2;x,y,rr,bb=p['bbox'];t=atlas.crop((round(j%cols*atlas.width/cols),round(j//cols*atlas.height/rows),round((j%cols+1)*atlas.width/cols),round((j//cols+1)*atlas.height/rows)));t=t.crop(maskbox(t)).resize(((rr-x)*4,(bb-y)*4),Image.Resampling.LANCZOS);out=Image.new('RGBA',old.size);out.alpha_composite(t,((x+px)*4,(y+py)*4));save(out,'costumes',name,{'master':master.name,'slot':j,'source_bbox':p['bbox'],'headless':p.get('headless',False)})
# The costume103 RGBS block is a placeholder skin ramp. In this action,
# the original game uses AKPL indices in the pool palette without remapping.
import sys
sys.path.insert(0,str(R/'kode/pipeline'))
from dighd import gamedata as g
G=Path('/home/tom/Documents/Codex/2026-10-16-the-dig-hd-remake-sp-rsm/testing/linux-release/AppDir/usr/share/the-dig-hd/game');d=(G/'DIG.LA1').read_bytes();ix=g.read_index(G/'DIG.LA0');rooms=g.read_rooms(G/'DIG.LA1');rn,ofs=ix.costume_dir[103];pos=rooms[rn].offset+ofs;b={t:d[o+8:o+n] for t,o,n in g.children(d,pos+8,pos+g.be32(d,pos+4))};pal=bytearray(768)
for i,v in enumerate(b[b'AKPL']):pal[i*3:i*3+3]=rooms[32].palettes[0][v*3:v*3+3]
for f in (M/'costumes').glob('costume103*_idx.png'):
 im=Image.open(f);before=np.asarray(im).copy();im.putpalette(pal);assert np.array_equal(before,np.asarray(im));save(im,'costumes',f.name,{'palette':'original AKPL in room32 palette0; RGBS placeholder discarded','original_indices_data_sha256':hashlib.sha256(before.tobytes()).hexdigest()})
# Geometric engraved rod icons, including their selected and disabled states.
atlas=Image.open(S/'rods-master.png').convert('RGBA')
for j,oid in enumerate([633,634,636,678]):
 t=atlas.crop((round(j*atlas.width/4),0,round((j+1)*atlas.width/4),atlas.height));t=t.crop(maskbox(t))
 for target in ([oid,652] if oid==634 else [oid]):
  for idx in sorted((M/'objects').glob(f'obj{target:03d}_*_idx.png')):
   src=Image.open(idx).convert('RGBA');x,y,r,b=src.getbbox();state=int(idx.stem.split('_')[1]);art=t.resize(((r-x)*4,(b-y)*4),Image.Resampling.LANCZOS);pix=np.asarray(art).copy()
   if state==3:pix[:,:,:3]=np.stack([pix[:,:,2]*.25,pix[:,:,2]*.4,np.maximum(pix[:,:,:3].max(2),70)],2).astype('uint8');art=Image.fromarray(pix)
   if state==2:
    al=art.getchannel('A');edge=np.asarray(al.filter(ImageFilter.MaxFilter(5)))-np.asarray(al);halo=Image.new('RGBA',art.size,(40,35,255,0));halo.putalpha(Image.fromarray(edge));halo.alpha_composite(art);art=halo
   for suffix in ['', '_hd']:
    base=M/'objects'/idx.name.replace('_idx',suffix)
    if not base.exists():continue
    old=Image.open(base).convert('RGBA');px=(old.width//4-src.width)//2;py=(old.height//4-src.height)//2;out=Image.new('RGBA',old.size);out.alpha_composite(art,((x+px)*4,(y+py)*4));save(out,'objects',base.name,{'master':'rods-master.png','slot':j,'state':state,'source_bbox':[x,y,r,b]})
# Save first pass records. Probe registration has its own reproducible receipt.
(P/'ACTION-REGISTRATION.json').write_text(json.dumps(records,indent=2));print(len(records),'actions, palettes and rod states imported')
