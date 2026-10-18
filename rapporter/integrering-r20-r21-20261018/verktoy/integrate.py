"""Integrate committed r20+r21 over published r19 with exact declared units."""
from pathlib import Path
import json,hashlib,shutil,subprocess,sys
R=Path('/home/tom/Documents/ChatGPT/THE DIG');sys.path.insert(0,str(R/'kode/pipeline'));from dighd import modflett as m
P=R/'grafikk/rapporter/integrering-r20-r21-20261018';P.mkdir(exist_ok=True);(P/'verktoy').mkdir(exist_ok=True)
BASE=R/'testing/r20-r21-published-base';C=R/'r20-r21-input';OUT=R/'hd-integrert-r20-r21';B=R/'hd-leveranse';P20=R/'grafikk/rapporter/restgrafikk-r20-20261017';P21=R/'grafikk/rapporter/restgrafikk-r21-20261017'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
base_commit=subprocess.check_output(['git','-C',str(B),'rev-parse','HEAD'],text=True).strip();assert base_commit=='630cadb3ebb398ac8ade1f4e1ea759f8a783cd5a'
source_commit=subprocess.check_output(['git','-C',str(R/'grafikk'),'rev-parse','HEAD'],text=True).strip()
assert not OUT.exists()
if not BASE.exists():shutil.copytree(B,BASE,ignore=shutil.ignore_patterns('.git'))
C.mkdir(exist_ok=True)
add=json.loads((P20/'ADDITIONS.json').read_text());over=json.loads((P21/'REPLACEMENTS.json').read_text());assert len(add)==442 and len(over)==210
old=m.file_hashes(BASE)
for rel,h in add.items():
 assert rel not in old;src=P20/'mod-tillegg'/rel;assert sha(src)==h;dst=C/rel;dst.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(src,dst)
units=sorted({m.unit_of(rel) for rel in over});assert len(units)==105
for rel in old:
 if m.unit_of(rel) in units:
  dst=C/rel;dst.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(BASE/rel,dst)
for rel,h in over.items():
 src=P21/'mod-erstatninger'/rel;assert sha(src)==h;shutil.copy2(src,C/rel)
meta=json.loads((BASE/'mod.json').read_text());meta['created']='2026-10-18 r20+r21';meta['costumes']=sorted(set(meta['costumes'])|{Path(f).stem.split('_')[0] for f in add});(C/'mod.json').write_text(json.dumps(meta,indent=2)+'\n')
rep=m.flett(BASE,C,OUT,replace=units)
meta=json.loads((OUT/'mod.json').read_text());meta['revision']='r21-20261018';meta['revision_note']='R20 og r21: 196 Nexus-faser,25 nye canyon-ruter og105 omtegnede canyon-ruter med riktige indeksreferansepaletter.';meta['r20_r21']=dict(graphics_commit=source_commit,published_base=base_commit,new_hd_cels=221,repainted_hd_cels=105,addition_files=442,replacement_files=210,replacement_units=105,remaining_art_cels=6011,engine_changed=False,human_visual_approval=False,full_playthrough=False,integration_requested_by_tom='2026-10-18',reports=['gpt-arbeid/rapporter/restgrafikk-r20-20261017','gpt-arbeid/rapporter/restgrafikk-r21-20261017']);(OUT/'mod.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False)+'\n')
with (OUT/'README.md').open('a') as f:f.write('\n18. oktober 2026: r20 og r21 integrert.221 nye HD-ruter:196 Nexus-faser og25 canyon-ruter.105 eldre canyon-ruter og105 indeksreferansepaletter rettet. Tidligere rettinger og55 HD-filmer bevart.6011 faktiske bilder og øvrige eldre grafikkfeil gjenstår. Nye ruter er ikke visuelt godkjent av Tom, og full gjennomspilling er ikke gjort.\n')
new=m.file_hashes(OUT);assert set(old)<=set(new);assert set(new)-set(old)==set(add);changed={f for f in old if old[f]!=new[f]};assert changed==set(over)
for rel,h in (add|over).items():assert new[rel]==h
films=[f for f in old if f.startswith('san/')];assert all(old[f]==new[f] for f in films);assert len(list((OUT/'san').glob('*.ivf')))==55
files=new|{n:sha(OUT/n) for n in ['README.md','mod.json']};(OUT/'SHA256SUMS').write_text(''.join(f'{h}  {p}\n' for p,h in sorted(files.items())))
ok,msg=m.sjekk(BASE/'SHA256SUMS',OUT);assert ok,msg
rep.update(base_commit=base_commit,graphics_commit=source_commit,added_files=442,replaced_files=210,new_hd_cels=221,repainted_hd_cels=105,files_removed=[],hd_movies_unchanged=55,check=msg,result='PASS')
(P/'integration.json').write_text(json.dumps(rep,indent=2,ensure_ascii=False)+'\n');(P/'payload.json').write_text(json.dumps(add|over,indent=2)+'\n')
print(msg);print('units',len(rep['lagt_til']),len(rep['erstattet']),'films preserved55')
