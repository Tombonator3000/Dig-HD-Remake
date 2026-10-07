# HD-motoren: slik virker den

HD-motoren er ScummVM med én patch (`engine/patches/0001-dighd-hd-grafikk.patch`). Spillet kjører som før i 320 x 200 med 256 farger. All logikk, alle skript, lagring, lyd og filmer er ScummVM sine. Det eneste som endres, er det aller siste steget, der bildet sendes til skjermen.

## Prinsippet

Hver gang motoren er ferdig med et område av skjermen, bygger patchen det samme området i 4x (eller annen skala) og full farge. For hver piksel avgjøres det hvor HD-pikselen skal hentes fra:

| Hva pikselen viser | Hvordan det avgjøres | Hvor HD-pikselen kommer fra |
| --- | --- | --- |
| Uendret rombakgrunn | Pikselen er lik i forgrunns- og bakgrunnsbufferen, og lik originalbildet `roomNNN_idx.png` | `rooms/roomNNN.png` |
| Objekt (dør, maskin, lys) | Lik i begge buffere, men lik et objektbilde motoren nettopp har tegnet | `objects/objNNN_SS.png` |
| Figur (kostymerute) | Forskjellig fra bakgrunnsbufferen, og innenfor en rute motoren nettopp har tegnet | `costumes/costumeCCC_NNN.png` |
| Filmramme | Filmen og rammenummeret er kjent, og pikselen er ikke tekst | `san/FILM/NNNNN.png` |
| Tekst over film (undertekster) | SmushPlayer tegner teksten en gang til i et eget lag | Originalpikselen skalert opp |
| Alt annet (tekst, effekter, ting uten HD-bilde) | | Originalpikselen skalert opp |

Fordi alt som ikke kan avgjøres sikkert faller tilbake til originalpikselen, kan HD-grafikken legges inn litt etter litt. Spillet virker hele veien.

## Farger

- **Palettbytte og toning:** Når fargen motoren viser er forskjellig fra fargen HD-bildet ble laget med, justeres HD-pikselen med forholdet mellom dem. Fade til svart og lysbytter følger derfor med. Bare pikslene som får en annen farge, bygges på nytt (se Fargesykling under).
- **Fargesykling:** Farger som sykles (vann, energi, lys) skifter hele tiden. HD-bakgrunnen og HD-objektene vises også der, og følger syklingen. Se eget avsnitt under.
- **Figurer:** Kostymene har sine "ekte" farger i RGBS-blokken. Motoren tilpasser dem til rompaletten og lyset. HD-sprites bruker de ekte fargene, og justeres bare når rommet er tydelig mørkere eller lysere. Skygger og spesialeffekter blir originalpiksler. Det samme gjelder en piksel som er svart i den ekte fargen, men vises lys i spillet, for da er det ikke denne fargen som vises (se kodek 5 under Hva som er testet).
- **Skalerte figurer:** Figurer som skaleres med dybden, tegnes med HD-pikslene skalert jevnt i stedet for med originalens hoppemønster. Silhuetten følger fortsatt originalen.

## Fargesykling

I 52 rom sykles deler av paletten (CYCL): fargene i et indeksområde roteres et steg om gangen, og vann, lys og energi ser ut til å bevege seg. Originalbildet har de samme indeksene hele tiden, det er fargen bak hver indeks som flytter seg.

Justering per piksel (forholdet mellom nåværende og opprinnelig farge for indeksen, som ved toning) virker ikke her. Nabopiksler med ulike indekser får helt ulike forhold samtidig, og da synes hver 4 x 4-blokk i HD-bildet som en egen rute. Før ble syklede piksler derfor vist som originalpiksler.

Nå brukes et jevnt fargekart:

1. For hver palettindeks regnes det ut hvordan fargen er endret: forholdet mellom nåværende og opprinnelig farge per kanal, som ved toning. Uendret farge gir 1. En kanal som er svart i originalen kan ikke skaleres og får den nåværende verdien, også som ved toning. Forholdet er begrenset til 2, og resten av endringen legges til, så støyen i HD-bildet ikke forsterkes mye der originalfargen er nesten svart.
2. For hver HD-piksel interpoleres disse tallene (forhold og tillegg) fra de 3 x 3 originalpikslene rundt med en kvadratisk B-spline. Kartet er glatt (også stigningen er sammenhengende), så det blir ingen kanter ved blokkgrensene.
3. HD-pikselen ganges med det interpolerte forholdet, og tillegget legges til.

