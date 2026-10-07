# Notat: obj241_01

Status: Kandidat til kontroll. Ikke bekreftet trofast.

Dato: 2026-10-07T08:46:39+02:00 (Europe/Oslo).
Verktøy: image_gen.imagegen, innebygd ChatGPT bildegenerering. Verktøyet oppga ikke modellnavn eller modellversjon.
Antall forsøk: 2. Levert bilde er forsøk 1.
Prompt: Gjeldende prompt.txt ble brukt ordrett, inkludert avsluttende linjeskift. Referanse.png var bilde 1, og stil/room009_core.png var bilde 2.
Resultatet er kopiert uendret fra generatoren. Ingen etterbehandling, beskjæring, fargelås eller reparasjon av gråkanten er utført.

Generert kilde: /home/tombonator3000t/.codex/generated_images/01a105a8-96c5-7003-8874-45f031b6d721/exec-ec0db90b-6dc8-4d21-b8b8-ab39797cf1d1.png
PNG størrelse: 1536 x 1024, hele lerretet. PNG strukturen kunne leses og verifiseres.

Visuell sammenligning med referanse.png:
Tavlas store form, plassering og hoveddiagrammer følger referansen. Flere små graveringer og forbindelser er omtolket. Etter to forsøk var dette fortsatt usikkert. De nøyaktige gåtesymbolene er derfor ikke bekreftet bevart. Forsøk 1 er beholdt som det beste sammenligningsgrunnlaget. Bør ikke integreres før disse avvikene er avklart.
Den grå kanten er svakt teksturert og har fargevariasjon. Den er ikke bevart som jevn #808080.

Skrivebeskyttet geometrikontroll:
Kun eksisterende compare, judge og deres analysefunksjoner ble kjørt i minnet mot original_1x.png. Utsnittet ble hentet fra bilde_i_lerret i jobb.json. Dette endrer ingen leveranser eller status. dighd gpt-inn ble ikke kjørt.
Analysefil: pipeline/dighd/gpt.py fra canonical main, Git blob ca8a4eb967bb563197ae798c0cb44ed070417fd7.
Analysefil SHA256: 4960f0c53451492fc4e778b99e1dc364f45de1e45ca5ee0e03957586b4f65003

| Måling | Resultat |
| --- | --- |
| Skift x, originalpiksler | -0.05 |
| Skift y, originalpiksler | -0.16 |
| Største blokkskift, originalpiksler | 0.41 |
| Kantlikhet | 0.936 |
| Fargeavvik | 11.5 |
| Format | lerret |
| Dom fra analysefunksjonen | godkjent |

Denne automatiske dommen gjelder grov geometri. Den bekrefter ikke nøyaktige graveringer, fravær av nye stjerner eller korrekt gråkant, og er ingen godkjenning fra Claude eller Tom.
Paddingkontroll: 547396 av 548864 piksler utenfor bildeutsnittet avviker fra RGB 128,128,128. Kanalverdier i kanten: 9 til 212.

Sjekksummer av filene som faktisk ble brukt:

| Fil | SHA256 |
| --- | --- |
| referanse.png | fe5e47af29c72f034d103058a8c1bf4edabcb19b427fd0ca9d91cafba4f20c15 |
| original_1x.png | 111fe2b891bd7adc8c2338bcc27fe1017756a6f7db1930f790ebebe17ff8802c |
| prompt.txt | 8b0ef908a526f6bf12b5f7ebc846f80a4b05f1d0293e1d3b59925c470fbf6292 |
| stil/room009_core.png | fd37d46069b111b1f5c85bdfde9f429dbc5f8a7f8333efc9d24ab466fc6c2ba4 |
| resultat.png | 20962b0430c2cde9eb73149e748a9c3914e62770711037a6a3393f6ce7ec1a7e |

SHA256 for prompt.txt over gjelder hele filen inkludert siste linjeskift. jobb.json lagrer samme promptsjekksum uten det siste linjeskiftet. Inputfilene er beholdt uendret.
