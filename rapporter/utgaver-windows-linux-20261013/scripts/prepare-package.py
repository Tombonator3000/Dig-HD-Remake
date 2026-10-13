from pathlib import Path
import shutil,subprocess,json,hashlib
R=Path(__file__).resolve().parent;out=R/'windows/TheDigHD';out.mkdir(parents=True,exist_ok=True)
app=Path.home()/'Skrivebord/TheDigHD-x86_64.appimage'
p=subprocess.Popen([str(app),'--appimage-mount'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
root=Path(p.stdout.readline().strip());assert str(root).startswith('/tmp/.mount_') and root.is_dir()
try:
 data=root/'usr/share/the-dig-hd'
 for name in ['game','mods']:
  shutil.copytree(data/name,out/name,dirs_exist_ok=True)
 themes=out/'support';themes.mkdir(exist_ok=True)
 for f in data.iterdir():
  if f.is_file():shutil.copy2(f,themes/f.name)
 for name in ['source-patches','delivery']:
  shutil.copytree(root/name,out/name,dirs_exist_ok=True)
 shutil.copy2(root/'BUILD.json',out/'LINUX-R10-BUILD.json')
 checks={str(f.relative_to(data)):hashlib.file_digest(f.open('rb'),'sha256').hexdigest() for d in ['game','mods'] for f in (data/d).rglob('*') if f.is_file()}
 (R/'linux-content-sha256.json').write_text(json.dumps(checks,indent=2))
 print('Copied',len(checks),'files from the verified r10 AppImage')
finally:
 p.terminate();p.wait(timeout=10)
# Launch directly in the game; user settings and saves stay outside extracted package.
launcher=r'''@echo off
setlocal
cd /d "%~dp0"
set "DATA=%~dp0"
if not defined DIGHD_USER_DIR set "DIGHD_USER_DIR=%APPDATA%\TheDigHD"
if not exist "%DIGHD_USER_DIR%" mkdir "%DIGHD_USER_DIR%"
if not exist "%DIGHD_USER_DIR%\saves" mkdir "%DIGHD_USER_DIR%\saves"
if not exist "%DIGHD_USER_DIR%\scummvm.ini" copy /y "%DATA%default.ini" "%DIGHD_USER_DIR%\scummvm.ini" >nul
if not defined DIGHD_MOD set "DIGHD_MOD=%DATA%mods\gpt"
"%DATA%scummvm.exe" --config="%DIGHD_USER_DIR%\scummvm.ini" --path="%DATA%game" --savepath="%DIGHD_USER_DIR%\saves" --themepath="%DATA%support" --extrapath="%DATA%support" %* dig
if errorlevel 1 (
 echo.
 echo Spillet kunne ikke starte. Se scummvm.log i %%APPDATA%%\ScummVM\Logs.
 pause
)
endlocal
'''
(out/'Start The Dig HD.cmd').write_bytes(launcher.replace('\n','\r\n').encode('utf-8'))
(out/'default.ini').write_text('[scummvm]\nfullscreen=true\naspect_ratio=true\nsubtitles=true\ngui_return_to_launcher_at_exit=false\nconfirm_exit=false\n\n[dig]\ndescription=The Dig HD\nengineid=scumm\ngameid=dig\nsubtitles=true\n')
print('Windows staging ready:',out)
