# Logg

Alt som gjøres i prosjektet, med tidspunkt (norsk tid). Nyeste nederst.

## 2026-10-05 21:22
- Repo opprettet av Tom. Tre konseptbilder lastet opp (Maggie Robbins, Boston Low, Ludger Brink).

## 2026-10-06 19:40 til 20:15 (Claude)
- Sjekket etter AGENTS.md. Finnes ikke i repoet.
- Gikk gjennom Drive-mappen med spillfilene (DIG.LA0, DIG.LA1, DIGMUSIC.BUN, DIGVOICE.BUN, VIDEO/ med 55 SAN, 4 NUT og 2 TRS). Ingen exe, ingen `_other/`.
- Leste DIG.LA0: motorversjon 7.3.4 (9. okt 1995), data 7. nov 1995, 111 navngitte rom, 306 skriptplasser (303 i bruk), 332 kostymeplasser, 984 globale objekter. Engelsk utgave (ingen LANGUAGE.BND).
- Fant at DIG.LA1 (88 673 344 byte) har samme størrelse som filen thedig-textures er verifisert mot.
- Gikk gjennom thedig-textures (README, AGENTS.md, docs/la1-census.txt) og ScummVM sin SCUMM-kode (master, commit c909132) for å finne stedene en HD-fork må koble seg inn.
- La til:
  - `docs/ANALYSE.md`: full analyse av filer, omfang, metoder og første steg.
  - `docs/rom-oversikt.csv`: alle 111 rom med mål, z-plan, paletter og antall objektbilder, med tomme kolonner for prioritet og status.
  - `tools/la0_info.py`: leser DIG.LA0 og skriver ut versjon, grenser, MD5 og romliste.
  - `.gitignore`: holder spillfiler og uttrukket grafikk ute av git.
  - `log.md`, `memory.md`, `todo.md`.
- Ikke gjort: MD5 av DIG.LA0 er ikke kontrollert (fikk ikke byte-eksakt kopi via Drive-koblingen). DIG.LA1 og SAN-filene er ikke lastet ned eller kjørt gjennom uttrekk ennå.
