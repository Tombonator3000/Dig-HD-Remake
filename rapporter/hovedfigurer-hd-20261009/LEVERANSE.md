# Hovedfigurene i HD

Tom har bestilt Boston Low, Ludger Brink og Maggie Robbins med alle kostymevarianter i den glatte, detaljerte stilen som ble godkjent i samtalen. Denne oversikten følger de 54 identifiserte kostymene i main-grenens docs/figurer.csv, commit d1ebb643b188b508938e59b477d58b7bd23232b8.

Inventaret inneholder 509 ark og 7 683 synlige originalruter. De fire nye Boston-pilotarkene er bevart. 505 nye referansejobber er pakket med Claudes eksisterende dighd-pipeline, uten kodeendringer og uten å skrive i den delte spillkopien. Originalene er hentet fra de lokale DIG.LA0- og DIG.LA1-filene. Indekser og animasjonsrekkefølge er bevart i jobbmetadataene. Referansepakking er ikke ferdig grafikk.

Første leveransegruppe inneholder seks nye ark med 146 originalruter:

| Jobb | Innhold | Originalruter | Bildeforsøk |
| --- | --- | ---: | ---: |
| fig015_01 | Brink, åtte ståretninger, løse hoder og høyregange | 29 | 5 |
| fig018_01 | Maggie, ståretninger og løse hoder | 18 | 1 |
| fig018_02 | Maggie, høyregange | 12 | 1 |
| fig018_03 | Maggie, venstregange og snakkehoder | 63 | 2 |
| fig014_05 | Boston, gange bort | 12 | 1 |
| fig014_06 | Boston, gange mot oss til høyre | 12 | 1 |

Alle seks er 1536 x 1024 RGBA fra den innebygde ChatGPT-bildegeneratoren. Eksakt modellversjon er ikke bekreftet av verktøyet. Ny native alfa er bevart. To store stilreferanser for Brink og Maggie er også vedlagt, begge 1024 x 1536 RGBA. Konseptreferansene kommer fra repoets main-gren og er bevart med opprinnelig signatur. Materialet forblir privat.

Antall og radfordeling er kontrollert fra faktisk alfa, med særskilt kontroll av en liten originalfragmentrute i fig015_01. Retninger, separate hoder, detaljer og kanter er inspisert. Arkene er vist på lys, mørk og grønn bakgrunn i visuell-del1.png. Brinks siste bakgrunnskorreksjon reduserte restalfa i det tomme nedre høyre hjørnet fra maksimum 43 til 1; 99-persentilen ble 0. Ingen binær originalmaske er lagt over tegningene.

Promptene som faktisk ble brukt, ligger her, inkludert avgrensede korreksjoner. Original prompt.txt og andre beskyttede jobbfiler er urørt. filkontroll-del1.json dokumenterer filene og rutekart-del1.json kobler de større delene diagnostisk til original-ID-er. Boksene ved alfa 128 er analysebokser, ikke ferdige utklipp eller sikre importrektangler.

Andre leveransegruppe inneholder seks nye ark med 199 originalruter:

| Jobb | Innhold | Originalruter | Bildeforsøk |
| --- | --- | ---: | ---: |
| fig014_07 | Boston, gange mot oss til venstre | 12 | 2 |
| fig014_08 | Boston, gange bort til høyre | 12 | 1 |
| fig015_02 | Brink, venstregange og snakkehoder | 72 | 4 |
| fig015_03 | Brink, snakkehoder i skrå retninger | 67 | 1 |
| fig015_04 | Brink, gange mot oss | 12 | 1 |
| fig018_05 | Maggie, gange bort og mot oss til høyre | 24 | 1 |

Antall og radfordeling er kontrollert, med små hudfragmenter skilt fra fullstendige hoder. fig015_02 har 70 større deler og to prikker; fig015_03 har 64 større deler og tre små fragmenter. filkontroll-del2.json, rutekart-del2.json og visuell-del2.png gjelder bare de seks valgte filene. Et tidligere Brink-forsøk med gjennomsiktige hoder er forkastet. Maggie-arket fig018_04 korrigeres fortsatt og er ikke levert.

Tredje leveransegruppe har åtte nye ark og 99 originalruter: fig015_05 til fig015_09 med de øvrige Brink-gangretningene og fire gestposer, fig018_06 og fig018_07 med to Maggie-gangretninger, og fig014_10 med Bostons armgestsekvens. Alle åtte bestod antalls- og radkontrollen på første forsøk. Separate hoder, hele figurer, farger og konturer er inspisert på lys, mørk og grønn bakgrunn. filkontroll-del3.json, rutekart-del3.json og visuell-del3.png dokumenterer denne gruppen.

