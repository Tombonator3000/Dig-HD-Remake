import os
from pathlib import Path
import json,sys,shutil,hashlib
import numpy as np,cv2
from PIL import Image,ImageDraw
from scipy.optimize import linear_sum_assignment
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]))
sys.path.insert(0,str(R/'kode/pipeline'))
from dighd import myk
G=R/'grafikk';P=G/'rapporter/restgrafikk-r19-20261016';S=R/'testing/source';O=P/'mod-tillegg';O.mkdir(parents=True,exist_ok=True)
maps={};deliveries=[];receipts={}
for job,native in [('fig008_02','resultat-r19-v2.png'),('fig008_03','resultat-r19.png'),('fig008_04','resultat-r19.png')]:
    meta=json.loads((G/'jobber'/job/'jobb.json').read_text());path=G/'jobber'/job/native;im=np.asarray(Image.open(path).convert('RGBA'))
    n,labels,stats,centers=cv2.connectedComponentsWithStats((im[:,:,3]>=128).astype('uint8'),8)
    components=[i for i in range(1,n) if stats[i,4]>500]
    large=[]
    for c in meta['ruter']:
        src=np.asarray(Image.open(S/'costumes'/(c['bilde']+'.png')).convert('RGBA'))
        if myk.measure_mask(src)[0].sum()>=40:large.append(c)
    assert len(large)==len(components),(job,len(large),len(components))
    expected=np.array([[64+(c['rekt'][0]+c['rekt'][2]/2)*4,32+(c['rekt'][1]+c['rekt'][3]/2)*4] for c in large])
    costs=((expected[:,None,:]-centers[components][None,:,:])**2).sum(2)
    ri,ci=linear_sum_assignment(costs);boxes={}
    for a,b in zip(ri,ci):
        x,y,w,h=map(int,stats[components[b],:4]);boxes[large[a]['bilde']]=[x,y,w,h]
    maps[job]={'koblinger':[{'bilde':k,'native_analyseboks_alfa128':v} for k,v in boxes.items()]}
    receipt=myk.import_sheet(im,meta['ruter'],boxes,S,O)
    receipts[job]=receipt
    deliveries.append(dict(jobb=job,resultat=str(path.relative_to(G)),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),ruter=len(large),status='levert',rutekart=str((P/'rutekart.json').relative_to(G)),game_tested=False,visually_approved_by_tom=False))
    for v in receipt['ruter'].values():
        if v.get('fil'):v['_sti']=str(O/v['fil'])
    myk.preview(receipt,S,P,job)
    print(job,{s:sum(c.get('status')==s for c in receipt['ruter'].values()) for s in ['ok','sjekk','mangler','teknisk']},flush=True)
# Earlier native deliveries: only currently absent cells, never replace r18.
for folder in ['restgrafikk-20261015','zz-ovrige-66-20261015']:
    data=json.loads((G/'rapporter'/folder/'fremdrift.json').read_text())
    for d in data['leveranser']:
        job=d['jobb'];meta=json.loads((G/'jobber'/job/'jobb.json').read_text());cells=[c for c in meta['ruter'] if not (R/'hd-leveranse/costumes'/(c['bilde']+'_hd.png')).exists() and not (R/'hd-leveranse/costumes'/(c['bilde']+'.png')).exists()]
        if not cells:continue
        path=G/d['resultat'];assert hashlib.sha256(path.read_bytes()).hexdigest()==d['sha256']
        boxes=myk.load_map(G/d['rutekart'],job)
        receipt=myk.import_sheet(np.asarray(Image.open(path).convert('RGBA')),cells,boxes,S,O);receipts[job]=receipt
        for v in receipt['ruter'].values():
            if v.get('fil'):v['_sti']=str(O/v['fil'])
        myk.preview(receipt,S,P,job)
        print(job,{s:sum(c.get('status')==s for c in receipt['ruter'].values()) for s in ['ok','sjekk','mangler','teknisk']},flush=True)
(P/'rutekart.json').write_text(json.dumps(maps,indent=2)+'\n')
(P/'fremdrift.json').write_text(json.dumps({'leveranser':deliveries},indent=2)+'\n')
(P/'mottak.json').write_text(json.dumps(receipts,indent=2)+'\n')
