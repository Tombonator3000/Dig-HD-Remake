# Glass, PDA-paneler og museumspanorama

Når Boston stod bak glasset i luftslusen (rom 25), erstattet glassmaskens pikselmerke figurens eiermerke. HD-tegningen ble da bygget fra rombakgrunnen, også der masken hadde behandlet Boston. Motoren bevarer nå fargen og figurmerket under en faktisk palettmaskering, tegner HD-underlaget og bruker originalens fargeendring til slutt. Masken identifiseres av dekoderen, ikke ved likhet med en tilfeldig palettfarge.

PDA-bilder i rom 79 blander transparente og ugjennomsiktige SMAP-striper. Et enkelt PNG-transparentindeks gjorde også ugjennomsiktig svart gjennomsiktig. Uttrekket lagrer nå en valgfri `objNNN_SS_mask.png` med dekoderens faktiske dekning per piksel. To dekodinger med ulikt startinnhold skiller skrevne nullpiksler fra uskrevne piksler uten å endre originalens indekser. Gamle pakker uten maskefilen bruker tidligere transparentindeks.

Et tegnet objekt kunne dessuten dele palettindeks med rommet bak. Rommet fikk da forrang og laget hull i HD-portretter og knapper. Motoren velger nå det sist tegnede, fortsatt aktive objektbildet før rommet når objektet har en eksakt dekningsmaske. For gamle pakker uten maskefilen beholder rommet tidligere forrang ved like indekser. Skjulte og erstattede objekttilstander får ikke eie nye piksler.

Museumsspirets panorama er originalens kostyme 119, tegnet av aktør 14 bak z-plan 3. Kandidaten bruker det myke HD-bildet og jevner bare ut den synlige siden av maskekanten. Skjulte originalpiksler forblir skjult. Den smale, lyse åpningen gjennom forgrunnen finnes også i originalbildet og er derfor beholdt.

Spillets skript, lagringer, animasjonstider og klikkfelt er uendret. Endringene gjelder tegning og eksport av dekning.

## Kontroll

- 42 pipeline-tester bestått lokalt med `pytest -m "not game"`. To spilltester er utelatt.
- Dekningstestene omfatter flere striper og rader, begge startverdiene 0 og 255, eksportert alfa, uendrede originalindekser og kopiering/fjerning av maskefiler i begge mod-byggveiene. Disse ti kontrollene bestod også med `digart` utilgjengelig.
- To ekstra konformitetstester kjører den faktiske SMAP-dekoderen med svart 0 og rommets transparente farge 5 i ugjennomsiktige og transparente striper. De bestod lokalt. CI uten den valgfrie dekoderen hopper bare over disse to.
- 15 Pages-tester bestått. Hele motorpatchen er byteidentisk med det native arbeidsdiffet og består både foroverkontroll mot den låste ScummVM-revisjonen og reverskontroll mot arbeidskilden.
- Feilen med Boston bak glasset er gjenskapt med publisert r11-motor, rettet i kandidatmotoren og kontrollert i skjermbilder.
- PDA-portretter er kontrollert i kandidatmotoren. Nye bilder og indeks-/maskefiler holdes i grafikkgrenen/modden.
- Målrettede native kjøringer kontrollerer inkrementell tegning mot full skjermtegning. Dette er teknisk kontroll og ikke Toms visuelle godkjenning av hele spillet.
- Museumspanoramaet er kontrollert med kamera x=160, 360 og 548: ni skjermdumper med null avvik mot full nytegning og null avvik mot originalens z-plan. Native- og Windows-motoren er bygget på nytt etter kantrettingen.
- Offentlige pakker og fysisk Windows testes/rapporteres separat ved levering.
