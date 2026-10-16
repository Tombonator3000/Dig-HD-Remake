import os
from pathlib import Path
import json, collections, hashlib, argparse
import numpy as np
from PIL import Image

R = Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]))
G = R / 'grafikk'
parser=argparse.ArgumentParser();parser.add_argument('--mod',default='hd-leveranse');parser.add_argument('--output',default='dekning-for.json');args=parser.parse_args()
M = R / args.mod
P = G / 'rapporter/restgrafikk-r19-20261016'
P.mkdir(parents=True, exist_ok=True)
cells = {}
for job in sorted((G / 'jobber').glob('fig*')):
    meta = json.loads((job / 'jobb.json').read_text())
    original = Image.open(job / 'original_1x.png').convert('RGB')
    for cel in meta['ruter']:
        name = cel['bilde']
        if name in cells:
            continue
        x, y, w, h = cel['rekt']
        a = np.asarray(original.crop((x, y, x+w, y+h)))
        mask = np.any(a != np.asarray(meta['bakgrunn']), axis=2)
        mask &= ~((a[...,0] > 180) & (a[...,2] > 150) & (a[...,1] < 100))
        count = int(mask.sum())
        hd = M / 'costumes' / (name + '_hd.png')
        plain = M / 'costumes' / (name + '.png')
        cells[name] = dict(name=name, costume=cel['kostyme'], cel=cel['rute'],
                           pixels=count, job=job.name, rect=cel['rekt'],
                           has_hd=hd.exists() or plain.exists(),
                           index_exists=(M / 'costumes' / (name+'_idx.png')).exists(),
                           person=meta['navn'], room=meta['rom'])
missing = [c for c in cells.values() if c['pixels'] and not c['has_hd']]
groups = collections.defaultdict(list)
for c in missing:
    groups[c['costume']].append(c)
summary = [dict(costume=k, person=v[0]['person'], room=v[0]['room'],
                missing=len(v), substantial=sum(c['pixels']>=40 for c in v),
                jobs=sorted(set(c['job'] for c in v))) for k,v in groups.items()]
report = dict(base=__import__('subprocess').check_output(['git','-C',str(M),'rev-parse','HEAD'],text=True).strip(),
              original_unique_cells=len(cells), missing=len(missing),
              substantial=sum(c['pixels']>=40 for c in missing), groups=summary, cells=missing)
(P/args.output).write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='cells'},indent=2,ensure_ascii=False))
