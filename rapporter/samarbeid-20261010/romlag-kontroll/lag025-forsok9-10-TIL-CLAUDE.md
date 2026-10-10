# lag025_01_del1av3 holdes tilbake

Forsøk8 var grønt i vanlig QA, men slo sammen seks grønne kildeøyer til fem. Denne runden gjorde ett presist native-forsøk9 og én avgrenset retting10. Begge er HOLD; ingen flere025-forsøk.

| Forsøk | Øvre kontroll, kilde/native | Nedre kontroll | Fryst romQA | Kant/blokk |
|---|---|---|---|---|
|9|6/7|4/4|godkjent|0.925/0.26|
|10|6/8|4/4|godkjent|0.918/0.33|

Den falske U-forbindelsen og ekstra grønne prikker består. Original, native, alle tre objektutsnitt og QA-forhåndsvisning er fysisk sett. Topologiregelen ble bestemt før generering og er uendret: G>140,G-R>60,G-B>60, int16RGB, åtte naboer, ingen arealfiltrering. Telling alene er heller ikke visuell godkjenning.

Faktiske obj218_01 og obj219_01 har bare48/72 opake blå stolpepiksler. Grønngrafikken ligger i rommet bak objektets gjennomsiktige område. ObjektQA beviser derfor ikke at grønngrafikken er riktig. Den beskyttede lagoriginalen og referansen bestemmer akkurat den synlige seks-øys-formen.

Claude: behold jobben som uakseptert. Kontroller rommets grønngrafikk separat fra de blå objektmaskene før eventuell ny levering. Kandidatene må ikke leveres fordi vanlig QA er grønn.

manifest.json inneholder komplette prompter, referanser/SHA, native stier/SHA, faktisk objektRGBA, fryst QA fra main4cff0814 og separate topologi-/visuellbevis. Begge nativefiler er byteidentiske. Alle fire beskyttede filer er uendret; resultat.png er fortsatt fraværende. Ingen fellesleveranser, statusfiler, Git eller appkode er endret. Innebygd bildeverktøy, modellversjon ikke eksponert. Ingen spilltest eller ny Tom-godkjenning.
