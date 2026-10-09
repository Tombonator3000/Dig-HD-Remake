# Spilltest

Slik spiller og tester du HD-versjonen rett fra repoet, og hva du bør se etter.

## Første gang

Linux (testet med Ubuntu og Fedora-pakkene under). Installer det motoren trenger:

```sh
sudo apt install build-essential git pkg-config libsdl2-dev libpng-dev zlib1g-dev     # Ubuntu/Debian
sudo dnf install gcc-c++ make git pkgconf SDL2-devel libpng-devel zlib-devel          # Fedora
```

Hent repoet og start:

```sh
git clone https://github.com/Tombonator3000/Dig-HD-Remake.git
cd Dig-HD-Remake
./spill.sh
```

Første gang henter skriptet spillfilene (grenen `spilldata`) og siste HD-mod (grenen `hd-mod`), og bygger motoren. Det tar noen minutter. Senere starter det med en gang, og henter bare ny HD-mod og bygger motoren på nytt når den er endret.

Musikk og tale ligger i grenen `spilldata` i deler på 90 MB (GitHubs grense er 100 MB per fil). `tools/hent_spilldata.sh` setter dem sammen til `game/DIGMUSIC.BUN` og `game/DIGVOICE.BUN` og sjekker sjekksummene.

## Valg

| Kommando | Hva |
| --- | --- |
| `./spill.sh` | Vanlig start med HD-modden |
| `./spill.sh --rom 22` | Hopper til rom 22 like etter starten, for å se på ett rom. Filmene hoppes over. Spillet er ikke i normal tilstand etter et hopp, så bruk det til å se, ikke til å spille videre |
| `./spill.sh --klassisk` | Starter med originalgrafikken |
| `./spill.sh --gult` | Farger gult der HD mangler |
| `./spill.sh --auto` | Fyller rom og objekter som ChatGPT ikke har laget ennå, med automatisk oppskalering. Krever Python 3.12. Første gang tar det 5 til 10 minutter |
| `./spill.sh --fort` | Starter uten å hente eller bygge noe |
| `./spill.sh --fullskjerm` | Fullskjerm |
| `./spill.sh --programvare` | Uten OpenGL. Bruk den hvis spillet ikke starter og terminalen sier "Could not load any graphics mode" |
| `git pull && ./spill.sh` | Siste versjon av koden og modden |

Andre valg sendes videre til ScummVM.

## Taster i spillet

| Tast | Hva |
| --- | --- |
| Ctrl+H | Bytter mellom HD og originalgrafikken |
| Ctrl+Shift+H | Gult felt der HD mangler, av og på |
| Alt+S | Skjermbilde (lagres i mappen ScummVM skriver ut i terminalen) |
| F5 | Spillmenyen (lagre, laste, avslutte) |
| Ctrl+F5 | ScummVM-menyen |

## Hva du bør se etter

HD fra ChatGPT finnes i over halvparten av rommene (se `STATUS.md`). Resten vises som originalen skalert opp, eller med automatisk oppskalering med `--auto`.

1. Rom 22 (`./spill.sh --rom 22`): stranden i HD. Vannet skal bevege seg jevnt, uten ruter eller blokker. Bytt med Ctrl+H og se at alt står på samme sted.
2. Rom 9 (`./spill.sh --rom 9`): kjernen. Se at figurer går bak ting i forgrunnen der de skal, og at kanter og dører ligger der de lå.
3. Rom 28 (`./spill.sh --rom 28`): tavla. Hele skjermen er et stort objektbilde; HD for det kommer fra ChatGPT senere.
4. Introen og den første scenen i romfergen (`./spill.sh`): teksten og undertekstene skal være glatte og stå der de står i originalen. Ingen tekst skal bli stående igjen.
5. Volumbanneret (Shift+P) og menyen (F5) over en figur: ingen figur skal skinne gjennom boksen.
6. Gå mellom rom med og uten HD, og se at spillet ikke krasjer eller blinker.
7. Ctrl+Shift+H: det gule skal vise nøyaktig det som mangler HD. Tekst og pekeren skal ikke bli gul.

