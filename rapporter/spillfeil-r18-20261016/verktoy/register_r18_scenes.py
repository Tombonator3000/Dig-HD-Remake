"""Register generated art against original game geometry; never change indices."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,cv2,sys,os,shutil,json
R=Path(__file__).resolve().parent;P=R/'grafikk/rapporter/spillfeil-r18-20261016';O=P/'mod-overrides';M=R/'kandidat-r18';B=R/'hd-integrert';S=R/'testing/source/costumes';A=P/'produksjon';records=[]
sys.path.insert(0,str(R/'kode/pipeline'))
from dighd import gamedata as g
G=Path('/home/tom/Documents/Codex/2026-10-16-the-dig-hd-remake-sp-rsm/testing/linux-release/AppDir/usr/share/the-dig-hd/game');data=(G/'DIG.LA1').read_bytes();ix=g.read_index(G/'DIG.LA0');rooms=g.read_rooms(G/'DIG.LA1')
def save(im,name):
 f=O/name;f.parent.mkdir(parents=True,exist_ok=True);im.save(f);t=M/name;t.parent.mkdir(parents=True,exist_ok=True);tmp=t.with_suffix('.new.png');shutil.copy2(f,tmp);os.replace(tmp,t);records.append(name)
def palidx(cid,cell,room):
 src=Image.open(S/f'costume{cid:03d}_{cell:03d}_idx.png');rn,off=ix.costume_dir[cid];p=rooms[rn].offset+off;bl={t:data[o+8:o+n] for t,o,n in g.children(data,p+8,p+g.be32(data,p+4))};pal=rooms[room].palettes[0];colors=[]
 for i in bl[b'AKPL']:colors+=list(pal[i*3:i*3+3])
 src.putpalette(colors+[0]*(768-len(colors)));return src
# Two genuinely separate moon actors. Keep their independent alpha and original actor positions.
master=Image.open(A/'moons-master.png').convert('RGBA')
for cid,half in [(148,0),(149,1)]:
 alpha=np.asarray(master)[:,:,3];n,labels,stats,_=cv2.connectedComponentsWithStats((alpha>128).astype('uint8'),8);components=sorted(range(1,n),key=lambda i:stats[i,cv2.CC_STAT_AREA],reverse=True)[:2];components.sort(key=lambda i:stats[i,cv2.CC_STAT_LEFT]);x,y,wc,hc,_=stats[components[half]];tile=master.crop((int(x),int(y),int(x+wc),int(y+hc)))
 for f in sorted(S.glob(f'costume{cid:03d}_*_idx.png')):
  cell=int(f.stem.split('_')[1]);src=palidx(cid,cell,55);w,h=src.size;a=np.asarray(src);yy,xx=np.where(a>1)
  if not len(xx):continue
  box=(int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1));art=Image.new('RGBA',((w+16)*4,(h+16)*4));art.alpha_composite(tile.resize(((box[2]-box[0])*4,(box[3]-box[1])*4),Image.Resampling.LANCZOS),((box[0]+8)*4,(box[1]+8)*4));stem=f'costumes/costume{cid:03d}_{cell:03d}';save(src,stem+'_idx.png');save(art,stem+'_hd.png');save(art.crop((32,32,(w+8)*4,(h+8)*4)),stem+'.png')
# Shared plateau texture for every opaque object tile, exact match outside original state changes.
bg=Image.open(A/'plateau-master.png').convert('RGB').resize((1280,960),Image.Resampling.LANCZOS);hole=Image.open(A/'plateau-hole-master.png').convert('RGB').resize(bg.size,Image.Resampling.LANCZOS);save(bg,'rooms/room055.png')
oldbg=Image.open(B/'rooms/room055.png').convert('RGB');idxbg=np.asarray(Image.open(B/'rooms/room055_idx.png'))
for obj in rooms[55].objects:
 if obj.obj_id not in [387,388]:continue
 for state in obj.states:
  stem=f'objects/obj{obj.obj_id:03d}_{state}';idx=Image.open(B/(stem+'_idx.png'));w,h=idx.size;x,y=obj.x,obj.y;box=(x*4,y*4,(x+w)*4,(y+h)*4);base=bg.crop(box);mask=(np.asarray(idx)!=idxbg[y:y+h,x:x+w]).astype('uint8')*255;mask=Image.fromarray(mask).resize(base.size,Image.Resampling.NEAREST).filter(ImageFilter.GaussianBlur(2))
  if obj.obj_id==387:changed=hole.crop(box)
  else:
   old=np.asarray(Image.open(B/(stem+'.png')).convert('RGB')).astype(float);ob=np.asarray(oldbg.crop(box)).astype(float);nb=np.asarray(base).astype(float);changed=Image.fromarray(np.clip(nb+old-ob,0,255).astype('uint8'))
  result=Image.composite(changed,base,mask).convert('RGBA');save(result,stem+'.png');save(idx,stem+'_idx.png')
# Laser textures are generated light only; PCA registers endpoints of all original directions.
beam=Image.open(A/'laser-master.png').convert('RGBA');aa=np.asarray(beam)[:,:,3];yy,xx=np.where(aa>150);beam=beam.crop((int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)))
for cid in [233,234,235]:
 for f in sorted(S.glob(f'costume{cid:03d}_*_idx.png')):
  c=int(f.stem.split('_')[1]);src=palidx(cid,c,85);a=np.asarray(src);w,h=src.size;ys,xs=np.where(a>=(3 if cid==233 else 4));points=np.stack([xs,ys],1).astype('float32');mu=points.mean(0);_,_,v=np.linalg.svd(points-mu,full_matrices=False);axis=v[0];t=(points-mu)@axis;start=mu+axis*t.min();end=mu+axis*t.max();vec=end-start;length=float(np.linalg.norm(vec))*4;strip=beam.resize((max(2,round(length)),7),Image.Resampling.LANCZOS);theta=np.degrees(np.arctan2(-vec[1],vec[0]));rot=strip.rotate(float(theta),Image.Resampling.BICUBIC,expand=True);center=(start+end)*2+32;art=Image.new('RGBA',((w+16)*4,(h+16)*4));art.alpha_composite(rot,(round(center[0]-rot.width/2),round(center[1]-rot.height/2)));stem=f'costumes/costume{cid:03d}_{c:03d}';save(src,stem+'_idx.png');save(art,stem+'_hd.png');save(art.crop((32,32,(w+8)*4,(h+8)*4)),stem+'.png')
# Giant-spider silhouette. Same source canvas, bounding box and walk phase order.
master=Image.open(A/'spider-master.png').convert('RGBA');tiles=[]
for j in range(8):
 tile=master.crop((j%4*master.width//4,j//4*master.height//2,(j%4+1)*master.width//4,(j//4+1)*master.height//2));tiles.append(tile.crop(tile.getchannel('A').getbbox()))
for f in sorted(S.glob('costume136_*_idx.png')):
 c=int(f.stem.split('_')[1]);src=palidx(136,c,44);a=np.asarray(src);w,h=src.size;ys,xs=np.where(a>1)
 if len(xs)<4:continue
 box=(int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1));tile=tiles[c%8].resize(((box[2]-box[0])*4,(box[3]-box[1])*4),Image.Resampling.LANCZOS);art=Image.new('RGBA',((w+16)*4,(h+16)*4));art.alpha_composite(tile,((box[0]+8)*4,(box[1]+8)*4));stem=f'costumes/costume136_{c:03d}';save(src,stem+'_idx.png');save(art,stem+'_hd.png');save(art.crop((32,32,(w+8)*4,(h+8)*4)),stem+'.png')
# Closed and opened states share exact original rectangular placement.
new=Image.open(A/'grate-closed-master.png').convert('RGBA').resize((320,352),Image.Resampling.LANCZOS);old=Image.open(B/'objects/obj357_01.png').convert('RGBA');yy,xx=np.mgrid[:352,:320];edge=np.minimum.reduce([xx,319-xx,yy,351-yy]);mask=Image.fromarray((np.clip(edge/6,0,1)*255).astype('uint8'));closed=Image.composite(new,old,mask);save(closed,'objects/obj357_01.png');save(closed.crop((64,0,256,128)),'objects/obj356_01.png')
for name in ['obj356_01','obj357_01']:save(Image.open(B/f'objects/{name}_idx.png'),f'objects/{name}_idx.png')
(P/'SCENE-REGISTRATION.json').write_text(json.dumps(records,indent=2));print(len(records),'scene files registered')
