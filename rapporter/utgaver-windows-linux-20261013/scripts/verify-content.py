from pathlib import Path
import json,hashlib,subprocess
R=Path(__file__).resolve().parent;P=R/'windows/TheDigHD';checks=json.loads((R/'linux-content-sha256.json').read_text())
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
for n,h in checks.items():assert sha(P/n)==h,n
src=Path('/home/tombonator3000t/.codex/tasks/the-dig-linux-20261012/native');manifest=json.loads((R/'source-scumm-sha256.json').read_text())
for n,h in manifest.items():assert sha(R/'source'/n)==sha(src/n)==h,n
result={'same_game_and_hd_files_as_linux_r10':len(checks),'same_scumm_source_files':len(manifest),'engine_sha256':sha(P/'scummvm.exe'),'SDL2_sha256':sha(P/'SDL2.dll'),'libwinpthread_sha256':sha(P/'libwinpthread-1.dll'),'platform':'Windows x86_64','passed':True}
(R/'WINDOWS-CONTENT.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
