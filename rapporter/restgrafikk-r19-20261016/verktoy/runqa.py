import os
import os, subprocess, sys
from pathlib import Path
ROOT=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]))
APP=Path('/home/tom/Documents/Codex/2026-10-16-the-dig-hd-remake-sp-rsm/testing/linux-release/AppDir')
def run(name, values, binary=None, mod=None):
    folder=ROOT/'testing'/name
    folder.mkdir(parents=True, exist_ok=True)
    env=os.environ.copy()
    env.update(SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',DIGHD_MOD=str(mod or ROOT/'kandidat-mod'),DIGHD_DUMP_DIR=str(folder),DIGHD_DUMP_EVERY='20',DIGHD_DUMP_FLAT='1',DIGHD_QUIT_AT='180',DIGHD_DEBUG_SOFT='1',DIGHD_DEBUG_BLAST='1',DIGHD_VERIFY='1',DIGHD_MANGLER='0',LD_LIBRARY_PATH=str(APP/'usr/lib'))
    env.update({k:str(v) for k,v in values.items() if k!='SAVE'})
    if binary: env['LD_LIBRARY_PATH']=values.get('QA_LIB','/home/tom/Documents/Codex/2026-10-16-the-dig-hd-remake-sp-rsm/.build-env/lib')
    cmd=[str(binary or APP/'usr/bin/scummvm'),'--config='+str(ROOT/'testing/scummvm.ini'),'--path='+str(APP/'usr/share/the-dig-hd/game'),'--savepath='+str(ROOT/'testing/saves'),'--themepath='+str(APP/'usr/share/the-dig-hd'),'--extrapath='+str(APP/'usr/share/the-dig-hd'),'--no-fullscreen','--gfx-mode=surfacesdl','--no-aspect-ratio']
    if 'SAVE' in values: cmd+=['--save-slot='+str(values['SAVE'])]
    if binary:
        cmd=[a for a in cmd if not a.startswith('--gfx-mode') and not a.startswith('--config=')]
    cmd=[a for a in cmd if not a.startswith('--config=')]
    conf=folder/'scummvm.ini'
    conf.write_text('[scummvm]\nfullscreen=false\naspect_ratio=false\nsubtitles=true\nconfirm_exit=false\n')
    cmd+=['--config='+str(conf)]
    cmd+=['--debuglevel=1','dig']
    with (folder/'log.txt').open('w') as log: result=subprocess.run(cmd,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=360)
    print(name,result.returncode,flush=True)
if __name__=='__main__':
    cases={
      'save0':{'SAVE':0}, 'save1':{'SAVE':1},
      'boston':{'DIGHD_TEST_ROOM':15,'DIGHD_TEST_COSTUME':14,'DIGHD_TEST_STATIC_SCENE':1,'DIGHD_TEST_POS':'160,170','DIGHD_TEST_CHORE_EVERY':10,'DIGHD_QUIT_AT':400},
      'maggie':{'DIGHD_TEST_ROOM':15,'DIGHD_TEST_COSTUME':18,'DIGHD_TEST_STATIC_SCENE':1,'DIGHD_TEST_POS':'160,170','DIGHD_TEST_CHORE_EVERY':10,'DIGHD_QUIT_AT':400},
      'brink':{'DIGHD_TEST_ROOM':15,'DIGHD_TEST_COSTUME':15,'DIGHD_TEST_STATIC_SCENE':1,'DIGHD_TEST_POS':'160,170','DIGHD_TEST_CHORE_EVERY':10,'DIGHD_QUIT_AT':400},
      'dead':{'DIGHD_TEST_ROOM':23,'DIGHD_TEST_COSTUME':58,'DIGHD_TEST_STATIC_SCENE':1,'DIGHD_TEST_POS':'160,170','DIGHD_TEST_CHORE_EVERY':12,'DIGHD_QUIT_AT':400},
      'glass':{'DIGHD_TEST_ROOM':25,'DIGHD_TEST_COSTUME':14,'DIGHD_TEST_STATIC_SCENE':0,'DIGHD_TEST_POS':'580,160','DIGHD_TEST_CAMX':580},
      'pda':{'DIGHD_TEST_ROOM':79,'DIGHD_TEST_KEYS':'120:i'},
      'crystal':{'DIGHD_TEST_ROOM':92},
    }
    from concurrent.futures import ThreadPoolExecutor
    names=sys.argv[1:] or list(cases)
    with ThreadPoolExecutor(max_workers=3) as pool:
      list(pool.map(lambda n:run('baseline/'+n,dict(SAVE=1,**cases[n]) if 'SAVE' not in cases[n] else cases[n]),names))
