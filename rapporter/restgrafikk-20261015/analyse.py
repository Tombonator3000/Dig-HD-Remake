import json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter,ImageDraw
root=Path(__file__).resolve().parents[2]
out=root/'rapporter/restgrafikk-20261015'; qa=out/'qa';qa.mkdir(exist_ok=True)
def spans(values):
 vals=np.flatnonzero(values)
 if not len(vals): return []
 cut=np.flatnonzero(np.diff(vals)>1)
 return [(int(vals[a]),int(vals[b])+1) for a,b in zip(np.r_[0,cut+1],np.r_[cut,len(vals)-1])]
summary={}; maps={}
for job in ['fig005_32','fig005_33','fig005_34','fig005_07','fig001_20']:
 attempt='03' if job=='fig005_07' else ('02' if job=='fig005_32' else '01')
 meta=json.loads((out/'fremdrift.json').read_text()); selected=next(d for d in meta['leveranser'] if d['jobb']==job)
 p=root/selected['resultat']; im=Image.open(p).convert('RGBA'); a=np.array(im.getchannel('A')); core=a>=128
 bands=[(y0,y1) for y0,y1 in spans(core.any(axis=1)) if y1-y0>=10]
 boxes=[]; rowcounts=[]
 for y0,y1 in bands:
  xb=[(x0,x1) for x0,x1 in spans(core[y0:y1].any(axis=0)) if x1-x0>=10]
  if job=='fig005_07': xb=[(0,672),(672,1536)]
  rowcounts.append(len(xb))
  for x0,x1 in xb:
   yy,xx=np.nonzero(core[y0:y1,x0:x1]); boxes.append([x0+int(xx.min()),y0+int(yy.min()),int(xx.max()-xx.min()+1),int(yy.max()-yy.min()+1)])
 d=json.loads((root/'jobber'/job/'jobb.json').read_text()); source=Image.open(root/'jobber'/job/'original_1x.png').convert('RGB')
 print(job,'rows',rowcounts,'boxes',boxes)
 assert len(boxes)==len(d['ruter']),(job,len(boxes),len(d['ruter']))
 entries=[]
 for r,b in zip(d['ruter'],boxes):
  x,y,w,h=r['rekt']; arr=np.array(source.crop((x,y,x+w,y+h))); smask=np.any(arr!=np.array(d['bakgrunn']),axis=2)
  smask &= ~((arr[...,0]>=230)&(arr[...,2]>=230)&(arr[...,1]<=120))
  sy,sx=np.nonzero(smask); sb=[int(sx.min()),int(sy.min()),int(sx.max()+1),int(sy.max()+1)]
  sm=Image.fromarray((smask[sb[1]:sb[3],sb[0]:sb[2]]*255).astype('uint8')).resize(((sb[2]-sb[0])*4,(sb[3]-sb[1])*4),Image.Resampling.NEAREST)
  bx,by,bw,bh=b; dm=Image.fromarray(((a[by:by+bh,bx:bx+bw]>=128)*255).astype('uint8')).resize(sm.size,Image.Resampling.NEAREST)
  s=np.array(sm)>0;t=np.array(dm)>0; iou=float((s&t).sum()/max(1,(s|t).sum()))
  entries.append({'bilde':r['bilde'],'native_analyseboks_alfa128':b,'original_rekt':r['rekt'],'original_animasjon':r['animasjon'],'original_retning':r['retning'],'original_lag':r['lag'],'original_nr':r['nr'],'normalized_bbox_iou_diagnostic':round(iou,4),'source_size_ratio':[round(bw/sm.width,4),round(bh/sm.height,4)]})
 maps[job]={'koblinger':entries,'native_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'mapping_method':'Rad og venstre-til-høyre-rekkefølge visuelt kontrollert mot originalarket. Alle separate komponenter innen hver boks beholdes.','runtime_tested':False}
 dil=np.array(Image.fromarray(core.astype('uint8')*255).filter(ImageFilter.MaxFilter(11)))>0
 outside=a[~dil]; suspicious=int((outside>16).sum())
 summary[job]={'size':list(im.size),'mode':im.mode,'sha256':maps[job]['native_sha256'],'alpha_range':[int(a.min()),int(a.max())],'transparent_pixels':int((a==0).sum()),'alpha128_pixels':int(core.sum()),'rows':rowcounts,'mapped_cels':len(entries),'alpha_over16_outside5px_from_core':suspicious,'max_alpha_outside5px':int(outside.max()),'normalized_iou_min':min(e['normalized_bbox_iou_diagnostic'] for e in entries),'normalized_iou_median':float(np.median([e['normalized_bbox_iou_diagnostic'] for e in entries])),'runtime_tested':False}
 # QA images are inspection composites; native files stay byte-identical.
 canvas=Image.new('RGB',(1536,1088),'white');draw=ImageDraw.Draw(canvas)
 draw.text((10,10),job+' / original (venstre), native alfa over hvitt (hoyre)',fill='black')
 canvas.paste(Image.open(root/'jobber'/job/'referanse.png').convert('RGB').resize((768,512)),(0,40))
 white=Image.new('RGBA',im.size,'white');white.alpha_composite(im);canvas.paste(white.convert('RGB').resize((768,512)),(768,40))
 draw.text((10,565),'Native alfa over gront (venstre) og svart (hoyre). Ingen bildeendring i leveransen.',fill='black')
 for k,bg in enumerate([(50,170,70,255),(0,0,0,255)]):
  comp=Image.new('RGBA',im.size,bg);comp.alpha_composite(im);canvas.paste(comp.convert('RGB').resize((768,512)),(768*k,592))
 canvas.save(qa/(job+'-kontroll.png'))
 print('IoU min/median',summary[job]['normalized_iou_min'],summary[job]['normalized_iou_median'],'outside alpha>16',suspicious)
(out/'qa-malinger-reprodusert.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n')
(out/'rutekart-reprodusert.json').write_text(json.dumps(maps,indent=2,ensure_ascii=False)+'\n')
