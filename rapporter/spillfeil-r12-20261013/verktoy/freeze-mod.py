from pathlib import Path
import hashlib, json, datetime, shutil, subprocess
R=Path(__file__).resolve().parent
P=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk/rapporter/spillfeil-r12-20261013')
M=R/'AppDir/usr/share/the-dig-hd/mods/gpt'
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
subprocess.run([str(R/'pyenv/bin/python'),str(R/'freeze-report.py')],check=True,cwd=R)
report=json.loads((P/'OVERSTYRINGER-MANIFEST.json').read_text())
assert not report['candidate_mismatches'],report['candidate_mismatches']
assert not list(M.rglob('*.hold'))
meta=json.loads((M/'mod.json').read_text())
meta['revision_note']='r12: kildestyrte lysfaser, bryterkrystaller, linse og hull, Boston-handlinger, Brink-hoder og syk palett, museum og PDA'
meta['created']=datetime.datetime.now(datetime.timezone.utc).isoformat()
meta['overrides_manifest_sha256']=sha(P/'OVERSTYRINGER-MANIFEST.json')
meta['r12']={'base_hd_mod':'113523ba12fd10fbf2a9ff49b3823cd9aa8095c6','overrides_files':len(report['files']),'overrides_visual_states':report['actual_art_states'],'report':'rapporter/spillfeil-r12-20261013','human_visual_approval':False,'full_game_hd_complete':False,'engine_pull_request':51}
meta['costumes']=sorted({p.stem.split('_')[0] for p in (M/'costumes').glob('*.png')})
meta['costume_cels']=len(list((M/'costumes').glob('*_idx.png')))
meta['available_visual_costume_cels']=len({p.name.replace('_hd','').removesuffix('.png') for p in (M/'costumes').glob('*.png') if not p.name.endswith('_idx.png')})
(M/'mod.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
(M/'README.md').write_text('# The Dig HD r12\n\nKomplett HD-mod fra r11 med de kontrollerte r12-rettingene. Krever motorrettingene fra PR #51.\n\nProduksjon, kildegrunnlag, metodeanalyse og kontroll: grafikkgrenen gpt-arbeid, rapporter/spillfeil-r12-20261013.\n\nDette er en integrert og teknisk kontrollert leveranse. Hele spillet er ikke gjennomspilt, og Toms visuelle godkjenning av alle nye bilder gjenstår.\n')
files=sorted(p for p in M.rglob('*') if p.is_file() and p.name!='SHA256SUMS')
(M/'SHA256SUMS').write_text(''.join(f'{sha(p)}  {p.relative_to(M).as_posix()}\n' for p in files))
subprocess.run(['sha256sum','--quiet','-c','SHA256SUMS'],cwd=M,check=True)
record={'files':len(files),'sha256sums_sha256':sha(M/'SHA256SUMS'),'mod_json_sha256':sha(M/'mod.json'),'overrides_manifest_sha256':meta['overrides_manifest_sha256'],'frozen_at':meta['created']}
(R/'MOD-FROZEN.json').write_text(json.dumps(record,indent=2)+'\n')
shutil.copy2(R/'MOD-FROZEN.json',P/'MOD-FROZEN.json')
print(json.dumps(record),flush=True)
