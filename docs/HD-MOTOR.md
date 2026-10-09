# HD-motoren: slik virker den

HD-motoren er ScummVM med én patch (`engine/patches/0001-dighd-hd-grafikk.patch`). Spillet kjører som før i 320 x 200 med 256 farger. All logikk, alle skript, lagring, lyd og filmer er ScummVM sine. Det eneste som endres, er det aller siste steget, der bildet sendes til skjermen.

## Prinsippet

Hver gang motoren er ferdig med et område av skjermen, bygger patchen det samme området i 4x (eller annen skala) og full farge. For hver piksel avgjøres det hvor HD-pikselen skal hentes fra:

| Hva pikselen viser | Hvordan det avgjøres | Hvor HD-pikselen kommer fra |
| --- | --- | --- |
| Uendret rombakgrunn | Pikselen er lik i forgrunns- og bakgrunnsbufferen, og lik originalbildet `roomNNN_idx.png` | `rooms/roomNNN.png` |
| Objekt (dør, maskin, lys) | Lik i begge buffere, men lik et objektbilde motoren nettopp har tegnet | `objects/objNNN_SS.png` |
| Figur (kostymerute) | Forskjellig fra bakgrunnsbufferen, tegnet av ruten sist den ble tegnet, og har fortsatt verdien ruten skrev (se Hvilke piksler som viser en figur) | `costumes/costumeCCC_NNN.png` |
| Filmramme | Filmen og rammenummeret er kjent, og pikselen er ikke tekst | `san/FILM/NNNNN.png` |
| Tekst (dialog, bannere, menyer, undertekster i spill og film) | Tegneren meldte glyfen rett før den ble tegnet, og pikselen har fortsatt verdien glyfen skrev | HD-glyf laget av spillets egen font, lagt over HD-pikselen for det som er under teksten (se Tekst i HD) |
| Tekst uten kjent glyf | SmushPlayer tegner filmteksten en gang til i et eget lag | Originalpikselen skalert opp |
| Alt annet (effekter, ting uten HD-bilde) | | Originalpikselen skalert opp |

Fordi alt som ikke kan avgjøres sikkert faller tilbake til originalpikselen, kan HD-grafikken legges inn litt etter litt. Spillet virker hele veien.

## Farger

- **Palettbytte og toning:** Når fargen motoren viser er forskjellig fra fargen HD-bildet ble laget med, justeres HD-pikselen med forholdet mellom dem. Fade til svart og lysbytter følger derfor med. Bare pikslene som får en annen farge, bygges på nytt (se Fargesykling under).
- **Fargesykling:** Farger som sykles (vann, energi, lys) skifter hele tiden. HD-bakgrunnen og HD-objektene vises også der, og følger syklingen. Se eget avsnitt under.
- **Figurer:** Kostymer med kodek 1 har sine "ekte" farger i RGBS-blokken. Motoren tilpasser dem til rompaletten og lyset. Kostymer med kodek 5 og 16 tegnes med kodene rett som palettindekser, så der er fargene rommets palett (se Kostymer med kodek 5 og 16). Uttrekket farger rutene slik spillet viser dem, og HD-sprites bruker de fargene. De justeres bare når fargen spillet viser er tydelig mørkere eller lysere. Skygger og spesialeffekter blir originalpiksler. Det samme gjelder en piksel som er svart i HD-fargen, men vises lys i spillet, for da er det ikke denne fargen som vises.
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

## Hvilke piksler som viser en figur

Motoren tegner figurene rute for rute (kostymeruter) i spillskjermen. Rett etter at en rute er tegnet, merker DigHD hver piksel i ruten der indeksbildet til ruten har farge: hvilken tegning av ruten pikselen kom fra, og hvilken verdi ruten etterlot der. Merkene ligger per piksel i bufferen, som merkene for teksten. En piksel viser HD-figuren bare når

- den er forskjellig fra bakgrunnsbufferen,
- merket hører til den siste tegningen av ruten (tegnes skuespilleren på nytt eller byttes rommet, gjelder ikke de gamle merkene lenger),
- den fortsatt har verdien ruten skrev. Under en tekst med HD-glyf gjelder verdien under glyfen, så figuren ligger under teksten.

Merkene tas bort der noe annet tegnes over figuren:

- Alt som går gjennom `markRectAsDirty` i spillskjermen: bokser og linjer (bannere, hovedmenyen, `drawBox` fra skriptene) og bakgrunn som legges tilbake. Da får heller ikke en piksel i boksen som tilfeldigvis har samme verdi som figuren, HD-figuren. Der bakgrunnen legges tilbake, tegner motoren skuespillerne der på nytt, og de merkes igjen.
- Glyfer uten HD-versjon (for eksempel med `DIGHD_TEXT=off`), i pikslene glyfen tegner.

Unntak: når en skuespiller merker rektangelet den skal tegne, beholder de andre figurene i rektangelet merkene sine. Blast-objekter har gjennomsiktige piksler, så figurene under dem beholder merkene. Der objektet tegnet, skiller verdien det fra figuren. Tekst merker sitt eget område uten å ta bort noe, fordi figuren ligger under glyfene.

Bannere: motoren lagrer pikslene under et banner og legger dem tilbake når banneret går (`showBannerAndPause`, `clearBanner`), og merker da hele skjermen. DigHD lagrer merkene samtidig og legger dem tilbake etter merkingen, så figurene er HD med en gang banneret er borte. Hovedmenyen tegner hele skjermen på nytt når den lukkes.

Figurer uten HD-bilde har ikke noe indeksbilde som viser hvilke piksler ruten tegnet. For dem merkes pikslene i rektangelet som er forskjellig fra bakgrunnen og ikke viser en HD-figur tegnet før. Det er disse pikslene som blir gule med gult felt.

Valg og begrunnelse. Før kjente figurkilden bare rektangelet til hver rute og om indeksbildet hadde farge der. Alt som ble tegnet innenfor rektangelet etter figuren (banner, meny, tekst), ble tatt for figuren. Der fargene ikke var altfor ulike, ble HD-pikselen brukt, så figuren skinte svakt gjennom boksen. Med gult felt ble tekst og bokser over en figur uten HD gule. Rektangelet sto også igjen etter at figuren var borte, til skuespilleren ble tegnet på nytt eller rommet byttet. To veier ble vurdert:

| Vei | Vurdering |
| --- | --- |
| Nullstille figurene når bannere og menyer tegnes | Retter bannere og menyer, men ikke tekst over figurer, gamle rektangler eller bokser fra skriptene |
| Merke per piksel med verdien ruten skrev (valgt) | Følger det som faktisk står i bufferen, uansett hva som har tegnet over. Verdien alene skiller ikke en boks med samme farge som figuren, derfor tar `markRectAsDirty` også bort merkene |

Merkingen koster lite: 0,006 ms per bilde i rom 2 (3 ruter). Oppslaget er en sammenligning per piksel i stedet for en løkke over alle rutene, og tidene for hele skjermen er de samme som før innenfor målestøyen. Se Hva som er testet.

## Kostymer med kodek 5 og 16

Kodeken står i AKHD-blokken i hvert kostyme. Av de 331 kostymene har 182 kodek 1 (Byle RLE), 144 kodek 5 (BOMP) og 5 kodek 16 (MajMin). Alle tre får HD-sprites på samme måte: tegneren melder hver rute til DigHD (`noteCel`) etter at den er tegnet, med rektangelet før klipping og om den er speilvendt.

### Kostymene med kodek 16

| Kostyme | Ligger i rom | Hva det er | Hvor det er sett |
| --- | --- | --- | --- |
| 95 | 30 (connect) | Lyn fra skyene ned i havet, 180 ruter | Rom 30, til høyre i rommet. Synes når kameraet står til høyre |
| 96 | 31 (mudoor) | Et lysende spøkelse i blågrønt og oransje, 68 ruter | Bare med testkroken. Fargene er bare riktige med rommets palett 1 |
| 118 | 33 (skeleton) | Boston Low som svømmer under vann, med bobler og vannflaten, 181 ruter | Bare med testkroken |
| 266 | 92 (library) | Små mørke detaljer i biblioteket: tynne streker og små former, 247 ruter | Rom 92 med en gang (skuespiller 13), og rom 79 i en mellomsekvens |
| 267 | 92 (library) | Bildene i krystallskapene i biblioteket: lysende kuler, pyramider og krystaller, 264 ruter | I mellomsekvensen som starter når spillet hopper til rom 95, og med testkroken |

Er det verdt det? Low som svømmer (118) er hovedpersonen i en hel scene, og bildene i biblioteket (267) dekker opptil 10 000 originalpiksler. Lynet, spøkelset og 266 er små effekter. Koblingen i motoren er en melding i `paintCelMajMin`, så alle fem er tatt med.

### Når ScummVM bruker AKPL

