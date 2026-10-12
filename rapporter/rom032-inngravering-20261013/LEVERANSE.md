# Rom 32: inngravering i søylen

Tom presiserte at motivet er innskåret i søylens stein. Den gamle dusjen og det fallende vannet var en feil HD-tolkning. Den rettede tegningen har innskårne linjer i en sammenhengende steinoverflate, uten påmontert armatur, utløpsleppe eller vannstråle. Første forsøk ble forkastet som ferdig leveranse fordi trekanten fortsatt så hevet ut. Andre forsøk er valgt. Se KILDEGRUNNLAG.md, prompter og GENERATED-SOURCES.json.

jobber/rom032/resultat.png er generatorens uendrede PNG. De syv lagjobbene har fått oppdatert romkontekst som tekniske atlas av den rettede bakgrunnen og eksisterende HD-objekter på native koordinater. Originale jobbinnganger, indeksfiler, spillmotor og de syv runtime-objektbildene er uendret. Objektene ligger i rektangel [48,144,64,32] i forgrunnen, utenfor den rettede søyleinngraveringen. Atlasplassering er teknisk integrasjon; ingen ny grafikk er malt med kode. Tidligere råresultater finnes i Git-historikken.

Eksisterende importfunksjoner _evaluate, fargelås sigma 6/styrke 1 og _stitch er brukt. Automatisk kontroll er godkjent, forskyvning +0,06/-0,26 originalpiksler, blokkavvik 0,72 og kantlikhet 0,872. Motiv, plassering og materialuttrykk er også sett visuelt i rommet.

Native kontroll er bestått: åtte avgrensede tester, rommets grunnbilde og de syv objekttilstandene. Alle 16 sammenligninger av løpende skjermtegning og full opptegning har null avvik. Lagringene er isolerte kopier. Dette er ikke full gjennomspilling, normal gåteprogresjon eller fysisk tastaturtest. Tidligere ekstra KS for lag032_05/07 gjelder fortsatt. Brukerens visuelle godkjenning er åpen.

Linux r10 er bygd og kontrollert i faktisk AppImage/FUSE. Åtte pakketester og 16 opptegningskontroller er bestått. Alle åtte ferdige skjermbilder er pikselidentiske med native test. Hvert av de syv objektene er tegnet med lastet HD-bilde, og inngraveringen er kontrollert i selve pakketestens skjermbilde. Se QA-APPIMAGE.json og screenshots/.

Alle 25379 modfiler har verifisert sjekksum. Bare rooms/room032.png og mod.json er endret fra r9; 25377 modfiler er uendret. Originale rom-/objektindekser og samtlige syv rom32-objektbilder er byteidentiske med r9. I tillegg er 247 pakkefiler utenfor modden kontrollert uendret, inkludert motor, spillfiler, lyd, biblioteker og tidligere leveransebevis. R9s gullstav, alle 15 HD-krystalltilstander, alle 106 rombakgrunner og 551 halsrettede hoder er bevart. Se PACKAGED-CONTENT.json.

Lokal fil: `/home/tombonator3000t/Skrivebord/TheDigHD-20261013-rettet-r10-x86_64.AppImage`.

SHA256: `d8769b180ee9c8acf532de03b36d2058f19badd3b7383d56d66323a26fc6ed68`.

Størrelse: 1485552120 byte.

Den lokale stabile AppImage-filen og snarveien `The Dig HD - NY r10.desktop` peker til r10 med verifisert mål. R9 og r9-snarveien er bevart. Snarveien er ikke fysisk klikk-testet. Se LOCAL-DELIVERY.json.

GitHub Linux-releasen er oppdatert til r10 som Latest. Den faste AppImage-nedlastingen har verifisert r10-sjekksum og størrelse, og offentlig HEAD gir HTTP 200 med riktig Content-Length. R9 er bevart som datert releasefil. Se PUBLISHED-R10.json.
