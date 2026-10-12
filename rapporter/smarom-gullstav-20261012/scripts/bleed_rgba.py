from PIL import Image,ImageFilter
import numpy as np
def bleed(im,erode=0):
 a=np.array(im);good=(np.array(im.getchannel("A").filter(ImageFilter.MinFilter(2*erode+1)))>240);sat=(a[:,:,0]>180)&(a[:,:,1]<65)&(a[:,:,2]>140);good&=~sat
 # Expand reliable opaque RGB into the transparent margin before native masking/resizing.
 rgb=a[:,:,:3].copy();h,w=good.shape
 for _ in range(200):
  total=np.zeros((h,w,3),np.float32);count=np.zeros((h,w),np.float32)
  for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
   gy=np.roll(good,(dy,dx),(0,1));rr=np.roll(rgb,(dy,dx),(0,1));
   if dy==-1:gy[-1,:]=False
   if dy==1:gy[0,:]=False
   if dx==-1:gy[:,-1]=False
   if dx==1:gy[:,0]=False
   total+=rr*gy[:,:,None];count+=gy
  fill=~good&(count>0)
  if not fill.any():break
  rgb[fill]=np.rint(total[fill]/count[fill,None]).astype(np.uint8);good[fill]=True
 a[:,:,:3]=rgb;return Image.fromarray(a)
