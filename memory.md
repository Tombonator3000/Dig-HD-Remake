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
- Dig-HD-Web skal ha de samme filene som `main` for `engine/pages`, patchen, `engine/SCUMMVM_COMMIT`, byggeskriptene og `docs/PAGES.md`. Endres noe av dette, kopieres det dit og pushes; Actions bygger motoren og publiserer. 16. oktober 2026: nettlesermotoren bygger lokalt med Emscripten 4.0.10, inkludert VP8; dekodertesten i WebAssembly og avspilling i Chromium er kontrollert. Actions bygger og kontrollerer også PR-ene.
- Beslutning 9. oktober (Tom): nettsiden skal gå rett inn i spillet som originalen, uten oppsettside eller knapper rundt spillet. HD eller originalgrafikk velges i spillets egen meny. Derfor: lesenøkkel (fin-kornet, bare Contents read på Dig-HD-Remake) første gang, så hentes filene fra `spilldata` og `hd-mod` via api.github.com og lagres etter blob-ID. Mapper på maskinen er reserve. `?ny-nokkel` ber om ny nøkkel.
- Musikk og tale: DIGMUSIC.BUN og DIGVOICE.BUN i deler på 90 MB i `spilldata` (`NAVN.BUN.001` osv.), sjekksummer for de hele filene i `game/SHA256SUMS.lyd`. Kilden er Drive-mappen (delt med lenke). Nettsiden og `hent_spilldata.sh` setter dem sammen.
- Berøring i nettleseren: `engine/pages/touch.mjs` tar over all berøring (ScummVMs egen er da ute). Tom vil ikke at skjermen snus til liggende.
- Linux-pakken: `tools/pakke_linux.sh` og `.github/workflows/linux.yml` lager `TheDigHD-x86_64.AppImage` (Ubuntu 22.04, linuxdeploy, appimagetool) og legger den i releasen `linux`. Tom ville ha Linux først; Windows og Android senere. Arbeidsflyten bygger hver natt bare når `hd-mod` er endret (sammenligner med `hd-mod: <sha>` i notatene).
- Linux-utgave 16. oktober 2026 (r16): kode e71da0d4, hd-mod cb4415a9, AppImage 1 779 378 680 byte med alle 55 HD-filmer (109,43 MB VP8/IVF, ingen PNG-videorammer). SHA-256 8ab662f44fc1b25c4f1006741baec10f2da8dfcc5da3bfb4babf5da6cf4e0d90. Motorkilden og byggeoppskriften ligger separat som TheDigHD-Linux-kildekode.tar.gz i samme release, sammen med sjekksummer og kontroll-linux.json.
- thedig-textures (digart, dekoderne bak `dighd extract`): CI fikk ikke klonet det 9. oktober ("could not read Username"), men repoet finnes. Det er nå ekstraen `uttrekk` i pipeline, så CI går uten. En verifisert kopi ligger i /home/claude/.venv-dig (commit 1cf355e, GPL-3.0-or-later). Tom sa ja til en kopi i repoet, men sikkerhetskontrollen stoppet det; ikke nødvendig så lenge dekoderne er valgfrie.
- Nettsiden på PC: første start laster ned 530 MB (lyd, spill, intro) før noe vises; nedlastingsbilde. Fullskjerm ved første klikk eller tast. Uten WebGL: `--gfx-mode=surfacesdl`.
- Menyvalget: raden HD Graphics i originalmenyen (`gfx_gui.cpp`, kontroll 25), lagres som `dighd_classic` i `[scummvm]` (et spill startet fra kommandolinjen uten mål har ingen lagret spillseksjon).
- Nettleser: `./spill.sh --nettleser` bygger WebAssembly-versjonen (Emscripten 4.0.10 i `engine/emsdk`, kilde i `engine/scummvm-web`) og serverer den bare på 127.0.0.1:8000. Aldri på en åpen adresse (Disney/Lucasfilm).
- Spille fra repoet: `./spill.sh` (valg `--rom N`, `--klassisk`, `--gult`, `--auto`, `--fort`, `--programvare`). Testliste i `docs/SPILLTEST.md`.
- SAN-rammenummer: filnavn = SmushPlayer `_frame - 1`.
- 16. oktober 2026 (Tom): komprimert HD-video og oppstartsintroen skal inn via PR. `san/SQ1.ivf` er VP8, 3772 bilder i 1280 x 800, 12 fps, 22 775 540 byte etter AnimeSR v2. SAN styrer fortsatt timing, lyd og tekst. Video velges før PNG, med tilbakefall til PNG/original. Filmen ligger bare i datagrenen; motoren og Dig-HD-Web får samme støtte. Se `docs/HD-VIDEO.md`.
- Fargesyklede områder i HD-bakgrunner og HD-objekter: forholdet mellom nåværende og opprinnelig farge interpoleres med kvadratisk B-spline fra 3 x 3 originalpiksler og ganges inn i HD-pikselen. På figurer er syklede farger originalpiksler.
- Tekst i HD: tegnsettene i DIG.LA1 (`CharsetRendererV7`) og NUT-fontene i filmene melder hver glyf til DigHD, som tegner en xBR-skalert glyf. `DIGHD_TEXT` = xbr (standard), scale4x, nearest eller off.
- Motor: Ctrl+H bytter HD og klassisk, Ctrl+Shift+H viser gult felt der HD mangler. `DIGHD_CLASSIC=1`, `DIGHD_SHOW_MISSING=1`, `DIGHD_TEST_KEYS=ramme:tast,...` for test uten skjerm. Binær her: /home/claude/scummvm.
- Fra 10. oktober får Claude ikke flette sine egne PR-er herfra (stoppet av sikkerhetskontrollen). Tom fletter når CI er grønn.
- `DIGHD_TEST_KEYS` tar a til z, 0 til 9, f1 til f12, space og escape, så Alt+1 (lagre) og Ctrl+1 (laste) kan testes uten skjerm.
- Kostymer i romdrakt (funnet 10. oktober i rom 4): 1 Boston Low, 2 Maggie Robbins, 3 Ludger Brink. 7 er Pig (atomsprengladningen, «flying pig»). 22 og 23 er trolig Brink og Maggie (samme ruter og mål som 3 og 2).
- Robotarmen på romfergen er kostyme 4 og 5 (kodek 5, rom 2). Hovedark for hovedpersonene, Pig og armen bestilt hos Codex 11. oktober (`hovedark/` i gpt-arbeid); Tom godkjenner dem.
- Uten dekoderne lager `tools/ruteindeks.py` manglende indeksbilder for myke ruter fra originalrutene og kostymets eksisterende indeksbilder. Ikke for kostymer der fargetabellen har like farger med ulik indeks (229).
- Inventaret er blast-objekter (ruten 627 med skyggemodus 3, ikonene oppå). Motoren bygger det mørknede i HD og mørkner det (`beginBlast`/`endBlast`).
- The Dig HD avslutter aldri rett til skrivebordet: alt som ber om å avslutte, åpner spillets meny; Quit der avslutter (Tom 10. oktober).
- `myke-figurer` versjon 2: hver rute tilpasses originalens omriss i bredde og høyde (FIT_RANGE 12 prosent), så figurene holder størrelse og form gjennom rutene. Avviste ark i `docs/gpt-avvisninger.csv` tas ikke inn.
- Uten dekoderne kan originalrutene lages fra `original_1x.png` og `rekt` i jobbmappene i `gpt-arbeid` (gjort 10. oktober for å lappe modden).
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

