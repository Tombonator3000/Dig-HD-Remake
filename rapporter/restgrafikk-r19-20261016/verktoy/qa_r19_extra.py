import os
from runqa import *
from concurrent.futures import ThreadPoolExecutor
import re,json
cases=[('swim-right',118,33,'300,60',6,1,1400),('small156-center',156,57,'160,100',None,2,1800),('lightning-peak',95,30,'104,0',8,1,250)]
def one(c):
 name,cid,room,pos,anim,direction,end=c;v=dict(SAVE=15,DIGHD_TEST_ROOM=room,DIGHD_TEST_COSTUME=cid,DIGHD_TEST_DIRECTION=direction,DIGHD_TEST_POS=pos,DIGHD_TEST_CAMX=264 if cid==95 else 160,DIGHD_QUIT_AT=end,DIGHD_TEST_CHORE_EVERY=10000 if anim else 30,DIGHD_TEST_STATIC_SCENE=1,DIGHD_SKIP_VIDEO=1,DIGHD_DUMP_EVERY=1 if cid==95 else 20)
 if anim:v['DIGHD_TEST_ANIMATION']=anim
 run('r19-extra/'+name,v,binary=ROOT/'motor/scummvm',mod=ROOT/'kandidat-r19');log=(ROOT/'testing/r19-extra'/name/'log.txt').read_text();checks=[(int(f),int(c)) for f,c in re.findall(r'verify frame (\d+): (\d+) screen pixels differ from the whole screen built again',log)];seen=sorted(set(int(c) for c in re.findall(r'soft cel (\d+) costume '+str(cid)+r' ',log)));errors=re.findall(r'^.*(?:ERROR|Assertion|failed).*$',log,re.M)
 return dict(case=name,costume=cid,checks=checks,seen_hd_cells=seen,errors=errors,passed=bool(checks) and bool(seen) and not any(c for f,c in checks if f>=100) and not errors)
with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(one,cases))
(ROOT/'testing/r19-extra-results.json').write_text(json.dumps(results,indent=2));print([(r['case'],len(r['seen_hd_cells']),r['passed']) for r in results])
