"""Assemble delivery atlases from generated room art and unchanged runtime objects.

This only places existing assets at metadata coordinates. It draws no new art.
"""
from pathlib import Path
import hashlib, json, shutil
from PIL import Image

G = Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk')
Q = Path(__file__).resolve().parent
R = G / 'rapporter/rom032-inngravering-20261013'
M = Path('/home/tombonator3000t/Skrivebord/TheDigHD-Linux-20261012-test/usr/share/the-dig-hd/mods/gpt')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

background = Image.open(R / 'assets/rom032-generert.png').convert('RGB')
assert background.size == (1536, 1024)
records = []
for d in sorted((G / 'jobber').glob('lag032_*')):
    metadata = json.loads((d / 'jobb.json').read_text())
    assert metadata['rom_storrelse'] == [320, 200] and metadata['region'] == [0, 0, 320, 200]
    backup = Q / 'before/jobber' / d.name
    backup.mkdir(parents=True, exist_ok=True)
    for name in ['resultat.png', 'notat.md']:
        if not (backup / name).exists():
            shutil.copy2(d / name, backup / name)
    canvas = background.copy()
    placed = []
    for entry in metadata['objekter']:
        source = M / 'objects' / (entry['bilde'] + '.png')
        art = Image.open(source).convert('RGBA')
        x, y, w, h = entry['rekt']
        assert art.size == (w * 4, h * 4)
        canvas.paste(art, (128 + x * 4, 112 + y * 4), art)
        placed.append({'object': entry['bilde'], 'rect_native': entry['rekt'],
                       'runtime_art_sha256': sha(source), 'alpha': 'unchanged native-derived runtime alpha'})
    canvas.save(d / 'resultat.png')
    record = {'job': d.name, 'kind': 'technical atlas, not a fresh raw generator image',
              'generated_room_source': 'assets/rom032-generert.png',
              'room_source_sha256': sha(R / 'assets/rom032-generert.png'),
              'objects': placed, 'result_sha256': sha(d / 'resultat.png')}
    records.append(record)
    note = d / 'notat.md'
    note.write_text(note.read_text() + '\n## Romanker rettet 13. oktober 2026\n\n'
        'Tom presiserer at motivet på søylen er en inngravering, uten utstikkende armatur eller vann. '
        'Det gamle dusjmotivet i romkonteksten er erstattet. Ny resultat.png er et teknisk atlas av '
        'det korrigerte generatorbildet for rom 32 og dette lagets eksisterende HD-objekt plassert '
        'etter jobbens posisjon og alfa. Objektets runtime-PNG og originale indeksfil er uendret. '
        'Motivrettelsen er tegnet med innebygd bildegenerator; kode er bare brukt til atlasplassering. '
        'Tidligere råresultat er bevart i Git-historikken. Se '
        'rapporter/rom032-inngravering-20261013/LAYER-CONTEXTS.json. Tidligere merknader om '
        'objektets ekstra bruker-KS gjelder fortsatt.\n\nNy atlas-SHA256: `' + record['result_sha256'] + '`\n')
(R / 'LAYER-CONTEXTS.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
print('Updated layer contexts:', len(records))
