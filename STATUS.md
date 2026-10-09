# Status

Oppdatert 9. oktober 2026, kveld. Siste runde med ChatGPT står i `work/gpt/RAPPORT.md` og i grenen `gpt-arbeid`.

## Kort

Motoren og verktøyene er ferdige nok til at grafikken kan lages rom for rom og spilles med en gang. ChatGPT har levert 103 av 106 godkjente rom (rom 32 gjøres om, rom 50 og 88 gjenstår), alle 30 store objekter og alle 149 ikonene i inventaret. Figurene tegnes nå i den glatte stilen Tom valgte: 148 av 509 ark for Boston, Brink og Maggie er levert, og 2957 ruter er tatt inn som myke ruter som motoren legger over bildet med myke kanter.

## HD-grafikk

| Del | Ferdig | Totalt | Kilde | Merknad |
| --- | --- | --- | --- | --- |
| Rombakgrunner | 103 | 106 | ChatGPT | Alle unntatt rom 32 (vannet ble stein, gjøres om), 50 og 88. Noen står til sjekk og kan bli bedre. Kontrollert i motoren med `tools/romtest.sh`. 5 nesten tomme rom tegnes av filmer og er tatt ut. |
| ChatGPT-jobber | 187 | 435 | ChatGPT | 162 for rom, 30 for store objekter, 236 lagjobber, 3 ikonark og 4 figurark i Boston-piloten. Se `work/gpt/status.csv` eller grenen `gpt-arbeid`. |
| Store objektbilder | 30 | 30 | ChatGPT | Nærbilder, kart, trikken og liknende som dekker mye av skjermen. I rom 28 dekker tavla (obj241) nesten hele bildet. 2 ensfargede rutenett i inventaret (rom 93) er tatt ut. |
| Mindre objektbilder | 167 | 609 | ChatGPT | 149 ikoner i ikonark (alle) og 18 av 460 i lagjobber (rommet med objektene på plass, klippes ut etterpå), blant dem håndcomputeren i rom 79. Resten: automatisk oppskalering. |
| Kostymeruter | 2957 | 28 490 | ChatGPT/Codex | Glatt stil med myke kanter for Boston, Brink og Maggie (54 kostymer, 509 ark, 7683 ruter): 148 ark levert, 2957 ruter tatt inn med `dighd myke-figurer` (392 av dem har et omriss som er ganske ulikt originalen og står til gjennomsyn i `myke.json`). Den gamle fig014_01 er erstattet av det glatte ark 1. Alle kostymer gir 4031 ark. |
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
| Motor: brytere | HD Graphics i spillets meny (F5) og Ctrl+H bytter mellom HD og originalgrafikk, og valget huskes (`dighd_classic`). Ctrl+Shift+H farger gult der HD mangler (også `DIGHD_CLASSIC`, `DIGHD_SHOW_MISSING`) | Uten skjerm med `DIGHD_TEST_KEYS`: klassisk dump lik originalen i rom 22 og 28, gult felt riktig i intro og rom 2; samme fart som før (8 til 9 ms per bilde). Menyen uten skjerm med `DIGHD_TEST_CLICKS` og i nettleseren med musklikk: byttet virker og huskes ved neste start. Ikke prøvd med ekte tastatur |
| Motor: store objekter | HD-objektbilder fra ChatGPT også i rom uten HD-bakgrunn | Rom 28 kjørt uten skjerm: tavla obj241 dekker nesten hele skjermen (69 492 objektpiksler mot 185 rompiksler) |
| Motor: myke figurer | Figurer i den glatte stilen legges over HD-bakgrunnen med egen alfa: myke kanter, eget omriss, bak forgrunnen (z-masken), under tekst og menyer, og borte når figuren er borte | Rom 22 uten skjerm: Boston går fram og tilbake med de ekte myke rutene, skjermen lik hele skjermen bygget på nytt i alle 48 dumper, ingen rester av margen. Bak forgrunnen med tre z-plan: 0 avvik fra z-masken. `engine/test.sh` som før. Ikke testet på ekte skjerm |
| Motor: ChatGPT-figur | De 28 rutene fra fig014_01 (Boston Low) vises i spillet | Rom 22 uten skjerm med `DIGHD_TEST_COSTUME=14` og `DIGHD_VERIFY=1`, 1400 bilder: når Boston står eller går mot siden, kommer 699 til 1088 figurpiksler fra HD-rutene og 0 fra originalen. Animasjoner som ikke er malt ennå, vises som originalen. Skjermen lik hele skjermen bygget på nytt i alle dumper |
| Romtest | Alle rom kjørt uten skjerm med `tools/romtest.sh` | 111 rom, 226 kjøringer: ingen krasj, HD-bakgrunnen brukt i alle rom som har den, ingen forskjøvne bilder, figurene går bak det samme som i originalen |
| Motor på laptopen | SDL2, Wayland, OpenGL, 1280 x 800, 32 bit | Codex sin pilotkjøring, logger i `grafikkdata/pilot-20261006` |
| Bygg | `engine/build.sh` fra ren checkout av låst ScummVM-commit | Kjørt fra tom mappe her og av Codex på laptopen |
| ChatGPT-kontroll | Sideforhold, forskyvning, zoom, kantlikhet, fargelås, sammensying, objektjobber, like tilstander | Kunstige svar: 3 px forskyvning og 3 prosent zoom avvises, riktig plassert godkjennes; pilotbildene godkjent (forskyvning 0,73 og 0,25 px) |
| Pipeline | 10 tester, 9 uten spillfiler | `cd pipeline && pytest`, og `pytest -m "not game"` i CI på hver push |

