# Restgrafikk r20, arbeidsrunde 17. oktober 2026

221 manglende HD-ruter er laget som en arbeidskandidat oppå publisert r19, hd-mod 630cadb3. De består av 196 dørfaser og 25 selvstendig tegnede figurruter. Alle 221 er observert i den native motoren. 561 fullomtegningskontroller etter oppstart gir null avvik. Hele restgrafikken og gjennomgangen av eldre figurfeil er fortsatt uferdig. Runden er ikke integrert i hd-mod eller pakket som distro.

## Dørene i Nexus

Kostyme 62, 63, 64, 65 og 66 har henholdsvis 25, 39, 47, 66 og 19 nye ruter. De er utfoldingen av dørene til museum, kart, gravkammer, planetarium og katedral i rom 23. Originalskriptene dokumenterer palett 1, 0, 2, 3 og 0. Kodek 5 bruker kodene direkte som rompalettindekser.

Åtte valgte native ark gir 91 referanseposer med malte materialer og lys. De øvrige fasene gjenbruker disse tegningene med begrenset bevegelsesregistrering, originalens grove lys og farger og glatt polygongeometri. 196 eksportfiler betyr derfor ikke 196 selvstendige nytegninger. Tynne lyslinjer beholder åpne polygoner. Små lukkede gjennomsiktige ditherhull under åtte originalpiksler fylles, mens reelle åpninger beholdes. Polygonforenklingens toleranse er 0,55 originalpiksel. Laveste silhuettoverlapp mot den kantete originalmasken er 0,7863. Dette er hjelpemål, ikke Toms kunstneriske godkjenning.

Første råforsøk gjorde noen glimt til stein eller røyk. Disse brukes ikke som eksportankere. Nye lysark og originalregistreringen holder lysfasene adskilt fra stein. Råforsøk er bevart og merket som ubrukte i fremdrift.json. Alle native tegninger er laget med innebygd image_gen; verktøyet oppgav ikke modellnavn. Eksakte prompter ligger i prompter-filene.

## Personene i canyon

De 25 nye rutene i kostyme 34 viser Boston, Maggie og Brink i canyon-sekvensen der Boston hjelper Brink opp. Dette er ikke undersøkelsen av en død Brink. Den første muntlige identifiseringen i samtalen var feil og ble rettet før tegning. Rom 15, lokal skript 2010 og animasjonene 6 til 9 er kildegrunnlaget.

Arbeidsoversiktens RGBS-farger var misvisende. Originalen er lest gjennom AKPL og rom 15, palett 0, uten å endre de fysiske pikselindeksene. Alle tre hovedarkene som Tom godkjente 15. oktober er brukt i hver generering. SHA256 står per rute i canyon-registration.json. Boston har grå tinninger og mørk skjorte, Maggie svart bob og oransje drakt, Brink blondt hår og grå jakke. Ingen solbriller eller fotorealistiske ansikter er lagt til.

Hver fysisk rute er tegnet og tilpasset som én samlet enhet med native alfa. Hoder er ikke klippet ut eller skalert separat. Syv poser er tegnet om enkeltvis for å bevare kroppsstilling, grep og tilsiktet avskårne kroppsdeler. En ekstra to-ruters reparasjon ble forkastet fordi den krysset rutegrenser. Den første kontrollen brukte et for strengt mål for samlet sideforhold. Sluttkontrollen måler i stedet hvert akseavvik fra én felles skala, som eksisterende fit_scales, med grense 12 prosent. Laveste silhuettoverlapp for sluttresultatet er 0,6970. Visuell godkjenning gjenstår.

## Motortester og begrensninger

Fem komplette Nexus-animasjoner viste først 191 nye ruter. To tilleggskjøringer i en annen retning og plassering viste de fem resterende små lysfasene. Alle 196 er dermed observert. Det var null omtegningsavvik i 303 kontroller etter oppstart. En tidligere eksport med annen alfa og startkontrollene er bevart som diagnostikk, men regnes ikke som sluttkontrollen.

Fire isolerte personanimasjoner viste alle 25 nye ruter og ga 172 kontroller uten avvik etter oppstart. Etter siste tre tegningsrettinger ble animasjon 8 prøvd igjen med hele figuren synlig, med 86 kontroller uten avvik. Alle endrede ruter ble observert på nytt. De seks rutene i animasjon 9 har samme SHA256 som i forrige beståtte prøve.

Canyon-romhopp med tre testlagringer ble sendt videre til andre rom av originalskriptene før aktøren ble satt inn. Dette er ikke godkjent naturlig scenetesting. De isolerte figurprøvene er derfor kjørt i rom 23. Alle brukte karakterfarger er kontrollert byteidentiske mellom rom 15 og 23, palett 0; se canyon-palette-proof.json. Skjermbildet canyon-i-motor.png viser denne isolerte prøven, ikke canyon-bakgrunnen. Vanlige brukerlagringer og innstillinger er ikke endret. Full gjennomspilling og naturlige overganger gjenstår.

## Eldre feil som fortsatt må rettes

Motorbildene viste at flere allerede publiserte ruter i kostyme 34 bruker feil personer og klær. Eksemplene costume034_050_hd.png og 108 er bevart som eldre-figurfeil-bilder. Disse er eldre filer, ikke en palettfeil i de nye rutene. De 100 tidligere HD-rutene i denne serien må gjennomgås samlet og de gale tegnes om. De er ikke automatisk erstattet eller regnet som rettet i denne leveransen. Serien er derfor ikke visuelt sammenhengende gjennom hele handlingen ennå og skal ikke omtales som ferdig.

## Filer og bevaring

mod-tillegg inneholder 442 nye filer, med 221 HD-bilder og 221 indeksbilder. ADDITIONS.json er SHA256-manifestet. Ingen publiserte filer er erstattet eller slettet. Alle 44 551 eksisterende manifestfiler og alle 55 HD-filmer er uendret. Alle nye indeksbilder har de opprinnelige pikselverdiene. Beskyttede jobbfiler, stilankere og hovedark er uendret. integrity.json dokumenterer kontrollen.

Råinventaret har nå 6 723 ruter uten HD. Etter utskilling av de samme 712 bekreftede palettmaskene gjenstår 6 011 faktiske bilder i arbeidskandidaten, pluss gjennomgangen av eldre feil. remaining.json inneholder neste arbeidsliste. Tellingene følger samme jobbinventar som r19; de er ikke et bevis for at alle ubrukte fysiske data i spillfilene er nåbare i spillet.

Registrering og kontrollverktøy ligger i verktoy. De bruker eksisterende ScummVM, dighd.myk, fasegeometri og kontrollkroker. Ingen motor- eller pipelinekode er endret. fremdrift.json skiller brukte native ankere, ubrukte forsøk, avledede faser og selvstendige tegninger. Teknisk kontroll er ikke Toms visuelle godkjenning.

Bibliotekskilder: figurark-fast-storrelse, logg-over-det-som-mangler-hd og publisert-mod-er-fasit. PASS i bibliotekets opphav er fulgt opp med målprosjektets gjeldende aktørskala, fysiske indekskontroll, faktisk rutedekning og bevaring av publisert r19.

## Neste

Fortsett gjennomgangen av de 100 eldre canyon-rutene først, særlig overgangen mellom eldre gale personer og de nye godkjente identitetsreferansene. Fortsett deretter remaining.json, med motiv, palett og skript avklart før hver serie. Integrasjon må bruke publisert hd-mod som grunnlag og bare legge til deklarerte filer, med eksplisitte erstatninger når eldre grafikk faktisk er rettet.
