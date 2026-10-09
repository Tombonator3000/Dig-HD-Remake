# memory.md

Faste fakta og beslutninger. Oppdateres når noe endrer seg.

## Mål
- HD-versjon av The Dig (LucasArts, 1995, SCUMM v7): HD-bakgrunner, HD-sprites, HD-mellomsekvenser.

## Spillfilene
- Original på Google Drive, mappe `1INroCLSVZQLhwsFeTmPuMFrF9ukyueEj` (under Arcade). Engelsk standardutgave, data bygget 7. nov 1995.
- Kopi i grenen `spilldata` (DIG.LA0, DIG.LA1, VIDEO/). Hentes med `tools/hent_spilldata.sh`.
- Repoet er offentlig siden 5. oktober. Tom spurte 9. oktober og valgte å la det være offentlig.
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
- Mod-mappe: `rooms/roomNNN(.png|_idx.png)`, `objects/objNNN_SS(.png|_idx.png)` (SS heksadesimalt), `costumes/costumeCCC_NNN(.png|_idx.png)`, `costumes/costumeCCC_NNN_hd.png` (myk rute med marg og egen alfa, brukes før den vanlige), `san/FILM/NNNNN.png`. Skala 4.
- Kostyme-ID = DCOS-katalogens ID, ikke rekkefølgen i LA1.
- Kostymefarger: kodek 1 fargelegges med RGBS-blokken i AKOS. Kodek 5 og 16 tegnes av ScummVM med kodene rett som palettindekser og fargelegges med rompaletten der kostymet vises (`docs/kostymefarger.csv`, ellers jevneste palett i hjemmerommet). thedig-textures sin egen PNG-eksport av kostymer har svart palett og brukes ikke.
- GitHub Pages: egen motor/nettside i det offentlige repoet Tombonator3000/Dig-HD-Web. Spillfilene og HD-pakken hentes fra spillrepoet og lagres i IndexedDB, aldri på nettsiden. `engine/build-pages.py` pakker bare motor, temaer og GPL-kildekode; `docs/PAGES.md` beskriver bygging og bruk. Codex laget dette etter Toms uttrykkelige Pages-oppdrag 9. oktober.
- Dig-HD-Web skal ha de samme filene som `main` for `engine/pages`, patchen, `engine/SCUMMVM_COMMIT`, byggeskriptene og `docs/PAGES.md`. Endres noe av dette, kopieres det dit og pushes; Actions bygger motoren og publiserer. Nettlesermotoren kan ikke bygges her (SDL3-porten til Emscripten lastes ned fra en adresse proxyen stopper), så den bygges og testes via Actions og den publiserte siden.
- Beslutning 9. oktober (Tom): nettsiden skal gå rett inn i spillet som originalen, uten oppsettside eller knapper rundt spillet. HD eller originalgrafikk velges i spillets egen meny. Derfor: lesenøkkel (fin-kornet, bare Contents read på Dig-HD-Remake) første gang, så hentes filene fra `spilldata` og `hd-mod` via api.github.com og lagres etter blob-ID. Mapper på maskinen er reserve. `?ny-nokkel` ber om ny nøkkel.
- Musikk og tale: DIGMUSIC.BUN og DIGVOICE.BUN i deler på 90 MB i `spilldata` (`NAVN.BUN.001` osv.), sjekksummer for de hele filene i `game/SHA256SUMS.lyd`. Kilden er Drive-mappen (delt med lenke). Nettsiden og `hent_spilldata.sh` setter dem sammen.
- Berøring i nettleseren: `engine/pages/touch.mjs` tar over all berøring (ScummVMs egen er da ute). Tom vil ikke at skjermen snus til liggende.
- Linux-pakken: `tools/pakke_linux.sh` og `.github/workflows/linux.yml` lager `TheDigHD-x86_64.AppImage` (Ubuntu 22.04, linuxdeploy, appimagetool) og legger den i releasen `linux`. Tom ville ha Linux først; Windows og Android senere. Arbeidsflyten bygger hver natt bare når `hd-mod` er endret (sammenligner med `hd-mod: <sha>` i notatene).
- thedig-textures (digart, dekoderne bak `dighd extract`): CI fikk ikke klonet det 9. oktober ("could not read Username"), men repoet finnes. Det er nå ekstraen `uttrekk` i pipeline, så CI går uten. En verifisert kopi ligger i /home/claude/.venv-dig (commit 1cf355e, GPL-3.0-or-later). Tom sa ja til en kopi i repoet, men sikkerhetskontrollen stoppet det; ikke nødvendig så lenge dekoderne er valgfrie.
- Nettsiden på PC: første start laster ned 530 MB (lyd, spill, intro) før noe vises; nedlastingsbilde. Fullskjerm ved første klikk eller tast. Uten WebGL: `--gfx-mode=surfacesdl`.
- Menyvalget: raden HD Graphics i originalmenyen (`gfx_gui.cpp`, kontroll 25), lagres som `dighd_classic` i `[scummvm]` (et spill startet fra kommandolinjen uten mål har ingen lagret spillseksjon).
- Nettleser: `./spill.sh --nettleser` bygger WebAssembly-versjonen (Emscripten 4.0.10 i `engine/emsdk`, kilde i `engine/scummvm-web`) og serverer den bare på 127.0.0.1:8000. Aldri på en åpen adresse (Disney/Lucasfilm).
- Spille fra repoet: `./spill.sh` (valg `--rom N`, `--klassisk`, `--gult`, `--auto`, `--fort`, `--programvare`). Testliste i `docs/SPILLTEST.md`.
- SAN-rammenummer: filnavn = SmushPlayer `_frame - 1`.
- Fargesyklede områder i HD-bakgrunner og HD-objekter: forholdet mellom nåværende og opprinnelig farge interpoleres med kvadratisk B-spline fra 3 x 3 originalpiksler og ganges inn i HD-pikselen. På figurer er syklede farger originalpiksler.
- Tekst i HD: tegnsettene i DIG.LA1 (`CharsetRendererV7`) og NUT-fontene i filmene melder hver glyf til DigHD, som tegner en xBR-skalert glyf. `DIGHD_TEXT` = xbr (standard), scale4x, nearest eller off.
- Motor: Ctrl+H bytter HD og klassisk, Ctrl+Shift+H viser gult felt der HD mangler. `DIGHD_CLASSIC=1`, `DIGHD_SHOW_MISSING=1`, `DIGHD_TEST_KEYS=ramme:tast,...` for test uten skjerm. Binær her: /home/claude/scummvm.
- Pipeline: `dighd` (Python 3.12+, Pillow, NumPy, SciPy, thedig-textures låst til commit 1cf355e som ekstra). CI kjører `pytest -m "not game"` på hver push og PR.

