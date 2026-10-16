from PIL import Image
from pathlib import Path
import cv2,numpy as np
p=Path('grafikk/rapporter/spillfeil-r18-20261016/referanser/tom-4.png');im=cv2.imread(str(p));im=cv2.resize(im,None,fx=.5,fy=.5);orb=cv2.ORB_create(6000);kp,des=orb.detectAndCompute(im,None);rows=[]
for f in Path('hd-integrert/rooms').glob('room[0-9][0-9][0-9].png'):
 b=cv2.imread(str(f));k,d=orb.detectAndCompute(b,None)
 if d is None:continue
 matches=cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(des,d,k=2);good=[m for m,n in matches if m.distance<n.distance*.7]
 if len(good)<8:continue
 src=np.float32([kp[m.queryIdx].pt for m in good]);dst=np.float32([k[m.trainIdx].pt for m in good]);h,mask=cv2.findHomography(src,dst,cv2.RANSAC,4);rows.append((int(mask.sum()) if mask is not None else 0,f.name,h.tolist() if h is not None else None))
for r in sorted(rows,reverse=True)[:5]:print(r)
