# R20 og r21 integrert i spillet, 18. oktober 2026

PR67 er flettet til hd-mod29cff6583dc45ec21bcccb5da0eb16afafa379a5. Lokal hd-leveranse er oppdatert med fast-forward pull. kjor-rettet-spill.sh bruker denne mappen, så lokal spillstart har grafikken fra begge rundene.

## Innhold

- 221 nye HD-ruter: 196 Nexus-dørfaser og 25 canyon-ruter fra r20.
- 105 omtegnede canyon-ruter fra r21, etter godkjente personark. De 105 indeksbildenes palettreferanse er rettet uten endring av opprinnelige kodeverdier.
- 442 nye filer og 210 eksplisitte erstatninger i 105 kostymeenheter. Ingen filer slettet. Øvrig r19-grafikk og alle 55 HD-filmer er bevart.
- 44 993 manifestfiler og 652 leveransefiler kontrollert etter pull. Kandidat, PR og publisert mod har identiske leveransefiler.

## Kontroll

11 native motorprøver på den sammenslåtte modden viser alle 196 nye Nexus-faser og alle 130 canyon-ruter. 543 fullomtegningskontroller etter oppstart har null avvik. Feilsøkingsmeldinger ved første kunstige romhopp inngår ikke i dette tallet. Naturlig canyon-inngang, alle overganger og full gjennomspilling er ikke testet. Se qa-integrated.json, motorlogs.json og de tapsfritt komprimerte motorloggene.

[Canyon i motoren](canyon-8.png). [Nexus i motoren](nexus-64.png).

Eksisterende modflett og publiseringsvern er brukt etter prosjektbibliotekets publisert-mod-er-fasit. Se integration.json, payload.json og published-check.json. Alle utenforliggende filer er bevart. Ingen motor, pipeline, hovedark eller beskyttet jobbfil er endret. Innledende sammenslåing stoppet på metadata som var kostymenavn og ikke tall; oppskriften er korrigert før modflett og publisering.

Linux-bygg39112677913 fra kode7b2f4398 bruker fast publisert mod29cff6583. Byggingen, pakkestarten/grafikkvalget og Debian12-prøven er grønne. Den faktiske nedlastingen er kontrollert: 2140813816 byte, SHA-256 f6c9786ca4f0ebb5f980e1761c79151e643d68a619f7cb0c37aff7b5f3cbe326. Alle 44 993 mod-manifestfiler og 652 leveransefiler stemmer. Standard AppRun med intro, tekst og HD/klassisk-bytte består 550 oppdateringer og fem nytegningskontroller. Pakkens egne 11 native prøver viser alle 196 nye Nexus-faser og alle 130 canyon-ruter, med 543 kontroller etter oppstart uten avvik. Se kontroll-linux.json og [canyon-ruten i pakken](canyon-package.png). Gjeldende kildearkiv er kontrollert mot uendrede motorpatcher, se source-unchanged.json.

All restgrafikk er ikke ferdig: 6 011 faktiske bilder og øvrige eldre figurfeil gjenstår. Toms visuelle godkjenning av alle nye ruter gjenstår. Testene bruker isolerte mapper og kopierte lagringer.
