# Boston: hodefestet i The Dig HD

12. oktober 2026. Brukerens skjermbilde viser glippe mellom hode og hals og et hode som sitter for langt bak. Personen er Boston Low i planetklær, kostyme 14: brunt hår med grå tinninger, mørk blågrønn skjorte, oransje bukser og svarte støvler. Identitet, tegning, skala og kropp skal beholdes.

Feilen finnes i r3. Den forrige kalibreringen brukte skallbredde og toppen av hodet per retning. Den manglet et kontrollert feste mot kroppens tegnede hals. Samme rom er gjenskapt fra en isolert kopi av brukerens lagring 3: rom 64, kropp 017 og talehode 411. Originalindekser og de faktiske native celposisjonene er brukt til å sammenligne delene. Lagret retning er forskjellig fra retningen i brukerens stillbilde; en separat kontroll gjenskaper alle åtte ståretninger i samme rom.

Rettelsen flytter de eksisterende 212 separate hodebildene med en fast forskyvning per retning. Halsens kontaktpunkt er grunnlaget, med en liten fremoverflytting i de to fremre trekvartvinklene etter brukerens presisering. Alle RGBA-piksler i selve tegningen bevares, og ingenting klippes. Den samme korreksjonen brukes for talevariantene i en retning. Ingen ny skalering eller nytegning, og ingen endring av native indeksbilder, spillposisjoner eller animasjonstempo.

ALIGNMENT.json angir R3-kildehash, ny hash, retning, forskyvning og referansepar for hvert hode. assets/costumes inneholder rettede bilder. import_alignment.py kan gjenta mottaket mot samme R3-grunnlag og avviser ukjente kilder. Aktuelle godkjente originaler og prompter er ikke endret.

Visuelt kontrollert: før/etter fra identisk ståpose og kamera i rom 64, de åtte ståretningene, det lagrede talehodet 411 sammen med kropp 017 og gange i halv skala. Den automatiske gjennomgangen av alle chores gir også tekniske redraw-kontroller, men hode-only chores kan beholde en kropp fra forrige retning; slike kunstige kombinasjoner er ikke brukt som visuell godkjenning av taleanimasjonen. Alle 212 filer er kontrollert for identisk tegning etter flytting. Hele spillet og alle mulige talekombinasjoner er ikke gjennomspilt.
