# Toms spillfunn, 13. oktober 2026

Tolv originale vedlegg er bevart uendret med SHA-256. De beskriver feil, og skal ikke brukes som motivanker. r10 er sammenligningsgrunnlag. Lagringer og innstillinger er kopiert til isolerte tester.

- Blå staver: kostyme 298 og 299 i rom 100. Begge har to kilderuter, men bare rute 000 har HD. De to rutene har samme mål; formoverlapp er 99,97 prosent og 100 prosent, bare 14 og 13 originalpiksler endres. Samme fysiske stav i en annen lysfase. Eksisterende korrekt HD-stav skal derfor gjenbrukes i rute 001, med riktig originalindeks og palett. Ingen ny designvariant.
- Luftsluse: rom 25. Den store pikselerte flaten følger kostyme 75. Dette er to ensfargede tekniske skyggemasker, ikke selvstendig trappegrafikk. De skal skyggelegge HD-bakgrunnen gjennom originalens palettfunksjon. Kostyme 74 er selve slusen og inneholder også tekniske farge-/skyggemasker; disse er ikke orange glassdører. Bare synlige deler produseres som motiv, tekniske masker skal beholde sin funksjon.
- Krystallgeometrier: rom 97, kostyme 286 til 289, fire separate roterende geometrier. Det er andre ressurser enn kostyme 319 med 15 krystaller i rom 50. Gul/orange kant i de roterende originalrutene er bakgrunns-/overgangsflate, ikke en tykk beige steinramme rundt en krystall. Kontroller riktig rompalett og skygge-/tegnemodus før ny produksjon.
- Inventory: Feilen er gjenskapt fra lagring5. Ved xstart416 ble bufferområdet feilaktig klippet mot pitch328. Klipping mot det synlige vinduet retter HD-visning og gjentatt åpning. Original lagring er uendret.
- Vann/bølger: rom 101, kostyme 301. Av 24 faser finnes bare én HD-rute. Kystlinje, skum og vanntekstur skal følge originalens bevegelse og tempo; ingen endring av gangflater.
- Lys/energi: Toms siste to bilder viser et påvist feil motiv. Ressursen er bekreftet som kostyme35 i rom15 fra originalskript og bildeavtrykk. Klær, belte, røyk og grå steinformer skal ikke være motivanker for rettingen.
- Sparks og lens-rom: originale rom-/kostymeressurser og riktig palett kartlegges. Energi skal være lys og elektriske utladninger med originalens forløp.
- Dører i bilde 3 til 5: bilde3 viser dør183 til rom94; bilde4 viser175 til rom95. Originale script og objektrom-tabellen bekrefter ulike transportrom. Bilde5 matcher rom95. Forbindelsene beholdes.

## Korrigert grunnlag for kostyme 75

Rå eksport har bare én ikke-transparent indeks og er rød i kildepaletten. Dette er en teknisk palett-/skyggemaske. Den skal ikke tegnes som fysisk arkitektur. Motoren skal bevare HD-flaten under masken og anvende originalens skyggemapping. Tidligere antakelse om en separat trapp er forkastet før produksjon.

Lagring 5 er kopiert fra brukerens save-mappe med SHA-256 4f89566a2daec02f35060983f8e42d9b4c908de7b1deb0a3aead2004dc0500a4. Testing skjer med kopien.
