# todo.md

Det som gjenstår, viktigst først. Kryss av når noe er gjort, og logg det i `log.md`.

## Neste

- [x] GitHub Pages-inngang med lokal import av spillfiler og HD-pakke, uten lokal webserver
- [x] Bekreft den publiserte Pages-adressen med faktisk HD-oppstart
- [x] HD-figurer i Pages-versjonen: testet mot den publiserte siden, og siden teller HD-rom, objektbilder og figurruter
- [x] Rett inn i spillet fra Pages: ingen oppsettside eller knapper, lesenøkkel første gang, filene fra grenene ved behov
- [x] HD eller originalgrafikk i spillets egen meny (F5, HD Graphics), valget huskes
- [ ] Tom lager lesenøkkelen og spiller fra Pages på mobil og PC (`docs/SPILLTEST.md`, Fra GitHub Pages) og sier fra
- [x] Musikk og tale i nettleseren: delene i `spilldata` settes sammen, `?uten-lyd`
- [x] Berøring på mobil og nettbrett, ny henting ved nettfeil, ingen snuing av skjermen
- [ ] Mindre minne i nettleseren: `http-fs.cpp` legger hele filen i WebAssembly-minnet før den skrives til MEMFS; skriv rett til MEMFS (må bygges i Actions, SDL3-porten kan ikke hentes her)
- [x] Komplett nedlastingsfil for Linux: AppImage i releasen `linux`, bygget og testet av arbeidsflyten Linux-pakke, ny hver natt når `hd-mod` endres
- [x] PC-nettleseren: nedlastingsbilde første gang, fullskjerm ved første klikk, programvaretegning uten WebGL
- [ ] Tom tester nettsiden på Kubuntu igjen (første start tar tid: 530 MB)
- [ ] thedig-textures (dekoderne for `dighd extract`): CI fikk ikke klonet repoet, men det finnes. Tom sa ja til en kopi i repoet; sikkerhetskontrollen stoppet det. Ikke nødvendig så lenge dekoderne er valgfrie
- [ ] Tom tester Linux-pakken på laptopen (skjerm, lyd, fullskjerm, menyvalget)
- [ ] Nedlastingsfil for Windows og Android (etter Linux)

- [ ] ChatGPT-runder hver halvtime med `tools/gpt_runde.sh` til alle 192 jobber (162 rom, 30 store objekter) er godkjent
- [ ] Se gjennom hvert nytt godkjent rom i forhåndsvisningen før det rapporteres (avvis med `docs/gpt-avvisninger.csv`)
- [ ] Juster grensene i `gpt.py` etter de første 20 ekte leveransene
- [x] Kontroller de nye rommene i motoren (`tools/romtest.sh`, alle 111 rom, PR 18)
- [x] Objektbytte i romtesten (`DIGHD_TEST_OBJSTATE`, `tools/romtest.sh --objekter`, PR 21)
- [ ] Rom 10 og 104 i romtesten (spillet forlater rommet like etter hoppet)
- [x] Lys ytterrad i ChatGPT-bildene (grå kant som blør inn) rettes i `gpt-inn` med `repair_edges`
- [x] `./spill.sh` og `docs/SPILLTEST.md`: spille og teste rett fra repoet
- [ ] Tom tester med `./spill.sh` etter `docs/SPILLTEST.md` (eller Codex med kodeoppgave 1): masker, objektbytte, Ctrl+H og Ctrl+Shift+H

## ChatGPT-grafikk