## Neste spill
- Fremgangsmåten for HD-utgaver av andre SCUMM-spill er samlet i skillen `scumm-hd-remake` (foreslått 9. oktober). Tom planlegger Zak McKracken og Sam & Max. Dette repoet er referansen skillen peker til.
- På Toms Drive: Zak McKracken FM-Towns i mappen `Zak-fm` (id 1C4-aa3j3Jgso3Z2J00UYS3lfvNcxl4-Z, LFL-filer og CD-lyd som FLAC, engelsk etter størrelsen på 00.LFL) og Sam & Max CD i mappen `samnmax` (id 1ZWXP2NLg9FzADXZ5G37HlkYGtoSKvHih, med MONSTER.SOU). Ikke delt med lenke 9. oktober.
- Beslutning 9. oktober (Tom): Zak og Sam & Max tas når The Dig er ferdig. Planen da: ett felles offentlig kode-repo (Dig-HD-Remake med nytt navn, for eksempel LucasArts-HD) med patchen, pipelinen, verktøyene, én nettside med spillvalg og Linux-pakken, og ett datarepo per spill (spillfiler, hd-mod, arbeidsbordet til Codex), helst privat. Om Claude kan opprette nye repoer herfra, er ikke prøvd (Dig-HD-Web ble laget av Codex); ellers lager Tom tomme repoer. Mappene på Drive må deles med lenke først.

