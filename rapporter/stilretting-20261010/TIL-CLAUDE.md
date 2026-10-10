# To avviste råforsøk og ny stilprøve

Begge vedleggene fra Toms stilavvisning er nå sporet til registrerte råforsøk. Se `kildekontroll.json` for native sha256, identisk alfa og maksimalt komposisjonsavvik på 1/255. Begge er allerede tilbakeholdt og skal fortsatt ikke importeres automatisk.

- `fig103_02`, forsøk 1: mangler tre reelle faser i midtraden. Kilden har et svært smalt varmt fargeområde over nesten hele figuren og oppgir ingen figuridentitet. Avklar actor/kostyme, faktisk palett og eventuelle effektlag i originalspillet. Ikke utled grått hår, oransje skjorte eller beige bukse fra den genererte kandidaten. Det er ikke bevist at palettvalget i pipelinen er feil.
- `fig170_04`, forsøk 1: den store blå plattform-/oppløsningseffekten er borte. Originalen viser bare en liten del av en figur omgitt av effekten. To hele flygende menn kan ikke brukes som erstatning selv om antallet deler er to.
- De sterke røde og gule prikkene i vedleggsvisningen ligger hovedsakelig ved alfa 1/255. Vanlig komposisjon på lys, mørk og grønn bakgrunn viser dem ikke som sterke prikker. Ingen motorkonklusjon eller restalfasletting er gjort.

`boston-stilprove.png` er én avgrenset stilprøve med pose fra det navngitte `costume014_289`, med konseptet og den direkte godkjente Boston-prøven som autoritet. Den erstatter ingen eksisterende leveranse. Den skal ikke legges i fremdriftsfilene eller importeres som et komplett ark. Tom vurderer prøven før serieproduksjon fortsetter. Native PNG/alfa er bevart byteidentisk; spillets import, fotpunkt, okklusjon og animasjon er ikke testet.

Ingen kode, originale jobbfiler, status.csv, RAPPORT.md eller retur.md er endret av grafikeren.
