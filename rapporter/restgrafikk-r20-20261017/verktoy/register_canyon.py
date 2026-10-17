"""Native whole-composite placement. Never separate or scale a human head."""
from pathlib import Path
import os,sys,json,hashlib,shutil
import numpy as np
from PIL import Image,ImageDraw
R=Path(os.environ.get('DIGHD_WORKSPACE',Path(__file__).resolve().parents[4]));P=R/'grafikk/rapporter/restgrafikk-r20-20261017';sys.path.insert(0,str(R/'kode/pipeline'))
from dighd import myk
plans=json.loads((P/'canyon-plans.json').read_text());O=P/'mod-tillegg/costumes';B=R/'hd-leveranse/costumes';records=[];exports=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for batch in plans['batches']:
    master=P/(batch['stem']+'-master.png')
    if not master.exists():print('WAITING',master.name);continue
    a=np.array(Image.open(master).convert('RGBA'));hh,ww=a.shape[:2]
    for c in batch['cells']:
        selected=master;native_sheet=a;h,w=hh,ww;slot=c['slot']
        # The first two-slot repair crossed tile boundaries and is not used.
        # Seven pose repairs are generated individually with no atlas tiling.
        repair=P/(f'canyon034-{c["cel"]}-single-master.png')
        single=c['cel'] in [100,102,103,104,105,107,118] and repair.exists()
        if single:
            selected=repair;slot=0;tile=np.array(Image.open(repair).convert('RGBA'))
        else:
            tile=native_sheet[round(slot//4*h/2):round((slot//4+1)*h/2),round(slot%4*w/4):round((slot%4+1)*w/4)].copy()
        owner,_,parts=myk.parts(tile[:,:,3]);keep=np.isin(owner,[v['nr'] for v in parts if v['areal']>=8]);tile[~keep]=0
        yy,xx=np.where(tile[:,:,3]>128);bb=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)];native=tile[bb[1]:bb[3],bb[0]:bb[2]]
        x,y,r,b=c['source_bbox'];sw,sh=r-x,b-y;aspect_error=abs((native.shape[1]/native.shape[0])/(sw/sh)-1)
        # Compare each axis against a single balanced scale, as fit_scales in
        # the existing importer does. Aspect error is a ratio of TWO axes and
        # is not itself either axis' deviation from the common scale.
        sx=sw*4/native.shape[1];sy=sh*4/native.shape[0];common=(sx*sy)**.5
        axis_deviation=max(abs(sx/common-1),abs(sy/common-1))
        assert axis_deviation<=.12,(c['name'],'whole-composite axis drift',axis_deviation)
        fit=myk._premul_resize(native,(sw*4,sh*4));ow,oh=c['source_size'];out=Image.new('RGBA',((ow+8)*4,(oh+8)*4));out.alpha_composite(Image.fromarray(fit),((x+4)*4,(y+4)*4))
        name=c['name'];hd=O/(name+'_hd.png');assert not (B/hd.name).exists();assert not (B/(name+'.png')).exists()
        index=P/'originaler'/(name+'_idx.png');source=R/'testing/source/costumes'/index.name
        assert np.array_equal(np.array(Image.open(source)),np.array(Image.open(index)))
        if (B/index.name).exists():assert np.array_equal(np.array(Image.open(B/index.name)),np.array(Image.open(index)))
        source_alpha=np.array(Image.open(P/'originaler'/(name+'.png')))[:,:,3]>128
        source_alpha=np.repeat(np.repeat(source_alpha[y:b,x:r],4,axis=0),4,axis=1)
        alpha=fit[:,:,3]>128;iou=float((source_alpha&alpha).sum()/max(1,(source_alpha|alpha).sum()))
        assert iou>=.6,(c['name'],'composition overlap',iou)
        exports.append((out,hd,index))
        records.append(dict(file=hd.name,source=index.name,source_index_values_unchanged=True,source_bbox=c['source_bbox'],master=selected.name,master_sha256=sha(selected),slot=slot,native_grid=[1,1] if single else [4,2],native_tile_bbox=bb,aspect_error=aspect_error,axis_deviation_from_common_scale=axis_deviation,alpha_iou=iou,method='one independent native drawing per physical cel; composite and its native alpha fitted as one unit, no separately transformed head',approved_references={n:sha(R/'grafikk/hovedark'/(n+'.png')) for n in ['boston','maggie','brink']},independently_painted=True))
assert len(exports)==25,'no partial human delivery'
for out,hd,index in exports:
    out.save(hd)
    if not (B/index.name).exists():shutil.copy2(index,O/index.name)
for record in records:record['sha256']=sha(O/record['file'])
(P/'canyon-registration.json').write_text(json.dumps(records,indent=2)+'\n')
manifest={str(f.relative_to(P/'mod-tillegg')):sha(f) for f in sorted((P/'mod-tillegg').rglob('*')) if f.is_file()};(P/'ADDITIONS.json').write_text(json.dumps(manifest,indent=2)+'\n')
preview=Image.new('RGB',(1600,2000),'#424650');draw=ImageDraw.Draw(preview)
for i,r in enumerate(records):
    x=i%4*400;y=i//4*280;old=Image.open(P/'originaler'/r['source']).convert('RGBA');old=old.resize((old.width*4,old.height*4),Image.Resampling.NEAREST);new=Image.open(O/r['file']).convert('RGBA')
    for j,im in enumerate([old,new]):
        im=im.crop(im.getbbox());im.thumbnail((190,235));preview.paste(im,(x+j*200+(190-im.width)//2,y+30+(235-im.height)//2),im)
    draw.text((x+5,y+5),r['file'],fill='white')
preview.save(P/'canyon-preview.png')
print('Registered',len(records),'whole cast cels; min IoU',min([r['alpha_iou'] for r in records],default=0))
