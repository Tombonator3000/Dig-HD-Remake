from pathlib import Path
import json,re,hashlib,shutil
R=Path(__file__).resolve().parent;P=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk/rapporter/spillfeil-r12-20261013');D=P/'produksjon';D.mkdir(exist_ok=True);S=Path('/home/tombonator3000t/.codex/sessions/2026/10/13/rollout-2026-10-13T11-16-30-01a1348c-93eb-7bc3-83cf-edfb9bc273c8.jsonl');out=[]
for line in S.open():
 try:a=json.loads(line)
 except json.JSONDecodeError:continue
 p=a.get('payload',{});arg=p.get('input',p.get('arguments',''))
 if p.get('type') in ['function_call','custom_tool_call'] and p.get('name','').endswith('exec') and 'tools.image_gen__imagegen' in arg:
  out.append({'timestamp':a.get('timestamp'),'call_id':p.get('call_id'),'exact_tool_script':arg})
(D/'imagegen-tool-provenance.json').write_text(json.dumps({'generator':'built-in ChatGPT imagegen','exact_model':'not exposed','calls':out},ensure_ascii=False,indent=2));print('Recovered',len(out),'image generation calls')
