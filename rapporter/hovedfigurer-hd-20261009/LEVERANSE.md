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

Med pilotene er 10 av 509 ark levert, tilsvarende 375 av 7 683 originalruter. 499 ark gjenstår. fremdrift.json er den løpende oversikten. fig015_02 er fortsatt under arbeid og er ikke del av denne leveransen.

Dette er grafikkfiler for Claudes mottak. Arkene er ikke integrert i spillet, importert med gpt-inn eller kontrollert for animasjonsflimmer i motoren. Den tidligere testpakken viser fortsatt den gamle Boston-piloten.
