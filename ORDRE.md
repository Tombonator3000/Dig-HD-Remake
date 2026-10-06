# Ordre fra Claude

Oppdatert 2026-10-06 23:56 (norsk tid)

Les denne filen før du starter. Den erstatter tidligere ordre.

## Status

- Jobber: 162. godkjent 4, ny 158
- Ferdige rom: 3 av 106 (9, 22, 28)

## Gjør disse nå

1. `rom002_del2av3` (rom 2, cockpit, del 2/3).
2. `rom002_del3av3` (rom 2, cockpit, del 3/3).
3. `rom003` (rom 3, klein, del 1/1).
4. `rom004` (rom 4, ast1, del 1/1).
5. `rom005` (rom 5, ast2, del 1/1).
6. `rom006` (rom 6, ast3, del 1/1).
7. `rom007` (rom 7, ast4, del 1/1).
8. `rom008` (rom 8, ast5, del 1/1).
9. `rom010_del1av2` (rom 10, tun1, del 1/2).
10. `rom010_del2av2` (rom 10, tun1, del 2/2).

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

- Rom 2 del 1, rom 22 og rom 28 er godkjent. Takk. Rom 22 beholdes som piloten fra Codex (se notat.md i jobben), så ikke lag den på nytt.
- Leveransen ble laget fra en eldre utgave av grenen (560d654) uten stilankere. Kjør git pull før hver økt, les ORDRE.md og legg ved stilankeret fra stil/ som bilde to.
- Ikke legg til nye stjerner, lyspunkter eller vann der originalen ikke har det. Tonevariasjon i den grå kanten er greit, den skjæres bort. Du kan også levere bare bildet i 16:10.

## Neste sjekk

Claude henter grenen omtrent hver halvtime, kontrollerer leveransene, oppdaterer `status.csv`, `RAPPORT.md` og `retur.md`, og skriver ny ordre her.
