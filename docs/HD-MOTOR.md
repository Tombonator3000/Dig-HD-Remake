# HD-motoren: slik virker den

HD-motoren er ScummVM med én patch (`engine/patches/0001-dighd-hd-grafikk.patch`). Spillet kjører som før i 320 x 200 med 256 farger. All logikk, alle skript, lagring, lyd og filmer er ScummVM sine. Det eneste som endres, er det aller siste steget, der bildet sendes til skjermen.

## Prinsippet

Hver gang motoren er ferdig med et område av skjermen, bygger patchen det samme området i 4x (eller annen skala) og full farge. For hver piksel avgjøres det hvor HD-pikselen skal hentes fra:

| Hva pikselen viser | Hvordan det avgjøres | Hvor HD-pikselen kommer fra |
| --- | --- | --- |
| Uendret rombakgrunn | Pikselen er lik i forgrunns- og bakgrunnsbufferen, og lik originalbildet `roomNNN_idx.png` | `rooms/roomNNN.png` |
| Objekt (dør, maskin, lys) | Lik i begge buffere, men lik et objektbilde motoren nettopp har tegnet | `objects/objNNN_SS.png` |
| Figur (kostymerute) | Forskjellig fra bakgrunnsbufferen, og innenfor en rute motoren nettopp har tegnet | `costumes/costumeCCC_NNN.png` |
| Filmramme | Filmen og rammenummeret er kjent | `san/FILM/NNNNN.png` |
| Alt annet (tekst, effekter, ting uten HD-bilde) | | Originalpikselen skalert opp |

Fordi alt som ikke kan avgjøres sikkert faller tilbake til originalpikselen, kan HD-grafikken legges inn litt etter litt. Spillet virker hele veien.

## Farger

- **Palettbytte og toning:** Når fargen motoren viser er forskjellig fra fargen HD-bildet ble laget med, justeres HD-pikselen med forholdet mellom dem. Fade til svart og lysbytter følger derfor med.
- **Fargesykling:** Farger som sykles (vann, energi) skifter fargetone hele tiden. Der brukes originalpikselen, så animasjonen blir som før. Vil du ha HD her, må det lages som eget animert lag senere.
- **Figurer:** Kostymene har sine "ekte" farger i RGBS-blokken. Motoren tilpasser dem til rompaletten og lyset. HD-sprites bruker de ekte fargene, og justeres bare når rommet er tydelig mørkere eller lysere. Skygger og spesialeffekter blir originalpiksler.
- **Skalerte figurer:** Figurer som skaleres med dybden, tegnes med HD-pikslene skalert jevnt i stedet for med originalens hoppemønster. Silhuetten følger fortsatt originalen.

## Klassisk grafikk og gult felt

To hurtigtaster virker mens spillet går, så lenge en HD-mod er lastet:

| Tast | Virkning |
| --- | --- |
| Ctrl+H | Bytter mellom HD-grafikk og klassisk grafikk |
| Ctrl+Shift+H | Slår gult felt der HD mangler av og på |

ScummVM viser en kort melding på skjermen når du bytter ("Dig HD: klassisk grafikk" og så videre). Tastene går ikke videre til spillet.

**Klassisk grafikk** er originalpikslene skalert opp med nearest over hele skjermen, også filmer som har HD-rammer. Skjermen er like stor som før, så vinduet og musen endres ikke. Pekeren er den samme i begge modusene. Motoren fortsetter å finne ut hvor HD-pikslene skal hentes fra også i klassisk modus, så byttet tilbake til HD skjer med en gang.

**Gult felt** blander halvparten gult inn i hver piksel som vises som originalpiksel fordi HD mangler:

- rombakgrunn i rom uten HD-bakgrunn
- bakgrunnspiksler som ikke stemmer med HD-bakgrunnen og ikke med noe HD-objekt (objekter uten HD-bilde)
- figurer der kostymeruten ikke har HD-bilde
- filmrammer uten HD-ramme (hele bildet, også undertekst som er tegnet inn i filmen)

Dette farges ikke gult, fordi det er originalt med vilje:

- fargesyklede palettindekser (vann, lys, energi)
- tekst og undertekster over spillet, så lenge de ikke ligger oppå en figur uten HD
- skygger og effekter på figurer med HD-bilde
- bannere (pause, volum), overgangseffekter og musepekeren

I klassisk modus farges ingenting gult. Når gult felt slås på mens spillet går, sendes skjermen gjennom motoren på nytt, så figurer uten HD blir gule fra neste bilde. Bakgrunn og objekter blir gule med en gang.

Valg av taster: SCUMM-motoren bruker Ctrl med tallene, F, G, T, V, K og C (og B, D, J, N og R i andre SCUMM-spill). ScummVM bruker Ctrl+M, Ctrl+R, Ctrl+U, Ctrl+Q, Ctrl+Z, Ctrl+F5, Ctrl+F7, Alt+S, Alt+Enter og Ctrl+Alt med flere taster for grafikkvalg. Sjekket i `engines/scumm/input.cpp`, `engines/scumm/metaengine.cpp`, `engines/metaengine.cpp`, `backends/events/default/default-events.cpp` og `backends/graphics/sdl/sdl-graphics.cpp`. H brukes ikke med Ctrl eller Ctrl+Shift i noen av disse, og ingen av tastaturoppsettene som er aktive i The Dig har H alene, så ScummVM sender tasten videre til motoren. Y og J ble valgt bort fordi bekreftelsesdialogene i ScummVM svarer ja på Y, og på J med norsk språk. Begge funksjonene ligger på samme bokstav, så de er lette å huske.

