# Todo

## Ferdig
- [x] Spillfilene fra Drive til grenen `spilldata`, med sjekksummer og hentescript
- [x] MD5 av DIG.LA0 sjekket (standardutgaven)
- [x] Uttrekk av rom, objekter, kostymer (med riktige farger) og filmrammer
- [x] Pipeline `dighd` med flere oppskaleringsmetoder og mod-mapper
- [x] ScummVM-patch: HD-bakgrunner, HD-objekter, HD-sprites, HD-filmrammer
- [x] Fargejustering ved palettbytte, fargesykling beholdt, mus og peker i HD
- [x] Byggeskript testet fra ren checkout, automatisk test uten skjerm

## ChatGPT-grafikk
- [x] Bestilling, jobbverktøy, kontroll og arbeidsgren `gpt-arbeid`
- [ ] Pilot: ChatGPT leverer rom022, rom002_del1av3 og rom028
- [ ] Tom godkjenner piloten, godkjente bilder legges i `stil/` som stilankere
- [ ] Juster grensene i `gpt.py` etter ekte resultater
- [ ] Resten av de 162 romjobbene
- [ ] Bestilling runde 2: objekter (642 bilder) i sammenheng med godkjente HD-rom
- [ ] Bestilling runde 3: modellark for hovedpersonene, så automatisk oppskalering av rutene

## Neste
- [ ] Bygg og kjør på laptopen (`engine/build.sh`, `engine/run.sh hd`), med musikk og tale fra Drive i game/
- [x] Velg stil: trofast HD
- [ ] Stiltest med KI: fem rom gjennom Real-ESRGAN og en pikselkunstmodell (`dighd compare`, `--method realesrgan`)
- [ ] Stiltest: Boston Low (kostyme 14) i ny stil
- [ ] Fyll inn prioritet i `docs/rom-oversikt.csv`

## Motor
- [ ] Undertekster over HD-filmrammer: legg teksten over HD-rammen i stedet for å skjule den
- [ ] HD-sprites for kodek 16 (5 kostymer) og kontroll av kodek 5 i spillet
- [ ] HD-fonter for tekst
- [ ] Fargesyklede områder i HD (eget animert lag)
- [ ] Hurtigtast for å bytte mellom klassisk og HD
- [ ] Vis et gult felt der HD mangler (som i Moonstone), for å se dekningen
- [ ] Spille av rene filmer som MP4/WebM i stedet for tusenvis av PNG-er
- [ ] Prøv en nyere ScummVM-commit og oppdater patchen

## Senere
- [ ] Finn ut i skriptene hvilke SAN-filer som er rene filmer og hvilke som styres av spillet (NUTCracker eller descumm -7)
- [ ] Skript som lager hele HD-pakken lokalt fra brukerens egne spillfiler (for eventuell deling)