- [x] Bestilling, jobbverktøy, kontroll og arbeidsgren `gpt-arbeid`
- [x] Pilot: rom 9 og 22 levert av Codex, kontrollert og godkjent, lagt i `stil/` som stilankere
- [x] Fast ordre i `ORDRE.md` og runde-skript (`tools/gpt_runde.sh`), mod publiseres i `hd-mod`
- [x] `GRAFIKKLISTE.md` med alt som skal lages, i 19 bestillinger, så ChatGPT kan jobbe videre uten å vente
- [ ] Resten av romjobbene (rom 32 på nytt, rom 50 og 88)
- [ ] Sømmer mot HD-rommet for obj343, obj347, obj355, obj547 og obj886 (sjekk, gjøres om med HD-rommet som bilde to)
- [x] Objektjobber for de 30 største objektbildene, med egne notater og like tilstander
- [x] De 30 objektjobbene
- [ ] Tom ser over stilen når 10 til 15 rom er ferdige
- [x] Bestilling runde 2 laget: 236 lagjobber og 3 ikonark for de mindre objektbildene (PR 16)
- [ ] Lagjobbene og ikonarkene fra ChatGPT
- [x] En dårligere ny leveranse erstatter ikke en godtatt (beste leveranse per jobb i `work/gpt/beste`)
- [x] Nettleserversjon lokalt: `./spill.sh --nettleser` (PR 15)
- [x] Figurark for kostymene og pilot for Boston Low (PR 20)
- [x] fig014_01 (Boston står og går, 28 ruter) godkjent av Tom og satt inn i modden
- [x] Pilotarkene fig014_02 til 04 fra ChatGPT (levert i glatt stil)
- [x] Glatt stil: `gpt-inn` klipper ikke ark med ekte alfa (PR 34)
- [x] Myke figurer i motoren og `dighd myke-figurer`: 148 ark, 2957 ruter
- [ ] Tom ser Boston, Brink og Maggie i spillet (nettsiden eller Linux-pakken) og sier om størrelse, fotfeste og stil stemmer
- [ ] Gå gjennom de 392 rutene med status sjekk i `myke.json` (omriss ulikt originalen, mest Brink og Maggie med smalere figur)
- [ ] Resten av hovedfigurene fra Codex (361 ark), tas inn av runden av seg selv
- [ ] Myke figurer: kant mot forgrunnen i 4 x 4-blokker; prøv å følge den myke kanten i HD-rommet
- [ ] Myke figurer på ekte skjerm: flere figurer over hverandre, skalerte figurer, banner og meny over, nedtoning
- [ ] Ansiktet til Boston nærmere originalen i de neste arkene (eldre, grått hår ved tinningene)
- [ ] Mykere kanter på HD-figurrutene: alfa jevnet ut innenfor originalens silhuett, i stedet for trappetrinn i 4x
- [ ] Lag Boston-ruter som består silhuettkontrollen og kontroller hele bevegelsesrekken i motoren

## Motor

- [x] Hurtigtast for å bytte mellom klassisk og HD (Ctrl+H)
- [x] Vis et gult felt der HD mangler (Ctrl+Shift+H)
- [x] Tekst over figurer uten HD ble gul med gult felt på (rettet i PR 10)
- [x] Undertekster over HD-filmrammer: teksten ligger over HD-rammen som originalpiksler
- [x] Kontroll av kodek 5 i spillet (fant og rettet at ingen ruter med kodek 5 fikk HD, og en krasj ved romskifte)
- [x] Farger i uttrekket for kodek 5 og 16: rompaletten der kostymet vises (PR 12)
- [x] HD-sprites for kodek 16 (5 kostymer, PR 12)
- [x] HD-tekst (xBR per glyf fra spillets egne fonter, PR 9)
- [x] HD-figur skinte svakt gjennom bannere og hovedmenyen (rettet i PR 10, merker per piksel)
- [ ] Tekst over et banner som tas bort, vises trolig som originalpiksler i én skjermoppdatering (ikke testet)
- [x] Fargesyklede områder i HD (fargekart med kvadratisk B-spline, PR 8)
- [ ] Spille av rene filmer som MP4/WebM i stedet for tusenvis av PNG-er
- [ ] Prøv en nyere ScummVM-commit og oppdater patchen

## Senere

- [ ] Stiltest med KI-oppskalering: fem rom gjennom Real-ESRGAN og en pikselkunstmodell (`dighd compare`, `--method realesrgan`)
- [ ] Stiltest: Boston Low (kostyme 14) i ny stil, hvis Tom vil prøve ny tegnestil
- [ ] Fyll inn prioritet i `docs/rom-oversikt.csv`
- [ ] Finn ut i skriptene hvilke SAN-filer som er rene filmer og hvilke som styres av spillet (NUTCracker eller descumm -7)
- [ ] Skript som lager hele HD-pakken lokalt fra brukerens egne spillfiler (for eventuell deling)

## Ferdig

- [x] Spillfilene fra Drive til grenen `spilldata`, med sjekksummer og hentescript
- [x] MD5 av DIG.LA0 sjekket (standardutgaven)
- [x] Uttrekk av rom, objekter, kostymer (med riktige farger) og filmrammer
- [x] Pipeline `dighd` med flere oppskaleringsmetoder og mod-mapper
- [x] ScummVM-patch: HD-bakgrunner, HD-objekter, HD-sprites, HD-filmrammer
- [x] Fargejustering ved palettbytte, fargesykling beholdt, mus og peker i HD
- [x] Byggeskript testet fra ren checkout, automatisk test uten skjerm
- [x] Grafikkpilot: rom 9 og 22 laget med ChatGPT-bildegeneratoren, kontrollert i native ScummVM med 32-bits farger og levert i privat grafikkdatagren
- [x] Boston Low-stilreferanse og kontroll av egne HD-filnavn, mål, indeks og alfasilhuett
- [x] Valgt stil: trofast HD
- [x] Repo ryddet: README, STATUS.md, AGENTS.md, konseptbilder i `docs/konsept/`, CI for pipelinen
- [x] PR 1 til 4 flettet inn i `main`