Dette gjelder bare piksler som viser HD-bakgrunn eller et HD-objekt (`roomNNN.png`, `objNNN_SS.png`), og bare der pikselen selv eller en av de 8 naboene i originalbildet har en syklet indeks. Kartet leses fra indeksbildet (`_idx.png`), ikke fra skjermen, så en figur som går foran vannet påvirker det ikke. Naboer som ikke sykles, har forhold 1, så endringen går jevnt over til null innen en halv originalpiksel utenfor det syklede området. Pikslene utenfor ringen av naboer blir ikke rørt, så det blir ingen glorie rundt steiner og kanter. Fordi naboene i ringen også går gjennom kartet, blir det heller ingen synlig kant rundt ikke-syklede piksler inne i vannet.

Når hele paletten tones (fade), har alle indekser samme forhold, og resultatet blir det samme som justeringen per piksel.

Valg og begrunnelse. Metodene ble først prøvd i Python på rom 22 (HD-bildet fra ChatGPT og paletten rotert 0 til 7 steg), så ble den valgte bygget inn og kontrollert i dumper fra spillet. To mål, regnet bare i vannet:

- Blokkmål: fargesprang over 4 x 4-blokkgrensene delt på fargesprang inne i blokkene. HD-bildet selv har 1,0.
- Kantsprang: gjennomsnittlig fargesprang over grensen mellom syklede og ikke-syklede piksler. HD-bildet selv har 29,8.

| Metode | Resultat |
| --- | --- |
| Originalpiksler (slik det var) | Blokkmål 5,6 til 6,0 og kantsprang 58 til 66 i dumpene |
| Forhold per piksel (som toning) | Tydelig rutenett. Blokkmål opptil 4,8 |
| Bilineær interpolasjon | Blokkmål 1,04, men små stjerne- og rutermønstre der nabofargene er svært ulike, fordi stigningen knekker midt i hver blokk |
| Kvadratisk B-spline (valgt) | Glatt, ingen synlige blokker. Blokkmål 1,04 til 1,09 i prøven og 1,01 til 1,07 i dumpene, kantsprang 30,6 til 32,3 |
| Kubisk B-spline | Blokkmål 1,02, men trenger 5 x 5 naboer og gir 10 prosent mindre bevegelse |
| Uskarphet først, så bilineær | Blokkmål 1,00, men bare 60 prosent av bevegelsen med bilineær |
| Uten naboringen (bare syklede piksler) | Harde kanter rundt de ikke-syklede pikslene inne i vannet: kantsprang 41 til 44 |
| Differanse (pluss) i stedet for forhold | Ser likt ut i vannet, men ville latt detaljene i HD-bildet stå igjen ved fade til svart. Forholdet ble valgt |

Bevegelsen er svakere enn i originalen der syklingen består av enkeltpiksler (glitter i fossen i rom 43), fordi kartet jevner ut over 3 x 3 piksler. I vannet i rom 22 synes bølgene tydelig.

Figurer med syklede farger (lys på drakter og maskiner) vises fortsatt med originalpikslene der fargen sykles, som andre effekter. Filmrammer med HD-ramme vises som de ble laget.

Hvilke piksler som bygges på nytt: når paletten endres, bygges bare de pikslene som viser en endret farge, og pikslene som sist gikk gjennom fargekartet (de avhenger av naboene), på nytt. Det skjer i bånd på 8 rader, hvert så bredt som de endrede pikslene i båndet. Ved fade blir det hele skjermen som før. Endres settet av syklede indekser (nytt rom eller skript), bygges hele skjermen.

## Klassisk grafikk og gult felt

To hurtigtaster virker mens spillet går, så lenge en HD-mod er lastet:

| Tast | Virkning |
| --- | --- |
| Ctrl+H | Bytter mellom HD-grafikk og klassisk grafikk |
| Ctrl+Shift+H | Slår gult felt der HD mangler av og på |

ScummVM viser en kort melding på skjermen når du bytter ("Dig HD: klassisk grafikk" og så videre). Tastene går ikke videre til spillet.

**Klassisk grafikk** er originalpikslene skalert opp med nearest over hele skjermen, også filmer som har HD-rammer. Skjermen er like stor som før, så vinduet og musen endres ikke. Pekeren er den samme i begge modusene. Motoren fortsetter å finne ut hvor HD-pikslene skal hentes fra også i klassisk modus, så byttet tilbake til HD skjer med en gang.

**Gult felt** blander halvparten gult inn i hver piksel som vises som originalpiksel fordi HD mangler:

- rombakgrunn i rom uten HD-bakgrunn, også fargesyklede piksler (før var de unntatt, fordi syklede piksler alltid var originalpiksler)
- bakgrunnspiksler som ikke stemmer med HD-bakgrunnen og ikke med noe HD-objekt (objekter uten HD-bilde)
- figurer der kostymeruten ikke har HD-bilde
- filmrammer uten HD-ramme (hele bildet unntatt teksten som SmushPlayer tegner over filmen)

Dette farges ikke gult, fordi det er originalt med vilje eller har HD:

- fargesyklede områder i HD-bakgrunnen og HD-objekter (de vises med HD, se Fargesykling)
- syklede farger på figurer (lys og effekter)
- tekst og undertekster over spillet, så lenge de ikke ligger oppå en figur uten HD
- undertekster og annen tekst over filmer, også over filmrammer uten HD-ramme
- skygger og effekter på figurer med HD-bilde
- bannere (pause, volum), overgangseffekter og musepekeren

I klassisk modus farges ingenting gult. Når gult felt slås på mens spillet går, sendes skjermen gjennom motoren på nytt, så figurer uten HD blir gule fra neste bilde. Bakgrunn og objekter blir gule med en gang.

Valg av taster: SCUMM-motoren bruker Ctrl med tallene, F, G, T, V, K og C (og B, D, J, N og R i andre SCUMM-spill). ScummVM bruker Ctrl+M, Ctrl+R, Ctrl+U, Ctrl+Q, Ctrl+Z, Ctrl+F5, Ctrl+F7, Alt+S, Alt+Enter og Ctrl+Alt med flere taster for grafikkvalg. Sjekket i `engines/scumm/input.cpp`, `engines/scumm/metaengine.cpp`, `engines/metaengine.cpp`, `backends/events/default/default-events.cpp` og `backends/graphics/sdl/sdl-graphics.cpp`. H brukes ikke med Ctrl eller Ctrl+Shift i noen av disse, og ingen av tastaturoppsettene som er aktive i The Dig har H alene, så ScummVM sender tasten videre til motoren. Y og J ble valgt bort fordi bekreftelsesdialogene i ScummVM svarer ja på Y, og på J med norsk språk. Begge funksjonene ligger på samme bokstav, så de er lette å huske.

Ytelse: når begge er av, er bildebyggingen like rask som før. Målt uten skjerm med 300 hele skjermbilder i rom 22 og 28 (beste tid): 8,0 til 8,9 ms per bilde både før og etter endringen, og 0,3 til 0,5 ms for å finne kildene til et helt bilde. Figurer uten HD letes bare etter i en egen runde når gult felt er på. Med gult felt på ble tidene de samme i disse rommene. Klassisk modus er raskere, under 1 ms per bilde. Tider etter fargesyklingen står under Hva som er testet.

## Undertekster over filmer

SmushPlayer tegner undertekster og annen filmtekst rett inn i filmrammen (8 bit), etter at rammen er pakket ut. En HD-ramme dekker hele bildet, så teksten må legges oppå HD-rammen igjen. Slik gjøres det:

1. Før teksten tegnes, lager DigHD et lag med hele filmrammen der hver byte er invertert (XOR 0xFF).
2. SmushPlayer tegner den samme teksten to ganger: først i laget, så i filmrammen som før.
3. Etterpå er laget og filmrammen like nøyaktig i de pikslene teksten skrev. Alle andre piksler er ulike, fordi en invertert byte aldri er lik seg selv. Pikslene som er like, merkes som tekst.
4. Når rammen vises, er tekstpikslene originalpiksler skalert opp med nearest, og resten kommer fra HD-rammen. Teksten ligger derfor på nøyaktig samme sted som i originalen.
5. Merkene nullstilles når en ny ramme pakkes ut og når en ny film starter. Viser filmen samme bilde videre uten å pakke ut noe nytt, står teksten i rammen fortsatt, og da beholdes merkene også.

Hvorfor denne løsningen: teksttegneren i ScummVM skriver bare piksler og leser aldri det som ligger under, så to tegninger gir samme resultat. Det enkleste alternativet, å ta vare på rammen før teksten og se hvilke piksler som endret seg, mister tekstpiksler som har samme farge som filmen under (svart kant på svart bakgrunn). Der ville HD-pikselen blitt vist i stedet. Med laget blir det nøyaktig, uten å endre teksttegneren. Det koster én ekstra tekstutskrift og to gjennomganger av rammen (64 000 byte) per tekst.

Med undertekster slått av (ScummVM-innstillingen `subtitles`) tegner SmushPlayer ikke underteksten, og hele rammen er HD. Tekst uten bryterflagget, som "Borneo Deep Space Observatory" i introen, vises alltid, som i originalen.

Klassisk grafikk viser hele filmen som originalpiksler. Med gult felt blir filmrammer uten HD-ramme gule, men ikke teksten.

Filmrammene bygges på samme måte som resten av skjermen, med en kilde per piksel. Dumpene (`DIGHD_DUMP_DIR`) og `DIGHD_VERIFY` viser derfor det som faktisk er på skjermen, også HD-rammen og teksten. Ytelse uten skjerm, snitt over 400 rammer av introen: lesing av HD-rammen (PNG i 1280 x 800) tar omtrent 23 ms per ramme, og resten (kilder, bygging av bildet og kopi til skjermen) omtrent 2 ms.

## Stedene i ScummVM som er endret

| Fil | Endring |
| --- | --- |
| `engines/scumm/dighd.cpp`, `dighd.h` | All HD-logikk (ny fil) |
| `scumm.cpp` | Lager DigHD, setter opp HD-skjermen, motoren holder seg i 8 bit, hook før hver skjermoppdatering |
| `gfx.cpp` | Siste blit (`drawStripToScreen`), overgangseffekter, `moveScreen`, risting av skjermen |
| `palette.cpp` | Palett sendes til DigHD i stedet for til skjermen |
| `object.cpp` | Melder hvilke objekter som tegnes og i hvilken tilstand |
| `akos.cpp`, `akos.h`, `base-costume.cpp` | Melder hvilke kostymeruter som tegnes, hvor og om de er speilvendt |
| `cursor.cpp`, `input.cpp`, `saveload.cpp` | Musepeker i HD, museposisjon delt på skala, hurtigtastene Ctrl+H og Ctrl+Shift+H |
| `smush/smush_player.cpp` | Filmrammer og filmpalett via DigHD. Filmteksten tegnes også i laget til DigHD, og DigHD får beskjed når en ny ramme er pakket ut |

## Innstillinger

| Variabel / nøkkel i scummvm.ini | Betydning |
| --- | --- |
| `DIGHD_MOD` / `dighd_mod` | Mappen med HD-grafikk. Uten denne kjører spillet helt som vanlig |
| `DIGHD_SCALE` / `dighd_scale` | Skala, standard 4 |
| `DIGHD_CLASSIC=1` / `dighd_classic=true` | Starter i klassisk grafikk (Ctrl+H bytter) |
| `DIGHD_SHOW_MISSING=1` / `dighd_show_missing=true` | Starter med gult felt der HD mangler (Ctrl+Shift+H slår av og på) |

Miljøvariabelen går foran nøkkelen i scummvm.ini. `DIGHD_CLASSIC=0` gir HD selv om `dighd_classic=true` står i filen.

