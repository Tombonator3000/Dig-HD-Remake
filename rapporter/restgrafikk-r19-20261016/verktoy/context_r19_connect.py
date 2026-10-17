import os
from runqa import *
from concurrent.futures import ThreadPoolExecutor
import re,json
P=ROOT/'grafikk/rapporter/restgrafikk-r19-20261016'
def one(anim):
 name=f'r19-connect-facing-right/95-{anim}'
 run(name,dict(SAVE=15,DIGHD_TEST_ROOM=30,DIGHD_TEST_COSTUME=95,DIGHD_TEST_ANIMATION=anim,DIGHD_TEST_DIRECTION=1,DIGHD_TEST_POS='104,0',DIGHD_TEST_CAMX=264,DIGHD_QUIT_AT=1200,DIGHD_TEST_CHORE_EVERY=10000,DIGHD_TEST_STATIC_SCENE=1,DIGHD_SKIP_VIDEO=1,DIGHD_DUMP_EVERY=300),binary=ROOT/'motor/scummvm',mod=ROOT/'kandidat-r19')
 return name
with ThreadPoolExecutor(max_workers=3) as pool: names=list(pool.map(one,range(6,12)))
rows={}
for name in names:
 log=(ROOT/'testing'/name/'log.txt').read_text()
 for cel,slot,x,y,w,h in re.findall(r'(?:soft )?cel (\d+) costume 95 slot (\d+) (?:seq \d+ at|without HD image at) (-?\d+),(-?\d+) (\d+)x(\d+)',log):
  if int(slot)>=928:rows.setdefault(int(cel),set()).add((int(x),int(y),int(w),int(h)))
result=[dict(cel=n,xy=list(sorted(v)[0][:2]),size=list(sorted(v)[0][2:]),unique_positions=len(v),positions=[list(t) for t in sorted(v)]) for n,v in sorted(rows.items())]
(P/'connect095-source-placement.json').write_text(json.dumps(result,indent=2)+'\n');print('placements',len(result))