En kode i en rute blir en palettindeks på en av to måter: gjennom AKPL og skuespillerpaletten, eller rett, slik at koden er palettindeksen. Fra `akos.cpp` (`AkosRenderer::setPalette`, `paintCelByleRLE`, `paintCelCDATRLE`, `paintCelMajMin`) og `actor.cpp`:

| Kodek | Hvordan koden blir en palettindeks |
| --- | --- |
| 1 | Alltid gjennom `_palette`: plassen i skuespillerpaletten når den er satt, ellers AKPL |
| 5 | Har AKPL 256 plasser og plass 0 i skuespillerpaletten er satt, går kodene gjennom `_palette` som for kodek 1 (`_useBompPalette`). Ellers tegnes de rett. `_useBompPalette` settes tilbake etter hver rute, så i en tegning med flere ruter får bare den første paletten |
| 16 | Alltid rett. `paintCelMajMin` bruker ikke paletten i The Dig (bare HE-spill fra versjon 61) |

Skuespillerpaletten tømmes (0xFF på alle plasser) når skuespilleren får et nytt kostyme (`setActorCostume`). Skriptet kan fylle den med `remapActorPalette` (kernelSetFunctions 13 og 14: RGBS ganget med en faktor og tilpasset rompaletten) eller én plass om gangen med actorOps.

Målt i spillet: med `DIGHD_VERIFY=1` skriver motoren en linje første gang et kostyme tegnes i et rom med en palett, for eksempel `costume 210 in room 78 with palette 0: codes as palette indices`. Spillet hoppet til hvert av de 111 rommene og gikk 860 bilder etter hoppet. 45 kostymer med kodek 1 og 34 med kodek 5 og 16 ble tegnet, og kostyme 95 i en egen kjøring med kameraet til høyre. Alle med kodek 5 og 16 ble tegnet rett, alle med kodek 1 gjennom AKPL. Ingen skript satte skuespillerpaletten på et kostyme med kodek 5 i disse kjøringene. Hoppet til rom 55 ble ikke gjort (spillet var i en film).

Hva det betyr for fargene: RGBS-blokken har fargen til hver AKPL-plass. For 105 av de 144 kostymene med kodek 5 er RGBS nesten nøyaktig fargen AKPL-plassen har i en av palettene i rommet kostymet ligger i (under 25 i hver kanal for alle kodene rutene bruker). Når kodene tegnes rett, viser spillet i stedet rompalettens farge for selve koden, og den er ofte en helt annen (i kostyme 210 for halvparten av pikslene). Øyet i rom 78 (kostyme 210) er glatt grått i spillet, men flekkete brunt og blått med RGBS-fargene.

### Uttrekket

`dighd extract` farger nå hver rute med fargene spillet viser:

- Kodek 1: RGBS som før. Filene er byte for byte like.
- Kodek 5 og 16: kodene rett i paletten til rommet der kostymet vises. Rommet og paletten står i `docs/kostymefarger.csv` når de er målt i spillet (35 kostymer). Ellers brukes rommet kostymet ligger i. Har rommet flere paletter, velges den som gir det jevneste bildet: snittet av største fargeforskjell mellom nabopiksler i alle rutene. Er flere nesten like jevne (under 2 prosent fra den beste), brukes den første av dem, helst palett 0, som rommet starter med. 57 kostymer ligger i rom med én palett, og for 57 er paletten valgt slik.
- Står det `rgbs` i tabellen, brukes RGBS som for kodek 1. Det er for kostymer skriptet setter skuespillerpaletten på. Ingen er funnet ennå.

Indeksbildet (`_idx.png`) har de samme fargene som palett, så motoren sammenligner med fargene uttrekket brukte. `costumes.json` har nå kodeken og hvordan fargene er valgt (`codec`, `colours`).

Jevnhet er brukt fordi det skiller tydelig: med den valgte paletten er 133 av de 146 kostymene som har RGBS, minst 20 prosent jevnere enn med RGBS, 13 er omtrent like, og ingen er jevnere med RGBS. Av de målte kostymene i rom med flere paletter valgte jevnheten den samme paletten som spillet for 229 (rom 82, palett 1) og 240 (rom 91, palett 0), men ikke for 225 (rom 79, palett 2 i spillet). Der er palettene nesten like for kodene kostymet bruker, og tabellen avgjør.

### Motoren

- `paintCelMajMin` melder rutene til DigHD som de andre tegnerne.
- Tegnerne sier om kodene ble tegnet rett (kodek 16 alltid, kodek 5 uten `_useBompPalette`). For slike ruter skal pikselen ha verdien koden har. Har den en annen verdi, har en skyggetabell endret den (skyggemodus 3 endrer kodene under 8 etter det som ligger under, som i kostyme 74 i rom 25), og pikselen blir originalpiksel. Før ble dette avgjort bare av hvor ulike fargene var.
- Fargene ellers som for kodek 1: HD-pikselen brukes som den er når fargen spillet viser er nær fargen i uttrekket, ellers justeres den med forholdet, og helt ulike farger blir originalpiksler. Vises kostymet med en annen palett enn uttrekket brukte, blir det dermed som for bakgrunner ved palettbytte.

Valg og begrunnelse:

| Vei | Vurdering |
| --- | --- |
| Motoren justerer HD-pikselen mot fargen spillet viser (forhold per kanal, slik det var) | HD-bildet lages fra uttrekket. Med RGBS-farger har det andre farger og former enn spillet viser, og forholdet per kode kan ikke rette det: en svart kanal kan ikke skaleres, og der en oppskalert piksel blander to koder, blandes feil farger. Målt med nearest-mod i 17 rom: 12 til 100 prosent av figurpikslene fikk HD (i 15 av rommene 56 til 99), og opptil 56 prosent av dem måtte tones (i rom 89 alle) |
| Uttrekket bruker rompaletten der kostymet vises (valgt) | HD-bildet lages fra de samme fargene som spillet viser, og motoren bruker HD-pikselen som den er. I de samme rommene: 96 til 100 prosent HD og ingen toning (se Hva som er testet). Fargene avhenger av rommets palett, så rommet og paletten må være kjent: målt (tabellen) eller valgt etter jevnhet |
| Ett HD-bilde per rom og palett | Bare nyttig for kostymer som vises med flere paletter. Bare 266 er sett slik, i en kort mellomsekvens. Ikke gjort |

## Klassisk grafikk og gult felt

**I spillets egen meny.** F5 åpner menyen til The Dig (ScummVM sin originalmeny, `original_gui`, som er standard). Når en HD-mod er lastet, har menyen en rad til nederst i venstre del, under Text Speed: **HD Graphics** med en avkrysningsboks. Krysset betyr HD, tom boks betyr originalgrafikken. Et klikk bytter med en gang, og hele skjermen bygges på nytt, så rommet rundt menyen viser valget mens menyen er oppe. Boksen og teksten er tegnet som resten av menyen. Menyen er 14 piksler høyere med denne raden (også sidene for lagring og lasting, så rammen står likt). Uten HD-mod er menyen som før.

Valget lagres i scummvm.ini som `dighd_classic` i `[scummvm]` og gjelder neste gang spillet startes, også i nettleseren (der ligger scummvm.ini i nettleserens lagring). Det ligger i `[scummvm]` fordi et spill som startes fra kommandolinjen uten et lagret mål, ikke har en egen seksjon som skrives til fil. `DIGHD_CLASSIC` går foran.

To hurtigtaster virker også mens spillet går, så lenge en HD-mod er lastet:

| Tast | Virkning |
| --- | --- |
| Ctrl+H | Bytter mellom HD-grafikk og klassisk grafikk |
| Ctrl+Shift+H | Slår gult felt der HD mangler av og på |

ScummVM viser en kort melding på skjermen når du bytter med tastene ("Dig HD: klassisk grafikk" og så videre). Ctrl+H lagrer valget på samme måte som menyen. Tastene går ikke videre til spillet.

**Klassisk grafikk** er originalpikslene skalert opp med nearest over hele skjermen, også filmer som har HD-rammer. Skjermen er like stor som før, så vinduet og musen endres ikke. Pekeren er den samme i begge modusene. Motoren fortsetter å finne ut hvor HD-pikslene skal hentes fra også i klassisk modus, så byttet tilbake til HD skjer med en gang.

**Gult felt** blander halvparten gult inn i hver piksel som vises som originalpiksel fordi HD mangler:

- rombakgrunn i rom uten HD-bakgrunn, også fargesyklede piksler (før var de unntatt, fordi syklede piksler alltid var originalpiksler)
- bakgrunnspiksler som ikke stemmer med HD-bakgrunnen og ikke med noe HD-objekt (objekter uten HD-bilde)
- figurer der kostymeruten ikke har HD-bilde
- filmrammer uten HD-ramme (hele bildet unntatt teksten som SmushPlayer tegner over filmen)

Dette farges ikke gult, fordi det er originalt med vilje eller har HD:

- fargesyklede områder i HD-bakgrunnen og HD-objekter (de vises med HD, se Fargesykling)
- syklede farger på figurer (lys og effekter)
- tekst med HD-glyf, også over figurer og filmrammer uten HD. Glyfen legges over det gule, så bare de myke kantene blander seg med det gule under
- tekst uten HD-glyf over spillet, også oppå figurer uten HD
- undertekster og annen tekst over filmer, også over filmrammer uten HD-ramme
- skygger og effekter på figurer med HD-bilde
- bannere (pause, volum) og hovedmenyen, også over figurer uten HD, overgangseffekter og musepekeren

I klassisk modus farges ingenting gult. Når gult felt slås på mens spillet går, bygges skjermen på nytt med en gang, og alt som mangler HD, også figurene, blir gult.

Valg av taster: SCUMM-motoren bruker Ctrl med tallene, F, G, T, V, K og C (og B, D, J, N og R i andre SCUMM-spill). ScummVM bruker Ctrl+M, Ctrl+R, Ctrl+U, Ctrl+Q, Ctrl+Z, Ctrl+F5, Ctrl+F7, Alt+S, Alt+Enter og Ctrl+Alt med flere taster for grafikkvalg. Sjekket i `engines/scumm/input.cpp`, `engines/scumm/metaengine.cpp`, `engines/metaengine.cpp`, `backends/events/default/default-events.cpp` og `backends/graphics/sdl/sdl-graphics.cpp`. H brukes ikke med Ctrl eller Ctrl+Shift i noen av disse, og ingen av tastaturoppsettene som er aktive i The Dig har H alene, så ScummVM sender tasten videre til motoren. Y og J ble valgt bort fordi bekreftelsesdialogene i ScummVM svarer ja på Y, og på J med norsk språk. Begge funksjonene ligger på samme bokstav, så de er lette å huske.

Ytelse: når begge er av, er bildebyggingen like rask som før. Målt uten skjerm med 300 hele skjermbilder i rom 22 og 28 (beste tid): 8,0 til 8,9 ms per bilde både før og etter endringen, og 0,3 til 0,5 ms for å finne kildene til et helt bilde. Med gult felt på ble tidene de samme i disse rommene. Figurer uten HD finnes nå med de samme merkene som figurer med HD (se Hvilke piksler som viser en figur), så det er ingen egen runde for dem lenger. Klassisk modus er raskere, under 1 ms per bilde. Tider etter fargesyklingen står under Hva som er testet.

## Undertekster over filmer

SmushPlayer tegner undertekster og annen filmtekst rett inn i filmrammen (8 bit), etter at rammen er pakket ut. En HD-ramme dekker hele bildet, så teksten må legges oppå HD-rammen igjen. Slik gjøres det:

1. Før teksten tegnes, lager DigHD et lag med hele filmrammen der hver byte er invertert (XOR 0xFF).
2. SmushPlayer tegner den samme teksten to ganger: først i laget, så i filmrammen som før.
3. Etterpå er laget og filmrammen like nøyaktig i de pikslene teksten skrev. Alle andre piksler er ulike, fordi en invertert byte aldri er lik seg selv. Pikslene som er like, merkes som tekst.
4. Når rammen vises, får tekstpikslene HD-glyfen over HD-rammen (se Tekst i HD). Tekstpiksler uten kjent glyf er originalpiksler skalert opp med nearest. Resten kommer fra HD-rammen. Teksten ligger derfor på nøyaktig samme sted som i originalen.
5. Merkene nullstilles når en ny ramme pakkes ut og når en ny film starter. Viser filmen samme bilde videre uten å pakke ut noe nytt, står teksten i rammen fortsatt, og da beholdes merkene også.

Hvorfor denne løsningen: teksttegneren i ScummVM skriver bare piksler og leser aldri det som ligger under, så to tegninger gir samme resultat. Det enkleste alternativet, å ta vare på rammen før teksten og se hvilke piksler som endret seg, mister tekstpiksler som har samme farge som filmen under (svart kant på svart bakgrunn). Der ville HD-pikselen blitt vist i stedet. Med laget blir det nøyaktig, uten å endre teksttegneren. Det koster én ekstra tekstutskrift og to gjennomganger av rammen (64 000 byte) per tekst.

Med undertekster slått av (ScummVM-innstillingen `subtitles`) tegner SmushPlayer ikke underteksten, og hele rammen er HD. Tekst uten bryterflagget, som "Borneo Deep Space Observatory" i introen, vises alltid, som i originalen.

Klassisk grafikk viser hele filmen som originalpiksler. Med gult felt blir filmrammer uten HD-ramme gule, men ikke teksten.

Filmrammene bygges på samme måte som resten av skjermen, med en kilde per piksel. Dumpene (`DIGHD_DUMP_DIR`) og `DIGHD_VERIFY` viser derfor det som faktisk er på skjermen, også HD-rammen og teksten. Ytelse uten skjerm, snitt over 400 rammer av introen: lesing av HD-rammen (PNG i 1280 x 800) tar omtrent 23 ms per ramme, og resten (kilder, bygging av bildet og kopi til skjermen) omtrent 2 ms.

## Tekst i HD

All tekst vises med HD-glyfer: dialog og undertekster i spillet, bannere (pause, volum), hovedmenyen og undertekster og annen tekst i filmene. Glyfene lages av spillets egne fontbilder, så formen er fontens egen, og de tegnes på nøyaktig samme sted og med samme farger som originalen.

### Fontene

The Dig har to slags fonter, tegnet av to forskjellige tegnere i ScummVM:

| Hvor | Font | Tegnes av | Farger |
| --- | --- | --- | --- |
| I spillet (dialog, undertekster, bannere, meny) | 4 tegnsett (CHAR i `DIG.LA1`) | `CharsetRendererV7::drawCharV7` | Verdi 1 er tekstfargen, de andre verdiene får farge fra tegnsettets fargetabell (`_charsetColorMap`, kan settes av skript) |
| I filmene | `FONT0.NUT` til `FONT3.NUT` i `VIDEO` | `SmushFont`, som bruker `NutRenderer::drawCharV7` | Font 0 (undertekster): verdi 1 er tekstfargen, 255 blir svart. Font 1 til 3 har palettindeksene i fonten |

Av de fire tegnsettene har ett 1 bit per piksel og tynne streker, ett tekstfarge med 1 piksel svart kant rundt (samme form som NUT-font 0), ett tre nivåer og ett tekstfarge med skygge. Bannere og menyer bruker et av de tynne. Ingen glyf er større enn 39 x 16 piksler eller har mer enn 3 farger. CJK-tegn (`draw2byte`) brukes ikke i den engelske utgaven og er ikke med.

### Slik virker det

1. Rett før en glyf tegnes, melder tegneren den til DigHD (`noteGlyph`): bufferen den tegnes i, posisjonen, glyfbildet, hvilken palettindeks hver verdi blir, og hvilken del som tegnes (klipping som i tegneloopen).
2. DigHD finner formen (hvilke piksler som har hvilket nivå) og lager HD-glyfen første gang formen sees. Samme form i en annen farge bruker samme HD-glyf. Fargen legges på når bildet bygges, så teksten følger paletten (fade).
3. For hver bufferpiksel glyfen dekker, husker DigHD glyfen, verdien glyfen skrev og verdien som lå der før, altså det som er under teksten. Det gjøres for spillskjermen (hovedbufferen) og for filmrammen mellom `smushTextBegin` og `smushTextEnd`. Laget for tekstmasken i filmene (se Undertekster over filmer) telles ikke.
4. Rett før teksten vises, ser hver nye glyf på de to pikslene rundt seg. Der en annen glyf berører den med en av dens egne farger (svarte kanter på bokstaver ved siden av hverandre, linjer satt sammen av flere tegn som skyveknappene i menyen), lages HD-glyfen med de pikslene på plass. Da går formene i ett, uten avrundede ender der tegnene møtes. Også disse variantene lages en gang og huskes.
5. Når bufferen sendes til skjermen, viser en piksel tekst bare hvis den har en glyf og fortsatt har verdien glyfen skrev. Da letes HD-kilden opp for verdien under teksten (bakgrunn, objekt, figur eller filmramme) som for alle andre piksler, og HD-glyfen legges oppå. En piksel glyfen lot være (gjennomsiktig) får den delen av HD-glyfen som når inn i den (avrundede indre hjørner), men bare så lenge alle pikslene rundt den som glyfen tegnet, fortsatt står.

Teksten fjernes riktig fordi glyfene nullstilles når teksten går bort, og fordi verdien må stemme:

- Teksten i spillet (blast-tekster) fjernes og tegnes på nytt hvert bilde. `removeBlastTexts` nullstiller alle glyfene i spillskjermen først.
- Alt annet som tegnes i spillskjermen, går gjennom `markRectAsDirty`: gjenopprettet bakgrunn, figurer, menybokser og banner som tas bort. Det nullstiller glyfene i det området. Teksttegningen merker sin egen tekst rett etter at den er tegnet; det nullstiller ingenting.
- I filmene nullstilles glyfene når en ny ramme pakkes ut og når filmen starter. Et nytt filmbilde nullstiller også tekst som ble tegnet i spillskjermen (bannere over filmen).
- En piksel som er tegnet over av noe annet, har ikke lenger verdien glyfen skrev, og viser aldri glyfen.

Klassisk grafikk (Ctrl+H) viser originalpikslene som før. Med gult felt (Ctrl+Shift+H) blir tekst med HD-glyf aldri gul. Glyfen legges over, så bare de myke kantene blander seg med det gule under, der det som er under teksten mangler HD.

### Valg av skalerer

Skalererne ble først prøvd i Python på alle 8 fontene, så i spillet og i introfilmen. HD-glyfene lages i 4x. Med en annen skala (`DIGHD_SCALE`) regnes de i 4x og skaleres til skjermen med område-snitt.

| Metode | Resultat |
| --- | --- |
| Nearest | Som originalen, grove 4 x 4-blokker. Brukes til test (`DIGHD_TEXT=nearest`): da skal HD-teksten være lik originalen |
| Scale4x (Scale2x to ganger, EPX) | Rette 45-graders kanter og harde kanter uten mellomtoner. Små trappetrinn i rundingene (o, b, g, R) |
| xBR 4x (valgt) | Jevne rundinger og skrå kanter med myke kanter, og formen er fontens egen. Hver farge skaleres som maske for seg. Nivået som ligger mest langs utsiden (den svarte kanten), får det som er igjen av hele glyfen, så kant og tekstfarge passer sammen |
| Hver glyf for seg, uten nabotegn | Avrundede ender der tegnene møtes: hakk i den svarte kanten mellom bokstavene og stiplede skyveknapper i menyen og volumbanneret. Derfor steg 4 over |

Innstillingen `DIGHD_TEXT` (eller `dighd_text` i scummvm.ini) velger skalerer: `xbr` (standard), `scale4x`, `nearest` eller `off` (tekst som originalpiksler, som før).

## Stedene i ScummVM som er endret

| Fil | Endring |
| --- | --- |
| `engines/scumm/dighd.cpp`, `dighd.h` | All HD-logikk (ny fil) |
| `scumm.cpp` | Lager DigHD, setter opp HD-skjermen, motoren holder seg i 8 bit, hook før hver skjermoppdatering |
| `gfx.cpp` | Siste blit (`drawStripToScreen`), overgangseffekter, `moveScreen`, risting av skjermen. `markRectAsDirty` nullstiller glyfene og figurmerkene i området (figurmerkene ikke når en skuespiller merker sitt eget rektangel) |
| `gfx_gui.cpp` | DigHD får beskjed når skjermen lagres før et banner og legges tilbake etterpå (`showBannerAndPause`, `clearBanner`). Raden HD Graphics i hovedmenyen til The Dig (`setUpMainMenuControls`, `updateMainMenuControls`, `executeMainMenuOperation`, `drawMainMenuTitle`) |
| `charset.cpp` | Melder hver glyf fra tegnsettene i spillet (`CharsetRendererV7::drawCharV7`) |
| `nut_renderer.cpp` | Melder hver glyf fra NUT-fontene i filmene (`NutRenderer::drawCharV7`) |
| `string_v7.cpp` | Teksten som tegnes og merkes, nullstiller ikke seg selv. `removeBlastTexts` nullstiller glyfene i spillskjermen |
| `palette.cpp` | Palett sendes til DigHD i stedet for til skjermen |
| `object.cpp` | Melder hvilke objekter som tegnes og i hvilken tilstand. Blast-objekter beholder figurmerkene under seg |
| `akos.cpp`, `akos.h`, `base-costume.cpp` | Melder hvilke kostymeruter som tegnes (kodek 1, 5 og 16), hvor, om de er speilvendt, om kodene er tegnet rett som palettindekser, og om de tegnes i skjermbufferen eller i bakgrunnsbufferen |
| `cursor.cpp`, `input.cpp`, `saveload.cpp` | Musepeker i HD, museposisjon delt på skala, hurtigtastene Ctrl+H og Ctrl+Shift+H |
| `smush/smush_player.cpp` | Filmrammer og filmpalett via DigHD. Filmteksten tegnes også i laget til DigHD, og DigHD får beskjed når en ny ramme er pakket ut |

## Innstillinger

| Variabel / nøkkel i scummvm.ini | Betydning |
| --- | --- |
| `DIGHD_MOD` / `dighd_mod` | Mappen med HD-grafikk. Uten denne kjører spillet helt som vanlig |
| `DIGHD_SCALE` / `dighd_scale` | Skala, standard 4 |
| `DIGHD_CLASSIC=1` / `dighd_classic=true` | Starter i klassisk grafikk. HD Graphics i menyen og Ctrl+H bytter og skriver `dighd_classic` i `[scummvm]` |
| `DIGHD_SHOW_MISSING=1` / `dighd_show_missing=true` | Starter med gult felt der HD mangler (Ctrl+Shift+H slår av og på) |
| `DIGHD_TEXT` / `dighd_text` | Skalerer for teksten: `xbr` (standard), `scale4x`, `nearest` eller `off` (tekst som originalpiksler) |

Miljøvariabelen går foran nøkkelen i scummvm.ini. `DIGHD_CLASSIC=0` gir HD selv om `dighd_classic=true` står i filen.

Test og feilsøking (bare miljøvariabler):

| Variabel | Betydning |
| --- | --- |
| `DIGHD_VERIFY=1` | Ved hver dump: sammenligner HD-bildet med originalen og skriver avviket i loggen (gult felt er ikke med), og sjekker at skjermen er lik hele skjermen bygget på nytt |
| `DIGHD_DUMP_DIR`, `DIGHD_DUMP_EVERY` | Lagrer skjermbildet som PNG hver N-te bilde: `frame_NNNNNN_roomRRR.png`, eller `frame_NNNNNN_FILM_RRRRR.png` under en film (RRRRR er rammenummeret, som i `san/FILM/`) |
| `DIGHD_DUMP_FLAT=1` | Lagrer også originalpikslene for det samme bildet ved siden av hver dump (`..._flat.png`, som klassisk grafikk), til sammenligninger |
| `DIGHD_BENCH=N` | Ved hver dump: bygger hele skjermen N ganger og skriver snittid per gang, og i rom med fargesykling tiden for ett steg i syklingen (alle syklede farger endret). Utenom film også tiden for spillskjermen sendt gjennom motoren med oppslag av kilden for hver piksel (`sources and whole screen`) og tiden for å merke pikslene til rutene som ble tegnet sist (`marking`, snitt over 10 x N ganger) |
| `DIGHD_SKIP_VIDEO=1` | Hopper over filmer |
| `DIGHD_TEST_ROOM`, `DIGHD_TEST_AT`, `DIGHD_TEST_CAMX`, `DIGHD_TEST_CAMY` | Hopper rett til et rom etter N bilder. Et rom som er mindre enn skjermen (rom 93 med ikonene i inventaret, 40 x 200), hoppes ikke til: spillet viser det aldri, og ScummVM stopper med en assert når kameraet skal plasseres. Med `CAMX` eller `CAMY` settes kameraet dit (midten av skjermen i rommet), og det følger ikke lenger en skuespiller. Flytter et skript kameraet, settes det tilbake etter neste bilde. Et skript som setter kameraet hver gang spillet går et steg (rom 27), vinner likevel |
| `DIGHD_QUIT_AT` | Avslutter etter N bilder |
| `DIGHD_TEST_KEYS` | Trykker taster ved gitte bilder, for eksempel `420:ctrl+h,570:ctrl+shift+h,600:f5`. Tastene a til z, f1 til f12, `space` og `escape`, med `ctrl+`, `shift+` og `alt+`. Tastene går gjennom den vanlige tastehåndteringen i motoren |
| `DIGHD_TEST_CLICKS` | Klikker med venstre museknapp ved gitte bilder, for eksempel `450:114/152,550:265/107` (x/y i originalpiksler). Knappen går ned ved bildet og opp 3 bilder senere. For menyene uten mus |
| `DIGHD_TEST_COSTUME` | Testkroken: 30 bilder etter hoppet med `DIGHD_TEST_ROOM` settes en skuespiller inn i rommet med dette kostymet, og den spiller alle animasjonene i AKCH (alle retninger) etter hverandre. For kostymer skriptene først viser senere i historien |
| `DIGHD_TEST_ACTOR`, `DIGHD_TEST_POS`, `DIGHD_TEST_PALETTE`, `DIGHD_TEST_CHORE_EVERY` | Skuespilleren testkroken bruker (standard 29), plassen i rommet (`x,y`, standard midt på skjermen og 180), rompaletten som settes (`setCurrentPalette`, standard ingen) og hvor mange bilder hver animasjon vises (standard 60) |
| `DIGHD_TEST_OBJSTATE` | Testkroken for objekttilstander. `884:2,886:1` setter objektene i disse tilstandene etter hoppet og holder dem der. `alle` viser hver tilstand av hvert objekt i rommet etter hverandre og lagrer skjermen etter hver tilstand. Se Objekttilstander i testen |
| `DIGHD_TEST_OBJSTATE_AT`, `DIGHD_TEST_OBJSTATE_EVERY` | Bilder etter at spillet er i testrommet før den første tilstanden settes (standard 30), og hvor mange bilder hver tilstand vises med `alle` (standard 40) |

