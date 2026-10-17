import os
"""Register each native Brink pose as one body/head/shovel unit, with its scripted room palette."""
from pathlib import Path
import sys,json,os,shutil,hashlib
import numpy as np
from PIL import Image,ImageDraw
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));sys.path.insert(0,str(R/'kode/pipeline'));from dighd import myk
P=R/'grafikk/rapporter/restgrafikk-r19-20261016';S=R/'testing/source/costumes';B=R/'hd-leveranse/costumes';O=P/'mod-tillegg/costumes';C=R/'kandidat-r19/costumes';plan=json.loads((P/'brink46-plan.json').read_text());records=[]
for batch in plan['batches']:
 master=P/f'brink46-{batch["batch"]:02d}-master.png';native=np.array(Image.open(master).convert('RGBA'));H,W=native.shape[:2]
 for c in batch['cells']:
  slot=c['slot'];tile=native[round(slot//4*H/2):round((slot//4+1)*H/2),round(slot%4*W/4):round((slot%4+1)*W/4)].copy();owner,labels,parts=myk.parts(tile[:,:,3]);keep=np.isin(owner,[p['nr'] for p in parts if p['areal']>=8]);tile[~keep]=0;yy,xx=np.where(tile[:,:,3]>128);bb=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)];art=tile[bb[1]:bb[3],bb[0]:bb[2]]
  idx=Image.open(S/c['file']);original=np.array(idx).copy();idx.putpalette(plan['source_palette']);assert np.array_equal(np.array(idx),original);ow,oh=idx.size;x,y,right,bottom=c['bbox'];fit=myk._premul_resize(art,((right-x)*4,(bottom-y)*4));out=Image.new('RGBA',((ow+8)*4,(oh+8)*4));out.alpha_composite(Image.fromarray(fit),((x+4)*4,(y+4)*4));hd=c['file'].replace('_idx','_hd');assert not (B/hd).exists();out.save(O/hd);idx.save(O/c['file'])
  for name in [hd,c['file']]:
   assert not (B/name).exists();temp=C/(name+'.new');shutil.copy2(O/name,temp);os.replace(temp,C/name)
  records.append(dict(file=hd,source=c['file'],master=str(master.relative_to(R)),master_sha256=hashlib.sha256(master.read_bytes()).hexdigest(),slot=slot,native_bbox=bb,source_bbox=c['bbox'],palette='costume46 AKPL through room15 palette0; index values unchanged',method='one native drawing per physical pose; whole head/body/shovel fitted together, native alpha retained; no separately transformed head',approved_reference='hovedark/brink.png',sha256=hashlib.sha256((O/hd).read_bytes()).hexdigest()))
(P/'brink46-registration.json').write_text(json.dumps(records,indent=2)+'\n');print(len(records),'whole Brink shovel poses registered')
preview=Image.new('RGB',(1600,1200),'#353840');draw=ImageDraw.Draw(preview)
for j,r in enumerate(records):
 im=Image.open(O/r['file']).convert('RGBA');im=im.crop(im.getbbox());im.thumbnail((285,350));x=j%5*320;y=j//5*400;preview.paste(im,(x+(320-im.width)//2,y+30),im);draw.text((x+5,y+5),r['file'],fill='white')
preview.save(P/'brink46-preview.png')
