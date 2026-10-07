# Notat: rom008

Status: Kandidat til kontroll. Ikke bekreftet trofast.

Dato: 2026-10-07T08:52:17+02:00 (Europe/Oslo).
Verktøy: image_gen.imagegen, innebygd ChatGPT bildegenerering. Verktøyet oppga ikke modellnavn eller modellversjon.
Antall forsøk: 1. Levert bilde er forsøk 1.
Prompt: Gjeldende prompt.txt ble brukt ordrett, inkludert avsluttende linjeskift. Referanse.png var bilde 1, og stil/room009_core.png var bilde 2.
Resultatet er kopiert uendret fra generatoren. Ingen etterbehandling, beskjæring, fargelås eller reparasjon av gråkanten er utført.

Generert kilde: /home/tombonator3000t/.codex/generated_images/01a105a8-96c5-7003-8874-45f031b6d721/exec-acfe8374-af19-4f80-8d43-9fa8ceadacb7.png
PNG størrelse: 1536 x 1024, hele lerretet. PNG strukturen kunne leses og verifiseres.

Visuell sammenligning med referanse.png:
Steinkonturene, gropen og hovedformene følger referansen. Fin overflatestruktur er omtegnet. Solens plassering er bevart, men strålene er sterkere og mer markerte enn i originalen. Ingen helt ny lyskilde ble sett. Nøyaktig bevaring av lys og små former er ikke bekreftet. Kandidaten må vurderes før integrasjon.
Den grå kanten er svakt teksturert og har fargevariasjon. Den er ikke bevart som jevn #808080.

Skrivebeskyttet geometrikontroll:
Kun eksisterende compare, judge og deres analysefunksjoner ble kjørt i minnet mot original_1x.png. Utsnittet ble hentet fra bilde_i_lerret i jobb.json. Dette endrer ingen leveranser eller status. dighd gpt-inn ble ikke kjørt.
Analysefil: pipeline/dighd/gpt.py fra canonical main, Git blob ca8a4eb967bb563197ae798c0cb44ed070417fd7.
Analysefil SHA256: 4960f0c53451492fc4e778b99e1dc364f45de1e45ca5ee0e03957586b4f65003.

| Måling | Resultat |
| --- | --- |
| Skift x, originalpiksler | 0.02 |
| Skift y, originalpiksler | 0.02 |
| Største blokkskift, originalpiksler | 0.10 |
| Kantlikhet | 0.965 |
| Fargeavvik | 9.4 |
| Format | lerret |
| Dom fra analysefunksjonen | godkjent |

Denne automatiske dommen gjelder grov geometri. Den bekrefter ikke nøyaktige overflateformer, fravær av nye stjerner, korrekt lys eller korrekt gråkant, og er ingen godkjenning fra Claude eller Tom.
Paddingkontroll: 548614 av 548864 piksler utenfor bildeutsnittet avviker fra RGB 128,128,128. Kanalverdier i kanten: 103 til 139.

Sjekksummer av filene som faktisk ble brukt:

| Fil | SHA256 |
| --- | --- |
| referanse.png | 4096d5ef65920362a3c733f7a8d880e4c411a7c15ca9124513aa97e432fda126 |
| original_1x.png | f7ab58549a665b75696976533de2161d7242cb2b9e05512e8ff29385be242f9a |
| prompt.txt | c4d6f198738b9bccb0c8ace65a2fe958f950713f2e7922f6b07f2c707786ef36 |
| stil/room009_core.png | fd37d46069b111b1f5c85bdfde9f429dbc5f8a7f8333efc9d24ab466fc6c2ba4 |
| resultat.png | a6ed5ced63c28b5bc51c01c1fcb2cb3f4d184d8471ed7f4bd026b6c9cd96bb87 |

SHA256 for prompt.txt over gjelder hele filen inkludert siste linjeskift. jobb.json lagrer samme promptsjekksum uten det siste linjeskiftet. Inputfilene er beholdt uendret.
