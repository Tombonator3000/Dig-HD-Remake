from pathlib import Path
import os,json,subprocess,shutil,re,hashlib
R=Path(__file__).resolve().parent
APP=R/'linux-package/squashfs-root'
MOD=APP/'usr/share/the-dig-hd/mods/gpt'
assert MOD.is_dir()
subprocess.run(['sha256sum','--quiet','-c','SHA256SUMS'],cwd=MOD,check=True)
assert (MOD/'SHA256SUMS').read_bytes()==(R/'AppDir/usr/share/the-dig-hd/mods/gpt/SHA256SUMS').read_bytes()
cases=[
 ('pda',6,79,{'DIGHD_TEST_OBJSTATE':'551:0,537:1,538:0,539:0,540:0,546:0,541:1,542:1,543:1,544:1'}),
 ('glass',6,25,{'DIGHD_TEST_COSTUME':'14','DIGHD_TEST_ACTOR':'3','DIGHD_TEST_POS':'185,136','DIGHD_TEST_ANIMATION':'3'}),
 ('cave',6,57,{'DIGHD_TEST_COSTUME':'158','DIGHD_TEST_ACTOR':'3','DIGHD_TEST_POS':'209,165','DIGHD_TEST_ANIMATION':'6'}),
 ('inventory',5,None,{}),
 ('plateau',6,55,{'DIGHD_TEST_OBJSTATE':'387:1,388:1'}),
 ('lens',6,27,{'DIGHD_TEST_CAMX':'180','DIGHD_TEST_CAMY':'680'}),
 ('bridge',6,56,{'DIGHD_TEST_COSTUME':'152','DIGHD_TEST_ACTOR':'12','DIGHD_TEST_POS':'0,0','DIGHD_TEST_ANIMATION':'7'}),
 ('energy',6,65,{'DIGHD_TEST_COSTUME':'175','DIGHD_TEST_ACTOR':'6','DIGHD_TEST_POS':'160,100','DIGHD_TEST_ANIMATION':'6'}),
 ('brink',6,105,{'DIGHD_TEST_COSTUME':'17','DIGHD_TEST_ACTOR':'29','DIGHD_TEST_POS':'245,110','DIGHD_TEST_ANIMATION':'6'}),
]
results=[]
for name,slot,room,extra in cases:
 d=R/'qa-linux-package'/name;d.mkdir(parents=True,exist_ok=True)
 saves=d/'.local/share/the-dig-hd/saves';saves.mkdir(parents=True,exist_ok=True)
 config=d/'.config/the-dig-hd';config.mkdir(parents=True,exist_ok=True)
 for s in (R/'saves-baseline').glob('dig.s*'):shutil.copy2(s,saves/s.name)
 shutil.copy2(R/'baseline-config.ini',config/'scummvm.ini')
 env=os.environ.copy()
 for k in list(env):
  if k.startswith('DIGHD_'):del env[k]
 env.update(HOME=str(d),XDG_CONFIG_HOME=str(d/'.config'),XDG_DATA_HOME=str(d/'.local/share'),SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',DIGHD_VERIFY='1',DIGHD_DEBUG_SOFT='1',DIGHD_DEBUG_BLAST='1',DIGHD_QUIT_AT='240',DIGHD_DUMP_EVERY='60',DIGHD_DUMP_DIR=str(d),DIGHD_SKIP_VIDEO='1',DIGHD_TEST_AT='60',DIGHD_TEST_CHORE_EVERY='600',DIGHD_TEST_STATIC_SCENE='1')
 if room:env['DIGHD_TEST_ROOM']=str(room)
 env.update(extra)
 with (d/'run.log').open('w') as f:
  proc=subprocess.run([str(APP/'AppRun'),f'--save-slot={slot}','--no-fullscreen','--debuglevel=1'],env=env,stdout=f,stderr=subprocess.STDOUT,timeout=240)
 log=(d/'run.log').read_text(errors='replace')
 checks=list(map(int,re.findall(r'verify frame \d+: (\d+) screen pixels differ',log)))
 rooms=sorted(set(map(int,re.findall(r'dumped frame \d+ \(room (\d+)',log))))
 result={'case':name,'exit_code':proc.returncode,'checks':checks,'rooms':rooms,'passed':proc.returncode==0 and bool(checks) and not any(checks) and (room is None or room in rooms)}
 results.append(result);(d/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
 if not result['passed']:break
summary={'package':str(R/'TheDigHD-r12-x86_64.AppImage'),'cases':results,'mod_checksums_verified':True,'launch':'extracted downloaded AppImage AppRun with embedded graphics, isolated HOME/XDG/saves','passed':len(results)==len(cases) and all(x['passed'] for x in results)}
(R/'LINUX-PACKAGE-QA.json').write_text(json.dumps(summary,indent=2)+'\n')
if not summary['passed']:raise SystemExit(1)
