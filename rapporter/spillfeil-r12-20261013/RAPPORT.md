# The Dig HD r12: rettinger og metodeanalyse

Brukerens rapporterte HD-feil er undersøkt mot originale ressurser, romskript, paletter og faktisk avspilling. Nye og korrigerte bilder leveres gjennom `mod-overrides` og den komplette `hd-mod`-grenen. Publiseringsstatus og nøyaktige pakkehashverdier føres i `LEVERING.md` og `DELIVERY.json` etter pakkeprøven. Dette er ikke en påstand om at hele spillet nå er ferdig HD eller gjennomspilt.

## Rettet i denne leveransen

- Boston: 23 ruter ved krystallplukking, samt 94 ressurser i hule-/lommelyktfamilien, med skillet mellom 62 tegnede ruter og 32 optiske masker/markører dokumentert.
- Brink: manglende handlingsfamilier 310/312, 709 eksplisitt retningskoblede hoder for normal ståing/gange/tale i 15/16/17 og korrekt syk palett i 16/17. De underliggende indeksbytes er bevart. Hender følger originalens varme farge i rom 105; dette er kontrollert, ikke glemt. Øvrige spesialhoder er bevart fra r11 og ikke erklært ferdig nykontrollert.
- Alle fem brobryterfamilier: tydelige krystaller uten den tidligere store blobskyggen. 66 små lysfaser som feilaktig ble behandlet som tekniske er lagt tilbake og faktisk observert i motoren.
- Lys/energi: egne originalfaser for diaset og linserommets krystallfelt. Kvinner, klær og fartøy brukes ikke som motiver. Den brede175-fasen er rekonstruert som ett 281×145-bilde og delt på originalens256 + 25-grense; høyrebiten blir dermed ikke et nytt svevende objekt.
- Hole/lens: ti registrerte objekttilstander, inkludert den lille optiske linsen238. Fire platåutsnitt er rettet mot samme rommaster.
- Luftsluse: synlig rute074_004 er produsert. Motoren bevarer både HD-figur og bakgrunn når originalens glassmaske skyggelegger dem.
- Museumsspiret: eksisterende nytegnet panorama er satt inn som mykt parallaxlag; synlig side av originalens skjulingskant er avtrappet. Den smale gulvåpningen finnes også i originalen og beholdes.
- PDA: 18 tilstander fra ni paneltegninger, med eksakt original objektdekning. Svart palettindeks er ikke lenger feilaktig tolket som gjennomsiktig, og objekter med eksakt maske har riktig prioritet over rommet.

Sparks: Det grove synlige feltet satt i objekt 187_01, ikke i den aktive partikkelkostymen 61. Objektlaget er rettet med nøyaktig SMAP-dekning og kontrollert i brukerens faktiske nyere save6 gjennom 480 bilder. De diagnostiske 61-erstatningene er tilbakeført. Tidligere r11-rettinger for inventory, blå staver, roterende krystaller og vann/bølger er med videre. Dørene i den første feilrapporten leder til to forskjellige originalrom 94/95; spillforbindelsene er uendret.

## Hva vi lærte av Sam & Max

`SAM-MAX-METODESAMMENLIGNING.md` sammenligner konkrete kildefiler og bilder ved låste revisjoner. Den støtter inntrykket av bedre presisjon i Sam & Max-produksjonen: godkjent identitet før serier, samlede panoramaer, lokale tilstandsfamilier, kontroll av små lysgrupper og faktisk visuell avvisning selv når målingene passerer.

Disse grepene ble brukt direkte i r12: den første Brink-importen ble forkastet, retningskoblingen ble gjort eksplisitt, energifaser ble knyttet til den enkelte originalform, og flere små lysglimt ble hentet tilbake. The Dig beholder sitt eget malte uttrykk. Sam & Max har foreløpig ikke tilsvarende import-/pakke-/spilltest for de undersøkte nye bildene, så rapporten hevder ikke at resultatet er bedre gjennom hele spillet.

`METODE-FRA-NAA.md` beskriver arbeidsmåten og nødvendig importsteg ved neste ombygging. Rapportmappens overstyringer blir ikke automatisk hentet av den gamle `gpt_runde.sh`; den komplette publiserte modden og manifestet er leveringsgrunnlaget.

## Kontroll og begrensninger

Motorrettingene er i PR 51. 42 lokale pipeline-tester og 15 nettlesertester har bestått, og hele motorpatchen er kontrollert mot låst ScummVM-kilde. De berørte rommene og originalanimasjonene er kjørt med kontroll mot full nytegning. Bilder av både avviste og endelige kandidater er bevart slik at teknisk pass ikke forveksles med visuell riktighet.

`DEKNING-R12.md` er en avgrenset kontroll av de rapporterte familiene. 22 mørke fragmenter i eldre lens-familier har ingen sikker feilklassifisering; de er uttrykkelig merket som visuelt uverifisert ved alle palettilstander. Filer som er tomme, tekniske masker og mørke bakgrunnsfragmenter behandles ikke som samme feiltype.

Testene bruker kopierte lagringer. Brukerens aktive save 0 og 6 ble oppdatert under arbeidet og er ikke skrevet tilbake eller overskrevet av testene. Full gjennomspilling og Toms endelige visuelle godkjenning gjenstår. Windows-kontroll skjer gjennom Wine 10; fysisk Windows er ikke tilgjengelig i denne kontrollen.
