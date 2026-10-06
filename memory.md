# Prosjektminne

Faste fakta og beslutninger. Oppdateres når noe endrer seg.

## Mål
- HD-versjon av The Dig (LucasArts, 1995, SCUMM v7): HD-bakgrunner, HD-sprites, HD-mellomsekvenser.

## Spillfilene
- Ligger i Google Drive-mappen `1INroCLSVZQLhwsFeTmPuMFrF9ukyueEj` (under Arcade). Ren datamappe, engelsk standardutgave, data bygget 7. nov 1995.
- DIG.LA0 16 304 byte, DIG.LA1 88 673 344 byte, VIDEO/ med 55 SAN, FONT0-3.NUT, DIG.TRS, DIGTXT.TRS. Totalt rundt 660 MB.
- Spillfiler og uttrukket grafikk skal aldri inn i git, selv om repoet er privat.

## Omfang (målt)
- 111 rom (27 brede, 11 høye), 61 med z-plan, 21 med flere paletter.
- 642 objektbilder, 331 kostymer med 28 490 ruter, 55 SAN med 12 638 rammer.
- Romliste: `docs/rom-oversikt.csv`.

## Tekniske valg så langt
- Ingen dekompilering av exe. ScummVM er motoren.
- Uttrekk: thedig-textures (Python 3.12, Pillow, `--game STI`). Skript: descumm -7 eller NUTCracker.
- Motor: egen ScummVM-fork med parallell HD-flate (4x, 1280 x 800) og mod-mappe. Forbilde: `_macScreen` og `mac_drawStripToScreen` i ScummVM.
- Filnavn for HD-filer: ID-ene fra thedig-textures sitt `manifest.json`.

## Åpne valg
- Stil: trofast HD (A) eller ny tegnestil som konseptbildene (B). Anbefalt: bygg A først, test B på Boston Low og ett rom.

## Annet
- Konseptbildene i roten av repoet er laget av en Reddit-tegner (signert). Brukes som stilreferanse. Spør og krediter før noe vises offentlig.
