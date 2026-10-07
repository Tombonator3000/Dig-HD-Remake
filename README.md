# The Dig HD Remake

HD-versjon av *The Dig* (LucasArts 1995). Spillet kjører i ScummVM med en patch som legger HD-grafikk nøyaktig oppå originalen: bakgrunner, objekter, figurer og filmer i 4x oppløsning fra en mod-mappe. Det som ikke har en HD-versjon ennå, vises som originalen skalert opp, så spillet kan spilles hele veien mens grafikken bygges.

Spillets regler, skript, lagring og lyd er ScummVM sine og helt som før. Bare bildet endres.

Arbeidsdeling: Claude skriver koden, ChatGPT lager HD-grafikken etter [bestillingen](docs/BESTILLING-CHATGPT.md), Tom godkjenner.

Repoet er privat. Spillfilene og alt som lages fra dem ligger i egne grener og skal aldri inn i `main`.

## Status

| Del | Status |
| --- | --- |
| Spillfiler | Engelsk standardutgave (DIG.LA0 MD5 `d8323015...`). LA0, LA1 og VIDEO i grenen `spilldata`. Musikk og tale bare på Drive. |
| Uttrekk | Alle 111 rom, 642 objektbilder, 28 490 kostymeruter (med fargene spillet viser, også for kodek 5 og 16) og 12 638 filmrammer ut som PNG. |
| HD-motor | ScummVM-patch med HD-bakgrunner, HD-objekter, HD-sprites (alle tre kostymekodekene) og HD-filmrammer, fargejustering ved palettbytte, mus og peker i HD. Testet uten skjerm (0 avvik med nearest-mod) og kjørt på laptopen med OpenGL og 32-bits farger. |
| HD-grafikk | 3 av 106 rom ferdige fra ChatGPT (rom 9, 22 og 28), og 0 av 30 store objektbilder. 188 av 192 jobber igjen. Oppdateres hver runde i `work/gpt/RAPPORT.md` og grenen `gpt-arbeid`. |
| Objekter og figurer | Bare automatisk oppskalering så langt. Egne runder med ChatGPT kommer etter rommene. |
| Filmer | Utskifting av rammer virker og er testet. Ingen HD-filmer laget ennå. |

Detaljer, tester og kjente begrensninger: [STATUS.md](STATUS.md). Hva som gjenstår: [todo.md](todo.md).

## Spille med HD-grafikken

```sh
sudo apt install build-essential git pkg-config libsdl2-dev libpng-dev zlib1g-dev   # én gang (Ubuntu/Debian)
git clone https://github.com/Tombonator3000/Dig-HD-Remake.git && cd Dig-HD-Remake
./spill.sh
```

`spill.sh` henter spillfilene og siste HD-mod, bygger motoren første gang (noen minutter) og når den er endret, og starter spillet. `./spill.sh --rom 22` hopper til et rom, `--klassisk` starter med originalgrafikken, `--gult` viser hvor HD mangler, og `--auto` fyller resten med automatisk oppskalering. Legg `DIGMUSIC.BUN` og `DIGVOICE.BUN` fra Drive i `game/` for musikk og tale.

Mens du spiller: Ctrl+H bytter mellom HD og klassisk grafikk, og Ctrl+Shift+H farger gult der HD mangler. Hva du bør se etter, og alle valgene: [docs/SPILLTEST.md](docs/SPILLTEST.md).

Det samme steg for steg: `tools/hent_spilldata.sh`, `tools/mod_gren.sh hent`, `engine/build.sh`, `engine/run.sh gpt`.

## Lage HD-grafikk selv

```sh
python3 -m venv .venv && . .venv/bin/activate
pip install -e "pipeline[dev]"
dighd info                       # sjekker spillfilene
dighd extract                    # originalgrafikken til work/extract (cirka 3 minutter)
dighd build-mod --name hd --method lanczos-sharp --kostymer 1-20
engine/run.sh hd
```

`--method` kan være `nearest`, `lanczos`, `lanczos-sharp`, `realesrgan` (realesrgan-ncnn-vulkan i PATH) eller `cmd` (`--cmd "verktoy {inn} {ut} {skala}"`). Egne bilder med samme navn og eksakt 4x størrelse brukes med `--egne MAPPE`. `dighd compare --room 22` viser flere metoder side om side. `dighd san` trekker ut filmrammene, og `--filmer SQ1` tar dem med i modden.

## Samarbeidet med ChatGPT

En runde (Claude kjører den jevnlig):

