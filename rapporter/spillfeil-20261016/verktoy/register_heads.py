"""Register approved-model head atlases and neck anchors in a separate candidate.

Original indices, actor positions, animation commands and timing are unchanged.
"""
from pathlib import Path
import json,hashlib,os,shutil
import numpy as np
from PIL import Image
R=Path(os.environ.get("DIGHD_WORKSPACE",Path.cwd()));M=R/'kandidat-mod/costumes';BASE=Path('/home/tom/Documents/Codex/2026-10-16-the-dig-hd-remake-sp-rsm/testing/linux-release/AppDir/usr/share/the-dig-hd/mods/gpt/costumes')
P=R/'grafikk/rapporter/spillfeil-20261016';O=P/'mod-overrides/costumes';O.mkdir(parents=True,exist_ok=True)
A=json.loads((R/'testing/anims.json').read_text());records=[]
old=P/'HEAD-REGISTRATION.json'
if old.exists():
 for rec in json.loads(old.read_text()):
  name=rec['file'];tmp=M/(name+'.reset.png');shutil.copy2(BASE/name,tmp);os.replace(tmp,M/name);(O/name).unlink(missing_ok=True)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(im,name):
 im.save(O/name);target=M/name;tmp=target.with_suffix('.new.png');shutil.copy2(O/name,tmp);os.replace(tmp,target)
def mask(im):
 a=np.asarray(im.convert('RGBA'));r,g,b=a[:,:,:3].transpose(2,0,1)
 return (a[:,:,3]>128)&~((r>180)&(b>150)&(g<100))
def bbox(m):
 y,x=np.where(m);return int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)
def normalized(im):
 a=np.asarray(im.convert('RGBA')).copy();a[~mask(im),3]=0;im=Image.fromarray(a);im=im.crop(bbox(mask(im))).resize((32,32),Image.Resampling.BILINEAR)
 a=np.asarray(im).astype(float)/255;return a[:,:,:3]*a[:,:,3,None]
def variant(im,cid):
 if cid not in [16,17]:return im
 a=np.asarray(im).copy();rr,gg,bb=a[:,:,:3].astype(float).transpose(2,0,1)
 skin=(rr>gg*1.12)&(gg>bb*1.02)&((rr-gg)>(gg-bb)*1.05)&(a[:,:,3]>0);lum=.299*rr+.587*gg+.114*bb
 a[skin,0]=np.clip(lum[skin]*1.04,0,255);a[skin,1]=np.clip(lum[skin]*1.01,0,255);a[skin,2]=np.clip(lum[skin]*.96,0,255)
 return Image.fromarray(a)
