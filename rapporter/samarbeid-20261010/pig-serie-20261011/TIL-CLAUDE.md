# Pig: ny serie etter Toms hovedarkgodkjenning

Tom svarte «Godkjenner» 11. oktober på `hovedark/pig.png`, SHA256 `0a8f82028f5365932ec737443abde290fd96ac66de15bc634a3b0b5786bf4a7c`. Pig er en automatisert null-G-utstyrscontainer. Hovedarket bestemmer felles design; originalens RGBA-ruter bestemmer fase, deler, vinkel og plassering.

Seks ark er grafikklevert til `gpt-arbeid`, med 147 originale ruteoppføringer. Tre heleark er HOLD. To separate native korreksjonsplater følger for kontrollert mottak. Ingen av de nye seriearkene er spilltestet eller individuelt godkjent av Tom. Claude har ikke kvittert for mottak.

| Ark | Forsøk | Kilder | Faktisk isolert VERSION2-import | Levering |
| --- | ---: | ---: | --- | --- |
| fig007_01 | 4 | 26 | 25 ok, 1 sjekk | resultat.png |
| fig007_02 | 4 | 35 | 35 ok | resultat.png |
| fig007_03 | 2 | 18 | 17 ok, 1 sjekk | HOLD064 |
| fig007_04 | 2 | 31 | 31 ok | resultat.png |
| fig007_05 | 2 | 28 | 25 ok, 3 sjekk | HOLD, separat retting113/117 |
| fig007_06 | 2 | 42 | 36 ok, 6 sjekk | resultat.png |
| fig007_07 | 4 | 48 | 46 ok, 2 sjekk; 23 originalfallback | HOLD, separat retting av fire kroppsfaser |
| fig007_08 | 2 | 5 | 5 ok | resultat.png |
| fig007_09 | 4 | 8 | 8 ok | resultat.png |

Resultatene ligger i `jobber/<jobb>/resultat.png`. De seks direkteleveransene har 140 ok og 7 sjekk, ingen mangler/tom og ingen originalfallback. 241 er kildeoppføringer i alle ni ark, ikke 241 godkjente HD-tegninger. 37 originaloppføringer har færre enn 40 synlige piksler; ingen er ren magenta. I 07 kommer 23 fra faktisk originalfallback og 25 fra nativegrupper.

## Neste handling hos Claude

1. Hent siste `gpt-arbeid` til egen mottakscheckout. `leveranser.json` har eksakte PNG-sjekksummer. Kart for de seks direkteleveransene ligger i `rapporter/romlag-brink-20261010/rutekart-nyordre-del44.json`. Root har kontrollert at uendret VERSION2 faktisk velger disse PNG-ene og boksene som ble testet. Se `mottaksfasit-verifisert.json`.
2. Hold 03/05/07 utenfor nytt automatisk mottak. Baser og kart ligger under `HOLD/`. Det gamle aktive 05-resultatet er bevart med SHA256 `6043eea7311d4199d245fd9a490175caf170a7a468ff402caf08436575c4c90c`. Det er en historisk versjon før dette hovedarket, ikke en ny godkjent Pig-leveranse. Nytt 05-kart er derfor ikke lagt i mottakets søkesti. 03/07 finnes ikke i faktisk leveranseforbruker.
3. Støtt separate nativekilder per bilde-ID for 05 og 07. `mottaksforslag-per-rute.json` er et konkret forslag med base, hjelpe-PNG, SHA og boks. Dagens kode konsumerer det ikke. Velg én nativekilde per rute og bevar originalens canvas, fase, skalagruppe og anker. Ikke sy om, male på eller rydde alfa i nativefiler. Kontroller hele arket etterpå.
4. Rett 064s komponentmål og anker uten å strekke kroppen. [Diagnosen](../pig-import-hold064-20261011/TIL-CLAUDE.md) gjenskaper faktisk eksport 888×592, IoU 0.010 og dekning 0.079. Originalen er 174×134 fordi én ekte opak svart piksel ved [173,133] utvider canvasen. Kropp/kappe dekker 61×54. Bevar fullcanvas og ekte punkt separat; mål og plasser tilsvarende kroppskomponenter. Redusert skala alene løser ikke bunnankeret. Native mangler punktet; ingen fallback påstås allerede utført.
5. Bygg mod og spilltest hele Pig-sekvensen: stabil fysisk størrelse, riktige åpne/lukkede ender, faseglimt, kapper, bevegelser, forgrunnsdekning og kanter. Svar i `../fra-claude/` med grafikkcommit, kodecommit, PNG-SHA, importresultat, modversjon og faktisk utførte tester.

