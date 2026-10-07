# todo.md

Det som gjenstår, viktigst først. Kryss av når noe er gjort, og logg det i `log.md`.

## Neste

- [ ] ChatGPT-runder hver halvtime med `tools/gpt_runde.sh` til alle 192 jobber (162 rom, 30 store objekter) er godkjent
- [ ] Se gjennom hvert nytt godkjent rom i forhåndsvisningen før det rapporteres (avvis med `docs/gpt-avvisninger.csv`)
- [ ] Juster grensene i `gpt.py` etter de første 20 ekte leveransene
- [ ] Kontroller de nye rommene i motoren med forgrunnsmasker og objektbytte (`engine/test.sh` og manuelt)
- [x] `./spill.sh` og `docs/SPILLTEST.md`: spille og teste rett fra repoet
- [ ] Tom tester med `./spill.sh` etter `docs/SPILLTEST.md` (eller Codex med kodeoppgave 1): masker, objektbytte, Ctrl+H og Ctrl+Shift+H

## ChatGPT-grafikk

- [x] Bestilling, jobbverktøy, kontroll og arbeidsgren `gpt-arbeid`
- [x] Pilot: rom 9 og 22 levert av Codex, kontrollert og godkjent, lagt i `stil/` som stilankere
- [x] Fast ordre i `ORDRE.md` og runde-skript (`tools/gpt_runde.sh`), mod publiseres i `hd-mod`
- [x] `GRAFIKKLISTE.md` med alt som skal lages, i 19 bestillinger, så ChatGPT kan jobbe videre uten å vente
- [ ] Resten av romjobbene (52 rom igjen)
- [x] Objektjobber for de 30 største objektbildene, med egne notater og like tilstander
- [ ] De 30 objektjobbene
- [ ] Tom ser over stilen når 10 til 15 rom er ferdige
- [ ] Bestilling runde 2: objekter (642 bilder) i sammenheng med godkjente HD-rom
- [ ] Bestilling runde 3: modellark for hovedpersonene, så automatisk oppskalering av rutene
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
