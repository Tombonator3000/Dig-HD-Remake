"""Register painted doorway anchors onto original physical phase geometry.

Uses the r19 effect/phase registration method. Exports art-only additions;
published r19 is immutable. Phase reuse is explicitly recorded, not counted
as independently painted images.
"""
from pathlib import Path
import os, sys, json, hashlib, shutil
import numpy as np
import cv2
from PIL import Image, ImageDraw
from scipy.ndimage import distance_transform_edt, gaussian_filter

R=Path(os.environ.get('DIGHD_WORKSPACE',Path(__file__).resolve().parents[4]))
P=R/'grafikk/rapporter/restgrafikk-r20-20261017'
sys.path.insert(0,str(R/'kode/pipeline'))
from dighd import myk
plans=json.loads((P/'plans.json').read_text())
B=R/'hd-leveranse/costumes'
O=P/'mod-tillegg/costumes';O.mkdir(parents=True,exist_ok=True)
masters={62:['nexus062-01'],63:['nexus063-01-traced','nexus063-03-solid'],64:['nexus064-01-traced'],65:['nexus065-01-traced','nexus065-04-solid'],66:['nexus066-01-traced','nexus066-02-solid']}
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def crop_source(c):
    im=np.array(Image.open(P/'originaler'/(c['name']+'.png')).convert('RGBA'))
    x,y,r,b=c['source_bbox'];return im[y:b,x:r].copy()
def feature(a):
    return cv2.resize(a,(96,96),interpolation=cv2.INTER_AREA).astype('float32')/255
def extend_rgb(a):
    good=a[:,:,3]>96
    assert good.any()
    _,near=distance_transform_edt(~good,return_indices=True)
    return a[near[0],near[1],:3].astype('float32')
def coverage(mask):
    # One-pixel transparency dithering inside a stone surface is not a hole
    # in the door. Keep real hollow polygons, remove only enclosed areas < 8 px.
    count, labels, stats, _=cv2.connectedComponentsWithStats((~mask).astype('uint8'),8)
    clean=mask.astype('uint8').copy()
    for k in range(1,count):
        x,y,w,h,area=stats[k]
        if area<8 and x>0 and y>0 and x+w<mask.shape[1] and y+h<mask.shape[0]:
            clean[labels==k]=1
    h,w=clean.shape;large=np.zeros((h*16,w*16),'uint8')
    contours,hierarchy=cv2.findContours(clean,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    if hierarchy is None:return np.zeros((h*4,w*4),'uint8')
    for k,c in enumerate(contours):
        depth=0;parent=int(hierarchy[0,k,3])
        while parent>=0:depth+=1;parent=int(hierarchy[0,parent,3])
        # Subpixel polygon simplification straightens pixel stair-steps;
        # displacement stays below the project's 0.75 source-pixel tolerance.
        c=cv2.approxPolyDP(c,.55,True)
        points=np.rint((c[:,0,:].astype('float32')+.5)*16).astype('int32')
        cv2.drawContours(large,[points[:,None,:]],-1,255 if depth%2==0 else 0,cv2.FILLED)
    large=cv2.dilate(large,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15)))
    return cv2.resize(large,(w*4,h*4),interpolation=cv2.INTER_AREA)
