# Lokal importkontroll av korrigert Brink

Kontrollen brukte uendret pipeline fra commit 4cff0814. Pipeline er uendret i fjern-main 0c002bd1, kontrollert 10. oktober 2026. Ni korrigerte ark ga 123 ruter med status ok og 12 med sjekk. Dette er isolert importdiagnostikk, ikke integrasjon eller spilltest. Native grafikkfiler og originalfiler er uendret.

## Konkret feil i hoderuten costume015_299

Kilden til fig015_11 inneholder et separat bakhode på 9 x 9 originalpiksler og 24 magenta skyggemarkørpiksler langt under hodet. Hele den synlige alfautstrekningen blir dermed 67 piksler høy. Generatoren har korrekt malt bare hodet, 53 piksler høyt i det nye arket. Prompten sier uttrykkelig at skyggemarkørene skal utelates.

myk.import_sheet måler originalhøyden med alle alfapiksler, inkludert markørene. Gruppen med den enslige hoderuten får skala 67 * 4 / 53 = 5,0566. Høyden blir 268 HD-piksler. Hodehøyden alene ville gitt 9 * 4 / 53 = 0,6792 og 36 HD-piksler. Prøveimportens snitt over union er 0,026. Dette er en påvist feil i denne lokale importen. Det er ikke bevis for at akkurat denne ruten forklarer alle Toms skjermbilder.

Bevis står i markorbevis-hode299.json. Importens foreslåtte plassering står i importkontroll-del01.json. Ikke ta denne feilskalerte hoderuten inn i en release. Claude må behandle skyggemarkørene riktig når originalhøyde, fotlinje og omriss måles. Oppdelingen på animasjon, lag og arkets rad må også vurderes mot kravet om stabil hodeskala og halsanker.

## Gange og omriss

Ni bakre gåfaser i fig015_05 og to i fig015_06 fikk sjekk for dekning. Markørene påvirker også disse målingene; markormåling-import.json viser samme plassering målt med og uten markørene. Denne ekstra målingen endrer ikke importens status eller terskler. Nye kildebundne bildekorreksjoner er under arbeid der omrisset fortsatt avviker.

## Videre kontroll hos Claude

Importer reviderte SHA256-verdier og rutekart etter at markeringsproblemet er rettet. Kontroller ståing, gange og tale i alle retninger med felles hodeskala og anatomisk halsanker, deretter z-masker og opptegning når figuren går. Rektangulære artefakter i Toms skjermbilder er fortsatt ikke bevist løst av grafikkrevisjonen.
