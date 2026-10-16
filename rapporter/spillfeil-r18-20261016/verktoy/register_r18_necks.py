from pathlib import Path
from PIL import Image
import numpy as np,json,os,shutil
R=Path(__file__).resolve().parent;P=R/'grafikk/rapporter/spillfeil-r18-20261016';O=P/'mod-overrides/costumes';O.mkdir(exist_ok=True,parents=True);M=R/'kandidat-r18/costumes';B=R/'hd-integrert/costumes';records=[]
for rec in json.loads((R/'grafikk/rapporter/spillfeil-20261016/HEAD-REGISTRATION.json').read_text()):
 if rec['kind']!='independent_head' or int(rec['file'][7:10]) not in [14,15,16,17,18]:continue
 name=rec['file'];im=Image.open(B/name).convert('RGBA');a=np.asarray(im)[:,:,3];y,x=np.where(a>128);box=(int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1));tile=im.crop(box);split=round(tile.height*.70);extra=6;out=Image.new('RGBA',im.size);out.alpha_composite(tile.crop((0,0,tile.width,split)),(box[0],box[1]));neck=tile.crop((0,split,tile.width,tile.height)).resize((tile.width,tile.height-split+extra),Image.Resampling.BICUBIC);out.alpha_composite(neck,(box[0],box[1]+split));out.save(O/name);temp=M/(name+'.new');shutil.copy2(O/name,temp);os.replace(temp,M/name);records.append({'file':name,'face_and_hair_placement_unchanged':True,'neck_extension_hd':extra,'split_hd':split,'source_bbox':box})
(P/'NECK-REGISTRATION.json').write_text(json.dumps(records,indent=2));print(len(records),'head neck contacts extended without moving faces')
