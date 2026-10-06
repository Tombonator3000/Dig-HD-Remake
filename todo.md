# Todo

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

## Neste
- [ ] Bygg og kjør på laptopen (`engine/build.sh`, `engine/run.sh hd`), med musikk og tale fra Drive i game/
- [ ] Velg stil: trofast HD (A) eller ny tegnestil (B)
- [ ] Stiltest med KI: fem rom gjennom Real-ESRGAN og en pikselkunstmodell (`dighd compare`, `--method realesrgan`)
- [ ] Stiltest: Boston Low (kostyme 14) i ny stil
- [ ] Kontroller grafikkpiloten med manuell bevegelse, forgrunnsmasker og obj171-tilstander før produksjonsgodkjenning
- [ ] Lag Boston-ruter som består silhuettkontrollen og kontroller hele bevegelsesrekken i motoren
- [ ] Fyll inn prioritet i `docs/rom-oversikt.csv`

## Motor
- [ ] Undertekster over HD-filmrammer: legg teksten over HD-rammen i stedet for å skjule den
- [ ] HD-sprites for kodek 16 (5 kostymer) og kontroll av kodek 5 i spillet
- [ ] HD-fonter for tekst
- [ ] Fargesyklede områder i HD (eget animert lag)
- [ ] Hurtigtast for å bytte mellom klassisk og HD
- [ ] Spille av rene filmer som MP4/WebM i stedet for tusenvis av PNG-er
- [ ] Prøv en nyere ScummVM-commit og oppdater patchen

## Senere
- [ ] Finn ut i skriptene hvilke SAN-filer som er rene filmer og hvilke som styres av spillet (NUTCracker eller descumm -7)
- [ ] Skript som lager hele HD-pakken lokalt fra brukerens egne spillfiler (for eventuell deling)
