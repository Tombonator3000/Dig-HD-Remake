> Rettelse 13. oktober 2026: Tom har presisert at søylemotivet er en inngravering i stein. Den historiske vanntolkningen nedenfor er feil og erstattet av rapporter/rom032-inngravering-20261013/.

# Rom 32 importert, rom 50 og 88 til kontroll

Bestilling: «Importer 32, vis rom 50 og 88 så jeg får kontrollert».

Rom 32 bruker den rettede, eksisterende leveransen fra jobber/rom032/resultat.png. Den har loddrett rennende vann under buen til venstre, i stedet for feilaktig steindekor. Ingen ny tegning er laget. Kildebildet og beskyttede jobbfiler er uendret.

Standard mottakskontroll er kjørt med eksisterende dighd.gpt._evaluate og _stitch, sigma 6, styrke 1. Samme godkjente kildehash er kontrollert. Bakgrunnen blir 1280 x 800, og ekte originalindekser følger som room032_idx.png på 320 x 200. Originalindeksene gir samme RGB-bilde som den beskyttede originalen. IMPORT-EVALUATION.json og PROVENANCE.json dokumenterer kilde, fargelås, gråkantbehandling og filhasher. Ferdige importfiler ligger i assets/rooms/.

Native motor er kjørt med isolerte kopier av lagringene. Rom 32 lastes som HD. Fem sammenligninger mellom løpende skjermtegning og full nytegning gir null avvik, ved bilde 40, 80, 120, 160 og 200. Før og etter vises i runtime-PNG-ene. Vann under buen, dam, steiner, dør, trapp og fjellplassering er kontrollert visuelt. Dette er en avgrenset romtest, ikke en full gjennomspilling eller manuell tastaturtest. Se QA-NATIVE.json og loggene.

Rom 50 og 88 er bare vist til kontroll. De er ikke importert. Rom 50 vises med originalen til venstre og nåværende kandidat til høyre. Rom 88 er en samlet visning av de ni nåværende kandidatdelene med standard myk overgang i overlappene, uten fargelås. Del 6 til 9 vises også hver for seg. Ingen feil er skjult: påmalte svarte felt, feil geometri og synlige overganger er fortsatt med. Forhåndsvisningene er ikke bilder fra Linux-pakken. Full original og samlet kandidat for rom 88 er også vedlagt.

Linux r6 har rom 32 i tillegg til de 103 rombakgrunnene fra r5. Rom 50 og 88 er de to som fortsatt mangler. Pakke- og publiseringskontroll legges i egne JSON-rapporter når de er fullført.

Den ferdige AppImage-pakken er kontrollert: 25327 modfiler har riktige sjekksummer, 25324 tidligere grafikkfiler er uendret, og motoren er identisk med r5. Alle 551 korrigerte hoder er bevart. Rom 32 lastes i faktisk AppImage/FUSE, fem kontroller gir null avvik og fire ferdige skjermbilder er pikselidentiske med native. Bilde 40 er midt i rommets åpningseffekt og har ulik tidsfase mellom de to kjøringene; det er ikke brukt til identitetskontroll mellom kjøringene. Se PACKAGED-CONTENT.json og QA-APPIMAGE.json.

GitHub Linux-releasen er oppdatert til r6 som Latest. Den stabile AppImage-nedlastingen har samme SHA256 og størrelse som den lokalt kontrollerte pakken. R5 er bevart som datert releasefil og lokal fil. Se PUBLISHED-R6.json.