## Uten skjerm: alle rom

```sh
tools/romtest.sh                     # alle rom med mods/gpt
tools/romtest.sh --rom 2,9,22        # noen rom (--rom 20-30 for et område)
tools/romtest.sh --mod test-nearest  # en annen mod
tools/romtest.sh --kamera ett        # bare der spillet selv setter kameraet
tools/romtest.sh --objekter          # i tillegg alle tilstandene til alle objektene i hvert rom
tools/romtest.sh --bare-rapport      # rapport og ark på nytt fra kjøringene som finnes
```

Skriptet kjører motoren uten skjerm (SDL dummy) én gang per rom og hopper til rommet med `DIGHD_TEST_ROOM`. I rom som er bredere eller høyere enn skjermen, kjører det i tillegg med kameraet satt (`DIGHD_TEST_CAMX` og `DIGHD_TEST_CAMY`) så hele rommet blir vist. Etter 600 bilder lagres skjermen i HD og med originalpikslene. Forlater spillet rommet før det første bildet (rom 1, 10 og 104), kjøres det en gang til med et bilde hvert 10. bilde. To kjøringer går samtidig. Alle 111 rom (226 kjøringer) tok 25 minutter her. Motoren er `$SCUMMVM_SRC/scummvm` eller `engine/scummvm/scummvm` (`--motor` for en annen).

For hver kjøring samles: om rommet ble lastet, om motoren krasjet eller hang (tidsgrense 180 sekunder), om HD-bakgrunnen ble lastet og brukt, andelen piksler fra HD-bakgrunn, HD-objekt, HD-figur og originalen i det siste bildet (linjen `whole screen` i loggen, se `docs/HD-MOTOR.md`), og avviket fra originalen (`DIGHD_VERIFY`). Bildene sammenlignes også i skriptet: forskyvning av HD-bildet, svarte felt der originalen ikke er svart, og de største avvikene. Der lages det nærbilder, og i rom med forgrunnsmasker nærbilder av figurene, så en kan se om de går bak det samme i HD som i originalen. Til slutt måles sømmene mellom HD-objekter og HD-rommet i modden: der et objekt er likt rombakgrunnen, viser motoren HD-rommet, og der objektet skiller seg fra den, HD-objektet. Er de to bildene laget hver for seg, kan grensen synes.

Resultatet ligger i `work/romtest`: `RAPPORT.md` (sammendrag og tabeller), `romtest.csv`, `somer.csv`, kontaktark `ark_NN.png` med HD og originalen side om side for hvert rom, en mappe per kjøring med logg og bilder, og `naerbilder/`. Med `--objekter` også `objekter.csv` (se under). Notater fra gjennomsynet kan skrives i `work/romtest/FUNN.md`, og kommer med i rapporten neste gang den lages. Stien i `--ut` kan være relativ; skriptet gjør den absolutt, fordi motoren kjører i en egen mappe.

Hoppet setter ikke spillet i vanlig tilstand. Figurer og objekter kan mangle eller stå et annet sted enn i vanlig spill, og noen rom starter en film eller bytter rom selv. Testen fanger krasj, rom som ikke lastes, rom der HD-bakgrunnen ikke brukes og tydelige feil i bildet, ikke feil som bare viser seg i vanlig spill.

### Objekttilstander

Etter hoppet står hvert objekt i tilstanden skriptene ga det, så HD-bildene for de andre tilstandene (`objNNN_02.png` og videre) blir ikke prøvd i den vanlige kjøringen. Med `--objekter` kjøres hvert rom som har objekter, én gang til med `DIGHD_TEST_OBJSTATE=alle` (se Objekttilstander i testen i `docs/HD-MOTOR.md`). Motoren setter hvert objekt i hver tilstand slik skriptene gjør det, viser tilstanden i 40 bilder (`--objekt-bilder`) og lagrer skjermen i HD og med originalpikslene. Objektet settes tilbake før neste objekt, og kameraet flyttes til objekter som ikke er på skjermen. Kjøringen heter `romNNN_objekter`.

