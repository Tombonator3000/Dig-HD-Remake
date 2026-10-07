# Notat: rom006

Status: Kandidat til kontroll. Ikke bekreftet trofast.

Dato: 2026-10-07T08:50:03+02:00 (Europe/Oslo).
Verktøy: image_gen.imagegen, innebygd ChatGPT bildegenerering. Verktøyet oppga ikke modellnavn eller modellversjon.
Antall forsøk: 1. Levert bilde er forsøk 1.
Prompt: Gjeldende prompt.txt ble brukt ordrett, inkludert avsluttende linjeskift. Referanse.png var bilde 1, og stil/room009_core.png var bilde 2.
Resultatet er kopiert uendret fra generatoren. Ingen etterbehandling, beskjæring, fargelås eller reparasjon av gråkanten er utført.

Generert kilde: /home/tombonator3000t/.codex/generated_images/01a105a8-96c5-7003-8874-45f031b6d721/exec-5856e625-3ab1-46dd-a6a5-ca4896679f7e.png
PNG størrelse: 1536 x 1024, hele lerretet. PNG strukturen kunne leses og verifiseres.

Visuell sammenligning med referanse.png:
Asteroidens kontur og de store gropene følger referansen. Små riss, groper og overflateformer er omtegnet. Enkelte stjerner er blitt tydeligere. Full trofasthet for stjernepunktene er usikker. Den begrensede stjerneprøven nedenfor er ikke en godkjenning av hele bildet. Kandidaten må vurderes før integrasjon.
Den grå kanten er svakt teksturert og har fargevariasjon. Den er ikke bevart som jevn #808080.

Skrivebeskyttet geometrikontroll:
Kun eksisterende compare, judge og deres analysefunksjoner ble kjørt i minnet mot original_1x.png. Utsnittet ble hentet fra bilde_i_lerret i jobb.json. Dette endrer ingen leveranser eller status. dighd gpt-inn ble ikke kjørt.
Analysefil: pipeline/dighd/gpt.py fra canonical main, Git blob ca8a4eb967bb563197ae798c0cb44ed070417fd7.
Analysefil SHA256: 4960f0c53451492fc4e778b99e1dc364f45de1e45ca5ee0e03957586b4f65003.

| Måling | Resultat |
| --- | --- |
| Skift x, originalpiksler | 0.10 |
| Skift y, originalpiksler | -0.06 |
| Største blokkskift, originalpiksler | 0.42 |
| Kantlikhet | 0.968 |
| Fargeavvik | 8.3 |
| Format | lerret |
| Dom fra analysefunksjonen | godkjent |

Denne automatiske dommen gjelder grov geometri. Den bekrefter ikke nøyaktige overflateformer, fravær av nye stjerner eller korrekt gråkant, og er ingen godkjenning fra Claude eller Tom.
Paddingkontroll: 548852 av 548864 piksler utenfor bildeutsnittet avviker fra RGB 128,128,128. Kanalverdier i kanten: 110 til 134.

Sjekksummer av filene som faktisk ble brukt:

| Fil | SHA256 |
| --- | --- |
| referanse.png | 6f1d345bd051ce85b3d648a017f588e7b1b4dd5325be5901e6fda6ad2ac210ff |
| original_1x.png | a2d95722f3a647a69e07b918972ba4bad8315ca77c4fe3f276e1e857b3b5b23a |
| prompt.txt | c4d6f198738b9bccb0c8ace65a2fe958f950713f2e7922f6b07f2c707786ef36 |
| stil/room009_core.png | fd37d46069b111b1f5c85bdfde9f429dbc5f8a7f8333efc9d24ab466fc6c2ba4 |
| resultat.png | 51b819d7b9b1fca635e20934abcd7f651d38837ef126870600c03a6e3414a6a4 |

SHA256 for prompt.txt over gjelder hele filen inkludert siste linjeskift. jobb.json lagrer samme promptsjekksum uten det siste linjeskiftet. Inputfilene er beholdt uendret.

Begrenset stjerneprøve:
Svart bakgrunn i delutsnitt [0, 140, 160, 200] målt i originalpiksler. Kandidaten ble bare analysert i minnet etter BOX nedskalering til 1x. Med terskel maks RGB over 40 ble sammenhengende lyspunkter i 8 naboretninger telt: referanse 80, kandidat 79. 79 kandidatpunktgrupper hadde et referansepunkt innen 1 originalpiksel, og 0 hadde ikke det. Dette er terskelavhengig diagnostikk av bare ett delutsnitt, ikke bevis for at alle stjerner er bevart. Forskjellene kan også påvirkes av endret lysstyrke.
