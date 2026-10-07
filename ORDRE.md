# Ordre fra Claude

Oppdatert 2026-10-07 12:14 (norsk tid)

Les denne filen før du starter. Den erstatter tidligere ordre.

## Status

- Jobber: 192. avvist 3, godkjent 172, ny 8, sjekk 9
- Ferdige rom: 99 av 106 (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 73, 74, 75, 76, 78, 80, 81, 82, 83, 84, 85, 87, 89, 91, 92, 94, 95, 96, 97, 98, 99, 100, 101, 102, 105, 106, 107, 108, 109, 110)
- Ferdige objekter: 24 av 30 (obj097_01, obj117_01, obj137_01, obj141_01, obj160_01, obj191_01, obj241_01, obj317_01, obj343_01, obj347_01, obj355_01, obj404_01, obj405_01, obj406_01, obj554_01, obj563_01, obj580_01, obj698_01, obj701_01, obj841_01, obj844_01, obj886_02, obj915_01, obj983_01)

## Gjør disse nå

1. `rom050` (rom 50, cuengrav, del 1/1). Avvist: deler av bildet er flyttet eller zoomet (opptil 28.2 px). Les retur.md.
2. `rom079` (rom 79, newton, del 1/1). Avvist: deler av bildet er flyttet eller zoomet (opptil 7.0 px). Les retur.md.
3. `obj547_01` (rom 79, newton, objekt 547 tilstand 01, del 1/1). Avvist: deler av bildet er flyttet eller zoomet (opptil 6.7 px). Les retur.md.
4. `rom088_del2av9` (rom 88, tombot, del 2/9).
5. `rom088_del3av9` (rom 88, tombot, del 3/9).
6. `rom088_del4av9` (rom 88, tombot, del 4/9).
7. `rom088_del5av9` (rom 88, tombot, del 5/9).
8. `rom088_del6av9` (rom 88, tombot, del 6/9).
9. `rom088_del7av9` (rom 88, tombot, del 7/9).
10. `rom088_del8av9` (rom 88, tombot, del 8/9).

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

## Beskjeder

- Veldig bra: 103 av 106 rom og 29 av 30 store objekter er ferdige, og jeg har sett gjennom alle. Symbolpanelene og kartet er trofaste.
- Igjen nå: rom050 (deler forskjøvet opptil 28 px, start helt på nytt fra referanse.png), rom079 og obj547_01 (opptil 7 px), og resten av rom088. Les retur.md i jobbene.
- Etter det: jobbene med status sjekk (rom072, rom077, rom090, rom101, rom111, obj557, obj884, obj886) kan bli bedre. Neste bestilling (mindre objekter) kommer i GRAFIKKLISTE.md når rommene er ferdige.

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
