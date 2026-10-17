# todo.md

Det som gjenstår, viktigst først. Kryss av når noe er gjort, og logg det i `log.md`.

## Neste, 17. oktober 2026

- [x] Integrert produsert r19-grafikk via PR66 til hd-mod 630cadb3.
- [x] Hentet kode/main, grafikk/gpt-arbeid, web/main og oppdatert lokal hd-mod med fast-forward.
- [x] Ny Linux-AppImage r19 publisert i bygg39027347179; nedlastet fil, alle 44 551 manifestfiler og faktisk AppRun kontrollert.
- [x] Kildearkiv oppdatert med gjeldende motorpatch 0007 og eksakt byggeoppskrift.
- [x] Pakkens egne figurtester: Brink46 15, Maggie331 52, kapsel270 30 og rotte183 37 ruter, ingen omtegningsavvik.
- [x] R20-arbeidsrunde: 196 nye Nexus-dørfaser og 25 nye canyon-ruter, alle observert i motoren. 561 kontroller etter oppstart uten omtegningsavvik. Grafikk i gpt-arbeid, ikke ny distro.
- [ ] Gå gjennom de 100 eldre HD-rutene i costume034. Blant annet 050 og 108 har feil personer/klær; hele canyon-serien er fortsatt ikke visuelt sammenhengende.
- [ ] Fortsett all restgrafikken: 6 011 faktiske bilder i r20-arbeidslisten etter utskilling av 712 palettmasker, samt øvrige eldre figurfeil.
- [ ] Toms visuelle godkjenning og full naturlig spill-/overgangstest. Windows og mobil er ikke testet i denne leveransen.

## Historikk, 16. oktober 14:59

- [x] R16 integrert via PR62/63, Linux-AppImage publisert og kontrollert med alle55 filmer.
- [x] Ferdig r17-grafikk til repo og utkast-PR64, uten uferdig pole178.
- [x] R18-kandidat: figurkontakter, talevarianter, pole178, felles aktørskala og strengere kontaktkontroll.
- [x] R18-kandidat: to måner148/149, detaljert plateau og tilpasset åpning387/388.
- [x] R18-kandidat: tram-gangflate890 i rom80, edderkoppsilhuett136, tett rist356/357, laser233/234/235.
- [x] Native kontroller, grafikkrapport og PR64/65 samt nettleser-PR6.
- [x] Flettet PR64/65 og nettleser-PR6 etter Toms bestilling, lokale repoer oppdatert.
- [x] R18 er avløst av integrert og etterkontrollert r19-AppImage, se nyeste leveranse over.
- [ ] Toms visuelle gjennomgang av r17/r18 og full naturlig spill-/overgangstest.

## Til komplett utgave (oversikt 14. oktober, rettet 09:48, mot hd-mod 05179ed / r12)

Telt fra filene i `hd-mod` mot originalrutene i jobbene i `gpt-arbeid` (`jobber/fig*/original_1x.png`). Ruter med bare skyggemerker (magenta, 362 i alt) og tomme ruter trenger ikke HD og er ikke regnet som mangler. Rom (106), objekter (640 av 642, to rutenett tatt ut med vilje), alle 149 inventarbilder og teksten er med. Ruter uten HD vises som originalpiksler i 4 x 4-blokker, og blir gule med Ctrl+Shift+H. Hvilke ruter som faktisk vises i spillet, er ikke kontrollert.

- [ ] Romdrakt, 92 ruter uten HD (Tom så ingen i gjennomspillingen på Linux 14. oktober, så de vises kanskje sjelden eller ikke):
  - Boston (kostyme 1) rute 62 til 82: sitter i stolen med jetpakken og snur seg (fig001_20, HOLD)
  - Mannskapet med jetpakke og verktøy i rom 5 (kostyme 8): 52 ruter, 1 av 53 har HD
  - Brink og Maggie i tunnelen (kostyme 22 og 23, rom 10): 9 og 10 ruter. Samme omriss som kostyme 3 og 2, men andre farger, så HD-tegningene derfra kan trolig fargelegges om
