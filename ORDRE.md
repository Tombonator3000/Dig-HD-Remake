# Ordre fra Claude

Oppdatert 2026-10-06 23:43 (norsk tid)

Les denne filen før du starter. Den erstatter tidligere ordre.

## Status

- Jobber: 162. godkjent 2, ny 160
- Ferdige rom: 2 av 106 (9, 22)

## Gjør disse nå

1. `rom002_del1av3` (rom 2, cockpit, del 1/3).
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

Skriv `notat.md` i jobbmappen. Commit 5 til 10 jobber om gangen i grenen `gpt-arbeid` og push.

## Beskjeder

- Pilotene rom009 og rom022 er godkjent og ligger nå i stil/ som stilankere. Bruk grenen gpt-arbeid for alle leveranser, ikke egne grener.

## Neste sjekk

Claude henter grenen omtrent hver halvtime, kontrollerer leveransene, oppdaterer `status.csv`, `RAPPORT.md` og `retur.md`, og skriver ny ordre her.
