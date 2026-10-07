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

Musikk og tale ligger ikke i repoet (filene er for store). Legg `DIGMUSIC.BUN` og `DIGVOICE.BUN` fra Drive i `game/` for å få lyd.

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

HD fra ChatGPT finnes foreløpig i rom 9 (core), 22 (beach) og 28 (shardcu). Resten vises som originalen skalert opp, eller med automatisk oppskalering med `--auto`.

1. Rom 22 (`./spill.sh --rom 22`): stranden i HD. Vannet skal bevege seg jevnt, uten ruter eller blokker. Bytt med Ctrl+H og se at alt står på samme sted.
2. Rom 9 (`./spill.sh --rom 9`): kjernen. Se at figurer går bak ting i forgrunnen der de skal, og at kanter og dører ligger der de lå.
3. Rom 28 (`./spill.sh --rom 28`): tavla. Hele skjermen er et stort objektbilde; HD for det kommer fra ChatGPT senere.
4. Introen og den første scenen i romfergen (`./spill.sh`): teksten og undertekstene skal være glatte og stå der de står i originalen. Ingen tekst skal bli stående igjen.
5. Volumbanneret (Shift+P) og menyen (F5) over en figur: ingen figur skal skinne gjennom boksen.
6. Gå mellom rom med og uten HD, og se at spillet ikke krasjer eller blinker.
7. Ctrl+Shift+H: det gule skal vise nøyaktig det som mangler HD. Tekst og pekeren skal ikke bli gul.

## Si fra

Skriv hva du så, i hvilket rom og omtrent hvor, og legg ved skjermbilde (Alt+S) hvis du kan. Gi det til Claude i chatten, eller legg det i `rapporter/` i grenen `gpt-arbeid`.
