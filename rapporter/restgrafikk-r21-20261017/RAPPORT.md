# Canyon-figurer, r21, 17. oktober 2026

105 eldre HD-ruter i kostyme 34 er tegnet om etter de godkjente hovedarkene. Boston har igjen brunt hår med grå tinninger, mørk blå trøye og oransje bukser. Maggie har svart bob og oransje drakt. Brink er blond med grå jakke. Hver fysisk rute er tegnet og registrert som én samlet figur eller gruppe. Hodene flyttes eller skaleres ikke separat.

Dette er en arbeidsleveranse i gpt-arbeid og kandidat-r21. Den er ikke integrert i hd-mod eller utgitt som distro. Toms visuelle godkjenning og naturlig gjennomspilling gjenstår.

## Resultat og avgrensning

- 105 selvstendige nytegninger erstatter de eldre publiserte rutene. Opptellingen omfatter også 125 til 129. Forrige rapport talte bare 100 eldre ruter fra jobbinventaret. Motorloggen bekrefter at de fem ekstra også brukes.
- De 25 manglende canyon-rutene som ble laget i r20 beholdes uendret. Kostyme 34 har dermed 130 fysiske HD-ruter i kandidaten.
- 105 indeksbilder får riktig palettreferanse. Indeksverdier, dimensjoner og original spillanimasjon er uendret.
- 210 eksplisitte filerstatninger, ingen nye manglende ruter fylt i denne runden. Restlisten er fortsatt 6 011 faktiske bilder, i tillegg til øvrige eldre grafikkfeil.
- Alle 44 551 filer i publisert r19 er kontrollert. Den publiserte arbeidskopien er uendret. Kandidaten avviker bare i de 210 deklarerte filene og bevarer r20s 442 tillegg og alle 55 HD-filmer.

## Visuell kontroll og motiv

Kilden er kostyme 34 med kodek 1, AKPL-kodene fargelagt gjennom rom 15, palett 0. Canyon-skriptet LSCR 2010 bruker denne sammensatte aktøren når personene hjelper hverandre opp. Serien er ikke scenen der død Brink undersøkes. Originalens beskårne kroppsdeler er bevisst delgrafikk og skal ikke kompletteres med nye hoder eller kropper.

[Før og etter](for-og-etter.png) viser original, publisert r19 og ny r21. Alle nye ruter er vist med original ved siden av i [del 1](preview-01.png), [del 2](preview-02.png) og [del 3](preview-03.png). [Den eldre serien](audit-before.png) dokumenterer feil identiteter og klær før arbeidet.

Tre første atlasforsøk satte feil person i enkelte ruter. De er bevart som rejected-first og er ikke brukt i eksporten. Ark 01 og 02 er laget på nytt med bare Bostons hovedark, ark 05 med Boston og Maggie. Åtte ytterligere fysiske ruter, 78, 79, 80, 81, 89, 95, 108 og 111, er tegnet separat for å rette personbytte, avkuttede hode-/armfragmenter og posering. Native alfa og transparente hull er bevart. Ingen automatisk omrissmåling brukes som bevis for riktig identitet.

Første formkontroll avviste 95 og 111. Et forsøk med sterkere opprydding av alle små separate deler avviste også 5 fordi en virkelig del forsvant. Den oppryddingen er forkastet. Bare den visuelt bekreftede løse blekkflekken ved håndflaten i 23 får sterkere opprydding. Alle 105 sluttfiler består med minst 0,6192 silhuettoverlapp og høyst 10,90 prosent akseavvik fra balansert skala. Dette er tekniske mål, ikke Toms godkjenning.

## Palettfeil funnet i motoren

De gamle indeksbildene bruker kostymets RGBS-palett. Det førte først til rød hud og klær også med riktig ny tegning, fordi motoren bruker indeksbildets palett ved fargetilpasning. [Feilen i motoren](feil-palett-i-motor.png) er bevart. Sluttfilene bruker den skriptfestede AKPL til rompalett-koblingen. Ingen kodeverdier er endret. [Samme prøve etter retting](motor-anim-07.png) viser riktige farger. De gamle HD-tegningene hadde i tillegg feil personer og klær og måtte derfor også tegnes om.

## Motorprøver

Fire native ScummVM-prøver med original animasjon 6, 7, 8 og 9 viser samtlige 130 fysiske ruter, inkludert alle 105 erstatningene. 172 fullomtegningskontroller etter oppstart har null avvik, og ingen kjøringer krasjet. Sluttfilenes SHA-256 er knyttet til prøven i qa-canyon.json og integrity.json. Etter sluttgjennomgangen ble 108 tegnet om separat fordi atlasgrensen klippet Maggie. [Den rettede ruten i motoren](motor-rute-108.png) viser hele Maggie. Animasjon 8 er kjørt på nytt etter denne endringen. Prøvene 6, 7 og 9 brukes videre bare etter SHA-kontroll av samtlige viste ruter og indeksreferanser. Tidlige tekniske prøver med feil palett er diagnostikk og regnes ikke som sluttbevis.

Animasjonene er vist i et isolert prøverom 23 med byteidentiske karakterfarger som rom 15, dokumentert i canyon-palette-proof.json. Dette er ikke en naturlig canyon-gjennomspilling. Testen bruker egne konfigurasjoner og kopierte lagringer. Vanlige lagringer og brukerinnstillinger er urørt.

- [Animasjon 6](motor-anim-06.gif), [stillbilde](motor-anim-06.png)
- [Animasjon 7](motor-anim-07.gif), [stillbilde](motor-anim-07.png)
- [Animasjon 8](motor-anim-08.gif), [stillbilde](motor-anim-08.png)
- [Animasjon 9](motor-anim-09.gif), [stillbilde](motor-anim-09.png)

GIF-ene er et komprimert utvalg av motorens skjermdumper med fast visningstid, ikke en måling av originalt avspillingstempo. Fullt kontrollgrunnlag ligger i motorloggene.

## Sporbarhet og senere integrering

Native bildeverktøy image_gen.imagegen er brukt, modellnavn ble ikke oppgitt. 25 rå native bilder er bevart, hvorav 22 er valgt som eksportkilder. Alle prompter og faktiske hovedarkroller står i prompter.json. Registreringen kobler hver fysisk rute til master, delrute, kildeboks, hovedarkenes SHA-256 og gammel/ny filhash.

REPLACEMENTS.json erklærer de 210 filene som kan byttes ved senere integrering. mod-erstatninger inneholder bare disse. Integreringen må bygge videre på publisert r19 og r20s ADDITIONS.json, med eksplisitt erstatning av de 105 oppførte kostymeenhetene. Ikke bygg modden fra tom mappe. Ingen motor, pipeline, hovedark eller beskyttet jobbfil er endret.

Gjenbruk: prosjektbibliotekets figurark-fast-storrelse og publisert-mod-er-fasit, samt r20s fargeanalyse, myk-registrering og native prøver. Kontrollene er prøvd på de faktiske sluttfilene i denne runden. Se verktoy/ for oppskrifter og fremdrift.json for maskinlesbart omfang.
