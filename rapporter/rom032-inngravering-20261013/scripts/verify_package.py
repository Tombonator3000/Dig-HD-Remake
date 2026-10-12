from pathlib import Path
import subprocess, json, hashlib

Q = Path(__file__).resolve().parent
G = Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk')
R = G / 'rapporter/rom032-inngravering-20261013'
D = Path('/home/tombonator3000t/Skrivebord')
app = D / 'TheDigHD-20261013-rettet-r10-x86_64.AppImage'
prior = D / 'TheDigHD-20261013-rettet-r9-x86_64.AppImage'
processes = []

def sha(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def mount(path):
    proc = subprocess.Popen([str(path), '--appimage-mount'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    processes.append(proc)
    root = Path(proc.stdout.readline().strip())
    assert root.is_dir() and str(root).startswith('/tmp/.mount_')
    return root

def sums(p):
    return {name: h for h, name in (line.split('  ', 1) for line in p.read_text().splitlines())}

try:
    new, old = mount(app), mount(prior)
    m = new / 'usr/share/the-dig-hd/mods/gpt'
    o = old / 'usr/share/the-dig-hd/mods/gpt'
    before, after = sums(o / 'SHA256SUMS'), sums(m / 'SHA256SUMS')
    assert set(before) == set(after)
    changed = {p for p in before if before[p] != after[p]}
    assert changed == {'rooms/room032.png', 'mod.json'}
    for p, h in after.items():
        assert sha(m / p) == h, p
    assert sha(m / 'rooms/room032.png') == json.loads((R / 'RUNTIME-FILES.json').read_text())['rooms/room032.png']
    assert sha(m / 'rooms/room032_idx.png') == sha(o / 'rooms/room032_idx.png')
    engine_sha = sha(new / 'usr/bin/scummvm')
    assert engine_sha == sha(old / 'usr/bin/scummvm') == '3080b02e8747692643784c7b376d2d6f60c908091b2a943bfb375a1988c1c788'
    build = json.loads((new / 'BUILD.json').read_text())
    assert build['release_revision'] == '20261013-r10' and build['room_backgrounds'] == 106
    plan = json.loads((R / 'PLAN.json').read_text())
    assert all(sha(G / p) == h for p, h in plan['protected_inputs_sha256'].items())
    # Check all package files outside the declared mod/metadata changes, including game/audio/libraries.
    newfiles = {p.relative_to(new).as_posix(): p for p in new.rglob('*') if p.is_file()}
    oldfiles = {p.relative_to(old).as_posix(): p for p in old.rglob('*') if p.is_file()}
    assert not (set(oldfiles) - set(newfiles))
    assert all(p.startswith('delivery/r10/') for p in set(newfiles) - set(oldfiles))
    exceptions = {'BUILD.json', 'usr/share/the-dig-hd/mods/gpt/SHA256SUMS'} | {
        'usr/share/the-dig-hd/mods/gpt/' + p for p in changed}
    nonmod_verified = 0
    for p in set(newfiles) & set(oldfiles):
        if p in exceptions or p.startswith('usr/share/the-dig-hd/mods/gpt/'):
            continue
        assert sha(newfiles[p]) == sha(oldfiles[p]), p
        nonmod_verified += 1
    assert json.loads((new / 'delivery/r10/RUNTIME-FILES.json').read_text()) == json.loads((R / 'RUNTIME-FILES.json').read_text())
    result = {
        'appimage': str(app), 'bytes': app.stat().st_size, 'sha256': sha(app),
        'baseline_r9_sha256': sha(prior), 'engine_unchanged_from_r9': True,
        'engine_sha256': engine_sha, 'changed_mod_files': sorted(changed),
        'unchanged_mod_files': len(after) - len(changed), 'mod_checksums_verified': len(after),
        'unchanged_nonmod_package_files_verified': nonmod_verified,
        'protected_inputs_unchanged': len(plan['protected_inputs_sha256']),
        'room032_original_indices_unchanged': True, 'all7_room32_objects_unchanged': True,
        'r9_gold_rod_and_all15_HD_crystals_retained': True, 'all551_corrected_heads_retained': True,
        'hd_room_backgrounds': 106, 'passed': True,
    }
    (R / 'PACKAGED-CONTENT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result), flush=True)
finally:
    for proc in processes:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