For hvert objekt og hver tilstand står dette i rapporten (avsnittet Objekttilstander) og i `objekter.csv`:

- Status: `HD brukt`, `likt rommet` (objektet er likt rombakgrunnen overalt, og motoren viser HD-rommet), `ikke i modden`, `HD-bildet ikke lest` (finnes, men har for eksempel feil størrelse), `ikke tegnet`, `ikke på skjermen` eller `utelatt` (BOMP-bilder som skriptene tegner som blast-objekter).
- HD-andel: hvor stor del av objektets egne synlige piksler som kom fra HD-objektet. Objektpikslene er de som ikke er gjennomsiktige, ikke like rombakgrunnen der modden har HD-rommet, og ikke dekket av noe annet. Talt i motoren.
- Snitt og sterkt avvik: HD-bildet skalert ned mot originalpikslene i objektpikslene (fra uttrekket), største kanal. Sterkt er over 56.
- Om skjermen var lik hele skjermen bygget på nytt etter byttet (`DIGHD_VERIFY`), og merknader: forelder satt, tilstanden endret av spillet, kameraet flyttet tilbake av et skript.
- Nærbilde i `naerbilder/objNNN_SS_romRRR.png` med HD til venstre og originalen til høyre.

Tid og plass: med to kjøringer samtidig tok rom 85 (64 tilstander) 65 sekunder og rom 23 (29 tilstander) 28 sekunder. `tools/romtest.sh --objekter --kamera ett` for alle 111 rom (111 vanlige kjøringer og 72 med objekttilstander) tok 16 minutter og 730 MB. Hver tilstand gir to bilder på omtrent 1 MB til sammen. Resultatet fra 2026-10-07 står under Hva som er testet i `docs/HD-MOTOR.md`.

Et objekt som et annet objekt dekker i tilstanden etter hoppet, får status `dekket`. Det kan testes for seg med en liste, der det som dekker får tilstand 0:

```sh
mkdir -p /tmp/dump
DIGHD_MOD="$PWD/mods/gpt" DIGHD_TEST_ROOM=100 DIGHD_TEST_OBJSTATE=769:0,775:5 DIGHD_SKIP_VIDEO=1 \
  DIGHD_DUMP_DIR=/tmp/dump DIGHD_DUMP_FLAT=1 DIGHD_QUIT_AT=400 \
  engine/scummvm/scummvm --path="$PWD/game" --debuglevel=1 dig 2>&1 | grep "DigHD: test"
```

Skjermen lagres i `/tmp/dump` 40 bilder etter at tilstandene er satt, og linjen `test object 775 state 5` sier om HD-bildet ble brukt.

## I nettleseren

```sh
./spill.sh --nettleser
```

Skriptet henter spillfilene og siste HD-mod som før, bygger ScummVM med HD-patchen for nettleseren (WebAssembly med Emscripten) og starter en webserver på maskinen. Åpne adressen det skriver ut, vanligvis http://localhost:8000. Ctrl+C i terminalen stopper serveren.

**Bare lokalt.** Spillet og HD-grafikken tilhører Disney/Lucasfilm. Nettleserversjonen skal bare kjøres på din egen maskin, og ingenting fra den skal legges på GitHub Pages eller en annen åpen adresse eller lastes opp noe sted. Derfor:

- webserveren (`engine/web/server.py`) lytter bare på 127.0.0.1 og svarer bare på forespørsler til localhost,
- siden (`engine/web/index.html`) nekter å starte hvis den er åpnet fra en annen adresse enn localhost,
- alt som serveres, ligger i `work/nettleser`, og byggefilene i `engine/emsdk` og `engine/scummvm-web`. Alle tre er ignorert av git.

Krav: git, make, python3, pkg-config, xz og zip, og en nyere Chrome, Edge eller Firefox.

