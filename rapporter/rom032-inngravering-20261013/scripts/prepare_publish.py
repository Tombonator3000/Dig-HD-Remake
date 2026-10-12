from pathlib import Path
import json, os, shutil

Q = Path(__file__).resolve().parent
R = Path('/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk/rapporter/rom032-inngravering-20261013')
package = json.loads((R / 'PACKAGED-CONTENT.json').read_text())
qa = json.loads((R / 'QA-APPIMAGE.json').read_text())
assert package['passed'] and qa['passed'] and qa['cases_count'] == 8 and qa['redraw_checks'] == 16
source = Path(package['appimage'])
upload = Q / 'TheDigHD-20261013-r10-x86_64.AppImage'
if upload.exists():
    assert os.path.samefile(source, upload)
else:
    os.link(source, upload)
(Q / 'TheDigHD-x86_64.AppImage.sha256').write_text(package['sha256'] + '  TheDigHD-x86_64.AppImage\n')
(Q / 'TheDigHD-20261013-r9-x86_64.AppImage.sha256').write_text(package['baseline_r9_sha256'] + '  TheDigHD-20261013-r9-x86_64.AppImage\n')
readme = '''The Dig HD for Linux, 13. oktober 2026 r10

Rom 32 er rettet: motivet på søylen er en inngravering i stein.
Den feilaktige dusjen, utstikkende armaturet og vannstrålen er fjernet.
Romankeret for de syv lagjobbene er også oppdatert.

R9s 20 lagjobber / 31 små objektbilder, gullstavrettelsen, alle 15
HD-krystalltilstander, 106 HD-rombakgrunner og 551 rettede hoder
er beholdt. Motor, originale indekser og de syv rom32-objektbildene
er uendret fra r9. Hele spillets grafikk er fortsatt ikke ferdig i HD.

Last ned TheDigHD-x86_64.AppImage, gjør filen kjørbar og start den.
Pakken inkluderer spill, motor, tale, musikk og mod for offline bruk.
Meny: F5, F1 eller Ctrl+K. Enkelte tastatur krever Fn+F5.

Kontrollert i faktisk AppImage: rom32s grunnbilde og syv objekttilstander,
16 opptegningskontroller uten avvik og åtte skjermbilder identiske med
native test. Alle modfiler har verifisert sjekksum. Ingen full
gjennomspilling, normal gåteprogresjon eller ny fysisk tastaturtest.

Visuell bruker-KS er åpen i HD-SJEKKLISTE.md på grenen gpt-arbeid.
Tidligere ekstra KS for lag027_03_del2av8, lag032_05/07 gjelder fortsatt.
R9 er bevart som datert fil.
'''
(Q / 'LES-MEG-LINUX-r10.txt').write_text(readme)
body = '''Linux r10 retter motivet på søylen i **rom 32 til en inngravering i stein**, slik Tom har presisert. Den feilaktige dusjen, det utstikkende armaturet og vannstrålen er fjernet. Romankeret for de syv lagjobbene er oppdatert.

R9s 20 lagjobber / 31 små objektbilder, den glatte gullstaven, alle 15 HD-krystalltilstander, 106 rombakgrunner og 551 korrigerte hoder er beholdt. Motor, originale indeksfiler og de syv rom32-objektbildene er uendret. Hele spillets grafikk er fortsatt ikke ferdig i HD.

Last ned **TheDigHD-x86_64.AppImage**, gjør filen kjørbar og start den. Pakken inneholder spill, motor, tale, musikk og HD-mod for offline bruk. Meny: **F5**, **F1** eller **Ctrl+K**. Fn+F5 kan være nødvendig på enkelte tastatur.

Faktisk AppImage/FUSE er kontrollert med **åtte rom-/tilstandstester og 16 opptegningskontroller uten avvik**. Alle åtte ferdige skjermbilder er pikselidentiske med native test. Alle modfiler har verifisert sjekksum; bare room032.png og modmetadata er endret fra r9. Ingen full gjennomspilling, normal gåteprogresjon eller ny fysisk tastaturtest er utført.

[KS-sjekklisten](https://github.com/Tombonator3000/Dig-HD-Remake/blob/gpt-arbeid/HD-SJEKKLISTE.md) og [rettelsesrapporten](https://github.com/Tombonator3000/Dig-HD-Remake/blob/gpt-arbeid/rapporter/rom032-inngravering-20261013/LEVERANSE.md) skiller teknisk kontroll fra brukerens visuelle godkjenning. Tidligere ekstra KS for lag027_03_del2av8, lag032_05 og lag032_07 gjelder fortsatt. R9 er bevart som datert releasefil.

SHA256: `''' + package['sha256'] + '''`

Størrelse: ''' + str(package['bytes']) + ''' byte.
'''
(Q / 'release-r10-body.md').write_text(body)
print('Verified r10 ready for upload:', package['sha256'])