## Separate rettinger

**05:** [native113117.png](rettinger/fig007_05/native113117.png), SHA256 `948c7f1a0aa538f9a1dae8185e1b0cc19222f251baad1259a24f9bc9c22faf03`. 113 har igjen ring/kappe-berøring. 117 har to ringbrudd. To isolerte importoppføringer er ok, IoU 0.828/0.791 og dekning 0.904/0.860. Metall er litt lysere og mer teksturert enn 05a2; gapbredde og kappekontur har mindre forbehold. De 26 øvrige fasene i 05a2 er urørt.

**07:** [native182186187192.png](rettinger/fig007_07/native182186187192.png), SHA256 `7f80b3be56cbbba6ba5d00e95f3736d28521bd710c361e4ae58c229f08fc5fb3`. Nye sølvkonsentriske endetrinn er fjernet; fasekapper/glimt er bevart. Fire isolerte importoppføringer er ok, IoU 0.859–0.925 og dekning 0.882–0.960. Kontrollfeltet er mer frontvendt med grønn geometrisk form/rød knapp. Lys tapperand, løkketendens 182/187, projeksjon 192 og overgang til de 21 øvrige nativefasene krever kontroll. 23 originale småfragmenter behandles separat.

Begge hjelpeplatene er ett nativeforsøk hver. Isolerte metadatautvalg med egen skalaberegning beviser ikke hvordan per-rutekilder oppfører seg i fullarkets skalagrupper. Rett ikke importproblemer ved å deformere grafikken.

## Opplyste forbehold

01s 162 står til sjekk, IoU 0.595 og dekning 0.827, selv om ringbruddene er tilbake.06s 153 har dekning 0.771 og et mindre form-/småflekkavvik. Smådelene 000/008/005/004/170 står også til sjekk. De er ikke kalt manglende eller erstattet med originalfallback.02s 060 har øvre kappe nærmere kroppen enn kilden; en ekstra malt skive er uttrykkelig utelatt fra kartet.08/09 har lysere ytterkontur og noe ekstra dybdeskygge. Se individuelle notater og importkontakter. Rå rektangeloverlapp er ikke alene en artefakt: importen bruker eierskap til sammenhengende alfakomponenter.

## Kontroll og telling

Alle native-PNG-er er kopiert byteidentisk fra innebygd ChatGPT-bildegenerator. Eksakt modellversjon er ikke eksponert. Ingen kreativ etterbehandling, alfarydding eller manuell sammensying. Gråbilder og sammenligningsplater er diagnostikk. Originalprompten er brukt ordrett først, med Toms autoriserte kildebundne tillegg. 36 beskyttede jobbfiler og 38 uvedkommende lokale arbeidsfiler er uendret. Ingen kode, ORDRE.md, status.csv, RAPPORT.md eller retur.md er endret.

Importkoden er uendret `pipeline/dighd/myk.py`, VERSION2 fra main `36cd09f13eb0201cff190d8d0c99c788a8bcaa6b`, SHA256 `7cb20ae673d0576a0f51ecc62f18a289c9c3f1e5b79cff6b9b0cd521f44b6176`. `import-v2/` dokumenterer kilde-, native-, kart- og eksport-SHA. Dette er mottaksdiagnostikk, ingen ny motorvideo.

Samlet ledger har 779/3523 øvrige figurark og 4379 kildeoppføringer. Nyordren har 47/50 tidligere grafikkleverte ark: Boston 21/22, Maggie 9/9, Brink 10/10 og Pig 7/9. Pig-tallet inkluderer gamle 05. Den nye serien etter godkjent hovedark har derfor **6/9 direkteleverte ark**, pluss HOLD-underlag og to separate rettingsplater. Boston 001_20 er også fortsatt HOLD. Romlag 210/230 og Brink-revisjoner 141/208 er uendret i denne leveringen.
