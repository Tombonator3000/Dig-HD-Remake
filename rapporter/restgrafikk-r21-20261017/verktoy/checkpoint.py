"""Prove strict declared r21 overrides over preserved published r19+r20."""
from pathlib import Path
import json,hashlib,subprocess
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[4];P=Path(__file__).resolve().parents[1];B=R/'hd-leveranse';C=R/'kandidat-r21';P20=R/'grafikk/rapporter/restgrafikk-r20-20261017'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
base=subprocess.check_output(['git','-C',str(B),'rev-parse','HEAD'],text=True).strip();assert base=='630cadb3ebb398ac8ade1f4e1ea759f8a783cd5a'
replacements=json.loads((P/'REPLACEMENTS.json').read_text());assert len(replacements)==210
records=json.loads((P/'registration.json').read_text());assert len(records)==105
base_sums={line[66:]:line[:64] for line in (B/'SHA256SUMS').read_text().splitlines() if line}
changed=[]
for rel,h in base_sums.items():
 assert sha(B/rel)==h,('published base changed',rel)
 expected=replacements.get(rel,h);assert sha(C/rel)==expected,('candidate incorrect',rel)
 if expected!=h:changed.append(rel)
assert set(changed)==set(replacements)
addition=json.loads((P20/'ADDITIONS.json').read_text())
for rel,h in addition.items():assert sha(C/rel)==h
for rel,h in replacements.items():assert sha(P/'mod-erstatninger'/rel)==h
files=lambda p:{str(f.relative_to(p)) for f in p.rglob('*') if f.is_file() and '.git' not in f.relative_to(p).parts}
base_files=files(B);candidate_files=files(C)
assert candidate_files-base_files==set(addition) and not base_files-candidate_files
for rec in records:
 f=rec['index_file'];a=Image.open(B/'costumes'/f);b=Image.open(C/'costumes'/f);src=Image.open(R/'testing/source/costumes'/f)
 assert a.mode==b.mode=='P';assert np.array_equal(a,b) and np.array_equal(a,src)
 assert b.getpalette()!=a.getpalette()
 assert sha(P/rec['master'])==rec['master_sha256']
qa=json.loads((P/'qa-canyon.json').read_text());assert qa['passed'];assert len(qa['seen_new_cells'])==105
seen=set().union(*(set(r['seen_hd_cells']) for r in qa['cases']));assert seen==set(range(130))
for rec in records:assert qa['tested_artifacts'][rec['file']]==rec['sha256']
# Index PNGs were held unchanged for the entire final four-case run.
qa['tested_index_artifacts']={r['index_file']:sha(C/'costumes'/r['index_file']) for r in records}
(P/'qa-canyon.json').write_text(json.dumps(qa,indent=2)+'\n')
report=dict(base=base,published_manifest_files_checked=len(base_sums),published_base_unchanged=True,explicit_changed_files=len(changed),repainted_hd_cels=105,index_palette_replacements=105,index_code_values_unchanged=True,r20_addition_files_unchanged=len(addition),r20_hd_cels_unchanged=221,hd_movies_unchanged=len(list((B/'san').rglob('*.ivf'))),native_observed_cels=130,native_observed_repainted_cels=105,post_startup_redraw_checks=sum(sum(f>=100 for f,n in r['checks']) for r in qa['cases']),post_startup_redraw_differences=sum(n for r in qa['cases'] for f,n in r['checks'] if f>=100),minimum_alpha_iou=min(r['alpha_iou'] for r in records),max_axis_deviation=max(r['axis_deviation'] for r in records),remaining_art_cels=6011,new_missing_cels_filled=0,engine_or_pipeline_changed=False,published=False,human_visual_approval=False)
report.update(strict_file_set_verified=True,unexpected_added_files=0,deleted_files=0)
(P/'integrity.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
