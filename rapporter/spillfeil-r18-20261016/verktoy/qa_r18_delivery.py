from runqa import *
from concurrent.futures import ThreadPoolExecutor
import re,json
cases={'moonmap':dict(SAVE=15),'moons':dict(SAVE=10,DIGHD_TEST_ROOM=55),'tram':dict(SAVE=10,DIGHD_TEST_ROOM=80,DIGHD_TEST_CAMX=680,DIGHD_TEST_OBJSTATE='554:1,983:1,890:1',DIGHD_TEST_COSTUME=14,DIGHD_TEST_ACTOR=3,DIGHD_TEST_POS='716,128',DIGHD_TEST_CHORE_EVERY=10000,DIGHD_TEST_STATIC_SCENE=1),'nest':dict(SAVE=15,DIGHD_TEST_ROOM=44),'laser':dict(SAVE=1,DIGHD_TEST_ROOM=85),'pole':dict(SAVE=10,DIGHD_TEST_ROOM=68,DIGHD_TEST_CAMX=440,DIGHD_TEST_COSTUME=178,DIGHD_TEST_POS='460,165',DIGHD_TEST_CHORE_EVERY=8,DIGHD_TEST_STATIC_SCENE=1,DIGHD_QUIT_AT=900)}
def task(z):
 n,v=z;run('r18-delivery/'+n,dict(DIGHD_QUIT_AT=300,**v) if 'DIGHD_QUIT_AT' not in v else v,binary=ROOT/'motor/scummvm',mod=ROOT/'hd-integrert-r18');log=(ROOT/'testing/r18-delivery'/n/'log.txt').read_text();checks=[(int(f),int(c)) for f,c in re.findall(r'verify frame (\d+): (\d+) screen pixels differ from the whole screen built again',log)];assert checks and not any(c for f,c in checks if f>=100),(n,checks);return {'case':n,'checks':checks,'errors':re.findall(r'^.*(?:ERROR|Assertion|failed).*$',log,re.M)}
with ThreadPoolExecutor(max_workers=3) as p:results=list(p.map(task,cases.items()))
assert not any(r['errors'] for r in results);(ROOT/'testing/r18-delivery-results.json').write_text(json.dumps(results,indent=2));print('PASS',len(results),'integrated delivery cases')
