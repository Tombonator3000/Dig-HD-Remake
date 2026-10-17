"""Register whole native drawings; explicit replacements of 105 bad r19 cels."""
from pathlib import Path
import sys,json,hashlib,shutil
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[4];P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'kode/pipeline'))
from dighd import myk
plans=json.loads((P/'canyon-plans.json').read_text());O=P/'mod-erstatninger/costumes';O.mkdir(parents=True,exist_ok=True);B=R/'hd-leveranse/costumes';records=[];rejects=[]
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
for batch in plans['batches']:
 master=P/(batch['stem']+'-master.png')
 if not master.exists():continue
 a=np.array(Image.open(master).convert('RGBA'));h,w=a.shape[:2]
 for c in batch['cells']:
  selected=master;slot=c['slot'];single=P/(f'canyon034-{c["cel"]:03d}-single-master.png')
  if single.exists():selected=single;tile=np.array(Image.open(single).convert('RGBA'))
  else:tile=a[round(slot//4*h/2):round((slot//4+1)*h/2),round(slot%4*w/4):round((slot%4+1)*w/4)].copy()
  # Cel23 has a verified isolated ink speck beside the palm. Do not apply
  # this stronger cleanup to other poses: cel5 has a real detached fragment.
  minimum=64 if c['cel']==23 else 8
  owner,_,parts=myk.parts(tile[:,:,3]);keep=np.isin(owner,[v['nr'] for v in parts if v['areal']>=minimum]);tile[~keep]=0
  yy,xx=np.where(tile[:,:,3]>128)
  if not len(xx):rejects.append(dict(cel=c['cel'],reason='empty'));continue
  bb=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)];native=tile[bb[1]:bb[3],bb[0]:bb[2]]
  x,y,r,b=c['source_bbox'];sw,sh=r-x,b-y;sx=sw*4/native.shape[1];sy=sh*4/native.shape[0];common=(sx*sy)**.5;dev=max(abs(sx/common-1),abs(sy/common-1))
  fit=myk._premul_resize(native,(sw*4,sh*4));source_alpha=np.array(Image.open(P/'originaler'/(c['name']+'.png')))[:,:,3]>128;source_alpha=np.repeat(np.repeat(source_alpha[y:b,x:r],4,axis=0),4,axis=1);alpha=fit[:,:,3]>128;iou=float((source_alpha&alpha).sum()/max(1,(source_alpha|alpha).sum()))
  rec=dict(cel=c['cel'],file=c['name']+'_hd.png',master=selected.name,master_sha256=sha(selected),slot=0 if single.exists() else slot,original_atlas_slot=slot,native_grid=[1,1] if single.exists() else [4,2],native_tile_bbox=bb,source_bbox=c['source_bbox'],axis_deviation=dev,alpha_iou=iou,old_sha256=sha(B/(c['name']+'_hd.png')),approved_references={n:sha(R/'grafikk/hovedark'/(n+'.png')) for n in ['boston','maggie','brink']},method='one independently painted whole unit, native alpha, head never moved separately')
  if dev>.12 or iou<.6:
   rejects.append(rec)
   (O/rec['file']).unlink(missing_ok=True)
   continue
  ow,oh=c['source_size'];out=Image.new('RGBA',((ow+8)*4,(oh+8)*4));out.alpha_composite(Image.fromarray(fit),((x+4)*4,(y+4)*4));out.save(O/rec['file']);rec['sha256']=sha(O/rec['file'])
  # Existing RGBS palettes are wrong for this scripted canyon actor. The
  # engine also uses the index PNG's PLTE for HD palette adaptation. Keep
  # physical codes identical but register the AKPL -> room15 palette0 PLTE.
  idxname=c['name']+'_idx.png';src=P/'originaler'/idxname
  assert np.array_equal(np.array(Image.open(src)),np.array(Image.open(B/idxname)))
  shutil.copy2(src,O/idxname)
  rec.update(index_file=idxname,index_sha256=sha(O/idxname),old_index_sha256=sha(B/idxname),source_index_values_unchanged=True,index_palette='AKPL mapped through room15 palette0')
  records.append(rec)
(P/'registration.json').write_text(json.dumps(records,indent=2)+'\n');(P/'rejected-shapes.json').write_text(json.dumps(rejects,indent=2)+'\n')
manifest={str(f.relative_to(P/'mod-erstatninger')):sha(f) for f in sorted((P/'mod-erstatninger').rglob('*.png'))};(P/'REPLACEMENTS.json').write_text(json.dumps(manifest,indent=2)+'\n')
preview=Image.new('RGB',(1920,((len(records)+5)//6)*260),'#424650');draw=ImageDraw.Draw(preview)
for i,r in enumerate(records):
 x=i%6*320;y=i//6*260;draw.text((x+5,y+5),r['file'],fill='white')
 for j,im in enumerate([Image.open(P/'originaler'/r['file'].replace('_hd','')),Image.open(O/r['file'])]):
  im=im.convert('RGBA');im=im.crop(im.getbbox());im.thumbnail((150,220));preview.paste(im,(x+j*160+(150-im.width)//2,y+30+(220-im.height)//2),im)
preview.save(P/'preview.png');print('Accepted',len(records),'Rejected',[(r['cel'],round(r.get('axis_deviation',0),3),round(r.get('alpha_iou',0),3)) for r in rejects])
