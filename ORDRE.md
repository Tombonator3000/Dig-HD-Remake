# Ordre fra Claude

Oppdatert 2026-10-07 06:54 (norsk tid)

Les denne filen før du starter. Den erstatter tidligere ordre.

## Status

- Jobber: 192. godkjent 4, ny 188
- Ferdige rom: 3 av 106 (9, 22, 28)
- Ferdige objekter: 0 av 30

## Gjør disse nå

1. `obj241_01` (rom 28, shardcu, objekt 241 tilstand 01, del 1/1).
2. `rom002_del2av3` (rom 2, cockpit, del 2/3).
3. `rom002_del3av3` (rom 2, cockpit, del 3/3).
4. `rom003` (rom 3, klein, del 1/1).
5. `rom004` (rom 4, ast1, del 1/1).
6. `rom005` (rom 5, ast2, del 1/1).
7. `rom006` (rom 6, ast3, del 1/1).
8. `rom007` (rom 7, ast4, del 1/1).
9. `rom008` (rom 8, ast5, del 1/1).
10. `rom010_del1av2` (rom 10, tun1, del 1/2).

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

- Nytt: 30 objektjobber (objNNN_SS). Det er store bilder spillet tegner over rommet, som nærbilder, kart og den blå trikken. De lages akkurat som romjobbene. obj241_01 (tavla i rom 28) står først fordi rom 28 er ferdig.
- Objekter med flere tilstander (obj884 og obj886): lag tilstand 01 først. For de andre tilstandene legger du ved resultat.png fra tilstand 01 som bilde to i stedet for stilankeret. Claude gjør resten likt automatisk.
- Kjør git pull før hver økt og les ORDRE.md. Ikke legg til stjerner, lyspunkter eller vann som ikke finnes i originalen.
- Motoren har fått HD-tekst, fargesykling i HD og undertekster over HD-filmrammer. Bygg motoren på nytt før laptoptesten (kodeoppgave 1).

## Kodeoppgaver

Disse er for Codex eller ChatGPT med tilgang til laptopen og repoet. Ta én om gangen, og skriv i `rapporter/` i denne grenen hva du gjorde og fant.

1. **Test HD-modden på laptopen med skjerm og tastatur.** Hent og bygg: `git checkout main && git pull`, `tools/hent_spilldata.sh`, `tools/mod_gren.sh hent`, `engine/build.sh` (patchen er ny, så bygg på nytt), `engine/run.sh gpt`. Gå til rom 9, 22 og 28 (start med `DIGHD_TEST_ROOM=22 DIGHD_TEST_AT=240 engine/run.sh gpt` hvis det er lettere). Sjekk:
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
