import os
from pathlib import Path
import json,hashlib,shutil,os
from PIL import Image
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));P=R/'grafikk/rapporter/restgrafikk-r19-20261016';O=P/'mod-overrides/costumes';M=R/'kandidat-r19/costumes';B=R/'hd-leveranse/costumes';O.mkdir(parents=True,exist_ok=True);records=[]
master=Image.open(P/'mod-tillegg/costumes/costume330_006_hd.png').convert('RGBA')
for n,x,y,w,h in [(0,0,27,160,153),(1,160,0,160,180)]:
 # The static state is split into two independently positioned source cels.
 # Cut both from one drawn state so their shared edge and figure proportions
 # remain identical when the engine assembles them.
 tile=master.crop((16+x*4,16+y*4,16+(x+w)*4,16+(y+h)*4));out=Image.new('RGBA',((w+8)*4,(h+8)*4));out.alpha_composite(tile,(16,16));name=f'costume330_{n:03d}_hd.png';out.save(O/name)
 temp=M/(name+'.new');shutil.copy2(O/name,temp);os.replace(temp,M/name)
 records.append(dict(path='costumes/'+name,base_sha256=hashlib.sha256((B/name).read_bytes()).hexdigest(),sha256=hashlib.sha256((O/name).read_bytes()).hexdigest(),reference='costume330_006_hd.png',source_crop=[x,y,w,h],reason='Replace older photographic static figure/surface with same approved-pilot drawing used by new animation phases',visually_approved_by_tom=False))
(P/'OVERRIDES.json').write_text(json.dumps(records,indent=2)+'\n');print('2 static laboratory parts aligned to new sequence')
