"""Prepare source-registered native-alpha drawings, with explicit shape gates."""
from pathlib import Path
import sys,json,hashlib,shutil
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[4];P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'kode/pipeline'));from dighd import myk
plans=json.loads((P/'plans.json').read_text());O=P/'mod-tillegg/costumes';O.mkdir(parents=True,exist_ok=True);records=[];rejects=[]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for batch in plans['batches']:
 master=P/(batch['stem']+'-master.png');a=np.array(Image.open(master).convert('RGBA'));h,w=a.shape[:2]
 for c in batch['cells']:
  slot=c['slot'];selected=master;single=P/(c['name']+'-single-master.png')
  if single.exists():selected=single;tile=np.array(Image.open(single).convert('RGBA'))
  else:tile=a[round(slot//4*h/2):round((slot//4+1)*h/2),round(slot%4*w/4):round((slot%4+1)*w/4)].copy()
  # Ignore invisible RGB and isolated encoding specks. Preserve painted native edges.
  owner,_,parts=myk.parts(tile[:,:,3]);keep=np.isin(owner,[p['nr'] for p in parts if p['areal']>=8]);tile[~keep]=0
  yy,xx=np.where(tile[:,:,3]>128);bb=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)];native=tile[bb[1]:bb[3],bb[0]:bb[2]];x,y,r,b=c['source_bbox'];sw,sh=r-x,b-y;sx=sw*4/native.shape[1];sy=sh*4/native.shape[0];common=(sx*sy)**.5;dev=max(abs(sx/common-1),abs(sy/common-1))
  fit=myk._premul_resize(native,(sw*4,sh*4));src=np.array(Image.open(P/'originaler'/(c['name']+'.png')))[:,:,3]>128;src=np.repeat(np.repeat(src[y:b,x:r],4,axis=0),4,axis=1);aa=fit[:,:,3]>128;iou=float((src&aa).sum()/max(1,(src|aa).sum()))
  rec=dict(name=c['name'],cel=c['cel'],file=c['name']+'_hd.png',master=selected.name,master_sha256=sha(selected),slot=0 if single.exists() else slot,native_grid=[1,1] if single.exists() else [4,2],native_tile_bbox=bb,source_bbox=c['source_bbox'],source_size=c['source_size'],alpha_iou=iou,axis_deviation=dev,source_index_values_unchanged=True,method='whole native drawing registered as a unit; no separately transformed head',approved_boston_sha256=sha(R/'grafikk/hovedark/boston.png'))
  if dev>.12 or iou<.6:
   rejects.append(rec);(O/rec['file']).unlink(missing_ok=True);continue
  ow,oh=c['source_size'];out=Image.new('RGBA',((ow+8)*4,(oh+8)*4));out.alpha_composite(Image.fromarray(fit),((x+4)*4,(y+4)*4));assert not (R/'testing/r22-published-base/costumes'/rec['file']).exists();out.save(O/rec['file']);rec['sha256']=sha(O/rec['file']);index=c['name']+'_idx.png';assert np.array_equal(np.array(Image.open(P/'originaler'/index)),np.array(Image.open(R/'testing/source/costumes'/index)));shutil.copy2(P/'originaler'/index,O/index);rec['index_sha256']=sha(O/index);records.append(rec)
(P/'registration.json').write_text(json.dumps(records,indent=2)+'\n');(P/'rejected-shapes.json').write_text(json.dumps(rejects,indent=2)+'\n')
preview=Image.new('RGB',(1920,((len(records)+5)//6)*280),'#dddde0');draw=ImageDraw.Draw(preview)
for i,c in enumerate(records):
 x=i%6*320;y=i//6*280;draw.text((x+4,y+3),c['name'],fill='black')
 for j,im in enumerate([Image.open(P/'originaler'/(c['name']+'.png')),Image.open(O/c['file'])]):
  im=im.convert('RGBA');im=im.crop(im.getbbox());im=im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST) if j==0 else im;im.thumbnail((150,240));preview.paste(im,(x+j*160+(150-im.width)//2,y+30+(240-im.height)//2),im)
preview.save(P/'preview.png');print('Accepted',len(records),'Rejected',[(r['cel'],round(r['axis_deviation'],3),round(r['alpha_iou'],3)) for r in rejects])
