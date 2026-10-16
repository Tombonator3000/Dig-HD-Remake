"""Remove detached atlas fragments outside the principal head component."""
from pathlib import Path
from PIL import Image
import numpy as np,cv2,json,shutil,os
P=Path('grafikk/rapporter/spillfeil-r18-20261016');O=P/'mod-overrides/costumes';M=Path('kandidat-r18/costumes');names=set();rows=[]
for report in ['NECK-REGISTRATION.json','EXTRA-HEADS.json','BRINK-COLOR-REGISTRATION.json','POLE-REGISTRATION.json']:
 for r in json.loads((P/report).read_text()):
  if r.get('kind','independent_head')=='independent_head':names.add(r['file'])
for r in json.loads(Path('grafikk/rapporter/spillfeil-20261016/HEAD-REGISTRATION.json').read_text()):
 if r.get('kind')=='independent_head':names.add(r['file'])
for name in sorted(names):
 f=O/name if (O/name).exists() else Path('hd-integrert/costumes')/name;im=Image.open(f).convert('RGBA');a=np.asarray(im).copy();n,lab,stats,_=cv2.connectedComponentsWithStats((a[:,:,3]>0).astype('uint8'),8)
 if n<3:continue
 biggest=1+int(stats[1:,cv2.CC_STAT_AREA].argmax());area=int(stats[biggest,cv2.CC_STAT_AREA]);removed=[]
 for i in range(1,n):
  if i!=biggest and stats[i,cv2.CC_STAT_AREA]<max(25,area*.15):removed.append(i)
 if not removed:continue
 mask=np.isin(lab,removed);a[mask,3]=0;Image.fromarray(a).save(O/name);tmp=M/(name+'.new');shutil.copy2(O/name,tmp);os.replace(tmp,M/name);rows.append({'file':name,'removed_disconnected_alpha_pixels':int(mask.sum()),'principal_face_pixels_unchanged':True})
(P/'HEAD-COMPONENT-CLEANUP.json').write_text(json.dumps(rows,indent=2));print(len(rows),'head cells cleaned; principal head/face unchanged')
