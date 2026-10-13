from pathlib import Path
import os,json,subprocess,shutil,re,argparse
R=Path(__file__).resolve().parent;S=R/'AppDir';a=argparse.ArgumentParser();a.add_argument('tag');a.add_argument('--at',type=int,default=1);a.add_argument('--room',type=int);a.add_argument('--saves-from',default='');a.add_argument('--slot',type=int,default=0);a.add_argument('--frames',type=int,default=180);a.add_argument('--dump',type=int,default=60);a.add_argument('--camera',default='');a.add_argument('--keys',default='');a.add_argument('--clicks',default='');a.add_argument('--states',default='');a.add_argument('--classic',action='store_true');a.add_argument('--candidate',action='store_true');a.add_argument('--costume',type=int);a.add_argument('--pos',default='160,160');a.add_argument('--palette',type=int);a.add_argument('--chore-every',type=int,default=4);a.add_argument('--animation',type=int);a.add_argument('--mod',default='');a.add_argument('--static-scene',action='store_true');a.add_argument('--actor',type=int,default=29);p=a.parse_args()
d=R/'qa'/p.tag;d.mkdir(parents=True,exist_ok=True);saves=d/'saves';saves.mkdir(exist_ok=True)
for f in (Path(p.saves_from) if p.saves_from else R/'saves-baseline').glob('dig.s*'):shutil.copy2(f,saves/f.name)
shutil.copy2(R/'baseline-config.ini',d/'config.ini')
env=os.environ.copy();env.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',LD_LIBRARY_PATH=str(S/'usr/lib'),DIGHD_MOD=(p.mod or str(S/'usr/share/the-dig-hd/mods/gpt')),DIGHD_VERIFY='1',DIGHD_DEBUG_SOFT='1',DIGHD_DEBUG_BLAST='1',DIGHD_QUIT_AT=str(p.frames),DIGHD_DUMP_EVERY=str(p.dump),DIGHD_DUMP_FLAT='1',DIGHD_DUMP_DIR=str(d),DIGHD_SKIP_VIDEO='1',DIGHD_TEST_AT=str(p.at))
if p.room:env['DIGHD_TEST_ROOM']=str(p.room)
if p.camera:
 x,y=p.camera.split(',');env.update(DIGHD_TEST_CAMX=x,DIGHD_TEST_CAMY=y)
if p.keys:env['DIGHD_TEST_KEYS']=p.keys
if p.clicks:env['DIGHD_TEST_CLICKS']=p.clicks
if p.states:env['DIGHD_TEST_OBJSTATE']=p.states
if p.classic:env['DIGHD_CLASSIC']='1'
if p.costume:env.update(DIGHD_TEST_COSTUME=str(p.costume),DIGHD_TEST_ACTOR=str(p.actor),DIGHD_TEST_POS=p.pos,DIGHD_TEST_CHORE_EVERY=str(p.chore_every))
if p.static_scene:env['DIGHD_TEST_STATIC_SCENE']='1'
if p.animation is not None:env['DIGHD_TEST_ANIMATION']=str(p.animation)
if p.palette is not None:env['DIGHD_TEST_PALETTE']=str(p.palette)
bin=R/'native/scummvm' if p.candidate else S/'usr/bin/scummvm'
cmd=[str(bin),'--config='+str(d/'config.ini'),'--path='+str(S/'usr/share/the-dig-hd/game'),'--savepath='+str(saves),'--themepath='+str(S/'usr/share/the-dig-hd'),'--extrapath='+str(S/'usr/share/the-dig-hd'),'--save-slot='+str(p.slot),'--no-fullscreen','--debuglevel=1','dig']
with (d/'run.log').open('w') as f:proc=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=240)
log=(d/'run.log').read_text(errors='replace');checks=[int(x) for x in re.findall(r'verify frame \d+: (\d+) screen pixels differ',log)];rooms=sorted(set(map(int,re.findall(r'dumped frame \d+ \(room (\d+)',log))))
result={'tag':p.tag,'exit_code':proc.returncode,'checks':checks,'rooms':rooms,'passed':proc.returncode==0 and bool(checks) and not any(checks)};(d/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
if not result['passed']:raise SystemExit(1)
