import os
from runqa import run,ROOT
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re,json
cases=[]
for name,cid in [('boston',14),('maggie',18),('brink',15)]:
 for action,anim in [('stand',1),('walk',2),('talk',4)]:
  for direction in range(8):
   cases.append((f'{name}-{action}-{direction}',dict(DIGHD_SKIP_VIDEO=1,DIGHD_TEST_ROOM=14,DIGHD_TEST_COSTUME=cid,DIGHD_TEST_STATIC_SCENE=1,DIGHD_TEST_POS='160,170',DIGHD_TEST_ANIMATION=anim,DIGHD_TEST_DIRECTION=direction,DIGHD_TEST_REMAP_PALETTE=1,DIGHD_TEST_CHORE_EVERY=1000,DIGHD_QUIT_AT=270 if action=='walk' else 210)))
cases += [('dead60',dict(DIGHD_SKIP_VIDEO=1,DIGHD_TEST_ROOM=23,DIGHD_TEST_COSTUME=60,DIGHD_TEST_STATIC_SCENE=1,DIGHD_TEST_POS='1280,0',DIGHD_TEST_CAMX=1440,DIGHD_TEST_CHORE_EVERY=50,DIGHD_QUIT_AT=1400)),('dead59',dict(DIGHD_SKIP_VIDEO=1,DIGHD_TEST_ROOM=23,DIGHD_TEST_COSTUME=59,DIGHD_TEST_STATIC_SCENE=1,DIGHD_TEST_POS='1280,0',DIGHD_TEST_CAMX=1440,DIGHD_TEST_CHORE_EVERY=50,DIGHD_QUIT_AT=1300)),('inventory',dict(SAVE=1,DIGHD_TEST_KEYS='90:i,160:i,190:i',DIGHD_QUIT_AT=260)),('glass',dict(SAVE=1,DIGHD_TEST_ROOM=15,DIGHD_TEST_COSTUME=14,DIGHD_TEST_POS='160,170',DIGHD_TEST_KEYS='140:i,190:i',DIGHD_TEST_CHORE_EVERY=1000,DIGHD_QUIT_AT=260)),('crystals',dict(DIGHD_SKIP_VIDEO=1,DIGHD_TEST_ROOM=97,DIGHD_QUIT_AT=220))]
def task(case):
 name,values=case;run('final/'+name,values,ROOT/'motor/scummvm')
 folder=ROOT/'testing/final'/name;log=(folder/'log.txt').read_text();allchecks=[(int(f),int(n)) for f,n in re.findall(r'verify frame (\d+): (\d+) screen pixels differ from the whole screen built again',log)];counts=[n for f,n in allchecks if f>=100]
 return {'case':name,'redraw_checks':len(counts),'max_redraw_difference':max(counts,default=-1),'startup_checks':[(f,n) for f,n in allchecks if f<100],'errors':re.findall(r'^.*(?:ERROR|Assertion|failed).*$',log,re.M),'frames':len(list(folder.glob('frame_*_room[0-9][0-9][0-9].png'))),'parameters':values}
with ThreadPoolExecutor(max_workers=5) as pool:results=list(pool.map(task,cases))
(ROOT/'testing/final-results.json').write_text(json.dumps(results,indent=2))
assert all(r['redraw_checks']>0 and r['max_redraw_difference']==0 and not r['errors'] and r['frames']>0 for r in results)
print('PASS',len(results),'cases,',sum(r['redraw_checks'] for r in results),'redraw comparisons')
