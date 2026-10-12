# Linux r5: halsfeste for Brink og Maggie

12. oktober 2026. Rettet 150 separate hodebilder for Brink i kostyme 15 og 189 for Maggie i kostyme 18, åtte retninger per person. Samme faste korreksjon gjelder talevariantene i en retning. Selve RGBA-tegningen er identisk etter flytting, uten skalering eller beskjæring. Krage, hals og hår er kontrollert samlet. Bostons 212 rettede r4-hoder beholdes. Ingen kropp, originalindeks, animasjonstid eller motor er endret.

Ny fil: TheDigHD-20261012-rettet-r5-x86_64.AppImage
SHA256: 9bbcf25b68dc79432c6dea7340f680b64fb250ce30f74294783ce1c8ce41e007
Størrelse: 1471392248 byte.

Fem tilfeller er kjørt både native og gjennom faktisk AppImage/FUSE: alle åtte ståretninger per person, gange i halv skala per person og den lagrede gruppescenen i rom 15. Begge testløp gir 47 opptegningskontroller med null avvik mellom delvis og full opptegning. 43 pakkebilder er pikselidentiske med native prøver. De fire ståbildene før testfiguren er satt inn er utelatt fra denne bildesammenligningen.

Før/etter-bildet viser native r4-filer og faktisk Linux r5 med identisk pose og kamera. after-directions.png er fra r5 AppImage; group-scene-packaged.png viser alle tre i rom 15. Alle åtte retninger, gruppescenen og eksempler fra gange i halv skala er også vurdert visuelt. packaged-walk-gallery.png viser tre gangfaser per person fra AppImage.

Pakken er montert og alle 25325 oppføringer i moddens sjekksumliste er kontrollert. Alle 339 erstatninger stemmer med leveransen og med registrerte r4-kilder. Alle øvrige modfiler, bortsett fra oppdatert mod.json og SHA256SUMS, er uendret fra r4. Motorhash og Bostons 212 r4-hoder stemmer. Mottaket er prøvd på alle 339 originalkilder, gjentatt uten nye endringer og avbrutt ved ukjent kilde før noen fil skrives. Den innebygde importeren er også prøvd på den ferdige pakken.

Hele spillet, alle mulige talekombinasjoner og fysisk bildeflyt på skjermen er ikke kontrollert her. Testene bruker SDL dummy og isolerte kopier av brukerens lagringer. Den åpne spilløkten og originale lagringer er ikke endret. Head-only-chores med en kropp fra forrige retning brukes ikke som visuell godkjenning.

ALIGNMENT.json angir kildehash, retning, forskyvning og rettet hash. assets/costumes og import_alignment.py er en selvstendig mottakspakke. Beskyttede originaljobber og annet arbeid i repoet er bevart.

GitHub Linux-releasen er oppdatert til r5 som Latest. Den stabile AppImage-nedlastingen har samme SHA256 og størrelse som den lokalt kontrollerte pakken. R4 er bevart som datert releasefil og som lokal fil. Se PUBLISHED-R5.json.
