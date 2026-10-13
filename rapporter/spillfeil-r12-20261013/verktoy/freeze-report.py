from pathlib import Path
import hashlib,json,shutil,subprocess
R=Path(__file__).resolve().parent;P=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk/rapporter/spillfeil-r12-20261013');M=R/'AppDir/usr/share/the-dig-hd/mods/gpt'
def sha(p):return hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
# Snapshot only final evidence; regression captures stay in the task directory.
Q=P/'spillkontroll';Q.mkdir(exist_ok=True)
for tag,frame,room in [('final-pda',120,79),('final-glass',120,25),('final-plateau',120,55),('final-lens238-visible',240,27),('final-energy175-seam',120,65),('final-phase-dais35',60,15),('final-bridge152',150,56),('final-bridge168',150,61),('actual-latest-save6-sparks187',120,23)]:
 d=R/'qa'/tag
 for f in [d/f'frame_{frame:06d}_room{room:03d}.png',d/'result.json']:
  if f.exists():shutil.copy2(f,Q/(tag+'-'+f.name))
records=[];conflicts=[]
for f in sorted((P/'mod-overrides').rglob('*.png')):
 rel=f.relative_to(P/'mod-overrides');target=M/rel
 if not target.is_file() or sha(f)!=sha(target):conflicts.append(str(rel))
 records.append({'path':str(rel),'sha256':sha(f),'bytes':f.stat().st_size})
(P/'OVERSTYRINGER-MANIFEST.json').write_text(json.dumps({'files':records,'candidate_mismatches':conflicts,'actual_art_states':sum(not e['path'].endswith(('_idx.png','_mask.png')) for e in records),'human_visual_approval':False},indent=2));print('overrides',len(records),'mismatches',conflicts[:30])
