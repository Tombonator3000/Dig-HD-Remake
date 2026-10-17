import os
"""Integrate the committed r19 additions on the current published r18 without rebuilding older art."""
from pathlib import Path
import sys,json,hashlib,shutil,subprocess
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));sys.path.insert(0,str(R/'kode/pipeline'));from dighd import modflett as m
P=R/'grafikk/rapporter/restgrafikk-r19-20261016';BASE=R/'testing/r19-published-base';C=R/'r19-input';OUT=R/'hd-integrert-r19';C.mkdir(exist_ok=True)
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
rows=json.loads((P/'ADDITIONS.json').read_text());overrides=json.loads((P/'OVERRIDES.json').read_text());source_commit=subprocess.check_output(['git','-C',str(R/'grafikk'),'rev-parse','HEAD'],text=True).strip();base_commit=subprocess.check_output(['git','-C',str(R/'hd-leveranse'),'rev-parse','HEAD'],text=True).strip()
assert base_commit=='4a0ab61efae8ead2f30eeb057d3a02d468ae98bc'
for row in rows:
 rel=row['path'];f=P/'mod-tillegg'/rel;assert sha(f)==row['sha256'];q=C/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,q)
units=sorted({m.unit_of(v['path']) for v in overrides})
for rel in m.file_hashes(BASE):
 if m.unit_of(rel) in units:
  q=C/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(BASE/rel,q)
for row in overrides:
 assert sha(BASE/row['path'])==row['base_sha256'];f=P/'mod-overrides'/row['path'];assert sha(f)==row['sha256'];shutil.copy2(f,C/row['path'])
meta=json.loads((BASE/'mod.json').read_text());meta['created']='2026-10-17 r19 restgrafikk';meta['costumes']=sorted(set(meta.get('costumes',[]))|{Path(v['path']).stem.split('_')[0] for v in rows if v['path'].startswith('costumes/costume')});(C/'mod.json').write_text(json.dumps(meta,indent=2)+'\n')
report=m.flett(BASE,C,OUT,replace=units);meta=json.loads((OUT/'mod.json').read_text());semantic=json.loads((P/'semantic-coverage.json').read_text());meta['revision']='r19-20261017';meta['revision_note']='Restgrafikk: nye figur- og effektserier, PDA, krystaller, bibliotek, svømming, trikkapsler, rotte/felle og Brink med spade. Produksjonen er fortsatt uferdig.';meta['r19']=dict(report='gpt-arbeid/rapporter/restgrafikk-r19-20261016',graphics_commit=source_commit,published_base=base_commit,new_hd_cells=sum(v['path'].endswith('_hd.png') for v in rows),addition_files=len(rows),replacements=len(overrides),remaining_art_cells=semantic['remaining_after_confirmed_mask_classification'],raw_missing=semantic['raw_missing'],engine_palette_masks_without_bitmaps=semantic['confirmed_palette_masks_without_bitmaps'],human_visual_approval=False,full_playthrough=False,integration_requested_by_tom='2026-10-17');(OUT/'mod.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False)+'\n')
with (OUT/'README.md').open('a') as f:f.write('\n17. oktober 2026: r19 legger til 7097 HD-ruter, inkludert tekniske småfragmenter og kontrollert gjenbruk. To eldre Maggie-bilder er erstattet. Alle tidligere r18-rettinger og 55 HD-filmer er bevart. Hele restgrafikken er ikke ferdig: 6232 faktiske bilder og gjennomgang av eldre figurfeil gjenstår. Nye bilder er ikke visuelt godkjent av Tom.\n')
files=m.file_hashes(OUT)
for n in ['mod.json','README.md']:files[n]=sha(OUT/n)
(OUT/'SHA256SUMS').write_text(''.join(f'{h}  {p}\n' for p,h in sorted(files.items())))
ok,msg=m.sjekk(BASE/'SHA256SUMS',OUT);assert ok,msg
old=m.file_hashes(BASE);new=m.file_hashes(OUT);removed=set(old)-set(new);changed={p for p in old if p in new and old[p]!=new[p]};added=set(new)-set(old);assert not removed;assert changed=={v['path'] for v in overrides};assert added=={v['path'] for v in rows}
for v in rows:assert sha(OUT/v['path'])==v['sha256']
films=[p for p in old if p.startswith('san/')];assert all(old[p]==new[p] for p in films);assert len(list((OUT/'san').glob('*.ivf')))==55
report.update(result='PASS',base_commit=base_commit,graphics_commit=source_commit,additions=len(added),changed_files=sorted(changed),removed_files=[],new_hd_cells=meta['r19']['new_hd_cells'],films55_unchanged=True,check=msg)
(R/'testing/integration-r19.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print({k:v for k,v in report.items() if not isinstance(v,list)})
