# AGENTS.md (grenen gpt-arbeid)

Denne grenen er arbeidsbordet for HD-grafikken til The Dig HD Remake. Du er grafikeren. Claude skriver koden, Tom godkjenner.

Les `ORDRE.md` først. Den er siste beskjed fra Claude, med jobbene du skal gjøre nå. Les deretter `BESTILLING.md`, som gjelder foran alt annet her.

## Faste regler

- Jobb bare i denne grenen (`gpt-arbeid`). Aldri push til `main`, og lag ikke egne grener eller PR-er for grafikken.
- Endre aldri `referanse.png`, `original_1x.png`, `prompt.txt` eller `jobb.json`.
- Lever `jobber/<jobb>/resultat.png` og `jobber/<jobb>/notat.md`. Resultatet kan være hele lerretet (1536 x 1024 med grå kant) eller bare bildet i samme sideforhold som utsnittet (16:10 for vanlige rom).
- Bruk `prompt.txt` ordrett. Legg ved stilankeret fra `stil/` som bilde to når det finnes.
- Skriv på norsk i notater, uten emoji og uten tankestreker.
- Repoet er privat. Ingenting herfra skal deles.

## Slik jobber du

1. Ta jobbene i `ORDRE.md`, i den rekkefølgen de står.
2. Lag bildet med bildeverktøyet: `referanse.png` er bildet som redigeres, `prompt.txt` er prompten, størrelse 1536 x 1024.
3. Sammenlign med `referanse.png` før du lagrer. Ligger noe feil, prøv igjen.
4. Lagre `resultat.png`. Skriv `notat.md` med verktøy og modell (hvis det vises), dato, antall forsøk og hva som var usikkert.
5. Har jobben en `retur.md`, bruk forslaget der og lever på nytt.
6. Commit 5 til 10 jobber om gangen med meldingen `GPT: rom022, rom024` og push.

Claude kjører kontrollen (`dighd gpt-inn`) og skriver `RAPPORT.md`, `status.csv` og `retur.md` tilbake hit.
