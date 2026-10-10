# Arbeidsmetode for trofast HD-remaster

Dato: 10. oktober 2026. Forfatter: Codex. Grunnlag: main ved commit 57c5588d5dfafa523837a56f94551d60d43039af.

Denne planen beskriver videre arbeid. Den er ikke en rapport om nye tester eller implementerte funksjoner. Den supplerer BESTILLING-CHATGPT.md og endrer ikke Toms godkjente glatte figurstil, Exo 2, originalens spillregler eller beslutningen om at filmene venter.

## 1. Målet

Samme spill og visuelle identitet i klar HD. Behold komposisjon, former, figuridentitet, lys, palett og gåteledetråder. Mer detalj er bare nyttig når den forklarer originalen. Ikke legg til materialer, effekter eller former bare fordi verktøyet kan.

The Dig beholder det malte science fiction-uttrykket. Sam & Max beholder tegneseriestreken. Zak trenger egne stilankere fra den valgte spillutgaven; coveret er støtte for figuridentitet, ikke erstatning for skjermbildets geometri. Nye spill starter først etter The Dig, som avtalt.

## 2. Hva de offisielle remasterne lærer oss

Dokumenterte forhold:
- Double Fine beskriver DOTT Remastered som ny håndtegnet høyoppløst grafikk. Spilleren kan kombinere klassisk og remastret grafikk, lyd og UI.
- Tim Schafer beskriver et nytt verb dial rundt interessepunktet og valgfri gammel verbbar. Han og Matt Hansen oppga over 100 bakgrunner og 10 000 animasjonsbilder som måtte males om.
- GDC-presentasjonen fra Double Fine og Shiny Shoe viser original SCUMM-logikk med et lag som leser og oversetter spilltilstand til ny grafikk, lyd og input. Den beskriver også kostymer, animasjoner og kroppsdeler.
- Craig Derrick forklarer at første Monkey Island Special Edition vurderte et trevalgs verb coin, men beholdt de ni handlingene i separat tilgjengelige verb- og inventarmenyer. Figurene var en nytolkning basert på flere spill og covere.
- Monkey Island 2 SE tilbyr håndtegnet HD, direkte kontroll som alternativ og bytte til originalgrafikken.

Grundigere gjennomgang av alle fem remasterne, kritikken av dem og tiltak for The Dig: `docs/REMASTER-FORBILDER.md`.

Konsekvens for oss: DOTT er det nærmeste forbildet for trofast nytegning. Bevar originalens handlinger når UI endres. Ikke påstå at alle prosjektene brukte samme hjul eller identisk arbeidsmetode.

Kildene dokumenterer prinsippene og omfanget. Lagstrukturen og kontrollpunktene nedenfor er vårt forslag, ikke en påstand om hvilket tegneprogram eller hvilken eksakt overtegningsprosedyre Double Fine brukte.

Kilder:
- https://www.doublefine.com/games/day-of-the-tentacle-remastered
- https://www.doublefine.com/games/day-of-the-tentacle-remastered/making
- https://www.p1xelcoder.com/resources/GDC_2017_Remastering_DotT_and_Grim.pdf
- https://www.shacknews.com/article/91891/double-fines-tim-schafer-on-day-of-the-tentacle-remastered-it-was-kind-of-now-or-never
- https://www.adventureclassicgaming.com/index.php/site/interviews/536/
- https://www.craigderrick.com/2010/03/10/monkey-island-2-special-addition-announced/
- https://store.steampowered.com/app/32460/Monkey_Island_2_Special_Edition_LeChucks_Revenge/
- Sam & Max originalmanual: https://www.mocagh.org/lucasfilm/sammax-manual.pdf

## 3. Gjennomgang av dagens repo

Dokumentasjonen og de relevante mottaksfunksjonene er lest. Spillet og grafikkdataene er ikke kjørt eller visuelt kontrollert i denne gjennomgangen.

