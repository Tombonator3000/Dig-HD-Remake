import os
from runqa import *
import re,json
cases={
 'eva6':dict(SAVE=1,DIGHD_TEST_ROOM=5,DIGHD_TEST_COSTUME=8,DIGHD_TEST_ANIMATION=6,DIGHD_TEST_DIRECTION=2),
 'eva8':dict(SAVE=1,DIGHD_TEST_ROOM=5,DIGHD_TEST_COSTUME=8,DIGHD_TEST_ANIMATION=8,DIGHD_TEST_DIRECTION=2),
 'eva10':dict(SAVE=1,DIGHD_TEST_ROOM=5,DIGHD_TEST_COSTUME=8,DIGHD_TEST_ANIMATION=10,DIGHD_TEST_DIRECTION=2),
 'eva-chair':dict(SAVE=1,DIGHD_TEST_ROOM=2,DIGHD_TEST_COSTUME=1,DIGHD_TEST_ANIMATION=6,DIGHD_TEST_DIRECTION=2),
 'robotarm':dict(SAVE=1,DIGHD_TEST_ROOM=2,DIGHD_TEST_COSTUME=5,DIGHD_TEST_ANIMATION=6,DIGHD_TEST_DIRECTION=2),
 'brink-tunnel':dict(SAVE=1,DIGHD_TEST_ROOM=9,DIGHD_TEST_COSTUME=22,DIGHD_TEST_CHORE_EVERY=25),
 'maggie-tunnel':dict(SAVE=1,DIGHD_TEST_ROOM=9,DIGHD_TEST_COSTUME=23,DIGHD_TEST_CHORE_EVERY=25),
 'boston-water':dict(SAVE=10,DIGHD_TEST_ROOM=32,DIGHD_TEST_COSTUME=103,DIGHD_TEST_ANIMATION=6,DIGHD_TEST_DIRECTION=2),
 'nexus-fx':dict(SAVE=10,DIGHD_TEST_ROOM=23,DIGHD_TEST_COSTUME=71,DIGHD_TEST_ANIMATION=6,DIGHD_TEST_DIRECTION=2),
 'eye-scene':dict(SAVE=10,DIGHD_TEST_ROOM=78,DIGHD_TEST_COSTUME=213,DIGHD_TEST_ANIMATION=6,DIGHD_TEST_DIRECTION=2),
 'eye-spiral':dict(SAVE=10,DIGHD_TEST_ROOM=78,DIGHD_TEST_COSTUME=214,DIGHD_TEST_ANIMATION=6,DIGHD_TEST_DIRECTION=2),
 'lockup-fx':dict(SAVE=10,DIGHD_TEST_ROOM=82,DIGHD_TEST_COSTUME=229,DIGHD_TEST_ANIMATION=6,DIGHD_TEST_DIRECTION=2),
}
results=[]
for name,values in cases.items():
 env=dict(DIGHD_QUIT_AT=1200,DIGHD_TEST_CHORE_EVERY=10000,DIGHD_TEST_STATIC_SCENE=1,DIGHD_TEST_POS='160,175',DIGHD_SKIP_VIDEO=1,DIGHD_DUMP_EVERY=40,**{k:v for k,v in values.items() if k!='DIGHD_TEST_CHORE_EVERY'})
 if 'DIGHD_TEST_CHORE_EVERY' in values:env['DIGHD_TEST_CHORE_EVERY']=values['DIGHD_TEST_CHORE_EVERY']
 run('r19/'+name,env,binary=ROOT/'motor/scummvm',mod=ROOT/'kandidat-r19')
 log=(ROOT/'testing/r19'/name/'log.txt').read_text();checks=[(int(f),int(c)) for f,c in re.findall(r'verify frame (\d+): (\d+) screen pixels differ from the whole screen built again',log)]
 errors=re.findall(r'^.*(?:ERROR|Assertion|failed).*$',log,re.M)
 result=dict(case=name,checks=checks,errors=errors,passed=bool(checks) and not any(c for f,c in checks if f>=100) and not errors)
 results.append(result);(ROOT/'testing/r19-results.json').write_text(json.dumps(results,indent=2))
 print(name,result['passed'],len(checks),flush=True)