## Åpne valg
- Ingen for figurstilen: den glatte stilen er valgt for hovedpersonene. Resten av kostymene er ikke bestilt.

## Annet
- Grafikkpilot 6. oktober 2026: to romkandidater (9 og 22) i 1280x800, native SDL2/Wayland/OpenGL-kjøring med 32-bits farger. Stil er foreløpig. Pakken ligger i grafikkdatagrenen `grafikkdata/pilot-20261006`, commit `cf8e6a9f6e30d662f7c73076ef1e1810851ceceb`; `tools/hent_grafikkpilot.sh` henter og kontrollerer den uten å skrive over endrede filer.
- Boston Low-prøven er bare stilreferanse. Alfasilhuetten avviker fra kostyme 14 rute 1 og den er ikke i mod-mappen. Manuell okklusjon, objektbytte og hele brukerreisen er ikke verifisert for nye rombilder. Se `docs/GRAFIKKPILOT.md`.
- Konseptbildene i `docs/konsept/` (flyttet fra roten 6. oktober) er laget av en Reddit-tegner (signert). Brukes som stilreferanse. Spør og krediter før noe vises offentlig.
- Teksten tegnes med Exo 2 (SIL OFL 1.1) fra 9. oktober (Tom: "bruk exo2"). Skriften ligger i `pipeline/dighd/skrifter/exo2/`, modden får `fonts/map.txt`, `fonts/exo2.png` og `fonts/exo2.txt`. Bokstaven får høyden til originalboksen og skriftens egen bredde (ganger 1,2 for sideforholdet).
- Tom har laget repoene `Tombonator3000/Sam-Max-HD` og `Tombonator3000/ZakMcKracken-HD` (9. oktober) til de to neste spillene. Brukes når The Dig er ferdig, etter planen over.
- Bestilling 9. oktober (Tom): alle de andre figurene bestilles nå. Filmene (SAN) venter til senere, Tom kan ikke skalere dem opp nå.


## Arbeidsmetode 10. oktober 2026
- Tom ba om at erfaringene fra DOTT og Monkey Island-remasterne ble lagt i dette repoet for videre arbeid. `docs/HD-REMASTER-METODE.md` samler kilder, gjennomgang av dagens mottak og prioritert forbedringsplan.
- Dette er dokumentasjon og forslag, ikke ny kode eller nye godkjenningsstatusverdier. Godkjent glatt figurstil, ekte alfa, Exo 2 og utsatte filmer beholdes. Teknisk mottak skal skilles fra visuell godkjenning i videre rapportering.