Test og feilsøking (bare miljøvariabler):

| Variabel | Betydning |
| --- | --- |
| `DIGHD_VERIFY=1` | Ved hver dump: sammenligner HD-bildet med originalen og skriver avviket i loggen (gult felt er ikke med), og sjekker at skjermen er lik hele skjermen bygget på nytt |
| `DIGHD_DUMP_DIR`, `DIGHD_DUMP_EVERY` | Lagrer skjermbildet som PNG hver N-te bilde: `frame_NNNNNN_roomRRR.png`, eller `frame_NNNNNN_FILM_RRRRR.png` under en film (RRRRR er rammenummeret, som i `san/FILM/`) |
| `DIGHD_BENCH=N` | Ved hver dump: bygger hele skjermen N ganger og skriver snittid per gang, og i rom med fargesykling tiden for ett steg i syklingen (alle syklede farger endret) |
| `DIGHD_SKIP_VIDEO=1` | Hopper over filmer |
| `DIGHD_TEST_ROOM`, `DIGHD_TEST_AT`, `DIGHD_TEST_CAMX` | Hopper rett til et rom etter N bilder |
| `DIGHD_QUIT_AT` | Avslutter etter N bilder |
| `DIGHD_TEST_KEYS` | Trykker taster ved gitte bilder, for eksempel `420:ctrl+h,570:ctrl+shift+h`. Tastene går gjennom den vanlige tastehåndteringen i motoren |

Loggen teller pikslene per kilde: `HD room px`, `HD object px`, `HD sprite px` og `original px`, og `HD film px` når en HD-filmramme er vist. `cycled HD px` er pikslene som gikk gjennom fargekartet for fargesykling (de er også med i `HD room px` eller `HD object px`). Med gult felt på kommer `yellow px` i tillegg (de gule er også med i `original px`), og i klassisk modus står det `classic` til slutt. Tallene er originalpiksler, summert over alt som er bygget siden forrige dump.

Med `DIGHD_VERIFY=1` skriver hver dump to eller tre linjer:

- `N screen pixels differ from the whole screen built again`: skjermen bygges bit for bit (skitne områder, palettendringer). Er tallet over 0, har en del av skjermen ikke blitt bygget på nytt når den skulle.
- `N of M HD pixels differ strongly from the original`: avvik mot originalen, for pikslene utenfor fargesyklingen.
- `colour cycling, N of M HD pixels differ strongly`: avvik i pikslene som gikk gjennom fargekartet. De er jevnet ut mellom originalpikslene med vilje, så med en `nearest`-mod avviker noen av dem. De holdes utenfor hovedtallet.

Under en film skriver hver dump også en linje for selve rammen, i originalpiksler: `film SQ1 frame 487: 61155 px from HD frame, 2845 px original on purpose (text), 0 px original without HD`. Med `DIGHD_VERIFY=1` skriver hver dump utenom film hvilke kostymer hver skuespiller sist ble tegnet med, og hvor mange av rutene som har HD-bilde: `costumes drawn: actor 6 costume 210 (1 cels HD, 0 without)`.

## Hva som er testet

Med en mod laget med `nearest` skal HD-bildet være likt originalen skalert opp. Det er sjekket i spillet uten skjerm (`engine/test.sh`):

- Bakgrunner og uskalerte figurer: 0 avvikende piksler.
- Skalerte figurer: avvik på indre kanter (under 0,25 prosent av skjermen), fordi HD-sprites skaleres jevnt. Det er ventet. Kjøring 2026-10-07 etter rettingene for kodek 5: 0 avvik ved bilde 250, 750, 1500 og 2250 til 3000, og 0,032 til 0,199 prosent ved bilde 500, 1000, 1250, 1750 og 2000. Avvikene i bilde 1250 er sett på: indre kanter i en astronaut.
- Siste kjøring (2026-10-07, etter fargesyklingen): 0 avvik ved bilde 250, 750, 1000, 1750 og 2500 til 3000, og 0,103 til 0,179 prosent ved bilde 500, 1250, 1500, 2000 og 2250. Hvilke bilder som har en skalert figur, varierer litt fra kjøring til kjøring, fordi animasjonen følger klokka. Avvikene i bilde 1500 er sett på: indre kanter i en astronaut. Skjermen var lik hele skjermen bygget på nytt i alle 12 dumper. Rommene i testen har ingen syklede piksler i bakgrunnen.
- Objekter: rom 34 og 105 testet med HD-objekter, 0 avvikende piksler.
- Filmrammer: 198 av 198 rammer i introen er like. Rammenummeret er `_frame - 1` i SmushPlayer. Etter endringen for undertekster: rammene 0 til 527 i introen er like (ingen avvik i stikkprøvene utenom teksten).

