#!/usr/bin/env python3
"""Register painted crystal atlases to all original puzzle forms.

Orange source pixels are the old background matte, never a stone frame.
The game retains its original state selection, silhouette and animation.
"""
import argparse, json, shutil
from pathlib import Path
import cv2
import numpy as np
from PIL import Image


def core(file):
    im=np.asarray(Image.open(file).convert('RGBA')).copy()
    r,g,b=im[:,:,:3].astype(float).transpose(2,0,1)
    matte=(r>65)&(g>30)&(g>r*.25)&(b<r*.55)
    mask=((im[:,:,3]>0)&~matte).astype(np.uint8)
    cc,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    hull=cv2.convexHull(max(cc,key=cv2.contourArea))
    mask[:]=0;cv2.fillConvexPoly(mask,hull,255)
    x,y,w,h=cv2.boundingRect(hull);im[:,:,3]=mask
    return im,(x,y,w,h),im[y:y+h,x:x+w]


def register(source, atlases, output, receipt):
    output.mkdir(parents=True,exist_ok=True)
    paintings=[Image.open(p).convert('RGBA') for p in atlases]
    refs=[];painted=[]
    for i in range(90):
        im,box,crop=core(source/f'costume286_{i:03d}.png')
        refs.append(cv2.resize(crop,(64,64),interpolation=cv2.INTER_AREA).astype(float)/255)
        atlas=paintings[i//30];j=i%30
        cell=atlas.crop((j%5*atlas.width/5,j//5*atlas.height/6,(j%5+1)*atlas.width/5,(j//5+1)*atlas.height/6))
        a=np.asarray(cell)[:,:,3];ys,xs=np.where(a>64)
        if len(xs)<100:raise ValueError(f'Missing painted crystal {i}')
        painted.append(cell.crop((int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1))))
    ref=np.asarray(refs);rows=[]
    for costume in range(286,290):
        for file in sorted(source.glob(f'costume{costume}_*.png')):
            if '_idx' in file.stem:continue
            im,(x,y,w,h),crop=core(file)
            q=cv2.resize(crop,(64,64),interpolation=cv2.INTER_AREA).astype(float)/255
            # Colour/facets and silhouette jointly select the corresponding
            # original geometry, including mixed-colour transition frames.
            delta=((ref[:,:,:,:3]-q[:,:,:3])**2).mean((1,2,3))
            delta+=((ref[:,:,:,3]-q[:,:,3])**2).mean((1,2))*.5
            k=int(np.argmin(delta))
            if costume==286:k=int(file.stem[-3:])
            art=np.asarray(painted[k].resize((w*4,h*4),Image.Resampling.LANCZOS)).copy()
            # Preserve the original dark crystal values across separately
            # generated atlases instead of allowing brightness to jump.
            valid=crop[:,:,3]>128
            original=crop[:,:,:3][valid].astype(float).mean(0)
            painted_mean=art[:,:,:3][art[:,:,3]>128].astype(float).mean(0)
            factor=np.clip(original.max()/max(painted_mean.max(),1),.45,1.3)
            art[:,:,:3]=np.clip(art[:,:,:3].astype(float)*factor,0,255).astype(np.uint8)
            H,W=im.shape[:2];out=Image.new('RGBA',((W+4)*4,(H+4)*4))
            out.alpha_composite(Image.fromarray(art),((x+2)*4,(y+2)*4))
            out.save(output/(file.stem+'_hd.png'))
            shutil.copy2(source/(file.stem+'_idx.png'),output/(file.stem+'_idx.png'))
            rows.append({'sprite':file.stem,'painted_reference':k,'source_match_mse':round(float(delta[k]),6)})
    receipt.write_text(json.dumps(rows,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('output',type=Path);p.add_argument('receipt',type=Path);p.add_argument('atlases',nargs=3,type=Path)
    a=p.parse_args();register(a.source,a.atlases,a.output,a.receipt)
