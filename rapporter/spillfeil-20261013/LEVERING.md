# The Dig HD r11 – levert 13. oktober 2026

Rettet og publisert for Linux og Windows. 1157 HD-ruter er korrigert eller komplettert. Motorfeilene i inventory og luftsluse er rettet. PR [49](https://github.com/Tombonator3000/Dig-HD-Remake/pull/49) og [50](https://github.com/Tombonator3000/Dig-HD-Remake/pull/50) er flettet etter grønne CI-tester.

## Nedlasting

- [Linux AppImage](https://github.com/Tombonator3000/Dig-HD-Remake/releases/download/linux/TheDigHD-x86_64.AppImage) – 1704700408 byte, SHA-256 `f659d3aa3062b4dbd7a77b92af7c08494209968a6e511af6f377f2f3118ffca1`.
- [Windows x64 ZIP](https://github.com/Tombonator3000/Dig-HD-Remake/releases/download/windows/TheDigHD-Windows-x64.zip) – 1754320528 byte, SHA-256 `2ef22a0f009c15e236b78b4bb6f19a4e39cb131d1f587d97ba1aed36a50ed947`.
- [Komplett motorkilde og byggeunderlag](https://github.com/Tombonator3000/Dig-HD-Remake/releases/download/windows/TheDigHD-r11-engine-source.tar.gz).

Linux-utgivelsen inneholder nå bare nyeste program, med sjekksum og les meg-fil. Skrivebordssnarveien «The Dig HD - NY r11» starter samme AppImage som den offentlige nedlastingen.

## Rettelser

- Inventory-feilen er reprodusert og rettet med en kopi av Toms lagring 5. Feilen skyldtes feil klipping når kameraforskyvningen oversteg bufferbredden. Original lagring er uendret.
- Begge manglende stavtilstandene er komplettert, og kantene rundt stavhullene er forbedret innenfor originalens skjulingsmaske.
- Luftslusens tekniske skyggemasker bevarer nå HD-bakgrunnen.
- Alle 360 krystallformer er registrert mot originalens geometri og farger; den feilaktige beige steinrammen er fjernet.
- Sparks, linserommets lys og vannets bølgefaser er komplettert. Lys-/energianimasjonen er erstattet med lysfilamenter, uten klær eller belter.
- Dørene i bilde 3 og 4 går til hvert sitt transportrom (94 og 95) i originalen. De blå transportmidlene ligner; forbindelsene er riktige og beholdt.

239 tilhørende produksjonsark er oppdatert fra de registrerte runtime-rutene. Samtlige 2314 endrede PNG-filer er med i begge pakker. Modden er låst til `113523ba12fd10fbf2a9ff49b3823cd9aa8095c6`. Detaljer og avgrensninger finnes i `ANALYSE.md`, produksjonsnotatene og JSON-bevisene i denne mappen.

## Kontroll

30 pipeline-tester bestått. Hele motorpatchen er kontrollert mot låst ScummVM-kilde. Berørte scener og animasjoner er kjørt med kontroll mot full nytegning.

Den faktiske publiserte Linux-pakken er lastet ned, sjekksumkontrollert og kjørt på Kubuntu med lagring 5 og linserommets kildeanimasjon. Åtte kontroller gir null avvik mot full nytegning. Bygg [38390612591](https://github.com/Tombonator3000/Dig-HD-Remake/actions/runs/38390612591) bestod oppstart på Ubuntu 22.04 og i Debian 12-container; høyeste glibc-symbol er 2.34. Alle 2314 endrede grafikkfiler matcher leveransen.

Windows-programmet og startfilen er testet gjennom Wine 10 på Kubuntu i seks målscener, samt direkte fra den utpakkede ZIP-pakken. ZIP-innhold og offentlig nedlasting er sjekksumkontrollert. Fysisk Windows er ikke testet.

Det første CI-bygget startet før mod-opplastingen var ferdig og ble forkastet. PR50 låser mod-revisjonen ved byggestart. En lokal prøvepakke som krevde glibc 2.43 er også forkastet; den offentlige Linux-pakken er Ubuntu 22.04-bygget beskrevet over.

Dette er teknisk QA og visuell gjennomgang av de berørte scenene. Full gjennomspilling og Toms endelige visuelle godkjenning gjenstår.

## Opprydding

Gamle godkjente testbygg og gamle Linux-utgivelsesfiler er fjernet. r10-skrivebordsprogrammet og snarveien er fjernet etter sjekksum- og håndtakskontroll. Midlertidige bygge- og testmapper fra denne oppgaven er ryddet; siste opprydding økte ledig diskplass med 17739370496 byte (17,7 GB).

Originale lagringer, urelaterte arbeidsfiler, nåværende offentlige pakker, komplett kildearkiv og QA-bevis er bevart. Se `SCRATCH-CLEANUP.json`, `DESKTOP-INSTALL.json` og `DELIVERY.json`.
