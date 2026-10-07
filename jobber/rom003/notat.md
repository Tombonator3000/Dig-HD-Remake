# Notat: rom003

Status: Kandidat til kontroll. Ikke bekreftet trofast.

Dato: 2026-10-07T08:46:39+02:00 (Europe/Oslo).
Verktøy: image_gen.imagegen, innebygd ChatGPT bildegenerering. Verktøyet oppga ikke modellnavn eller modellversjon.
Antall forsøk: 1. Levert bilde er forsøk 1.
Prompt: Gjeldende prompt.txt ble brukt ordrett, inkludert avsluttende linjeskift. Referanse.png var bilde 1, og stil/room009_core.png var bilde 2.
Resultatet er kopiert uendret fra generatoren. Ingen etterbehandling, beskjæring, fargelås eller reparasjon av gråkanten er utført.

Generert kilde: /home/tombonator3000t/.codex/generated_images/01a105a8-96c5-7003-8874-45f031b6d721/exec-f719f362-e66f-4dfd-8598-aab47e7bf3e0.png
PNG størrelse: 1536 x 1024, hele lerretet. PNG strukturen kunne leses og verifiseres.

Visuell sammenligning med referanse.png:
Hovedformer, sti og steinplassering følger referansen. Små riss og overflatetekstur i steinen er tolket med flere detaljer. Ingen åpenbare nye stjerner, vann eller lyskilder ble sett ved sammenligningen. Nøyaktig bevaring av alle små riss er likevel ikke bekreftet. Kandidaten må vurderes før integrasjon.
Den grå kanten er svakt teksturert og har fargevariasjon. Den er ikke bevart som jevn #808080.

Skrivebeskyttet geometrikontroll:
Kun eksisterende compare, judge og deres analysefunksjoner ble kjørt i minnet mot original_1x.png. Utsnittet ble hentet fra bilde_i_lerret i jobb.json. Dette endrer ingen leveranser eller status. dighd gpt-inn ble ikke kjørt.
Analysefil: pipeline/dighd/gpt.py fra canonical main, Git blob ca8a4eb967bb563197ae798c0cb44ed070417fd7.
Analysefil SHA256: 4960f0c53451492fc4e778b99e1dc364f45de1e45ca5ee0e03957586b4f65003

| Måling | Resultat |
| --- | --- |
| Skift x, originalpiksler | 0.02 |
| Skift y, originalpiksler | -0.01 |
| Største blokkskift, originalpiksler | 0.16 |
| Kantlikhet | 0.950 |
| Fargeavvik | 7.4 |
| Format | lerret |
| Dom fra analysefunksjonen | godkjent |

Denne automatiske dommen gjelder grov geometri. Den bekrefter ikke nøyaktige graveringer, fravær av nye stjerner eller korrekt gråkant, og er ingen godkjenning fra Claude eller Tom.
Paddingkontroll: 548557 av 548864 piksler utenfor bildeutsnittet avviker fra RGB 128,128,128. Kanalverdier i kanten: 107 til 141.

Sjekksummer av filene som faktisk ble brukt:

| Fil | SHA256 |
| --- | --- |
| referanse.png | c404249a6c8f86d9f8d4776b30103607187563dbf9ee29febdb88a2e322d6598 |
| original_1x.png | 79a289af399e9119f5a082e14cb669e59bcce36480bda2443eb3b5589c87d6cd |
| prompt.txt | c4d6f198738b9bccb0c8ace65a2fe958f950713f2e7922f6b07f2c707786ef36 |
| stil/room009_core.png | fd37d46069b111b1f5c85bdfde9f429dbc5f8a7f8333efc9d24ab466fc6c2ba4 |
| resultat.png | e1f3733b981024c9a68399bba4324aecaee67a975e20e0994cea4a1054a2af5e |

SHA256 for prompt.txt over gjelder hele filen inkludert siste linjeskift. jobb.json lagrer samme promptsjekksum uten det siste linjeskiftet. Inputfilene er beholdt uendret.
