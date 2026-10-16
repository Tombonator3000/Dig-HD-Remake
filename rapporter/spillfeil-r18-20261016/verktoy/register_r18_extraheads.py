from pathlib import Path
from PIL import Image
import numpy as np,json,os,shutil
R=Path(__file__).resolve().parent;P=R/'grafikk/rapporter/spillfeil-r18-20261016';O=P/'mod-overrides/costumes';B=R/'hd-integrert/costumes';M=R/'kandidat-r18/costumes';S=R/'testing/source/costumes';A=json.loads((R/'testing/anims.json').read_text());records=[]
def bbox(m):
 y,x=np.where(m);return int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)
def norm(im):
 a=np.asarray(im.convert('RGBA')).copy();m=(a[:,:,3]>128)&~((a[:,:,0]>180)&(a[:,:,2]>150)&(a[:,:,1]<100));a[~m,3]=0;t=Image.fromarray(a).crop(bbox(m)).resize((32,32));q=np.asarray(t).astype(float)/255;return q[:,:,:3]*q[:,:,3,None]
for label,main,ids in [('boston',14,[38]),('brink',15,[48,188]),('maggie',18,[47])]:
 atlas=Image.open(R/f'grafikk/rapporter/spillfeil-20261016/produksjon/{label}-heads.png').convert('RGBA');tiles={};refs={}
 for row in range(3):
  for di in range(8):
   t=atlas.crop((round(di*atlas.width/8),round(row*atlas.height/3),round((di+1)*atlas.width/8),round((row+1)*atlas.height/3)));tiles[row,di]=t.crop(bbox(np.asarray(t)[:,:,3]>128))
 for a in A[str(main)]['animasjoner']:
  if a['animasjon']==1 and a['lag']==1:refs[a['retning']]=norm(Image.open(B/f"costume{main:03d}_{a['ruter'][-1]:03d}_idx.png"))
 for cid in ids:
  for f in S.glob(f'costume{cid:03d}_*_idx.png'):
   src=Image.open(f).convert('RGBA');w,h=src.size
   if not(6<=w<=27 and 6<=h<=23):continue
   name=f.name.replace('_idx','_hd');old=B/name
   if not old.exists():continue
   m=np.asarray(src)[:,:,3]>128;valid=m&~((np.asarray(src)[:,:,0]>180)&(np.asarray(src)[:,:,2]>150)&(np.asarray(src)[:,:,1]<100))
   if valid.sum()<15:continue
   score={di:float(((norm(src)-q)**2).mean()) for di,q in refs.items()};di=min(score,key=score.get);box=bbox(valid);art=Image.open(old).convert('RGBA');pad=((art.width//4-w)//2,(art.height//4-h)//2);tile=tiles[1,di].resize(((box[2]-box[0])*4,(box[3]-box[1])*4+6),Image.Resampling.LANCZOS);out=Image.new('RGBA',art.size);out.alpha_composite(tile,((box[0]+pad[0])*4,(box[1]+pad[1])*4));out.save(O/name);tmp=M/(name+'.new');shutil.copy2(O/name,tmp);os.replace(tmp,M/name);records.append({'file':name,'direction':di,'source_template_error':score[di],'atlas':f'{label}-heads.png','neck_extension_hd':6})
(P/'EXTRA-HEADS.json').write_text(json.dumps(records,indent=2));print(len(records),'additional independent heads registered')