Loggen teller pikslene per kilde: `HD room px`, `HD object px`, `HD sprite px` og `original px`, og `HD film px` når en HD-filmramme er vist. `cycled HD px` er pikslene som gikk gjennom fargekartet for fargesykling (de er også med i `HD room px` eller `HD object px`). `HD text px` er pikslene som fikk en HD-glyf over seg (de er også med i tallet for det som er under teksten). `tinted sprite px` er figurpikslene som ble justert med forholdet mellom fargene (de er også med i `HD sprite px`), og `figure px kept original` figurpikslene med HD-bilde som ble originalpiksler med vilje: skygger, effekter, syklede farger og farger som er helt forskjellige (de er også med i `original px`). Med gult felt på kommer `yellow px` i tillegg (de gule er også med i `original px`), og i klassisk modus står det `classic` til slutt. Tallene er originalpiksler, summert over alt som er bygget siden forrige dump.

Utenom film skriver hver dump også en linje for bildet i dumpen alene, hele skjermen i originalpiksler (64 000 i alt): `whole screen frame 840 (room 27, screen at 91,490): HD room px 42358, HD object px 0, HD sprite px 0, original px 21642 (background without HD 0, figure without HD 21642), HD text px 0, cycled HD px 7697`. `screen at` er stedet i rommet som vises øverst til venstre på skjermen (`xstart` og `_screenTop`, satt da kameraet sist ble flyttet før skjermen ble tegnet). Originalpikslene uten HD er delt i bakgrunn (rom uten HD-bakgrunn, eller objekter uten HD-bilde: pikselen er lik bakgrunnsbufferen) og det som er tegnet over (figurer uten HD-bilde). Resten av originalpikslene er originale med vilje (skygger, effekter, syklede farger på figurer). `tools/romtest.sh` bruker denne linjen.

Med `DIGHD_VERIFY=1` skriver hver dump to til fire linjer:

- `N screen pixels differ from the whole screen built again`: skjermen bygges bit for bit (skitne områder, palettendringer). Er tallet over 0, har en del av skjermen ikke blitt bygget på nytt når den skulle.
- `N of M HD pixels differ strongly from the original`: avvik mot originalen, for pikslene utenfor fargesyklingen og utenfor HD-teksten.
- `colour cycling, N of M HD pixels differ strongly`: avvik i pikslene som gikk gjennom fargekartet. De er jevnet ut mellom originalpikslene med vilje, så med en `nearest`-mod avviker noen av dem. De holdes utenfor hovedtallet.
- `HD text, N of M HD pixels differ strongly`: avvik i pikslene med HD-glyf. Kantene på glyfene er glatte med vilje, så med xBR avviker omtrent 10 prosent av dem. Med `DIGHD_TEXT=nearest` skal tallet være 0. De holdes utenfor hovedtallet.

Under en film skriver hver dump også en linje for selve rammen, i originalpiksler: `film SQ1 frame 487: 61155 px from HD frame, 0 px original on purpose (text), 0 px original without HD, HD text over 2845 px`. Tekstpiksler med HD-glyf telles under det som er under dem (her HD-rammen), og i tillegg i det siste tallet. Med `DIGHD_VERIFY=1` skriver hver dump utenom film hvilke kostymer hver skuespiller sist ble tegnet med, og hvor mange av rutene som har HD-bilde: `costumes drawn: actor 6 costume 210 (1 cels HD, 0 without, raw codes)`. `raw codes` betyr at kodene ble tegnet rett som palettindekser. Første gang et kostyme tegnes i et rom med en palett, kommer også en linje som `costume 210 in room 78 with palette 0: codes as palette indices` (eller `codes through AKPL and the actor palette`).

## Objekttilstander i testen

Et objekt (dør, maskin, lys) har ett bilde per tilstand: `objNNN_01.png`, `objNNN_02.png` og så videre. Etter testhoppet vises hvert objekt bare i tilstanden skriptene ga det, så HD-bildene for de andre tilstandene blir aldri prøvd. `DIGHD_TEST_OBJSTATE` setter tilstanden selv:

- `DIGHD_TEST_OBJSTATE=884:2,886:1`: objektene settes i disse tilstandene `DIGHD_TEST_OBJSTATE_AT` bilder (standard 30) etter at spillet er i testrommet. Uten `DIGHD_TEST_ROOM` gjelder det rommet spillet er i ved bilde `DIGHD_TEST_AT`.
- `DIGHD_TEST_OBJSTATE=alle`: alle objektene i rommet som har bilder, sortert etter nummer, og for hvert av dem tilstand 1 til antallet bilder (IM01, IM02 og så videre). Hver tilstand vises i `DIGHD_TEST_OBJSTATE_EVERY` bilder (standard 40, omtrent 0,4 sekunder uten skjerm; bildene her er skjermoppdateringer, som for de andre testvariablene). Før neste objekt settes objektet tilbake til tilstanden det hadde. Når alt er vist, skriver loggen `object states done`, og med `DIGHD_QUIT_AT` avslutter spillet med en gang.

Tilstanden settes slik skript-opkoden setState gjør det (`o6_setState`): `putState`, `markObjectRectAsDirty`, og tegnekøen tømmes når bakgrunnen skal tegnes på nytt. Motoren tegner da objektet på den vanlige veien i neste bilde (`drawObject`, som melder objektet til DigHD), og DigHD ser det slik det ser det i spillet. Andre ting testkroken gjør:

- Setter spillet en annen tilstand på objektet senere, settes den tilbake. Loggen sier det én gang per objekt.
- Har objektet en forelder, tegner motoren det bare når forelderen har tilstanden objektet krever (`drawRoomObject`). Da settes forelderen også.
- Er objektet ikke helt på skjermen, flyttes kameraet til midten av objektet og holdes der som med `DIGHD_TEST_CAMX`. Ikke når `DIGHD_TEST_CAMX` eller `DIGHD_TEST_CAMY` er satt.
- Tilstander uten rombilde (SMAP) hoppes over: noen objekter har bare BOMP-bilder (6 i rom 107 og ikonene i rom 93), og skriptene tegner dem som blast-objekter. Tegnet som en del av rommet ville ScummVM stoppet med en assert i `Gdi::drawBitmap`.
- Uten variabelen gjør testkroken ingenting.

Ved slutten av hver tilstand lagres skjermen når `DIGHD_DUMP_DIR` er satt, og loggen får en linje per objekt testkroken holder. Med en liste skjer det én gang, `DIGHD_TEST_OBJSTATE_EVERY` bilder etter at tilstandene ble satt. Linjen kommer også ved hver vanlig dump. Eksempel fra rom 50:

```
DigHD: test, object 884 state 2 at frame 334 (step 2 of 3), at 0,88 160x112, 3 images
DigHD: test object 884 state 2 frame 373: drawn yes, HD image yes, object px 15894, HD object px 15894, at 0,88 160x112, on screen 17920 px: HD room px 0, other HD object px 0, HD sprite px 0, original px 2026 (without HD 2026)
```

- `drawn`: `yes` når objektet er tegnet i tilstanden etter at den ble satt, `no` når det ikke er tegnet (for eksempel utenfor skjermen), og `with state N` når spillet har tegnet det i en annen tilstand.
- `HD image`: `yes` (lest og brukt der objektet vises), `no` (`objects/objNNN_SS.png` eller `_idx.png` finnes ikke i modden), `unreadable` (finnes, men kunne ikke brukes; advarselen over sier hvorfor, for eksempel feil størrelse) og `not loaded` (objektet er ikke tegnet i tilstanden ennå).
- `object px`: objektets egne piksler på skjermen. Det vil si piksler som ikke er gjennomsiktige, som ikke er like rombakgrunnen når rommet har HD-bakgrunn (der viser motoren HD-rommet), og som ikke er dekket av noe annet: pikselen har verdien objektet tegnet, og ikke et annet objekt tegnet senere viser den. `HD object px` er de av dem som kom fra HD-objektet.
- Resten er kildene for alle pikslene i objektets rektangel på skjermen, som i linjen `whole screen`.

`tools/romtest.sh --objekter` bruker `alle` i hvert rom og lager en rapport med nærbilder per objekt og tilstand (se `docs/SPILLTEST.md`).

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

