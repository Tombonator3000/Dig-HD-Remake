from pathlib import Path
import json,re,sys
from concurrent.futures import ThreadPoolExecutor
R=Path('/home/tom/Documents/ChatGPT/THE DIG');sys.path.insert(0,str(R));from runqa import run
P=R/'grafikk/rapporter/integrering-r20-r21-20261018';MOD=R/'hd-integrert-r20-r21'
plans=json.loads((R/'grafikk/rapporter/restgrafikk-r20-20261017/plans.json').read_text());targets={cid:{c['cel'] for b in plans['batches'] if b['costume']==cid for c in b['cells']} for cid in [62,63,64,65,66]};targets[34]=set(range(130))
cases=[(f'nexus-{c}',c,p,6,2,f'{x},0') for c,p,x in [(62,1,632),(63,0,480),(64,2,216),(65,3,984),(66,0,1488)]]+[(f'nexus-{c}-extra',c,p,6,1,'0,60') for c,p in [(64,2),(65,3)]]+[(f'canyon-{a}',34,0,a,2,'160,135') for a in [6,7,8,9]]
def one(case):
 name,c,p,a,d,pos=case;folder=R/'testing/integration-r20-r21'/name
 run('integration-r20-r21/'+name,dict(SAVE=15,DIGHD_TEST_ROOM=23,DIGHD_TEST_COSTUME=c,DIGHD_TEST_ANIMATION=a,DIGHD_TEST_DIRECTION=d,DIGHD_TEST_POS=pos,DIGHD_TEST_CAMX=int(pos.split(',')[0]),DIGHD_TEST_CAMY=100,DIGHD_TEST_PALETTE=p,DIGHD_QUIT_AT=2200 if c!=34 else 1800,DIGHD_TEST_CHORE_EVERY=10000,DIGHD_TEST_STATIC_SCENE=1,DIGHD_SKIP_VIDEO=1,DIGHD_DUMP_EVERY=40),binary=R/'motor/scummvm',mod=MOD)
 log=(folder/'log.txt').read_text();checks=[(int(f),int(n)) for f,n in re.findall(r'verify frame (\d+): (\d+) screen pixels differ from the whole screen built again',log)];seen={int(v) for v in re.findall(r'soft cel (\d+) costume '+str(c)+' ',log)};errors=re.findall(r'^.*(?:ERROR|Assertion|failed).*$',log,re.M)
 return dict(name=name,costume=c,palette=p,animation=a,direction=d,checks=checks,seen_hd_cels=sorted(seen),seen_target_cels=sorted(seen&targets[c]),errors=errors,passed=bool(checks) and not errors and all(n==0 for f,n in checks if f>=100))
with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(one,cases))
coverage={str(c):dict(expected=len(t),observed=sorted(set().union(*(set(r['seen_target_cels']) for r in results if r['costume']==c))),unseen=sorted(t-set().union(*(set(r['seen_target_cels']) for r in results if r['costume']==c)))) for c,t in targets.items()}
report=dict(cases=results,coverage=coverage,post_startup_checks=sum(sum(f>=100 for f,n in r['checks']) for r in results),passed=all(r['passed'] for r in results) and all(not d['unseen'] for d in coverage.values()))
(P/'qa-integrated.json').write_text(json.dumps(report,indent=2)+'\n');print('Coverage',[(c,d['expected'],len(d['observed'])) for c,d in coverage.items()]);print('PASS',report['passed'],'checks',report['post_startup_checks'])
assert report['passed']
