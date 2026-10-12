from pathlib import Path
import json,sys,hashlib,numpy as np
from PIL import Image
Q=Path(__file__).resolve().parent;T=Q.parent;G=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk');R=G/'rapporter/smarom-gullstav-20261012';M=Path('/home/tombonator3000t/Skrivebord/TheDigHD-Linux-20261012-test/usr/share/the-dig-hd/mods/gpt');sys.path[:0]=[str(T/'code/pipeline'),str(T/'deps')];from dighd import gpt
d=json.loads((R/'IMPORT-LAG.json').read_text());base=None
for j,n in [('lag032_05','obj257_01'),('lag032_07','obj257_02')]:
 master=Image.open(Q/(j+'-assembled.png')).convert('RGB');hd=np.array(master.crop((320,688,576,816)))
 if base is not None:hd=gpt.match_state(hd,base,Q/'extract/objects'/f'{n}_idx.png',Q/'extract/objects/obj257_01_idx.png')
 else:base=hd
 dest=M/'objects'/f'{n}.png';gpt._with_alpha(hd,Q/'extract/objects'/f'{n}.png').save(dest)
 e=next(e for e in d['entries'] if e['object']==n);e['sha256']=hashlib.sha256(dest.read_bytes()).hexdigest();e['color_lock_strength']=0;e['color_lock_reason']='Preserve generated smooth surfaces; original colour lock reintroduced narrow pixel colour fringes on disconnected native-alpha strips.'
(R/'IMPORT-LAG.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
