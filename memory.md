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

## HD-grafikk fra ChatGPT
- Roller: Claude koden, ChatGPT grafikken (bestilling i `docs/BESTILLING-CHATGPT.md`), Tom godkjenner.
- Valgt stil: trofast HD (samme motiv og farger, mer detalj). Ingen ny tegnestil i denne runden.
- Jobber: 1536 x 1024 lerret = 384 x 256 originalpiksler i 4x, grå kant (#808080), overlapp 64. 162 jobber for 106 rom.
- Arbeidsgren: `gpt-arbeid` (privat, egen AGENTS.md). Synk med `tools/gpt_gren.sh send|hent`.
- Pilot: rom022, rom002_del1av3, rom028. Godkjente piloter blir stilankere i `stil/`.
- Godkjenning: forskyvning 0,75 px, blokker 1,0 px, kantlikhet 0,55 (sjekk: 1,5 / 2,0 / 0,40). Fargelås sigma 6, styrke 1.
- Erfaring fra Jones: ChatGPT bommer på tekst og plassering, og stilen ble skiftet flere ganger. Derfor pilot, stilankere, automatisk kontroll og sporing.

## Åpne valg
- Ny tegnestil som konseptbildene (B) er ikke valgt bort, men venter. Kan testes på Boston Low (kostyme 14) senere.

## Annet
- Konseptbildene i roten av repoet er laget av en Reddit-tegner (signert). Brukes som stilreferanse. Spør og krediter før noe vises offentlig.
