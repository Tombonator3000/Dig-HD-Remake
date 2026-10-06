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

## Stedene i ScummVM som er endret

| Fil | Endring |
| --- | --- |
| `engines/scumm/dighd.cpp`, `dighd.h` | All HD-logikk (ny fil) |
| `scumm.cpp` | Lager DigHD, setter opp HD-skjermen, motoren holder seg i 8 bit, hook før hver skjermoppdatering |
| `gfx.cpp` | Siste blit (`drawStripToScreen`), overgangseffekter, `moveScreen`, risting av skjermen |
| `palette.cpp` | Palett sendes til DigHD i stedet for til skjermen |
| `object.cpp` | Melder hvilke objekter som tegnes og i hvilken tilstand |
| `akos.cpp`, `akos.h`, `base-costume.cpp` | Melder hvilke kostymeruter som tegnes, hvor og om de er speilvendt |
| `cursor.cpp`, `input.cpp`, `saveload.cpp` | Musepeker i HD, museposisjon delt på skala |
| `smush/smush_player.cpp` | Filmrammer og filmpalett via DigHD |

## Innstillinger

| Variabel / nøkkel i scummvm.ini | Betydning |
| --- | --- |
| `DIGHD_MOD` / `dighd_mod` | Mappen med HD-grafikk. Uten denne kjører spillet helt som vanlig |
| `DIGHD_SCALE` / `dighd_scale` | Skala, standard 4 |

Test og feilsøking (bare miljøvariabler):

| Variabel | Betydning |
| --- | --- |
| `DIGHD_VERIFY=1` | Sammenligner HD-bildet med originalen ved hver dump og skriver avviket i loggen |
| `DIGHD_DUMP_DIR`, `DIGHD_DUMP_EVERY` | Lagrer skjermbildet som PNG hver N-te bilde |
| `DIGHD_SKIP_VIDEO=1` | Hopper over filmer |
| `DIGHD_TEST_ROOM`, `DIGHD_TEST_AT`, `DIGHD_TEST_CAMX` | Hopper rett til et rom etter N bilder |
| `DIGHD_QUIT_AT` | Avslutter etter N bilder |

## Hva som er testet

Med en mod laget med `nearest` skal HD-bildet være likt originalen skalert opp. Det er sjekket i spillet uten skjerm (`engine/test.sh`):

- Bakgrunner og uskalerte figurer: 0 avvikende piksler.
- Skalerte figurer: avvik på indre kanter (under 0,25 prosent av skjermen), fordi HD-sprites skaleres jevnt. Det er ventet.
- Objekter: rom 34 og 105 testet med HD-objekter, 0 avvikende piksler.
- Filmrammer: 198 av 198 rammer i introen er like. Rammenummeret er `_frame - 1` i SmushPlayer.

## Kjente begrensninger

- Undertekster over filmer som er byttet ut med HD-rammer, blir borte, fordi teksten er tegnet inn i originalrammen. Må løses før filmer med tekst byttes ut.
- Kostymer med kodek 16 (5 kostymer) får ikke HD-sprites ennå. Kodek 1 (182 kostymer, blant dem hovedpersonene) er testet i spillet. Kodek 5 (144 kostymer) er koblet inn, men ikke kontrollert for seg.
- Objekter som tegnes direkte i bakgrunnsbufferen av skript (sjeldent) blir originalpiksler.
- Tegnsett og tekst er originalpiksler. HD-fonter er en senere jobb.