records=[];maps=[]
for cid, stems in masters.items():
    anchors=[]
    for stem in stems:
        source_stem=stem.replace('-traced','').replace('-solid','')
        plan=next(b for b in plans['batches'] if b['stem']==source_stem)
        master=P/(stem+'-master.png')
        if not master.exists():
            print('WAITING',master.name,flush=True);continue
        native=np.array(Image.open(master).convert('RGBA'));hh,ww=native.shape[:2]
        for c in plan['cells']:
            slot=c['slot'];tile=native[round(slot//4*hh/3):round((slot//4+1)*hh/3),round(slot%4*ww/4):round((slot%4+1)*ww/4)].copy()
            owner,_,parts=myk.parts(tile[:,:,3]);keep=np.isin(owner,[v['nr'] for v in parts if v['areal']>=8]);tile[~keep]=0
            yy,xx=np.where(tile[:,:,3]>96)
            if not len(xx):
                print('EMPTY',stem,slot,flush=True);continue
            bb=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]
            art=tile[bb[1]:bb[3],bb[0]:bb[2]].copy()
            source=crop_source(c);q=feature(source)
            anchors.append(dict(c=c,source=source,feature=q,native=art,master=master,bb=bb))
            maps.append(dict(master=master.name,master_sha256=sha(master),source=c['name'],slot=slot,native_tile_bbox=bb))
    if not anchors:continue
    cells=[c for b in plans['batches'] if b['costume']==cid for c in b['cells']]
    for c in cells:
        name=c['name'];assert not (B/(name+'_hd.png')).exists();assert not (B/(name+'.png')).exists()
        source=crop_source(c);h,w=source.shape[:2];q=feature(source);mask=source[:,:,3]>128
        scores=[]
        for anchor in anchors:
            aq=anchor['feature'];visible=(q[:,:,3]>.5)&(aq[:,:,3]>.5)
            color=float(((q[:,:,:3]-aq[:,:,:3])**2)[visible].mean()) if visible.any() else 1
            shape=float(((q[:,:,3]-aq[:,:,3])**2).mean())
            aspect=abs(np.log((w/h)/(anchor['source'].shape[1]/anchor['source'].shape[0])))
            scores.append(color+shape*2+aspect*.12)
        k=int(np.argmin(scores));anchor=anchors[k]
        fitted=myk._premul_resize(anchor['native'],(w*4,h*4))
        rgb=extend_rgb(fitted)
        # Small original-to-original phase motion, same bounded flow as r19.
        gray=cv2.cvtColor((q[:,:,:3]*255).astype('uint8'),cv2.COLOR_RGB2GRAY)
        refgray=cv2.cvtColor((anchor['feature'][:,:,:3]*255).astype('uint8'),cv2.COLOR_RGB2GRAY)
        flow=cv2.calcOpticalFlowFarneback(gray,refgray,None,.5,3,17,4,7,1.3,0)
        flow=cv2.GaussianBlur(np.clip(flow,-4,4),(0,0),8);flow=np.clip(flow,-1.5,1.5)
        flow=cv2.resize(flow,(w*4,h*4),interpolation=cv2.INTER_CUBIC)
        yy,xx=np.mgrid[:h*4,:w*4].astype('float32')
        rgb=cv2.remap(rgb,xx+flow[:,:,0]*(w*4/96),yy+flow[:,:,1]*(h*4/96),cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
        # Source controls low-frequency light and palette; painting supplies detail.
        ref=extend_rgb(source)
        ref=cv2.resize(ref,(w*4,h*4),interpolation=cv2.INTER_CUBIC)
        ref=np.clip(ref,0,255)
        detail=rgb-gaussian_filter(rgb,(6,6,0))
        limit=8+ref.max(axis=2,keepdims=True)*.1
        detail=np.clip(detail,-limit,limit)
        rgb=np.clip(gaussian_filter(ref,(2,2,0))+detail,0,255).astype('uint8')
        # Smooth original polygon topology, not a hard original pixel mask.
        alpha=coverage(mask)
        art=np.dstack([rgb,alpha])
        ow,oh=c['source_size'];x,y,rr,bb=c['source_bbox']
        out=Image.new('RGBA',((ow+8)*4,(oh+8)*4));out.alpha_composite(Image.fromarray(art),((x+4)*4,(y+4)*4))
        hd=O/(name+'_hd.png');out.save(hd)
        index=P/'originaler'/(name+'_idx.png')
        if not (B/index.name).exists():shutil.copy2(index,O/index.name)
        else:
            assert np.array_equal(np.array(Image.open(B/index.name)),np.array(Image.open(index)))
        original=np.array(Image.open(R/'testing/source/costumes'/index.name))
        assert np.array_equal(np.array(Image.open(index)),original)
        oldmask=cv2.resize(mask.astype('uint8'),(w*4,h*4),interpolation=cv2.INTER_NEAREST)>0
        amask=alpha>=128
        iou=float((amask&oldmask).sum()/max(1,(amask|oldmask).sum()))
        records.append(dict(file=hd.name,sha256=sha(hd),source=name+'_idx.png',source_index_values_unchanged=True,source_bbox=c['source_bbox'],master=anchor['master'].name,master_sha256=sha(anchor['master']),anchor_source=anchor['c']['name'],anchor_score=scores[k],native_slot=anchor['c']['slot'],alpha_iou=iou,method='painted anchor material registered to original phase, bounded flow, source low-frequency palette/light, antialiased original polygon topology at 0.55px tolerance; enclosed transparency dithering under 8px filled',independently_painted=False))
(P/'registration.json').write_text(json.dumps(records,indent=2)+'\n')
(P/'rutekart.json').write_text(json.dumps(maps,indent=2)+'\n')
manifest={str(f.relative_to(P/'mod-tillegg')):sha(f) for f in sorted((P/'mod-tillegg').rglob('*')) if f.is_file()}
(P/'ADDITIONS.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Registered',len(records),'phases; minimum silhouette IoU',min([r['alpha_iou'] for r in records],default=0))
# A source/HD visual comparison; full atlas master files are retained separately.
selected=[]
for cid in masters:
    group=[r for r in records if r['file'].startswith(f'costume{cid:03d}_')]
    if group:selected += [group[0],group[len(group)//3],group[2*len(group)//3],group[-1]]
preview=Image.new('RGB',(1600,1600),'#424650');draw=ImageDraw.Draw(preview)
for i,r in enumerate(selected):
    x=i%4*400;y=i//4*320
    old=Image.open(P/'originaler'/r['source']).convert('RGBA');old=old.resize((old.width*4,old.height*4),Image.Resampling.NEAREST);new=Image.open(O/r['file'])
    for j,im in enumerate([old,new]):
        im=im.crop(im.getbbox());im.thumbnail((180,270));preview.paste(im,(x+j*200+(180-im.width)//2,y+30+(270-im.height)//2),im)
    draw.text((x+5,y+5),r['file'],fill='white')
preview.save(P/'preview.png')