```sh
sudo apt install git make python3 pkg-config xz-utils zip     # Ubuntu/Debian
sudo dnf install git make python3 pkgconf xz zip              # Fedora
```

Første gang installeres Emscripten 4.0.10 i `engine/emsdk` (omtrent 350 MB), og ScummVM hentes til `engine/scummvm-web`. Det er den versjonen ScummVM sin egen byggeoppskrift (`dists/emscripten/build.sh`) bruker på den låste commiten. Bygget tok omtrent 5 minutter på en maskin med 2 kjerner. Motoren bygges på nytt når patchen, ScummVM-versjonen eller `engine/build-web.sh` er endret (stempel i `engine/scummvm-web/.dighd-stempel`).

| Kommando | Adresse | Hva |
| --- | --- | --- |
| `./spill.sh --nettleser` | http://localhost:8000/ | Vanlig start med HD-modden |
| `./spill.sh --nettleser --rom 22` | http://localhost:8000/?rom=22 | Hopper til rom 22, filmene hoppes over |
| `./spill.sh --nettleser --klassisk` | http://localhost:8000/?klassisk=1 | Starter med originalgrafikken |
| `./spill.sh --nettleser --gult` | http://localhost:8000/?gult=1 | Gult felt der HD mangler |
| `./spill.sh --nettleser --auto` | http://localhost:8000/?mod=auto | Med automatisk oppskalering for resten |
| `./spill.sh --nettleser --fort` | | Starter uten å hente eller bygge noe |
| `./spill.sh --nettleser --port 8001` | http://localhost:8001/ | En annen port, hvis 8000 er i bruk |

Valgene kan også skrives rett i adressen mens serveren går, for eksempel http://localhost:8000/?rom=9, og siden lastes på nytt. For test og feilsøking kan variablene i `docs/HD-MOTOR.md` settes på samme måte, for eksempel `?DIGHD_VERIFY=1`.

Tastene er de samme som ellers. Siden stopper nettleserens egne snarveier for F1 til F10 og for Ctrl og Alt med en bokstav, så F5 skal åpne spillmenyen i stedet for å laste siden på nytt, og Ctrl+H skal gå til spillet i stedet for historikken. F11 gir fullskjerm.

Lagring: lagrede spill og innstillingene ligger i nettleseren (IndexedDB for localhost og porten), ikke i repoet. De blir borte hvis du sletter nettstedsdataene for localhost, og port 8000 og 8001 har hver sine.

Slik virker det: `engine/run-web.sh` legger nettleserversjonen, spillfilene og modden i `work/nettleser`. Spillfilene og modden legges inn som lenker under `data/`, og det lages en `index.json` i hver mappe. Nettleserversjonen av ScummVM henter filene under `/data` over HTTP når de trengs (`backends/fs/emscripten/http-fs.cpp`). DigHD leser modden gjennom ScummVM sitt filsystem og innstillingene fra miljøvariabler, som siden setter fra adressen før spillet starter. Patchen er derfor ikke endret for nettleseren.

Testet 2026-10-07 her, i Chromium uten skjerm (Playwright, programvaregrafikk), med modden fra grenen `hd-mod` (54 rom):

