# Krystallene i rom 50, Linux r8

Tom påviste at blå og grønne krystaller fortsatt var grov originalgrafikk. R7 hadde bare de tre første av femten ruter i kostyme 319 i HD. Fire nye originale generatorark, fig319_02 til 05, fyller de tolv manglende rutene. Alle fem former finnes nå i rødt, grønt og blått. Tidligere tre røde ruter er beholdt.

Motiv, palett og funksjon er kontrollert i originalreferanser og spillvisning. Krystallene beholder egne fasetter, former, farger, plassering og indre lysbrytning. Innebygd ChatGPT Images er brukt, med ett forsøk per ark. Verktøyet oppga ikke eksakt modellversjon. Originale genererte PNG-er ligger i jobbmappe og assets/, og 24 ferdige HD-/indeksfiler ligger i assets/costumes/. Beskyttede jobbfiler er uendret.

Standard myk v3-import har status ok for alle tolv nye ruter. Minste omrissoverlapp er 0,918 og minste dekning 0,920. Rutekart, kildehasher, prompter og importerens målinger er vedlagt. Den blå oktaederen er flyttet 2 HD-piksler ned innenfor egen transparente importmarg, uten endring eller klipping av noen tegningspiksel. Dette tilsvarer en halv originalpiksel og plasserer spissen innenfor originalens første pikselblokk. En utdatert flekk på fire piksler ved romåpning er etter rettelsen borte. Se ANCHOR-CALIBRATION.json. Ved senere reimport må dette importfestet beholdes; ferdig kalibrerte filer ligger i assets/costumes/. Generatorens originalfil er uendret.

Native kontroll: vanlig rom50-visning, en injisert skuespiller som viser alle femten tilstander, og en egen gjentakelse av romåpningen. Alle femten tilstander er sett i faktiske skjermbilder og kontrollert samlet. 49 avsluttende skjermkontroller gir null avvik. Logger og galleri er vedlagt. Feilene i de innledende prøvene er ført i ankerkontrollen sammen med rettelsen. Testene bruker isolerte lagringskopier og endrer ikke brukerens lagringer. Ingen motorendring er gjort. Dette er avgrensede grafikk- og romtester, ikke full gjennomspilling eller fysisk tastaturtest.

Alle 106 HD-rombakgrunner og øvrige r7-rettelser beholdes. Dette betyr ikke at alle andre objekter og animasjoner er ferdige i HD. Utført AppImage- og publiseringskontroll er dokumentert nedenfor.

Den ferdige AppImage-filen er kjørt via sin faktiske FUSE-runtime. Alle femten krystallruter lastes. 49 skjermkontroller gir null avvik, og alle 40 ferdige skjermbilder er pikselidentiske med de tilsvarende native prøvene. Alle 25355 modfiler har riktige sjekksummer. Bare 24 nye krystallfiler og modmetadata er endret fra r7. Alle 25330 øvrige eksisterende modfiler, alle 106 rombakgrunner, 551 rettede hoder og motoren er uendret. Se PACKAGED-CONTENT.json og QA-APPIMAGE.json.

Lokal Linux r8 ligger på skrivebordet med egen snarvei «The Dig HD - NY r8». Den lokale stabile filen er oppdatert til samme kontrollerte r8-fil; datert r7 og snarveien til r7 er bevart. Selve AppImage-filen er kjørt i testen, men skrivebordssnarveien er ikke fysisk klikket. Se LOCAL-DELIVERY.json.

GitHub Linux-releasen er oppdatert til r8 som Latest. Den stabile AppImage-nedlastingen har samme SHA256 og størrelse som den lokalt kontrollerte pakken. R7 er bevart som datert releasefil og lokal fil. Se PUBLISHED-R8.json.
