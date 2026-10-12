from pathlib import Path
from PIL import Image,ImageChops,ImageFilter
import numpy as np
import json,re,shutil
Q=Path(__file__).resolve().parent;R=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk/rapporter/smarom-gullstav-20261012');cases=json.loads((Q/'cases.json').read_text());suite=json.loads((Q/'packaged-suite.json').read_text());assert len(suite)==21 and all(c['exit_code']==0 for c in suite);results=[];visible=[];zero=[]
for c in cases:
 D=Q/('packaged-'+c['tag']);N=Q/('final-native-'+c['tag']);r=json.loads((D/'result.json').read_text());assert r['passed'];log=(D/'run.log').read_text();n=next(N.glob('frame_000110_room[0-9][0-9][0-9].png'));p=D/n.name;a=Image.open(n).convert('RGB');b=Image.open(p).convert('RGB');identical=ImageChops.difference(a,b).getbbox() is None;phase=None
 if not identical:
  assert c['room']==25
  aa=np.array(Image.open(N/n.name.replace('.png','_flat.png')).convert('RGB'));bb=np.array(Image.open(D/n.name.replace('.png','_flat.png')).convert('RGB'));fd=np.any(aa!=bb,2);assert fd.any();mask=np.array(Image.fromarray(fd.astype('uint8')*255).filter(ImageFilter.MaxFilter(25)))>0;hd=np.any(np.array(a)!=np.array(b),2);outside=int(np.count_nonzero(hd&~mask));max_outside_delta=int(np.abs(np.array(a).astype(int)-np.array(b).astype(int))[hd&~mask].max()) if outside else 0
  phase={'reason':'room25 water colour-cycle phase varies with elapsed wall time; original flat frame also differs','hd_differing_pixels':int(hd.sum()),'original_flat_differing_pixels':int(fd.sum()),'outside_3_native_pixel_neighbourhood':outside,'maximum_channel_difference_outside':max_outside_delta,'comparison_status':'informational, not pixel-identical; within-run redraw checks and packaged-content hashes are the pass criteria'}
 for obj in c['objects']:
  i=int(obj[3:6]);s=int(obj[7:],16);lines=[l for l in log.splitlines() if f'test object {i} state {s} frame 110:' in l];assert len(lines)==1 and 'drawn yes, HD image yes' in lines[0],(obj,lines);visible.append({'case':c['tag'],'object':obj,'evidence':lines[0]})
  if int(re.search(r'HD object px (\d+)',lines[0]).group(1))==0:zero.append(obj)
 (R/'packaged-qa').mkdir(exist_ok=True)
 for f in ['run.log','result.json']:shutil.copy2(D/f,R/'packaged-qa'/(c['tag']+'-'+f))
 shutil.copy2(p,R/'screenshots'/('packaged-'+c['tag']+'.png'));results.append({'case':c,**r,'native_final_frame_pixel_identical':identical,'original_cycle_phase_comparison':phase})
qa={'passed':True,'cases':results,'cases_count':21,'redraw_checks':sum(len(r['checks']) for r in results),'native_final_frames_pixel_identical':sum(r['native_final_frame_pixel_identical'] for r in results),'nonidentical_animated_frame_comparisons':sum(r['original_cycle_phase_comparison'] is not None for r in results),'requested_object_states':31,'rod_states':3,'visibility_evidence':visible,'object_sources_reused_as_HD_room':sorted(set(zero)),'scope':'Isolated saved-game copies, forced object states, not full playthrough or physical keyboard test. Room77 fixture simultaneously shows markers for coverage; this is not a normal progression state. Every requested image loads; source pixels identical to background can be rendered as HD room rather than HD object.','manual_visual_KS_pending':['lag027_03_del2av8','lag032_05','lag032_07']};(R/'QA-APPIMAGE.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n');print({k:v for k,v in qa.items() if k not in ['cases','visibility_evidence']},flush=True)