Klassisk grafikk og gult felt (testet uten skjerm 2026-10-07, modden `gpt` i rom 22 og 28 og introen):

- Klassisk dump i rom 22 og 28: alle 4 x 4 blokker er ensfargede, og bildet skalert ned er likt originalgrafikken i `work/extract` bortsett fra fargesyklet vann (rom 22) og teksten "exit" (rom 28).
- Gult felt: rom uten HD-bakgrunn blir gult, HD-bakgrunnen i rom 22 og HD-objektet i rom 28 blir ikke gule, heller ikke vannet i rom 22 eller teksten i rom 28. I introen med en mod uten kostymer blir astronautene gule, mens bakgrunnen og underteksten ikke blir det.
- Film med HD-rammer: HD-rammene brukes i HD-modus, ikke i klassisk modus, og blir ikke gule.
- Tastene: `DIGHD_TEST_KEYS` trykket Ctrl+H og Ctrl+Shift+H mens spillet gikk, og byttet virket begge veier. Ikke testet med ekte tastatur og skjerm, og meldingen på skjermen er ikke sett.
- `engine/test.sh` gir fortsatt 0 avvik for bakgrunner og uskalerte figurer.

Fargesykling (testet uten skjerm 2026-10-07). Spillet hoppet med `DIGHD_TEST_ROOM` til rommet ved bilde 240, med dumper hvert 2. bilde:

- Rom 22 med modden `gpt` (HD-bildet fra ChatGPT): vannet er HD og beveger seg mellom rammene, uten rutenett. Blokkmål 1,01 til 1,07 i 8 dumper på rad (HD-bildet 1,01, før 5,6 til 6,0). Kantsprang 30,6 til 32,3 (HD-bildet 29,8, før 58 til 66). Endringen holder seg i vannet og en halv originalpiksel utenfor, ingen glorie ved steinene. 5667 syklede piksler og 3112 naboer går gjennom kartet.
- Rom 43 og 11 med en `lanczos-sharp`-mod: fossen (bakgrunn og objekt 347) og sjøen beveger seg uten rutenett. I rom 43 går 9736 piksler gjennom kartet, også objektpiksler. De mørke flekkene som kommer og går i fossen, er piksler med en fast mørk indeks (85) i objektet, og de er like i originalen.
- Rom 2 (modden har ikke bakgrunn her): som før, originalpiksler. Rommets bakgrunn og objekter har ingen syklede indekser. Indeks 198 til 200 sykles, men brukes av figurene.
- Klassisk grafikk (rom 22): alle 4 x 4-blokker ensfargede, også vannet.
- Gult felt (rom 22): 0 gule piksler, vannet er HD. I rom 2 er hele bakgrunnen gul.
- Med `nearest`-mod (`test-nearest`) i rom 22 og 43 og `DIGHD_VERIFY=1`: 0 avvik utenfor syklingen. I syklingen avviker 0 til 6,2 prosent av HD-pikslene kraftig, fordi kartet er jevnt med vilje (andelen avhenger av hvor langt syklingen har kommet).
- Skjermen lik hele skjermen bygget på nytt (`DIGHD_VERIFY`): 0 avvikende piksler i rom 22, 43, 11 og 2, i introen med modden `test-san` (HD-rammer for SQ1), og i rom 22 med Ctrl+H og Ctrl+Shift+H av og på. Kontrollen ble prøvd med en feil med vilje (naboene i kartet ble ikke bygget på nytt): da fant den 297 til 435 piksler.
- Ytelse, målt med `DIGHD_BENCH=100` ved hver 25. bilde i 1300 bilder (42 målinger, 25-persentil og median). Før ble hele skjermen bygget ved hver endring av paletten, også ved hvert steg i syklingen:

