import os
from pathlib import Path
import sys,json,hashlib,shutil,os
import numpy as np,cv2
from PIL import Image,ImageDraw
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]))
sys.path.insert(0,str(R/'kode/pipeline'))
from dighd import myk
P=R/'grafikk/rapporter/restgrafikk-r19-20261016';S=R/'testing/source/costumes';B=R/'hd-leveranse/costumes';O=P/'mod-tillegg/costumes';M=R/'kandidat-r19/costumes'
plans=json.loads((P/'maggie328-plans.json').read_text());tiles={};records=[]
def components(a,limit):
 n,l,stats,centers=cv2.connectedComponentsWithStats((a[:,:,3]>128).astype('uint8'),8)
 return l,sorted([i for i in range(1,n) if stats[i,4]>=limit],key=lambda i:-stats[i,4]),stats
for batch in plans:
 f=P/f'maggie328-{batch["batch"]}-master.png';a=np.array(Image.open(f).convert('RGBA'));H,W=a.shape[:2]
 for c in batch['cells']:
  s=c['slot'];x0=round(s%4*W/4);x1=round((s%4+1)*W/4);y0=round(s//4*H/2);y1=round((s//4+1)*H/2)
  t=a[y0:y1,x0:x1].copy();owner,lab,found=myk.parts(t[:,:,3]);ids=sorted([v for v in found if v['areal']>=20],key=lambda v:-v['areal']);parts=[]
  for v in ids:
   x,y,w,h=v['boks'];crop=t[y:y+h,x:x+w].copy();crop[owner[y:y+h,x:x+w]!=v['nr']]=0
   parts.append(dict(image=crop,bbox=[x0+x,y0+y,w,h],area=v['areal']))
  tiles[c['file']]=dict(parts=parts,batch=batch['batch'],native_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),native_size=[W,H])
for name,info in tiles.items():
 src=np.array(Image.open(S/name).convert('RGBA'));h,w=src.shape[:2];l,ids,stats=components(src,4);out=Image.new('RGBA',((w+8)*4,(h+8)*4));notes=[]
 if name in ['costume328_018_idx.png','costume328_024_idx.png']:
  # Narrow, intentionally clipped flesh strips have no complete drawing.
  # Preserve their exact coverage as explicit source fragments, not new art.
  result=myk.from_original(src);out=Image.fromarray(result['bilde']);notes=[dict(source_fragment=True,pixels=int((src[:,:,3]>0).sum()))]
 else:
  for rank,i in enumerate(ids):
   x,y,sw,sh=map(int,stats[i,:4]);area=int(stats[i,4]);reuse=None
   if area<20:
    fragment=src.copy();fragment[l!=i]=0;small=Image.fromarray(myk.from_original(fragment)['bilde']);out.alpha_composite(small,(8,8));notes.append(dict(source_fragment=True,source_bbox=[x,y,sw,sh]));continue
   if rank<len(info['parts']):part=info['parts'][rank]
   else:
    # Two native phases omitted the cropped right-edge hand sliver.
    # Reuse the neighboring drawn sliver, not a whole invented hand.
    assert rank==1 and sw<=16,(name,rank,sw)
    part=tiles['costume328_009_idx.png']['parts'][1];reuse='costume328_009_idx.png'
   fitted=myk._premul_resize(part['image'],(sw*4,sh*4))
   out.alpha_composite(Image.fromarray(fitted),((x+4)*4,(y+4)*4))
   notes.append(dict(source_bbox=[x,y,sw,sh],native_bbox=part['bbox'],native_reuse=reuse))
 for cid in [328,329]:
  target=name.replace('costume328',f'costume{cid}');other=np.array(Image.open(S/target).convert('RGBA'));assert np.array_equal(src,other),(name,target)
  hd=target.replace('_idx','_hd')
  if (B/hd).exists() or (B/target.replace('_idx','')).exists():continue
  out.save(O/hd)
  for source,dest in [(O/hd,hd),(S/target,target)]:
   if (B/dest).exists():continue
   if source!=O/hd:shutil.copy2(source,O/dest)
   tmp=M/(dest+'.new');shutil.copy2(source,tmp);os.replace(tmp,M/dest)
  records.append(dict(file=hd,source=name,batch=info['batch'],native_size=info['native_size'],native_sha256=info['native_sha256'],parts=notes,sha256=hashlib.sha256((O/hd).read_bytes()).hexdigest()))
(P/'maggie-registration.json').write_text(json.dumps(records,indent=2)+'\n');print(len(records),'Maggie phases registered')
preview=Image.new('RGB',(1600,1200),(36,45,56));d=ImageDraw.Draw(preview)
for j,n in enumerate([3,4,11,15,18,19,24,25,27,30,32,37]):
 x=j%4*400;y=j//4*400;name=f'costume328_{n:03d}';old=Image.open(S/(name+'_idx.png')).convert('RGBA');new=Image.open(O/(name+'_hd.png')).convert('RGBA')
 old.thumbnail((180,350));new.thumbnail((180,350));preview.paste(old,(x,y+35),old);preview.paste(new,(x+195,y+35),new);d.text((x+5,y+5),name,fill='white')
preview.save(P/'maggie-registration-preview.png')