## Kildetro grafikk og design (12. oktober 2026)
- Tom ba om samme regel i remake-skillen i Dig, Sam & Max og Zak: avklar motiv, funksjon, palett, figuridentitet og design fra riktig originalkontekst før grafisk HD-arbeid, også stilpilot.
- Skillen ligger i `docs/skills/scumm-hd-remake/SKILL.md`. Den er koblet fra AGENTS, remastermetoden, bestillingen og malen for grafikkgrenen. Spillets egne stilvalg gjelder; Dig sine figurer og materialer er ikke designfasit for de andre spillene.
- Rett påviste feil i produksjonsgrunnlaget før generering. Beskyttede jobbfiler beholdes; korrigert prompt og kildebegrunnelse leveres i et separat notat.
- Visuell kontroll av mening, identitet og hele animasjoner i spillet kommer i tillegg til teknisk mottak. Innført regel er ikke bevis for at alle ressursene er analysert eller spilltestet.
- Deling (13. oktober 2026): Tom tillater at grafikk og annet fra spillet deles utenfor repoet til hans eget private bruk (egne enheter, private steder). Spillfilene og det som lages fra dem holdes fortsatt utenfor `main`.
- Releaser (15. oktober 2026): Tom sier releasene kan ha spillgrafikk og hele spillet, «drit i det». Linux- og Windows-pakken i releasene `linux` og `windows` er offentlige fordi repoet er offentlig. Nettsiden på Pages har fortsatt ingen spillgrafikk.

## Spillfunn 13. oktober 2026
- Inventory-feilen i lagring5 skyldes xstart416 som ble klippet mot pitch328. Bufferforskyvning og synlig vindu er forskjellige størrelser i SCUMM.
- Kostyme75 i luftslusen er en skyggemaske. Kostyme35 i canyon er lys/energi, ikke fysisk klær. Krystallformene i nærbildet er kostyme286 til289; orange matte er ikke steinramme.
- Teknisk kontroll og grafikkleveranser fra denne runden: docs/HD-RETTINGER-20261013.md. Tom har ikke visuelt godkjent hele serien.

## Dekningsmasker og luftsluse (r12-kandidat 13. oktober 2026)
- Valgfri `objects/objNNN_SS_mask.png` angir eksakt SMAP-dekning, inkludert ugjennomsiktig svart i blandede striper. Den beholdes som originaloppløsning i modpakken.
- Aktive objekter med eksakt maske kan få forrang ved lik indeks med rommet. Uten maske beholdes tidligere romprioritet. Palettmasker bevarer HD-figuren under luftsluseglasset.
- Kilde og begrensninger: `docs/HD-RETTINGER-r12-20261013.md`. Dette er kandidatstatus, ikke bekreftelse på en publisert pakke eller Toms visuelle godkjenning.

## Overstyringer fra Codex (r11 og r12, funnet 15. oktober 2026)
- Codex leverte r11 og r12 (13. oktober) som filer lagt oppå en vanlig modbygging: `gpt-arbeid/rapporter/spillfeil-20261013/mod-overrides` (manifest `MOD-OVERRIDES.json`) og `gpt-arbeid/rapporter/spillfeil-r12-20261013/mod-overrides` (manifest `OVERSTYRINGER-MANIFEST.json`, legges på med `verktoy/apply-overrides.py <modmappe>`). Den publiserte `hd-mod` 05179ed er fasit: 28 472 filer, hash for SHA256SUMS c7b650b0 (`MOD-FROZEN.json` i r12-mappen).
- `tools/gpt_runde.sh` kjenner ikke overstyringene. Den sletter `mods/gpt`, bygger på nytt fra `work/gpt-ferdig` og tvangspusher til `hd-mod`. Uten retting fjerner neste runde med noe nytt godkjent r11- og r12-rettingene, og nettsiden og nattbygget av Linux-pakken henter det som ligger i `hd-mod`.
- Rettet 15. oktober: runden fletter kandidaten inn i den publiserte modden (`dighd flett-mod`). Bare enheter som ikke er publisert, legges til; publiserte byttes bare med `--erstatt` og tas ut med `--fjern`. `tools/mod_gren.sh send` henter sjekksummene til den publiserte (bare trærne, i en egen tom git-mappe) og stopper ved tap eller endring som ikke står i `mod.json` (`runder`). `--tving` bare etter Toms ord. Prøvd på den ekte r12-modden: 25 sekunder for 1,2 GB, alle publiserte filer urørt.

