# spilldata

Denne grenen inneholder spillfilene til The Dig (engelsk standardutgave, data fra november 1995): `DIG.LA0`, `DIG.LA1`, `VIDEO/`, og musikk og tale.

Musikk og tale (`DIGMUSIC.BUN` 261 MB, `DIGVOICE.BUN` 130 MB) er over GitHubs grense på 100 MB per fil og ligger derfor i deler på 90 MB: `DIGMUSIC.BUN.001` til `.003` og `DIGVOICE.BUN.001` og `.002`. `tools/hent_spilldata.sh` setter dem sammen igjen, og nettsiden gjør det samme i nettleseren.

Grenen er privat bruk. Repoet må holdes privat så lenge denne grenen finnes. Hent dataene inn i `game/` i main med `tools/hent_spilldata.sh`.

Sjekksummer: `game/SHA256SUMS` (filene som de ligger her) og `game/SHA256SUMS.lyd` (musikk og tale satt sammen).
