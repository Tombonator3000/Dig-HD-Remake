# Status

Oppdatert 7. oktober 2026, 13:05. Siste runde med ChatGPT står i `work/gpt/RAPPORT.md` og i grenen `gpt-arbeid`.

## Kort

Motoren og verktøyene er ferdige nok til at grafikken kan lages rom for rom og spilles med en gang. ChatGPT har levert 104 av 106 rom (rom 50 og 88 gjenstår) og alle 30 store objekter. Neste bestilling er de mindre objektene i lagjobber og ikonark.

## HD-grafikk

| Del | Ferdig | Totalt | Kilde | Merknad |
| --- | --- | --- | --- | --- |
| Rombakgrunner | 104 | 106 | ChatGPT | Alle unntatt rom 50 og 88. Noen står til sjekk og kan bli bedre. Se `GRAFIKKLISTE.md` i `gpt-arbeid`. 5 nesten tomme rom tegnes av filmer og er tatt ut. |
| ChatGPT-jobber | 187 | 431 | ChatGPT | 162 for rom, 30 for store objekter, 236 lagjobber og 3 ikonark. Se `work/gpt/status.csv` eller grenen `gpt-arbeid`. |
| Store objektbilder | 30 | 30 | ChatGPT | Nærbilder, kart, trikken og liknende som dekker mye av skjermen. I rom 28 dekker tavla (obj241) nesten hele bildet. 2 ensfargede rutenett i inventaret (rom 93) er tatt ut. |
| Mindre objektbilder | 0 | 609 | ChatGPT | 460 i lagjobber (rommet med objektene på plass, klippes ut etterpå) og 149 ikoner i ikonark. Til de er levert: automatisk oppskalering. |
| Kostymeruter | 0 | 28 490 | | Automatisk oppskalering. Plan: modellark per hovedperson fra ChatGPT, så oppskalering. |
| Filmrammer | 0 | 12 638 | | Utskifting virker. Videooppskalering senere. |

Stil: trofast HD, samme motiv og farger med mer detalj. Stilankere: rom 9 og 22 (i `gpt-arbeid/stil/`).

## Det som virker

| Del | Hva | Hvordan det er testet |
| --- | --- | --- |
| Spillfiler | DIG.LA0, DIG.LA1 og VIDEO i `spilldata`, hentes og sjekkes med `tools/hent_spilldata.sh` | SHA-256 for alle 62 filer; LA1 er byte for byte lik filen thedig-textures er verifisert mot |
| Uttrekk | Rom, objekter, kostymer med RGBS-farger og DCOS-ID, filmrammer | Tellinger mot LA1 (111, 642, 28 490, 12 638), testen `pytest -m game` |
| Motor: bakgrunner og objekter | HD der originalen viser uendret bakgrunn eller et kjent objektbilde | `engine/test.sh` med nearest-mod: 0 avvikende piksler i rom 2, 26, 34 og 105 |
| Motor: figurer | HD-sprites for kostymeruter med kodek 1, 5 og 16. Kodek 5 og 16 fargelegges med rompaletten der kostymet vises | 0 avvik for uskalerte figurer, under 0,25 prosent for skalerte (jevn skalering, ventet). Kodek 5 og 16: nearest-mod i 19 rom og med testkroken `DIGHD_TEST_COSTUME`, 0 avvik; 96 til 100 prosent av figurpikslene får HD |
| Spille fra repoet | `./spill.sh` henter spillfiler og HD-mod, bygger motoren og starter spillet. Valg for rom, klassisk, gult felt og automatisk oppskalering | Kjørt fra en fersk `git clone` her: alt hentet og bygget, spillet startet i rom 22 med HD-bakgrunnen (uten skjerm, med `--programvare`). `--auto`-modden bygget på 86 sekunder med ChatGPT-rommene i |
| Motor: filmer | HD-rammer per SAN-fil, med undertekstene oppå som originalpiksler | 198 av 198 rammer i introen like med nearest-rammer etter rettingen til `_frame - 1`. Undertekster: hele SQ1 med nearest-rammer og merkede rammer, all synlig tekst på samme sted som i originalen og resten HD |
| Motor: tekst | All tekst i spillet (tegnsettene i DIG.LA1) og i filmene (NUT-fontene) tegnes med glatte HD-bokstaver laget med xBR fra spillets egne fonter, på samme sted og med samme farger. `DIGHD_TEXT` velger skalerer | Rom 2 og introen med undertekster: med `nearest` 0 avvik i 45 dumper med tekst, plasseringen stemmer i 47 av 47, ingen tekst står igjen, ingen målbar tidsøkning i rommet |
| Motor: farger | Fade og palettbytte følger med. Fargesyklede områder (vann, fosser) vises med HD-bildet og følger syklingen | Rom 22 med ChatGPT-bakgrunn og rom 11 og 43 med lanczos-sharp: vannet beveger seg uten rutenett eller glorie. Ett syklingssteg i rom 22 tar 2,0 ms (før 7,8 ms) |
| Motor: brytere | Ctrl+H bytter mellom HD og klassisk, Ctrl+Shift+H farger gult der HD mangler (også `DIGHD_CLASSIC`, `DIGHD_SHOW_MISSING`) | Uten skjerm med `DIGHD_TEST_KEYS`: klassisk dump lik originalen i rom 22 og 28, gult felt riktig i intro og rom 2; samme fart som før (8 til 9 ms per bilde). Ikke prøvd med ekte tastatur |
| Motor: store objekter | HD-objektbilder fra ChatGPT også i rom uten HD-bakgrunn | Rom 28 kjørt uten skjerm: tavla obj241 dekker nesten hele skjermen (69 492 objektpiksler mot 185 rompiksler) |
| Motor på laptopen | SDL2, Wayland, OpenGL, 1280 x 800, 32 bit | Codex sin pilotkjøring, logger i `grafikkdata/pilot-20261006` |
| Bygg | `engine/build.sh` fra ren checkout av låst ScummVM-commit | Kjørt fra tom mappe her og av Codex på laptopen |
| ChatGPT-kontroll | Sideforhold, forskyvning, zoom, kantlikhet, fargelås, sammensying, objektjobber, like tilstander | Kunstige svar: 3 px forskyvning og 3 prosent zoom avvises, riktig plassert godkjennes; pilotbildene godkjent (forskyvning 0,73 og 0,25 px) |
| Pipeline | 10 tester, 9 uten spillfiler | `cd pipeline && pytest`, og `pytest -m "not game"` i CI på hver push |

## Kjente begrensninger

- Kodek 5 og 16: 110 av kostymene ble ikke tegnet da testen hoppet gjennom rommene, så fargene deres er valgt etter hvilken palett som gir jevnest bilde. Et kostyme som vises med to helt ulike paletter, får riktige HD-farger bare i den ene (sett for 266 i rom 79).
- Fargesyklede farger på figurer er originalpiksler. Glitter av enkeltpiksler (fossen i rom 43) beveger seg svakere enn i originalen.
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
