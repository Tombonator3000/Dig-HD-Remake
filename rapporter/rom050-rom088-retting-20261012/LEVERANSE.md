# Rom 50 og rom 88, Linux r7

Rom 50 er tatt inn med den konkrete kandidaten Tom godkjente. Den er ikke tegnet om. Opprinnelig automatisk avvisning på lokalt geometriavvik 6,87 piksler er bevart i rapporten, sammen med den uttrykkelige manuelle godkjenningen og kildehashen.

Rom 88 er bygget av ni deler. Del 1 til 5 er beholdt. Del 6, 8 og 9 er nye første forsøk i denne runden; del 7 bruker forsøk 2, fra originalen alene. Alle ni består den opprinnelige delkontrollen. Store påmalte svarte felt, feil plassering og tydelige skjøter fra gammel kandidat er rettet. 1883552 kontrollerte interiørpiksler i originalens svarte områder holder maksimal verdi 1 av 255. Hele rommet har kantlikhet 0,991 og fargeavvik 0,5. Den ekstra helbildekontrollen har et grensetilfelle på 1,15 originalpiksler i én grov blokk, som er ført som sjekk og kontrollert visuelt i sammenstilling og fire runtime-vinkler.

Motivene er undersøkt i originalmotoren og spilldataene før produksjon. Små mørke skapninger beholder blå øyne på stilker. Den separate kiste-/plategrafikken er ikke malt inn i bakgrunnen. Originalens dør, søyleflater, gulvsprekker og lys er bevart. KILDE-OG-RETTEPLAN.md og korrigerte promptfiler dokumenterer analysen. Verktøyet var innebygd ChatGPT Images; eksakt modell og versjon ble ikke oppgitt av verktøyet.

Native test: rom 50, samt nedre venstre, nedre midtre, nedre høyre og øvre høyre kameravinkel i rom 88. Ti kontroller av løpende skjermtegning mot full nytegning gir null avvik. Skjermbilder og logger er vedlagt. Testene bruker isolerte kopier av lagringene. Ingen motorendring er gjort. Dette er avgrensede romtester, ikke en full gjennomspilling eller en ny fysisk tastaturtest.

Alle 106 av 106 rombakgrunner følger med i HD etter denne importen. Dette er antallet rombakgrunner, ikke en påstand om at alle separate objekter, figurer og animasjoner er ferdige. Blant annet bruker noen vaktanimasjoner ved døren i rom 88 og krystall-/stavtilstander i rom 50 fortsatt originalgrafikk.

IMPORT-MANIFEST.json angir kildefiler, kontrollverdier og SHA256. Ferdige importfiler ligger i assets/rooms/. Kildejobber 6 til 9 er oppdatert, mens beskyttede referanser, originaler, metadata og originalprompter er uendret. Pakke-, lokal leverings- og publiseringskontroller er dokumentert nedenfor og i egne JSON-filer.

Ferdig AppImage/FUSE er kontrollert: 25331 modfiler har riktige sjekksummer. Bare fire nye romfiler og modmetadata skiller seg fra r6; 25326 eksisterende modfiler, motoren og alle 551 korrigerte hoder er uendret. Rom 50 og fire kameravinkler i rom 88 lastes med HD-bakgrunn. Ti kontroller av løpende skjermtegning mot full nytegning gir null avvik, og alle ti ferdige skjermbilder er pikselidentiske med de tilsvarende native kjøringene. Se PACKAGED-CONTENT.json og QA-APPIMAGE.json.

Lokal Linux r7 ligger på skrivebordet med egen snarvei «The Dig HD - NY r7». Den lokale stabile filen er oppdatert til samme kontrollerte r7-fil; datert r6 og snarveien til r6 er bevart. Selve AppImage-filen er kjørt i testen, men skrivebordssnarveien er ikke fysisk klikket. Se LOCAL-DELIVERY.json.

GitHub Linux-releasen er oppdatert til r7 som Latest. Den stabile AppImage-nedlastingen har samme SHA256 og størrelse som den lokalt kontrollerte pakken. R6 er bevart som datert releasefil og lokal fil. Se PUBLISHED-R7.json.