Ytelse: når begge er av, er bildebyggingen like rask som før. Målt uten skjerm med 300 hele skjermbilder i rom 22 og 28 (beste tid): 8,0 til 8,9 ms per bilde både før og etter endringen, og 0,3 til 0,5 ms for å finne kildene til et helt bilde. Figurer uten HD letes bare etter i en egen runde når gult felt er på. Med gult felt på ble tidene de samme i disse rommene. Klassisk modus er raskere, under 1 ms per bilde.

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
| `smush/smush_player.cpp` | Filmrammer og filmpalett via DigHD |

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
| `DIGHD_VERIFY=1` | Sammenligner HD-bildet med originalen ved hver dump og skriver avviket i loggen. Gult felt er ikke med i sammenligningen |
| `DIGHD_DUMP_DIR`, `DIGHD_DUMP_EVERY` | Lagrer skjermbildet som PNG hver N-te bilde |
| `DIGHD_SKIP_VIDEO=1` | Hopper over filmer |
| `DIGHD_TEST_ROOM`, `DIGHD_TEST_AT`, `DIGHD_TEST_CAMX` | Hopper rett til et rom etter N bilder |
| `DIGHD_QUIT_AT` | Avslutter etter N bilder |
| `DIGHD_TEST_KEYS` | Trykker taster ved gitte bilder, for eksempel `420:ctrl+h,570:ctrl+shift+h`. Tastene går gjennom den vanlige tastehåndteringen i motoren |

Loggen teller pikslene per kilde: `HD room px`, `HD object px`, `HD sprite px` og `original px`. Med gult felt på kommer `yellow px` i tillegg (de gule er også med i `original px`), og i klassisk modus står det `classic` til slutt.

## Hva som er testet

Med en mod laget med `nearest` skal HD-bildet være likt originalen skalert opp. Det er sjekket i spillet uten skjerm (`engine/test.sh`):

- Bakgrunner og uskalerte figurer: 0 avvikende piksler.
- Skalerte figurer: avvik på indre kanter (under 0,25 prosent av skjermen), fordi HD-sprites skaleres jevnt. Det er ventet.
- Objekter: rom 34 og 105 testet med HD-objekter, 0 avvikende piksler.
- Filmrammer: 198 av 198 rammer i introen er like. Rammenummeret er `_frame - 1` i SmushPlayer.

Klassisk grafikk og gult felt (testet uten skjerm 2026-10-07, modden `gpt` i rom 22 og 28 og introen):

- Klassisk dump i rom 22 og 28: alle 4 x 4 blokker er ensfargede, og bildet skalert ned er likt originalgrafikken i `work/extract` bortsett fra fargesyklet vann (rom 22) og teksten "exit" (rom 28).
- Gult felt: rom uten HD-bakgrunn blir gult, HD-bakgrunnen i rom 22 og HD-objektet i rom 28 blir ikke gule, heller ikke vannet i rom 22 eller teksten i rom 28. I introen med en mod uten kostymer blir astronautene gule, mens bakgrunnen og underteksten ikke blir det.
- Film med HD-rammer: HD-rammene brukes i HD-modus, ikke i klassisk modus, og blir ikke gule.
- Tastene: `DIGHD_TEST_KEYS` trykket Ctrl+H og Ctrl+Shift+H mens spillet gikk, og byttet virket begge veier. Ikke testet med ekte tastatur og skjerm, og meldingen på skjermen er ikke sett.
- `engine/test.sh` gir fortsatt 0 avvik for bakgrunner og uskalerte figurer.

## Kjente begrensninger

- Undertekster over filmer som er byttet ut med HD-rammer, blir borte, fordi teksten er tegnet inn i originalrammen. Må løses før filmer med tekst byttes ut.
- Kostymer med kodek 16 (5 kostymer) får ikke HD-sprites ennå. Kodek 1 (182 kostymer, blant dem hovedpersonene) er testet i spillet. Kodek 5 (144 kostymer) er koblet inn, men ikke kontrollert for seg.
- Objekter som tegnes direkte i bakgrunnsbufferen av skript (sjeldent) blir originalpiksler.
- Tegnsett og tekst er originalpiksler. HD-fonter er en senere jobb.
- Gult felt: tekst som ligger oppå en figur uten HD, blir gul, fordi motoren bare vet hvilket rektangel figuren dekker. Det samme gjelder tekst der en figur uten HD sist ble tegnet, til figuren tegnes på nytt eller rommet byttes.
- Dumpene (`DIGHD_DUMP_DIR`) viser filmrammer som originalbilde også når en HD-ramme vises på skjermen.
