import os
from runqa import *
from concurrent.futures import ThreadPoolExecutor
import re,json
def one(anim):
 name=f'r19-swim/118-{anim}'
 run(name,dict(SAVE=15,DIGHD_TEST_ROOM=33,DIGHD_TEST_COSTUME=118,DIGHD_TEST_ANIMATION=anim,DIGHD_TEST_DIRECTION=1,DIGHD_TEST_POS='160,60',DIGHD_QUIT_AT=2200,DIGHD_TEST_CHORE_EVERY=10000,DIGHD_TEST_STATIC_SCENE=1,DIGHD_SKIP_VIDEO=1,DIGHD_DUMP_EVERY=20),binary=ROOT/'motor/scummvm',mod=ROOT/'kandidat-r19')
 log=(ROOT/'testing'/name/'log.txt').read_text();checks=[(int(f),int(c)) for f,c in re.findall(r'verify frame (\d+): (\d+) screen pixels differ from the whole screen built again',log)];seen=sorted(set(int(c) for c in re.findall(r'soft cel (\d+) costume 118 ',log)));errors=re.findall(r'^.*(?:ERROR|Assertion|failed).*$',log,re.M)
 return dict(case=name,checks=checks,seen_hd_cells=seen,errors=errors,passed=bool(checks) and bool(seen) and not any(c for f,c in checks if f>=100) and not errors)
with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(one,[6,7]))
(ROOT/'testing/r19-swim-results.json').write_text(json.dumps(results,indent=2));print([(r['case'],len(r['seen_hd_cells']),r['passed']) for r in results])
