import os
from runqa import *
from concurrent.futures import ThreadPoolExecutor
import re,json
cases=[(80,270),(81,272),(83,274),(94,276),(95,268)]
def one(c):
 room,cid=c;name=f'r19-tram-context/room{room}'
 run(name,dict(SAVE=15,DIGHD_TEST_ROOM=room,DIGHD_TEST_STATIC_SCENE=0,DIGHD_SKIP_VIDEO=1,DIGHD_QUIT_AT=1600,DIGHD_DUMP_EVERY=80),binary=ROOT/'motor/scummvm',mod=ROOT/'kandidat-r19')
 log=(ROOT/'testing'/name/'log.txt').read_text();shadows=sorted(set((int(n),int(s)) for n,s in re.findall(r'palette-mask costume '+str(cid)+r' cel (\d+) shadow mode (\d+)',log)));original=sorted(set(int(n) for n in re.findall(r'cel (\d+) costume '+str(cid)+r' ',log)));return dict(room=room,costume=cid,shadow_modes=shadows,seen_source_cells=original)
with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(one,cases))
(ROOT/'grafikk/rapporter/restgrafikk-r19-20261016/tram-source-context.json').write_text(json.dumps(results,indent=2)+'\n');print(results)
