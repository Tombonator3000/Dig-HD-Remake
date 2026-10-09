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

Med pilotene er 166 av 509 ark levert, tilsvarende 3191 av 7 683 originalruter. 343 ark gjenstår. fremdrift.json er den løpende oversikten.

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
