from pathlib import Path
from PIL import Image,ImageDraw
import json
R=Path('.');plans=[]
for name,cid,cels,cols,rows in [('energy175',175,[0]+list(range(3,13))+list(range(15,32)),7,4),('dais35a',35,list(range(200,220)),5,4),('dais35b',35,list(range(220,240)),5,4)]:
 can=Image.new('RGB',(1792 if cols==7 else 1536,1024),(38,39,47));d=ImageDraw.Draw(can);cw=can.width/cols;ch=can.height/rows;cells=[]
 for j,c in enumerate(cels):
  stem=f'costume{cid:03d}_{c:03d}';im=Image.open(R/'context'/(stem+'.png')).convert('RGBA');bbox=im.getbbox();im=im.crop(bbox);scale=min((cw-30)/im.width,(ch-30)/im.height);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST);x=round((j%cols+.5)*cw-im.width/2);y=round((j//cols+.5)*ch-im.height/2);can.paste(im,(x,y),im);d.text((round(j%cols*cw+4),round(j//cols*ch+4)),str(j+1),fill='white');cells.append({'cel':c,'source_bbox':bbox,'reference_xy':[x,y]})
 can.save(name+'-phases-reference.png');plans.append({'name':name,'costume':cid,'cols':cols,'rows':rows,'cells':cells})
Path('energy-phase-plan.json').write_text(json.dumps(plans,indent=2))