| Funn | Grunnlag | Tiltak |
| --- | --- | --- |
| God infrastruktur for trofast utskifting | HD-MOTOR.md, gpt.py, romtest og opprinnelig ScummVM-logikk | Behold og utvid kontrollene; ikke bygg ny spillogikk for å modernisere grafikken |
| Teknisk sjekk brukes også i modden | gpt.py tar med sjekk når only_approved er av; myk.py skriver ruter med status sjekk | Skill arbeidsmod fra visuelt godkjent pakke. Før dette finnes, merk pakken som arbeidsversjon |
| Myke ruter mangler samme kontrollvei som vanlige figurark | gpt.py registrerer native alfa som levert; myk.py måler plassering og omriss | Lag egen kontroll av identitet, farger, fotfeste og flimmer for myke animasjoner |
| Automatisk rutekobling kan bli usikker | myk.py bruker rad/rekkefølge uten rutekart; hodene og kroppene skaleres separat | Krev eksplisitt rutekart for nye leveranser; kontroller gamle før de regnes som ferdige |
| Tekniske tester dekker ikke kunstnerisk innhold | rom 32 er avvist fordi vann ble stein, selv om geometrimålinger finnes | Kontroller materialer og gåteledetråder visuelt i tillegg til tallene |
| Motorens myke figurer har kjente lagbegrensninger | HD-MOTOR.md: figur bak smalere myk tegning kan erstattes av bakgrunn; z-masker i originaloppløsning | Test flere figurer, masker, skalering og menyer før nye effekter |
| Minne og filhenting trenger arbeid | todo.md: MEMFS-kopier; siste logg: gpt-inn rundt 4 GB etter minnekart | Mål mottak og nettleser separat; mindre grupper i produksjonen, ingen vilkårlig svekking av kontroll |
| Statusdokumentene er ikke helt samstemte | README sier ingen småjobber laget; STATUS sier 167; seneste logg sier 628 objektbilder og 5596 kostymeruter | Oppdater senere fra én verifisert pakke og dater tellingene; ikke bland antall levert, sjekk og godkjent |

Siste logg beskriver 307 figurark, 5091 ruter ok og 505 til gjennomsyn. Dette er historiske loggtall, ikke en ny opptelling av hd-mod. Ikke erklær 5596 ruter visuelt godkjent.

## 4. Produksjon per ressurs

### A. Referanse og låsing
1. Identifiser spillutgave, ressurs-ID, rom/kostyme/tilstand, palett og checksum.
2. Bruk uttrukket ressurs som hovedreferanse. Skjermbilder viser sammenhengen, men inneholder også andre lag.
3. Lag et låst 1x- og 4x-underlag med samme sideforhold. Skill spillkoordinater fra visningsformat. Ikke strekk til 16:9.
4. Marker viktige punkter: føtter, øyne, hodefeste, dørkanter, brytere, symboler, vannkant og objektkontakt.
5. Bruk godkjent stilanker som tillegg. Originalen bestemmer innhold og plassering.

### B. Nytegning
- Arbeidslag: låst original, konturer, grunnfarger, skygger/lys, materialdetaljer, alfa og eksport.
- Bevar den store formen først. Tegn detaljene etter at sammenligningen stemmer.
- Hold originale fargeflater og lysretning. Unngå ekstra glans, støy, skarphetsglorier og oppdiktede teksturer.
- Bildegenerering brukes til kandidater og avgrensede rettelser. En vellykket prompt er ikke dokumentasjon på nøyaktig plassering.
- Rett én konkret feil om gangen med original og godkjent kandidat som referanser. Ikke regenerer hele rommet når bare én kant er feil.
- Symboler og teksten på rekvisitter kontrolleres tegn for tegn. HD-undertekster skal fortsatt bruke valgt Exo 2.
- Behold både rå kandidat og ferdig behandlet eksport; fargelås eller skalering kan introdusere nye feil.

### C. Lag, objekter og tilstander
- Bakgrunn, bevegelige objekter og figurer leveres separat gjennom dagens jobbformat.
- Bruk det godkjente HD-rommet som sammenheng for lagjobber, slik bestillingen allerede krever.
- Kontroller åpnet/lukket, tent/slukket og før/etter i samme bildeområde. Uendrede områder må ikke hoppe i farge eller form.
- Kontroller sømmer før og etter sammensying og fargelås, spesielt obj343, obj347, obj355, obj547 og obj886.
- Vann, energi, transparens og palettbytte må sees i bevegelse. BESTILLING-CHATGPT.md har en eldre formulering om at vann alltid blir originalpiksler; HD-MOTOR.md beskriver nå HD-fargesykling. Bruk motorbeskrivelsen for dette.