| Rom | Før: hele skjermen | Etter: ett syklingssteg | Etter: hele skjermen (fade, romskifte) |
| --- | --- | --- | --- |
| 22 (`gpt`) | 7,8 / 8,0 til 8,1 ms | 2,0 / 2,1 til 2,2 ms | 9,0 til 9,1 / 9,4 til 9,8 ms |
| 43 (`lanczos-sharp`) | 7,9 / 8,2 ms | 4,8 / 5,0 ms | 9,3 / 9,9 ms |
| 28 (`gpt`, ingen sykling) | 8,5 / 8,7 ms | | 8,3 / 8,6 ms |

  Maskinen er en delt virtuell maskin, og tidene varierer med omtrent 1 ms mellom kjøringer. Ikke testet med ekte skjerm.
- Fade med syklede farger på skjermen er ikke sett i spillet. Formelen gir det samme som justeringen per piksel når alle farger endres likt.

Undertekster over filmer (testet uten skjerm 2026-10-07, introen SQ1 med `--subtitles`):

- Moddene: `test-sub` (alle 3772 rammer i SQ1 laget med `nearest`) og `test-sub-merket` (bare rammene 340 til 560, der grønt i piksel (3, 3) i hver 4 x 4-blokk er byttet med XOR 0x20). Merket viser i dumpen om en blokk kom fra HD-rammen eller er en originalpiksel skalert opp.
- `test-sub` med `DIGHD_VERIFY=1`: 0 sterkt avvikende piksler i alle 28 dumper, og ingen avvik i stikkprøvene mellom HD-rammen og originalen for 528 rammer. Rammer med tekst har 1213 til 2845 tekstpiksler som originalpiksler, resten fra HD-rammen.
- `test-sub-merket` med gult felt, sammenlignet piksel for piksel med en klassisk kjøring av de samme filmrammene og med rammene uten tekst fra `dighd san` (27 dumper):
  - 10 rammer med HD-ramme, 8 av dem med undertekst. Hver blokk er enten merket (fra HD-rammen) eller ensfarget (originalpiksel). Alle synlige tekstpiksler er originalpiksler. De andre originalpikslene (0 til 32 per ramme) er tekstpiksler med samme farge som filmen under. HD-blokkene har samme farge som rammen fra `dighd san`, og bildet skalert ned er likt den klassiske dumpen, så teksten står på samme sted som i originalen.
  - 17 rammer uten HD-ramme: alt er gult unntatt teksten. I de to rammene med "Borneo Deep Space Observatory" er nøyaktig de 1425 tekstpikslene ikke gule.
  - Klassisk grafikk: alle blokker ensfargede.
- `--no-subtitles`: ingen tekstpiksler i rammene med undertekst. Teksten uten bryterflagg vises fortsatt.
- `DIGHD_TEST_KEYS` midt i filmen: Ctrl+H ga klassisk grafikk og tilbake til HD, og etter Ctrl+Shift+H var det 0 gule piksler i rammer med HD-ramme og tekst.
- Skjermen uten skjermkort (SDL dummy) er 16 bit (RGB565). Sammenligningene med `work/san` er gjort etter samme avrunding.
- Ikke testet med ekte skjerm.

Kodek 5 (testet uten skjerm 2026-10-07). Modden `test-k5` er laget med `nearest` og har alle 144 kostymer med kodek 5 og de 59 rommene de ligger i. Spillet hoppet med `DIGHD_TEST_ROOM` til hvert av rommene, med `DIGHD_VERIFY=1` og 700 bilder etter hoppet. Kodeken er lest fra AKHD-blokken i hver kostyme (`work/extract/costumes.json` har ikke kodek).

