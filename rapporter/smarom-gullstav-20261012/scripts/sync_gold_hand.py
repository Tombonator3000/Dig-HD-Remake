exec((__import__('pathlib').Path(__file__).resolve().parent/'import_gold.py').read_text().split('records=[]')[0])
# Shared hand/rod artwork prevents hard native object masks from revealing another version at the finger edges.
orig=Image.open(Q/'gold-before/rooms/room050.png').convert('RGBA');arr=np.zeros((800,1280),np.uint8);arr[352:,:640]=255;blend=Image.fromarray(arr).filter(ImageFilter.GaussianBlur(12));out=Image.composite(new.convert('RGBA'),orig,blend);out.save(M/'rooms/room050.png')
for s in ['01','02','03']:
 old=Image.open(Q/f'gold-before/objects/obj884_{s}.png').convert('RGBA');cut=out.crop((0,352,640,800));cut.putalpha(old.getchannel('A'));cut.save(M/f'objects/obj884_{s}.png')
p=R/'GULLSTAV-IMPORT.json';d=json.loads(p.read_text());d['shared_hand_and_rod']='One generated hand/rod crop in room and all three object states, to prevent native masking seams. Original object alpha retained. Gold base palette from native palette3; no game palette change.'
for a in d['records']:a['sha256']=hashlib.sha256((M/a['file']).read_bytes()).hexdigest();a['mask_native_indices']='shared hand/rod crop, feather12px outside object rectangle'
p.write_text(json.dumps(d,indent=2)+'\n')
