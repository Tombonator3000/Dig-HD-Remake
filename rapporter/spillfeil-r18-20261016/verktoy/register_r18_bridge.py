from pathlib import Path
from PIL import Image,ImageFilter
import numpy as np,cv2,shutil,os,json
P=Path('grafikk/rapporter/spillfeil-r18-20261016');O=P/'mod-overrides/objects';M=Path('kandidat-r18/objects');B=Path('hd-integrert/objects');gen=Path('/home/tom/.codex/generated_images/01a143a5-2c2d-7dc3-9827-943c3e7c6e0e/exec-235a4788-cb70-4626-a126-2876a0b8b387.png');shutil.copy2(gen,P/'produksjon/tram-gangway-master.png');old=Image.open(B/'obj890_01.png').convert('RGBA');new=Image.open(gen).convert('RGBA').resize(old.size,Image.Resampling.LANCZOS);rgb=np.asarray(new).copy();anchor=np.median(np.asarray(old)[0:80,0:160,:3],axis=(0,1))/np.maximum(np.median(rgb[0:80,0:160,:3],axis=(0,1)),1);rgb[:,:,:3]=np.clip(rgb[:,:,:3].astype(float)*anchor,0,255).astype('uint8');new=Image.fromarray(rgb);a=np.asarray(old);blue=(a[:,:,2]>a[:,:,0]*1.2)&(a[:,:,2]>a[:,:,1]*1.05);yy,xx=np.mgrid[:old.height,:old.width];edge=np.minimum.reduce([xx,old.width-1-xx,yy,old.height-1-yy]);mask=(~blue).astype('float32')*np.clip(edge/8,0,1);mask=Image.fromarray((mask*255).astype('uint8')).filter(ImageFilter.GaussianBlur(.7));bridge=Image.composite(new,old,mask)
def save(im,name):
 im.save(O/name);tmp=M/(name+'.new');shutil.copy2(O/name,tmp);os.replace(tmp,M/name)
save(bridge,'obj890_01.png');save(Image.open(B/'obj890_01_idx.png'),'obj890_01_idx.png')
for obj,x in [(554,16),(983,8)]:
 im=Image.open(B/f'obj{obj}_01.png').convert('RGBA');im.paste(bridge,(x*4,104*4));save(im,f'obj{obj}_01.png');save(Image.open(B/f'obj{obj}_01_idx.png'),f'obj{obj}_01_idx.png')
(P/'BRIDGE-REGISTRATION.json').write_text(json.dumps({'room':80,'source_object':890,'source_rect':[696,104,64,32],'shared_station_objects':[554,983],'source_indices_unchanged':True,'blue_tram_pixels_preserved':True,'meaning':'stone boarding gangway from ledge to tram, same source paving/entrance geometry'},indent=2))