- `./spill.sh --nettleser --rom 22` fra en arbeidskopi uten modden og uten motoren: modden ble hentet, motoren bygget, serveren startet og rom 22 vist med HD-bakgrunnen. Ny kjøring bygget ikke på nytt.
- Introen går, og undertekstene er HD-tekst. Rom 22 og 9 vises med HD-bakgrunn, og vannet i rom 22 beveger seg.
- Ctrl+H (klassisk og tilbake), Ctrl+Shift+H (gult felt) og F5 (spillmenyen) gjennom nettleserens tastehendelser. Tastene må holdes slik et menneske gjør: ScummVM leser Ctrl og Shift når spillet henter tasten, så et trykk der alt slippes i samme øyeblikk, mister Ctrl.
- Lagring med Alt+1 og lasting med Ctrl+1, også etter at siden var lastet på nytt.
- Kontrollen fra `engine/test.sh` i nettleseren (modden `test-nearest`, 3000 bilder, `DIGHD_VERIFY=1`): skjermen var lik hele skjermen bygget på nytt i alle 12 dumper, og avvik fra originalen bare i skalerte figurer (0,005 til 0,174 prosent), som i den vanlige motoren. Bilde 500 hadde 1753 avvikende piksler begge steder, indre kanter i en astronaut.
- Fart: spillet holdt samme tempo som den vanlige motoren. 1200 bilder etter hoppet til rom 22 tok 12,0 sekunder i nettleseren og 11,5 sekunder i den vanlige motoren uten skjerm. Skjermen ble tegnet omtrent 12 ganger i sekundet, like ofte som spillet endrer bildet. Å bygge hele HD-skjermen (`DIGHD_BENCH`) tok 13 til 25 ms i nettleseren mot 8,5 til 12 ms i den vanlige motoren, og ett steg i fargesyklingen 1 til 6 ms mot 0 til 4 ms. Den vanlige motoren uten skjerm bruker 16 bit per piksel, nettleseren 32.

Ikke testet: en vanlig nettleser med skjermkort, ekte tastatur og mus, at F5 og Ctrl+H ikke når nettleseren (nettleseren uten skjerm har ikke disse snarveiene), lyd (musikk og tale mangler her), Firefox, Safari og Edge, fullskjerm og lange økter.

Kjente begrensninger:

- Alt spillet leser (DIG.LA1 på 88 MB, filmene og HD-bildene), hentes første gang det trengs og blir liggende i minnet til siden lukkes. En lang økt kan derfor bruke flere hundre MB.
- Som i den vanlige motoren vises HD-skjermen i 16:10 (1280 x 800) med svarte felt. ScummVM retter bildeforholdet bare for 200 og 400 linjer.
- Innstillingene i `engine/web/scummvm.ini` brukes bare første gang. Etterpå er det nettleserens kopi som gjelder.

## Fra GitHub Pages, uten å bygge noe

https://tombonator3000.github.io/Dig-HD-Web/ går rett inn i spillet, på PC og mobil. Nettsiden har bare motoren. Spillet og HD-grafikken hentes fra grenene `spilldata` og `hd-mod` i dette repoet når spillet trenger dem, og lagres i nettleseren.

Første gang spør siden etter en lesenøkkel til repoet. Lag den på https://github.com/settings/personal-access-tokens/new:

1. Token name: for eksempel The Dig HD. Expiration: etter eget valg.
2. Repository access: Only select repositories, velg Dig-HD-Remake.
3. Permissions, Repository permissions: Contents, Read-only.
4. Generate token, kopier nøkkelen, lim den inn på siden og trykk **Spill**.

Etterpå går lenken rett inn i spillet. Ny HD-grafikk i `hd-mod` kommer med av seg selv neste gang siden åpnes. Utløper nøkkelen, spør siden etter en ny. `?ny-nokkel` bak adressen gir feltet med en gang.

- **Grafikk:** F5, så **HD Graphics** i menyen (kryss er HD, tom boks er originalgrafikken). Valget huskes.
- **Mobil og nettbrett:** trykk er klikk, dra flytter pekeren, hold fingeren i ro et halvt sekund for høyreklikk, to fingre åpner menyen, tre fingre hopper over en filmscene. Første trykk gir fullskjerm, og skjermen snus ikke.
- **Lyd:** musikk og tale hentes første gang spillet spiller musikk (391 MB, siden viser hvor langt den har kommet). `?uten-lyd` bak adressen starter uten, og på enheter med under 4 GB minne er lyden av.
- **Nett:** mistes kontakten, venter spillet og siden prøver igjen til filen kommer.
- **Første start:** et svart bilde viser at talen, musikken, spillet og introfilmen lastes ned (omtrent 530 MB). Bare første gang.
- **Fullskjerm:** kommer ved første klikk eller tast. Firefox går ut av fullskjerm på Esc; neste klikk gir den igjen.
- **Uten WebGL:** siden tegner med programvare av seg selv; `?programvare` velger det.
- **Testvalg i adressen:** `?rom=22`, `?klassisk`, `?gult` og testkrokene, for eksempel `?rom=22&DIGHD_TEST_COSTUME=14` for å se Boston i alle retninger.

