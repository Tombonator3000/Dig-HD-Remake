from pathlib import Path
from PIL import Image,ImageFilter
from bleed_rgba import bleed
import numpy as np,json,shutil,hashlib
Q=Path(__file__).resolve().parent;G=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk');R=G/'rapporter/smarom-gullstav-20261012';sources=json.loads((Q/'detail-sources.json').read_text());assets=R/'assets';assets.mkdir(exist_ok=True);images={};provenance=[]
for k,d in sources.items():
 src=Path(d['path']);shutil.copy2(src,assets/(k+'.png'));(R/(k+'-prompt.txt')).write_text(d['prompt']+'\n');images[k]=Image.open(src).convert('RGBA');d.update(saved='assets/'+k+'.png',sha256=hashlib.sha256(src.read_bytes()).hexdigest())
# Exact native positions and alpha act as the atlas placement contract. All painted RGB is generated artwork.
bar=images['bar219'];aa=np.array(bar.getchannel('A'));ys,xs=np.where(aa>240);bar=bar.crop((int(xs.min())+3,int(ys.min()),int(xs.max())-2,int(ys.max())+1))
for j,base,parts in [
 ('lag025_01_del1av3','/home/tombonator3000t/.codex/generated_images/01a12ef9-b3db-7603-9fd9-e7f8474c5dcf/exec-b636ca77-9026-4806-89e4-22d74ef50031.png',['obj218_01','obj219_01']),
 ('lag026_03_del2av3',None,['obj224_01','obj226_01','obj227_01']),
 ('lag032_05',None,['obj257_01']),('lag032_07',None,['obj257_02'])]:
 d=json.loads((G/'jobber'/j/'jobb.json').read_text());canvas=Image.open(base or G/d['bilde_to']).convert('RGBA');assert canvas.size==(1536,1024);used=[]
 for n in parts:
  p=next(x for x in d['objekter'] if x['bilde']==n);src=Image.open(Q/'extract/objects'/f'{n}.png').convert('RGBA');a=src.getchannel('A');box=a.getbbox();rgb=Image.new('RGBA',(src.width*4,src.height*4),(0,0,0,0))
  if n.startswith('obj257'):
   painting=images['strip25701' if n.endswith('01') else 'isolated257'];pa=np.array(painting.getchannel('A'))>200
   # Both source and generated artwork have two disconnected strips. Scale their painted surfaces separately to the original strip bounds.
   for lo,hi in [(0,16),(16,32)]:
    nm=np.array(a)[lo:hi]>0;yy,xx=np.where(nm);nb=(int(xx.min()),int(yy.min())+lo,int(xx.max())+1,int(yy.max())+lo+1)
    gl,gh=(0,painting.height//2) if lo==0 else (painting.height//2,painting.height);gy,gx=np.where(pa[gl:gh]);gb=(int(gx.min()),int(gy.min())+gl,int(gx.max())+1,int(gy.max())+gl+1)
    tile=bleed(painting.crop(gb)).resize(((nb[2]-nb[0])*4,(nb[3]-nb[1])*4),Image.Resampling.LANCZOS);rgb.paste(tile,(nb[0]*4,nb[1]*4))
  else:
   tile=bar.resize(((box[2]-box[0])*4,(box[3]-box[1])*4),Image.Resampling.LANCZOS);rgb.paste(tile,(box[0]*4,box[1]*4))
  # Same source alpha that the existing importer uses, with antialiasing for the master canvas.
  alpha=a.resize(rgb.size,Image.Resampling.BICUBIC);rgb.putalpha(alpha)
  x,y,w,h=p['rekt'];rx,ry,_,_=d['region'];px,py=d['plassering'];dest=((x-rx+px)*4,(y-ry+py)*4);canvas.alpha_composite(rgb,dest=dest);used.append({'object':n,'dest':dest,'native_alpha_bbox':box,'source': 'strip25701' if n=='obj257_01' else 'isolated257' if n=='obj257_02' else 'bar219'})
 out=Q/(j+'-assembled.png');canvas.convert('RGB').save(out);provenance.append({'job':j,'canvas':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'parts':used,'method':'technical atlas placement only; generated surfaces fitted to exact native alpha bounds; no code-painted content'})
(R/'DETAIL-ATLAS.json').write_text(json.dumps({'sources':sources,'masters':provenance},ensure_ascii=False,indent=2)+'\n');print(json.dumps(provenance),flush=True)
