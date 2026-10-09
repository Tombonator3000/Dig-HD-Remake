# Status

Oppdatert 9. oktober 2026. Grafikkgrunnlaget er modden fra 9. oktober, 09:49. Siste runde med ChatGPT står i `work/gpt/RAPPORT.md` og i grenen `gpt-arbeid`.

## Kort

Motoren og verktøyene er ferdige nok til at grafikken kan lages rom for rom og spilles med en gang. ChatGPT har levert 103 av 106 godkjente rom (rom 32 gjøres om, rom 50 og 88 gjenstår) og alle 30 store objekter. Det første figurarket er satt inn: Boston Low står og går i HD (28 ruter). Neste bestilling er resten av Boston-piloten og de mindre objektene i lagjobber og ikonark.

## HD-grafikk

| Del | Ferdig | Totalt | Kilde | Merknad |
| --- | --- | --- | --- | --- |
| Rombakgrunner | 103 | 106 | ChatGPT | Alle unntatt rom 32 (vannet ble stein, gjøres om), 50 og 88. Noen står til sjekk og kan bli bedre. Kontrollert i motoren med `tools/romtest.sh`. 5 nesten tomme rom tegnes av filmer og er tatt ut. |
| ChatGPT-jobber | 187 | 435 | ChatGPT | 162 for rom, 30 for store objekter, 236 lagjobber, 3 ikonark og 4 figurark i Boston-piloten. Se `work/gpt/status.csv` eller grenen `gpt-arbeid`. |
| Store objektbilder | 30 | 30 | ChatGPT | Nærbilder, kart, trikken og liknende som dekker mye av skjermen. I rom 28 dekker tavla (obj241) nesten hele bildet. 2 ensfargede rutenett i inventaret (rom 93) er tatt ut. |
| Mindre objektbilder | 0 | 609 | ChatGPT | 460 i lagjobber (rommet med objektene på plass, klippes ut etterpå) og 149 ikoner i ikonark. Til de er levert: automatisk oppskalering. |
| Kostymeruter | 28 | 28 490 | ChatGPT | Figurark: rutene i en animasjon males samlet og klippes ut. Pilot med 4 ark (229 ruter) for Boston Low. Ark 1 (fig014_01, stående og gående, 28 ruter) er godkjent av Tom 9. oktober og ligger i modden. Ansiktet er litt yngre enn originalen og mangler det grå håret ved tinningene. Alle kostymer gir 4031 ark, hovedpersonene 114. |
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
| Motor: ChatGPT-figur | De 28 rutene fra fig014_01 (Boston Low) vises i spillet | Rom 22 uten skjerm med `DIGHD_TEST_COSTUME=14` og `DIGHD_VERIFY=1`, 1400 bilder: når Boston står eller går mot siden, kommer 699 til 1088 figurpiksler fra HD-rutene og 0 fra originalen. Animasjoner som ikke er malt ennå, vises som originalen. Skjermen lik hele skjermen bygget på nytt i alle dumper |
| Romtest | Alle rom kjørt uten skjerm med `tools/romtest.sh` | 111 rom, 226 kjøringer: ingen krasj, HD-bakgrunnen brukt i alle rom som har den, ingen forskjøvne bilder, figurene går bak det samme som i originalen |
| Motor på laptopen | SDL2, Wayland, OpenGL, 1280 x 800, 32 bit | Codex sin pilotkjøring, logger i `grafikkdata/pilot-20261006` |
| Bygg | `engine/build.sh` fra ren checkout av låst ScummVM-commit | Kjørt fra tom mappe her og av Codex på laptopen |
| ChatGPT-kontroll | Sideforhold, forskyvning, zoom, kantlikhet, fargelås, sammensying, objektjobber, like tilstander | Kunstige svar: 3 px forskyvning og 3 prosent zoom avvises, riktig plassert godkjennes; pilotbildene godkjent (forskyvning 0,73 og 0,25 px) |
| Pipeline | 10 tester, 9 uten spillfiler | `cd pipeline && pytest`, og `pytest -m "not game"` i CI på hver push |

## Nettleser og GitHub Pages

Egen inngang i `engine/pages`: spillfiler og HD-pakke velges fra maskinen og
lagres lokalt i IndexedDB. Fire filtester bestått, inkludert at manglende
private filer ikke gir HTTP-forespørsler og at ScummVM-temaer bruker riktig
prosjektprefiks. Nettsidepakken har bare motor, temaer og tilhørende GPL-kode.

Bygget med den låste ScummVM-commiten og Emscripten 4.0.10, med uendret HD-patch.
Testet i Chromium uten skjerm: rom 22 og 9 med 1280 x 800 HD, mappeimport,
begge filpakkene beholdt etter omlasting, HD/klassisk-knapp og F5-meny. Ekte
lagring av `dig.s01`, lukking av nettleseren og lasting fra rom 9 tilbake til
rom 22 bestått. Ingen spill- eller HD-filer sendt som HTTP-forespørsler.
Musikk og tale ikke testet fordi DIGMUSIC.BUN og DIGVOICE.BUN mangler lokalt.

GitHub avviste Pages fra det private repoet med gjeldende abonnement. Derfor
brukes det separate offentlige motorrepoet `Tombonator3000/Dig-HD-Web`.
Spillrepoets synlighet er uendret. [Nettsiden](https://tombonator3000.github.io/Dig-HD-Web/)
er publisert og kontrollert: HTTP 200, faktisk HD-oppstart fra Pages,
HD/klassisk-knapp og fullskjerm. Offentlig motorbygg og deploy i GitHub Actions
bestått. Direkte adresser til spillfiler og HD-bilder gir HTTP 404.
Full gjennomspilling og mobiltest er ikke utført.

HD-figurer fra Pages (testet 9. oktober i Chromium uten skjerm, mot den
publiserte siden): spillmappen og `mods/gpt` med de 28 figurrutene valgt,
`?rom=22&DIGHD_TEST_COSTUME=14`. Boston ble vist med HD-rutene i rom 22, og
rutene som ikke er malt ennå (gange mot kameraet), som originalen. HD/klassisk-
knappen byttet til klassisk. Ingen forespørsler mot spill- eller HD-stier.
Den publiserte motoren er bygget fra samme patch som `main` (filene i
Dig-HD-Web er like). Siden viser nå hvor mange HD-rom, objektbilder og
figurruter pakken har, og når den ble laget, så det er lett å se om en
nyere HD-pakke må velges på nytt.

## Kjente begrensninger

- Kodek 5 og 16: 110 av kostymene ble ikke tegnet da testen hoppet gjennom rommene, så fargene deres er valgt etter hvilken palett som gir jevnest bilde. Et kostyme som vises med to helt ulike paletter, får riktige HD-farger bare i den ene (sett for 266 i rom 79).
- Fargesyklede farger på figurer er originalpiksler. Glitter av enkeltpiksler (fossen i rom 43) beveger seg svakere enn i originalen.
- Fargelåsen gjør ChatGPT-bildene litt mindre mettet enn generatoren laget dem, fordi fargene trekkes mot originalen. Styrken kan justeres (`dighd gpt-inn --styrke`).
- HD-figurrutene klippes ut med originalens silhuett, så kantene blir trappete i 4x (se fig014_01). Mykere kanter innenfor silhuetten står i `todo.md`.
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
