#!/usr/bin/env python3
"""Source-driven light masks with a painted HD filament field.

Original cells determine light positions, phase, palette and timing. Dark
matte/architecture pixels reveal the existing HD room. They are not repainted
as smoke, clothing, rocks or new scenery. Tiny sparks use analytic light cores.
"""
import argparse, shutil
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter


def register(source, field, output, costumes):
    output.mkdir(parents=True,exist_ok=True)
    tex=np.asarray(Image.open(field).convert('RGBA')).astype(float)/255
    total=0
    for costume in costumes:
        for f in sorted(source.glob(f'costume{costume:03d}_*.png')):
            if '_idx' in f.stem:continue
            cel=int(f.stem[-3:]);im=np.asarray(Image.open(f).convert('RGBA')).astype(float)/255
            h,w=im.shape[:2];rgb=im[:,:,:3];live=im[:,:,3]
            peak=rgb.max(2)
            # A field is attached to source coordinates; a modest phase offset
            # supplies coherent light motion without moving the source geometry.
            th,tw=(h+8)*4,(w+8)*4
            yy,xx=np.mgrid[:th,:tw].astype(np.float32)
            shift=cel*.007 if costume==35 else 0
            field_w=max(tw-1,1) if costume==35 else 1024
            field_h=max(th-1,1) if costume==35 else 800
            mx=((xx/field_w+shift)%1*(tex.shape[1]-1)).astype(np.float32)
            my=((yy/field_h+shift*.65)%1*(tex.shape[0]-1)).astype(np.float32)
            detail=cv2.remap(tex.astype(np.float32),mx,my,cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)
            if costume==35:
                strength=live*np.clip((peak-.035)/.68,0,1)
                opacity=.72
            elif costume==61:
                hot=(rgb[:,:,1]>rgb[:,:,0]*.55)&(rgb[:,:,1]>.25)
                hot|=(rgb[:,:,2]>rgb[:,:,0]*1.2)
                if live.sum()<12:hot=live>0
                strength=live*hot*np.clip((peak-.12)/.75,0,1)
                opacity=.95
            else:
                # Remove the source's opaque dark polygon backing. The room
                # already contains the HD lens; only emitted light belongs here.
                emission=rgb[:,:,0]*.25+rgb[:,:,1]*.5+rgb[:,:,2]*.25
                strength=live*np.clip((emission-.35)/.55,0,1)**1.2
                opacity=.9
            padded=np.pad(strength,4)
            high=cv2.resize(padded,(tw,th),interpolation=cv2.INTER_CUBIC)
            high=np.clip(gaussian_filter(high,.85),0,1)
            glow=gaussian_filter(high,4.5)
            alpha=np.clip((high*(.5+.5*detail[:,:,3])+glow*.28)*opacity,0,1)
            if costume==35:
                colour=detail[:,:,:3]
            else:
                # Match original yellow/white sparks or cyan/blue lens energy.
                sr=cv2.resize(np.pad(rgb,((4,4),(4,4),(0,0))),(tw,th),interpolation=cv2.INTER_CUBIC)
                den=np.maximum(sr.max(2,keepdims=True),.01)
                tint=np.clip(sr/den,0,1)
                colour=np.clip(tint*.75+detail[:,:,:3]*.25,0,1)
            # Highlight the original luminous cores, without opaque grey fill.
            colour=np.clip(colour+(high[:,:,None]**3)*.22,0,1)
            if w<=3 and h<=3:
                # Subpixel source sparks become small, smooth light points.
                cx=(tw-1)/2;cy=(th-1)/2
                rad=((xx-cx)/max(2,w*2))**2+((yy-cy)/max(2,h*2))**2
                alpha=np.exp(-rad*1.8)*float(strength.max())
            out=np.dstack((colour,alpha))
            Image.fromarray(np.rint(np.clip(out,0,1)*255).astype(np.uint8)).save(output/(f.stem+'_hd.png'))
            shutil.copy2(source/(f.stem+'_idx.png'),output/(f.stem+'_idx.png'))
            total+=1
    print(f'{total} source-controlled HD light cells')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('field',type=Path);p.add_argument('output',type=Path);p.add_argument('costumes',nargs='+',type=int)
    a=p.parse_args();register(a.source,a.field,a.output,a.costumes)
