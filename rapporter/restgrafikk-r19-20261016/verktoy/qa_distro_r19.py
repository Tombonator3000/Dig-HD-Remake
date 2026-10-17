import os
"""Use the downloaded AppRun and its own game, graphics and libraries with copied test saves."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,os,re,json,shutil
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));T=R/'testing/distro-r19';A=T/'AppDir'
cases=[('brink',15,23,46,6,2,'160,175',160,0),('maggie',1,111,331,6,0,'0,0',160,0),('capsule',15,80,270,8,2,'0,5',160,0),('rat',15,68,183,18,2,'320,0',480,1)]
def one(c):
 name,save,room,cid,chore,direction,pos,cam,pal=c;P=T/'figurer'/name;P.mkdir(parents=True,exist_ok=True);saved=P/'data/the-dig-hd/saves';saved.mkdir(parents=True,exist_ok=True);filename=f'dig.s{save:02d}';shutil.copy2(R/'testing/saves'/filename,saved/filename)
 env=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',XDG_CONFIG_HOME=str(P/'config'),XDG_DATA_HOME=str(P/'data'),DIGHD_MOD=str(A/'usr/share/the-dig-hd/mods/gpt'),DIGHD_VERIFY='1',DIGHD_DEBUG_SOFT='1',DIGHD_MANGLER='0',DIGHD_DUMP_DIR=str(P/'dumps'),DIGHD_DUMP_EVERY='100',DIGHD_QUIT_AT='700',DIGHD_TEST_ROOM=str(room),DIGHD_TEST_COSTUME=str(cid),DIGHD_TEST_ANIMATION=str(chore),DIGHD_TEST_DIRECTION=str(direction),DIGHD_TEST_POS=pos,DIGHD_TEST_CAMX=str(cam),DIGHD_TEST_PALETTE=str(pal),DIGHD_TEST_CHORE_EVERY='10000',DIGHD_TEST_STATIC_SCENE='1',DIGHD_SKIP_VIDEO='1')
 with (P/'log.txt').open('w') as log:subprocess.run([str(A/'AppRun'),f'--save-slot={save}','--debuglevel=1'],env=env,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=240)
 s=(P/'log.txt').read_text();checks=[int(n) for n in re.findall(r'verify frame \d+: (\d+) screen pixels differ from the whole screen built again',s)];seen=sorted(set(int(n) for n in re.findall(r'soft cel (\d+) costume '+str(cid)+r' ',s)));errors=re.findall(r'^.*(?:ERROR|Assertion).*$',s,re.M);ok=bool(checks) and bool(seen) and max(checks)==0 and not errors
 return dict(case=name,costume=cid,seen_hd_cells=seen,redraw_checks=len(checks),max_redraw_difference=max(checks) if checks else None,errors=errors,passed=ok)
with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(one,cases))
(T/'figure-tests.json').write_text(json.dumps(results,indent=2)+'\n');print([(v['case'],len(v['seen_hd_cells']),v['passed']) for v in results]);assert all(v['passed'] for v in results)
report=json.loads((T/'kontroll-linux.json').read_text());report['packaged_figure_tests']=results;(T/'kontroll-linux.json').write_text(json.dumps(report,indent=2)+'\n')