```sh
tools/gpt_runde.sh               # henter, kontrollerer, bygger og publiserer modden, skriver ny ordre
```

Det samme steg for steg:

```sh
dighd gpt-pakke                  # 162 jobber for 106 rom og 30 for store objektbilder i work/gpt
tools/gpt_gren.sh send           # jobbene, status og ordre til grenen gpt-arbeid
tools/gpt_gren.sh hent           # resultatene fra ChatGPT tilbake
dighd gpt-inn                    # plassering, fargelås, sammensying, RAPPORT.md og retur.md
dighd gpt-ordre                  # ORDRE.md med de neste jobbene
dighd build-mod --name gpt --egne work/gpt-ferdig
tools/mod_gren.sh send           # modden til grenen hd-mod
```

ChatGPT jobber i grenen `gpt-arbeid` og leser `ORDRE.md` først. `GRAFIKKLISTE.md` i samme gren har alt som skal lages, i prioritert rekkefølge og delt i bestillinger. Regler og format: [docs/BESTILLING-CHATGPT.md](docs/BESTILLING-CHATGPT.md).

## Test

```sh
cd pipeline && pytest -m "not game"   # pipelinen uten spillfiler (kjøres også i CI)
cd pipeline && pytest -m game         # mot de ekte spillfilene
engine/test.sh                        # spillet uten skjerm: HD-pikslene skal ligge der originalen har dem
```

## Grener

| Gren | Innhold |
| --- | --- |
| `main` | Kode og dokumentasjon. Ingen spillfiler eller grafikk. |
| `spilldata` | Spillfilene (DIG.LA0, DIG.LA1, VIDEO/) med sjekksummer. Privat. |
| `gpt-arbeid` | Arbeidsbordet med ChatGPT: jobber, resultater, status, ordre og stilankere. Privat. |
| `hd-mod` | Siste ferdige HD-mod, én commit som erstattes hver runde. Privat. |
| `grafikkdata/pilot-20261006` | Grafikkpiloten fra Codex med prompter og kjøringsbevis. Privat. |

## Mappene

```
pipeline/dighd/   gamedata (LA0/LA1), export, upscale, modpack, gpt (jobber og kontroll), cli
pipeline/tests/   tester for pipelinen
engine/           patches/ (ScummVM-patchen), SCUMMVM_COMMIT, build.sh, run.sh, test.sh
tools/            hent_spilldata.sh, gpt_runde.sh, gpt_gren.sh, mod_gren.sh, la0_info.py,
                  check_hd_art.py, hent_grafikkpilot.sh
docs/             ANALYSE, HD-MOTOR, BESTILLING-CHATGPT, GRAFIKKPILOT, rom-oversikt.csv,
                  gpt-romnotater.csv, gpt-arbeid-AGENTS.md, kostymefarger.csv (rom og palett
                  for kostymer med kodek 5 og 16), konsept/ (stilreferanser)
game/             spillfilene (lokalt, fra spilldata)
work/             uttrekk, jobber og mellomresultater (lokalt)
mods/             ferdige mod-mapper (lokalt)
```

## Dokumentasjon

- [STATUS.md](STATUS.md): hva som virker, hva som er testet og hva som mangler
- [docs/SPILLTEST.md](docs/SPILLTEST.md): spille og teste rett fra repoet, og hva du bør se etter
- [docs/HD-MOTOR.md](docs/HD-MOTOR.md): hvordan HD-motoren bestemmer hvor hver piksel kommer fra
- [docs/BESTILLING-CHATGPT.md](docs/BESTILLING-CHATGPT.md): bestillingen til ChatGPT
- [docs/GRAFIKKPILOT.md](docs/GRAFIKKPILOT.md): første grafikkpilot fra Codex
- [docs/ANALYSE.md](docs/ANALYSE.md): analysen av spillfilene og planen
- [AGENTS.md](AGENTS.md), [memory.md](memory.md), [todo.md](todo.md), [log.md](log.md): for alle som jobber i repoet

## Lisenser og opphavsrett

Egen kode i prosjektet er laget for Tom. ScummVM-patchen er GPL-3.0 som ScummVM. thedig-textures (dekoderne pipelinen bruker) er GPL-3.0. *The Dig* tilhører Disney/Lucasfilm. Spillfiler og HD-grafikk laget fra dem skal ikke deles. Konseptbildene i `docs/konsept/` er laget av en Reddit-tegner og brukes bare som stilreferanse; spør og krediter før noe vises offentlig.
