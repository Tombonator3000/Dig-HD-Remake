from pathlib import Path
import sys,shutil,json,hashlib
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'kode/pipeline'))
from dighd import modflett as m
BASE=R/'hd-integrert-r17';C=R/'r18-input';OUT=R/'hd-integrert-r18';OV=R/'grafikk/rapporter/spillfeil-r18-20261016/mod-overrides';P=R/'hd-leveranse';C.mkdir(exist_ok=True)
units={m.unit_of(str(f.relative_to(OV))) for f in OV.rglob('*') if f.is_file()}
for f in BASE.rglob('*'):
 if f.is_file() and m.unit_of(str(f.relative_to(BASE))) in units:
  q=C/f.relative_to(BASE);q.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(f,q)
for f in OV.rglob('*'):
 if f.is_file():
  q=C/f.relative_to(OV);q.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(f,q)
shutil.copy2(BASE/'mod.json',C/'mod.json');report=m.flett(BASE,C,OUT,replace=sorted(units));meta=json.loads((OUT/'mod.json').read_text());meta['revision']='r18-20261016';meta['revision_note']='Figurkontakter og palett, pole, to måner, plateau/utgravd åpning, tram-gangflate, edderkoppsilhuett, tett rist og laserstråler.';meta['r18']={'report':'gpt-arbeid/rapporter/spillfeil-r18-20261016','human_visual_approval':False,'files':len(list(OV.rglob('*.png'))),'original_indices_preserved':True,'approved_character_reference':'hovedark/boston.png','integration_requested_by_tom':'2026-10-16'};(OUT/'mod.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');p=OUT/'README.md';p.write_text(p.read_text()+'\n16. oktober: r18 retter figurkontakter, pole, måner, plateau, tram-gangflate, edderkopp, rist og laserstråler. R17 er med. Alle r16-rettinger og55 HD-filmer bevart. Full gjennomspilling og Toms visuelle godkjenning av alle nye ruter gjenstår.\n');files=m.file_hashes(OUT)
for p in ['README.md','mod.json']:files[p]=m._sha256(OUT/p)
(OUT/'SHA256SUMS').write_text(''.join(f'{h}  {p}\n' for p,h in sorted(files.items())))
ok,msg=m.sjekk(BASE/'SHA256SUMS',OUT);assert ok,msg
old=m.file_hashes(BASE);new=m.file_hashes(OUT);allowed={str(f.relative_to(OV)) for f in OV.rglob('*') if f.is_file()};assert set(old)<=set(new);changed={p for p in old if old[p]!=new[p]};added=set(new)-set(old);assert (changed|added)<=allowed
for f in (BASE/'san').rglob('*'):
 if f.is_file():assert f.read_bytes()==(OUT/f.relative_to(BASE)).read_bytes()
for p in changed|added|{'README.md','mod.json','SHA256SUMS'}:
 q=P/p;q.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(OUT/p,q)
report.update(check=msg,changed_files=len(changed),added_files=len(added),no_files_removed=True,films55_unchanged=True);(R/'testing/integration-r18.json').write_text(json.dumps(report,indent=2));print(msg,len(changed),len(added),'all55films preserved')
