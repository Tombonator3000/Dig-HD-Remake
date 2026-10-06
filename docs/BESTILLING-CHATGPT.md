# Bestilling til ChatGPT: trofast HD-grafikk for The Dig

Til: ChatGPT (bildegenerering, helst som Codex i dette repoet)
Fra: Tom, med Claude som står for koden
Dato: 6. oktober 2026

## 1. Hva vi bestiller

Vi lager en HD-versjon av LucasArts' The Dig (1995). Spillet kjører i ScummVM med en patch som legger HD-bilder nøyaktig oppå originalgrafikken, piksel for piksel. Vi trenger at du maler bakgrunnene på nytt i 4x oppløsning (1280 x 800 for et vanlig rom), **trofast mot originalen**: samme motiv, samme former på samme sted, samme farger og samme stemning. Bare skarpere og med mer detalj.

Første runde er de 106 rombakgrunnene, delt i 162 jobber. Hver jobb er ett bilde på 1536 x 1024 piksler.

## 2. Hvem gjør hva

| Hvem | Ansvar |
| --- | --- |
| **ChatGPT** | Lager HD-bildene etter jobbene. Gir råd om stil og sier fra når en jobb er uklar eller umulig. Skriver et kort notat per jobb. |
| **Claude** | All kode: lager jobbene, tar imot bildene, sjekker plassering og farger, syr sammen deler, lager mod-mappen, tester i motoren og skriver rapport. |
| **Tom** | Godkjenner stilen, flytter filer mellom dere hvis ChatGPT ikke jobber i repoet, og har siste ord. |

ChatGPT skal ikke endre kode, jobbfiler eller noe i grenen `main`.

## 3. Hva trofast betyr her

Motoren bruker HD-bildet bare der den vet at originalen viser uendret bakgrunn. Den sammenligner piksel for piksel. Figurer går foran og bak ting etter masker i originalens oppløsning, og klikkområder og gangflater ligger der de lå. Derfor:

1. **Ingenting flyttes.** Kanter, horisont, dører, maskiner, stjerner og lys skal ligge på nøyaktig samme sted. Ikke zoom, beskjær, roter, speil eller komponer om.
2. **Ingenting legges til eller fjernes.** Ingen nye gjenstander, figurer, tekst, symboler, planeter eller detaljer som endrer hva man ser.
3. **Symboler og inngraveringer kopieres nøyaktig.** Mange av dem er gåteledetråder.
4. **Samme farger, lys og stemning.** Samme lysretning, skygger og kontrast. Ikke varmere, kaldere, mørkere eller lysere.
5. **Samme stil.** Malt og forhåndsrendret 1990-tallsstil fra LucasArts. Ikke fotorealisme, ikke moderne 3D, ikke filmkorn, ikke vignett.
6. **Det som blir bedre:** jevne overganger i stedet for dithering og fargebånd, skarpe kanter, troverdig tekstur i stein, metall, himmel, vann og lys.

Vann og energi som animeres med fargesykling, viser motoren alltid som originalpiksler. Mal dem gjerne fint, men bruk ikke tid på dem.

## 4. Jobbene

Hver jobb ligger i `jobber/<jobb>/`:

| Fil | Innhold |
| --- | --- |
| `referanse.png` | Originalen forstørret 4x med harde pikselkanter, på en grå kant (#808080). 1536 x 1024. Dette er bildet du redigerer. |
| `original_1x.png` | Det samme utsnittet i originalstørrelse, til sammenligning. |
| `prompt.txt` | Teksten til bildeverktøyet, på engelsk. Brukes ordrett. Den inneholder et notat for rom med spesielle hensyn. |
| `jobb.json` | Metadata (rom, utsnitt, sjekksummer). Skal ikke endres. |
| `resultat.png` | **Det du leverer.** PNG, enten hele lerretet (1536 x 1024 med grå kant) eller bare bildet i samme sideforhold som utsnittet (16:10 for vanlige rom, minst 1280 x 800). |
| `notat.md` | **Det du skriver:** verktøy og modell hvis det vises, dato, antall forsøk, og hva som var usikkert. |
| `retur.md` | Kommer fra Claude hvis jobben ble avvist eller må sjekkes, med grunn og forslag til ny prompt. |

Den grå kanten er bare fyll, slik at bildet får sideforholdet 3:2. Hold den grå. Rom som er bredere eller høyere enn ett lerret, er delt i deler med overlapp (for eksempel `rom002_del1av3`). Delene sys sammen av Claude, så kantene skal være naturlige, uten ramme eller toning.

Oversikt over alle jobber: `JOBBER.md`. Status: `status.csv` (ny, godkjent, sjekk, avvist).

## 5. Rekkefølge

1. **Pilot (ferdig):** Codex leverte rom 9 og 22 den 6. oktober. Begge besto kontrollen og er godkjent av Claude på Tom sine vegne (Tom ba om at arbeidet skal fortsette). Tom kan overstyre.
2. **Stilankere:** Pilotbildene ligger i `stil/` (`room009_core.png`, `room022_beach.png`). Legg ved det ankeret som passer best som bilde nummer to i hver jobb (prompten forklarer hvordan det brukes). Det holder stilen lik fra rom til rom.
3. **Løpende ordre:** Claude skriver `ORDRE.md` i grenen etter hver kontroll, med de neste 10 jobbene. Ta dem i den rekkefølgen.
4. **Retur:** Jobber med `retur.md` står først i ordren og gjøres på nytt med teksten der.

Senere runder (egne bestillinger):

- **Objekter** (642 bilder: dører, maskiner, lys). Lages i sammenheng med det godkjente HD-rommet.
- **Figurer:** 331 kostymer med 28 490 animasjonsruter er for mye å male enkeltvis. Plan: et modellark per hovedperson fra ChatGPT som stilfasit, og så automatisk oppskalering av rutene, med retusj der det trengs.
- **Filmer:** 12 638 rammer. Ikke ChatGPT. Videooppskalering.

## 6. Arbeidsflyt

### A. ChatGPT som Codex i repoet (anbefalt)

1. Åpne repoet `Tombonator3000/Dig-HD-Remake` og bytt til grenen `gpt-arbeid`. Den har sin egen `AGENTS.md` og en kopi av denne bestillingen.
2. Les `ORDRE.md` og ta jobbene der. Lag ikke egne grener eller PR-er for grafikken.
3. For hver jobb: bruk bildeverktøyet med `referanse.png` som bildet som skal redigeres (og et stilanker som bilde to, når de finnes), og `prompt.txt` ordrett som prompt. Be om 1536 x 1024. Lagre som `resultat.png` og skriv `notat.md`.
4. Se på resultatet ved siden av referansen før du leverer. Ligger noe feil, prøv igjen.
5. Commit i grenen `gpt-arbeid` med meldingen `GPT: rom022, rom024` (jobbene i commiten) og push. Aldri til `main`.

Claude henter grenen, kjører kontrollen og skriver `RAPPORT.md` og `retur.md` tilbake.

### B. Vanlig ChatGPT-chat (manuelt)

1. Lag et ChatGPT-prosjekt «The Dig HD» og lim inn teksten i punkt 10 som instruksjoner.
2. For hver jobb: last opp `referanse.png` (og stilankeret), lim inn `prompt.txt`.
3. Last ned bildet og lagre det som `work/gpt/innboks/<jobb>.png`, for eksempel `rom022.png`.
4. Kjør `dighd gpt-inn`. Bildene flyttes inn i riktig jobb og sjekkes.

## 7. Slik sjekkes leveransene

`dighd gpt-inn` gjør dette med hvert bilde:

| Sjekk | Hva den måler | Godkjent | Sjekk | Avvist |
| --- | --- | --- | --- | --- |
| Størrelse | Sideforhold 3:2 (lerret) eller samme som utsnittet (direkte) | ett av dem | | annet |
| Forskyvning | Hele bildet mot originalen, i originalpiksler | 0,75 eller mindre | 1,5 eller mindre | mer |
| Blokker | Forskyvning i deler av bildet (avslører zoom og flyttede ting) | 1,0 eller mindre | 2,0 eller mindre | mer |
| Kantlikhet | Om formene er de samme (0 til 1) | 0,55 eller mer | 0,40 eller mer | mindre |

Testet med kunstige svar: et bilde som er forskjøvet 3 piksler, avvises. 3 prosent zoom avvises, 1 prosent zoom havner på sjekk, feil sideforhold avvises. Et omtegnet bilde som ligger riktig, godkjennes.

Etter sjekken **låses fargene til originalen**: de grove fargeflatene hentes fra originalen og detaljene fra ditt bilde. Et lite fargestikk gjør derfor ikke noe, men feil plassering gjør det. Grensene justeres når vi har sett ekte resultater.

Ferdige rom havner i `work/gpt-ferdig/rooms/`, og `dighd build-mod --egne work/gpt-ferdig` lager mod-mappen motoren bruker.

## 8. Sporing

Hver leveranse skal kunne spores. Claude skriver `work/gpt-ferdig/provenance.json` med sjekksum for referanse, prompt og resultat, målingene og innstillingene for fargelåsen. Ditt `notat.md` utfyller med verktøy, modell, dato, antall forsøk og eventuelle endringer i prompten.

## 9. Erfaringer fra Jones og Moonstone

**Jones in the Fast Lane** fikk HD-grafikk fra ChatGPT sitt innebygde bildeverktøy (via Codex):

- Det som virket: én presis prompt per bilde med «bevar» og «ikke»-lister, referansebildet som bildet som redigeres, og atlas for flere animasjonsrammer i ett bilde.
- Det som gikk galt og måtte rettes: verktøyet skrev feil tekst på et skilt (UNIVERSITY i stedet for HI-TECH U), og hår ble kuttet under toppfeltet i valgskjermen fordi figurene var plassert litt annerledes. Begge ble rettet med en ny, smal korrigeringsprompt.
- Stilen ble skiftet to ganger (malt, så fotorealistisk, så utvidet fotorealistisk). Derfor starter vi her med pilot og stilankere før resten.
- Sporingen (prompt, referanse og sjekksum for hvert bilde) og automatisk kontroll av størrelser og plassering gjorde det mulig å holde orden. Det bruker vi her også.
- Bildeverktøyet tok maks fem referansebilder om gangen og ga ikke alltid nøyaktig størrelse. Derfor tåler `gpt-inn` andre størrelser med samme sideforhold.

**Moonstone** fikk motoren for HD-grafikk, men ikke ferdig grafikk:

- HD-bildene navngis likt som utpakkede filer, i 4x størrelse.
- Liste over all grafikk med mål og HD-navn (her `docs/rom-oversikt.csv` og `JOBBER.md`).
- Bryter mellom HD og original, og gult felt der HD mangler. Står på todo for motoren her.
- Plasseringen sjekkes automatisk mot skjermbildet. Her gjør `gpt-inn` det før bildet slipper inn, og `engine/test.sh` i motoren etterpå.
- Lærdom: HD-bildene må tones med paletten når spillet fader. Det gjør motoren her allerede.

## 10. Tekst til ChatGPT-prosjektet

Lim inn dette som instruksjoner i et ChatGPT-prosjekt (arbeidsflyt B), eller la Codex lese denne filen (arbeidsflyt A):

```text
Du er grafiker i et prosjekt som lager en trofast HD-versjon av The Dig (LucasArts, 1995).
Claude skriver all kode. Du lager bildene. Tom godkjenner.

For hver jobb får du referanse.png (originalen forstørret 4x med harde piksler på grå kant, 1536 x 1024)
og prompt.txt. Bruk prompt.txt ordrett og referanse.png som bildet som redigeres. Lever ett bilde på
1536 x 1024 med samme oppsett.

Regler: ingenting flyttes, zoomes eller beskjæres. Ingenting legges til eller fjernes. Symboler og
inngraveringer kopieres nøyaktig. Samme farger, lys og stemning. Samme malte 1990-tallsstil fra
LucasArts, ikke fotorealisme. Den grå kanten skal være grå. Bedre detalj, jevne overganger og
skarpe kanter er målet.

Hvis et stilanker er vedlagt som bilde to, følg detaljnivået og penselarbeidet i det, men ta alt
innhold fra referansen.

Se på resultatet ved siden av referansen før du leverer. Si fra hvis noe ikke lar seg gjøre trofast.
Skriv et kort notat: verktøy, dato, antall forsøk, hva som var usikkert.
```

## 11. Privat

Spillet eies av Disney/Lucasfilm. Jobbene, referansene og resultatene ligger bare i det private repoet (grenen `gpt-arbeid`) og i `work/`. De skal ikke deles eller legges i `main`.
