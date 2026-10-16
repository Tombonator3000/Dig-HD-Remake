import os
from runqa import run,ROOT
from concurrent.futures import ThreadPoolExecutor
import re,json
cases=[]
for x in [160,360,548]:cases.append((f'museum-{x}',dict(DIGHD_TEST_ROOM=34,DIGHD_TEST_CAMX=x,DIGHD_QUIT_AT=240)))
for cid in [78,80,81,82,83]:cases.append((f'probe-{cid}',dict(DIGHD_TEST_ROOM=14,DIGHD_TEST_COSTUME=cid,DIGHD_TEST_POS='0,0' if cid in [80,81,83] else '160,100',DIGHD_TEST_STATIC_SCENE=1,DIGHD_TEST_CHORE_EVERY=70,DIGHD_QUIT_AT=650)))
for cid in [67,73]:cases.append((f'brink-{cid}',dict(DIGHD_TEST_ROOM=23,DIGHD_TEST_COSTUME=cid,DIGHD_TEST_POS='1280,0',DIGHD_TEST_CAMX=1440,DIGHD_TEST_STATIC_SCENE=1,DIGHD_TEST_CHORE_EVERY=140,DIGHD_QUIT_AT=1300)))
cases+=[('boston-water',dict(DIGHD_TEST_ROOM=32,DIGHD_TEST_COSTUME=103,DIGHD_TEST_POS='160,170',DIGHD_TEST_STATIC_SCENE=1,DIGHD_TEST_CHORE_EVERY=170,DIGHD_QUIT_AT=650)),('bones',dict(SAVE=1,DIGHD_SKIP_VIDEO=0,DIGHD_TEST_ROOM=36,DIGHD_QUIT_AT=250)),('crystal-cycle',dict(DIGHD_TEST_ROOM=97,DIGHD_TEST_KEYS='120:i,180:i',DIGHD_QUIT_AT=250))]
def task(case):
 name,values=case;run('expanded/'+name,dict({'DIGHD_SKIP_VIDEO':1},**values),ROOT/'motor/scummvm');f=ROOT/'testing/expanded'/name;log=(f/'log.txt').read_text();checks=[int(n) for frame,n in re.findall(r'verify frame (\d+): (\d+) screen pixels differ from the whole screen built again',log) if int(frame)>=100];return {'case':name,'redraw_checks':len(checks),'max_redraw_difference':max(checks,default=-1),'parameters':values}
with ThreadPoolExecutor(max_workers=4) as p:results=list(p.map(task,cases))
(ROOT/'testing/expanded-results.json').write_text(json.dumps(results,indent=2));print(results)
assert all(x['redraw_checks'] and x['max_redraw_difference']==0 for x in results)
