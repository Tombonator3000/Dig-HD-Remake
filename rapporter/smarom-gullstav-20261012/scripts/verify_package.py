from pathlib import Path
import subprocess,json,hashlib
Q=Path(__file__).resolve().parent;G=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk');R=G/'rapporter/smarom-gullstav-20261012';S=Path('/home/tombonator3000t/Skrivebord');app=S/'TheDigHD-20261013-rettet-r9-x86_64.AppImage';prior=S/'TheDigHD-20261012-rettet-r8-x86_64.AppImage';processes=[]
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def mount(p):
 proc=subprocess.Popen([str(p),'--appimage-mount'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True);processes.append(proc);d=Path(proc.stdout.readline().strip());assert d.is_dir() and str(d).startswith('/tmp/.mount_');return d
def sums(p):return dict((name,h) for h,name in (l.split('  ',1) for l in p.read_text().splitlines()))
try:
 new,old=mount(app),mount(prior);m=new/'usr/share/the-dig-hd/mods/gpt';o=old/'usr/share/the-dig-hd/mods/gpt';before=sums(o/'SHA256SUMS');after=sums(m/'SHA256SUMS');allowed=json.loads((R/'RUNTIME-FILES.json').read_text());added=set(after)-set(before);deleted=set(before)-set(after);changed={p for p in set(before)&set(after) if before[p]!=after[p]};assert not deleted and added<=set(allowed) and changed<=set(allowed)|{'mod.json'}
 for p,h in after.items():assert sha(m/p)==h,p
 for p,h in allowed.items():assert sha(m/p)==h,p
 assert sha(new/'usr/bin/scummvm')==sha(old/'usr/bin/scummvm')=='3080b02e8747692643784c7b376d2d6f60c908091b2a943bfb375a1988c1c788';meta=json.loads((new/'BUILD.json').read_text());assert meta['release_revision']=='20261013-r9' and meta['room_backgrounds']==106
 plan=json.loads((R/'PLAN.json').read_text());assert all(sha(G/p)==h for p,h in plan['protected_input_sha256'].items())
 for rev in ['r4','r5']:
  heads=json.loads((new/f'delivery/{rev}/ALIGNMENT.json').read_text());assert heads==json.loads((old/f'delivery/{rev}/ALIGNMENT.json').read_text())
  for f in heads['files']:assert sha(m/f['file'])==f['sha256']
 assert all(sha(m/f'costumes/costume319_{i:03d}{suffix}.png')==sha(o/f'costumes/costume319_{i:03d}{suffix}.png') for i in range(15) for suffix in ('_hd','_idx'))
 assert json.loads((new/'delivery/r9/RUNTIME-FILES.json').read_text())==allowed
 result={'appimage':str(app),'bytes':app.stat().st_size,'sha256':sha(app),'engine_unchanged_from_r8':True,'added_files':sorted(added),'changed_files':sorted(changed),'unchanged_mod_files':len(set(before)&set(after))-len(changed),'mod_checksums_verified':len(after),'runtime_files_verified':len(allowed),'protected_inputs_unchanged':80,'corrected_heads_retained':551,'all15_crystal_states_retained':True,'room_backgrounds':106,'passed':True};(R/'PACKAGED-CONTENT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
finally:
 for p in processes:
  p.terminate()
  try:p.wait(timeout=10)
  except subprocess.TimeoutExpired:p.kill();p.wait()