- [ ] Hovedpersonene ellers, 66 ruter: Boston og Brink i lockup (kostyme 229) 25, Boston og Maggie i theeye (213, 214, 222) 20, robotarmen (5) 13, Boston i nexus (71) 8
- [ ] Andre kostymer: 10 158 ruter med figurgrafikk uten HD, pluss 4 500 bitte små (under 40 piksler, mest lysglimt). 101 kostymer har ingen HD. Største: trikkekartet (270, 268, 272, 274, 276) 959, portrettene i håndcomputeren (newton 224, 225, 227, 228) 658, de preglede figurene (emboss 31, 318, 320, 326) 498, pool (101, 113) 339, energivirvelen i eyehub (247) 281, plandoor (183) 194
- [x] Filmene (SAN): alle 55 og 12 638 rammer produsert i HD, publisert i hd-mod etter Toms fletting av PR 60 og pakket i ny Linux-AppImage (1,78 GB). Filmene tar 109,43 MB uten PNG-video. Se docs/VIDEO-PRODUKSJON.md.
- [ ] Full visuell kontroll av alle 55 filmene i bevegelse og vanlig spilling.
- [ ] Toms visuelle godkjenning av r12 (`human_visual_approval` er false i `mod.json`) og én full gjennomspilling med HD. Tom har spilt r12 på Linux fram til slutten (14. oktober), slutten gjenstår; han sier fra når den er gjennomført
- [ ] Windows-pakken prøvd på en ekte Windows-maskin (bare Wine til nå)
- [ ] STATUS.md og README samstemt med r12 (STATUS sier fortsatt 103 rom og 2957 myke ruter; modden har 13 268). Linux-releasens navn og les-meg er oppdatert 16. oktober, med r12 og alle 55 HD-filmer. `ORDRE.md` i `gpt-arbeid` er fra 11. oktober
- [ ] Helt til slutt: mindre HD-filer (se Senere)

## Neste

- [x] Lokal kandidat for Toms grafikkfeil 16. oktober, med hovedark, original registrering og motorregresjoner.
- [x] Integrert r16 via PR61/62/63 og nettleser-PR5. Ny publisert Linux-pakke lastet ned og kontrollert.
- [ ] Tom vurderer r16 i bevegelse. Full visuell godkjenning gjenstår.
- [ ] Neste fem grafikkfunn: andre dørlåser, fjernvann, pole-handling, dowel og silver/gold scepter.
- [ ] Kontroller patch0006 i Windows, mobil og 32-bit OpenGL, samt full gjennomspilling.
- [x] Etter Toms fletting av PR 60: ny Linux-pakke med alle 55 HD-videoer. Bygg, Debian 12, nedlastet AppImage og alle mod-sjekksummer kontrollert 16. oktober.

- [x] Satt opp og kjørt de 54 resterende HD-videoene i rekkefølge, med teknisk kontroll, komprimering og PR 60 (16. oktober).

- [x] Ny nedlastbar Linux-pakke med komprimert SQ1-intro, oppdatert motorkilde og sjekksummer. Bygg, Debian 12 og nedlastet pakke kontrollert 16. oktober.

- [x] Sikre r11- og r12-rettingene før neste runde (15. oktober: runden fletter inn i den publiserte modden, `send` stopper tap): `tools/gpt_runde.sh` bygger modden på nytt fra `work/gpt-ferdig` uten Codex sine overstyringer (`gpt-arbeid/rapporter/spillfeil-20261013/mod-overrides` og `rapporter/spillfeil-r12-20261013/mod-overrides`) og tvangspusher den til `hd-mod`. Runden må bygge videre på publisert `hd-mod` eller legge på manifestene, og stoppe hvis filer forsvinner eller endres uten at det er meningen. (funnet 15. oktober)
- [x] Motoren skriver det som vises uten HD til `dighd-uten-hd.txt` i lagringsmappen, og `dighd mangler` lager oversikten (15. oktober, testet uten skjerm)
- [ ] Tom spiller med en pakke bygget etter at PR-en er flettet, og sender `dighd-uten-hd.txt` (Linux: `~/.local/share/the-dig-hd/saves/`). Claude lager bestillingen ut fra `dighd mangler`
- [ ] Etter fletting: kopier patchen til Dig-HD-Web, så nettsiden får samme motor. Windows-pakken bygges på nytt (Codex)

- [x] [HD] Boston beholder HD bak luftslusens glass i r12-kandidaten
- [x] [HD] Eksakt SMAP-dekning og objektprioritet for PDA-portretter og knapper
- [ ] Verifiser r12-pakkene separat fra lokal motor og grafikkandidat

- [x] [HD] Inventory beholder HD ved horisontal scroll, testet fra Toms lagring5
- [x] [HD] Luftslusens palettmasker bevarer HD-underlaget
- [x] [HD] Produsert/registrert manglende krystall-, vann-, sparks- og lysfaser i r11-kandidat
- [ ] Tom gjennomgår de korrigerte animasjonene i den publiserte pakken

- [x] Innført kildetro motiv- og designanalyse før HD-produksjon i `docs/skills/scumm-hd-remake/SKILL.md`, med henvisninger fra arbeidsinstruksene (12. oktober 2026)

### Remastermetode og kvalitet (10. oktober)

