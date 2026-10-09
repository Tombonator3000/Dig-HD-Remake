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

Med pilotene er 29 av 509 ark levert, tilsvarende 765 av 7 683 originalruter. 480 ark gjenstår. fremdrift.json er den løpende oversikten.

Dette er grafikkfiler for Claudes mottak. Arkene er ikke integrert i spillet, importert med gpt-inn eller kontrollert for animasjonsflimmer i motoren. Den tidligere testpakken viser fortsatt den gamle Boston-piloten.
