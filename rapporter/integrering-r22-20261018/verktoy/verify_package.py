"""Verify downloaded release bytes and run the package's default AppRun in isolation."""
from pathlib import Path
import json,hashlib,subprocess,os,re
R=Path('/home/tom/Documents/ChatGPT/THE DIG');P=R/'grafikk/rapporter/integrering-r22-20261018';T=R/'testing/distro-r22';A=T/'AppDir';img=T/'TheDigHD-x86_64.AppImage';release=json.loads((T/'release.json').read_text());asset=next(a for a in release['assets'] if a['name']==img.name)
sha=lambda p:hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
h=sha(img);assert h==(T/(img.name+'.sha256')).read_text().split()[0];assert asset['digest']=='sha256:'+h and asset['size']==img.stat().st_size;assert 'hd-mod: 044ae88e521a08846e8129be4e87e5e06d6993a9' in release['body'];img.chmod(0o700)
offset=subprocess.check_output([str(img),'--appimage-offset'],text=True).strip();assert offset.isdigit()
if not A.exists():
 with (T/'extract.log').open('w') as log:subprocess.run(['unsquashfs','-no-progress','-processors','4','-d',str(A),'-o',offset,str(img)],stdout=log,stderr=subprocess.STDOUT,check=True)
D=A/'usr/share/the-dig-hd';M=D/'mods/gpt';build=(D/'BYGG.txt').read_text();code='64df34e0142d28e1d049d05372bb800ab20070a6';assert code.startswith(re.search(r'Dig-HD-Remake: ([0-9a-f]+)',build)[1]);assert 'hd-mod: 044ae88e521a08846e8129be4e87e5e06d6993a9' in build
sums={line[66:]:line[:64] for line in (M/'SHA256SUMS').read_text().splitlines() if line}
for f,d in sums.items():assert sha(M/f)==d,f
assert {str(f.relative_to(M)) for f in M.rglob('*') if f.is_file() and f.name!='SHA256SUMS'}==set(sums)
local={line[66:]:line[:64] for line in (R/'hd-leveranse/SHA256SUMS').read_text().splitlines() if line};assert sums==local
payload=json.loads((P/'payload.json').read_text())
for f,d in payload.items():assert sums[f]==d
assert len(list((M/'san').glob('*.ivf')))==55 and not list((M/'san').rglob('*.png'));meta=json.loads((M/'mod.json').read_text());assert meta['revision']=='r22-20261018'
assert hashlib.file_digest((D/'game/DIG.LA0').open('rb'),'md5').hexdigest()=='d8323015ecb8b10bf53474f6e6b0ae33';assert sha(D/'game/DIG.LA1')=='8f2a0474dfe2d99c37b8182b08d8bb79afe95388df5c9d608ae3bb267536a957'
S=T/'smoke';S.mkdir(exist_ok=True);env={k:v for k,v in os.environ.items() if not k.startswith('DIGHD_')};env.update(HOME=str(S/'home'),XDG_CONFIG_HOME=str(S/'config'),XDG_DATA_HOME=str(S/'data'),XDG_CACHE_HOME=str(S/'cache'),SDL_VIDEODRIVER='dummy',SDL_AUDIODRIVER='dummy',DIGHD_VERIFY='1',DIGHD_MANGLER='0',DIGHD_DUMP_DIR=str(S/'dumps'),DIGHD_DUMP_EVERY='100',DIGHD_TEST_KEYS='200:ctrl+h,400:ctrl+h',DIGHD_QUIT_AT='550')
with (S/'log.txt').open('w') as log:subprocess.run([str(A/'AppRun'),'--debuglevel=1'],env=env,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=240)
s=(S/'log.txt').read_text();assert 'compressed video SQ1, 3772 frames' in s and 'classic graphics, all 64000 px original' in s and 'DigHD: HD graphics' in s and 'DigHD: frame 550,' in s;checks=[int(n) for n in re.findall(r'verify frame \d+: (\d+) screen pixels differ from the whole screen built again',s)];assert checks and max(checks)==0;assert "can't open bundle" not in s.lower();assert not re.search(r'^(?:ERROR|Assertion).*$',s,re.M)
report=dict(result='PASS',code=code,hd_mod='044ae88e521a08846e8129be4e87e5e06d6993a9',graphics=json.loads((P/'integration.json').read_text())['graphics_commit'],build_run=39117793203,appimage_sha256=h,appimage_bytes=img.stat().st_size,verified_mod_files=len(sums),payload_files_verified=len(payload),added_files=96,replaced_files=182,new_hd_cels=48,palette_corrected_fragments=91,films=55,previous_resources_preserved=True,default_AppRun_smoke_updates=550,redraw_checks=len(checks),redraw_differences=max(checks),source=json.loads((P/'source-unchanged.json').read_text()),remaining_art_cels=5963,human_visual_approval=False,full_playthrough=False,windows_mobile_tested=False)
(T/'kontroll-linux.json').write_text(json.dumps(report,indent=2)+'\n');print('Package PASS',img.stat().st_size,h,len(sums),'mod files, smoke550 checks',len(checks))
