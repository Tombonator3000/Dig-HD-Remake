# Todo

## Nå
- [ ] Kopier spillfilene fra Drive til laptopen (for eksempel `~/Games/TheDig`)
- [ ] Kjør `python3 tools/la0_info.py ~/Games/TheDig/DIG.LA0` og sjekk MD5
- [ ] Start spillet i ScummVM og bekreft at filene er hele
- [ ] Installer thedig-textures og kjør `extract --game ~/Games/TheDig --out ~/dig-out` (krever 15 GB ledig)
- [ ] Dekompiler skriptene med NUTCracker eller `descumm -7`

## Motor
- [ ] Fork ScummVM og bygg på Linux
- [ ] Legg til HD-flate (32 bit, 4x) etter mønster fra `_macScreen` / `mac_drawStripToScreen`
- [ ] Bakgrunnsbytte for ett rom (kandidater: 22 beach eller 24 view)
- [ ] Test et rullende rom (34 museum eller 25 airlock)
- [ ] Objektbilder og z-planer i HD
- [ ] AKOS-ruter i HD med ankerpunkter ganget med 4
- [ ] Palettbytte og fargesykling i HD
- [ ] SMUSH: bytte rammer per SAN-fil, og video for rene filmer
- [ ] Hurtigtast for klassisk og HD

## Grafikk
- [ ] Velg stil: trofast HD (A) eller ny tegnestil (B)
- [ ] Stiltest: fem rom gjennom tre oppskaleringsmetoder
- [ ] Stiltest: Boston Low gangsyklus i ny stil
- [ ] Fyll inn prioritet i `docs/rom-oversikt.csv`

## Senere
- [ ] Finn ut i skriptene hvilke SAN-filer som er rene filmer og hvilke som styres av spillet
- [ ] Skript som genererer HD-pakken lokalt fra brukerens egne spillfiler
