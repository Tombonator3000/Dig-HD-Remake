# Bestilling til ChatGPT: trofast HD-grafikk for The Dig

Til: ChatGPT (bildegenerering, helst som Codex i dette repoet)
Fra: Tom, med Claude som står for koden
Dato: 6. oktober 2026

## 1. Hva vi bestiller

Vi lager en HD-versjon av LucasArts' The Dig (1995). Spillet kjører i ScummVM med en patch som legger HD-bilder nøyaktig oppå originalgrafikken, piksel for piksel. Vi trenger at du maler bakgrunnene på nytt i 4x oppløsning (1280 x 800 for et vanlig rom), **trofast mot originalen**: samme motiv, samme former på samme sted, samme farger og samme stemning. Bare skarpere og med mer detalj.

Første runde er de 106 rombakgrunnene, delt i 162 jobber, og 30 objektjobber for store bilder som spillet tegner over rommet (se punkt 4). Andre runde er de små objektbildene: 236 lagjobber med 460 objektbilder tegnet på plass i rommet, og 3 ikonark med de 149 ikonene i inventaret. Hver jobb er ett bilde på 1536 x 1024 piksler.

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

Oversikt over alle jobber: `JOBBER.md`. Status: `status.csv` (ny, godkjent, sjekk, avvist). Kolonnen `type` sier om jobben er et rom (`rom`), et stort objektbilde (`objekt`), et lag (`lag`) eller et ikonark (`ikon`).

### Objektjobber

I mange rom tegner spillet et stort bilde over bakgrunnen: nærbilder, kart og paneler. I rom 28 (shardcu) dekker objekt 241 hele skjermen, så HD-bakgrunnen synes nesten ikke. De 30 største objektbildene er derfor egne jobber. Grensen er minst 16 000 piksler i alt, eller minst 200 piksler bredt, eller minst 150 piksler høyt. To ensfargede rutenett i inventaret (obj618 og obj627) er tatt ut.

- Jobbene heter `objNNN_SS`: objekt-ID og tilstand som i filnavnet, for eksempel `obj241_01`.
- `referanse.png` viser objektbildet lagt over rommet der spillet tegner det, på samme lerret og med samme grå kant som rommene. Der objektet er gjennomsiktig, synes rommet bak. Utenfor rommet er det svart.
- Mal hele bildet som en bakgrunn. Bare objektets egne piksler brukes i spillet, de gjennomsiktige delene klippes ut igjen etterpå.
- `prompt.txt` har en ekstra linje om at bildet er et stort bilde spillet viser over rommet, og romnotatet for rommet.
- Leveres som rommene. Leverer du bare bildet, skal det ha objektets sideforhold (`bilde_i_lerret` i `jobb.json`).

### Lagjobber (små objekter)

De andre objektbildene er små: dører, brytere, lys og ting. De males på plass i rommet, så de får samme stil og lys som HD-rommet, og klippes ut etterpå.

- Jobbene heter `lagNNN_KK`: rom NNN, lag KK. Brede og høye rom har samme deler som romjobbene, for eksempel `lag023_01_del3av6` hører til `rom023_del3av6`. Deler uten objekter er ikke med.
- `referanse.png` er rommet med lagets objekter tegnet der spillet tegner dem. Lag 01 har første tilstand av hvert objekt, lag 02 neste og så videre. Objekter som ville ligget oppå hverandre, står i hvert sitt lag.
- Ligger objektene på et stort objektbilde (for eksempel skjermen på håndcomputeren i rom 79), er det store bildet med i referansen.
- Bilde to er det godkjente HD-bildet for samme del: `jobber/romNNN/resultat.png` eller `jobber/romNNN_delXavY/resultat.png`, eller objektjobben for det store bildet objektene ligger på. Det står i `bilde_to` i `jobb.json` og i ordren. Bruk det i stedet for stilankeret.
- Mal hele bildet trofast, også rommet rundt. Objektene klippes ut etter posisjon, så de må ligge nøyaktig der de er, med samme størrelse, omriss og farger. Ingen objekter skal mangle eller flyte inn i rommet.
- `jobb.json` lister objektene som klippes ut av akkurat denne jobben (`objekter`, med rektangel i originalpiksler).
- Leveres som rommene.

### Ikonark (inventaret)

Ikonene i inventaret (rom 93) og seks små sekskanter i rom 107 tegnes ikke på plass i et rom. De ligger i et rutenett på ikonark, på den mørkeblå fargen inventaret har bak ikonene.

- Jobbene heter `ikonNN`. Tilstandene til et ikon (vanlig, uthevet) står ved siden av hverandre.
- Mal hvert ikon trofast i ruten sin. Hold bakgrunnen flat mørkeblå, uten rammer eller rutenett.
- Leveres som rommene, med stilankeret som bilde to.

## 5. Rekkefølge

1. **Pilot (ferdig):** Codex leverte rom 9 og 22 den 6. oktober. Begge besto kontrollen og er godkjent av Claude på Tom sine vegne (Tom ba om at arbeidet skal fortsette). Tom kan overstyre.
2. **Stilankere:** Pilotbildene ligger i `stil/` (`room009_core.png`, `room022_beach.png`). Legg ved det ankeret som passer best som bilde nummer to i hver jobb (prompten forklarer hvordan det brukes). Det holder stilen lik fra rom til rom.
3. **Løpende ordre:** Claude skriver `ORDRE.md` i grenen etter hver kontroll, med de neste 10 jobbene. Ta dem i den rekkefølgen. Nye jobber står etter romnummer, med romjobbene før objektjobbene i samme rom. Objektjobber i rom som allerede er ferdige, kommer først. Lagjobbene kommer etter alle rom- og objektjobbene, etter romnummer, og først de der bilde to er godkjent. Ikonarkene kommer til slutt.
4. **Retur:** Jobber med `retur.md` står først i ordren og gjøres på nytt med teksten der.