- [x] Dokumentert repo-gjennomgang og arbeidsmetode i `docs/HD-REMASTER-METODE.md`, med kilder fra offisielle remastere og konkrete forbedringspunkter
- [ ] Lag animasjonsforhåndsvisning for myke ruter med original og HD, hode/kropp samlet, korrekt rekkefølge og tempo
- [ ] Lag visuell godkjenningsliste per ressurs og checksum, og skill arbeidsmod fra ferdig kontrollert pakke
- [ ] Krev eksplisitt rutekart for nye myke figurark og kontroller eldre radkoblinger før ferdigmelding
- [ ] Kontroller at avviste myke eksportfiler ikke blir stående ved ny bygging, og at fallback virker
- [ ] Samstem README, STATUS og pakketellinger fra samme verifiserte hd-mod-SHA; skill levert, ok, sjekk og visuelt godkjent
- [ ] Test flere myke figurer over hverandre, z-masker, skalering og menyer i ekte spilltilstand
- [x] Gjennomgang av hvordan LucasArts og Double Fine laget remasterne, med tiltak: `docs/REMASTER-FORBILDER.md`
- [x] Master-figurark for Boston, Brink, Maggie og Pig (forfra, profil, bakfra, i drakt og uten), godkjent av Tom, og påbudt som referanse i alle figurjobber for dem. Bestilt i ORDRE.md 11. oktober. Levert av Codex 12. oktober: `hovedark/boston.png`, `maggie.png`, `brink.png` og `robotarm.png` i `gpt-arbeid`, oversikt i `rapporter/hovedark-20261012/OVERSIKT.png` (Pig godkjent 11. oktober). Tom godkjente Boston, Maggie, Brink og robotarmen 15. oktober 2026. Godkjenning med SHA-256 er registrert i `gpt-arbeid/rapporter/hovedark-20261012/GODKJENNING.md`; riktig hovedark brukes i nye figurjobber
- [ ] Visuell kontroll av figur mot rom i ekte spillbilde: samme kantmykhet, lysretning og metning
- [ ] Merk feil i todo som `[original]` eller `[HD]` (påbegynt 11. oktober i Motor), og skriv i HD-MOTOR.md om hver motorendring leser tilstand, endrer tilstand eller lapper skript


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
- [x] Alle de andre figurene bestilt i glatt stil: 4031 figurark (28481 ruter), beskjed i ORDRE.md 9. oktober
- [ ] Figurarkene fra Codex, tas inn av runden av seg selv
- [x] Filmene (SAN) i HD: alle 55 oppskalert, komprimert, publisert og med i Linux-pakken 16. oktober. Full visuell kontroll i bevegelse står separat over.
- [ ] Myke figurer: kant mot forgrunnen i 4 x 4-blokker; prøv å følge den myke kanten i HD-rommet
- [ ] Myke figurer på ekte skjerm: flere figurer over hverandre, skalerte figurer, banner og meny over, nedtoning
- [ ] Ansiktet til Boston nærmere originalen i de neste arkene (eldre, grått hår ved tinningene)
- [ ] Mykere kanter på HD-figurrutene: alfa jevnet ut innenfor originalens silhuett, i stedet for trappetrinn i 4x
- [ ] Lag Boston-ruter som består silhuettkontrollen og kontroller hele bevegelsesrekken i motoren

## Motor

- [x] Felles patch med Sam-Max-HD (15. oktober, Claude). Endringer i patchen bør gjøres i begge repoer, eller slås sammen på nytt
- [ ] Kjør `engine/test.sh` (nearest) med den felles patchen på en maskin der dekoderne kan hentes

