# Små romobjekter og gullstav, Linux r9

De 20 lagjobbene som manglet resultatfil er levert i gpt-arbeid. De omfatter 31 objektbilder i rom 23, 25, 26, 27, 32, 77, 88 og 90. Alle 236 lagjobber har nå resultatfil. Dette er en leveranse for videre bruker-KS, ikke en påstand om at hele spillets HD-grafikk er ferdig.

Gullstaven har fått ny glatt gull-/håndgrafikk og riktig gullgrunnpalett i rom 50 og alle tre obj884-tilstander. Motor og native indeksdata er bevart. Rom 77-objektenes bakgrunn er synkronisert med HD-rommet for å fjerne rektangulære skjøter. Originalt uendrede områder beholdes gjennom tilstandsmatching. Se IMPORT-LAG.json, GULLSTAV-IMPORT.json og MAP-BACKGROUND-SYNC.json.

16 jobbresultater er uendrede generatorbilder. Fire er tekniske atlas med separat genererte detaljbilder plassert etter native alfa og posisjoner. Uendrede råtegninger for detaljene ligger i assets/. DETAIL-ATLAS.json, prompter og scripts/ dokumenterer sammensetningen. Ingen kode er brukt til å tegne erstatningsgrafikk.

## Kontroll og videre KS

Faktisk AppImage/FUSE er kjørt i 21 avgrensede rom-/tilstandstester. Alle 42 opptegningskontroller har null skjermavvik. Alle 34 ønskede objekt-/stavbilder lastes; noen originalpiksler som er identiske med rommet tegnes gjennom HD-rombakgrunnen. 20 av 21 ferdige skjermbilder er pikselidentiske med tilsvarende native test. Rom 25s tidsstyrte fargesyklus gir et annet originalbilde mellom kjøringer; denne sammenligningen er informativ og står med eksakte differansetall i QA-APPIMAGE.json. Det er ikke utført en full gjennomspilling eller ny fysisk tastaturtest.

Tre lag trenger ekstra bruker-KS: lag027_03_del2av8, lag032_05 og lag032_07. Automatisk avvisning er ikke omskrevet til godkjenning. Rom 27s utslag gjelder bakgrunnsblokker utenfor objektet; objektet er kontrollert separat. De to lag032-jobbene har nøyaktige native masker, men nytegnede innvendige flater gir lav kantlikhet. Kontroller disse gjennom den normale gåterekken. Brukerens godkjenning er åpen for alle 20 rader i HD-SJEKKLISTE.md.

Alle 25379 modfiler og 70 leveransefiler har verifisert sjekksum. 80 beskyttede jobbinput er uendret. Alle 106 rombakgrunner er med; 105 er uendret fra r8 og rom 50 er rettet. Alle 15 HD-krystallruter og 551 tidligere halsrettede hoder er beholdt. 25327 modfiler og motoren er uendret fra r8. Se PACKAGED-CONTENT.json.

## Linux-fil

Lokal fil: `/home/tombonator3000t/Skrivebord/TheDigHD-20261013-rettet-r9-x86_64.AppImage`

SHA256: `1a104bb4660fa2eaffdddeacc8a941475ec374a4a01015d170f49ecba5bd739e`

Størrelse: 1485683192 byte. Publisering og lokal snarvei er verifisert nedenfor. R8 er bevart.

Lokal stabil AppImage peker nå til r9. Snarveien `The Dig HD - NY r9.desktop` er opprettet med verifisert mål. R8-filen og r8-snarveien er bevart. Snarveien er ikke fysisk klikk-testet. Se LOCAL-DELIVERY.json.

GitHub Linux-releasen er oppdatert til r9 som Latest. Den stabile AppImage-nedlastingen har samme SHA256 og størrelse som den lokalt kontrollerte pakken. R8 er bevart som datert releasefil. Se PUBLISHED-R9.json.