## Nettleser og GitHub Pages

[Nettsiden](https://tombonator3000.github.io/Dig-HD-Web/) går rett inn i
spillet, som originalen, uten oppsettside eller knapper (endret 9. oktober
etter beskjed fra Tom). Første gang ber den om en lesenøkkel til dette repoet.
Spillet og HD-pakken hentes så fra grenene `spilldata` og `hd-mod` via
api.github.com når spillet trenger dem, og lagres i nettleseren etter
git-blob-ID. Ny HD-grafikk kommer med av seg selv ved neste start. Mapper på
maskinen virker fortsatt som reserve. HD eller originalgrafikk velges i
spillets egen meny (F5, HD Graphics), og valget huskes. Mobil: fullskjerm ved
første trykk, to fingre åpner menyen, tre hopper over en scene.

Berøring (endret 9. oktober etter Toms første test på mobil): siden tar over
berøringen selv (`engine/pages/touch.mjs`). Trykk er klikk, dra flytter
pekeren, hold er høyreklikk, to fingre gir menyen, tre hopper over en scene.
Skjermen snus ikke lenger. Filer som ikke kommer fram (Tom fikk "Failed to
fetch" for FONT1.NUT og ScummVMs feilsøkingskonsoll), prøves igjen til de
kommer. Musikk og tale ligger i deler på 90 MB i `spilldata` og settes sammen i
nettleseren; uten lyd med `?uten-lyd` og på enheter med under 4 GB minne. Med
lyd brukte Chromium omtrent 0,9 GB JavaScript-minne og 0,37 GB
WebAssembly-minne.

Nettsiden ligger i det offentlige motorrepoet `Tombonator3000/Dig-HD-Web`
(GitHub avviste Pages fra det private repoet med gjeldende abonnement). Den har
bare motor, temaer og tilhørende GPL-kode, med samme patch og sidefiler som
`main`. Actions bygger og publiserer (siste bygg 9. oktober bestått).

Testet 9. oktober i Chromium uten skjerm mot den publiserte siden: nøkkelfeltet
første gang, rett inn i introen og videre til rom 22, F5 med raden HD Graphics,
klikk på boksen ga klassisk grafikk, Play, og etter omlasting rett inn i spillet
i klassisk grafikk uten nøkkelfelt og uten at noen fil ble hentet på nytt.
Ingen forespørsler med spill- eller HD-stier mot nettsiden. Filtester: 9
bestått. Tidligere tester (Codex) med mapper: lagring og lasting av spill,
HD-figurene fra fig014_01.

Testet 9. oktober mot den publiserte siden i Chromium uten skjerm som telefon
(liggende og stående, ekte berøringshendelser): tre fingre hoppet over introen,
trykk, hold, to fingre ga menyen, trykk på HD Graphics byttet grafikk, Play.
Musikk og tale lastet (ingen "Can't open bundle file"). Ingen feil.
I et hopp med testkroken (`?rom=22`) stoppet motoren én gang på en assert i
skriptene etter hold og tre fingre; testhoppet etterlater skriptene i en
tilstand spillet aldri er i (loggen sier "Script 2000 stopped with active
cutscene"), og det skjedde ikke fra vanlig start.

Ikke testet: en ekte nøkkel (i testmiljøet gir proxyen selv tilgang til
GitHub), ekte telefon, hvordan telefonen tåler minnet med lyd, full
gjennomspilling.

PC (endret 9. oktober etter Toms test på Kubuntu: ingen musepeker, ingen
knapper): første start laster ned talen, musikken, spillet og introfilmen
(omtrent 530 MB) før noe vises, og det viser siden nå i et eget bilde.
Fullskjerm kommer ved første klikk eller tast. Uten WebGL tegner ScummVM med
programvare. Testet i Firefox 157 mot den publiserte siden uten WebGL
(introen, Esc, rom 2, F5, klikk på HD Graphics, musepekeren vises) og med
WebGL under Xvfb (nedlastingsbildet, introen). Fullskjerm testet i Chromium.
Ikke testet: tastene i fullskjerm (testriggen sender ingen taster i
fullskjerm) og Toms egen maskin.

## Linux-pakken

Én fil med alt: `TheDigHD-x86_64.AppImage` (765 MB) i den private releasen
[linux](https://github.com/Tombonator3000/Dig-HD-Remake/releases/tag/linux):
ScummVM med HD-patchen, spillet, musikk, tale og HD-modden. Starter rett i
spillet i fullskjerm. Innstillinger i `~/.config/the-dig-hd`, lagrede spill i
`~/.local/share/the-dig-hd/saves`.

Lages av arbeidsflyten Linux-pakke på Ubuntu 22.04 (glibc 2.35) når motoren
eller pakkeskriptet endres, og hver natt hvis `hd-mod` er endret. Testet i
arbeidsflyten 9. oktober: pakken uten skjerm (rom 22, F5 og klikk på HD
Graphics ga klassisk, valget lagret, ingen "Can't open bundle file") og på
Debian 12 med bare skrivebordsbibliotekene (ingen manglende biblioteker, rom 22
lastet). AppDir og oppstarten også testet her. Ikke testet: en ekte
Linux-maskin med skjerm og lyd, FUSE på Toms maskin, Wayland.

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
