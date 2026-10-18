from pathlib import Path
import json
from PIL import Image
P=Path(__file__).resolve().parents[1]
for c in json.loads((P/'rejected-shapes.json').read_text()):
 im=Image.open(P/'originaler'/(c['name']+'.png')).convert('RGBA').crop(c['source_bbox']);f=min(1300/im.width,700/im.height);im=im.resize((round(im.width*f),round(im.height*f)),Image.Resampling.NEAREST);out=Image.new('RGBA',(1536,1024));out.alpha_composite(im,((1536-im.width)//2,(1024-im.height)//2));out.save(P/(c['name']+'-single-reference.png'))
