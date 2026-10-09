# Til Claude: 201 nye Boston-ruter med godkjent glatt stil

Tom har direkte godkjent den nye stilretningen i samtalen og bestilt resten av Boston-piloten. fig014_02, fig014_03 og fig014_04 er levert som resultat.png og notat.md, totalt 201 ruter. Nye særskilte stilprompter er dokumentert. Originale jobbfiler er uendret.

## Velg det nye settet konsekvent

Bruk det glatte 28-ruters stilarket i rapporter/boston-konsept-glatte-kanter-20261009/boston-28-ruter.png som ark 1 sammen med de tre nye arkene. Den gamle jobber/fig014_01/resultat.png og den gamle installerte testmodden er bevart. Ikke bland den gamle pikselkonturen med de nye glatte tegningene og kall settet ferdig.

| Ark | Kilde | Antall |
| --- | --- | --- |
| 1 | rapporter/boston-konsept-glatte-kanter-20261009/boston-28-ruter.png | 28 |
| 2 | jobber/fig014_02/resultat.png | 62 |
| 3 | jobber/fig014_03/resultat.png | 127 |
| 4 | jobber/fig014_04/resultat.png | 12 |

## Bevar de nye konturene

Tidligere rapport i rapporter/boston-konsept-glatte-kanter-20261009/TIL-CLAUDE.md dokumenterer at finish_cels bruker gpt._with_alpha, som legger originalens NEAREST-maske i 4x over resultatet. Motorens kSrcCel-komposisjon har hard alfagrense 128. Disse forholdene er ikke rettet av grafikeren.

Det nye arket har egen antialiasing i RGBA. Behold den gjennom tilpasning og eksport. Ikke erstatt den med originalens trappetrinn, og ikke gjør alfaen binær for å bestå den gamle omrisskontrollen. Riktig blanding mot scenen bak må løses i mottak og motor.

## Rektangler, skala og identitet

rutekart.json knytter alle 201 figurområdene til originale rute-ID-er etter rad og plass. drawn_bbox_alpha128 angir målt figurgrense, og bbox_with_2px_margin er bare et diagnostisk utsnitt. Alfa under 128 kan ligge utenfor denne boksen. Filen angir også omfanget av svak alfa utenfor boksene. Bruk hele native filen ved tilpasning og kontroller kantene før eksport.

Ikke behandle rutekartet som et nytt jobb.json eller som en fasit for ferdige ankerpunkter. Originalens rute-ID-er, indeksbilder, scripts, rekkefølge, paletter, hodelag og gangoppførsel skal bevares.

Ark 4 er omtrent 370 piksler høyt per figur på lerretet. Dette er større enn de gamle rutene i 4x. Også hodene og flere gangruter har endret kontur og plassering. En blind beskjæring med gamle rektangler vil kutte motivet eller hente feil rute.

## Test ved import

1. Tilpass først én hel figur og ett separat hode mot originalens størrelse, anker og fotfeste.
2. Vis mot lys og mørk bakgrunn i motoren. Bekreft at glatte kantpiksler faktisk blandes med bakgrunnen.
3. Kontroller lag foran figuren, hodefeste på stående kropper, palettbytter og originale skygger.
4. Spill de opprinnelige 12-ruters gangrekkene og snakkehodene i normal fart. Sjekk at munnfase, arm/benfase, overgang og høyde er riktig, uten flimmer.
5. Test HD/klassisk-bytte og klikkgange. Grafikkfilenes antallskontroll er ikke en motor- eller gameplaytest.

## Status

Antall, retninger, filformat, native alfa og visuell filvisning er kontrollert. Posefasenes nøyaktighet, ankere og animasjon i motoren er ikke verifisert. De nye tre arkene er ikke gpt-inn-godkjent, installert eller godkjent som spillresultat av Tom. Claude gjør kode og tilpasset import; Tom vurderer spillets utseende.

Stilgodkjenningen gjelder denne Boston-piloten. Den bestiller ikke automatisk flere kostymer, lagjobber eller ikonark.
