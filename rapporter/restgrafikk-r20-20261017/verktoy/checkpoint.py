"""Verify a graphics-only r20 addition set against immutable published r19."""
from pathlib import Path
import os,sys,json,hashlib,subprocess
import numpy as np
from PIL import Image
R=Path(os.environ.get('DIGHD_WORKSPACE',Path(__file__).resolve().parents[4]));P=R/'grafikk/rapporter/restgrafikk-r20-20261017';B=R/'hd-leveranse';C=R/'kandidat-r20'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
base=subprocess.check_output(['git','-C',str(B),'rev-parse','HEAD'],text=True).strip();assert base=='630cadb3ebb398ac8ade1f4e1ea759f8a783cd5a'
base_manifest={}
for line in (B/'SHA256SUMS').read_text().splitlines():
    digest,rel=line.split(maxsplit=1);rel=rel.lstrip('*');base_manifest[rel]=digest
    assert sha(B/rel)==digest,('base',rel)
    assert sha(C/rel)==digest,('candidate changed base',rel)
manifest=json.loads((P/'ADDITIONS.json').read_text());new_cels=[]
for rel,digest in manifest.items():
    assert not (B/rel).exists(),('not a strict addition',rel)
    assert sha(P/'mod-tillegg'/rel)==digest,rel
    assert sha(C/rel)==digest,('candidate',rel)
    if rel.endswith('_hd.png'):
        new_cels.append(Path(rel).name[:-7])
        im=Image.open(P/'mod-tillegg'/rel);assert im.mode=='RGBA';alpha=np.array(im)[:,:,3];assert (alpha==0).any() and (alpha>128).any()
        idxname=Path(rel).name.replace('_hd','_idx');source=R/'testing/source/costumes'/idxname;index=P/'mod-tillegg/costumes'/idxname
        assert np.array_equal(np.array(Image.open(source)),np.array(Image.open(index))),idxname
base_files={str(f.relative_to(B)) for f in B.rglob('*') if f.is_file() and '.git' not in f.relative_to(B).parts}
work_files={str(f.relative_to(C)) for f in C.rglob('*') if f.is_file()}
assert work_files-base_files==set(manifest),'unexpected extra candidate files'
assert not base_files-work_files,'missing baseline files'
old=json.loads((R/'grafikk/rapporter/restgrafikk-r19-20261016/dekning-arbeid.json').read_text());classified=json.loads((R/'grafikk/rapporter/restgrafikk-r19-20261016/semantic-coverage.json').read_text());masks=set(classified['technical_mask_cells'])
missing=[c for c in old['cells'] if c['name'] not in new_cels];actual=[c for c in missing if c['name'] not in masks]
assert set(new_cels)<=set(c['name'] for c in old['cells'])
movies=list((B/'san').glob('*.ivf'));assert len(movies)==55
sys.path.insert(0,str(R/'kode/pipeline'));from dighd import gamedata as g
game=R/'testing/distro-r19/AppDir/usr/share/the-dig-hd/game';rooms=g.read_rooms(game/'DIG.LA1');d=(game/'DIG.LA1').read_bytes();ix=g.read_index(game/'DIG.LA0');rn,off=ix.costume_dir[34];p=rooms[rn].offset+off;chunks={t:d[o+8:o+n] for t,o,n in g.children(d,p+8,p+g.be32(d,p+4))};mapping=np.array(list(chunks[b'AKPL']));used=set()
for f in (R/'testing/source/costumes').glob('costume034_*_idx.png'):used|=set(mapping[np.array(Image.open(f))].ravel())
used-={0,13};assert all(rooms[15].palettes[0][int(i)*3:int(i)*3+3]==rooms[23].palettes[0][int(i)*3:int(i)*3+3] for i in used)
palette=dict(source_room=15,qa_room=23,palette=0,costume=34,used_indices=sorted(map(int,used)),byte_identical=True)
(P/'canyon-palette-proof.json').write_text(json.dumps(palette,indent=2)+'\n')
protected=subprocess.check_output(['git','-C',str(R/'grafikk'),'diff','--name-only','--','jobber','hovedark','stil'],text=True).strip();assert not protected
report=dict(base=base,base_manifest_files_checked=len(base_manifest),base_files_unchanged=True,unchanged_hd_movies=len(movies),strict_new_files=len(manifest),new_hd_cels=len(new_cels),source_index_values_unchanged=True,protected_job_files_and_model_sheets_unchanged=True,raw_remaining=len(missing),classified_masks_remaining=sum(c['name'] in masks for c in missing),actual_remaining=len(actual),new_costumes=sorted(set(int(n[7:10]) for n in new_cels)),published=False,human_visual_approval=False)
(P/'integrity.json').write_text(json.dumps(report,indent=2)+'\n')
(P/'remaining.json').write_text(json.dumps(dict(base=base,cells=actual),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,indent=2))
