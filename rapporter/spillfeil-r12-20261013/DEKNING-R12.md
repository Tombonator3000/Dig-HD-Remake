# Avgrenset HD-dekning for r12

Kontrollert 13. oktober 2026 mot den ferdig iscenesatte lokale kandidaten. Maskinlesbar dokumentasjon: `DEKNING-R12.json`. Dette gjelder brukerens rapporterte familier og sammenligning med r11, ikke en påstand om komplett HD for hele spillet.

Audit omfatter **1649 kilderuter i 37 kostymefamilier, 15 objekttilstander og 2 rombakgrunner**. Alle tilgjengelige indeksmasker matcher originalens faktiske pikselindekser. Alle tilstedeværende bilder oppfyller motorens størrelseskontrakt: 4x med like marger på motsatte sider; vann og eldre myke sprites bruker andre margstørrelser enn nye r12-sprites. Alle HD-hasher ble kontrollert på nytt etter målingen uten endringer under audit. De **1343 indeksfilene** i Brinks siste palettmanifest er dessuten kontrollert mot ferdig kandidat uten avvik.

Det sikre grafikkhullet **luftsluse 074_004** og de **66 feilaktig tomme lysfasene** som audit fant, er lukket. De undersøkte figur-/effektfamiliene har ingen ytterligere sikkert påviste, udekkede synlige ruter. Dette betyr ikke at alle palettilstander og animasjoner er visuelt godkjent: 22 mørke linsefragmenter står uttrykkelig som uavklart visuell tilstand, beskrevet nedenfor.

## Resultat per rapportert område

| Område | Originalressurs | Resultat |
| --- | --- | --- |
| Boston med lommelykt | 158: 94 ruter | 62 tegnede handlingsruter og 32 eksplisitt registrerte optiske masker/markører. De 32 er ikke manglende Boston-kropper. |
| Boston plukker krystaller | 231: 23 ruter | Alle 23 har registrert HD; kilde-/utsnittsspor i `BOSTON231-REGISTRERING.json`. |
| Brink i krystallscener | 310: 27; 312: 39 ruter | Alle 66 har registrert HD. Hode-/syketilstandens separate kontroll beholdes: 709 eksplisitte hodevalg i sluttimporten, og korrekt palett via originalens AKPL-rute. |
| Luftsluse | 74: 20; 75: 2 ruter | 12 tegnede sluseruter, inkludert ny 074_004; 10 palett-/skyggemasker eller markører uten egen HD-tegning. De ensfargede maskene skal fremdeles virke gjennom motoren. |
| Lensrommets effekter | 78–91 | Alle filer er tilstede. Kostyme 86 har 34 synlige HD-ruter og 2 mørke fragmenter som utslippsterskelen filtrerer. Totalt 27 tomme HD-ruter i hele lensfamilien er fordelt og navngitt nedenfor. |
| Sparks | 61: 54 ruter | Alle 54 aktørruter matcher r11, men dette var utilstrekkelig bevis: det grove synlige feltet lå i objekt 187_01. Det aktive objektet er nå rettet, se egen dokumentasjon nedenfor. |
| Roterende krystallgeometrier | 286–289: 90 hver | Alle 360 matcher registrert grafikk. Originale indeksmasker er bevart; ingen gjeninnført tykk steinramme påvist av denne dekningskontrollen. Visuell kvalitet utover kontrollerte eksempler er ikke bevist av filantallet. |
| Blå staver | 298/299/300: 2+2+1 ruter | Begge tidligere manglende 001-tilstander er med. De tre gamle 000-tegningene er ikke identiske med enkel originaloppskalering, men har ikke et nytt r12-produksjonsbevis. |
| Vann og bølger | 301: 24 ruter | Alle 24 matcher registrerte r11-bilder. Originalens indeksmaske og antall ressursfaser er bevart. |
| Museum spire | rom 34 og 119_000 | Begge finnes. Kostyme 119 er HD-parallaxlaget; `MUSEUM119-KONTROLL.json` dokumenterer kamera 160/360/548 og kontroll av z-maske. |
| Hole/lens-objekter | 121_01,253_01–02,368_01–02,395_01–02,426_01–02 og 238_01 | Alle 10 registrerte tilstander matcher kandidaten; kildeindekser og eksakte 4x-mål er kontrollert. Linsen 238 er den nye kildeforankrede HD-utgaven. |
| Platåoverganger | 387_01 og 388_01–03 | Alle fire registrerte utsnitt matcher kandidaten. |
| Dias og broenergi | 35: 240; 175: 32 ruter | Hele 175-familien på 32 cels har nå særskilt registrering: 30 tegnede kildefaser og 2 tekniske markører. 000/001 er skåret fra én samlet 281×145-master ved x256; 013 har egen master. Sammen med 40 sentrale 35-faser gir manifestet 72 oppføringer. De øvrige 200 cels i 35 er kildeformede utslippsfelt med stabil master innen familien. Ingen valg ved `cel % 3` i sluttstegene. |

