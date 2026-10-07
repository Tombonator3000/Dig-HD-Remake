# Notat: rom004

Status: Kandidat til kontroll. Ikke bekreftet trofast.

Dato: 2026-10-07T08:47:48+02:00 (Europe/Oslo).
Verktøy: image_gen.imagegen, innebygd ChatGPT bildegenerering. Verktøyet oppga ikke modellnavn eller modellversjon.
Antall forsøk: 1. Levert bilde er forsøk 1.
Prompt: Gjeldende prompt.txt ble brukt ordrett, inkludert avsluttende linjeskift. Referanse.png var bilde 1, og stil/room009_core.png var bilde 2.
Resultatet er kopiert uendret fra generatoren. Ingen etterbehandling, beskjæring, fargelås eller reparasjon av gråkanten er utført.

Generert kilde: /home/tombonator3000t/.codex/generated_images/01a105a8-96c5-7003-8874-45f031b6d721/exec-b05dbd89-0725-4c20-9eab-e30e8001b0a5.png
PNG størrelse: 1536 x 1024, hele lerretet. PNG strukturen kunne leses og verifiseres.

Visuell sammenligning med referanse.png:
De store steinformene og silhuetten følger referansen. Overflatestruktur og små groper er omtegnet med mer detalj. Bakgrunnen har flere fine lyspunkter som kan være nye stjerner, men dette er ikke bekreftet med kontroll av hvert enkelt punkt. Nøyaktig bevaring av stjerner og små former er usikker. Kandidaten må vurderes før integrasjon.
Den grå kanten er svakt teksturert og har fargevariasjon. Den er ikke bevart som jevn #808080.

Skrivebeskyttet geometrikontroll:
Kun eksisterende compare, judge og deres analysefunksjoner ble kjørt i minnet mot original_1x.png. Utsnittet ble hentet fra bilde_i_lerret i jobb.json. Dette endrer ingen leveranser eller status. dighd gpt-inn ble ikke kjørt.
Analysefil: pipeline/dighd/gpt.py fra canonical main, Git blob ca8a4eb967bb563197ae798c0cb44ed070417fd7.
Analysefil SHA256: 4960f0c53451492fc4e778b99e1dc364f45de1e45ca5ee0e03957586b4f65003.

| Måling | Resultat |
| --- | --- |
| Skift x, originalpiksler | -0.12 |
| Skift y, originalpiksler | -0.21 |
| Største blokkskift, originalpiksler | 0.46 |
| Kantlikhet | 0.968 |
| Fargeavvik | 7.6 |
| Format | lerret |
| Dom fra analysefunksjonen | godkjent |

Denne automatiske dommen gjelder grov geometri. Den bekrefter ikke nøyaktige overflateformer, fravær av nye stjerner eller korrekt gråkant, og er ingen godkjenning fra Claude eller Tom.
Paddingkontroll: 548776 av 548864 piksler utenfor bildeutsnittet avviker fra RGB 128,128,128. Kanalverdier i kanten: 106 til 137.

Sjekksummer av filene som faktisk ble brukt:

| Fil | SHA256 |
| --- | --- |
| referanse.png | c9b7a0505cc944f11696994e0fafeca328945172ef9a57bb6168933f027049af |
| original_1x.png | 1df8123612dda7b9be70af0713dc45f1871192ecffa7c896c8d6ba613bc53cf2 |
| prompt.txt | c4d6f198738b9bccb0c8ace65a2fe958f950713f2e7922f6b07f2c707786ef36 |
| stil/room009_core.png | fd37d46069b111b1f5c85bdfde9f429dbc5f8a7f8333efc9d24ab466fc6c2ba4 |
| resultat.png | 837f119e556cb122a11a4d7e9c7142d7ae66256b17503701c6be1e9eb3afd744 |

SHA256 for prompt.txt over gjelder hele filen inkludert siste linjeskift. jobb.json lagrer samme promptsjekksum uten det siste linjeskiftet. Inputfilene er beholdt uendret.

Begrenset stjerneprøve:
Svart bakgrunn i delutsnitt [0, 0, 60, 200] målt i originalpiksler. Kandidaten ble bare analysert i minnet etter BOX nedskalering til 1x. Med terskel maks RGB over 40 ble sammenhengende lyspunkter i 8 naboretninger telt: referanse 105, kandidat 82. 81 kandidatpunktgrupper hadde et referansepunkt innen 1 originalpiksel, og 1 hadde ikke det. Dette er terskelavhengig diagnostikk av bare ett delutsnitt, ikke bevis for at alle stjerner er bevart. Forskjellene kan også påvirkes av endret lysstyrke.
