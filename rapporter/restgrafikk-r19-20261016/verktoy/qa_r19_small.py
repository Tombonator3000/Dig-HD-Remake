import os
from runqa import *
from concurrent.futures import ThreadPoolExecutor
import re,json
P=ROOT/'grafikk/rapporter/restgrafikk-r19-20261016';tiny=json.loads((P/'small-fragment-registration.json').read_text())['new_fragments'];targets={cid:{int(r['file'].split('_')[1]) for r in tiny if r['file'].startswith(f'costume{cid:03d}_')} for cid in [56,116,156,238]}
def one(pair):
 cid,room=pair;name=f'r19-small/{cid}'
 run(name,dict(SAVE=15,DIGHD_TEST_ROOM=room,DIGHD_TEST_COSTUME=cid,DIGHD_TEST_POS='0,0',DIGHD_TEST_CAMX=160,DIGHD_QUIT_AT=1800,DIGHD_TEST_CHORE_EVERY=30,DIGHD_TEST_STATIC_SCENE=1,DIGHD_SKIP_VIDEO=1,DIGHD_DUMP_EVERY=100),binary=ROOT/'motor/scummvm',mod=ROOT/'kandidat-r19')
 log=(ROOT/'testing'/name/'log.txt').read_text();checks=[(int(f),int(c)) for f,c in re.findall(r'verify frame (\d+): (\d+) screen pixels differ from the whole screen built again',log)];seen=set(int(c) for c in re.findall(r'soft cel (\d+) costume '+str(cid)+r' ',log));errors=re.findall(r'^.*(?:ERROR|Assertion|failed).*$',log,re.M);actual=sorted(seen&targets[cid])
 return dict(case=name,checks=checks,seen_new_fragments=actual,seen_hd_cells=sorted(seen),errors=errors,passed=bool(checks) and bool(actual) and not any(c for f,c in checks if f>=100) and not errors)
with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(one,[(56,20),(116,32),(156,57),(238,89)]))
(ROOT/'testing/r19-small-results.json').write_text(json.dumps(results,indent=2));print([(r['case'],len(r['seen_new_fragments']),r['passed']) for r in results])
