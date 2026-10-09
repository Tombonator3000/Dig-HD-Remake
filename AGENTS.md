# AGENTS.md (grenen gpt-arbeid)

Denne grenen er arbeidsbordet for HD-grafikken til The Dig HD Remake. Du er grafikeren. Claude skriver koden, Tom godkjenner.

Les `ORDRE.md` først. Den er siste beskjed fra Claude, med jobbene du skal gjøre nå. Les deretter `BESTILLING.md`, som gjelder foran alt annet her.

## Faste regler

- Jobb bare i denne grenen (`gpt-arbeid`). Aldri push til `main`, og lag ikke egne grener eller PR-er for grafikken.
- Endre aldri `referanse.png`, `original_1x.png`, `prompt.txt` eller `jobb.json`.
- Lever `jobber/<jobb>/resultat.png` og `jobber/<jobb>/notat.md`. Resultatet kan være hele lerretet (1536 x 1024 med grå kant) eller bare bildet i samme sideforhold som utsnittet (16:10 for vanlige rom).
- Bruk `prompt.txt` ordrett. Legg ved stilankeret fra `stil/` som bilde to når det finnes, eller det bildet ordren sier.
- Jobbene heter `romNNN` (rombakgrunner), `objNNN_SS` (objektjobber: store bilder som spillet tegner over rommet, som nærbilder, kart og paneler), `lagNNN_KK` (lagjobber), `ikonNN` (ikonark) eller `figCCC_KK` (figurark). Alle lages og leveres på samme måte. I en objektjobb viser `referanse.png` objektet lagt over rommet. Mal hele bildet som en bakgrunn. Leverer du bare bildet, skal det ha objektets sideforhold (`bilde_i_lerret` i `jobb.json`).
- Objekter med flere tilstander (for eksempel `obj884_01`, `_02`, `_03`): lag tilstand 01 først. For de andre legger du ved `jobber/<objekt>_01/resultat.png` som bilde to i stedet for stilankeret. Claude gjør det som er likt, helt likt etterpå.
- Lagjobber (`lagNNN_KK`, for eksempel `lag023_01_del3av6`): rommet med små objekter (dører, brytere, lys, ting) tegnet på plass. Mal alt trofast. Objektene klippes ut etter posisjonen, så hvert objekt må ligge nøyaktig der det er, med samme størrelse, omriss og farger, og ingen må mangle. Legg ved det godkjente HD-bildet som står i ordren (`bilde_to` i `jobb.json`, for eksempel `jobber/rom023_del3av6/resultat.png`) som bilde to i stedet for stilankeret. Står det i ordren at jobben skal lages etter en annen, vent til den er godkjent.
- Ikonark (`ikonNN`): ikonene i inventaret i et rutenett på mørkeblå bakgrunn. Mal hvert ikon trofast i ruten sin, og hold bakgrunnen flat mørkeblå. Stilankeret som bilde to.
- Figurark (`figCCC_KK`, kostyme CCC, ark KK): animasjonsruter av samme figur, i den rekkefølgen spillet viser dem. Referansen står på en flat bakgrunnsfarge. Mal alle rutene som den samme personen (samme ansikt, hår, klær, farger og lys) i den glatte stilen, med samme pose og plass som originalen, på gjennomsiktig bakgrunn med ekte alfa. Kropper uten hode og hoder alene males som de er. Ark 01 med stilankeret som bilde to, de andre arkene med det godkjente ark 01 (`bilde_to` i `jobb.json`). Arkene for Boston Low (`fig014_01` til `fig014_04`) er en pilot og står tidlig i ordren. Ark i den glatte stilen Tom har valgt (Boston, Brink og Maggie) leveres med gjennomsiktig bakgrunn og ekte alfa, føres i `leveranser` i `rapporter/*/fremdrift.json` med sha256, og bør ha et rutekart; Claude tar dem inn med `dighd myke-figurer` (se `docs/BESTILLING-CHATGPT.md` i `main`).
- Kodeoppgaver i `ORDRE.md` er for den som har laptopen med spillet. Rapporter skrives i `rapporter/` i denne grenen. Kodeendringer går som PR mot `main`.
- Skriv på norsk i notater, uten emoji og uten tankestreker.
- Repoet er privat. Ingenting herfra skal deles.

## Slik jobber du

1. Kjør `git pull` i grenen `gpt-arbeid` før hver økt. Ta jobbene i `ORDRE.md`, i den rekkefølgen de står. Når de er levert, fortsett med neste bestilling i `GRAFIKKLISTE.md` uten å vente på ny ordre. Hopp over jobber som er krysset av.
2. Lag bildet med bildeverktøyet: `referanse.png` er bildet som redigeres, `prompt.txt` er prompten, størrelse 1536 x 1024.
3. Sammenlign med `referanse.png` før du lagrer. Ligger noe feil, prøv igjen.
4. Lagre `resultat.png`. Skriv `notat.md` med verktøy og modell (hvis det vises), dato, antall forsøk og hva som var usikkert.
5. Har jobben en `retur.md`, bruk forslaget der og lever på nytt.
6. Commit 5 til 10 jobber om gangen med meldingen `GPT: rom022, obj241_01` og push.

Claude kjører kontrollen (`dighd gpt-inn`) og skriver `RAPPORT.md`, `status.csv` og `retur.md` tilbake hit.