- [x] Lagring i Linux-pakken undersøkt (10. oktober): virker uten skjerm og med ekte X11-inndata, ingen feil funnet. Patchen i `saveload.cpp` flytter bare pekeren etter lasting
- [ ] Tom prøver lagring fra F5-menyen igjen på laptopen og sier fra (hvor det stopper hvis det ikke virker)
- [x] Inventaret i HD (blast-objekter med skygge, ikonene med HD-bilde), PR 44
- [x] Aldri rett til skrivebordet: avslutning åpner menyen, Esc starter ikke stoppede skript, PR 44
- [ ] [original] F5 ga «HEAP ... MEM ... VID» hos Tom; F5 virker her. Meldingen er spillets egen (SYSTEM.022, tasten h). Se i loggen hans etter `DigHD: key 286` neste gang
- [x] Beskrivelsesteksten (navn ved musen) med Exo 2 og skygge, PR 44
- [x] [original] Luft etter r i HD-skriften («Br ink»): originalskriften har samme luft (r er fire piksler med armen øverst). Prøvd å tilpasse bredden og plassen til originalbokstaven 11. oktober; ingen synlig forskjell, tatt ut igjen
- [ ] [HD] Armen som løfter Pig ut av romfergen ser rar ut (Tom 10. oktober): robotarmen er kostyme 4 og 5, og hver rute er tegnet for seg, så festet, leddene og enden skifter form fra rute til rute. Bestilt hovedark og nye ark i ORDRE.md 11. oktober. Scenen er ikke sett i spill her (skjer etter at spilleren gjør noe i rom 2)
- [x] [HD] Flekker av originalpiksler rundt skalerte myke figurer (astronauten som holder Pig i rom 4): PR 45, venter på at Tom fletter
- [x] Mottak av myke figurer versjon 3 (PR 46, venter på fletting): tekniske magentapiksler, utliggere (Pig 064), hodepuls mellom munnstillinger, rettingsark per rute via `fra-claude/mottak-per-rute.json`
- [x] Pig-serien etter Toms godkjente hovedark tatt inn 11. oktober (fig007_01 til 09, 03/05/07 med rettinger): 225 ruter ok, 16 sjekk; modden `hd-mod` 3f5f769
- [ ] Tom ser Pig i spillet (romdrakt-scenen i rom 4) og godkjenner serien
- [ ] Se på de 16 Pig-rutene til sjekk, blant dem 192 fra rettingsarket (0,78)
- [ ] Sju ruter for Boston i romdrakt uten HD (kostyme 1: 92, 109 til 112, 120, 161), trolig fra fig001_20 som er HOLD
- [x] Nye ark for Boston, Maggie og Brink i romdrakt (kostyme 1, 2, 3) og Pig (7) fra Codex tatt inn 11. oktober (riktige personer); Tom ser dem i pakken
- [ ] Tom ser på astronautene og Brink (kostyme 16 og 17 har mørkere hake i originalen, HD-Brink er glattbarbert som konseptet)
- [ ] 20 nye ruter for kostyme 229 er holdt ute (kodek 5, fargetabellen har like farger med ulik indeks, indeksbildet kan ikke lages uten dekoderne)
- [ ] Rom 32 og 77 er levert på nytt, men kan ikke kontrolleres her (rommene trenger uttrekket med dekoderne)
- [ ] Kostyme 22 og 23 (romdrakt i tunnelen) er trolig Brink og Maggie (samme ruter og mål som 3 og 2); ikke kontrollert i spill
- [x] Fast størrelse mellom rutene i myke-figurer (versjon 2), modden lappet og publisert (fdad5c7)
- [ ] Temaet `scummremastered` lastes ikke i Linux-pakken (LiberationSans-Bold.ttf mangler); legg skriften i pakken eller ta temaet ut
- [x] PR 42 var flettet 07:44; runden ble ferdig (`hd-mod` 07:50, `gpt-arbeid` 07:53)
- [x] Ctrl+Shift+H byttet til klassisk grafikk i stedet for gult felt (PR 43). Sifre i `DIGHD_TEST_KEYS`
- [ ] Codex-arkene levert 07:29 til 07:50 (gruppe 90, fig169 og fig170 m.fl.) er ikke i modden (holdt utenfor da modden ble lappet 10. oktober). Neste runde tar dem inn, men se først på stilavvisningen under. Tom avviste stilen på de siste figurarkene i Codex-chatten (overlevering i `gpt-arbeid`, `rapporter/overlevering-ny-chat-20261010/`)

- [x] HD-skrift for teksten: Exo 2 i stedet for xBR (PR 38 og 40)
- [ ] Tom ser teksten på ekte skjerm og sier om Exo 2 passer (vekt, luft mellom bokstavene)
- [ ] HD-skrift: tegnsett 0 og 3 og NUT-font 1 til 3 er ikke sett i spill ennå

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
- [x] Komprimert HD-video: VP8 i IVF per SAN-fil, følger SAN-rammene og beholder lyd/tekst, med PNG/original som tilbakefall (16. oktober, via PR)
- [ ] Prøv en nyere ScummVM-commit og oppdater patchen

## Senere

- [ ] Stiltest med KI-oppskalering: fem rom gjennom Real-ESRGAN og en pikselkunstmodell (`dighd compare`, `--method realesrgan`)
- [ ] Stiltest: Boston Low (kostyme 14) i ny stil, hvis Tom vil prøve ny tegnestil
- [ ] Fyll inn prioritet i `docs/rom-oversikt.csv`
- [ ] Finn ut i skriptene hvilke SAN-filer som er rene filmer og hvilke som styres av spillet (NUTCracker eller descumm -7)
- [ ] Skript som lager hele HD-pakken lokalt fra brukerens egne spillfiler (for eventuell deling)
- [ ] Helt til slutt (Tom 10. oktober): mindre HD-filer. Prøvd på utvalg: oxipng 3 til 6 prosent (tapsfritt), pngquant 55 til 60 prosent (rom snittavvik under 1 av 255, figurer 1,3), JPEG q92 for rom 80 prosent (krever at motoren leser JPEG). `_idx.png` må være tapsfrie. Modden er 1 GB, 756 MB av det er figurer

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