HD Graphics i spillets meny (testet uten skjerm 2026-10-09, modden `gpt` i rom 22, med `DIGHD_TEST_KEYS=400:f5` og `DIGHD_TEST_CLICKS`):

- Menyen viser raden HD Graphics under Text Speed, med kryss når HD er på. Rammen og knappene til høyre står riktig, også på siden for lagring.
- Klikk på boksen: loggen sier `classic graphics`, rommet rundt menyen blir klassisk med en gang, og boksen blir tom. Play lukker menyen, og spillet fortsetter i klassisk grafikk (64 000 originalpiksler i hele skjermen).
- Ny start med samme HOME: spillet starter i klassisk grafikk (`dighd_classic=true` i `[scummvm]`), og boksen er tom. Klikk igjen gir HD og `dighd_classic=false`.
- `engine/test.sh` etter endringen: 0 avvik for bakgrunner og uskalerte figurer, skjermen lik hele skjermen bygget på nytt i alle 12 dumper, og avvik bare i skalerte figurer som før.
- Ikke testet: ekte mus og skjerm, og menyen under en film.

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

Undertekster over filmer (testet uten skjerm 2026-10-07, introen SQ1 med `--subtitles`, før HD-teksten kom, så tekstpikslene var originalpiksler. Testen med HD-tekst står under Tekst i HD):

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

Kodek 5 (testet uten skjerm 2026-10-07). Modden `test-k5` er laget med `nearest` og har alle 144 kostymer med kodek 5 og de 59 rommene de ligger i. Spillet hoppet med `DIGHD_TEST_ROOM` til hvert av rommene, med `DIGHD_VERIFY=1` og 700 bilder etter hoppet. Kodeken er lest fra AKHD-blokken i hver kostyme (`costumes.json` har nå kodeken). Uttrekket brukte RGBS også for kodek 5 da dette ble testet, så andelene under gjelder de gamle fargene. Se Kodek 16 og fargene for kodek 5 og 16 for tallene etter rettingen.

- Funnet og rettet: indeksbildene for alle kostymer med kodek 5 (14 124 ruter) og 150 objektbilder (inventaret i rom 93 og 6 i rom 107) har gjennomsiktig palettindeks 255. I PNG krever det en tRNS-blokk med 256 verdier, og da gjør PNG-leseren i ScummVM bildet om til RGBA. DigHD avviste dem ("not an 8-bit indexed PNG"), så ingen av dem fikk HD. Nå leses indeksbildet uten tRNS-blokken, og den gjennomsiktige indeksen hentes fra blokken.
- Funnet og rettet: piksler der den ekte fargen er svart, men spillet viser en lys farge, ble svarte i HD (30 piksler i kostyme 210 i rom 78). Nå blir de originalpiksler, som skygger og effekter. Dette fjernet også noen avvik i `engine/test.sh` (bilde 250 gikk fra 72 til 0).
- Funnet og rettet: krasj i `compose` når en fade bygget skjermen på nytt rett etter bytte fra et rom med HD-bakgrunn til et rom uten (rom 79 til 92, sett med gdb). Pikslene pekte fortsatt inn i bildet til det gamle rommet. Nå blir de originalpiksler ved romskifte til de tegnes på nytt. Dette kan også skje i vanlig spill.
- Etter rettingene ble 30 kostymer med kodek 5 tegnet med HD i 15 rom: 31 (rom 13), 74 (25), 119 (34), 278 til 281 (40), 318 (47), 326 (66), 320 (72), 210 (78), 238 (89), 240 (91), 225 (79), 282 til 297 (96 til 99). 0 sterkt avvikende piksler i alle 135 dumper.
- Andel av figurpikslene som kom fra HD-bildet (resten er originalpiksler som skygger, effekter eller farger som ikke stemmer): 91 prosent i rom 13, 69 prosent i rom 40, 60 til 85 prosent i rom 78.
- Ikke testet: inventaret (rom 93) og rom 107 i spillet, og ekte HD-bilder for kodek 5.

Kodek 16 og fargene for kodek 5 og 16 (testet uten skjerm 2026-10-07). To modder laget med `nearest`, en fra det gamle uttrekket (RGBS) og en fra det nye, med de 34 kostymene med kodek 5 og 16 som ble sett da spillet hoppet til hvert rom, og 95, 96 og 118. Spillet hoppet med `DIGHD_TEST_ROOM`, gikk 1000 bilder med `DIGHD_VERIFY=1` og dumpet hvert 25. bilde.

- 0 sterkt avvikende piksler, og skjermen lik hele skjermen bygget på nytt, i alle 40 dumper i hver av de 22 kjøringene, med begge moddene.
- Kodek 16 tegnes med HD: 95 i rom 30 (med `DIGHD_TEST_CAMX=264`), 266 i rom 92, og med testkroken 267 i rom 92, 96 i rom 31 (med `DIGHD_TEST_PALETTE=1`) og 118 i rom 33.
- Andel av figurpikslene med HD-bilde som fikk HD, og hvor mange av dem som måtte tones, summert over dumpene:

| Rom | Kostymer | Gammelt uttrekk | Nytt uttrekk |
| --- | --- | --- | --- |
| 8 | 21 | 91 % (13 % tonet) | 100 % |
| 13 | 31 | 90 % (56 %) | 100 % |
| 25 | 74 | 0 % | 0 % (skygge, se under) |
| 34 | 119 | 97 % (38 %) | 99,7 % |
| 40 | 278 til 281 | 69 % (24 %) | 100 % |
| 47 | 318 | 81 % (49 %) | 100 % |
| 66 | 326 | 87 % (44 %) | 100 % |
| 72 | 320 | 83 % (41 %) | 100 % |
| 78 | 210 | 72 % (32 %) | 100 % |
| 82 | 229 | ikke tegnet i kjøringen | 99 % |
| 89 | 238 | 12 % (100 %) | 96 % |
| 91 | 240 | 99 % (22 %) | 99 % |
| 92 | 266 | 88 % (21 %) | 100 % |
| 95, mellomsekvens i rom 79 og 92 | 225, 266, 267 | 84 % (23 %) | 99,8 % |
| 96 til 99 | 282 til 297 | 56 til 78 % (19 til 39 %) | 100 % |
| 30 | 95 | 100 % (0 %) | 99 % |
| 31, testkroken | 96 | 47 % (72 %) | 70 % |
| 33, testkroken | 118 | 66 % (21 %) | 68 % |
| 92, testkroken | 267 | 73 % (64 %) | 100 % |

  Med det nye uttrekket ble ingen figurpiksler tonet.
- Rom 25 (kostyme 74, airlock): ruten tegnes med skyggemodus, så alle pikslene er en blanding med det som ligger under. De blir originalpiksler med vilje, med begge uttrekkene.
- 96 og 118: 5 prosent av pikslene har koder som sykles i rommet, og syklede farger på figurer er originalpiksler. Tallene i tabellen er summert over alt som ble bygget, også når skjermen bygges på nytt etter et syklingssteg før skuespillerne er tegnet på nytt. Da peker noen piksler en kort stund på en rute som er byttet, og de blir originalpiksler. Talt bare i de ferdige bildene i dumpene (midlertidig måling, tatt ut igjen) fikk 96 76 prosent HD og 118 81 prosent, og resten var syklede farger.
- Med `lanczos-sharp` for 95, 96, 118, 210, 266 og 267: figurene er glatte og står på samme sted som originalen (sett på kulene i biblioteket og spøkelset).
- Uttrekket: `dighd extract` til en ny mappe og sammenlignet fil for fil med det gamle. 149 kostymer endret, nøyaktig de med kodek 5 og 16. De 182 med kodek 1 er byte for byte like. Rutene og størrelsene er de samme.
- `engine/test.sh`: 0 avvik ved bilde 250, 750, 1000, 1750 og 2500 til 3000, og 0,081 til 0,195 prosent ved 500, 1250, 1500, 2000 og 2250 (de samme bildene med skalerte astronauter som før). Skjermen lik hele skjermen bygget på nytt i alle 12 dumper.
- Ikke testet: ekte skjerm, 96 og 118 der skriptene viser dem, og de 110 kostymene med kodek 5 og 16 som ikke ble tegnet da spillet hoppet til rommene.

Tekst i HD (testet uten skjerm 2026-10-07, med `--subtitles`, `DIGHD_VERIFY=1` og `DIGHD_DUMP_FLAT=1`):

