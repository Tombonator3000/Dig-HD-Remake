"""Apply this frozen r12 delivery after a standard mod build.

Usage: python3 apply-overrides.py /absolute/path/to/mods/gpt
Only paths and exact file hashes in OVERSTYRINGER-MANIFEST.json are accepted.
This is an explicit delivery importer, not an automatic gpt_runde hook.
"""
from pathlib import Path
import argparse, hashlib, json, shutil

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('mod',type=Path)
args=parser.parse_args()
report=Path(__file__).resolve().parents[1]
manifest=json.loads((report/'OVERSTYRINGER-MANIFEST.json').read_text())
target=args.mod.resolve()
if not (target/'mod.json').is_file():parser.error('Target must be an existing complete mod with mod.json')
files=[]
for row in manifest['files']:
    rel=Path(row['path'])
    if rel.is_absolute() or '..' in rel.parts or rel.parts[0] not in {'costumes','objects','rooms','fonts'}:
        raise ValueError('Invalid delivery path: '+str(rel))
    source=report/'mod-overrides'/rel
    if hashlib.sha256(source.read_bytes()).hexdigest()!=row['sha256']:
        raise ValueError('Source hash mismatch: '+str(rel))
    if not (target/rel).resolve().is_relative_to(target):raise ValueError('Target escapes mod: '+str(rel))
    files.append((source,target/rel,row['sha256']))
for source,destination,digest in files:
    destination.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source,destination)
    assert hashlib.sha256(destination.read_bytes()).hexdigest()==digest
print(f'Applied and verified {len(files)} r12 files. Regenerate the complete mod SHA256SUMS before packaging.')