Fjerde leveransegruppe har fem nye ark og 92 originalruter: fig014_09, fig017_01, fig019_01, fig038_01 og fig038_02. De dekker Boston-gange og gester, Brinks skitne kostyme og Maggie-gester. Antall, radfordeling og native alfa er kontrollert. filkontroll-del4.json, rutekart-del4.json og visuell-del4.png dokumenterer gruppen. Den smale hudstripen costume019_003 er eksplisitt klassifisert som fragment etter visuell originalkontroll.

Femte leveransegruppe har sju ark med 105 originalruter. Seks er nytegnet: fig014_11 til fig014_13, fig015_10, fig018_09 og fig018_10. fig047_01 gjenbruker fig019_01 byteidentisk etter bekreftet identisk originalreferanse; original-ID-ene er koblet til kostyme 47. Visuell kontroll for duplikatet ligger i del4, øvrige i del5. filkontroll-del5.json og rutekart-del5.json gjelder alle sju.

Sjette leveransegruppe har seks nytegnede ark med 225 originalruter: fig014_14 til fig014_17, fig018_04 og fig018_08. De to siste er korrigert for riktig antall, retning og native gjennomsiktighet. Visuell kontroll på tre bakgrunner, filkontroll-del6.json og rutekart-del6.json følger leveransen.

Sjuende leveransegruppe har sju ark med 116 originalruter. Seks er nytegnet: fig015_11 til fig015_13, fig018_12, fig018_13 og fig019_02. Gangretninger, løse hoder, hodeløse kropper og håndbevegelser er visuelt kontrollert. Radene i fig015_11 er gruppert etter tre manuelt verifiserte radbånd fordi det løse bakhodet ligger høyt i nederste rad. fig047_02 gjenbruker den byteidentiske leveransen fig019_02 etter bekreftet identisk originalreferanse, med koblinger til kostyme 47. filkontroll-del7.json og rutekart-del7.json gjelder alle sju, visuell-del7.png de seks nye tegningene.

Åttende leveransegruppe har ti ark med 117 originalruter. Åtte er nytegnet: fig018_11, fig019_03, fig019_04, fig019_05, fig019_07, fig019_08, fig019_11 og fig014_18. fig047_03 og fig047_04 gjenbruker identiske 19-ark etter verifisert identisk originalreferanse, med kostyme 47-ID-er i rutekartet. Riktig antall, hodeløs oppdeling og retninger er visuelt kontrollert. De speilvendte kandidatene fig019_06, fig019_09 og fig019_10 ble holdt utenfor denne gruppen og er rettet i gruppe 9. fig019_02 og fig047_02 fikk et retningsavvik etter levering og er erstattet i gruppe 10.

Med pilotene er 475 av 509 ark levert, tilsvarende 7333 av 7 683 originalruter. 34 ark gjenstår. fremdrift.json er den løpende oversikten.

Dette er grafikkfiler for Claudes mottak. Arkene er ikke integrert i spillet, importert med gpt-inn eller kontrollert for animasjonsflimmer i motoren. Den tidligere testpakken viser fortsatt den gamle Boston-piloten.

Niende delleveranse: fig014_19, fig014_20, fig014_21, fig014_22, fig014_24, fig015_14, fig015_16, fig015_17, fig018_14, fig018_15, fig019_06, fig019_09, fig019_10, fig047_05, fig047_06, fig047_07, fig047_08, fig047_09, fig047_10, fig047_11. 20 nye ark og 425 originalruter. Tre Maggie-ark har korrigerte hoderetninger. Sju ark i kostyme 47 er kontrollert byteidentisk gjenbruk fra kostyme 19 med identiske originalreferanser. Antall, radfordeling, retninger og native alfa er kontrollert; tre bakgrunnsprøver finnes i visuell-del9-1.png til visuell-del9-3.png.

Tiende leveransegruppe: fig014_23, fig015_15, fig018_16 og fig018_17, fire nye ark med 65 originalruter. fig019_02 og fig047_02 er samtidig erstattet med korrekt venstrevendte hoder. Alle seks ark har bestått antall, radfordeling, retningskontroll og visuell native alfakontroll på tre bakgrunner. Brinks fig016_01 ble holdt utenfor gruppe 10 og er rettet i gruppe 11. filkontroll-del10.json og rutekart-del10.json gjelder de seks leverte arkene; visuell-del10.png viser de fem ulike tegningene.

Ellevte leveransegruppe: fig014_25, fig014_26, fig014_27, fig014_29, fig014_30, fig015_18, fig015_19, fig015_20, fig018_18, fig018_19, fig018_20, fig018_21, fig016_01. 13 nye ark og 239 originalruter. Brinks skadede kostyme fig016_01 bestod etter ti forsøk. Antall, radfordeling, retninger og native alfa er kontrollert. Visuell kontroll på lys, mørk og grønn bakgrunn ligger i visuell-del11-1.png til visuell-del11-3.png. filkontroll-del11.json og rutekart-del11.json gjelder kun de leverte filene. fig014_28 og fig015_21 korrigeres videre separat.