## Sparks: det aktive objektet måtte kontrolleres

Ny faktisk lagring 6 viste at fildekning for aktør 14/kostyme 61 ikke forklarte det synlige problemet. Ved frame 120 brukte aktøren 061_000/001 som HD, men et diagnostisk bytte av akkurat disse ga **0 endrede skjermpiksler**. Den grove gnisten var bakt inn i **objekt 187_01**, plassert ved 608,112 med 40×32 originalpiksler. HD-rommet under inneholder ikke gnisten.

To kildebaserte grunnformer ble nytegnet med innebygd `image_gen`, med originalens brun/orange fragmenter, transparente gap og hvitt/lilla lyspunkter. Disse brukes nå bare i det aktive objektlaget: eksisterende HD-romutsnitt er bevart, de nye formene står på originalens koordinater, og originalens eksakte SMAP-maske og indeksbilde styrer dekningen. De diagnostiske aktørerstatningene er tilbakeført; alle 54 kostyme 61-ruter er identiske med tidligere kandidat.

Faktisk ny save 6 er kjørt 480 frames: exit 0, 8 nytegningskontroller og 0 avvik. Frame 120 endrer 1845 piksler, avgrenset til skjermrektangelet 828,504–904,540. Hele scenen og detaljen er sett visuelt og viser tydeligere lys uten den grove gamle flaten. Bevis: `SPARKS187-REGISTRERING.json`, `QA/sparks187-before.png`, `QA/sparks187-final.png`, `QA/sparks187-final-detail.png`. Genereringens eksakte modellversjon ble ikke oppgitt av verktøyet; master og prompt er bevart under `produksjon/`. Ingen andre romdeler ble endret.

## De 66 korrigerte små lysfasene

Den tidligere regelen «bredde eller høyde under fem» behandlet reelle lysglimt som tekniske. Dette er rettet bare for den kontrollerte listen. Dimensjon alene er ikke lenger årsak til å gjøre dem tomme. Originalens alfa, farge og utslipp bestemmer den lokale lysformen; den eksisterende riktige lysmasteren bidrar svakt innenfor denne formen. Det er ingen ny krystall eller skygge rundt blinket.

- 120: **000,001,002,003,004,021,027,028,029,031,032,033,035,036,037,042,043,044,045,046,047**.
- 146: **000,001,002,003,004,005,006,007,008,009,010,011,012,013,014,015,027,029,031,032,033,048,049,050**.
- 165: **012,013,018,031,032,045,046**.
- 185: **026,027,028,029,030**.
- 207: **000,001,003,019,022,025,028,035,039**.

Alle 66 er observert som myke HD-cels i runtime-loggene. Originalchore 8 er kjørt, i tillegg til chore 1 for 165 og chore 7 for 207. **10 isolerte kjøringer, 80 full-redraw-kontroller, 0 avvik, alle prosesser exit 0**. Fem hele rombilder er også sett visuelt. Dette er en målrettet test med kopi av lagring 6, ikke manuell full gjennomspilling. De øvrige 185 bryterbildene er byteidentiske med første auditsnapshot, og alle 251 indeksmasker er uendret. `BRYTER-LYSMINIFASER.json` har hver kildedimensjon, før-/etterhash, lysstyrke og observerte cels per logg.

