"""Keep the rear HD moon visible through the front moon's source restore area."""
from pathlib import Path
from PIL import Image
import shutil,os,json
P=Path('grafikk/rapporter/spillfeil-r18-20261016');O=P/'mod-overrides/costumes';M=Path('kandidat-r18/costumes');back=Image.open(O/'costume148_000_hd.png').convert('RGBA');front=Image.open(O/'costume149_000_hd.png').convert('RGBA');out=Image.new('RGBA',front.size);out.alpha_composite(back,(-24,-28));out.alpha_composite(front,(0,0));name='costume149_000_hd.png';out.save(O/name);tmp=M/(name+'.new');shutil.copy2(O/name,tmp);os.replace(tmp,M/name);(P/'MOON-OVERLAP.json').write_text(json.dumps({'rear_source_position':[185,42],'front_source_position':[191,49],'rear_offset_in_front_hd':[-24,-28],'reason':'original front cel restores some background pixels inside rear moon; reuse same rear HD texture in that area instead of leaving original crescents visible'},indent=2))