for label,main,ids in [('brink',15,[15,16,17,67,73]),('boston',14,[14,59]),('maggie',18,[18,60])]:
 masterfile=P/'produksjon'/(label+'-heads.png')
 if not masterfile.exists():continue
 master=Image.open(masterfile).convert('RGBA');tiles={}
 for row in range(3):
  for direction in range(8):
   tile=master.crop((round(direction*master.width/8),round(row*master.height/3),round((direction+1)*master.width/8),round((row+1)*master.height/3)))
   tiles[row,direction]=tile.crop(bbox(np.asarray(tile)[:,:,3]>128))
 stands={}
 for a in A[str(main)]['animasjoner']:
  if a['animasjon']==1 and a['lag']==1:
   c=a['ruter'][-1];f=BASE/f'costume{main:03d}_{c:03d}_idx.png';im=Image.open(f).convert('RGBA');stands[a['retning']]=(c,im,normalized(im))
 for cid in ids:
  uses={}
  for a in A[str(cid)]['animasjoner']:
   for c in a['ruter']:uses.setdefault(c,[]).append(a)
  for f in sorted(BASE.glob(f'costume{cid:03d}_*_idx.png')):
   src=Image.open(f).convert('RGBA');w,h=src.size;c=int(f.stem.split('_')[1])
   # Only independent heads. Full-body art and action crops are retained.
   if w>27 or h>23 or w<6 or h<6:continue
   if cid in [14,15,16,17,18] and not any(a['lag']==1 for a in uses.get(c,[])):continue
   actual=mask(src)
   if actual.sum()<15:continue
   dirs={a['retning'] for a in uses.get(c,[]) if a['animasjon'] in [1,4,5] and a['lag']==1}
   scores={di:float(((normalized(src)-ref[2])**2).mean()) for di,ref in stands.items()}
   direction=next(iter(dirs)) if len(dirs)==1 else min(scores,key=scores.get)
   standcell,standsrc,_=stands[direction]
   ownstand=[a for a in A[str(cid)]['animasjoner'] if a['animasjon']==1 and a['lag']==1 and a['retning']==direction]
   closed=any(c in a['ruter'] for a in ownstand) if cid in [14,15,16,17,18] else np.array_equal(normalized(src),normalized(standsrc))
   row=0 if closed else 1
   sa=np.asarray(src);dark=((sa[:,:,:3].max(2)<55)&actual)
   if not closed and dark[-max(2,h//3):].sum()>5:row=2
   current=Image.open(BASE/f'costume{cid:03d}_{c:03d}_hd.png').convert('RGBA');pad=((current.width//4-w)//2,(current.height//4-h)//2)
   sb=bbox(actual)
   tw,th=(standsrc.width,standsrc.height) if cid in [14,15,16,17,18] else (sb[2]-sb[0],sb[3]-sb[1])
   tile=tiles[row,direction].resize((tw*4,th*4),Image.Resampling.LANCZOS)
   # Preserve the source attachment at the lower neck, not bbox overlap.
   x=(sb[0]+pad[0])*4;y=(sb[3]+pad[1])*4-th*4
   out=Image.new('RGBA',current.size);out.alpha_composite(tile,(x,y))
   out=variant(out,cid)
   name=f'costume{cid:03d}_{c:03d}_hd.png';save(out,name)
   records.append({'file':name,'kind':'independent_head','direction':direction,'expression':row,'direction_source':'AKCH' if len(dirs)==1 else 'original_head_template','original_template_error':scores[direction],'placement_hd':[x,y,tw*4,th*4],'atlas':masterfile.name,'original_indices_sha256':digest(f)})
 # Embedded heads in the actual walking layer must use the same model as
 # independently animated speech heads. The direction is explicit in AKCH.
 for cid in ids:
  if cid not in [14,15,16,17,18]:continue
  walk={}
  for a in A[str(cid)]['animasjoner']:
   if a['animasjon']==2 and a['lag']==0:
    for c in a['ruter']:walk.setdefault(c,set()).add(a['retning'])
  for c,dirs in sorted(walk.items()):
   if len(dirs)!=1:continue
   direction=next(iter(dirs));stem=f'costume{cid:03d}_{c:03d}'
   src=Image.open(BASE/(stem+'_idx.png')).convert('RGBA');actual=mask(src);h,w=actual.shape
   if h<30 or w<10:continue
   top=actual[:min(8,h)];ys,xs=np.where(top)
   if not len(xs):continue
   stand=stands[direction][1];tw,th=stand.size
   if label=='brink':th=min(th,11)
   left=int(round((xs.min()+xs.max()+1-tw)/2));headheight=th
   out=Image.open(BASE/(stem+'_hd.png')).convert('RGBA');pad=((out.width//4-w)//2,(out.height//4-h)//2)
   # Original head occupies the first 10/11 rows in these walk families.
   # Keep the shoulder/collar rows; overlay a one-pixel neck connection.
   clear=(max(0,(left+pad[0]-3)*4),max(0,(pad[1]-2)*4),min(out.width,(left+pad[0]+tw+3)*4),min(out.height,(pad[1]+headheight)*4))
   out.paste((0,0,0,0),clear)
   tile=variant(tiles[0,direction],cid).resize((tw*4,(th+1)*4),Image.Resampling.LANCZOS)
   out.alpha_composite(tile,((left+pad[0])*4,pad[1]*4));save(out,stem+'_hd.png')
   records.append({'file':stem+'_hd.png','kind':'embedded_walk_head','direction':direction,'direction_source':'AKCH walk layer','head_region_source':[left,0,tw,th],'atlas':masterfile.name,'original_indices_sha256':digest(BASE/(stem+'_idx.png'))})
 # Register headless standing bodies by neck contact, preserving the feet.
 bodyids={a['ruter'][-1] for a in A[str(main)]['animasjoner'] if a['animasjon']==1 and a['lag']==0}
 bodygroups=[(main,bodyids)]
 if label=='boston':bodygroups.append((59,{5}))
 for cid,cells in bodygroups:
  for c in sorted(cells):
   stem=f'costume{cid:03d}_{c:03d}';src=Image.open(BASE/(stem+'_idx.png')).convert('RGBA');art=Image.open(BASE/(stem+'_hd.png')).convert('RGBA');pad=((art.width//4-src.width)//2,(art.height//4-src.height)//2)
   def neck(im,scale):
    ar=np.asarray(im).astype(float);rr,gg,bb=ar[:,:,:3].transpose(2,0,1)
    skin=(rr>70)&(gg>rr*.57)&(bb>rr*.32)&(rr>gg*1.04)&(ar[:,:,3]>128)
    skin[int(im.height*.3):]=False;y,x=np.where(skin)
    if not len(y):return None
    top=y.min();xs=x[y<=top+2*scale]
    return float(xs.mean()),float(top)
   sn=neck(src,1);an=neck(art,4)
   if sn is None or an is None:continue
   dx=(sn[0]+pad[0])*4-an[0];dy=(sn[1]+pad[1])*4-an[1]
   if abs(dx)>32 or abs(dy)>20:continue
   out=Image.new('RGBA',art.size);waist=(pad[1]+src.height*.45)*4
   # Row shifts are a registration warp, with fixed lower-body/foot anchor.
   # At four pixels per source pixel the per-row shift stays subpixel.
   arr=np.asarray(art).astype(float);arr[:,:,:3]*=arr[:,:,3,None]/255;dest=np.zeros_like(arr)
   for yy in range(art.height):
    weight=max(0,1-yy/waist);sy=yy-dy*weight;y0=int(np.floor(sy));fy=sy-y0
    if y0<0 or y0+1>=art.height:continue
    xs=np.arange(art.width)-dx*weight;x0=np.floor(xs).astype(int);fx=xs-x0;valid=(x0>=0)&(x0+1<art.width)
    row0=arr[y0];row1=arr[y0+1]
    q0=row0[x0[valid]]*(1-fx[valid,None])+row0[x0[valid]+1]*fx[valid,None]
    q1=row1[x0[valid]]*(1-fx[valid,None])+row1[x0[valid]+1]*fx[valid,None]
    dest[yy,valid]=q0*(1-fy)+q1*fy
   alpha=dest[:,:,3];good=alpha>0;dest[good,:3]*=255/alpha[good,None]
   out=Image.fromarray(np.clip(dest,0,255).astype('uint8'));save(out,stem+'_hd.png')
   records.append({'file':stem+'_hd.png','kind':'neck_registration','shift_hd':[dx,dy],'source_neck':sn,'previous_neck':an,'foot_anchor_unchanged':True,'original_indices_sha256':digest(BASE/(stem+'_idx.png'))})
# Solve independent head contacts from the original AKSQ part coordinates and
# the registered body's collar. Apply one fixed offset per standing direction
# to the entire head family, including speech, rather than maximising overlap.
geom=json.loads((R/'testing/geometry.json').read_text())
for cid in [14,15,16,17,18]:
 commands={}
 for step in geom[str(cid)]:
  if len(step['parts'])==1:
   part=step['parts'][0];commands.setdefault(part['cel'],part)
 body={a['retning']:a['ruter'][-1] for a in A[str(cid)]['animasjoner'] if a['animasjon']==1 and a['lag']==0}
 head={a['retning']:a['ruter'][-1] for a in A[str(cid)]['animasjoner'] if a['animasjon']==1 and a['lag']==1}
 for direction in range(8):
  if direction not in body or direction not in head:continue
  bc,hc=body[direction],head[direction]
  if bc not in commands or hc not in commands:continue
  bi=Image.open(M/f'costume{cid:03d}_{bc:03d}_idx.png');hi=Image.open(M/f'costume{cid:03d}_{hc:03d}_idx.png')
  ba=Image.open(M/f'costume{cid:03d}_{bc:03d}_hd.png').convert('RGBA');ha=Image.open(M/f'costume{cid:03d}_{hc:03d}_hd.png').convert('RGBA')
  def skin(im):
   ar=np.asarray(im).astype(float);rr,gg,bb=ar[:,:,:3].transpose(2,0,1)
   return (rr>70)&(gg>rr*.57)&(bb>rr*.32)&(rr>gg*1.04)&(ar[:,:,3]>128)
  bm=skin(ba);bm[int(ba.height*.28):]=False;by,bx=np.where(bm);hy,hx=np.where(skin(ha))
  if not len(by) or not len(hy):continue
  btop=by.min();hbottom=hy.max();bneck=bx[by<=btop+8].mean();hneck=hx[hy>=hbottom-3].mean()
  bpad=((ba.width//4-bi.width)//2,(ba.height//4-bi.height)//2);hpad=((ha.width//4-hi.width)//2,(ha.height//4-hi.height)//2)
  bp,hp=commands[bc],commands[hc]
  dx=(bp['x']-bpad[0]-hp['x']+hpad[0])*4+bneck-hneck
  dy=(bp['y']-bpad[1]-hp['y']+hpad[1])*4+btop+2-hbottom
  if (cid,direction)==(15,6):dx,dy=0,4  # This covered collar has no exposed neck skin.
  if (cid,direction)==(18,3):dy+=4  # Alpha-collar contact found by assembled-pose audit
  if abs(dx)>28 or abs(dy)>24:continue
  for rec in records:
   if rec['kind']!='independent_head' or not rec['file'].startswith(f'costume{cid:03d}_') or rec['direction']!=direction:continue
   im=Image.open(O/rec['file']).convert('RGBA')
   padded=Image.new('RGBA',(im.width+64,im.height+64));padded.alpha_composite(im,(32,32))
   out=padded.transform(padded.size,Image.Transform.AFFINE,(1,0,-dx,0,1,-dy),resample=Image.Resampling.BICUBIC)
   save(out,rec['file']);rec['neck_contact_shift_hd']=[dx,dy];rec['neck_contact_source']='AKSQ standing body/head positions and HD collar'
(P/'HEAD-REGISTRATION.json').write_text(json.dumps(records,indent=2,default=lambda x:x.item()));print(len(records),'registered assets')
