from pathlib import Path
import hashlib,json,zipfile,shutil
R=Path(__file__).resolve().parent;P=R/'windows/TheDigHD'
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
build=json.loads((R/'WINDOWS-CONTENT.json').read_text());build.update(revision='20261013-r10',game_data_baseline='TheDigHD-x86_64.AppImage',linux_baseline_sha256='d8769b180ee9c8acf532de03b36d2058f19badd3b7383d56d66323a26fc6ed68',runtime_test='Wine 10 on Kubuntu, six cases, 32 redraw checks',physical_Windows_tested=False,compiler='MinGW-w64 GCC 13.2 posix',SDL2='2.32.10',libpng='1.6.55',zlib='1.3.2',source_download='https://github.com/Tombonator3000/Dig-HD-Remake/releases/download/windows/TheDigHD-r10-engine-source.tar.gz')
(P/'BUILD-WINDOWS.json').write_text(json.dumps(build,indent=2))
(P/'BUILD-WINDOWS.txt').write_text('Motorens fulle kildekode:\n'+build['source_download']+'\n\nScummVM-base c9091321060acfc8f037767c18f8279a86305b7e med de vedlagte patchene.\nByggeskriptet og kildefingeravtrykk følger kildearkivet.\nAvhengigheter: SDL2-devel-2.32.10-mingw.tar.gz fra libsdl-org/SDL,\nzlib-1.3.2 fra zlib.net, libpng v1.6.55 fra pnggroup/libpng.\nMinGW-w64 GCC 13.2 posix fra Ubuntu-pakkearkivet.\n')
for dep,src in [('SDL2-LICENSE.txt',R/'SDL2-2.32.10/LICENSE.txt'),('libpng-LICENSE.txt',R/'libpng-1.6.55/LICENSE'),('zlib-LICENSE.txt',R/'zlib-1.3.2/LICENSE')]:
 assert src.is_file(),src
 shutil.copy2(src,P/'support'/dep)
shutil.copy2(R/'toolchain/usr/share/doc/mingw-w64-x86-64-dev/copyright',P/'support/MinGW-w64-COPYRIGHT.txt')
files=[f for f in P.rglob('*') if f.is_file()];names=[f.relative_to(P).as_posix() for f in files];assert len(names)==len({n.casefold() for n in names})
assert max(map(len,names))<200
checks={n:sha(P/n) for n in names};(P/'SHA256SUMS').write_text(''.join(h+'  '+n+'\n' for n,h in sorted(checks.items())))
zip_path=R/'TheDigHD-Windows-x64.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in sorted(P.rglob('*')):
  if f.is_file():z.write(f,Path('TheDigHD')/f.relative_to(P))
with zipfile.ZipFile(zip_path) as z:
 assert z.testzip() is None
 target=R/'qa-zip/Windows test with spaces';target.mkdir(parents=True,exist_ok=True);z.extractall(target)
for n,h in checks.items():assert sha(target/'TheDigHD'/n)==h,n
zipsha=sha(zip_path);(R/(zip_path.name+'.sha256')).write_text(zipsha+'  '+zip_path.name+'\n')
result={'file':str(zip_path),'bytes':zip_path.stat().st_size,'sha256':zipsha,'files':len(checks)+1,'zip_CRC_passed':True,'extracted_checksums_verified':len(checks),'extracted_to':str(target/'TheDigHD'),'passed':True}
(R/'WINDOWS-ZIP-QA.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
