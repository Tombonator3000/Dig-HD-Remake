from pathlib import Path
from PIL import Image,ImageFilter
import numpy as np,shutil,os,sys
R=Path(__file__).resolve().parent;P=R/'grafikk/rapporter/spillfeil-r17-20261016';S=P/'produksjon';O=P/'mod-overrides';M=R/'kandidat-r17';B=R/'hd-integrert'
def save(im,kind,name):
 dest=O/kind/name;dest.parent.mkdir(exist_ok=True,parents=True);im.save(dest);temp=M/kind/(name+'.new');shutil.copy2(dest,temp);os.replace(temp,M/kind/name)
def bbox(im):
 a=np.asarray(im)[:,:,3];yy,xx=np.where(a>128);return int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)
water=R/'testing/r17-water-source';water.mkdir(exist_ok=True)
for f in (B/'costumes').glob('costume301*_idx.png'):
 shutil.copy2(f,water/f.name);Image.open(f).convert('RGBA').save(water/f.name.replace('_idx',''))
from register_r17_water import register
register(water,S/'vann-master.png',O/'costumes')
for f in (O/'costumes').glob('costume301*'):
 temp=M/'costumes'/(f.name+'.new');shutil.copy2(f,temp);os.replace(temp,M/'costumes'/f.name)
master=S/'scepters-master.png'
if not master.exists():shutil.copy2('/home/tom/.codex/generated_images/01a143a5-2c2d-7dc3-9827-943c3e7c6e0e/exec-9fff589b-7522-43bb-8a60-188f1f652186.png',master)
a=Image.open(master).convert('RGBA')
for j,oid in enumerate([864,667]):
 t=a.crop((j*a.width//2,0,(j+1)*a.width//2,a.height));t=t.crop(bbox(t))
 for idx in (B/'objects').glob(f'obj{oid:03d}_*_idx.png'):
  src=Image.open(idx).convert('RGBA');x,y,rr,bb=bbox(src);state=int(idx.stem.split('_')[1]);height=(bb-y)*4;tw=max(8,round(height*t.width/t.height));art=t.resize((tw,height),Image.Resampling.LANCZOS)
  if state==2:
   al=art.getchannel('A');edge=np.maximum(np.asarray(al.filter(ImageFilter.MaxFilter(5))).astype(int)-np.asarray(al).astype(int),0).astype('uint8');halo=Image.new('RGBA',art.size,(40,35,255,0));halo.putalpha(Image.fromarray(edge));halo.alpha_composite(art);art=halo
  for suffix in ['', '_hd']:
   name=idx.name.replace('_idx',suffix);f=B/'objects'/name
   if not f.exists():continue
   old=Image.open(f).convert('RGBA');px=(old.width//4-src.width)//2;py=(old.height//4-src.height)//2;out=Image.new('RGBA',old.size);out.alpha_composite(art,((x+px)*4+((rr-x)*4-tw)//2,(y+py)*4));save(out,'objects',name)
print('water and scepters imported')
