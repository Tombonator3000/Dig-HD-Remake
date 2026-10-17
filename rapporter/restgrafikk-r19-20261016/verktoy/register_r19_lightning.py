import os
"""Register lightning phase deltas over the existing painted connect-room sky.
All large patches were located by forcing each original right-facing chore.
Small sparks preserve the source signal; this is material reuse, not new art.
"""
from pathlib import Path
import sys,json,shutil,os,hashlib
import numpy as np,cv2
from PIL import Image
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));sys.path.insert(0,str(R/'kode/pipeline'))
from dighd import myk
P=R/'grafikk/rapporter/restgrafikk-r19-20261016';S=R/'testing/source/costumes';B=R/'hd-leveranse';O=P/'mod-tillegg/costumes';M=R/'kandidat-r19/costumes'
old=np.array(Image.open(B/'rooms/room030_idx.png').convert('RGBA'));new=np.array(Image.open(B/'rooms/room030.png').convert('RGBA'));assert new.shape[:2]==(old.shape[0]*4,old.shape[1]*4)
where={r['cel']:r for r in json.loads((P/'connect095-source-placement.json').read_text())};records=[]
for f in sorted(S.glob('costume095_*_idx.png')):
 src=np.array(Image.open(f).convert('RGBA'));h,w=src.shape[:2];mask=src[:,:,3]>128;area=int(mask.sum());n=int(f.stem.split('_')[1]);hd=f.name.replace('_idx','_hd');assert not (B/'costumes'/hd).exists()
 if area<40:
  result=myk.from_original(src)['bilde'];method='small original spark or light update fragment, soft resampling';xy=None
 else:
  pos=where[n];assert pos['unique_positions']==1,pos;x,y=pos['xy'];assert 0<=x and 0<=y and x+w<=old.shape[1] and y+h<=old.shape[0],pos
  base=old[y:y+h,x:x+w,:3].astype('float32');native=new[y*4:(y+h)*4,x*4:(x+w)*4].copy()
  delta=src[:,:,:3].astype('float32')-base;weight=cv2.GaussianBlur(mask.astype('float32'),(0,0),1.1)
  delta=cv2.GaussianBlur(delta*mask[:,:,None],(0,0),1.1)/np.maximum(weight[:,:,None],1e-5)
  light=cv2.resize(delta,(w*4,h*4),interpolation=cv2.INTER_CUBIC);native[:,:,:3]=np.clip(native[:,:,:3].astype('float32')+light,0,255).astype('uint8')
  coverage=cv2.resize(cv2.GaussianBlur(mask.astype('float32'),(0,0),.65),(w*4,h*4),interpolation=cv2.INTER_CUBIC);native[:,:,3]=np.rint(np.clip(coverage,0,1)*255).astype('uint8')
  result=np.zeros(((h+8)*4,(w+8)*4,4),'uint8');result[16:-16,16:-16]=native;method='existing painted HD sky plus original smoothed lightning phase delta and coverage';xy=[x,y]
 Image.fromarray(result).save(O/hd)
 for source,name in [(O/hd,hd),(f,f.name)]:
  if (B/'costumes'/name).exists():continue
  if source!=O/hd:shutil.copy2(source,O/name)
  tmp=M/(name+'.new');shutil.copy2(source,tmp);os.replace(tmp,M/name)
 records.append(dict(file=hd,pixels=area,source_position=xy,method=method,hd_reference='rooms/room030.png',sha256=hashlib.sha256((O/hd).read_bytes()).hexdigest()))
(P/'lightning-registration.json').write_text(json.dumps(records,indent=2)+'\n');print(len(records),'lightning patches,',sum(v['source_position'] is not None for v in records),'large phases')
preview=Image.fromarray(new)
r=next(v for v in records if v['file']=='costume095_086_hd.png');x,y=r['source_position'];preview.alpha_composite(Image.open(O/r['file']).convert('RGBA'),(x*4-16,y*4-16));preview.save(P/'lightning-registration-preview.png')
