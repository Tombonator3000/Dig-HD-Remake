from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
root=Path(__file__).resolve().parents[2];out=root/'rapporter/zz-ovrige-66-20261015';qa=out/'qa';qa.mkdir(exist_ok=True)
plan=json.loads((out/'plan.json').read_text())['jobs'];maps={};measure={}
files={'fig229_12':'02','fig229_22':'01','fig214_18':'01','fig214_19':'01','fig213_19':'01','fig071_08':'01','fig213_01':'02'}
windows={
 'fig229_12': [[0,25,610,185],[610,25,1536,185],[0,185,645,290],[645,185,1536,290],[0,290,640,401],[640,290,1536,401]]+[[x0,y0,x1,y1] for y0,y1 in [(401,524),(524,643),(643,753),(753,858)] for x0,x1 in [(0,532),(532,1017),(1017,1536)]]+[[0,858,572,1024],[572,858,1536,1024]],
 'fig229_22': [[a,0,b,1024] for a,b in [(0,430),(430,760),(760,1015),(1015,1290),(1290,1536)]],
 'fig214_18': [[0,0,483,500],[483,0,1010,500],[1010,0,1536,500],[0,500,660,1024],[660,500,1536,1024]],
 'fig214_19': [[0,0,680,530],[680,0,1536,530],[0,530,750,1024]],
 'fig213_19': [[0,0,320,500],[320,0,700,500]],
 'fig071_08': [[a,0,b,500] for a,b in [(0,312),(312,576),(576,839),(839,1104),(1104,1293),(1293,1536)]]+[[0,500,250,1024],[250,500,520,1024]],
 'fig213_01': [[0,680,230,1024],[230,0,1536,1024]],
}
for job,att in files.items():
 manifest=json.loads((out/'fremdrift.json').read_text()); delivery=next(d for d in manifest['leveranser'] if d['jobb']==job)
 p=root/delivery['resultat'];im=Image.open(p).convert('RGBA');a=np.array(im.getchannel('A'));assert im.size==(1536,1024);assert a.min()==0
 srcfolder=root/'jobber'/job;meta=json.loads((srcfolder/'jobb.json').read_text());src=Image.open(srcfolder/'original_1x.png').convert('RGB');entries=[]
 claimed=np.zeros(a.shape,bool)
 assert len(plan[job]['ruter'])==len(windows[job]),job
 for r,rect in zip(plan[job]['ruter'],windows[job]):
  x0,y0,x1,y1=rect;mask=a[y0:y1,x0:x1]>=16;yy,xx=np.nonzero(mask);assert len(xx),r['bilde']
  box=[x0+int(xx.min()),y0+int(yy.min()),int(xx.max()-xx.min()+1),int(yy.max()-yy.min()+1)]
  bx,by,bw,bh=box;claimed[y0:y1,x0:x1]=True
  x,y,w,h=r['rekt'];original=np.array(src.crop((x,y,x+w,y+h)));m=np.any(original!=np.array(meta['bakgrunn']),axis=2);m &= ~((original[...,0]>=230)&(original[...,2]>=230)&(original[...,1]<=120))
  oy,ox=np.nonzero(m);sbox=[int(ox.min()),int(oy.min()),int(ox.max()+1),int(oy.max()+1)];source_mask=Image.fromarray((m[sbox[1]:sbox[3],sbox[0]:sbox[2]]*255).astype('uint8')).resize(((sbox[2]-sbox[0])*4,(sbox[3]-sbox[1])*4),Image.Resampling.NEAREST)
  dm=Image.fromarray(((a[by:by+bh,bx:bx+bw]>=128)*255).astype('uint8')).resize(source_mask.size,Image.Resampling.NEAREST);sm=np.array(source_mask)>0;nm=np.array(dm)>0
  iou=float((sm&nm).sum()/max(1,(sm|nm).sum()));near=np.array(source_mask.filter(ImageFilter.MaxFilter(17)))>0;near_cover=float((nm&near).sum()/max(1,nm.sum()))
  entries.append({'bilde':r['bilde'],'rect':box,'box_alpha_threshold':16,'source_rekt':r['rekt'],'source_original_pixels':r['visible_pixels'],'animasjon':r['animasjon'],'retning':r['retning'],'lag':r['lag'],'nr':r['nr'],'normalized_core_iou_diagnostic':round(iou,4),'native_core_within8px_of_source_diagnostic':round(near_cover,4),'game_tested':False})
 maps[job]={'koblinger':entries,'native_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'native_source':str(p.relative_to(root)),'box_threshold':16,'method':'Eksplisitte, visuelt kontrollerte fasevinduer; alle alfa-16-fragmenter innen hvert vindu beholdes. IoU er diagnostikk etter boksnormalisering, ikke motorregistrering.'}
 measure[job]={'size':list(im.size),'mode':'RGBA','alpha_range':[int(a.min()),int(a.max())],'requested_cels':len(entries),'alpha16_pixels_outside_phase_windows':int(((a>=16)&~claimed).sum()),'source_original_visible_pixels':sum(r['visible_pixels'] for r in plan[job]['ruter']),'native_alpha128_pixels':int((a>=128).sum()),'iou_min_diagnostic':min(e['normalized_core_iou_diagnostic'] for e in entries),'iou_median_diagnostic':float(np.median([e['normalized_core_iou_diagnostic'] for e in entries])),'game_tested':False}
 canvas=Image.new('RGB',(1536,1104),'white');draw=ImageDraw.Draw(canvas);draw.text((10,10),job+' / original (venstre), faktisk native alfa over hvitt (hoyre)',fill='black');canvas.paste(Image.open(srcfolder/'referanse.png').convert('RGB').resize((768,512)),(0,40))
 for position,bg in [((768,40),(255,255,255,255)),((0,592),(40,160,75,255)),((768,592),(0,0,0,255))]:
  c=Image.new('RGBA',im.size,bg);c.alpha_composite(im);canvas.paste(c.convert('RGB').resize((768,512)),position)
 draw.text((10,565),'Native alfa over gront / svart. Komposisjoner er bare QA; native-filen er uendret.',fill='black');canvas.save(qa/(job+'-kontroll.png'))
 print(job,'ruter',len(entries),'min/medianIoU',measure[job]['iou_min_diagnostic'],round(measure[job]['iou_median_diagnostic'],3),'utenfor fasevinduer',measure[job]['alpha16_pixels_outside_phase_windows'])
 # Source/native normalized pairs make sparse fragments inspectable at the same size.
 tile_w=768;tile_h=290;cols=2;rows=(len(entries)+1)//2;contact=Image.new('RGB',(tile_w*cols,tile_h*rows),(55,75,90));dr=ImageDraw.Draw(contact)
 for idx,(r,e) in enumerate(zip(plan[job]['ruter'],entries)):
  X=(idx%cols)*tile_w;Y=(idx//cols)*tile_h;dr.text((X+8,Y+8),r['bilde']+' : original / ny',fill='white')
  x,y,w,h=r['rekt'];crop=src.crop((x,y,x+w,y+h)).convert('RGBA');ar=np.array(crop);bg=np.all(ar[:,:,:3]==np.array(meta['bakgrunn']),axis=2);tech=(ar[:,:,0]>=230)&(ar[:,:,2]>=230)&(ar[:,:,1]<=120);ar[:,:,3]=np.where(bg|tech,0,255);orig=Image.fromarray(ar)
  bx,by,bw,bh=e['rect'];native=im.crop((bx,by,bx+bw,by+bh))
  for k,obj in enumerate([orig,native]):
   factor=min(350/obj.width,240/obj.height);rs=obj.resize((max(1,round(obj.width*factor)),max(1,round(obj.height*factor))),Image.Resampling.NEAREST if k==0 else Image.Resampling.LANCZOS);contact.paste(rs,(X+k*384+int((384-rs.width)/2),Y+35),rs)
 contact.save(qa/(job+'-par.png'))
for job in ['fig222_18','fig222_19']:
 base=plan[job]['reuse_from'];d=json.loads(json.dumps(maps[base]));d['reuse_from']=base
 for row,r in zip(d['koblinger'],plan[job]['ruter']):row['bilde']=r['bilde'];row['source_rekt']=r['rekt']
 maps[job]=d;measure[job]=dict(measure[base],reused_from=base)
(out/'rutekart-reprodusert.json').write_text(json.dumps(maps,ensure_ascii=False,indent=2)+'\n');(out/'qa-malinger-reprodusert.json').write_text(json.dumps(measure,ensure_ascii=False,indent=2)+'\n')
assert sum(len(d['koblinger']) for d in maps.values())==53
print('53 unike nye mål-ID-er mappet.')
