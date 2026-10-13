from pathlib import Path
import os,json,subprocess,shutil,re,hashlib
R=Path(__file__).resolve().parent;P=R/'windows/TheDigHD';old=Path.home()/'.codex/tasks/the-dig-linux-20261012'
wine=R/'toolchain/usr/lib/x86_64-linux-gnu/wine/wine';server=wine.parent/'wineserver'
def win(p):return 'Z:'+str(p.resolve()).replace('/','\\')
results=[]
cases=[('room22',22,None),('room32',32,None),('room32-object256',32,256),('room32-object257',32,257),('room50',50,None),('room88',88,None)]
for tag,room,obj in cases:
 d=R/'qa-windows'/tag;d.mkdir(parents=True,exist_ok=True);saves=d/'saves';saves.mkdir(exist_ok=True)
 for s in (old/'qa-neck-r4/before-save3/saves').glob('dig.s*'):shutil.copy2(s,saves/s.name)
 shutil.copy2(old/'qa-planet-r3/config.ini',d/'scummvm.ini')
 env=os.environ.copy();env.update(WINEPREFIX=str(R/'wine-qa2'),WINEDEBUG='-all',WINESERVER=str(server),SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',DIGHD_USER_DIR=win(d),DIGHD_VERIFY='1',DIGHD_QUIT_AT='100',DIGHD_DUMP_EVERY='20',DIGHD_DUMP_FLAT='1',DIGHD_DUMP_DIR=win(d),DIGHD_SKIP_VIDEO='1',DIGHD_TEST_ROOM=str(room),DIGHD_TEST_AT='1')
 if obj:env.update(DIGHD_TEST_OBJSTATE=f'{obj}:1',DIGHD_TEST_OBJSTATE_AT='2')
 cmd=[str(wine),'cmd','/c',win(P/'Start The Dig HD.cmd'),'--save-slot=3','--no-fullscreen','--gfx-mode=surfacesdl','--debuglevel=1']
 with (d/'run.log').open('w') as f:proc=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=180)
 logs=[(d/'run.log').read_text(errors='replace')]
 for p in (R/'wine-qa2/drive_c/users').rglob('scummvm.log'):logs.append(p.read_text(errors='replace'))
 text=logs[0] if 'verify frame' in logs[0] else '\n'.join(logs[1:]);(d/'combined.log').write_text(text)
 checks=[{'frame':int(f),'pixels':int(n)} for f,n in re.findall(r'verify frame (\d+): (\d+) screen pixels differ',text)]
 rooms=[int(x) for x in re.findall(r'dumped frame \d+ \(room (\d+)',text)]
 pictures=list(d.glob('frame_*.png'))
 result={'tag':tag,'room':room,'exit_code':proc.returncode,'checks':checks,'rooms':sorted(set(rooms)),'screenshots':len(pictures),'passed':proc.returncode==0 and bool(checks) and all(x['pixels']==0 for x in checks) and room in rooms and bool(pictures),'launcher':'Start The Dig HD.cmd via Wine 10 on Kubuntu'}
 results.append(result);(d/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
 if not result['passed']:break
(R/'WINDOWS-RUNTIME-QA.json').write_text(json.dumps({'cases':results,'passed':len(results)==len(cases) and all(c['passed'] for c in results),'physical_Windows_tested':False},indent=2))
if len(results)!=len(cases) or not all(c['passed'] for c in results):raise SystemExit(1)
