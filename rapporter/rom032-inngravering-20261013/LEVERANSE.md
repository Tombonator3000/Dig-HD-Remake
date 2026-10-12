# Rom 32: inngravering i søylen

Tom presiserte at motivet er innskåret i søylens stein. Den gamle dusjen og det fallende vannet var en feil HD-tolkning. Den rettede tegningen har innskårne linjer i en sammenhengende steinoverflate, uten påmontert armatur, utløpsleppe eller vannstråle. Første forsøk ble forkastet som ferdig leveranse fordi trekanten fortsatt så hevet ut. Andre forsøk er valgt. Se KILDEGRUNNLAG.md, prompter og GENERATED-SOURCES.json.

jobber/rom032/resultat.png er generatorens uendrede PNG. De syv lagjobbene har fått oppdatert romkontekst som tekniske atlas av den rettede bakgrunnen og eksisterende HD-objekter på native koordinater. Originale jobbinnganger, indeksfiler, spillmotor og de syv runtime-objektbildene er uendret. Objektene ligger i rektangel [48,144,64,32] i forgrunnen, utenfor den rettede søyleinngraveringen. Atlasplassering er teknisk integrasjon; ingen ny grafikk er malt med kode. Tidligere råresultater finnes i Git-historikken.

Eksisterende importfunksjoner _evaluate, fargelås sigma 6/styrke 1 og _stitch er brukt. Automatisk kontroll er godkjent, forskyvning +0,06/-0,26 originalpiksler, blokkavvik 0,72 og kantlikhet 0,872. Motiv, plassering og materialuttrykk er også sett visuelt i rommet.

Native kontroll er bestått: åtte avgrensede tester, rommets grunnbilde og de syv objekttilstandene. Alle 16 sammenligninger av løpende skjermtegning og full opptegning har null avvik. Lagringene er isolerte kopier. Dette er ikke full gjennomspilling, normal gåteprogresjon eller fysisk tastaturtest. Tidligere ekstra KS for lag032_05/07 gjelder fortsatt. Brukerens visuelle godkjenning er åpen.

Linux r10 bygges med rettelsen. Pakke- og publiseringsbevis legges til etter kontroll.
