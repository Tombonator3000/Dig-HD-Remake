from pathlib import Path
import os,shutil,subprocess,json,re,argparse
p=argparse.ArgumentParser();p.add_argument('tag');p.add_argument('--room',type=int,default=88);p.add_argument('--camx',type=int,default=-1);p.add_argument('--camy',type=int,default=-1);p.add_argument('--costume',type=int,default=15);p.add_argument('--actor',type=int,default=29);p.add_argument('--slot',type=int,default=3);p.add_argument('--chore',action='store_true');p.add_argument('--pos',default='220,150');p.add_argument('--chore-every',type=int,default=4);p.add_argument('--walk',action='store_true');p.add_argument('--scale',type=int);p.add_argument('--frames',type=int,default=100);p.add_argument('--dump',type=int,default=20);p.add_argument('--appimage',type=Path);a=p.parse_args()
Q=Path(__file__).resolve().parent;T=Q.parent;S=Path('/home/tombonator3000t/Skrivebord/TheDigHD-Linux-20261012-test');D=Q/a.tag;D.mkdir(exist_ok=True)
saves=D/'saves';saves.mkdir(exist_ok=True)
for src in (T/'qa-neck-r4/before-save3/saves').glob('dig.s*'):shutil.copy2(src,saves/src.name)
conf=D/'config.ini';shutil.copy2(T/'qa-planet-r3/config.ini',conf)
env=os.environ.copy();env.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',DIGHD_VERIFY='1',DIGHD_DEBUG_SOFT='1',DIGHD_QUIT_AT=str(a.frames),DIGHD_DUMP_EVERY=str(a.dump),DIGHD_DUMP_FLAT='1',DIGHD_DUMP_DIR=str(D))
env.update(DIGHD_SKIP_VIDEO='1',DIGHD_TEST_ROOM=str(a.room),DIGHD_TEST_AT='1',DIGHD_TEST_CAMX=str(a.camx),DIGHD_TEST_CAMY=str(a.camy))
if a.chore or a.walk:
 env.update(DIGHD_SKIP_VIDEO='1',DIGHD_TEST_ROOM=str(a.room),DIGHD_TEST_AT='1',DIGHD_TEST_ACTOR=str(a.actor),DIGHD_TEST_COSTUME=str(a.costume),DIGHD_TEST_POS=a.pos,DIGHD_TEST_CHORE_EVERY=str(a.chore_every))
if a.walk:env['DIGHD_TEST_WALK']='290,126'
if a.scale:env['DIGHD_TEST_SCALE']=str(a.scale)
if a.appimage:
 cd=D/'config/the-dig-hd';cd.mkdir(parents=True,exist_ok=True);shutil.copy2(conf,cd/'scummvm.ini')
 sd=D/'data/the-dig-hd/saves';sd.mkdir(parents=True,exist_ok=True)
 for src in saves.glob('dig.s*'):shutil.copy2(src,sd/src.name)
 env.update(XDG_CONFIG_HOME=str(D/'config'),XDG_DATA_HOME=str(D/'data'))
 cmd=[str(a.appimage.resolve()),'--save-slot='+str(a.slot),'--no-fullscreen','--debuglevel=1']
else:
 env.update(LD_LIBRARY_PATH=str(S/'usr/lib'),DIGHD_MOD=str(S/'usr/share/the-dig-hd/mods/gpt'))
 cmd=[os.environ.get('DIGHD_QA_ENGINE',str(S/'usr/bin/scummvm')),'--config='+str(conf),'--path='+str(S/'usr/share/the-dig-hd/game'),'--savepath='+str(saves),'--save-slot='+str(a.slot),'--no-fullscreen','--debuglevel=1','dig']
with (D/'run.log').open('w') as f:r=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=240)
log=(D/'run.log').read_text();checks=[{'frame':int(f),'pixels':int(n)} for f,n in re.findall(r'verify frame (\d+): (\d+) screen pixels differ',log)];rooms=[int(x) for x in re.findall(r'dumped frame \d+ \(room (\d+)',log)]
result={'tag':a.tag,'exit_code':r.returncode,'checks':checks,'rooms':sorted(set(rooms)),'passed':r.returncode==0 and bool(checks) and all(x['pixels']==0 for x in checks) and a.room in rooms,'test_mode': 'AppImage' if a.appimage else 'native with staged mod','save_source':'isolated copies from before-save3/saves; user saves unchanged'}
(D/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
if not result['passed']:raise SystemExit(1)
