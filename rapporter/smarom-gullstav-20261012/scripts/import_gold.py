from pathlib import Path
from PIL import Image,ImageFilter
import numpy as np,sys,shutil,json,hashlib
Q=Path(__file__).resolve().parent;T=Q.parent;G=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk');R=G/'rapporter/smarom-gullstav-20261012';M=Path('/home/tombonator3000t/Skrivebord/TheDigHD-Linux-20261012-test/usr/share/the-dig-hd/mods/gpt');sys.path[:0]=[str(T/'code/pipeline'),str(T/'deps')];from dighd import gamedata
pals=gamedata.read_rooms(Path('/home/tombonator3000t/Skrivebord/TheDigHD-Linux-20261012-test/usr/share/the-dig-hd/game/DIG.LA1'))[50].palettes;gold=np.frombuffer(pals[3],np.uint8).reshape(256,3)
raw=Path('/home/tombonator3000t/.codex/generated_images/01a12ef9-b3db-7603-9fd9-e7f8474c5dcf/exec-dcc3d5f3-2c83-46b5-9c02-e8c3fcfd570c.png');(R/'assets').mkdir(exist_ok=True);shutil.copy2(raw,R/'assets/gullstav-generert.png');new=Image.open(raw).convert('RGB').resize((1280,800),Image.Resampling.LANCZOS)
records=[]
for n in ['rooms/room050','objects/obj884_01','objects/obj884_02','objects/obj884_03']:
 f=M/(n+'.png');idx=M/(n+'_idx.png');backup=Q/'gold-before'/n;backup.parent.mkdir(parents=True,exist_ok=True)
 for src in [f,idx]:
  dest=backup.with_name(src.name)
  if not dest.exists():shutil.copy2(src,dest)
 original=Image.open(backup.with_suffix('.png')).convert('RGBA');ixim=Image.open(backup.with_name(idx.name));ix=np.array(ixim);mask=Image.fromarray(((ix>=240)&(ix<=253)).astype(np.uint8)*255).resize(original.size,Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(0.7))
 # Only generated rod pixels, clipped to the native silhouette; original hand, crystals and background are preserved.
 insert=new if n.startswith('rooms/') else new.crop((0,352,640,800))
 out=Image.composite(insert.convert('RGBA'),original,mask);out.putalpha(original.getchannel('A'));out.save(f)
 pal=np.array(ixim.getpalette(),np.uint8).reshape(256,3);pal[240:256]=gold[240:256];ixim.putpalette(pal.ravel().tolist());ixim.save(idx)
 assert np.array_equal(np.array(Image.open(idx)),ix)
 records.append({'file':str(f.relative_to(M)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'palette_file':str(idx.relative_to(M)),'palette_sha256':hashlib.sha256(idx.read_bytes()).hexdigest(),'index_data_unchanged':True,'mask_native_indices':[240,253]})
(R/'GULLSTAV-IMPORT.json').write_text(json.dumps({'raw':str(raw),'raw_saved':'assets/gullstav-generert.png','raw_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'base_palette':'native room050 palette3, indices240..255, all other entries unchanged; game palette unchanged','records':records},indent=2)+'\n');print(json.dumps(records),flush=True)
