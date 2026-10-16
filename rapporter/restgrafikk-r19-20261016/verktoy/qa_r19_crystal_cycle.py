import os
from runqa import *
import re,json
cases={'map278-cycle': {'SAVE': 15, 'DIGHD_TEST_ROOM': 40, 'DIGHD_TEST_COSTUME': 278, 'DIGHD_TEST_CHORE_EVERY': 30, 'DIGHD_TEST_POS': '0,0'}, 'lock285-cycle': {'SAVE': 15, 'DIGHD_TEST_ROOM': 96, 'DIGHD_TEST_COSTUME': 285, 'DIGHD_TEST_CHORE_EVERY': 30, 'DIGHD_TEST_POS': '0,0'}}

results=[]
for name,v in cases.items():
 env=dict(DIGHD_QUIT_AT=8500,DIGHD_TEST_STATIC_SCENE=1,DIGHD_SKIP_VIDEO=1,DIGHD_DUMP_EVERY=200,**v)
 run('r19-crystal-cycle/'+name,env,binary=ROOT/'motor/scummvm',mod=ROOT/'kandidat-r19')
 log=(ROOT/'testing/r19-crystal-cycle'/name/'log.txt').read_text();checks=[(int(f),int(c)) for f,c in re.findall(r'verify frame (\d+): (\d+) screen pixels differ from the whole screen built again',log)]
 cid=v['DIGHD_TEST_COSTUME'];seen=sorted(set(int(c) for c in re.findall(r'soft cel (\d+) costume '+str(cid)+r' ',log)));errors=re.findall(r'^.*(?:ERROR|Assertion|failed).*$',log,re.M)
 results.append(dict(case=name,checks=checks,seen_hd_cells=seen,errors=errors,passed=bool(checks) and bool(seen) and not any(c for f,c in checks if f>=100) and not errors))
 (ROOT/'testing/r19-crystal-cycle-results.json').write_text(json.dumps(results,indent=2));print(name,len(seen),results[-1]['passed'],flush=True)