- Spillet: rom 2 med modden `test-nearest`, 2500 bilder, dump hvert 50. bilde. 25 dumper med tekst (replikkene «Low here. Come on out, kids.», «The water's fine.», «Robbins here. Going independent.», «Welcome to the wonderful world of space.» og «Don't bump into anything.»). Skjermen var lik hele skjermen bygget på nytt i alle 50 dumper. Hovedtallet var som før (0 utenom skalerte astronauter). I pikslene med HD-glyf avvek 9,2 prosent av HD-pikslene kraftig fra originalen, fordi kantene er glatte.
- Filmen: introen SQ1 med en mod med HD-rammer laget med nearest for rammene 0 til 650, 700 bilder, dump hvert 10. bilde. 22 dumper med tekst («Borneo Deep Space Observatory» og undertekstene). 0 avvik i hovedtallet og skjermen lik hele skjermen bygget på nytt i alle 70. I pikslene med HD-glyf avvek 10,2 prosent kraftig.
- `DIGHD_TEXT=nearest`: 0 avvikende piksler i teksten i alle 24 dumper med tekst i spillet og alle 21 i filmen. Glyfene står på riktig sted med riktige farger, og det som er under teksten, er riktig.
- Plassering: HD-dumpen skalert ned med område-snitt (4 x 4) og sammenlignet med originalpikslene for det samme bildet, i området der de skiller seg pluss én piksel rundt. HD-bildet ble også forskjøvet fra minus 4 til 4 HD-piksler i begge retninger. Minst feil uten forskyvning i alle 25 dumper med tekst i spillet og alle 22 i filmen. Snittfeil per farge uten forskyvning 4,3 til 11,4 i spillet og 13,1 til 18,3 i filmen (glatte kanter), med en fjerdedels originalpiksel forskyvning 9,7 til 26,0 og med én originalpiksel 32,6 til 74,5.
- Ingen spøkelsestekst: i dumpene etter at en replikk er borte, er det ingen piksler med HD-glyf, og der replikken sto, er bildet nøyaktig likt originalen (bilde 1600 og 1650 i rom 2).
- Bannere og menyer: Shift+P (volumbanneret) og F5 (hovedmenyen) med `DIGHD_TEST_KEYS` i rom 2. Teksten er HD, skyveknappene er sammenhengende linjer, og banneret er borte uten rester når det tas bort.
- Klassisk grafikk: Ctrl+H i rom 2 og midt i filmen ga ensfargede 4 x 4-blokker, likt originalen, også teksten.
- Gult felt: i rom 2 med modden `gpt` (rommet har ikke HD-bakgrunn) og i filmrammer uten HD-ramme er bakgrunnen gul og teksten ikke. I rom 2 hadde 85 prosent av de indre delpikslene i den svarte kanten og den gule teksten nøyaktig originalfargen. Resten er glatte kanter.
- `engine/test.sh`: 0 avvik ved bilde 250, 750, 1000, 1750 og 2500 til 3000, og 0,08 til 0,21 prosent ved 500, 1250, 1500, 2000 og 2250 (skalerte figurer, sett på i bilde 2250: en astronaut). Skjermen lik hele skjermen bygget på nytt i alle 12 dumper.
- Ytelse, `DIGHD_BENCH` (hele skjermen bygget, median over dumpene med tekst på skjermen). Maskinen er delt, og tidene varierer med omtrent 0,5 ms mellom kjøringer:

| Hva | Før | Med HD-tekst |
| --- | --- | --- |
| Rom 2, 28 dumper med tekst, to kjøringer | 9,0 og 9,3 ms | 8,9 og 9,2 ms |
| Rom 2, uten tekst (6 dumper) | 9,0 og 8,8 ms | 8,9 og 8,9 ms |
| Filmen SQ1 med HD-rammer, 15 dumper med tekst | 1,25 ms | 1,74 ms |
| Filmen uten tekst (14 dumper) | 1,25 ms | 1,35 ms |

  I rommet forsvinner kostnaden for glyfene (omtrent 1500 til 3000 tekstpiksler) i støyen. I filmen, der resten av bildet bare kopieres fra HD-rammen, koster de omtrent 0,5 ms. Lesingen av HD-rammen (omtrent 23 ms) er fortsatt det som koster mest. Med `DIGHD_TEXT=off` er tiden som før.
- Skala 2 og 3 (`DIGHD_SCALE`), rom 2 i 1500 bilder: ingen feil, skjermen lik hele skjermen bygget på nytt i alle 30 dumper, teksten glatt (sett på ved skala 3).
- Ikke testet med ekte skjerm. Ikke testet i andre rom enn rom 2 eller i andre filmer enn SQ1.

Figurkilden (testet uten skjerm 2026-10-07, rom 2, med `DIGHD_DUMP_FLAT=1`). Samme kjøring med motoren før og etter endringen. Avvik er telt piksel for piksel mot originalpikslene for det samme bildet, uten terskel:

- Volumbanneret (Shift+P med `DIGHD_TEST_KEYS`) over en skalert astronaut, modden `test-nearest` og `DIGHD_TEXT=nearest`: før avvek 241 originalpiksler inne i boksen (56, 90 til 264, 103), etter 0.
- Hovedmenyen (F5) over en uskalert astronaut: før avvek 691 originalpiksler inne i boksen (16, 40 til 304, 161), og `DIGHD_VERIFY` fant 308 sterkt avvikende HD-piksler. Etter: 0 og 0.
- Gult felt med en mod uten kostymer (rom og objekter fra `test-nearest`) og `DIGHD_TEXT=off`: volumbanneret over en figur hadde 1082 gule piksler i boksen før, 0 etter. Replikken «A professor once told me, ...» over en astronaut (samme replikk i to kjøringer): før var 303 av 1374 piksler i tekstfargen gule, etter 0. Astronauten under er fortsatt gul.
- Gammel og ny regel i samme kjøring (midlertidig måling, tatt ut igjen): i 3000 bilder i rom 2 med `test-nearest` fikk alle piksler som den gamle regelen ga en figurkilde, nøyaktig samme kilde med den nye, og ingen andre. Med volumbanneret, hovedmenyen og `DIGHD_TEXT=off` var de eneste forskjellene pikslene i boksene (360 og 5817). Første bilde etter at banneret var borte, hadde 4691 figurpiksler med HD. Uten at merkene ble lagt tilbake, ville 4820 figurpiksler vært originalpiksler i det bildet.
- Gult felt slått på midt i rom 2 (Ctrl+Shift+H): figurene var gule i første dump etterpå.
- `engine/test.sh`: 0 avvik ved bilde 250, 750, 1000, 1750 og 2500 til 3000, og 0,081 til 0,210 prosent ved 500, 1250, 1500, 2000 og 2250 (skalerte figurer, sett på i bilde 2250: indre kanter i en astronaut). Skjermen lik hele skjermen bygget på nytt i alle 12 dumper.
- Ytelse, `DIGHD_BENCH=100` ved hver 25. bilde i 1300 bilder med `test-nearest` (50 dumper i rom 2, median): hele skjermen 9,63 ms før og 9,66 ms etter. Spillskjermen sendt gjennom motoren med oppslag av kildene: 9,4 til 10,0 ms med den nye regelen og 9,6 til 9,7 ms med den gamle (den gamle med en midlertidig bryter i samme program, to kjøringer hver). Forskjellen ligger i støyen. Merking av 3 ruter: 0,006 ms per bilde.
- Ikke testet: ekte skjerm, andre rom enn rom 2, blast-objekter over figurer, figurer bak en maske, og tekst der en figur uten HD sist ble tegnet (ikke fanget i en dump, men det er samme regel).

Alle rom (testet uten skjerm 2026-10-07 med `tools/romtest.sh`, modden `gpt` med 104 HD-rom, 226 kjøringer med kameraet over hele bredden og høyden av store rom):

- 110 av 111 rom ble lastet. Ingen krasj eller heng etter rettingen under. HD-bakgrunnen ble lastet og brukt i alle 104 rom som har den. Skjermen var lik hele skjermen bygget på nytt i alle dumper, og ingen HD-bilder var forskjøvet.
- Funnet og rettet: hoppet til rom 93 (ikonene i inventaret, 40 x 200) stoppet ScummVM med en assert i `clampCameraPos`. Testhoppet hopper nå ikke til rom som er mindre enn skjermen. Gjelder bare testkroken; spillet viser aldri rommet.
- Funnet og rettet: `DIGHD_TEST_CAMX` ble overstyrt når kameraet fulgte en skuespiller eller et skript flyttet det. Rom 27 og 105 setter kameraet hele tiden og vinner fortsatt for noen plasser.
- Figurene gikk bak det samme i HD som i originalen i alle rom med figurer i bildet.
- `engine/test.sh` etter endringene: 0 avvik ved bilde 250, 750, 1000, 1500, 1750 og 2500 til 3000, og 0,077 til 0,172 prosent ved 500, 1250, 2000 og 2250 (skalerte figurer, som før). Skjermen lik hele skjermen bygget på nytt i alle 12 dumper.
- Ikke kontrollert: rom 10 og 104 (spillet tonet ned og forlot rommet straks etter hoppet).