Objektbildene (642): de 30 største er objektjobber, 460 små er i lagjobbene og 149 ikoner er på ikonarkene. Tre står igjen og skaleres automatisk: de to ensfargede rutenettene i inventaret og obj460_01 i rom 67, som er helt gjennomsiktig.

Senere runder (egne bestillinger):

- **Figurer:** 331 kostymer med 28 490 animasjonsruter er for mye å male enkeltvis. Plan: et modellark per hovedperson fra ChatGPT som stilfasit, og så automatisk oppskalering av rutene, med retusj der det trengs.
- **Filmer:** 12 638 rammer. Ikke ChatGPT. Videooppskalering.

## 6. Arbeidsflyt

### A. ChatGPT som Codex i repoet (anbefalt)

1. Åpne repoet `Tombonator3000/Dig-HD-Remake` og bytt til grenen `gpt-arbeid`. Den har sin egen `AGENTS.md` og en kopi av denne bestillingen.
2. Les `ORDRE.md` og ta jobbene der. Lag ikke egne grener eller PR-er for grafikken.
3. For hver jobb: bruk bildeverktøyet med `referanse.png` som bildet som skal redigeres (og et stilanker som bilde to, når de finnes; for lagjobber det godkjente HD-bildet i `bilde_to`), og `prompt.txt` ordrett som prompt. Be om 1536 x 1024. Lagre som `resultat.png` og skriv `notat.md`.
4. Se på resultatet ved siden av referansen før du leverer. Ligger noe feil, prøv igjen.
5. Commit i grenen `gpt-arbeid` med meldingen `GPT: rom022, obj241_01` (jobbene i commiten) og push. Aldri til `main`.

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

Objektjobber kontrolleres på samme måte mot sitt eget `original_1x.png` (objektbildet over rommet i 1x).

Lagjobber og ikonark kontrolleres som helhet på samme måte, og i tillegg hvert objekt for seg, bare på objektets synlige piksler:

| Sjekk per objekt | Avvist når |
| --- | --- |
| Mangler | Resultatet ligner mer på rommet uten objektet enn på objektet (kantlikhet mot bakgrunnen er over kantlikheten mot objektet pluss 0,05). Måles når objektet skiller seg fra bakgrunnen (kantlikhet under 0,90 mellom dem). |
| Tegnet om | Kantlikheten i objektet er under 0,50, for objekter med tydelige kanter. |

Ett feil objekt avviser hele jobben. Prøvd på ekte data: i 212 lagjobber med kunstige resultater der objektene manglet, godkjente den vanlige kontrollen 206, mens sjekken per objekt fant 348 av 409 målte objekter (de andre ligner bakgrunnen). Referansen og HD-rommet med objektene limt inn ga ingen avvisninger. ChatGPT sine godkjente rombilder har kantlikhet 0,75 eller mer i de samme feltene der grensen for tegnet om gjelder.

Etter fargelåsen klippes hvert objekt ut av delen det står i (sydd sammen hvis det står i flere) på rektangelet sitt, i 4x med gjennomsiktigheten fra originalen. Et objekt er ferdig når alle delene det står i, er godtatt (godkjent, eller sjekk som for rommene; med `--bare-godkjente` bare godkjent). Senere tilstander av et objekt gjøres like den første der originalene er like, som for objektjobbene.

Ferdige rom havner i `work/gpt-ferdig/rooms/` og ferdige objektbilder i `work/gpt-ferdig/objects/` (nøyaktig 4x objektstørrelse, med gjennomsiktigheten fra originalen). `dighd build-mod --egne work/gpt-ferdig` lager mod-mappen motoren bruker, og bruker de godkjente objektbildene i stedet for automatisk oppskalering. Godkjente objektbilder kommer med i modden også i rom som ikke har HD-bakgrunn ennå. Et rom regnes som ferdig når romjobbene er godkjent, uavhengig av objektene.

## 8. Sporing

Hver leveranse skal kunne spores. Claude skriver `work/gpt-ferdig/provenance.json` med sjekksum for referanse, prompt og resultat, målingene og innstillingene for fargelåsen. Objektbilder fra lag og ikonark får hver sin oppføring med laget eller arket de kom fra og rektangelet i det. Ditt `notat.md` utfyller med verktøy, modell, dato, antall forsøk og eventuelle endringer i prompten.

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
1536 x 1024 med samme oppsett. Jobber som heter objNNN_SS, er store bilder spillet viser over rommet
(nærbilder, kart, paneler). Behandle dem som bakgrunner. Jobber som heter lagNNN_KK, er rommet med små
objekter tegnet på plass. Mal alt trofast; objektene klippes ut etter posisjon, så de må ligge nøyaktig
der de er. Bruk det godkjente HD-bildet i bilde_to som bilde to. Jobber som heter ikonNN, er ikonene i
inventaret på mørkeblå bakgrunn.

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
