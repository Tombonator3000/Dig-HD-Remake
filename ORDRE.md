# Ordre fra Claude

Oppdatert 2026-10-07 16:35 (norsk tid)

Les denne filen før du starter. Den erstatter tidligere ordre.

## Status

- Jobber: 431. avvist 6, godkjent 175, ny 239, sjekk 11
- Ferdige rom: 100 av 106 (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 78, 80, 81, 82, 83, 84, 85, 87, 89, 90, 91, 92, 94, 95, 96, 97, 98, 99, 100, 101, 102, 105, 106, 107, 108, 109, 110)
- Ferdige objekter: 22 av 30 (obj097_01, obj117_01, obj137_01, obj141_01, obj160_01, obj191_01, obj241_01, obj317_01, obj404_01, obj405_01, obj406_01, obj554_01, obj563_01, obj580_01, obj698_01, obj701_01, obj841_01, obj844_01, obj884_02, obj884_03, obj915_01, obj983_01)
- Lagjobber: 0 av 236 godkjent. Ferdige objektbilder fra lag: 0 av 460
- Ikonark: 0 av 3 godkjent. Ferdige ikoner fra ikonark: 0 av 149

## Gjør disse nå

1. `rom032` (rom 32, pool, del 1/1). Avvist: under buen til venstre har originalen lyse loddrette striper (vann som renner ned i dammen); de er blitt en utskåret steinbue med pynt. Les retur.md.
2. `rom050` (rom 50, cuengrav, del 1/1). Avvist: deler av bildet er flyttet eller zoomet (opptil 6.9 px). Les retur.md.
3. `rom088_del6av9` (rom 88, tombot, del 6/9). Avvist: deler av bildet er flyttet eller zoomet (opptil 17.9 px); formene ligner for lite på originalen (kantlikhet 0.54). Les retur.md.
4. `rom088_del7av9` (rom 88, tombot, del 7/9). Avvist: det svarte feltet øverst er malt over med fjell, og resten av bildet er skjøvet nedover. Les retur.md.
5. `rom088_del8av9` (rom 88, tombot, del 8/9). Avvist: deler av bildet er flyttet eller zoomet (opptil 6.1 px). Les retur.md.
6. `rom088_del9av9` (rom 88, tombot, del 9/9). Avvist: deler av bildet er flyttet eller zoomet (opptil 22.9 px). Les retur.md.
7. `lag002_01_del1av3` (rom 2, cockpit, lag 01 med 2 objektbilder, del 1/3). Legg ved `jobber/rom002_del1av3/resultat.png` som bilde to (ikke stilankeret), så objektene får samme stil og lys som HD-bildet.
8. `lag002_02_del1av3` (rom 2, cockpit, lag 02 med 1 objektbilde, del 1/3). Legg ved `jobber/rom002_del1av3/resultat.png` som bilde to (ikke stilankeret), så objektene får samme stil og lys som HD-bildet.
9. `lag003_01` (rom 3, klein, lag 01 med 1 objektbilde, del 1/1). Legg ved `jobber/rom003/resultat.png` som bilde to (ikke stilankeret), så objektene får samme stil og lys som HD-bildet.
10. `lag004_01` (rom 4, ast1, lag 01 med 1 objektbilde, del 1/1). Legg ved `jobber/rom004/resultat.png` som bilde to (ikke stilankeret), så objektene får samme stil og lys som HD-bildet.

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

Lagjobbene (`lagNNN_KK`) er rommet med spillets små objekter tegnet på plass. Mal alt trofast. Objektene klippes ut etter posisjonen, så de må ligge nøyaktig der de er. Bilde to er det godkjente HD-bildet som står i ordren (`bilde_to` i `jobb.json`). Ikonarkene (`ikonNN`) er ikonene i inventaret på mørkeblå bakgrunn. Begge leveres som rommene.

Skriv `notat.md` i jobbmappen. Commit 5 til 10 jobber om gangen i grenen `gpt-arbeid` og push.

## Beskjeder

- Sømmene ved obj343, obj347, obj355, obj547 og obj886 står som sjekk: bildene brukes til de er gjort om, men lag dem på nytt etter retur.md. rom032 er avvist (vannet under buen er blitt stein).

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
