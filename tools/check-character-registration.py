#!/usr/bin/env python3
"""Compose character parts using original AKSQ coordinates and flag detached heads.

Requires private game/mod files. Never changes the game or candidate images.
"""
import argparse,json,struct,sys
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'pipeline'))
from dighd import gamedata as g

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--game',required=True,type=Path);p.add_argument('--mod',required=True,type=Path);p.add_argument('--out',required=True,type=Path);p.add_argument('--costumes',default='14,15,16,17,18,59,60,67,73,103');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 d=(a.game/'DIG.LA1').read_bytes();ix=g.read_index(a.game/'DIG.LA0');rooms=g.read_rooms(a.game/'DIG.LA1');receipt=[]
 for cid in map(int,a.costumes.split(',')):
  rn,ofs=ix.costume_dir[cid];pos=rooms[rn].offset+ofs;bl={t:d[o+8:o+n] for t,o,n in g.children(d,pos+8,pos+g.be32(d,pos+4))};seq=bl[b'AKSQ'];ncel=len(bl[b'AKOF'])//6;steps=[];at=0
  while at<len(seq)-7:
   if seq[at:at+2] not in [b'\xc0\x20',b'\xc0\x25']:at+=1;continue
   q=at+2+(4 if seq[at+1]==0x25 else 0);count=seq[q];q+=1;parts=[]
   try:
    for _ in range(count):
     x,y=struct.unpack_from('<hh',seq,q);q+=4;c=struct.unpack_from('>H',seq,q)[0] if seq[q]&128 else seq[q];q+=2 if seq[q]&128 else 1
     if c&0xc000==0xc000 or c&0xfff>=ncel:raise ValueError()
     parts.append((c&0xfff,x,y))
    if parts:steps.append((at,parts))
    at=q
   except (ValueError,IndexError,struct.error):at+=1
  # Single-part commands on separate animation layers are combined by AKCH.
  anim=g.akos_animations(d,pos,g.be32(d,pos+4))['animasjoner'];single={parts[0][0]:parts[0] for _,parts in steps if len(parts)==1};poses=[]
  for direction in range(8):
   body=[z for z in anim if z['animasjon']==1 and z['lag']==0 and z['retning']==direction];head=[z for z in anim if z['animasjon']==1 and z['lag']==1 and z['retning']==direction]
   if body and head:
    bc,hc=body[-1]['ruter'][-1],head[-1]['ruter'][-1]
    if bc in single and hc in single:poses.append((f'stand-{direction}',[single[bc],single[hc]]))
  # Speech heads can differ from the standing head. Check every source
  # combination on matching animation layers, retaining original positions.
  # These are conservative candidate pairs, not a reconstruction of timing.
  for action in (1,4,5):
   for direction in range(8):
    heads=[z for z in anim if z['animasjon']==action and z['lag']==1 and z['retning']==direction]
    bodies=[z for z in anim if z['animasjon']==action and z['lag']==0 and z['retning']==direction]
    if not bodies:bodies=[z for z in anim if z['animasjon']==1 and z['lag']==0 and z['retning']==direction]
    for body in bodies:
     for head in heads:
      for bc in body['ruter']:
       for hc in head['ruter']:
        if bc in single and hc in single:poses.append((f'layers-{action}-{direction}',[single[bc],single[hc]]))
  poses += [(f'aksq-{off}',parts) for off,parts in steps if len(parts)>1]
  seen=set();panels=[]
  for name,parts in poses:
   key=tuple(parts)
   if key in seen:continue
   seen.add(key);layers=[];originals=[]
   for c,x,y in parts:
    stem=f'costume{cid:03d}_{c:03d}';idx=a.mod/'costumes'/(stem+'_idx.png');hd=a.mod/'costumes'/(stem+'_hd.png')
    if not idx.exists() or not hd.exists():continue
    src=Image.open(idx);art=Image.open(hd).convert('RGBA');px=(art.width//4-src.width)//2;py=(art.height//4-src.height)//2;layers.append((art,(x-px)*4,(y-py)*4,c,src.size))
    rgba=np.asarray(src.convert('RGBA'));valid=(rgba[:,:,3]>128)&~((rgba[:,:,0]>180)&(rgba[:,:,2]>150)&(rgba[:,:,1]<100));original=Image.new('L',art.size);original.paste(Image.fromarray(valid.astype('uint8')*255).resize((src.width*4,src.height*4),Image.Resampling.NEAREST),(px*4,py*4));originals.append(original)
   if not layers:continue
   x0=min(x for im,x,y,c,s in layers);y0=min(y for im,x,y,c,s in layers);x1=max(x+im.width for im,x,y,c,s in layers);y1=max(y+im.height for im,x,y,c,s in layers)
   if max(x1-x0,y1-y0)>2048:continue
   im=Image.new('RGBA',(x1-x0+16,y1-y0+16));masks=[];source_masks=[]
   for (layer,x,y,c,size),original in zip(layers,originals):
    im.alpha_composite(layer,(x-x0+8,y-y0+8));mask=Image.new('L',im.size);mask.paste(layer.getchannel('A'),(x-x0+8,y-y0+8));masks.append(np.asarray(mask)>128);source=Image.new('L',im.size);source.paste(original,(x-x0+8,y-y0+8));source_masks.append(np.asarray(source)>128)
   gap=None;contact=None;source_gap=None
   if name.startswith(('stand-','layers-')) and len(masks)==2:
    h,b=np.where(masks[1]),np.where(masks[0]);headpoints=np.stack(h,1);bodypoints=np.stack(b,1)
    if len(headpoints) and len(bodypoints):
     # Collar/body nearest distance, in HD pixels; no face/style inference.
     import scipy.ndimage as nd
     distance=nd.distance_transform_edt(~masks[0]);gap=float(distance[masks[1]].min())
     if source_masks[0].any() and source_masks[1].any():source_gap=float(nd.distance_transform_edt(~source_masks[0])[source_masks[1]].min())/4
     # One touching pixel is not a sound neck joint after downscaling.
     # Report the width of the contact as well as its nearest distance.
     contact=int(np.count_nonzero(np.any((distance<=2)&masks[1],axis=0)))
   # A cel can occur at several original positions. A conservative layer
   # pair already separated in the source is not evidence of an HD neck gap.
   eligible=source_gap is not None and source_gap<=2
   rec={'costume':cid,'pose':name,'parts':[c for _,_,_,c,_ in layers],'head_body_gap_hd':gap,'contact_width_hd':contact,'source_gap_px':source_gap,'originally_separated_candidate':source_gap is not None and not eligible,'needs_review':gap is not None and eligible and (gap>4 or contact<3),'candidate_layer_pair':name.startswith('layers-')};receipt.append(rec)
   panel=Image.new('RGB',(260,310),'#666677');im.thumbnail((252,280));panel.paste(im,((260-im.width)//2,24),im);ImageDraw.Draw(panel).text((5,4),name+(' GAP' if rec['needs_review'] else ''),fill='white');panels.append(panel)
  for page,start in enumerate(range(0,len(panels),48)):
   chunk=panels[start:start+48];sheet=Image.new('RGB',(260*6,310*((len(chunk)+5)//6)),'#666677')
   for j,im in enumerate(chunk):sheet.paste(im,(j%6*260,j//6*310))
   sheet.save(a.out/f'costume{cid:03d}-parts-{page:02d}.png')
 (a.out/'registration-check.json').write_text(json.dumps(receipt,indent=2));flags=sum(r['needs_review'] for r in receipt);print(f'{len(receipt)} assembled poses; {flags} head/body gaps need review. Identity and style require visual approval.');return 1 if flags else 0
if __name__=='__main__':raise SystemExit(main())
