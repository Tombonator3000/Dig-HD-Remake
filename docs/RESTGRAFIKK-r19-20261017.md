# Restgrafikk r19, 17. oktober 2026

Tom ba om å integrere den produserte restgrafikken, hente repoendringer og legge den i en ny distro. Data-PR66 er flettet til `hd-mod` 630cadb3ebb398ac8ade1f4e1ea759f8a783cd5a. Grafikkgrunnlaget er `gpt-arbeid` f5a23834, rapporten `rapporter/restgrafikk-r19-20261016`.

## Integrasjon

Modflett tar utgangspunkt i publisert r18, 4a0ab61e. Den legger til 14 173 filer med 7 097 HD-ruter og erstatter bare to eksplisitt dokumenterte Maggie-bilder. Ingen publiserte ressurser slettes. Alle 55 komprimerte HD-filmer og deres metadata er uendret. Grafikk, indeksbilder og mastere ligger bare i datagrenene.

Antallet HD-ruter inkluderer tekniske småfragmenter og kontrollert gjenbruk. Det betyr ikke 7 097 selvstendige nytegninger. Alle 7 076 nye indeksbilder er kontrollert for uendrede fysiske pikselindekser. Samtlige tillegg matcher SHA256-manifestet i grafikkrapporten. 30 378 publiserte manifestfiler er bevart med to tilsiktede HD-erstatninger og oppdaterte rotmetadata.

Kandidatens nye serier omfatter romdrakt, robotarm, Nexus og Eye, portretter på håndcomputeren, krystaller, Maggie i laboratoriet, biblioteklys, lyn, Boston i vannet, trikkapsler, rotte/felle og Brink med spade. Se grafikkrapporten for nøyaktige metoder, kildepaletter og begrensninger per serie.

## Kontroller

Alle 394 nye kapselruter, 194 rotte-/felleruter og 15 Brink-ruter ble observert i isolerte motortester under produksjonen. På den ferdig integrerte modden ble Brink46 (15 ruter), kapsel270 (30), rotte183 (37) og Maggie331 (52) observert uten avvik mellom løpende skjermbuffer og full omtegning. Et første Maggie-hopp gikk til feil rom og så ingen ny grafikk; det teller ikke som vellykket figurtest. Riktig rom 111 er kontrollert separat.

En gjenbrukskontroll fant 25 identiske originale tegninger som kunne bruke eksisterende HD. 24 ble observert i motoren; beinfragment 212_002 er fortsatt ikke observert. Elleve andre treff ble avvist fordi HD-figurens klær avvek fra pilotarket.

822 trikkeruter er bekreftede palettmasker i originalskriptene og motoren, ikke røde kapseltegninger. 712 av dem mangler selvstendige HD-filer og beholdes i råinventaret, men skal tegnes av motoren som paletteffekter. De er ikke telt som nytegnet kunst.

## Linux-pakke

Linux-kjøring 39027347179 er fullført med grønn motorbygging, oppstartskontroll og Debian 12-test. Pakken bruker kode c2c9b8e0 og den integrerte modden. Den faktiske releasefilen er lastet ned og SHA-256 er kontrollert mot både sjekksumfilen og GitHubs digest.

AppImage: 2 123 475 448 byte, SHA-256 47b04c1bc468cb4dccd35cc33a6241504ea0cefaac6b87d144cd963c652c9b7a. Alle 44 551 mod-manifestfiler stemmer, inkludert alle 14 173 tillegg og to erstatninger. Ingen modfiler ligger utenfor manifestet. Alle tidligere ressurser, inkludert 55 filmer, er bevart.

AppRun er startet med standardinnstillinger i egne XDG-testmapper. Intro, tekst og HD/klassisk-bytte er kontrollert over 550 oppdateringer; fem omtegningskontroller gir null avvik. En tvungen vindus-/surfacesdl-test feilet før spillinitialisering i den lokale hodeløse SDL-driveren. Den ordinære AppRun-oppstarten og CI-testene består; den tvungne varianten er bevart som en mislykket diagnostisk test. Ingen vanlige lagringer eller innstillinger er endret.

Det tidligere GPL-kildearkivet var fra r16 og manglet patch 0007. Nytt kildearkiv inneholder den eksakte låste ScummVM-kilden med gjeldende patchstakk og byggeoppskrift, uten spilldata eller HD-bilder. Arkivet er kontrollert mot lokal motor før pakking og lagt i samme Linux-release. SHA-256: b3d35f9ac36c6e227426bb9044317797a01e04c1e5db23f78f8206f675826dfd.

## Gjenstående arbeid

Grafikkproduksjonen er ikke ferdig. Råinventaret har 6 944 originalruter uten HD. Etter utskilling av de 712 bekreftede palettmaskene gjenstår 6 232 faktiske bilder. Eldre HD-figurer med feil klær, identitet eller hodeplassering krever gjennomgang i tillegg. Teknisk kontroll er ikke Toms visuelle godkjenning eller en full gjennomspilling.

Ingen motor- eller pipelinekode er endret i denne integrasjonen. Eksisterende motorpatcher og alle tidligere r18-rettinger beholdes.

Bibliotekskilde: [Publisert mod er fasit](https://github.com/Tombonator3000/prosjektbibliotek/blob/main/losninger/bygg/publisert-mod-er-fasit.md). Den eksisterende modflett-implementasjonen er gjenbrukt, med eksplisitte erstatninger og kontroll av alle tidligere sjekksummer.

Pakkens egen motor, spilldata, mod og biblioteker er også brukt direkte via AppRun til isolerte figurtester med kopierte testlagringer: Brink46 15, Maggie331 52, kapsel270 30 og rotte183 37 ruter. Alle fire tester består uten omtegningsavvik. Testene bruker egne XDG-mapper.
