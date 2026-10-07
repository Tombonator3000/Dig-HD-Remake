# Ordre fra Claude

Oppdatert 2026-10-07 10:58 (norsk tid)

Les denne filen før du starter. Den erstatter tidligere ordre.

## Status

- Jobber: 192. avvist 1, godkjent 98, ny 92, sjekk 1
- Ferdige rom: 53 av 106 (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 91, 92, 94, 95, 96, 97, 98, 99, 100, 102, 105, 106, 107, 108, 109, 110)
- Ferdige objekter: 10 av 30 (obj097_01, obj117_01, obj137_01, obj141_01, obj160_01, obj191_01, obj241_01, obj317_01, obj698_01, obj701_01)

## Gjør disse nå

1. `rom111` (rom 111, labcu3, del 1/1). Avvist: deler av bildet er flyttet eller zoomet (opptil 6.8 px). Les retur.md.
2. `rom039_del2av2` (rom 39, batdoor, del 2/2).
3. `rom040` (rom 40, mapcntl, del 1/1).
4. `rom041` (rom 41, falls, del 1/1).
5. `obj343_01` (rom 41, falls, objekt 343 tilstand 01, del 1/1).
6. `rom042` (rom 42, pit, del 1/1).
7. `rom043` (rom 43, fallsour, del 1/1).
8. `obj347_01` (rom 43, fallsour, objekt 347 tilstand 01, del 1/1).
9. `rom044_del1av2` (rom 44, nest, del 1/2).
10. `rom044_del2av2` (rom 44, nest, del 2/2).

Når disse er levert, fortsett med bestilling 2 i `GRAFIKKLISTE.md` uten å vente på ny ordre.

## Stilankere

- `stil/room009_core.png`
- `stil/room022_beach.png`

Legg ved det ankeret som ligner mest på rommet som bilde to.

## Leveringsformat

Begge formatene godtas av kontrollen:

- `resultat.png` på 1536 x 1024 med samme grå kant som `referanse.png`.
- `resultat.png` med bare bildet, i samme sideforhold som utsnittet (16:10 for vanlige rom, minst 1280 x 800). Slik pilotbildene ble levert.

Objektjobbene (`objNNN_SS`) er store bilder som spillet tegner over rommet (nærbilder, kart, paneler). De lages og leveres på samme måte. Utsnittet er da objektbildet, så leverer du bare bildet, skal det ha objektets sideforhold (se `bilde_i_lerret` i `jobb.json`).

Skriv `notat.md` i jobbmappen. Commit 5 til 10 jobber om gangen i grenen `gpt-arbeid` og push.

## Kodeoppgaver

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

## Neste sjekk

Claude henter grenen omtrent hver halvtime, kontrollerer leveransene, oppdaterer `status.csv`, `RAPPORT.md` og `retur.md`, og skriver ny ordre her.
