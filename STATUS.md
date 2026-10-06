# Status

Oppdatert 6. oktober 2026, 23:55. Siste runde med ChatGPT står i `work/gpt/RAPPORT.md` og i grenen `gpt-arbeid`.

## Kort

Motoren og verktøyene er ferdige nok til at grafikken kan lages rom for rom og spilles med en gang. ChatGPT har levert 2 av 106 rom. Resten går i runder: ChatGPT lager, Claude kontrollerer og bygger modden, Tom godkjenner.

## HD-grafikk

| Del | Ferdig | Totalt | Kilde | Merknad |
| --- | --- | --- | --- | --- |
| Rombakgrunner | 2 | 106 | ChatGPT | Rom 9 (core) og 22 (beach). 5 nesten tomme rom tegnes av filmer og er tatt ut. |
| ChatGPT-jobber | 2 | 162 | ChatGPT | Brede og høye rom er delt i flere jobber. Se `work/gpt/status.csv` eller grenen `gpt-arbeid`. |
| Objektbilder | 0 | 642 | | Automatisk oppskalering i sammenheng med rommet. Egen ChatGPT-runde senere. |
| Kostymeruter | 0 | 28 490 | | Automatisk oppskalering. Plan: modellark per hovedperson fra ChatGPT, så oppskalering. |
| Filmrammer | 0 | 12 638 | | Utskifting virker. Videooppskalering senere. |

Stil: trofast HD, samme motiv og farger med mer detalj. Stilankere: rom 9 og 22 (i `gpt-arbeid/stil/`).

## Det som virker

| Del | Hva | Hvordan det er testet |
| --- | --- | --- |
| Spillfiler | DIG.LA0, DIG.LA1 og VIDEO i `spilldata`, hentes og sjekkes med `tools/hent_spilldata.sh` | SHA-256 for alle 62 filer; LA1 er byte for byte lik filen thedig-textures er verifisert mot |
| Uttrekk | Rom, objekter, kostymer med RGBS-farger og DCOS-ID, filmrammer | Tellinger mot LA1 (111, 642, 28 490, 12 638), testen `pytest -m game` |
| Motor: bakgrunner og objekter | HD der originalen viser uendret bakgrunn eller et kjent objektbilde | `engine/test.sh` med nearest-mod: 0 avvikende piksler i rom 2, 26, 34 og 105 |
| Motor: figurer | HD-sprites for kostymeruter med kodek 1 og 5 | 0 avvik for uskalerte figurer, under 0,25 prosent for skalerte (jevn skalering, ventet) |
| Motor: filmer | HD-rammer per SAN-fil | 198 av 198 rammer i introen like med nearest-rammer etter rettingen til `_frame - 1` |
| Motor: farger | Fade og palettbytte følger med; fargesyklede farger vises som originalen | Sett i dumpede bilder fra rom 2 og 22 |
| Motor på laptopen | SDL2, Wayland, OpenGL, 1280 x 800, 32 bit | Codex sin pilotkjøring, logger i `grafikkdata/pilot-20261006` |
| Bygg | `engine/build.sh` fra ren checkout av låst ScummVM-commit | Kjørt fra tom mappe her og av Codex på laptopen |
| ChatGPT-kontroll | Sideforhold, forskyvning, zoom, kantlikhet, fargelås, sammensying | Kunstige svar: 3 px forskyvning og 3 prosent zoom avvises, riktig plassert godkjennes; pilotbildene godkjent (forskyvning 0,73 og 0,25 px) |
| Pipeline | 7 tester, 6 uten spillfiler | `cd pipeline && pytest`, og `pytest -m "not game"` i CI på hver push |

## Kjente begrensninger

- Undertekster over filmer med HD-rammer blir borte (teksten er tegnet inn i originalrammen).
- Kostymer med kodek 16 (5 stykker) får ikke HD-sprites. Kodek 5 er koblet inn, men ikke kontrollert for seg i spillet.
- Tekst og fonter er originalpiksler.
- Fargesyklede områder (vann, energi) er originalpiksler også med HD-bakgrunn.
- Fargelåsen gjør ChatGPT-bildene litt mindre mettet enn generatoren laget dem, fordi fargene trekkes mot originalen. Styrken kan justeres (`dighd gpt-inn --styrke`).
- Ingen full gjennomspilling med HD-grafikk ennå. Forgrunnsmasker og objektbytte i de nye rommene er ikke kontrollert manuelt.
- Musikk og tale er ikke med i repoet (for store filer).

## Grener

| Gren | Innhold |
| --- | --- |
| `main` | Kode og dokumentasjon |
| `spilldata` | Spillfilene, privat |
| `gpt-arbeid` | Jobber, resultater, status, ORDRE.md og stilankere for ChatGPT, privat |
| `hd-mod` | Siste ferdige HD-mod, privat |
| `grafikkdata/pilot-20261006` | Grafikkpiloten fra Codex, privat |
