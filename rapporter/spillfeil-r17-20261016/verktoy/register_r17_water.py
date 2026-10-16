#!/usr/bin/env python3
"""Register an HD sea painting to the game's original 24 wave phases.

The original shoreline and foam masks control the wave. A shared water field
uses room coordinates so adjacent cells and successive phases cannot acquire
stretched boundary colours or opaque rectangular mattes.
"""
import argparse
from pathlib import Path
import shutil
import cv2
import numpy as np
from scipy.ndimage import distance_transform_edt, gaussian_filter
from PIL import Image


def register(source, painting, output, scale=4, pad=2):
    output.mkdir(parents=True, exist_ok=True)
    tex=np.asarray(Image.open(painting).convert('RGBA'))
    # Sample an interior patch of actual painted sea. Shore foam is attached
    # to the current source phase, rather than dragged from the first phase.
    hh,ww=tex.shape[:2]
    body=cv2.resize(tex[:,:,:3],(166*scale,200*scale),interpolation=cv2.INTER_AREA)
    for file in sorted(source.glob('costume301_*.png')):
        if '_idx' in file.stem:continue
        frame=np.asarray(Image.open(file).convert('RGBA'))
        h,w=frame.shape[:2];cel=int(file.stem[-3:]);phase=cel/24*2*np.pi
        yy,xx=np.mgrid[:h*scale,:w*scale].astype(np.float32)
        # Right/bottom alignment matches the original AKOS wave placement.
        mx=(xx+(166-w)*scale+np.sin(phase)*4).astype(np.float32)
        my=(yy+(200-h)*scale+np.cos(phase)*3).astype(np.float32)
        texture=cv2.remap(body,mx,my,cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT_101).astype(float)
        colour=frame[:,:,:3].astype(float)
        mask=frame[:,:,3].astype(float)/255
        land=(colour[:,:,0]>colour[:,:,2]*1.4)&(colour[:,:,0]>65)
        mask[land]=0
        signed=distance_transform_edt(mask>.5)-distance_transform_edt(mask<=.5)
        signed=gaussian_filter(signed,.75)
        alpha=np.clip(cv2.resize(signed,(w*scale,h*scale),interpolation=cv2.INTER_CUBIC)*scale+.5,0,1)
        foam=(colour[:,:,0]>145)&(colour[:,:,1]>175)&(mask>.5)
        foam=cv2.resize(foam.astype(float),(w*scale,h*scale),interpolation=cv2.INTER_CUBIC)
        foam=np.clip(gaussian_filter(foam,1),0,1)
        # The painted ripples give the narrow source foam a fine texture.
        grain=.7+.3*np.clip(texture.mean(2)/100,0,1)
        foam*=grain
        texture=texture*(1-foam[:,:,None])+np.array([222,246,255])*foam[:,:,None]
        out=np.zeros(((h+pad*2)*scale,(w+pad*2)*scale,4),np.uint8)
        q=out[pad*scale:(h+pad)*scale,pad*scale:(w+pad)*scale]
        q[:,:,:3]=np.clip(texture,0,255).astype(np.uint8)
        q[:,:,3]=np.rint(alpha*255).astype(np.uint8)
        Image.fromarray(out).save(output/(file.stem+'_hd.png'))
        shutil.copy2(source/(file.stem+'_idx.png'),output/(file.stem+'_idx.png'))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('painting',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();register(a.source,a.painting,a.output)
