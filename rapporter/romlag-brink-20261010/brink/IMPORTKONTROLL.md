# Lokal importkontroll av korrigert Brink

Kontrollen brukte uendret pipeline fra commit 4cff0814. Pipeline er uendret i fjern-main 0c002bd1, kontrollert 10. oktober 2026. Første historiske prøveimport av ni korrigerte ark ga 123 ruter med status ok og 12 med sjekk. fig015_05 og fig015_06 er senere erstattet som beskrevet nedenfor. Dette er isolert importdiagnostikk, ikke integrasjon eller spilltest. Native grafikkfiler og originalfiler er uendret.

## Konkret feil i hoderuten costume015_299

Kilden til fig015_11 inneholder et separat bakhode på 9 x 9 originalpiksler og 24 magenta skyggemarkørpiksler langt under hodet. Hele den synlige alfautstrekningen blir dermed 67 piksler høy. Generatoren har korrekt malt bare hodet, 53 piksler høyt i det nye arket. Prompten sier uttrykkelig at skyggemarkørene skal utelates.

myk.import_sheet måler originalhøyden med alle alfapiksler, inkludert markørene. Gruppen med den enslige hoderuten får skala 67 * 4 / 53 = 5,0566. Høyden blir 268 HD-piksler. Hodehøyden alene ville gitt 9 * 4 / 53 = 0,6792 og 36 HD-piksler. Prøveimportens snitt over union er 0,026. Dette er en påvist feil i denne lokale importen. Det er ikke bevis for at akkurat denne ruten forklarer alle Toms skjermbilder.

Bevis står i markorbevis-hode299.json. Importens foreslåtte plassering står i importkontroll-del01.json. Ikke ta denne feilskalerte hoderuten inn i en release. Claude må behandle skyggemarkørene riktig når originalhøyde, fotlinje og omriss måles. Oppdelingen på animasjon, lag og arkets rad må også vurderes mot kravet om stabil hodeskala og halsanker.

## Gange og omriss

Ni bakre gåfaser i fig015_05 og to i fig015_06 fikk sjekk for dekning. Markørene påvirker også disse målingene; markormåling-import.json viser samme plassering målt med og uten markørene. Denne ekstra målingen endrer ikke importens status eller terskler. Nye kildebundne native korreksjoner av fig015_05 og fig015_06 er nå levert. Prøveimporten av de to nye SHA256-verdiene gir 24 ok og ingen sjekk; dermed er de 11 gamle gåvarslene ikke aktuelle for de nye filene.

## Andre kontrollrunde

Ni nye eller erstattede native ark (fig015_02, 03, 05, 06, 17–21) er kontrollert med samme uendrede importer. Resultatet er 244 ok og 13 sjekk fordelt på 257 originaloppføringer. De fem gå-/vendearkene 17–21 gir 94 ok. fig015_02 har 70 hovedtegninger og to originalfragmenter: 69 ok, 3 sjekk. fig015_03 har 64 hovedtegninger og tre originalfragmenter: 57 ok, 10 sjekk. De 13 gjenstående varslene gjelder bakhoder og bakre trekvartshoder; de nye tegningene har annen detaljert silhuett enn de små originale pikselhodene. Omriss og stabil hodeskala må vurderes manuelt av Claude før integrasjon. Ingen terskler er senket eller varselstatus endret. fig015_02 har fått en ekstra native retting for å fjerne oppdiktede grå jakkekrager under tre separate bakhoder.

importkontroll-del02.json oppgir aktuelle native SHA256, målinger, skala, originalrute og lokal importstatus. Hodeskalle og hår er visuelt sammenlignet mellom munnfasene. Det er fortsatt ingen motor- eller spilltest.

## Gåark og lagdelte kropper, tredje runde

fig015_22–31 gir 162 ok og 4 sjekk i lokal prøveimport av aktuelle SHA256-verdier. fig015_26 ble rettet nativt fordi to figurer vendte feil vei, og gir nå alle 12 originaloppføringer ok. fig015_31 beholder 20 separate hoder, 12 hodeløse kropper og 6 hele figurer. De fire frontale hoderutene costume015_624, 625, 626 og 021 får sjekk for omriss/dekning (IoU0,702–0,719); de må vurderes manuelt mot godkjent ansiktsform før integrasjon. importkontroll-del03.json inneholder målingene.

Arkene fig015_12–16 er dessuten kontrollert fra den faktiske leveranseoppdagelsen og rutekartene. Disse fem arkene gir 80 ok og 0 sjekk, se importkontroll-del04.json. Disse kontrollene gjør ingen endring i kildefiler, native bildefiler eller motoren.

## Fullført standardkostyme og første mørke variantark

Seks nye ark fig015_32,33 og fig017_03,04,06,07 gir samlet168ok og3sjekk i isolert prøveimport. Standardkostymet har nå33grafikkreviderte ark. fig017_03 har102tegnede hoder og ett ekte originalfragment. De tre varslene gjelder hoderutene costume017_128,154,169 (IoU0,716–0,767, dekning0,750–0,772), og krever manuell vurdering hos Claude. Tallene i importkontroll-del06.json gjelder de faktiske leverte SHA256-verdiene.

fig017_01,02 og05 holdes tilbake lokalt på grunn av palett, antall/oppsplitting eller oppdiktet skade i forsøkene. De gamle jobbfilene er bevart. Et teknisk riktig radantall er ikke alene nok til grafikklevering.

## Samlet leveranseoppdagelse for alle33standardark

En samlet prøveimport fra den faktiske leveranseoppdagelsen og rutekartene finner alle33reviderte standardark med aktuelle SHA256. Resultatet er626ok og18sjekk over644originaloppføringer. De18varslene er de allerede beskrevne13bakre hodeomrissene,4frontale hodeomrissene og den påviste feilskaleringen av costume015_299. Ingen nye varsler kom til fra fig015_32 eller33. Full rapport står i importkontroll-standardkostyme-33ark.json. Dette bekrefter filruting i den isolerte importen, ikke motorintegrasjon eller spilltest.

## Knelebevegelser, gester og vendinger

Åtte nye ark fig017_10–17 gir 133 ok og ingen sjekk i isolert prøveimport, se importkontroll-del07.json. fig017_12 beholder originalens to celler med separat hode og hånd/underarm. Delene er koblet per originalcelle uten pikselendring. De hodeløse kroppene i fig017_10,13,14,15,17 er beholdt hodeløse. fig017_17 har faktisk fire komplette figurer og 18 hodeløse kropper; et feil delantall i prompten er dokumentert i visuell-kontroll.json, og bildet er kontrollert mot de faktiske kildedelene.

## Videre kontroll hos Claude

Importer reviderte SHA256-verdier og rutekart etter at markeringsproblemet er rettet. Kontroller ståing, gange og tale i alle retninger med felles hodeskala og anatomisk halsanker, deretter z-masker og opptegning når figuren går. Rektangulære artefakter i Toms skjermbilder er fortsatt ikke bevist løst av grafikkrevisjonen.
