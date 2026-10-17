import os
from runqa import *
from concurrent.futures import ThreadPoolExecutor
import re,json,sys
sys.path.insert(0,str(ROOT/'kode/pipeline'));from dighd import gamedata as g
P=ROOT/'grafikk/rapporter/restgrafikk-r19-20261016';rows=json.loads((P/'identical-source-registration.json').read_text())['imported'];targets={cid:{int(r['target'].split('_')[1]) for r in rows if int(r['target'][7:10])==cid} for cid in sorted({int(r['target'][7:10]) for r in rows})};G=APP/'usr/share/the-dig-hd/game';d=(G/'DIG.LA1').read_bytes();ix=g.read_index(G/'DIG.LA0');rooms=g.read_rooms(G/'DIG.LA1');cases=[]
for cid,wanted in targets.items():
 rn,off=ix.costume_dir[cid];p=rooms[rn].offset+off;choices=g.akos_animations(d,p,g.be32(d,p+4))['animasjoner'];by={}
 for v in choices:by.setdefault(v['animasjon'],set()).update(v['ruter'])
 pending=set(wanted)
 while pending:
  anim=max(by,key=lambda n:len(by[n]&pending));hit=by[anim]&pending
  if not hit:break
  cases.append((cid,rn,anim));pending-=hit
print('cases',cases,flush=True)
def one(c):
 cid,room,anim=c;name=f'r19-identical/{cid}-{anim}'
 run(name,dict(SAVE=15,DIGHD_TEST_ROOM=room,DIGHD_TEST_COSTUME=cid,DIGHD_TEST_ANIMATION=anim,DIGHD_TEST_DIRECTION=2,DIGHD_TEST_POS='160,140',DIGHD_TEST_CAMX=160,DIGHD_QUIT_AT=2200,DIGHD_TEST_CHORE_EVERY=10000,DIGHD_TEST_STATIC_SCENE=1,DIGHD_SKIP_VIDEO=1,DIGHD_DUMP_EVERY=200),binary=ROOT/'motor/scummvm',mod=ROOT/'kandidat-r19')
 log=(ROOT/'testing'/name/'log.txt').read_text();checks=[(int(f),int(c)) for f,c in re.findall(r'verify frame (\d+): (\d+) screen pixels differ from the whole screen built again',log)];seen=set(int(c) for c in re.findall(r'soft cel (\d+) costume '+str(cid)+r' ',log));errors=re.findall(r'^.*(?:ERROR|Assertion|failed).*$',log,re.M);new=sorted(seen&targets[cid])
 return dict(case=name,costume=cid,checks=checks,seen_new_art_cells=new,errors=errors,passed=bool(checks) and bool(new) and not any(c for f,c in checks if f>=100) and not errors)
with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(one,cases))
(ROOT/'testing/r19-identical-results.json').write_text(json.dumps(results,indent=2));print([(v['case'],len(v['seen_new_art_cells']),v['passed']) for v in results])
