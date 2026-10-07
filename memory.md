# memory.md

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
- Kostymefarger: kodek 1 fargelegges med RGBS-blokken i AKOS. Kodek 5 og 16 tegnes av ScummVM med kodene rett som palettindekser og fargelegges med rompaletten der kostymet vises (`docs/kostymefarger.csv`, ellers jevneste palett i hjemmerommet). thedig-textures sin egen PNG-eksport av kostymer har svart palett og brukes ikke.
- Nettleser: `./spill.sh --nettleser` bygger WebAssembly-versjonen (Emscripten 4.0.10 i `engine/emsdk`, kilde i `engine/scummvm-web`) og serverer den bare på 127.0.0.1:8000. Aldri på en åpen adresse (Disney/Lucasfilm).
- Spille fra repoet: `./spill.sh` (valg `--rom N`, `--klassisk`, `--gult`, `--auto`, `--fort`, `--programvare`). Testliste i `docs/SPILLTEST.md`.
- SAN-rammenummer: filnavn = SmushPlayer `_frame - 1`.
- Fargesyklede områder i HD-bakgrunner og HD-objekter: forholdet mellom nåværende og opprinnelig farge interpoleres med kvadratisk B-spline fra 3 x 3 originalpiksler og ganges inn i HD-pikselen. På figurer er syklede farger originalpiksler.
- Tekst i HD: tegnsettene i DIG.LA1 (`CharsetRendererV7`) og NUT-fontene i filmene melder hver glyf til DigHD, som tegner en xBR-skalert glyf. `DIGHD_TEXT` = xbr (standard), scale4x, nearest eller off.
- Motor: Ctrl+H bytter HD og klassisk, Ctrl+Shift+H viser gult felt der HD mangler. `DIGHD_CLASSIC=1`, `DIGHD_SHOW_MISSING=1`, `DIGHD_TEST_KEYS=ramme:tast,...` for test uten skjerm. Binær her: /home/claude/scummvm.
- Pipeline: `dighd` (Python 3.12+, Pillow, NumPy, thedig-textures låst til commit 1cf355e). CI kjører `pytest -m "not game"` på hver push og PR.

## HD-grafikk fra ChatGPT
- Roller: Claude koden, ChatGPT grafikken (bestilling i `docs/BESTILLING-CHATGPT.md`), Tom godkjenner.
- Valgt stil: trofast HD (samme motiv og farger, mer detalj). Ingen ny tegnestil i denne runden.
- Jobber: 1536 x 1024 lerret = 384 x 256 originalpiksler i 4x, grå kant (#808080), overlapp 64. 162 jobber for 106 rom.
- Arbeidsgren: `gpt-arbeid` (privat, egen AGENTS.md laget fra `docs/gpt-arbeid-AGENTS.md`). Synk med `tools/gpt_gren.sh send|hent`.
- ChatGPT leser `ORDRE.md` i `gpt-arbeid` først. Claude skriver den hver runde (`dighd gpt-ordre`): avviste jobber først, så nye, så de som kan bli bedre, 10 om gangen.
- En runde = `tools/gpt_runde.sh`. Ferdig mod publiseres i grenen `hd-mod` (én commit som erstattes, med SHA256SUMS). Hentes med `tools/mod_gren.sh hent`.
- Pilot: rom 9 og 22 fra Codex, godkjent av Claude på vegne av Tom 6. oktober (forskyvning 0,73 og 0,25 px). Stilankere: `stil/room009_core.png` og `stil/room022_beach.png`.
- Store objektbilder (w*h >= 16000, w >= 200 eller h >= 150) er egne jobber `objNNN_SS`, 30 stykker. Rutenettene obj618 og obj627 (rom 93) er tatt ut. Objektnotater i `docs/gpt-romnotater.csv` med `objNNN` i kolonnen rom. Senere tilstander gjøres like den første der originalene er like (`match_state`).
- Mindre objektbilder: lagjobber `lagNNN_KK` (rommet med et sett objekttilstander på plass, klippes ut etterpå, godkjent HD-rom som bilde to) og ikonark `ikonNN` for inventaret. Kontroll per objekt i `gpt-inn` (mangler eller tegnet om).
- Kodeoppgaver til Codex står i `docs/gpt-kodeoppgaver.md` og kommer med i ORDRE.md. Rapporter i `rapporter/` i `gpt-arbeid`.
- Rom 22 i modden er piloten fra Codex. En senere leveranse ligger som `alternativ_forsok2.png` (bakken ble til vann).
- `gpt-inn` tar vare på beste godtatte leveranse per jobb i `work/gpt/beste/`. En ny leveranse som er dårligere, erstatter den ikke.
- Manuell avvisning etter gjennomsyn: `docs/gpt-avvisninger.csv` (jobb, sha256 for resultatet, grunn, forslag). Avviste bilder fjernes fra `work/gpt-ferdig`.
- Leveranse godtas som hele lerretet (1536 x 1024 med grå kant) eller bare bildet i utsnittets sideforhold (`detect_layout`).
- Godkjenning: forskyvning 0,75 px, blokker 1,0 px, kantlikhet 0,55 (sjekk: 1,5 / 2,0 / 0,40). Fargelås sigma 6, styrke 1.
- Erfaring fra Jones: ChatGPT bommer på tekst og plassering, og stilen ble skiftet flere ganger. Derfor pilot, stilankere, automatisk kontroll og sporing.

## Åpne valg
- Ny tegnestil som konseptbildene (B) er ikke valgt bort, men venter. Kan testes på Boston Low (kostyme 14) senere.

## Annet
- Grafikkpilot 6. oktober 2026: to romkandidater (9 og 22) i 1280x800, native SDL2/Wayland/OpenGL-kjøring med 32-bits farger. Stil er foreløpig. Pakken ligger i privat grafikkdatagren `grafikkdata/pilot-20261006`, commit `cf8e6a9f6e30d662f7c73076ef1e1810851ceceb`; `tools/hent_grafikkpilot.sh` henter og kontrollerer den uten å skrive over endrede filer.
- Boston Low-prøven er bare stilreferanse. Alfasilhuetten avviker fra kostyme 14 rute 1 og den er ikke i mod-mappen. Manuell okklusjon, objektbytte og hele brukerreisen er ikke verifisert for nye rombilder. Se `docs/GRAFIKKPILOT.md`.
- Konseptbildene i `docs/konsept/` (flyttet fra roten 6. oktober) er laget av en Reddit-tegner (signert). Brukes som stilreferanse. Spør og krediter før noe vises offentlig.
