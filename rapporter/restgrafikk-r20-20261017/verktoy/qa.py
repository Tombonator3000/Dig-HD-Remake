"""Nexus physical-cel coverage in isolated original game state, no user saves."""
from pathlib import Path
import os, sys, re, json, argparse
from concurrent.futures import ThreadPoolExecutor
R=Path(os.environ.get('DIGHD_WORKSPACE',Path(__file__).resolve().parents[4]))
sys.path.insert(0,str(R))
from runqa import run
P=R/'grafikk/rapporter/restgrafikk-r20-20261017'
parser=argparse.ArgumentParser();parser.add_argument('--mod',default='hd-leveranse');parser.add_argument('--name',default='baseline');a=parser.parse_args()
plans=json.loads((P/'plans.json').read_text())
targets={cid:{v['cel'] for b in plans['batches'] if b['costume']==cid for v in b['cells']} for cid in [62,63,64,65,66]}
def one(case):
    cid,pal,x=case;name=f'r20-{a.name}/{cid}'
    run(name,dict(SAVE=15,DIGHD_TEST_ROOM=23,DIGHD_TEST_COSTUME=cid,DIGHD_TEST_ANIMATION=6,DIGHD_TEST_DIRECTION=2,DIGHD_TEST_POS=f'{x},0',DIGHD_TEST_CAMX=x,DIGHD_TEST_PALETTE=pal,DIGHD_QUIT_AT=2200,DIGHD_TEST_CHORE_EVERY=10000,DIGHD_TEST_STATIC_SCENE=1,DIGHD_SKIP_VIDEO=1,DIGHD_DUMP_EVERY=40),binary=R/'motor/scummvm',mod=R/a.mod)
    log=(R/'testing'/name/'log.txt').read_text()
    checks=[(int(f),int(n)) for f,n in re.findall(r'verify frame (\d+): (\d+) screen pixels differ from the whole screen built again',log)]
    seen={int(c) for c in re.findall(r'soft cel (\d+) costume '+str(cid)+r' ',log)}
    errors=re.findall(r'^.*(?:ERROR|Assertion|failed).*$',log,re.M)
    return dict(case=name,costume=cid,palette=pal,checks=checks,seen_hd_cells=sorted(seen),seen_new_cells=sorted(seen&targets[cid]),unseen_new_cells=sorted(targets[cid]-seen),errors=errors,passed=bool(checks) and not any(n for f,n in checks if f>=100) and not errors)
with ThreadPoolExecutor(max_workers=3) as pool:
    results=list(pool.map(one,[(62,1,632),(63,0,480),(64,2,216),(65,3,984),(66,0,1488)]))
(P/f'qa-{a.name}.json').write_text(json.dumps(results,indent=2)+'\n')
print([(r['costume'],len(r['seen_new_cells']),len(r['unseen_new_cells']),r['passed']) for r in results])