## Lista over det som vises uten HD (15. oktober 2026)
- Motoren skriver alt som står på skjermen som originalpiksler fordi HD mangler, til `dighd-uten-hd.txt` i lagringsmappen (Linux-pakken: `~/.local/share/the-dig-hd/saves/`). Én linje per bilde og rom: type (rute, objekt, rom, film), id som i modden, rom, bilder, piksler, sett først. Standard på; `DIGHD_MANGLER=0` slår av. Leses inn igjen ved start, så den vokser over flere økter.
- Svart og rom 0 telles ikke, og ingenting i klassisk grafikk. Det som er originalt med vilje, telles ikke (samme regler som gult felt).
- `dighd mangler FIL` gir oversikten per kostyme med navn fra `docs/figurer.csv`, sortert etter hvor mye det ble vist. Dette er grunnlaget for å bestille det som faktisk synes, i stedet for alle 10 158 rutene i tellingen fra spillfilene.
- Testkroken `DIGHD_TEST_ROOM` alene setter ingen figurer i rommet. Bruk `DIGHD_TEST_COSTUME` for å teste figurer.
- Dekoderne (thedig-textures) kan heller ikke hentes fra Claudes skyøkt (15. oktober, «could not read Username»), så `engine/test.sh` med nearest-modden går ikke her. Motorendringer testes da med den ekte modden og `DIGHD_VERIFY=1`.

## Felles motorpatch med Sam-Max-HD (15. oktober 2026)
- `engine/patches/0001-dighd-hd-grafikk.patch` er den samme i Dig-HD-Remake og Sam-Max-HD. Det som gjelder bestemte kostymer, objekter eller rom i ett spill, sperres med `_vm->_game.id` (`GID_DIG`, `GID_SAMNMAX`) eller `_game.version`.
- Endrer noen patchen i ett repo, må den kopieres til det andre eller slås sammen tre-veis (felles base: forrige felles patch). Beskrivelse i `docs/HD-MOTOR.md`, «Felles patch med Sam & Max».


## Hovedark godkjent 15. oktober 2026
- Tom svarte «2:godkjent.» på vurderingen av hovedarkene for Boston, Maggie, Brink og robotarmen. Alle fire er godkjent som referanser for videre grafikkarbeid.
- Godkjenningen er bundet til SHA-256 for eksisterende bilder i `gpt-arbeid/rapporter/hovedark-20261012/GODKJENNING.md` og registrert i leveranse.json. Bruk riktig hovedark som bilde to i nye figurjobber.
- Dette godkjenner ikke alle animasjonsruter, r12-pakken eller full gjennomspilling. Tidligere Pig-godkjenning beholdes.

## HD-filmer 16. oktober 2026
- Tom ba om å sette opp resten av videoene for HD i rekkefølge. Alle 54 resterende er produsert, 8866 nye rammer, 86 659 409 byte. Med SQ1: 55 filmer, 12 638 rammer og 109 434 949 byte video. PR 60 mot hd-mod, med alle tidligere grafikkfiler bevart og ingen nye PNG-videorammer.
- SQ3 er 14 fps, SQ19A 15 fps, resten 12. SQ14SC07 har en tom første SAN-ramme; denne beholdes for å unngå forskyvning. AnimeSR FP32, 8 oppvarmingsrammer per klipp, avgrenset skrivekø på 6 CPU-rammer. SQ5 bruker den tidligere godkjente masteren.
- Alle nye rammer er lest med motorens dekoder i RGB32; de første fem per film i RGB565. Repetisjon/bakoverhopp og nettleserfilter er kontrollert. Kompresjons-SSIM minst 0,98 etter omkoding av sju effektsekvenser. Full visuell kontroll i bevegelse og i alle spilltilstander gjenstår; Linux-pakken må bygges på nytt etter fletting. Se docs/VIDEO-PRODUKSJON.md.