## HD-grafikk fra ChatGPT
- Roller: Claude koden, ChatGPT grafikken (bestilling i `docs/BESTILLING-CHATGPT.md`), Tom godkjenner.
- Valgt stil: trofast HD (samme motiv og farger, mer detalj). Ingen ny tegnestil i denne runden.
- Jobber: 1536 x 1024 lerret = 384 x 256 originalpiksler i 4x, grå kant (#808080), overlapp 64. 162 jobber for 106 rom.
- Arbeidsgren: `gpt-arbeid` (egen AGENTS.md laget fra `docs/gpt-arbeid-AGENTS.md`). Synk med `tools/gpt_gren.sh send|hent`. Codex lager også egne jobber der (fig015 og videre) som ikke står i `work/gpt/status.csv`.
- ChatGPT leser `ORDRE.md` i `gpt-arbeid` først. Claude skriver den hver runde (`dighd gpt-ordre`): avviste jobber først, så nye, så de som kan bli bedre, 10 om gangen.
- En runde = `tools/gpt_runde.sh`. Ferdig mod publiseres i grenen `hd-mod` (én commit som erstattes, med SHA256SUMS). Hentes med `tools/mod_gren.sh hent`.
- Pilot: rom 9 og 22 fra Codex, godkjent av Claude på vegne av Tom 6. oktober (forskyvning 0,73 og 0,25 px). Stilankere: `stil/room009_core.png` og `stil/room022_beach.png`.
- Store objektbilder (w*h >= 16000, w >= 200 eller h >= 150) er egne jobber `objNNN_SS`, 30 stykker. Rutenettene obj618 og obj627 (rom 93) er tatt ut. Objektnotater i `docs/gpt-romnotater.csv` med `objNNN` i kolonnen rom. Senere tilstander gjøres like den første der originalene er like (`match_state`).
- Mindre objektbilder: lagjobber `lagNNN_KK` (rommet med et sett objekttilstander på plass, klippes ut etterpå, godkjent HD-rom som bilde to) og ikonark `ikonNN` for inventaret. Kontroll per objekt i `gpt-inn` (mangler eller tegnet om).
- Figurer: figurark `figCCC_KK` (rutene i en animasjon på ett ark, klippes ut med originalens alfa). Hovedpersonene: Boston Low kostyme 14, Maggie Robbins 18, Ludger Brink 15 (varianter 16 og 17). `dighd gpt-pakke --figurer alle` eller en liste; standard er bare piloten.
- fig014_01 (Boston stående og gående, 28 ruter) godkjent av Tom 9. oktober og satt inn i modden, selv om ansiktet er litt yngre og mangler grått hår ved tinningene. Rutene klippes med originalens alfa, så kantene er trappete i 4x. Tom avviste trappekantene samme dag.
- Beslutning 9. oktober (Tom): Boston, Brink og Maggie med alle kostymevarianter i den glatte, detaljerte stilen med myke kanter (509 ark, Codex tegner). Ark 1 for Boston er `rapporter/boston-konsept-glatte-kanter-20261009/boston-28-ruter.png` og erstatter den gamle fig014_01.
- Glatte figurark: `gpt-inn` gir dem status levert og klipper dem ikke (`has_native_alpha`). `dighd myke-figurer` (pipeline/dighd/myk.py) tar dem inn fra `leveranser` i `rapporter/*/fremdrift.json` og rutekartene, skalerer per gruppe (animasjon, lag og rad på arket) til originalens høyde, plasserer etter best overlapp og skriver `_hd.png` med marg. Hodene er tegnet omtrent 35 prosent større enn kroppene og skaleres for seg. Motoren legger myke ruter over HD-bakgrunnen (docs/HD-MOTOR.md, Myke figurer).
- Kodeoppgaver til Codex står i `docs/gpt-kodeoppgaver.md` og kommer med i ORDRE.md. Rapporter i `rapporter/` i `gpt-arbeid`.
- Rom 22 i modden er piloten fra Codex. En senere leveranse ligger som `alternativ_forsok2.png` (bakken ble til vann).
- `gpt-inn` retter ytterrader der den grå lerretskanten har blødd inn (`repair_edges`, bare sider som grenser mot kanten).
- `gpt-inn` tar vare på beste godtatte leveranse per jobb i `work/gpt/beste/`. En ny leveranse som er dårligere, erstatter den ikke.
- Manuell avvisning etter gjennomsyn: `docs/gpt-avvisninger.csv` (jobb, sha256 for resultatet, grunn, forslag, status avvist eller sjekk). Sjekk beholder bildet i modden til et bedre kommer.
- Romtest i motoren: `tools/romtest.sh` (alle rom uten skjerm, rapport og kontaktark i work/romtest). Avviste bilder fjernes fra `work/gpt-ferdig`.
- Leveranse godtas som hele lerretet (1536 x 1024 med grå kant) eller bare bildet i utsnittets sideforhold (`detect_layout`).
- Godkjenning: forskyvning 0,75 px, blokker 1,0 px, kantlikhet 0,55 (sjekk: 1,5 / 2,0 / 0,40). Fargelås sigma 6, styrke 1.
- Erfaring fra Jones: ChatGPT bommer på tekst og plassering, og stilen ble skiftet flere ganger. Derfor pilot, stilankere, automatisk kontroll og sporing.

## Åpne valg
- Ingen for figurstilen: den glatte stilen er valgt for hovedpersonene. Resten av kostymene er ikke bestilt.

## Annet
- Grafikkpilot 6. oktober 2026: to romkandidater (9 og 22) i 1280x800, native SDL2/Wayland/OpenGL-kjøring med 32-bits farger. Stil er foreløpig. Pakken ligger i grafikkdatagrenen `grafikkdata/pilot-20261006`, commit `cf8e6a9f6e30d662f7c73076ef1e1810851ceceb`; `tools/hent_grafikkpilot.sh` henter og kontrollerer den uten å skrive over endrede filer.
- Boston Low-prøven er bare stilreferanse. Alfasilhuetten avviker fra kostyme 14 rute 1 og den er ikke i mod-mappen. Manuell okklusjon, objektbytte og hele brukerreisen er ikke verifisert for nye rombilder. Se `docs/GRAFIKKPILOT.md`.
- Konseptbildene i `docs/konsept/` (flyttet fra roten 6. oktober) er laget av en Reddit-tegner (signert). Brukes som stilreferanse. Spør og krediter før noe vises offentlig.
