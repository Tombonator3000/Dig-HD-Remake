import os
"""Read original game scripts for costume/palette context with official descumm.
Only analysis summaries belong in the graphics report; full game script dumps
remain under ignored testing/. Does not execute or modify original scripts.
"""
from pathlib import Path
import sys,os,json,subprocess
from concurrent.futures import ThreadPoolExecutor
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));sys.path.insert(0,str(R/'kode/pipeline'));from dighd import gamedata as g
G=Path('/home/tom/Documents/Codex/2026-10-16-the-dig-hd-remake-sp-rsm/testing/linux-release/AppDir/usr/share/the-dig-hd/game');d=(G/'DIG.LA1').read_bytes();ix=(G/'DIG.LA0').read_bytes();rooms=g.read_rooms(G/'DIG.LA1');O=R/'testing/r19-original-scripts';O.mkdir(exist_ok=True);tasks=[]
for tag,off,size in g.children(ix,0,len(ix)):
 if tag==b'DSCR':
  for n,(rn,ofs) in enumerate(g._directory(ix[off+8:off+size])):
   if rn:
    p=rooms[rn].offset+ofs;assert d[p:p+4]==b'SCRP';tasks.append((f'global{n:03d}',d[p:p+g.be32(d,p+4)]))
for rn,room in rooms.items():
 p=room.offset
 for tag,off,size in g.children(d,p+8,p+g.be32(d,p+4)):
  if tag in [b'ENCD',b'EXCD',b'LSCR',b'LSC2']:
   suffix=str(g.le16(d,off+8)) if tag==b'LSCR' else str(off-p);tasks.append((f'room{rn:03d}-{tag.decode()}-{suffix}',d[off:off+size]))
  elif tag==b'OBCD':
   for sub,so,ss in g.children(d,off+8,off+size):
    if sub==b'VERB':tasks.append((f'room{rn:03d}-VERB-{so-p}',d[so:so+ss]))
env=os.environ.copy();env['LD_LIBRARY_PATH']='/home/tom/Documents/Codex/2026-10-16-the-dig-hd-remake-sp-rsm/.build-env/lib'
def one(t):
 name,data=t;f=O/(name+'.bin');f.write_bytes(data);r=subprocess.run([str(R/'testing/scummvm-tools/descumm'),'-7',str(f)],env=env,capture_output=True,text=True);(O/(name+'.txt')).write_text(r.stdout+'\n'+r.stderr);return dict(script=name,returncode=r.returncode)
with ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(one,tasks))
(O/'index.json').write_text(json.dumps(results,indent=2)+'\n');print(len(tasks),'scripts read;',sum(r['returncode']!=0 for r in results),'nonzero exits')