## Grafikkfeil 16. oktober 2026
- Gjenoppstandelsen med solbriller er kostyme67. Boston ved vannets gjenoppliving er kostyme103; dets RGBS er en plassholder-hudrampe. Originalen bruker AKPL i rom32 palett0. Hovedarkene er fortsatt stilfasit.
- Skjelettets puslespill er rom36/kostyme121. Originalens silhuetter og ledd må styre registreringen. Tekniske palettmasker skal ikke inngå som malt figur i histogrammet for HD-fargetilpasning.
- Sonden i energikammeret bruker kostyme78 til83; mørk kropp må være ugjennomsiktig. Engraved rods er objekt633,634,636,652 og678, med både myke HD-bilder og reservebilder.
- Den lokale rettingskandidaten og nye patch0006 er dokumentert i docs/HD-RETTINGER-20261016.md. Ikke en ny publisert AppImage eller visuell godkjenning av alle nye ruter.
- Alle nye rammer er lest med motorens dekoder i RGB32; de første fem per film i RGB565. Repetisjon/bakoverhopp og nettleserfilter er kontrollert. Kompresjons-SSIM minst 0,98 etter omkoding av sju effektsekvenser. Full visuell kontroll i bevegelse og i alle spilltilstander gjenstår. PR 60 er flettet av Tom; Linux-bygg 38880540065 har alle 55 filmene og er kontrollert med SHA-256, alle modfiler, Debian 12 og 550 skjermoppdateringer med tekst og HD/klassisk-bytte. Se docs/VIDEO-PRODUKSJON.md.

## Integrert r16 og Linux-pakke, 16. oktober 2026

PR61,62,63 og nettleser-PR5 er flettet. Publisert Linux-AppImage fra e71da0d4/cb4415a9 har alle2223 rettinger og alle55 filmer. Nedlastet pakke, mod-sjekksummer og 550 oppdateringer er kontrollert, null avvik i fem fullnytegningskontroller. Full gjennomspilling og visuell godkjenning av alle ruter gjenstår. Fem nye funn behandles i neste grafikkrunde.

- 16. oktober 2026, r18: Tom bekrefter at siste feilbilder er fra ny AppImage. Avviste HD-bilder brukes aldri som designanker. Separate måner148/149 og laser233/234/235 bruker faktisk rompalett via AKPL, ikke RGBS-råfarger. Tram-skjermbildet i siste serie er rom80. R17/r18 er flettet: PR64 til hd-mod4a0ab61e, PR65 til maindcc09e3f og nettleser-PR6 til mainb8ea79ba. Ny Linux-pakke bygges automatisk; publisering og pakketest rapporteres separat.

## R19 integrasjon og Linux, 17. oktober 2026

- Tom ba om integrasjon, pull og ny distro av den produserte restgrafikken. Data-PR66 er flettet til hd-mod630cadb3ebb398ac8ade1f4e1ea759f8a783cd5a. Grafikkgrunnlag f5a23834 i gpt-arbeid; rapport rapporter/restgrafikk-r19-20261016.
- Modden legger til 14 173 filer med 7 097 HD-ruter, inkludert små tekniske fragmenter og kontrollert gjenbruk. Bare to dokumenterte Maggie-bilder erstattes. Ingen tidligere ressurser eller55 HD-filmer mistes. Omtrent6232 faktiske bilder og gjennomgang av eldre figurfeil gjenstår; all grafikken er ikke ferdig.
- Linux-bygg39027347179 er grønt, kode c2c9b8e0. AppImage på 2 123 475 448 byte, SHA25647b04c1bc468cb4dccd35cc33a6241504ea0cefaac6b87d144cd963c652c9b7a. Faktisk nedlastet fil kontrollert mot SHA-fil og GitHub-digest, alle 44 551 mod-manifestfiler og opprinnelig LA0/LA1.
- Standard AppRun: intro, tekst, HD/klassisk over 550 oppdateringer, fem kontroller med null omtegningsavvik. Pakkens egne figurtester: Brink 15, Maggie 52, kapsel 30, rotte 37 HD-ruter, alle bestått. Tvungen surfacesdl/vindusoppstart feilet lokalt før spillinitialisering med hodeløs SDL; dette er separat fra standardoppstarten som består. Ingen vanlige lagringer er endret.
- GPL-kildearkivet i releasen var fra r16 og manglet patch 0007. Oppdatert eksakt patchet kilde og oppskrift uten spilldata/HD:262499909 byte, SHA256b3d35f9ac36c6e227426bb9044317797a01e04c1e5db23f78f8206f675826dfd. Se kontroll-linux.json i releasen.

