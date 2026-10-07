Disse er for Codex eller ChatGPT med tilgang til laptopen og repoet. Ta én om gangen, og skriv i `rapporter/` i denne grenen hva du gjorde og fant.

1. **Test HD-modden på laptopen med skjerm og tastatur.** `git checkout main && git pull && ./spill.sh` henter, bygger og starter alt. Gå til rom 9, 22 og 28 med `./spill.sh --rom 22` og så videre. Følg `docs/SPILLTEST.md`. Sjekk:
   - at figurer går bak ting i forgrunnen der de skal,
   - at objekter bytter bilde riktig,
   - at Ctrl+H bytter mellom HD og klassisk, og at Ctrl+Shift+H viser gult felt der HD mangler, med melding på skjermen.
   - at vannet i rom 22 er HD og beveger seg jevnt, uten rutenett,
   - at teksten (replikker, menyer og undertekstene i introfilmen) er glatt og står der den skal,
   - at ingenting krasjer når du går mellom rom med og uten HD.
   Ta skjermbilder i `rapporter/laptop-test/` og skriv `rapporter/laptop-test.md`: hva du testet, hva som var feil, med rom og omtrentlig sted. Ikke rett i motoren selv. Beskriv feilen, så retter Claude den.
2. **Mål fart og lyd.** Kjør rom 22 i ett minutt med og uten modden, og noter bilder per sekund hvis ScummVM viser det, og om lyd eller tale hakker. Skriv det i `rapporter/laptop-test.md`.

Kodeendringer går som PR mot `main`, aldri rett i `main`. Skjermbilder og andre filer fra spillet skal bare ligge i denne grenen.
