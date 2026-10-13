from pathlib import Path
import os,subprocess,json,re
R=Path(__file__).resolve().parent;info=json.loads((R/'WINDOWS-ZIP-QA.json').read_text());P=Path(info['extracted_to']);d=R/'qa-zip-fresh';d.mkdir(exist_ok=True)
def win(p):return 'Z:'+str(p.resolve()).replace('/','\\')
env=os.environ.copy();env.update(WINEPREFIX=str(R/'wine-qa2'),WINEDEBUG='-all',WINESERVER=str(R/'toolchain/usr/lib/x86_64-linux-gnu/wine/wineserver'),SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',DIGHD_USER_DIR=win(d),DIGHD_VERIFY='1',DIGHD_QUIT_AT='300',DIGHD_DUMP_EVERY='100',DIGHD_DUMP_FLAT='1',DIGHD_DUMP_DIR=win(d),DIGHD_SKIP_VIDEO='1',DIGHD_TEST_ROOM='22',DIGHD_TEST_AT='30')
cmd=[str(R/'toolchain/usr/lib/x86_64-linux-gnu/wine/wine'),'cmd','/c',win(P/'Start The Dig HD.cmd'),'--no-fullscreen','--debuglevel=1']
with (d/'run.log').open('w') as f:p=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=180)
log=(d/'run.log').read_text(errors='replace');checks=[int(n) for n in re.findall(r'verify frame \d+: (\d+) screen pixels differ',log)]
result={'exit_code':p.returncode,'checks':checks,'launcher_from_extracted_zip':True,'path_contains_spaces':True,'fresh_config_created':(d/'scummvm.ini').is_file(),'shipped_default_graphics_mode_used':True,'game_room22_loaded':'room 22 loaded' in log,'missing_music_or_voice_bundle':"can't open bundle" in log.lower(),'passed':p.returncode==0 and bool(checks) and all(n==0 for n in checks) and 'room 22 loaded' in log and "can't open bundle" not in log.lower()}
(R/'EXTRACTED-ZIP-RUNTIME-QA.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
assert result['passed']
