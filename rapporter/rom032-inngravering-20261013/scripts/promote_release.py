from pathlib import Path
import subprocess, json, hashlib

Q = Path(__file__).resolve().parent
R = Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk/rapporter/rom032-inngravering-20261013')
repo = 'Tombonator3000/Dig-HD-Remake'
base = 'repos/' + repo
checked = json.loads((R / 'PACKAGED-CONTENT.json').read_text())
qa = json.loads((R / 'QA-APPIMAGE.json').read_text())
assert checked['passed'] and qa['passed'] and qa['cases_count'] == 8 and qa['redraw_checks'] == 16
expected = 'sha256:' + checked['sha256']
previous = 'sha256:' + checked['baseline_r9_sha256']

def api(path, *args):
    return json.loads(subprocess.check_output(['gh', 'api', base + path, *args], text=True))

def rename(asset, name):
    return api('/releases/assets/' + str(asset['id']), '-X', 'PATCH', '-f', 'name=' + name)

def digest(path):
    return 'sha256:' + hashlib.sha256(path.read_bytes()).hexdigest()

release = api('/releases/tags/linux')
assert release['id'] == 407919635 and release['name'] == 'The Dig HD for Linux (2026-10-13 r9)'
assets = {a['name']: a for a in release['assets']}
new, old = assets['TheDigHD-20261013-r10-x86_64.AppImage'], assets['TheDigHD-x86_64.AppImage']
assert new['state'] == 'uploaded' and new['size'] == checked['bytes'] and new['digest'] == expected
assert old['digest'] == previous and old['id'] == 635168934
assert 'TheDigHD-20261013-r9-x86_64.AppImage' not in assets and 'LES-MEG-LINUX-r9.txt' not in assets
assert assets['LES-MEG-LINUX.txt']['id'] == 635176668
assert assets['LES-MEG-LINUX.txt']['digest'] == 'sha256:275c89b26d7d0ddcc63f4d1ae88cc2c3466fbe0f65db5427b259888aae227299'
assert assets['LES-MEG-LINUX-r10.txt']['state'] == 'uploaded'
assert assets['LES-MEG-LINUX-r10.txt']['digest'] == digest(Q / 'LES-MEG-LINUX-r10.txt')
rename(old, 'TheDigHD-20261013-r9-x86_64.AppImage')
try:
    rename(new, 'TheDigHD-x86_64.AppImage')
except Exception:
    rename(old, 'TheDigHD-x86_64.AppImage')
    raise
rename(assets['LES-MEG-LINUX.txt'], 'LES-MEG-LINUX-r9.txt')
try:
    rename(assets['LES-MEG-LINUX-r10.txt'], 'LES-MEG-LINUX.txt')
except Exception:
    rename(assets['LES-MEG-LINUX.txt'], 'LES-MEG-LINUX.txt')
    raise
subprocess.run(['gh', 'release', 'upload', 'linux', str(Q / 'TheDigHD-x86_64.AppImage.sha256'), str(Q / 'TheDigHD-20261013-r9-x86_64.AppImage.sha256'), '--repo', repo, '--clobber'], check=True)
subprocess.run(['gh', 'release', 'edit', 'linux', '--repo', repo, '--title', 'The Dig HD for Linux (2026-10-13 r10)', '--notes-file', str(Q / 'release-r10-body.md'), '--latest'], check=True)
latest = api('/releases/latest')
assert latest['id'] == 407919635 and latest['name'] == 'The Dig HD for Linux (2026-10-13 r10)'
final = {a['name']: a for a in latest['assets']}
asset = final['TheDigHD-x86_64.AppImage']
assert asset['id'] == new['id'] and asset['digest'] == expected and asset['state'] == 'uploaded' and asset['size'] == checked['bytes']
assert final['TheDigHD-20261013-r9-x86_64.AppImage']['digest'] == previous
assert final['LES-MEG-LINUX.txt']['digest'] == digest(Q / 'LES-MEG-LINUX-r10.txt')
for name in ['TheDigHD-x86_64.AppImage.sha256', 'TheDigHD-20261013-r9-x86_64.AppImage.sha256']:
    assert final[name]['digest'] == digest(Q / name)
result = {'release_id': latest['id'], 'release_title': latest['name'], 'latest_verified': True,
          'asset_id': asset['id'], 'asset_name': asset['name'], 'bytes': asset['size'],
          'sha256': checked['sha256'], 'download': asset['browser_download_url'],
          'r9_preserved_as_dated_asset': True, 'room032_engraving_corrected': True,
          'packaged_test_cases': qa['cases_count'], 'packaged_redraw_checks': qa['redraw_checks'],
          'user_visual_QA_pending': True, 'passed': True}
(R / 'PUBLISHED-R10.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result), flush=True)