### D. Figurer og animasjoner
- Én godkjent identitetsreferanse per figur: ansikt, alder, hår, kroppsform, klær, lys og palett. Boston skal beholde alder og grå tinninger.
- Ekte alfa og myke kanter beholdes. Ikke bruk originalens harde pikselmaske som ny kontur.
- Rutekartet skal koble hver original-ID til riktig tegnet del og boks. Antall, rekkefølge, hode/kropp og tomme ruter må stemme.
- Vurder fotpunkt og hodefeste i tillegg til maksimal silhuettoverlapp. En høy overlapp garanterer ikke riktig ansikt eller stabil gange.
- Spill hele animasjonen i originalens rekkefølge og tempo, med hode og kropp samlet. Stillbilder alene er utilstrekkelige.
- Kontroller minst én hel sløyfe og overgangen til neste handling: ansikt, størrelse, klær, skygge, alfa, glorie og fotglidning.
- Et bevisst omrissavvik kan godkjennes av Tom, men må knyttes til konkret rute og checksum. Ingen automatisk redesign for å nå terskelen.

## 5. Godkjenning

Foreslått arbeidsflyt, ikke nye implementerte statusverdier:

| Trinn | Betydning | Bevis |
| --- | --- | --- |
| Levert | Kandidaten og rutekartet finnes | Fil og checksum |
| Teknisk kontrollert | Format, plassering og ressurskobling stemmer | Dagens mottaksrapport |
| Visuelt kontrollert | Motiv, stil, figurer og gåteledetråder stemmer | Overlegg, kontaktark og konkret vurdering |
| Kontrollert i bevegelse | Tilstander, animasjon og lag fungerer sammen | Sekvens eller opptak og testscenario |
| Godkjent av Tom | Godkjent stil eller resultat innen avtalt omfang | Notat med dato, ressurs og checksum |

Dagens godkjent er en teknisk mottaksstatus. Behold betydningen i eksisterende filer til kode og rapporter er oppdatert. Legg heller ved en separat vurdering enn å endre statusformat på egen hånd.

Arbeidsmodden kan bruke sjekk for kontinuerlig spilltesting. En pakke omtalt som ferdig må utelate eller ha dokumentert godkjenning av slike avvik. Hvis en rute utelates, bekreft at fallback til originalen faktisk virker og at gamle eksportfiler ikke blir stående.

Kontrollpakken per ressurs:
- original og HD side om side;
- 50 prosent overlegg og kantvisning;
- rå kandidat og behandlet eksport;
- relevante objekttilstander eller animasjon;
- spillvisning med lag, tekst og menyer;
- vurdering, åpne feil og referanser til checksums.

Geometriske mål er et hjelpemiddel. De oppdager ikke sikkert vann som blir stein, feil alder, endrede symboler eller feil objektidentitet.

## 6. Testrekkefølge for The Dig

Bruk eksisterende tester før nye verktøy:
- Pipelineendring: cd pipeline && pytest -m "not game".
- Med tilgjengelige spillfiler: pytest -m game.
- Motorendring: engine/test.sh, med dagens nearest-referanse.
- Rom: tools/romtest.sh og tools/romtest.sh --objekter.
- Manuell sammenligning: Ctrl+H, gult felt og originale lagrede spill som gjenskaper ekte skripttilstand.

Tillegg som Claude bør implementere og teste i PR:
1. Lesbar animasjonsforhåndsvisning i korrekt rekkefølge, med original og myk HD side om side.
2. Visuell godkjenningsliste bundet til ressurs-ID og resultatets checksum, også for myke ruter.
3. Pakkerapport som skiller levert, teknisk ok, sjekk, visuelt kontrollert og fallback.
4. Kontroll som hindrer gamle avviste eksportfiler i å bli med ved ny bygging.
5. Målinger av minne og tid for mottak og nettleser, med reproducerbart scenario.