- Funnet og rettet: indeksbildene for alle kostymer med kodek 5 (14 124 ruter) og 150 objektbilder (inventaret i rom 93 og 6 i rom 107) har gjennomsiktig palettindeks 255. I PNG krever det en tRNS-blokk med 256 verdier, og da gjør PNG-leseren i ScummVM bildet om til RGBA. DigHD avviste dem ("not an 8-bit indexed PNG"), så ingen av dem fikk HD. Nå leses indeksbildet uten tRNS-blokken, og den gjennomsiktige indeksen hentes fra blokken.
- Funnet og rettet: piksler der den ekte fargen er svart, men spillet viser en lys farge, ble svarte i HD (30 piksler i kostyme 210 i rom 78). Nå blir de originalpiksler, som skygger og effekter. Dette fjernet også noen avvik i `engine/test.sh` (bilde 250 gikk fra 72 til 0).
- Funnet og rettet: krasj i `compose` når en fade bygget skjermen på nytt rett etter bytte fra et rom med HD-bakgrunn til et rom uten (rom 79 til 92, sett med gdb). Pikslene pekte fortsatt inn i bildet til det gamle rommet. Nå blir de originalpiksler ved romskifte til de tegnes på nytt. Dette kan også skje i vanlig spill.
- Etter rettingene ble 30 kostymer med kodek 5 tegnet med HD i 15 rom: 31 (rom 13), 74 (25), 119 (34), 278 til 281 (40), 318 (47), 326 (66), 320 (72), 210 (78), 238 (89), 240 (91), 225 (79), 282 til 297 (96 til 99). 0 sterkt avvikende piksler i alle 135 dumper.
- Andel av figurpikslene som kom fra HD-bildet (resten er originalpiksler som skygger, effekter eller farger som ikke stemmer): 91 prosent i rom 13, 69 prosent i rom 40, 60 til 85 prosent i rom 78.
- Ikke testet: inventaret (rom 93) og rom 107 i spillet, og ekte HD-bilder for kodek 5.

## Kjente begrensninger

- Kostymer med kodek 16 (5 kostymer) får ikke HD-sprites ennå. Kodek 1 (182 kostymer, blant dem hovedpersonene) og kodek 5 (144 kostymer) er testet i spillet.
- Kodek 5: når skriptet ikke har satt skuespillerpaletten, tegner ScummVM kodene rett som palettindekser i rommet, uten AKPL (`_useBompPalette` i `akos.cpp`). Uttrekket farger rutene med RGBS, som følger AKPL. Da har HD-bildet andre farger enn spillet for kodene der AKPL ikke er lik koden. Sett i kostyme 210 i rom 78: kode 26 er svart i uttrekket og brun i spillet. Pikslene med for store fargeforskjeller blir originalpiksler, de andre justeres med forholdet mellom fargene. Om uttrekket bør bruke rompaletten for slike kostymer, er ikke avgjort.
- Objekter som tegnes direkte i bakgrunnsbufferen av skript (sjeldent) blir originalpiksler.
- Fargesykling: kartet jevner ut over 3 x 3 originalpiksler, så glitter av enkeltpiksler (fossen i rom 43) beveger seg svakere enn i originalen. Bølger over flere piksler (vannet i rom 22) synes godt.
- Fargesykling: kartet leses fra indeksbildet til rommet eller objektet. Ligger et objekt over syklet vann, får bakgrunnspikselen rett ved siden av objektet litt av syklingen under objektet. Ikke sett i rommene som er prøvd.
- Fargesykling på figurer (lys på drakter og maskiner) er fortsatt originalpiksler.
- Tegnsett og tekst er originalpiksler, også undertekster over HD-filmer. HD-fonter er en senere jobb.
- Undertekster over filmer: merkene for tekst nullstilles når en ny ramme pakkes ut. Pakker en film ut bare en del av bildet (RLE i SMUSH med mindre rektangel, ikke brukt i The Dig), regnes tekst utenfor den delen som borte selv om den står igjen.
- Gult felt: tekst som ligger oppå en figur uten HD, blir gul, fordi motoren bare vet hvilket rektangel figuren dekker. Det samme gjelder tekst der en figur uten HD sist ble tegnet, til figuren tegnes på nytt eller rommet byttes.
