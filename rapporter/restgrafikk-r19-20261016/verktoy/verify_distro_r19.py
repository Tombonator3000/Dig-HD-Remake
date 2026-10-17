import os
"""Verify the actual downloaded r19 AppImage, its graphics manifest and isolated launcher."""
from pathlib import Path
import hashlib,json,subprocess,re,os
R=Path(os.environ.get("DIGHD_WORKSPACE", Path(__file__).resolve().parents[4]));T=R/'testing/distro-r19';img=T/'TheDigHD-x86_64.AppImage';meta=json.loads((T/'release.json').read_text());asset=next(a for a in meta['assets'] if a['name']==img.name);digest=hashlib.file_digest(img.open('rb'),'sha256').hexdigest();expected=(T/(img.name+'.sha256')).read_text().split()[0];assert digest==expected;assert asset['digest']=='sha256:'+digest;assert img.stat().st_size==asset['size'];img.chmod(0o700)
offset=subprocess.check_output([str(img),'--appimage-offset'],text=True).strip();assert offset.isdigit();A=T/'AppDir'
if not A.exists():
 with (T/'extract.log').open('w') as log:subprocess.run(['unsquashfs','-no-progress','-processors','4','-d',str(A),'-o',offset,str(img)],stdout=log,stderr=subprocess.STDOUT,check=True)
D=A/'usr/share/the-dig-hd';build=(D/'BYGG.txt').read_text();assert 'c2c9b8e00ba2e83af4001088bbccb976f0f22d1d'.startswith(re.search(r'Dig-HD-Remake: ([0-9a-f]+)',build)[1]);assert 'hd-mod: 630cadb3ebb398ac8ade1f4e1ea759f8a783cd5a' in build;M=D/'mods/gpt';count=0;sums={}
for line in (M/'SHA256SUMS').read_text().splitlines():
 h,p=line.split(maxsplit=1);p=p.lstrip('*');assert hashlib.file_digest((M/p).open('rb'),'sha256').hexdigest()==h,p;count+=1;sums[p]=h
actual={str(f.relative_to(M)) for f in M.rglob('*') if f.is_file() and f.name!='SHA256SUMS'};assert actual==set(sums),'unmanifested or absent mod files'
P=R/'grafikk/rapporter/restgrafikk-r19-20261016';adds=json.loads((P/'ADDITIONS.json').read_text());overrides=json.loads((P/'OVERRIDES.json').read_text())
for v in adds+overrides:assert sums[v['path']]==v['sha256'],v['path']
mm=json.loads((M/'mod.json').read_text());assert len(mm['compressed_films'])==55;assert len(list((M/'san').glob('*.ivf')))==55;assert not list((M/'san').rglob('*.png'));assert mm['revision']=='r19-20261017';assert mm['r19']['new_hd_cells']==7097
base=R/'testing/r19-published-base';base_sums={}
for line in (base/'SHA256SUMS').read_text().splitlines():
 h,p=line.split(maxsplit=1);p=p.lstrip('*');base_sums[p]=h
allowed={v['path'] for v in overrides}|{'README.md','mod.json'}
for p,h in base_sums.items():
 assert p in sums,p
 if p not in allowed:assert sums[p]==h,p
for f in ['DIG.LA0','DIG.LA1','DIGMUSIC.BUN','DIGVOICE.BUN','VIDEO/SQ1.SAN']:assert (D/'game'/f).is_file(),f
assert hashlib.file_digest((D/'game/DIG.LA0').open('rb'),'md5').hexdigest()=='d8323015ecb8b10bf53474f6e6b0ae33'
assert hashlib.file_digest((D/'game/DIG.LA1').open('rb'),'sha256').hexdigest()=='8f2a0474dfe2d99c37b8182b08d8bb79afe95388df5c9d608ae3bb267536a957'
S=T/'spilltest';S.mkdir(exist_ok=True);env=dict(os.environ,SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',XDG_CONFIG_HOME=str(S/'config'),XDG_DATA_HOME=str(S/'data'),DIGHD_VERIFY='1',DIGHD_DUMP_DIR=str(S/'dumps'),DIGHD_DUMP_EVERY='100',DIGHD_MANGLER='0',DIGHD_TEST_KEYS='200:ctrl+h,400:ctrl+h',DIGHD_QUIT_AT='550')
with (S/'log.txt').open('w') as log:subprocess.run([str(A/'AppRun'),'--debuglevel=1'],env=env,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=180)
s=(S/'log.txt').read_text();assert 'compressed video SQ1, 3772 frames' in s;assert 'classic graphics, all 64000 px original' in s;assert 'DigHD: HD graphics' in s;assert 'DigHD: frame 550,' in s;checks=[int(n) for n in re.findall(r'verify frame \d+: (\d+) screen pixels differ from the whole screen built again',s)];assert checks and max(checks)==0;assert "can't open bundle" not in s.lower();assert not re.search(r'^(?:ERROR|Assertion).*$',s,re.M)
report=dict(result='PASS',launcher_mode='default AppRun',forced_surfacesdl_windowed_headless_test='failed before game init with SDL null surface; default launcher tested separately',code='c2c9b8e00ba2e83af4001088bbccb976f0f22d1d',hd_mod='630cadb3ebb398ac8ade1f4e1ea759f8a783cd5a',graphics='f5a23834b969fe974714615eb36ea026a1aede23',appimage_sha256=digest,appimage_bytes=img.stat().st_size,verified_mod_files=count,additions_verified=len(adds),new_hd_cells=7097,replacements_verified=2,previous_files_preserved=True,films=55,smoke_updates=550,redraw_checks=len(checks),redraw_difference=max(checks),source=json.loads((T/'kildekontroll.json').read_text()),remaining_art_cells=6232,human_visual_approval=False,windows_mobile_full_playthrough='not tested')
(T/'kontroll-linux.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