## 2026-10-17, r20 under arbeid

- Grafikkrapport rapporter/restgrafikk-r20-20261017 i gpt-arbeid: 221 nye HD-ruter, 196 registrerte Nexus-faser fra 91 malte referanseposer og 25 selvstendig tegnede canyon-ruter i costume034 etter alle tre godkjente hovedark. Ingen publiserte ressurser endret. 442 rene filtillegg, 44 551 r19-manifestfiler og 55 filmer bevart.
- Alle 221 observert i native motorprøver; 561 fullomtegningskontroller etter oppstart uten avvik. Canyon-romhopp omdirigeres av de brukte lagringene; isolert rom23-prøve bruker beviselig samme karakterfarger som rom15. Naturlig scene og full gjennomspilling gjenstår.
- Eldre costume034_050 og 108 har feil personer/klær. De 100 tidligere HD-rutene i serien må gjennomgås, og det er ikke rettet ved å fylle de nye 25 manglene. Hele serien er fortsatt ikke visuelt ferdig.
- R20 er en arbeidskandidat, ikke integrert i hd-mod eller pakket. 6 011 faktiske bilder mangler i r20-listen, pluss eldre figurfeil. Restoppdraget og Toms visuelle godkjenning er fortsatt åpne.

## R21, canyon-figurer, 17. oktober 2026

- Kostyme34 har 130 fysiske ruter i arbeidskandidaten. R20 la til25; r21 tegner om de105 eldre. Forrige telling100 utelot125 til129 fra jobbinventaret; disse er faktisk brukt i motoren.
- Indeksbildenes palett brukes ved HD-fargetilpasning. Gamle RGBS-farger i costume34 gav rød hud/klær selv med riktig ny tegning. AKPL koblet gjennom rom15 palett0 retter dette, uten å endre noen fysiske indeksverdier.105 HD-bilder og105 indeksbilder er eksplisitte erstatninger.
- Alle130 vist i fire isolerte native animasjonsprøver,172 fullomtegningskontroller etter oppstart uten avvik. Etter siste108-retting er animasjon8 prøvd igjen, øvrige tilfeller videreført etter SHA-kontroll. Ikke naturlig canyon-gjennomspilling, ikke Toms nye godkjenning.
- Kandidat-r21 og grafikkgrenen inneholder arbeidet. Ingen ny integrering eller distro. R19 publisert, r20s221 tillegg og55 filmer bevart.6011 manglende faktiske bilder gjenstår, samt øvrige eldre feil.

## Integrert r20/r21 og Linux, 18. oktober 2026

- PR67 flettet til hd-mod29cff6583dc45ec21bcccb5da0eb16afafa379a5. Lokal hd-leveranse oppdatert; kjor-rettet-spill.sh bruker den.221 nye HD-ruter,105 omtegnede canyon-ruter og105 korrigerte indeksreferansepaletter.442 nye filer,210 eksplisitte erstatninger, ingen slettinger. Alle55 filmer bevart.
- Sammenføyd mod og nedlastet pakke: hver har11 native tilfeller med543 fullomtegningskontroller etter oppstart uten avvik. Alle196 nye Nexus-faser og130 canyon-ruter observert.44993 mod-manifestfiler og652 leveransefiler kontrollert. Naturlig gjennomspilling og Toms visuelle godkjenning er fortsatt ikke gjort.
- Linux-bygg39112677913 fra kode7b2f4398457adb34a3b9753102295a5b987d6252 er grønt, inkludert Debian12. AppImage 2140813816 byte, SHA256f6c9786ca4f0ebb5f980e1761c79151e643d68a619f7cb0c37aff7b5f3cbe326. Faktisk nedlasting og standard AppRun med intro/tekst/HD-bytte er kontrollert,550 oppdateringer og fem nytegningskontroller uten avvik.
- Motorkilder og oppskrift i det tidligere publiserte kildearkivet er uendret og kontrollert mot gjeldende fem patcher og motorcommit. Ingen ny motor-/pipelinekode.6011 faktiske bilder og andre eldre figurfeil gjenstår.
