import os
from runqa import *
import re,json
cases={
 'chair24':dict(SAVE=1,DIGHD_TEST_ROOM=2,DIGHD_TEST_COSTUME=1,DIGHD_TEST_ANIMATION=24,DIGHD_TEST_DIRECTION=4,DIGHD_TEST_POS='160,150'),
 'nexus11':dict(SAVE=10,DIGHD_TEST_ROOM=23,DIGHD_TEST_COSTUME=71,DIGHD_TEST_ANIMATION=11,DIGHD_TEST_DIRECTION=2,DIGHD_TEST_POS='200,120'),
 'water6':dict(SAVE=10,DIGHD_TEST_ROOM=32,DIGHD_TEST_COSTUME=103,DIGHD_TEST_ANIMATION=6,DIGHD_TEST_DIRECTION=2,DIGHD_TEST_POS='280,100'),
 'eye-scene1':dict(SAVE=10,DIGHD_TEST_ROOM=78,DIGHD_TEST_COSTUME=213,DIGHD_TEST_ANIMATION=1,DIGHD_TEST_DIRECTION=2,DIGHD_TEST_POS='200,150'),
}
results=[]
for name,v in cases.items():
 env=dict(DIGHD_QUIT_AT=1500,DIGHD_TEST_CHORE_EVERY=10000,DIGHD_TEST_STATIC_SCENE=1,DIGHD_SKIP_VIDEO=1,DIGHD_DUMP_EVERY=20,**v)
 run('r19-focused/'+name,env,binary=ROOT/'motor/scummvm',mod=ROOT/'kandidat-r19')
 log=(ROOT/'testing/r19-focused'/name/'log.txt').read_text();checks=[(int(f),int(c)) for f,c in re.findall(r'verify frame (\d+): (\d+) screen pixels differ from the whole screen built again',log)]
 cid=v['DIGHD_TEST_COSTUME'];seen=sorted(set(int(c) for c in re.findall(r'soft cel (\d+) costume '+str(cid)+r' ',log)));errors=re.findall(r'^.*(?:ERROR|Assertion|failed).*$',log,re.M)
 results.append(dict(case=name,checks=checks,seen_hd_cells=seen,errors=errors,passed=bool(checks) and bool(seen) and not any(c for f,c in checks if f>=100) and not errors))
 (ROOT/'testing/r19-focused-results.json').write_text(json.dumps(results,indent=2));print(name,len(seen),results[-1]['passed'],flush=True)