Ekte scenarioer som mangler eller må utvides:
- Flere myke figurer foran og bak hverandre.
- Skalerte myke figurer og figurer bak flere forgrunnsplan.
- Meny, banner og undertekst over myke figurer, også etter at de forsvinner.
- Fade, palettbytte og fargesykling.
- Objekter på hver side av en sammensydd del.
- Rom 10 og 104 via faktisk spillsekvens fremfor romhopp.
- Lagring og lasting etter objektbytte og HD-bytte.
- Ekte Kubuntu med lyd og mus, ekte telefon med lyd og minnemåling.
- Gjennomspilling. Romhopp beviser ikke at gåter og skript fungerer i vanlig spill.

Ingen nye slike tester er kjørt for denne dokumentleveransen.

## 7. UI uten å endre gåtene

The Dig har ikke DOTT sin verbbar. Ikke legg til et hjul bare for å kopiere DOTT. Behold eksisterende samhandling i første ferdige versjon; undersøk konkrete klikk- og berøringsproblemer først.

For senere Zak og Sam & Max:
- Registrer alle originalhandlinger og hvordan de brukes på objekt og inventar.
- Et hjul sender samme verb-ID og objekt-ID som originalsystemet. Det må også håndtere kombinasjoner og mottakerobjekt.
- Ikke fjern mislykkede valg bare fordi de virker lite nyttige; de kan ha morsomme eller viktige svar. Et konteksthjul må ikke avsløre gåteløsningen.
- Sam & Max har allerede markørmoduser og eget inventar. Et lite hjul bør presentere disse, ikke innføre en ny verbbar.
- PC: pek/klikk og valgfritt høyreklikk for hjul. Mobil: trykk og tydelig valg med nok avstand. Tilby et alternativ til hold for brukere som ikke oppdager gesten.
- Test meny ved skjermkant, avbryt, inventar mot inventar, inventar mot rom, dialog og tastatur.
- UI og HD-bryter bør være uavhengige når dette implementeres.
- Ikke innfør nye knapper rundt The Dig-nettsiden i strid med Toms valg om direkte oppstart.

## 8. Prioritert plan

| Prioritet | Arbeid | Ferdig når |
| --- | --- | --- |
| P0 | Gå gjennom myke ruter med sjekk, feil figuridentitet og rutekobling | Avvik har konkret godkjenning eller korrigert erstatning |
| P0 | Rom 32, 50 og 88 og de kjente objektsømmene | Motiv og tilstander stemmer både i overlegg og spill |
| P1 | Animasjonsforhåndsvisning og godkjenningsliste | En full bevegelse kan kontrolleres før den omtales som ferdig |
| P1 | Flere figurer, z-masker, tekst og menyer i samme scenario | Kontrollert i ekte spilltilstand uten gjennomsynsfeil |
| P1 | Samstemte tellinger fra én pakke | Rapport med pakke-SHA, dato, kilde og kontrollnivå |
| P1 | Minne i nettleser og mottak | Dokumentert før/etter med samme filer og scenario |
| P2 | Ekte PC/mobil og gjennomspilling | Logget test med åpne avvik |
| Senere | Felles metode for Zak og Sam & Max, mulig handlingshjul | The Dig ferdig og egne piloter godkjent |

Filmene venter fortsatt. Nye shadere, ekstra bloom og parallax prioriteres etter fidelitet og spilltest, og skal være valgfrie hvis de endrer originalens uttrykk.

## 9. Samarbeid og leveranse

- Claude implementerer kontrollverktøy og motorendringer gjennom PR og CI.
- ChatGPT/Codex lager og retter grafikk i gpt-arbeid etter ORDRE.md.
- Tom godkjenner stilen og bevisste avvik.
- Ikke skriv over godkjent leveranse med en ny kandidat uten konkret sammenligning.
- Logg hva som er laget, kontrollert og fortsatt usikkert. Verifiser metadata fra samme pakke før status oppdateres.
- Dokumentasjon kan deles i main. Spillfiler og avledet grafikk følger eksisterende datagrener.
