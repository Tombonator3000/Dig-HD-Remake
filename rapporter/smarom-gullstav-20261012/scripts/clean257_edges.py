from pathlib import Path
from PIL import Image
from bleed_rgba import bleed
import json,hashlib
Q=Path(__file__).resolve().parent;R=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk/rapporter/smarom-gullstav-20261012');M=Path('/home/tombonator3000t/Skrivebord/TheDigHD-Linux-20261012-test/usr/share/the-dig-hd/mods/gpt');d=json.loads((R/'IMPORT-LAG.json').read_text())
for n in ['obj257_01','obj257_02']:
 f=M/'objects'/f'{n}.png';im=Image.open(f).convert('RGBA');bleed(im,erode=4).save(f);e=next(e for e in d['entries'] if e['object']==n);e['sha256']=hashlib.sha256(f.read_bytes()).hexdigest();e['alpha_edge_bleed']='Reliable interior RGB extended4HDpx into the existing alpha edge, alpha unchanged; removes generator colour fringe.'
(R/'IMPORT-LAG.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