Leveransegruppe 12: fig014_34, fig014_35, fig014_36, fig015_22, fig015_23, fig015_25, fig018_24, fig018_25, fig014_28, fig015_21, fig014_32. 11 ark, 157 originalruter. Antall, radfordeling, retninger og native alfa er kontrollert. Se filkontroll-del12.json, rutekart-del12.json og visuell-del12-*.png.

Leveransegruppe 13: fig014_31, fig014_33, fig014_37, fig014_38, fig014_39, fig014_40, fig014_42, fig014_43, fig014_44. 9 ark, 168 originalruter. Antall, radfordeling, retninger og native alfa er kontrollert. Se filkontroll-del13.json, rutekart-del13.json og visuell-del13-*.png.

Leveransegruppe 14: fig015_24, fig015_26, fig015_27, fig015_32, fig015_33, fig018_22, fig015_28, fig015_29, fig015_30, fig015_31. 10 ark, 157 originalruter. Antall, radfordeling, retninger og native alfa er kontrollert. Se filkontroll-del14.json, rutekart-del14.json og visuell-del14-*.png.

Leveransegruppe 15: fig018_23, fig018_26, fig018_27, fig018_29, fig018_31, fig018_28, fig018_30. 7 ark, 75 originalruter. Antall, radfordeling, retninger og native alfa er kontrollert. Se filkontroll-del15.json, rutekart-del15.json og visuell-del15-*.png.

Leveransegruppe 16: fig018_32, fig018_33, fig018_34, fig018_35, fig018_36, fig018_37, fig016_02, fig016_04, fig016_05, fig016_06, fig017_03, fig017_04, fig017_05, fig014_41, fig017_06. 15 ark, 343 originalruter. Antall, radfordeling, retninger og native alfa er kontrollert. Se filkontroll-del16.json, rutekart-del16.json og visuell-del16-*.png.

