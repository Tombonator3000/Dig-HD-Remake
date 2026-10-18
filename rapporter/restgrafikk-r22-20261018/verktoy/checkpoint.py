from pathlib import Path
import json,hashlib,gzip,shutil
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parents[4];P=Path(__file__).resolve().parents[1];O=P/'mod-tillegg';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();records=json.loads((P/'registration.json').read_text());rejected=json.loads((P/'rejected-shapes.json').read_text());qa=json.loads((P/'qa.json').read_text());assert qa['passed'] and len(records)==48
manifest={str(f.relative_to(O)):sha(f) for f in sorted(O.rglob('*.png'))};assert len(manifest)==96
for r in records:
 f=O/'costumes'/r['file'];im=Image.open(f);sw,sh=r['source_size'];assert im.mode=='RGBA' and im.size==((sw+8)*4,(sh+8)*4);assert r['alpha_iou']>=.6 and r['axis_deviation']<=.12;assert not (R/'hd-leveranse/costumes'/f.name).exists();index=r['name']+'_idx.png';assert np.array_equal(np.array(Image.open(O/'costumes'/index)),np.array(Image.open(R/'testing/source/costumes'/index)))
(P/'ADDITIONS.json').write_text(json.dumps(manifest,indent=2)+'\n');old=json.loads((R/'grafikk/rapporter/restgrafikk-r20-20261017/remaining.json').read_text());filled={r['name'] for r in records};old['cells']=[c for c in old['cells'] if c['name'] not in filled];old['base']=dict(published_hd_mod='29cff6583dc45ec21bcccb5da0eb16afafa379a5',candidate_additions='ADDITIONS.json',not_published=True);assert len(old['cells'])==5963;(P/'remaining-candidate.json').write_text(json.dumps(old,indent=2)+'\n')
with gzip.open(P/'native-boston100.log.gz','wb') as f:f.write((R/'testing/r22-boston100/log.txt').read_bytes())
for n,label in [(210,'kneeling-scene.png'),(420,'rising-scene.png'),(660,'standing-scene.png')]:shutil.copy2(R/'testing/r22-boston100'/f'frame_{n:06d}_room032.png',P/label)
masters=[]
for f in sorted(P.glob('*master.png')):
 masters.append(dict(file=f.name,sha256=sha(f),used_for_exports=any(r['master']==f.name for r in records),native_grid=[1,1] if 'single' in f.name else [4,2]))
f=dict(date='2026-10-18',round='r22',tool='built-in image_gen.imagegen',model='not reported',selected_missing_cels=48,new_missing_cels_filled=48,held_for_redraw=[r['cel'] for r in rejected],remaining_published_art_cels=6011,remaining_candidate_art_cels=5963,explicit_addition_files=96,source_palette='costume100 AKPL through room32 palette0',native_observed_new_cels=48,native_redraw_checks_after_startup=len([v for v in qa['checks'] if v[0]>=100]),palette_corrected_small_fragments=91,replacement_files=182,published=False,distro=False,human_visual_approval=False,leveranser=[],native_ark=masters,rutekart='registration.json',prompts='prompter.json',manifest='ADDITIONS.json',natural_playthrough=False)
(P/'fremdrift.json').write_text(json.dumps(f,indent=2)+'\n');print('48 cels;96 new files;5963 candidate remaining;source indices unchanged')
