from pathlib import Path
from PIL import Image
import numpy as np,json,shutil,os
R=Path(__file__).resolve().parent;P=R/'grafikk/rapporter/spillfeil-r18-20261016';O=P/'mod-overrides/costumes';M=R/'kandidat-r18/costumes';B=R/'hd-integrert/costumes';src=R/'grafikk/rapporter/spillfeil-20261016';master=Image.open(src/'produksjon/brink-heads.png').convert('RGBA');tiles={}
for row in range(3):
 for di in range(8):
  im=master.crop((round(di*master.width/8),round(row*master.height/3),round((di+1)*master.width/8),round((row+1)*master.height/3)));a=np.asarray(im)[:,:,3];ys,xs=np.where(a>128);tiles[row,di]=im.crop((int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)))
records=[]
for rec in json.loads((src/'HEAD-REGISTRATION.json').read_text()):
 name=rec['file'];cid=int(name[7:10])
 if cid not in [16,17] or rec['kind'] not in ['independent_head','embedded_walk_head']:continue
 old=Image.open(B/name).convert('RGBA');di=rec['direction']
 if rec['kind']=='independent_head':
  x,y,w,h=rec['placement_hd'];tile=tiles[rec['expression'],di].resize((w,h),Image.Resampling.LANCZOS);out=Image.new('RGBA',old.size)
  if 'neck_contact_shift_hd' in rec:
   dx,dy=rec['neck_contact_shift_hd'];out.alpha_composite(tile,(x+32,y+32));out=out.transform(out.size,Image.Transform.AFFINE,(1,0,-dx,0,1,-dy),resample=Image.Resampling.BICUBIC)
  else:out.alpha_composite(tile,(x,y))
  a=np.asarray(out)[:,:,3];ys,xs=np.where(a>128);box=(int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1));tile=out.crop(box);split=round(tile.height*.7);out=Image.new('RGBA',old.size);out.alpha_composite(tile.crop((0,0,tile.width,split)),(box[0],box[1]));out.alpha_composite(tile.crop((0,split,tile.width,tile.height)).resize((tile.width,tile.height-split+6),Image.Resampling.BICUBIC),(box[0],box[1]+split))
 else:
  left,top,tw,th=rec['head_region_source'];idx=Image.open(B/name.replace('_hd','_idx'));pad=((old.width//4-idx.width)//2,(old.height//4-idx.height)//2);out=old.copy();out.paste((0,0,0,0),(max(0,(left+pad[0]-3)*4),max(0,(pad[1]-2)*4),min(out.width,(left+pad[0]+tw+3)*4),min(out.height,(pad[1]+th)*4)));tile=tiles[0,di].resize((tw*4,(th+1)*4),Image.Resampling.LANCZOS);out.alpha_composite(tile,((left+pad[0])*4,pad[1]*4))
 out.save(O/name);tmp=M/(name+'.new');shutil.copy2(O/name,tmp);os.replace(tmp,M/name);records.append({'file':name,'change':'remove duplicate manual skin desaturation; preserve approved atlas colors and runtime palette mapping','kind':rec['kind']})
(P/'BRINK-COLOR-REGISTRATION.json').write_text(json.dumps(records,indent=2));print(len(records),'Brink head colors corrected')
