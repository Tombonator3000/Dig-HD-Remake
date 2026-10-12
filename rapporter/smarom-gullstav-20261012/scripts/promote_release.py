from pathlib import Path
import subprocess, json, hashlib

Q = Path(__file__).resolve().parent
R = Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk/rapporter/smarom-gullstav-20261012')
repo = 'Tombonator3000/Dig-HD-Remake'
base = 'repos/' + repo
checked = json.loads((R / 'PACKAGED-CONTENT.json').read_text())
qa = json.loads((R / 'QA-APPIMAGE.json').read_text())
assert checked['passed'] and qa['passed']
assert qa['cases_count'] == 21 and qa['redraw_checks'] == 42
assert checked['runtime_files_verified'] == 70 and checked['protected_inputs_unchanged'] == 80
expected = 'sha256:' + checked['sha256']
previous = 'sha256:3d8581d5282b74385ed3f56a02c0621582c23505c82cbc83d70eaa79b38ee249'

def api(path, *args):
    return json.loads(subprocess.check_output(['gh', 'api', base + path, *args], text=True))

def rename(asset, name):
    return api('/releases/assets/' + str(asset['id']), '-X', 'PATCH', '-f', 'name=' + name)

release = api('/releases/tags/linux')
assert release['id'] == 407919635 and release['name'] == 'The Dig HD for Linux (2026-10-12 r8)'
assets = {a['name']: a for a in release['assets']}
new = assets['TheDigHD-20261013-r9-x86_64.AppImage']
old = assets['TheDigHD-x86_64.AppImage']
assert new['state'] == 'uploaded' and new['size'] == checked['bytes'] and new['digest'] == expected
assert old['digest'] == previous and old['id'] == 635006706
assert 'TheDigHD-20261012-r8-x86_64.AppImage' not in assets and 'LES-MEG-LINUX-r8.txt' not in assets
assert assets['LES-MEG-LINUX.txt']['id'] == 635006705
assert assets['LES-MEG-LINUX-r9.txt']['state'] == 'uploaded'
assert assets['LES-MEG-LINUX-r9.txt']['digest'] == 'sha256:' + hashlib.sha256((Q / 'LES-MEG-LINUX-r9.txt').read_bytes()).hexdigest()
rename(old, 'TheDigHD-20261012-r8-x86_64.AppImage')
try:
    rename(new, 'TheDigHD-x86_64.AppImage')
except Exception:
    rename(old, 'TheDigHD-x86_64.AppImage')
    raise
rename(assets['LES-MEG-LINUX.txt'], 'LES-MEG-LINUX-r8.txt')
try:
    rename(assets['LES-MEG-LINUX-r9.txt'], 'LES-MEG-LINUX.txt')
except Exception:
    rename(assets['LES-MEG-LINUX.txt'], 'LES-MEG-LINUX.txt')
    raise
subprocess.run(['gh', 'release', 'upload', 'linux', str(Q / 'TheDigHD-x86_64.AppImage.sha256'), str(Q / 'TheDigHD-20261012-r8-x86_64.AppImage.sha256'), '--repo', repo, '--clobber'], check=True)
subprocess.run(['gh', 'release', 'edit', 'linux', '--repo', repo, '--title', 'The Dig HD for Linux (2026-10-13 r9)', '--notes-file', str(Q / 'release-r9-body.md'), '--latest'], check=True)
latest = api('/releases/latest')
assert latest['id'] == 407919635 and latest['name'] == 'The Dig HD for Linux (2026-10-13 r9)'
final = {a['name']: a for a in latest['assets']}
asset = final['TheDigHD-x86_64.AppImage']
assert asset['id'] == new['id'] and asset['digest'] == expected and asset['state'] == 'uploaded' and asset['size'] == checked['bytes']
assert final['TheDigHD-20261012-r8-x86_64.AppImage']['digest'] == previous
assert final['LES-MEG-LINUX.txt']['digest'] == 'sha256:' + hashlib.sha256((Q / 'LES-MEG-LINUX-r9.txt').read_bytes()).hexdigest()
for name in ['TheDigHD-x86_64.AppImage.sha256', 'TheDigHD-20261012-r8-x86_64.AppImage.sha256']:
    assert final[name]['digest'] == 'sha256:' + hashlib.sha256((Q / name).read_bytes()).hexdigest()
result = {
    'release_id': latest['id'], 'release_title': latest['name'], 'latest_verified': True,
    'asset_id': asset['id'], 'asset_name': asset['name'], 'bytes': asset['size'],
    'sha256': checked['sha256'], 'download': asset['browser_download_url'],
    'r8_preserved_as_dated_asset': True, 'small_object_jobs': 20, 'object_images': 31,
    'golden_rod_states_checked': 3, 'hd_room_backgrounds': 106,
    'all15_crystal_states_retained': True, 'corrected_heads_retained': 551,
    'packaged_test_cases': qa['cases_count'], 'packaged_redraw_checks': qa['redraw_checks'],
    'user_visual_QA_pending': True, 'passed': True,
}
(R / 'PUBLISHED-R9.json').write_text(json.dumps(result, indent=2) + '\n')
p = R / 'LEVERANSE.md'
p.write_text(p.read_text() + '\nGitHub Linux-releasen er oppdatert til r9 som Latest. Den stabile AppImage-nedlastingen har samme SHA256 og størrelse som den lokalt kontrollerte pakken. R8 er bevart som datert releasefil. Se PUBLISHED-R9.json.\n')
print(json.dumps(result), flush=True)
