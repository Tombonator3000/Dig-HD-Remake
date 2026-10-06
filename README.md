# Grafikkpilot for The Dig HD, 6. oktober 2026

Denne pakken inneholder to HD-bakgrunnskandidater laget fra originale rombilder og en separat Boston Low-stilreferanse. Begge bakgrunnene er lastet og inspisert i den faktiske ScummVM-forken på laptopen med SDL2, Wayland, OpenGL og 32-bits farger. Stilen er foreløpig.

## Innhold og dekning

| Fil | Kilde | Mål | Status |
| --- | --- | --- | --- |
| assets/rooms/room009.png | Rom 9, core, 320x200 | 1280x800 RGB | Kandidat. Gulvhjørnet korrigert i andre generering. |
| assets/rooms/room022.png | Rom 22, beach, 320x200 | 1280x800 RGB | Kandidat. Motoren beholder fargesyklet vann fra originalen. |
| concepts/boston-low-cel001.png | Kostyme 14, rute 1, 21x65 | 713x2205 RGBA | Stilreferanse. Silhuettkontrollen avviser direkte spritesbruk. |

Det er laget kandidater for 2 av 111 rom. Ingen nye objektbilder, godkjente spritesanimasjoner eller filmrammer er produsert. De to objektbildene i mod/ er originalene skalert med nearest. Boston-prøven ligger utenfor mod/ og assets/.

mod/ er en komplett, avgrenset testmod med de to bakgrunnene, deres uendrede indeksbilder og to objektvarianter fra originalen. Resten av spillet vises av motorens vanlige fallback. Originaldata og motorpatch er beholdt.

## Kjør prøven

Fra prosjektroten, når spillfilene og den patchede motoren er på plass:

```sh
DIGHD_MOD="$PWD/work/graphics-pilot-20261006/mod" engine/scummvm/scummvm --path="$PWD/game" --gfx-mode=opengl --aspect-ratio dig
```

Begynn et vanlig spill for å vurdere interaksjoner og forgrunnsmasker. De dokumenterte kjøringene under brukte motorens testhook for å hoppe til rommene. De er ikke en full gjennomspilling.

## Verifikasjon

- Spillfilenes SHA-256-kontroll fra grenen spilldata bestod. DIG.LA0 er standardutgaven med MD5 d8323015ecb8b10bf53474f6e6b0ae33.
- Motoren er bygd fra prosjektets låste ScummVM-commit c9091321060acfc8f037767c18f8279a86305b7e og uendret patch fra kodecommit 70aed0523ff624cb6176d9b5911cdc1fdef0f336.
- Pipeline: 4 tester bestod, inkludert telling mot de ekte spillfilene.
- Begge egne rombilder består kontroll av størrelse, RGB-format og originalindeks. Generatorens 1586x992-bilder ble teknisk tilpasset til 1280x800 med Lanczos uten beskjæring. Dette var formattilpasning, ikke maling.
- Native nearest-kontroll i rom 9 og 22: 0 piksler med sterke avvik etter motorens terskel på mer enn 48 i en fargekanal. Dette er ikke en påstand om byteidentiske skjermbilder.
- Begge nye bakgrunner: exit 0, innlasting bekreftet, 1280x800 og 4 byte per piksel. Se qa/runtime/final-results.json og de uredigerte frame_000480_roomNNN.png-filene i roomNNN-final-hd/.
- Negativ kontroll: original generatorstørrelse avvises før mod-bygging. Boston-prøven avvises fordi alfasilhuetten avviker fra originalen ved motorens terskel 128. Se qa/rejected-size.json og qa/sprite-preflight.json.

De første testhoppene med SDL dummy ved bilde 60 ble overstyrt av spillets oppstartsskript og endte i rom 2. De dokumenterer ikke de bestilte rommene. Native kontroll ved bilde 240 løste dette. Forsøkslogger er bevart for sporbarhet.

## Visuelle funn og videre arbeid

Asteroidrommets gulvhjørne flyttet seg i første generering. Det ble korrigert mot originalens geometri i andre generering og inspisert i motoren. Helt nøyaktig registrering langs alle forgrunnsmasker er fortsatt ikke godkjent gjennom manuell bevegelse.

Kysten viser både det malte HD-bildet og originale blokker i fargesyklede områder. Den avgrensede kjøringen tegnet ikke obj171-variantene eller en figur i dette rommet. Sømmer ved objektbytte, figurkontakt og full forgrunnsokklusjon gjenstår å kontrollere. Dette er en stil- og integrasjonsprøve.

Boston-prøven kan brukes til å vurdere ansikt, klær og farger. En ekte spriteserie må følge hver originalrutes kroppsvinkel, silhuett, mål og anker før alle bevegelser kontrolleres i spillet. Ingen slik serie er levert her.

Musikk og tale mangler lokalt. Bildetestene var dempet. Lyd og hele brukerreisen er ikke testet.

## Kilder

reference/ inneholder de uendrede uttrukne kildebildene og indeksbildene. generated/ inneholder generatorens originale rombilder og første rom 9-forsøk. prompts.json har de fullstendige promptene og beskriver hvert referansebildes rolle. Den innebygde ChatGPT-bildegeneratoren ble brukt. Verktøyet oppga ikke et eksakt modellnavn.

Boston bruker den eksisterende, signerte Boston-referansen i repoet som identitetsstøtte. Eksisterende kreditering og regler for konseptbildene i README.md gjelder videre. The Dig og originalgrafikken tilhører Disney/Lucasfilm.

Hele denne pakken er avledet grafikk eller dokumentasjon av den. Den skal bli i den separate private grafikkdatagrenen og aldri flettes inn i main.