Reproduksjon: `stage-switches.py --light-miniphases-only` i det lokale r12-arbeidsområdet. Flagget retter bare listen over; øvrige bilder og registreringer beholdes.

## Gjennomsiktige HD-filer er ikke én feiltype

- **Tom kilde:** 082_004 har ingen synlige originalpiksler. En gjennomsiktig HD-fil er riktig.
- **Mørke arkitekturribber:** 087_006,087_017,091_006,091_017 er visuelt undersøkte lilla linseribber. `register_energy_field.py` lar den eksisterende HD-romgrafikken tegne disse og tilfører bare emittert lys. De er ikke tomme originaler og må aldri registreres som slike.
- **22 mørke fragmenter under utslippsterskelen:** 081_000,002,003,004,006,007,008,014,015,016,017,019,020,021,022,025,032,033,034; 086_002,019; 088_015. Kildene har lave røde/lilla lysverdier. De filtreres fordi vektingen `0.25R+0.5G+0.25B` er under 0,35. Det forklarer fraværet teknisk, men beviser ikke at alle skal være usynlige ved alle runtime-paletter. Derfor står de som `dark_fragment_filtered_visual_state_unverified`, ikke «komplett», «mangler sikkert HD» eller «teknisk maske». Det ble ikke laget nye former ut fra usikker identitet.
- **Optiske/tekniske markører:** 32 ruter i 158 er eksplisitt registrert som `optical_mask_or_marker` i handlingsmanifestet. Luftslusens 10 masker har separat original-/motorbevis. 175_002/014 er små markørruter, atskilt fra de 30 tegnede energifasene i den samlede 175-familien.

Ingen synlig fil i dette utvalget er pikselidentisk med en ren nearest- eller Lanczos-oppskalering av den registrerte originalen. Den eneste identiske er den tomme 082_004. Dette utelukker bare akkurat de to uendrede transformene; det beviser ikke at et bilde er nytegnet eller semantisk riktig. De 66 minifasene er med hensikt kildeformet lys med filtrering og masterbidrag, og beskrives som dette.

## Bedre bevis enn filantall

`DEKNING-R12.json` inneholder kilde-/HD-/indekshash, originalpalett, synlig flate, dimensjoner, klassifisering og registreringsspor per celle. Hver original AKCH-gruppe har kostyme, valg, animasjon, retning, lag, kilderuter og HD-hasher. Dermed er det mulig å skille manglende fil, tomt innhold, feil kildeindeks og feil registrering.

En viktig begrensning ble bekreftet i `code/pipeline/dighd/gamedata.py:311`: `akos_animations()` samler førstegangs-/nåbare celler og utelater stoppede eller tømte lag. Dette er ikke et eksakt animasjonstidsmanifest. Full fasekontroll bør i tillegg lagre:

1. Originalspill- og AKCH/AKSQ-hash med kommandooffset, faktisk gren, ventetid, repetisjon, samtidige lag og tømmetidspunkt.
2. Runtimeframe, aktør, kostyme/cel, sekvensposisjon, retning, rom, kamera, faktisk palett/tegnemodus og koordinater.
3. SHA for kilde og aktiv HD-fil i samme test, kopiert lagring og valgt originaltilstand, samt original/HD-bilder før, under og etter overgangen.
4. Separate utfall for kildeidentitet, registrering, runtime, visuell kontroll og kontroll av distribuert pakke.

De korrigerte minifasenes logger dokumenterer nå hvilke ruter som faktisk ble tegnet. De fyller ikke alle feltene i denne utvidede kontrakten, og rapporten presenterer derfor ikke fildekning som full fase- eller kvalitetsgodkjenning. Sam & Max-sammenligningen er oppdatert med forbedringene som faktisk ble gjennomført etter analysen.

Sluttsnapshot er låst til kandidatens `SHA256SUMS`-filhash `c7b650b07429567163af62e9ac103db81792b745f4543cbd081ac15dfae9c563`. Rapport- og grafikksjekk etter siste 175-/sparksendring gir ingen ytterligere forskjeller mot manifestet.
