import os
from runqa import *
import re,json
name='r19-rat-script/room068-2006'
run(name,dict(SAVE=15,DIGHD_TEST_ROOM=68,DIGHD_TEST_CAMX=480,DIGHD_TEST_SCRIPT='110:2006',DIGHD_TEST_COSTUME=183,DIGHD_TEST_ACTOR=14,DIGHD_TEST_ANIMATION=1,DIGHD_TEST_PALETTE=1,DIGHD_TEST_POS='320,0',DIGHD_TEST_CHORE_EVERY=10000,DIGHD_TEST_STATIC_SCENE=1,DIGHD_QUIT_AT=1200,DIGHD_SKIP_VIDEO=1,DIGHD_DUMP_EVERY=20),binary=ROOT/'motor/scummvm',mod=ROOT/'kandidat-r19')
log=(ROOT/'testing'/name/'log.txt').read_text();checks=[(int(f),int(c)) for f,c in re.findall(r'verify frame (\d+): (\d+) screen pixels differ from the whole screen built again',log)];seen=set(int(c) for c in re.findall(r'soft cel (\d+) costume 183 ',log));errors=re.findall(r'^.*(?:ERROR|Assertion|failed).*$',log,re.M)
result=dict(case=name,script='original local script2006 sets actor14 costume183 shadowMode1 palette1 and animations20/21',checks=checks,seen_hd_cells=sorted(seen),errors=errors,passed=bool(checks) and bool(seen) and not any(c for f,c in checks if f>=100) and not errors)
(ROOT/'testing/r19-rat-script-results.json').write_text(json.dumps([result],indent=2));print('source-script rat',len(seen),'seen',result['passed'])
