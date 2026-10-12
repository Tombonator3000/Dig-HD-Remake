from pathlib import Path
import os,json,shutil
Q=Path(__file__).resolve().parent;R=Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk/rapporter/smarom-gullstav-20261012');meta=json.loads((R/'PACKAGED-CONTENT.json').read_text());qa=json.loads((R/'QA-APPIMAGE.json').read_text());assert meta['passed'] and qa['passed'] and qa['redraw_checks']==42
app=Path(meta['appimage']);alias=Q/'TheDigHD-20261013-r9-x86_64.AppImage'
if not alias.exists():os.link(app,alias)
(Q/'TheDigHD-x86_64.AppImage.sha256').write_text(meta['sha256']+'  TheDigHD-x86_64.AppImage\n');(Q/'TheDigHD-20261012-r8-x86_64.AppImage.sha256').write_text('3d8581d5282b74385ed3f56a02c0621582c23505c82cbc83d70eaa79b38ee249  TheDigHD-20261012-r8-x86_64.AppImage\n')
(Q/'LES-MEG-LINUX-r9.txt').write_text('''The Dig HD for Linux, 13. oktober 2026 r9

20 tidligere manglende lagjobber er levert.31 små objektbilder i rom
23,25,26,27,32,77,88 og90 er integrert. Gullstaven i rod-nærbildet
har ny glatt grafikk og riktig gullgrunnpalett i alle tre tilstander.
Alle106 HD-rombakgrunner,15 HD-krystallruter og551 halsrettede hoder
følger med. Spillmotoren er uendret fra r8. Hele spillets grafikk er
fortsatt ikke ferdig i HD.

KS-listen ligger i HD-SJEKKLISTE.md på grenen gpt-arbeid. Rom27 og de
to bakgrunns-/beintilstandene lag032_05 og lag032_07 har egne merknader
for ekstra visuell KS. Brukergodkjenning står åpen.

Last ned TheDigHD-x86_64.AppImage, gjør filen kjørbar og start den.
Pakken inneholder spill, motor, tale, musikk og mod for offline bruk.
Meny: F5, F1 eller Ctrl+K. Fn+F5 kan være nødvendig på enkelte tastatur.

Kontrollert i faktisk AppImage:21 avgrensede rom-/tilstandstester,
42 opptegningskontroller uten avvik.70 leveransefiler og25379 modfiler
har verifisert sjekksum. Ingen full gjennomspilling eller ny fysisk
tastaturtest. R8 beholdes som datert fil.
''')
(Q/'release-r9-body.md').write_text(f'''Linux r9 inneholder **20 nye lagjobber med31 små objektbilder**, særlig i rom32,77 og88. **Gullstaven i rod-nærbildet har ny glatt HD-grafikk og riktig gullgrunnpalett**, med kontroll av alle tre hånd-/stavtilstander. Bakgrunnsskjøter i kartlagene i rom77 er rettet.

Alle106 HD-rombakgrunner, alle15 HD-krystallruter og551 rettede hoder er beholdt. Spillmotoren er uendret fra r8. Hele spillets grafikk er fortsatt ikke ferdig i HD.

Dette er også et bygg for videre visuell KS. [HD-SJEKKLISTE.md](https://github.com/Tombonator3000/Dig-HD-Remake/blob/gpt-arbeid/HD-SJEKKLISTE.md) har egne avkryssinger for brukerens godkjenning. **lag027_03_del2av8, lag032_05 og lag032_07 er merket for ekstra visuell KS**, med automatiske kontrollutslag og begrunnelse bevart i jobbnotatene.

Last ned **TheDigHD-x86_64.AppImage**, gjør filen kjørbar og start den. Pakken inkluderer spill, motor, tale, musikk og HD-mod for offline bruk. Meny: **F5**, **F1** eller **Ctrl+K**. Fn+F5 kan være nødvendig på enkelte tastatur.

Faktisk AppImage/FUSE er kjørt gjennom21 avgrensede rom- og tilstandstester. Alle42 opptegningskontroller ga null avvik.20 ferdige skjermbilder var pikselidentiske med native; rom25 har tidsstyrt fargesyklus og er ført separat.70 leveransefiler og alle25379 modfiler har verifisert sjekksum. Dette er ikke en full gjennomspilling eller ny fysisk tastaturtest. R8 er bevart som datert releasefil.

SHA256: `{meta['sha256']}`

Størrelse: {meta['bytes']} byte.
''')
shutil.copy2(Q/'TheDigHD-x86_64.AppImage.sha256',R/'TheDigHD-x86_64.AppImage.sha256');print('Ready for upload',alias,flush=True)
