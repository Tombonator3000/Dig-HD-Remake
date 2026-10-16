# Restgrafikk r19, arbeidsrapport 16. oktober 2026

Tom har bekreftet at oppdraget gjelder all restgrafikk i hele spillet. Arbeidet er ikke ferdig. Rapporten er et etterprøvbart mellomlager, ikke en utgivelse eller visuell godkjenning.

Kandidaten har 1676 nye HD-ruter. Den siste opptellingen har 12343 originalruter uten HD, hvorav 7947 har minst 40 synlige originalpiksler. Små fragmenter telles separat. Ingen ny distro er bygget fra denne kandidaten.

## Kilder og metode

Godkjente pilotark i hovedark/boston.png, brink.png og maggie.png styrer menneskene. Originaldata fra DIG.LA1, indeksbilder, animasjonsvalg og spillkontekst bestemmer motiv, plassering og palett. Originale jobbfiler er bevart.

Prosjektbibliotekets losninger/grafikk/figurark-fast-storrelse.md ble lest. Prinsippet om opprinnelig geometri brukes, men bibliotekets PASS gjelder tidligere kilderevisjoner og er ikke visuell godkjenning her. Se https://github.com/Tombonator3000/prosjektbibliotek/blob/main/losninger/grafikk/figurark-fast-storrelse.md.

Verktøy: innebygd image_gen for nytegning, Python med Pillow, NumPy, OpenCV og eksisterende dighd.myk for mekanisk registrering. Faktiske native bildemål er registrert der de avviker fra ønsket størrelse. Modellnavn er ikke eksponert av verktøyet.

De fire kommunikasjonsportrettene beholder original identitet, uttrykk og signalforstyrrelser. Ken Borden og Cora Miles er kontrollert mot spillets offisielle manual: https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/6040/manuals/THE_DIG_Manual-English.pdf?t=1542756570.

## Det som er produsert og tatt inn i arbeidskandidaten

* Boston i romdrakt, tre nye ark og tilhørende småfragmenter.
* Boston ved gjenopplivingen i vannrommet, 17 nytegnede større poser og 6 småfragmenter. Paletten er hentet via AKPL i rom 32, ikke feilfarget eksportpalett.
* Manglende faser fra tidligere leverte stol-, robotarm-, Nexus-, Eye- og Lockup-ark.
* Spiralfaser med nytegnet materiale registrert mot originalens hull og fragmenter.
* Brink, Maggie, Ken og Cora på PDA, inkludert uttrykk og signalstøy. Støy uten figur er teknisk oppskalering av originalsignalet.
* 670 krystallfaser gjenbruker den eksisterende krystalltegningen, tilpasset originalens fasegeometri og farge. Brune matter rundt krystallene fjernes.
* 70 manglende nærbildefaser av Maggies bakhode, skulder og hånd. Kostyme 328 og 329 har identiske originale bilder, kontrollert før gjenbruk. To smale hudfragmenter bevarer originalformen teknisk. Manglende avklipte håndstrimler i to native faser gjenbruker en nytegnet nabofase. Dette står eksplisitt i maggie-registration.json.

## Kontroller og begrensninger

kontroller/ inneholder råresultater fra isolerte spillmotortester. Skjermbufferen sammenlignes med full omtegning. Ruter som faktisk ble tegnet registreres. En test uten synlig HD-figur teller ikke som figurtest, selv om skjermbufferen er stabil. Tidlige tester med feil kameraposisjon er bevart som diagnostikk; senere sentrerte tester viser den faktiske dekningen.

base-preservation.json kontrollerer alle 30 378 publiserte r18-filer mot Git-innholdet. Kandidaten legger til ruter og endrer ikke disse filene. ADDITIONS.json er hashmanifestet for tilleggene.

Dette er ikke en full gjennomspilling. Flere tekniske tester dekker bare utvalgte animasjonsvalg. Hode, kropp og stil må vurderes samlet gjennom overgangene. Tom har ikke visuelt godkjent disse nye arkene. Krystalltester som bare viser en eller to faser beviser ikke hele seriens visuelle kvalitet.

## Gjenstående arbeid

dekning-arbeid.json er den konkrete listen. Neste arbeid omfatter øvrige nærbilder, figurer, skapninger, mekanismer og effekter. Noen eksporterte paletter viser tekniske farger eller masker. Disse må avklares i original spillkontekst før nytegning; de skal ikke males bokstavelig som nakne figurer eller røde kjøretøy.

verktoy/ bevarer registreringsoppskrifter. Sett DIGHD_WORKSPACE til arbeidsroten med kode/, grafikk/, hd-leveranse/, kandidat-r19/ og testing/source/ ved reproduksjon. Skriptene er arbeidsverktøy og krever kildedataene som rapporten viser til. Ikke kjør import_r19.py ukritisk over senere rettede spiralfaser.