Objekttilstander (testet uten skjerm 2026-10-07 med `tools/romtest.sh --objekter --kamera ett`, modden `gpt`, 40 bilder per tilstand, `DIGHD_VERIFY=1`, alle 111 rom på 16 minutter med to kjøringer samtidig):

- 72 rom har objekter med bilder. 70 ble kjørt med `alle`: 489 tilstander av 296 objekter. Rom 93 hoppes ikke til (mindre enn skjermen), og i rom 10 forlater spillet rommet ved bilde 290, før den første tilstanden.
- HD-bildet ble brukt i 406 tilstander, og i alle av dem kom alle objektets synlige piksler fra HD-bildet. Alle 30 ChatGPT-objektene er blant dem, også obj884 i rom 50 (3 tilstander) og obj886 i rom 46 (2).
- 5 tilstander er like rombakgrunnen overalt (obj179_03 i rom 23 og fire andre), og der viser motoren HD-rommet. 12 tilstander mangler i modden (rom 32 og 88, som ikke er i modden). 3 er utenfor skjermen: obj789 i rom 105, der skriptet flytter kameraet tilbake hvert bilde. 6 er BOMP-bilder i rom 107 og ble hoppet over.
- 57 tilstander er dekket av et annet objekt i tilstanden etter hoppet: krystallene obj775, obj776, obj778 og obj779 i rom 100 (14 tilstander hver) og obj592 i rom 89. Med listen `DIGHD_TEST_OBJSTATE=769:0,775:5` i rom 100 synes obj775, og alle 337 objektpikslene kom fra HD-bildet.
- Skjermen var lik hele skjermen bygget på nytt i alle 483 dumpene etter et tilstandsbytte, også når kameraet ble flyttet. Tegningen etter `putState` går riktig gjennom de skitne områdene.
- Nærbildene er sett på for obj884 (alle tre tilstandene), obj886 (skjelettet er der i tilstand 1 og borte i tilstand 2), obj191, obj547, obj400 (fire tilstander), obj775 og obj537: HD-bildet står der originalen har objektet, og byttet mellom tilstandene synes.
- Funnet og rettet: testkroken satte først også objekter med bare BOMP-bilde, og ScummVM stoppet med en assert i `Gdi::drawBitmap` (rom 107, obj807). Nå hoppes de over.
- Funnet og rettet i `tools/romtest.py`: med en relativ `--ut` havnet dumpene i den midlertidige mappen motoren kjører i, og ble slettet. Alle rom fikk status svart skjerm. Stiene gjøres nå absolutte.
- Med en mod med feil med vilje (obj884_02 fjernet og obj884_03 i feil størrelse) skrev loggen `HD image no` og `HD image unreadable` med advarselen `objects/obj884_03.png is 320x224, expected 640x448`, og rapporten viste `ikke i modden` og `HD-bildet ikke lest` med HD-andel 0.
- Funnet, ikke rettet (gjelder bildene i modden, ikke motoren): obj547_01 (ChatGPT, rom 79) har en grå strek, 1 HD-piksel bred, langs nederste rad og venstre kolonne. Nederste rad har snittlysstyrke 88 mot 45 i raden over, og venstre kolonne 62 mot 9. Den synes langs skjermkanten i rom 79, der originalen er mørk. 10 andre ChatGPT-bilder har også en nederste rad som er tydelig lysere enn raden over. I obj844, obj701 og obj160 er den nederste originalraden lik rommet, så motoren viser HD-rommet der, og streken synes ikke. Det samme ligger i `work/gpt-ferdig`, så det kommer fra bildet eller fra `dighd gpt-inn`, ikke fra motoren. I ChatGPT sitt lerret (`resultat.png`) går bildet 1 til 4 piksler ut over feltet det skulle ligge i, inn i den grå kanten; det kan være årsaken, men det er ikke undersøkt.
- Funnet, ikke rettet: obj400 i rom 58 (automatisk oppskalert) har en lys loddrett strek langs venstre og høyre kant i tilstand 1 og 3, som originalen ikke har. Den ytterste HD-kolonnen er lysere enn de neste. Målt på alle bildene i modden har 59 av 455 automatiske objektbilder en kant som skiller seg mer enn 3 ganger så mye fra pikslene innenfor som de indre pikselgrensene gjør. Ikke alle synes i spillet, for der objektet er likt rommet, vises HD-rommet.
- Ikke testet: at testkroken setter en forelder, og at den setter tilstanden tilbake når spillet endrer den. Ingen av objektene i kjøringene trengte det.
- `engine/test.sh` etter endringen, to kjøringer: 0 avvik ved bilde 250, 750, 1000, 1750 og 2500 til 3000, og 0,103 til 0,236 prosent ved 500, 1250, 1500, 2000 og 2250 (skalerte figurer, sett på i bilde 1500: en astronaut). Skjermen lik hele skjermen bygget på nytt i alle dumpene. Ingen linjer fra testkroken i loggen; den gjør ingenting uten variabelen.

## Kjente begrensninger

- Kostymer med kodek 16: 96 (spøkelset) og 118 (Low som svømmer) er bare testet med testkroken, ikke der skriptene viser dem. Paletten for 96 er valgt etter jevnhet.
- Kodek 5 og 16: fargene i uttrekket er rompaletten der kostymet vises. For 35 kostymer er rommet og paletten målt i spillet, for de andre er det rommet kostymet ligger i og den jevneste paletten. Vises et kostyme i et annet rom eller med en annen palett (266 i rom 79), eller setter skriptet skuespillerpaletten, justerer motoren fargene, og farger som er helt forskjellige blir originalpiksler. Et kostyme som vises med to helt ulike paletter, kan bare få riktige HD-farger i den ene.
- Kodek 5: setter skriptet skuespillerpaletten, får bare den første ruten i hver tegning paletten (`_useBompPalette` settes tilbake etter hver rute i ScummVM). Motoren følger dette per rute. Ikke sett i spillet.
- Objekter som tegnes direkte i bakgrunnsbufferen av skript (sjeldent) blir originalpiksler.
- Testkroken for objekttilstander (`DIGHD_TEST_OBJSTATE=alle`) viser hvert objekt med de andre objektene i tilstanden de har etter hoppet. Et objekt som et annet objekt dekker, synes ikke (57 tilstander i rom 89 og 100), og må testes med en liste der det som dekker har tilstand 0. I rom der skriptet setter kameraet hvert bilde (27 og 105), blir objekter utenfor kameraet ikke vist. BOMP-objekter (blast-objekter) testes ikke.
- Fargesykling: kartet jevner ut over 3 x 3 originalpiksler, så glitter av enkeltpiksler (fossen i rom 43) beveger seg svakere enn i originalen. Bølger over flere piksler (vannet i rom 22) synes godt.
- Fargesykling: kartet leses fra indeksbildet til rommet eller objektet. Ligger et objekt over syklet vann, får bakgrunnspikselen rett ved siden av objektet litt av syklingen under objektet. Ikke sett i rommene som er prøvd.
- Fargesykling på figurer (lys på drakter og maskiner) er fortsatt originalpiksler.
- Tekst: glyfer som klippes i venstre kant i filmene, blir originalpiksler, fordi tegneloopen i ScummVM da tegner dem forskjøvet. Det samme gjelder CJK-tegn (`draw2byte`) og glyfer over 63 x 63 piksler eller med mer enn 4 farger (ingen i The Dig).
- Tekst: sammenhengen med nabotegnene tar bare med piksler i glyfens egne farger. Møtes to tekster i ulike farger, rundes kantene der de møtes.
- Tekst: tegnes noe annet over en tekst uten `markRectAsDirty`, og de nye pikslene tilfeldigvis har samme verdi som glyfen skrev, vises glyfen der til teksten tegnes på nytt. Ikke sett. Blast-tekstene nullstilles uansett hvert bilde.
- Undertekster over filmer: merkene for tekst nullstilles når en ny ramme pakkes ut. Pakker en film ut bare en del av bildet (RLE i SMUSH med mindre rektangel, ikke brukt i The Dig), regnes tekst utenfor den delen som borte selv om den står igjen.
- Figurer: hvilke piksler en rute tegnet, leses fra indeksbildet til ruten, ikke fra tegningen. En rute bak et forgrunnsobjekt (maske) merkes også der den ikke ble tegnet. Viser pikselen da en annen figur, hentes HD-bildet fra feil rute. Slik var det før også. Ikke sett.
- Figurer uten HD-bilde: hvilke piksler ruten tegnet, er ikke kjent. Pikslene i rektangelet som er forskjellig fra bakgrunnen og ikke viser en HD-figur, regnes som figuren (gult felt).
- Blast-objekter over en figur: en piksel objektet tegner med nøyaktig samme verdi som figuren, viser HD-figuren. Ikke sett i The Dig.
- Bannere: merkene legges tilbake bare når banneret tas bort med `clearBanner`. Andre steder som lagrer og legger tilbake skjermen i ScummVM, gjelder andre spill.
