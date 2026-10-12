#!/usr/bin/env python3
"""Apply the reviewed R4 head placements after the R3 import, without repainting.

Usage: python3 import_alignment.py /path/to/mod
Unknown input drawings are rejected before any file is written. Already applied
files are accepted so the same delivery can be imported again safely.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil


def digest(path):
    with path.open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mod', type=Path)
    parser.add_argument('--manifest', type=Path, default=here / 'ALIGNMENT.json')
    parser.add_argument('--assets', type=Path, default=here / 'assets')
    args = parser.parse_args()
    records = json.loads(args.manifest.read_text())['files']
    pending = []
    for record in records:
        relative = Path(record['file'])
        if relative.is_absolute() or '..' in relative.parts:
            raise SystemExit(f'Invalid asset path: {relative}')
        source, target = args.assets / relative, args.mod / relative
        if not source.is_file() or digest(source) != record['sha256']:
            raise SystemExit(f'Missing or changed reviewed asset: {source}')
        if not target.is_file():
            raise SystemExit(f'Missing R3 input: {target}')
        current = digest(target)
        if current == record['sha256']:
            continue
        if current != record['input_sha256']:
            raise SystemExit(f'Unknown input drawing, left untouched: {target}')
        pending.append((source, target))
    for source, target in pending:
        temporary = target.with_name(target.name + '.r4-tmp')
        if temporary.exists():
            raise SystemExit(f'Unexpected temporary file: {temporary}')
        shutil.copy2(source, temporary)
        os.replace(temporary, target)
    print(json.dumps({'reviewed_heads': len(records), 'updated': len(pending),
                      'already_applied': len(records) - len(pending)}))


if __name__ == '__main__':
    main()
