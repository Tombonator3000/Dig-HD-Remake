from pathlib import Path
import json, shutil, re
from PIL import Image, ImageChops, ImageDraw

Q = Path(__file__).resolve().parent
G = Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk')
R = G / 'rapporter/rom032-inngravering-20261013'
cases = json.loads((Q / 'cases.json').read_text())
assert len(cases) == 8
redraw, identical, entries = 0, 0, []
gallery = Image.new('RGB', (1280, 4 * 424), '#15171b')
draw = ImageDraw.Draw(gallery)
for i, case in enumerate(cases):
    tag = case['tag']
    packaged, native = Q / ('packaged-' + tag), Q / ('native-' + tag)
    qa = json.loads((packaged / 'result.json').read_text())
    assert qa['passed'] and all(c['pixels'] == 0 for c in qa['checks'])
    redraw += len(qa['checks'])
    frame = 'frame_000110_room032.png'
    p, n = Image.open(packaged / frame).convert('RGB'), Image.open(native / frame).convert('RGB')
    same = ImageChops.difference(p, n).getbbox() is None
    identical += same
    assert same, tag
    log = (packaged / 'run.log').read_text()
    assert 'room 32 loaded (1280x800)' in log
    objects = []
    for name in case['objects']:
        obj, state = map(int, name.removeprefix('obj').split('_'))
        found = re.search(rf'test object {obj} state {state} frame 110: drawn yes, HD image yes, object px (\d+), HD object px (\d+)', log)
        assert found, name
        objects.append({'name': name, 'drawn': True, 'HD_image_loaded': True,
                        'object_pixels': int(found[1]), 'HD_object_pixels': int(found[2])})
    for name in ['run.log', 'result.json']:
        out = R / 'packaged-qa' / (tag + '-' + name)
        out.parent.mkdir(exist_ok=True)
        shutil.copy2(packaged / name, out)
    out = R / 'screenshots' / ('packaged-' + tag + '.png')
    out.parent.mkdir(exist_ok=True)
    shutil.copy2(packaged / frame, out)
    x, y = (i % 2) * 640, (i // 2) * 424
    draw.text((x + 8, y + 5), tag, fill='white')
    gallery.paste(p.resize((640, 400), Image.Resampling.LANCZOS), (x, y + 24))
    entries.append({'case': tag, 'passed': True, 'checks': len(qa['checks']), 'pixel_identical_to_native': same, 'objects': objects})
gallery.save(R / 'KS-OVERSIKT.png')
shutil.copy2(R / 'screenshots/packaged-room32-base.png', R / 'rom032-runtime-r10.png')
assert redraw == 16 and identical == 8
result = {'passed': True, 'cases_count': 8, 'redraw_checks': redraw, 'all_redraw_differences_zero': True,
          'complete_frames_pixel_identical_to_native': identical, 'entries': entries,
          'scope': 'Actual AppImage/FUSE, room32 base plus seven forced object states, isolated save copies. No full playthrough, normal puzzle progression or physical keyboard test. User visual approval remains pending.'}
(R / 'QA-APPIMAGE.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result), flush=True)
