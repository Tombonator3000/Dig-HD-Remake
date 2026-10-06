# The Dig HD Remake

HD-versjon av LucasArts' The Dig (1995). Spillet kjører i ScummVM som før, men bakgrunner, objekter, figurer og filmer vises i 4x oppløsning fra en mod-mappe. Det som ikke har en HD-versjon ennå, vises som originalen skalert opp, så spillet kan spilles hele veien mens grafikken bygges.

Repoet er privat. Spillfilene ligger i grenen `spilldata` og skal aldri inn i `main`.

## Innhold

| Mappe | Hva |
| --- | --- |
| `pipeline/` | `dighd`: eksporterer originalgrafikken, skalerer opp og bygger mod-mapper |
| `engine/` | Patch for ScummVM og skript for å bygge, kjøre og teste |
| `tools/` | Henting av spilldata, lesing av DIG.LA0 |
| `docs/` | Analysen, romoversikten og beskrivelse av HD-motoren |

## Kom i gang (Linux)

```sh
# 1. Spillfilene (fra grenen spilldata)
tools/hent_spilldata.sh

# 2. Pipelinen
python3 -m venv .venv && . .venv/bin/activate
pip install -e "pipeline[dev]"
dighd info

# 3. Eksporter originalgrafikken (rom, objekter og 28 490 kostymeruter, cirka 3 minutter)
dighd extract

# 4. Lag en HD-mod (her med enkel oppskalering, alle rom og objekter, kostyme 1-20)
dighd build-mod --name hd --method lanczos-sharp --kostymer 1-20

# 5. Bygg ScummVM med patchen og start spillet
sudo apt install build-essential git libsdl2-dev libpng-dev zlib1g-dev
engine/build.sh
engine/run.sh hd
```

Musikk og tale (`DIGMUSIC.BUN`, `DIGVOICE.BUN`) er for store for GitHub. Legg dem fra Drive i `game/` for å spille med lyd.

## Bedre oppskalering

`--method` kan være `nearest`, `lanczos`, `lanczos-sharp`, `realesrgan` eller `cmd`:

```sh
# Real-ESRGAN (last ned realesrgan-ncnn-vulkan og legg den i PATH)
dighd build-mod --name esrgan --method realesrgan --kostymer 14-18

# Hvilket som helst verktøy som tar inn- og utfil
dighd build-mod --name test --method cmd --cmd "mittverktoy {inn} {ut} {skala}"

# Egne bilder (maling, KI-verktøy): samme navn og eksakt 4x størrelse
dighd build-mod --name hd --egne mine_hd_bilder/
```

`dighd compare --room 22` lager et bilde med flere metoder side om side, nyttig for stiltester.

Filmer: `dighd san` trekker ut alle 12 638 filmrammer. `dighd build-mod --filmer SQ1` skalerer dem opp. Det tar mye plass som PNG, så velg filmene du tester.

## Test

```sh
cd pipeline && pytest            # pipelinen
pytest -m game                   # mot de ekte spillfilene
engine/test.sh                   # kjører spillet uten skjerm og sjekker at HD-pikslene ligger riktig
```

Mer om hvordan motoren virker: `docs/HD-MOTOR.md`. Analyse og plan: `docs/ANALYSE.md`.

## Opphavsrett

The Dig eies av Disney/Lucasfilm. Patchen og pipelinen kan deles (ScummVM er GPL-3.0). Spillfiler og HD-grafikk laget fra dem skal ikke deles. Konseptbildene i roten er laget av en Reddit-tegner og brukes bare som stilreferanse.