Leveransegruppe 18: fig016_07, fig016_10, fig016_11, fig016_09, fig016_14, fig016_15. 84 tegnede figurområder, 85 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 19: fig016_08, fig016_13, fig016_21, fig016_26, fig016_27, fig016_28, fig016_30. 82 tegnede figurområder, 85 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 20: fig016_33, fig016_34, fig016_35, fig017_21, fig017_24. 63 tegnede figurområder, 64 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 21: fig017_22, fig017_25, fig017_27, fig017_28, fig017_29, fig017_30. 79 tegnede figurområder, 88 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Kostymerevisjon 22, hele bukseknær: fig016_01, fig016_02, fig016_04, fig016_05, fig016_06, fig016_07, fig016_08, fig016_09. 175 tegnede figurområder, 178 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 23: fig017_07, fig017_08, fig017_10, fig017_11, fig017_13, fig017_14, fig017_15, fig017_16. 117 tegnede figurområder, 118 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Kostymerevisjon 24, hele bukseknær: fig016_13, fig016_14, fig016_15, fig016_21, fig016_26, fig016_28, fig016_30, fig016_33, fig016_34, fig016_35. 126 tegnede figurområder, 131 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 25: fig016_16, fig016_17, fig016_18, fig016_19, fig016_20, fig016_22, fig016_23, fig016_24, fig016_25, fig016_31. 189 tegnede figurområder, 195 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 26: fig016_12, fig016_29, fig017_02, fig017_17, fig017_18, fig017_19, fig017_20, fig017_09, fig017_12, fig016_36. 192 tegnede figurområder, 194 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 27: fig055_01, fig073_01, fig188_01, fig068_01, fig262_01, fig263_01, fig114_01, fig017_26, fig017_31, fig016_32. 169 tegnede figurområder, 182 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Kostymerevisjon 28r, hele bukseknær: fig016_10, fig016_11. 29 tegnede figurområder, 29 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 28s: fig016_03, fig017_23, fig204_01, fig048_01, fig055_04, fig055_06, fig073_04, fig188_02. 175 tegnede figurområder, 184 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 29: fig068_02, fig068_03, fig068_04, fig068_05, fig068_06, fig073_05, fig073_06, fig073_07, fig204_02, fig204_03. 133 tegnede figurområder, 142 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 30: fig204_04, fig070_01, fig048_03, fig048_04, fig048_06, fig188_03. 61 tegnede figurområder, 62 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 31: fig016_37, fig073_02, fig073_03, fig055_02, fig055_03, fig055_05, fig068_07, fig263_02, fig048_02, fig048_05, fig048_07. 310 tegnede figurområder, 328 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 32: fig048_08, fig048_10, fig048_11, fig048_12, fig068_08, fig068_09, fig068_10, fig068_11, fig068_12, fig068_13, fig068_14, fig068_15, fig068_16, fig068_17, fig068_18, fig068_19, fig068_20, fig071_02, fig052_01. 189 tegnede figurområder, 194 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 33: fig104_01, fig107_01, fig107_02, fig260_01, fig137_01, fig137_03, fig137_04, fig137_05, fig173_01, fig173_02. 148 tegnede figurområder, 161 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 34: fig173_03, fig173_04, fig173_05, fig306_02, fig306_03, fig104_02, fig137_06, fig306_04. 133 tegnede figurområder, 140 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 35: fig071_04, fig071_05, fig071_06, fig052_02, fig069_01, fig138_01, fig138_02, fig223_01, fig305_02, fig305_03. 130 tegnede figurområder, 139 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 36: fig037_01, fig071_03, fig151_01, fig151_02, fig151_03. 79 tegnede figurområder, 100 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 37: fig071_01, fig048_09, fig137_02, fig305_01, fig305_04, fig059_02, fig059_03, fig094_01, fig094_04, fig072_05. 176 tegnede figurområder, 183 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 38: fig072_01, fig072_02, fig072_03, fig050_03, fig050_04, fig050_02, fig203_02, fig099_01, fig099_02, fig069_02. 122 tegnede figurområder, 138 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 39: fig178_02, fig178_03, fig178_04, fig178_05, fig178_06, fig178_07, fig178_08, fig178_09, fig178_10, fig178_11. 90 tegnede figurområder, 90 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 40: fig178_12, fig178_13, fig178_14, fig178_15, fig178_16, fig178_17, fig178_18, fig178_19, fig178_20, fig072_04. 75 tegnede figurområder, 75 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 41: fig059_01, fig094_02, fig094_03, fig203_01, fig306_01, fig178_21, fig178_22, fig178_23, fig178_24, fig178_26. 151 tegnede figurområder, 161 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 42: fig178_29, fig178_30, fig178_31, fig178_32, fig178_33, fig178_34, fig178_35, fig178_36, fig178_39, fig178_40. 52 tegnede figurområder, 52 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 43: fig262_03, fig262_05, fig230_01, fig230_02, fig230_03, fig230_04, fig230_05, fig174_01, fig174_03, fig174_05. 113 tegnede figurområder, 118 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 44: fig174_06, fig221_01, fig178_01, fig050_01, fig178_27, fig178_37, fig178_38, fig178_41, fig221_02, fig262_02. 109 tegnede figurområder, 110 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 45: fig058_02, fig058_04, fig058_05, fig058_06, fig058_07, fig058_08, fig178_25, fig178_28, fig174_07, fig174_02. 92 tegnede figurområder, 92 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 46: fig174_04, fig058_03, fig053_04, fig053_09, fig053_11, fig126_02, fig126_03, fig053_05. 152 tegnede figurområder, 164 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 47: fig214_04, fig214_05, fig214_06, fig214_07, fig214_08, fig214_09, fig214_10, fig214_11, fig214_12, fig214_14. 41 tegnede figurområder, 41 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 48: fig214_01, fig214_02, fig214_03, fig214_15, fig214_16, fig164_03, fig164_02, fig060_02, fig060_03. 92 tegnede figurområder, 92 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 49: fig053_01, fig126_01, fig164_01, fig060_01, fig199_01, fig214_13, fig262_04, fig098_01, fig126_04, fig229_04. 228 tegnede figurområder, 243 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 50: fig222_01, fig222_02, fig222_03, fig222_04, fig222_05, fig222_06, fig222_07, fig222_08. 39 tegnede figurområder, 39 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 51: fig222_09, fig222_10, fig222_11, fig222_12, fig222_13, fig222_14, fig222_15, fig222_16. 42 tegnede figurområder, 42 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 52: fig229_01, fig229_02, fig229_03, fig229_05, fig229_06, fig229_07, fig229_08, fig229_09, fig229_10, fig229_11. 42 tegnede figurområder, 42 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 53: fig229_13, fig229_14, fig229_15, fig229_16, fig229_17, fig229_18, fig229_19, fig229_20, fig229_21. 50 tegnede figurområder, 52 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 54: fig214_17, fig214_18, fig214_19, fig071_07, fig071_08, fig229_12, fig199_02, fig199_03, fig199_04. 112 tegnede figurområder, 125 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.

Leveransegruppe 55: fig213_18, fig213_19, fig229_22, fig053_08, fig222_17, fig222_18, fig222_19. 45 tegnede figurområder, 56 originaloppføringer. Originalfragmenter og mottaksbegrensninger står i notatene.
