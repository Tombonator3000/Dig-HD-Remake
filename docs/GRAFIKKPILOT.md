# Grafikkpilot til Claude, 6. oktober 2026

To malte HD-bakgrunnskandidater er laget fra originale rombilder og inspisert i den faktiske ScummVM-forken på laptopen. En Boston Low-stilreferanse følger med separat. Stilen er foreløpig.

## Hent og kjør

Bildene, mod-mappen, originalreferansene, promptene og bevisene ligger i den separate private grenen [grafikkdata/pilot-20261006](https://github.com/Tombonator3000/Dig-HD-Remake/tree/grafikkdata/pilot-20261006), commit cf8e6a9f6e30d662f7c73076ef1e1810851ceceb. Grafikkgrenen har ingen felles historikk med main og skal ikke flettes inn i kodegrenene. Verktøyene og denne dokumentasjonen kan tas inn i kodegrenen.

Fra prosjektroten:

```sh
bash tools/hent_grafikkpilot.sh
.venv/bin/python tools/check_hd_art.py --extract work/graphics-pilot-20261006/reference --own work/graphics-pilot-20261006/assets
DIGHD_MOD="$PWD/work/graphics-pilot-20261006/mod" engine/scummvm/scummvm --path="$PWD/game" --gfx-mode=opengl --aspect-ratio dig
```

Henteskriptet sjekker den konkrete committen og alle SHA-256-summer. En eksisterende arbeidsmappe kontrolleres og bevares. Endrede lokale filer gir feil i stedet for overskriving. Pipeline og spillfiler settes opp som i README.md dersom de mangler.

Mod-mappen er ferdig bygd og trenger ikke et nytt uttrekk. Den inneholder bare to rom og to originalobjektvarianter. Motorens vanlige fallback viser resten. Den aktive hd-modden og spilldataene skrives ikke over.

## Levert

| Ressurs | Kilde | Fil og mål | Bruk |
| --- | --- | --- | --- |
| Asteroidens indre | Rom 9, core, 320x200 | assets/rooms/room009.png, 1280x800 RGB | Bakgrunnskandidat. Gulvhjørne korrigert i andre generering. |
| Blå kyst | Rom 22, beach, 320x200 | assets/rooms/room022.png, 1280x800 RGB | Bakgrunnskandidat. Fargesyklede områder tegnes fortsatt fra originalen. |
| Boston Low | Kostyme 14, rute 1, 21x65 | concepts/boston-low-cel001.png, 713x2205 RGBA | Stilreferanse. Avvist som direkte spritesrute på grunn av silhuettavvik. |

Begge rombildene finnes også i mod/rooms/ sammen med deres uendrede originalindekser. obj171_01 og obj171_02 er originale objektvarianter skalert med nearest. Ingen malte objektvarianter eller ny spriteserie er levert.

2 av 111 rom har nye kandidater. Ingen egne spritesruter eller SAN-rammer er integrert. Manuell maskekontroll og godkjent art direction gjenstår før kandidater kalles produksjonsgrafikk.

## Bevis og grenser

- Kodegrunnlag: Claude-grenen claude/analyse-hd, commit 70aed0523ff624cb6176d9b5911cdc1fdef0f336, PR 1 fortsatt åpen ved kontroll. Ingen motorendring i denne leveransen.
- Spillfilenes sjekksummer bestod. Uttrekk av fem rom ga 19 rom- og objektbilder uten dekoderfeil. Kostyme 14 ga 840 ruter med RGBS-farger.
- ScummVM bygd fra låst commit c9091321060acfc8f037767c18f8279a86305b7e med uendret patch. libpng-utviklingsfiler ble hentet fra Ubuntu og pakket ut lokalt i work/build-deps/. Ingen systeminstallasjon.
- 4 pipeline-tester bestod, inkludert originaldata. Begge nye bakgrunnsbilder består format-, mål- og indekskontroll.
- Native SDL2/Wayland/OpenGL-kjøringer: begge HD-bakgrunner lastet, 1280x800, 4 byte per piksel, exit 0. qa/runtime/final-results.json og roomNNN-final-hd/frame_000480_roomNNN.png er bevisene.
- Native nearest-kontroll: 0 sterke pikselavvik i rom 9 og 22 etter motorens terskel på mer enn 48 per fargekanal. Det er ikke en måling av byteidentitet.
- Negative kontroller: generatorens 1586x992-mål avvises før mod-bygging. Boston-prøvens alfasilhuett avvises ved motorens terskel 128. Bildet er beholdt som konsept utenfor mod/.
- Kjøringene brukte testhopp til rommene. De første dummy-hoppene ved bilde 60 ble overstyrt av oppstartsskript og endte i rom 2. Native hopp ved bilde 240 traff de riktige rommene. Logger fra begge forsøk er bevart.
- Ingen full gjennomspilling, manuell bevegelse gjennom forgrunnsmasker, lytting eller ytelsesmåling. Musikk og tale mangler lokalt. Kystkjøringen tegnet ikke obj171 eller en figur, så den beviser ikke objektbytte eller okklusjon i rommet.

Pakken har fullstendige prompter, originale generatorbilder, kildehashene og SHA-256-manifest. Den innebygde ChatGPT-bildegeneratoren ble brukt. Verktøyet bekreftet ikke et eksakt modellnavn. Den eksisterende, signerte Boston-referansen i repoet var identitetsstøtte; repoets kreditering og bruksregler beholdes.

## Neste konkrete grafikkarbeid

Velg stil med brukeren fra de faktiske prøvene. Kontroller rom 9 med vanlig bevegelse langs den fremre skråveggen. Kontroller rom 22 med figur, forgrunnsmasker og begge obj171-tilstander før flere rom males.

For Boston: start med noen originale ruter for hvile og gange. Bevar hver rutes mål, silhuett og anker. Kontroller bildene med tools/check_hd_art.py før mod-bygging og vurder hele sekvensen i motoren. Et nytt figurkonsept alene er ikke en spritesanimasjon.
