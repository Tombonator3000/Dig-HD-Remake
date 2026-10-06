# Prosjektminne

Faste fakta og beslutninger. Oppdateres når noe endrer seg.

## Mål
- HD-versjon av The Dig (LucasArts, 1995, SCUMM v7): HD-bakgrunner, HD-sprites, HD-mellomsekvenser.

## Spillfilene
- Original på Google Drive, mappe `1INroCLSVZQLhwsFeTmPuMFrF9ukyueEj` (under Arcade). Engelsk standardutgave, data bygget 7. nov 1995.
- Kopi i grenen `spilldata` (DIG.LA0, DIG.LA1, VIDEO/). Hentes med `tools/hent_spilldata.sh`. Repoet må være privat så lenge grenen finnes.
- DIG.LA0 MD5 `d8323015ecb8b10bf53474f6e6b0ae33`. DIG.LA1 SHA-256 `8f2a0474dfe2d99c37b8182b08d8bb79afe95388df5c9d608ae3bb267536a957`.
- DIGMUSIC.BUN og DIGVOICE.BUN er over GitHubs grense og ligger bare på Drive.
- Spillfiler og alt laget fra dem (work/, mods/) skal aldri inn i main.

## Omfang (målt)
- 111 rom (27 brede, 11 høye), 61 med z-plan, 21 med flere paletter, 52 med fargesykling.
- 642 objektbilder, 331 kostymer med 28 490 ruter (kodek 1: 182, kodek 5: 144, kodek 16: 5), 55 SAN med 12 638 rammer.
- Romliste: `docs/rom-oversikt.csv`.

## Teknisk oppsett
- Motor: ScummVM med patchen i `engine/patches/`, låst til commit i `engine/SCUMMVM_COMMIT`. Spillet går i 8 bit internt. DigHD bygger HD-bildet i siste steg.
- HD-kilder per piksel: bakgrunn (lik i begge buffere og lik `_idx`-bildet), objekt (lik objekt som nettopp er tegnet), kostymerute (forskjellig fra bakgrunnsbufferen og innenfor en tegnet rute), ellers originalpikselen.
- Mod-mappe: `rooms/roomNNN(.png|_idx.png)`, `objects/objNNN_SS(.png|_idx.png)` (SS heksadesimalt), `costumes/costumeCCC_NNN(.png|_idx.png)`, `san/FILM/NNNNN.png`. Skala 4.
- Kostyme-ID = DCOS-katalogens ID, ikke rekkefølgen i LA1.
- Kostymefarger: RGBS-blokken i AKOS har de ekte fargene. thedig-textures sin egen PNG-eksport av kostymer har svart palett og brukes ikke.
- SAN-rammenummer: filnavn = SmushPlayer `_frame - 1`.
- Fargesyklede palettindekser vises som originalpiksler.
- Pipeline: `dighd` (Python 3.12+, Pillow, thedig-textures låst til commit 1cf355e).

## Åpne valg
- Stil: trofast HD (A) eller ny tegnestil som konseptbildene (B). Anbefalt: bygg A først, test B på Boston Low (kostyme 14 i rom 7) og ett rom.

## Annet
- Grafikkpilot 6. oktober 2026: to romkandidater (9 og 22) i 1280x800, native SDL2/Wayland/OpenGL-kjøring med 32-bits farger. Stil er foreløpig. Pakken ligger i privat grafikkdatagren `grafikkdata/pilot-20261006`, commit `cf8e6a9f6e30d662f7c73076ef1e1810851ceceb`; `tools/hent_grafikkpilot.sh` henter og kontrollerer den uten å skrive over endrede filer.
- Boston Low-prøven er bare stilreferanse. Alfasilhuetten avviker fra kostyme 14 rute 1 og den er ikke i mod-mappen. Manuell okklusjon, objektbytte og hele brukerreisen er ikke verifisert for nye rombilder. Se `docs/GRAFIKKPILOT.md`.
- Konseptbildene i roten av repoet er laget av en Reddit-tegner (signert). Brukes som stilreferanse. Spør og krediter før noe vises offentlig.
