# Spillfunn og rettinger 13. oktober 2026

Toms tolv skjermbilder og lagring 5 er grunnlaget. Lagringen testes som kopi, med SHA-256 `4f89566a2daec02f35060983f8e42d9b4c908de7b1deb0a3aead2004dc0500a4`. Originalen er bevart.

## Motor

Inventory mistet HD ved horisontal kamerarulling. `beginBlast` klippet kameraets forskjøvede bufferkoordinat mot skjermens pitch, selv om SCUMM kan ha xstart større enn pitch. Lagring5 har xstart416 og pitch328. Klipping skjer nå mot det synlige vinduet, mens eierskap fortsatt følger de faktiske bufferforskyvningene. Ikonene blir riktig tegnet også ved gjenåpning.

Luftslusens kostyme75 er en teknisk palettmaske, ikke en separat rød eller blå trapp. Dekoderen registrerer de pikslene som faktisk går gjennom skyggemapping. Motoren bygger HD-underlaget og anvender originalens skyggefarge. Masken lager ikke lenger et stort originalfelt over HD-rommet. Vanlige figurpiksler får ikke maskebehandling bare fordi de tilfeldigvis har samme farge.

Glidende blå staver får mykere z-maske på den synlige siden av hullkanten. Piksler som originalens maske skjuler forblir skjult. Registrerte HD-lysruter viser HD-bakgrunnen under gjennomskinnelig lys, uten gamle opake palettflater.

Testkrokene kan holde hele kildeanimasjoner i stedet for å bytte retning etter fire bilder. Eksplisitt kameravalg kan nå inspisere hele rommet uavhengig av forrige scenes kamera- og scrollgrenser. En valgfri statisk testscene stanser skriptene mens AKOS-animasjonen kjøres. Ingen av disse testvalgene brukes ved vanlig start.

## Grafikk

Tre nye krystallark og én master hver for hav og lys er produsert med innebygd ChatGPT-bildegenerator. De bevares i grafikkgrenen sammen med prompt, proveniens og rutekart. 1157 HD-ruter kompletteres eller korrigeres: 360 krystallformer, 240 canyon-lysruter, 54 sparks-ruter, 477 kraftrom-/linseruter, 24 bølgefaser og to stavfaser. Registrering, gjenbruk og maskebehandling er dokumentert; antallet er ikke antall separate AI-genereringer.

`register_crystal_atlas.py` fjerner den orange bakgrunnsmatten og registrerer malte former til kildens form og fargetilstand. Den tykke beige rammen var en feil motivtolkning. `register_wave_texture.py` bruker ett felles malt vannfelt, originalens strand-/skummasker og originalt tempo. `register_energy_field.py` legger et malt filamentfelt i originale lyssilhuetter; mørke bakgrunnspolygoner viser HD-rommet, og små sparks får glatte lyskjerner. Klær og belter er ikke lysmotivet.

Originale spillfiler og beskyttede grafikkjobb-filer er uendret. Bilder og spilldata ligger ikke i denne kodegrenen.

## Dørene

Bilde3 er nexus-dør183 ved x1064, bilde4 er dør175 ved x736. Originalkode for183 leder via objekt696 til rom94, mens175 leder via699 til rom95. Begge transportrommene har lignende transportfartøy. Bilde5 matcher rom95. Forbindelsene beholdes.

## Kontroller

30 eksisterende pipeline-tester bestått, to spilltester utelatt i denne kjøringen. Native motor er kompilert. Nearest-kontroller for inventory, luftsluse, bølger og kraftrom gir null avvik i vanlig HD/original-sammenligning og null avvik mot hel nytegning. Fargesykling og HD-tekst rapporteres separat av motoren.

Kandidatbilder og hele kildefaser for inventory, glassmaske, krystallformer, bølger, sparks, canyon-lys og kraftrom-lys er kontrollert i isolerte kjøringer. Pakker og Windows-kjøring kontrolleres separat ved utgivelse. Dette er teknisk QA og en visuell kandidatgjennomgang, ikke Toms endelige stilgodkjenning eller en full gjennomspilling.
