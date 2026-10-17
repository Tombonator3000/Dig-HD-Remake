import os
"""Register original library lighting updates over the painted HD room.

These MajMin cels are changed-pixel patches, not new free-standing objects.
Larger patches keep the HD room texture and transfer the original light delta.
Tiny repeated sparks/strips retain source geometry and palette mechanically.
"""
from pathlib import Path
import sys,json,shutil,os,hashlib
import numpy as np,cv2
from PIL import Image,ImageDraw
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));sys.path.insert(0,str(R/'kode/pipeline'))
from dighd import myk
P=R/'grafikk/rapporter/restgrafikk-r19-20261016';S=R/'testing/source/costumes';B=R/'hd-leveranse';O=P/'mod-tillegg/costumes';M=R/'kandidat-r19/costumes'
original=np.array(Image.open(B/'rooms/room092_idx.png').convert('RGBA'));painted=np.array(Image.open(B/'rooms/room092.png').convert('RGBA'));assert painted.shape[:2]==(original.shape[0]*4,original.shape[1]*4)
records=[]
for cid in [266,267]:
 placements=json.loads((P/f'library{cid}-source-placement.json').read_text());bycell={}
 for r in placements:bycell.setdefault(r['cel'],[]).append(r)
 for f in sorted(S.glob(f'costume{cid}_*_idx.png')):
  hd=f.name.replace('_idx','_hd');assert not (B/'costumes'/hd).exists()
  src=np.array(Image.open(f).convert('RGBA'));h,w=src.shape[:2];mask=src[:,:,3]>128;area=int(mask.sum());n=int(f.stem.split('_')[1]);placements=bycell.get(n,[])
  if cid==266 or area<40:
   result=myk.from_original(src)['bilde'];method='technical dark detail, spark or update strip, source-preserving soft resampling';where=None
  else:
   assert len(placements)==1 and placements[0]['unique_positions']==1,(f,placements)
   x,y=placements[0]['xy'];assert x>=0 and y>=0 and x+w<=original.shape[1] and y+h<=original.shape[0]
   old=original[y:y+h,x:x+w,:3].astype('float32');native=painted[y*4:(y+h)*4,x*4:(x+w)*4].copy()
   # Only the original illumination change is transferred. No old room
   # texture or character pixels are pasted over the new painted scene.
   delta=src[:,:,:3].astype('float32')-old;weight=cv2.GaussianBlur(mask.astype('float32'),(0,0),1.1)
   delta=cv2.GaussianBlur(delta*mask[:,:,None],(0,0),1.1)/np.maximum(weight[:,:,None],1e-5)
   light=cv2.resize(delta,(w*4,h*4),interpolation=cv2.INTER_CUBIC);native[:,:,:3]=np.clip(native[:,:,:3].astype('float32')+light,0,255).astype('uint8')
   # The scene already supplies the same HD texture below the alpha edge,
   # so softened changed-pixel coverage cannot reveal an old painted matte.
   coverage=cv2.GaussianBlur(mask.astype('float32'),(0,0),.55);coverage=cv2.resize(coverage,(w*4,h*4),interpolation=cv2.INTER_CUBIC);native[:,:,3]=np.rint(np.clip(coverage,0,1)*255).astype('uint8')
   result=np.zeros(((h+8)*4,(w+8)*4,4),'uint8');result[16:-16,16:-16]=native;method='existing painted HD room texture plus original smoothed illumination delta and source phase coverage';where=[x,y]
  Image.fromarray(result).save(O/hd)
  for source,name in [(O/hd,hd),(f,f.name)]:
   if (B/'costumes'/name).exists():continue
   if source!=O/hd:shutil.copy2(source,O/name)
   tmp=M/(name+'.new');shutil.copy2(source,tmp);os.replace(tmp,M/name)
  records.append(dict(file=hd,pixels=area,method=method,source_position=where,hd_reference='rooms/room092.png',sha256=hashlib.sha256((O/hd).read_bytes()).hexdigest()))
(P/'library-registration.json').write_text(json.dumps(records,indent=2)+'\n');print(len(records),'library light phases registered;',sum(v['source_position'] is not None for v in records),'with HD room texture')
preview=Image.fromarray(painted).convert('RGBA')
for n in [159]:
 row=next(v for v in records if v['file']==f'costume267_{n:03d}_hd.png');x,y=row['source_position'];preview.alpha_composite(Image.open(O/row['file']).convert('RGBA'),(x*4-16,y*4-16))
preview.save(P/'library-light-preview.png')
