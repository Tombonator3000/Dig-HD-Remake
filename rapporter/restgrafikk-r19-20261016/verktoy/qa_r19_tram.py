import os
from runqa import *
from concurrent.futures import ThreadPoolExecutor
import re,json
P=ROOT/'grafikk/rapporter/restgrafikk-r19-20261016';registered=json.loads((P/'tram-art-registration.json').read_text());targets={cid:{int(r['file'].split('_')[1]) for r in registered if r['file'].startswith(f'costume{cid:03d}_')} for cid in [268,270,272,274,276]}
def one(c):
 cid,room,anim=c;name=f'r19-tram/{cid}-{anim}'
 run(name,dict(SAVE=15,DIGHD_TEST_ROOM=room,DIGHD_TEST_COSTUME=cid,DIGHD_TEST_ANIMATION=anim,DIGHD_TEST_DIRECTION=2,DIGHD_TEST_POS='0,5' if room==80 else '0,0',DIGHD_TEST_CAMX=160,DIGHD_QUIT_AT=2200,DIGHD_TEST_CHORE_EVERY=10000,DIGHD_TEST_STATIC_SCENE=1,DIGHD_SKIP_VIDEO=1,DIGHD_DUMP_EVERY=100),binary=ROOT/'motor/scummvm',mod=ROOT/'kandidat-r19')
 log=(ROOT/'testing'/name/'log.txt').read_text();checks=[(int(f),int(c)) for f,c in re.findall(r'verify frame (\d+): (\d+) screen pixels differ from the whole screen built again',log)];seen=set(int(c) for c in re.findall(r'soft cel (\d+) costume '+str(cid)+r' ',log));errors=re.findall(r'^.*(?:ERROR|Assertion|failed).*$',log,re.M);new=sorted(seen&targets[cid])
 return dict(case=name,costume=cid,checks=checks,seen_hd_cells=sorted(seen),seen_new_art_cells=new,errors=errors,passed=bool(checks) and bool(new) and not any(c for f,c in checks if f>=100) and not errors)
cases=[(cid,r,a) for cid,r in [(268,95),(270,80),(272,81),(274,83),(276,94)] for a in [6,8]]
with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(one,cases))
(ROOT/'testing/r19-tram-results.json').write_text(json.dumps(results,indent=2));print([(r['case'],len(r['seen_new_art_cells']),r['passed']) for r in results])
