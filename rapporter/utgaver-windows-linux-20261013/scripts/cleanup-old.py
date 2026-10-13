from pathlib import Path
import hashlib,json,os,subprocess
R=Path(__file__).resolve().parent;H=Path.home();D=H/'Skrivebord'
expected='d8769b180ee9c8acf532de03b36d2058f19badd3b7383d56d66323a26fc6ed68'
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
stable=D/'TheDigHD-x86_64.appimage';new=D/'TheDigHD-20261013-rettet-r10-x86_64.AppImage'
assert sha(stable)==sha(new)==expected
saved={str(p):sha(p) for p in (H/'.local/share/the-dig-hd/saves').rglob('*') if p.is_file()}
repo=H/'Documents/Codex/Dig-HD-Remake-gpt-grafikk'
status=subprocess.check_output(['git','-C',str(repo),'status','--porcelain=v1'])
# Keep audit evidence and reports. Only named obsolete packaged executables,
# their desktop checksums and the old desktop launchers are removed here.
inventory=json.loads((R/'local-inventory.json').read_text());targets=[]
for item in inventory:
 p=Path(item['path'])
 if p.suffix.lower()=='.appimage':
  if 'r10-' in p.name or p==stable:continue
 elif p.suffix=='.desktop':
  if 'r10.' in p.name:continue
 elif p.suffix=='.sha256':
  if p.parent!=D or 'r10-' in p.name:continue
 else:continue
 assert not p.is_symlink() and p.is_file(),p
 assert p.lstat().st_ino==item['inode'] and p.stat().st_size==item['size'],p
 assert '.git' not in p.parts
 targets.append(p)
targetset={str(p) for p in targets}
active=[]
for proc in Path('/proc').iterdir():
 if not proc.name.isdigit():continue
 candidates=[proc/'exe',proc/'cwd']
 try:candidates+=list((proc/'fd').iterdir())
 except (PermissionError,FileNotFoundError):pass
 for q in candidates:
  try:
   if os.readlink(q) in targetset:active.append({'pid':proc.name,'path':os.readlink(q)})
  except OSError:pass
assert not active,active
removed=[];inodes={}
for p in targets:
 s=p.stat();inodes.setdefault((s.st_dev,s.st_ino),{'size':s.st_size,'links':s.st_nlink,'removed':0});inodes[(s.st_dev,s.st_ino)]['removed']+=1
 removed.append({'path':str(p),'bytes':s.st_size})
(R/'cleanup-plan.json').write_text(json.dumps({'targets':removed,'active_handles':active,'preserved_latest_sha256':expected},indent=2))
for p in targets:p.unlink()
assert sha(stable)==sha(new)==expected
assert subprocess.check_output(['git','-C',str(repo),'status','--porcelain=v1'])==status
assert all(Path(p).is_file() and sha(Path(p))==h for p,h in saved.items())
result={'removed':removed,'removed_count':len(removed),'old_appimage_paths_removed':sum(p.suffix.lower()=='.appimage' for p in targets),'freed_unique_bytes':sum(x['size'] for x in inodes.values() if x['removed']==x['links']),'latest_preserved':str(stable),'sha256':expected,'save_files_preserved':len(saved),'graphics_git_status_unchanged':True,'passed':True}
(R/'LOCAL-CLEANUP.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='removed'},indent=2))
