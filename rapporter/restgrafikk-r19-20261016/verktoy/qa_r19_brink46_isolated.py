import os
from runqa import *
from concurrent.futures import ThreadPoolExecutor
import re,json
P=ROOT/'grafikk/rapporter/restgrafikk-r19-20261016';targets={int(v['file'].split('_')[1]) for v in json.loads((P/'brink46-registration.json').read_text())}
def one(anim):
 name=f'r19-brink46-isolated/{anim}'
 run(name,dict(SAVE=15,DIGHD_TEST_ROOM=23,DIGHD_TEST_COSTUME=46,DIGHD_TEST_ANIMATION=anim,DIGHD_TEST_DIRECTION=2,DIGHD_TEST_POS='160,175',DIGHD_TEST_CAMX=160,DIGHD_TEST_CAMY=100,DIGHD_TEST_PALETTE=0,DIGHD_QUIT_AT=1200,DIGHD_TEST_CHORE_EVERY=10000,DIGHD_TEST_STATIC_SCENE=1,DIGHD_SKIP_VIDEO=1,DIGHD_DUMP_EVERY=20),binary=ROOT/'motor/scummvm',mod=ROOT/'kandidat-r19')
 log=(ROOT/'testing'/name/'log.txt').read_text();checks=[(int(f),int(c)) for f,c in re.findall(r'verify frame (\d+): (\d+) screen pixels differ from the whole screen built again',log)];seen=set(int(c) for c in re.findall(r'soft cel (\d+) costume 46 ',log));errors=re.findall(r'^.*(?:ERROR|Assertion|failed).*$',log,re.M)
 return dict(case=name,checks=checks,seen_new_art_cells=sorted(seen&targets),errors=errors,passed=bool(checks) and bool(seen&targets) and not any(c for f,c in checks if f>=100) and not errors)
with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(one,[1,6]))
(ROOT/'testing/r19-brink46-isolated-results.json').write_text(json.dumps(results,indent=2));print([(v['case'],len(v['seen_new_art_cells']),v['passed']) for v in results])
