import os
from runqa import *
from concurrent.futures import ThreadPoolExecutor
import re,json
P=ROOT/'grafikk/rapporter/restgrafikk-r19-20261016';registered=json.loads((P/'rat183-trap-registration.json').read_text());targets={int(r['file'].split('_')[1]) for r in registered}
def one(anim):
 name=f'r19-rattrap-fix/183-{anim}'
 run(name,dict(SAVE=15,DIGHD_TEST_ROOM=68,DIGHD_TEST_COSTUME=183,DIGHD_TEST_ANIMATION=anim,DIGHD_TEST_DIRECTION=2,DIGHD_TEST_POS='320,0',DIGHD_TEST_CAMX=480,DIGHD_TEST_PALETTE=1,DIGHD_QUIT_AT=1200,DIGHD_TEST_CHORE_EVERY=10000,DIGHD_TEST_STATIC_SCENE=1,DIGHD_SKIP_VIDEO=1,DIGHD_DUMP_EVERY=100),binary=ROOT/'motor/scummvm',mod=ROOT/'kandidat-r19')
 log=(ROOT/'testing'/name/'log.txt').read_text();checks=[(int(f),int(c)) for f,c in re.findall(r'verify frame (\d+): (\d+) screen pixels differ from the whole screen built again',log)];seen=set(int(c) for c in re.findall(r'soft cel (\d+) costume 183 ',log));errors=re.findall(r'^.*(?:ERROR|Assertion|failed).*$',log,re.M);new=sorted(seen&targets)
 return dict(case=name,checks=checks,seen_new_art_cells=new,errors=errors,passed=bool(checks) and bool(new) and not any(c for f,c in checks if f>=100) and not errors)
with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(one,[6,18,19,20,21]))
(ROOT/'testing/r19-rattrap-fix-results.json').write_text(json.dumps(results,indent=2));print([(v['case'],len(v['seen_new_art_cells']),v['passed']) for v in results])
