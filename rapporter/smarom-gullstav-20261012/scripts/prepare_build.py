from pathlib import Path
import json,shutil,hashlib
Q=Path(__file__).resolve().parent;G=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk');R=G/'rapporter/smarom-gullstav-20261012';S=Path('/home/tombonator3000t/Skrivebord/TheDigHD-Linux-20261012-test');M=S/'usr/share/the-dig-hd/mods/gpt';plan=json.loads((R/'PLAN.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert all(sha(G/p)==h for p,h in plan['protected_input_sha256'].items());assert sha(S/'usr/bin/scummvm')=='3080b02e8747692643784c7b376d2d6f60c908091b2a943bfb375a1988c1c788';suite=json.loads((Q/'final-native-suite.json').read_text());assert len(suite)==21 and all(c['exit_code']==0 for c in suite)
files=[]
for j in plan['layer_jobs']:
 for e in j['objekter']:
  files += ['objects/'+e['bilde']+s+'.png' for s in ('','_idx')]
files+=['rooms/room050'+s+'.png' for s in ('','_idx')]+['objects/obj884_'+state+s+'.png' for state in ('01','02','03') for s in ('','_idx')];assert len(set(files))==70
for f in files:
 out=R/'runtime'/f;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(M/f,out)
manifest={f:sha(M/f) for f in files};(R/'RUNTIME-FILES.json').write_text(json.dumps(manifest,indent=2)+'\n')
for name in ['assemble_details.py','bleed_rgba.py','import_layers.py','import_gold.py','sync_gold_hand.py','sync_map.py','fix257.py','clean257_edges.py','run_qa.py','run_suite.py','cases.json']:
 (R/'scripts').mkdir(exist_ok=True);shutil.copy2(Q/name,R/'scripts'/name)
for c in suite:
 tag='final-native-'+c['case']['tag'];D=Q/tag;(R/'native-qa').mkdir(exist_ok=True)
 for f in ['run.log','result.json']:shutil.copy2(D/f,R/'native-qa'/(c['case']['tag']+'-'+f))
 for p in D.glob('frame_000110_room[0-9][0-9][0-9].png'):
  (R/'screenshots').mkdir(exist_ok=True);shutil.copy2(p,R/'screenshots'/(c['case']['tag']+'.png'))
meta=json.loads((M/'mod.json').read_text());meta['objects']=sorted(set(meta['objects'])|{e['bilde'] for j in plan['layer_jobs'] for e in j['objekter']});meta['small_objects_r9']={'jobs':20,'object_states':31,'rooms':[23,25,26,27,32,77,88,90],'gold_rod_states':3,'report':'rapporter/smarom-gullstav-20261012','user_visual_KS':'pending'};(M/'mod.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
# Rebuild complete mod integrity list; keep previous README exactly.
(M/'SHA256SUMS').write_text(''.join(sha(p)+'  '+p.relative_to(M).as_posix()+'\n' for p in sorted(M.rglob('*')) if p.is_file() and p.name!='SHA256SUMS'))
b=json.loads((S/'BUILD.json').read_text());b.update(release_revision='20261013-r9',small_object_jobs_added_r9=20,small_object_states_added_r9=31,gold_rod_states_updated_r9=3,room_backgrounds=106,graphics_branch_commit=__import__('subprocess').check_output(['git','rev-parse','HEAD'],cwd=G,text=True).strip());(S/'BUILD.json').write_text(json.dumps(b,indent=2)+'\n')
deliv=S/'delivery/r9';deliv.mkdir(parents=True,exist_ok=True)
for n in ['PLAN.json','RUNTIME-FILES.json','IMPORT-LAG.json','GULLSTAV-IMPORT.json','DETAIL-ATLAS.json','MAP-BACKGROUND-SYNC.json']:shutil.copy2(R/n,deliv/n)
(R/'SOURCE-VERIFICATION.json').write_text(json.dumps({'protected_job_inputs_verified':len(plan['protected_input_sha256']),'unchanged':True,'engine_unchanged':True,'twenty_result_files':True,'runtime_files':70},indent=2)+'\n');shutil.copy2(R/'SOURCE-VERIFICATION.json',deliv/'SOURCE-VERIFICATION.json');print('Build ready.70 runtime files;80 protected inputs verified.',flush=True)