Uten nøkkel går det også med mapper på maskinen (lenken under nøkkelfeltet): spillmappen `game` og HD-mappen `mods/gpt`. Mappene kan lastes ned som zip uten git: https://github.com/Tombonator3000/Dig-HD-Remake/archive/refs/heads/spilldata.zip og https://github.com/Tombonator3000/Dig-HD-Remake/archive/refs/heads/hd-mod.zip.

Testet 2026-10-09 i Chromium uten skjerm (Playwright): nøkkelfeltet første gang, så rett inn i introen med fillisten og filene hentet fra api.github.com, og rett inn i spillet uten nøkkelfelt etter omlasting, uten at noen fil ble hentet på nytt. Ingen forespørsler med spill- eller HD-stier mot nettsiden. I testmiljøet legger proxyen til egen tilgang mot GitHub, så en ekte nøkkel er ikke prøvd; at GitHub avviser en feil nøkkel, er bare testet med filtester. Menyvalget er testet i motoren uten skjerm (se `docs/HD-MOTOR.md`). Ikke testet: mobil, berøring og fullskjerm på ekte telefon.

## Linux: én fil med alt

Den komplette pakken er én AppImage med ScummVM med HD-patchen, spillet, musikk, tale og HD-grafikken (omtrent 950 MB). Den ligger under Releases i dette repoet, release `linux`: https://github.com/Tombonator3000/Dig-HD-Remake/releases/tag/linux. Repoet er offentlig, så filen kan lastes ned uten å logge inn.

```sh
chmod +x TheDigHD-x86_64.AppImage
./TheDigHD-x86_64.AppImage
```

Spillet starter rett, i fullskjerm, med introen som originalen. Alt+Enter bytter mellom vindu og fullskjerm. F5 åpner menyen; der velger HD Graphics HD eller originalgrafikk, og valget huskes. Innstillingene ligger i `~/.config/the-dig-hd/scummvm.ini`, lagrede spill i `~/.local/share/the-dig-hd/saves`. Mangler FUSE på maskinen (noen nyere Ubuntu-versjoner), start med `./TheDigHD-x86_64.AppImage --appimage-extract-and-run`.

Pakken lages av arbeidsflyten Linux-pakke (`.github/workflows/linux.yml`) på Ubuntu 22.04, så den går på distroer med glibc 2.35 eller nyere. Den henter spillet og lyden fra `spilldata` og HD-modden fra `hd-mod`, bygger motoren, lager AppImage med `tools/pakke_linux.sh` (linuxdeploy tar med SDL2 og libpng), tester den uten skjerm (rom 22, menyvalget, at musikk og tale finnes) og på Debian 12 uten byggepakker, og legger den i releasen. Den går av seg selv når motoren eller pakkeskriptet endres i `main`, og hver natt (02:17 UTC) hvis HD-modden i `hd-mod` er endret siden forrige pakke. Den kan også startes for hånd under Actions. `BYGG.txt` i pakken og notatene i releasen sier hvilken motor og hvilken HD-mod den er laget av.

`tools/pakke_linux.sh` kan også kjøres her. Uten `LINUXDEPLOY` og `APPIMAGETOOL` lager den bare mappen `out/linux/AppDir`, som startes med `out/linux/AppDir/AppRun`.

## Si fra

Skriv hva du så, i hvilket rom og omtrent hvor, og legg ved skjermbilde (Alt+S) hvis du kan. Gi det til Claude i chatten, eller legg det i `rapporter/` i grenen `gpt-arbeid`.
