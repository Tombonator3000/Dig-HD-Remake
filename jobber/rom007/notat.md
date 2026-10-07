# Notat: rom007

Status: Kandidat til kontroll. Ikke bekreftet trofast.

Dato: 2026-10-07T08:52:17+02:00 (Europe/Oslo).
Verktøy: image_gen.imagegen, innebygd ChatGPT bildegenerering. Verktøyet oppga ikke modellnavn eller modellversjon.
Antall forsøk: 1. Levert bilde er forsøk 1.
Prompt: Gjeldende prompt.txt ble brukt ordrett, inkludert avsluttende linjeskift. Referanse.png var bilde 1, og stil/room009_core.png var bilde 2.
Resultatet er kopiert uendret fra generatoren. Ingen etterbehandling, beskjæring, fargelås eller reparasjon av gråkanten er utført.

Generert kilde: /home/tombonator3000t/.codex/generated_images/01a105a8-96c5-7003-8874-45f031b6d721/exec-9cb9fb4a-e928-46be-b793-fa44995b1edc.png
PNG størrelse: 1536 x 1024, hele lerretet. PNG strukturen kunne leses og verifiseres.

Visuell sammenligning med referanse.png:
Steinens store kontur og hovedgroper følger referansen. Små riss og overflatestruktur er omtegnet med mer detalj. Stjernepunktene ser forholdsvis nær referansen ut, men hvert enkelt punkt er ikke kontrollert. Ingen åpenbart nytt vann eller nye lyskilder ble sett. Full trofasthet for små former og stjerner er usikker. Kandidaten må vurderes før integrasjon.
Den grå kanten er svakt teksturert og har fargevariasjon. Den er ikke bevart som jevn #808080.

Skrivebeskyttet geometrikontroll:
Kun eksisterende compare, judge og deres analysefunksjoner ble kjørt i minnet mot original_1x.png. Utsnittet ble hentet fra bilde_i_lerret i jobb.json. Dette endrer ingen leveranser eller status. dighd gpt-inn ble ikke kjørt.
Analysefil: pipeline/dighd/gpt.py fra canonical main, Git blob ca8a4eb967bb563197ae798c0cb44ed070417fd7.
Analysefil SHA256: 4960f0c53451492fc4e778b99e1dc364f45de1e45ca5ee0e03957586b4f65003.

| Måling | Resultat |
| --- | --- |
| Skift x, originalpiksler | -0.04 |
| Skift y, originalpiksler | -0.01 |
| Største blokkskift, originalpiksler | 0.47 |
| Kantlikhet | 0.946 |
| Fargeavvik | 7.6 |
| Format | lerret |
| Dom fra analysefunksjonen | godkjent |

Denne automatiske dommen gjelder grov geometri. Den bekrefter ikke nøyaktige overflateformer, fravær av nye stjerner, korrekt lys eller korrekt gråkant, og er ingen godkjenning fra Claude eller Tom.
Paddingkontroll: 548808 av 548864 piksler utenfor bildeutsnittet avviker fra RGB 128,128,128. Kanalverdier i kanten: 19 til 158.

Sjekksummer av filene som faktisk ble brukt:

| Fil | SHA256 |
| --- | --- |
| referanse.png | c6d5da8b5daa87236f2ce92cb322281112818ef93c018fe39cf5e1ef836b05d0 |
| original_1x.png | 070d27adf51ebd136b4c36ab7e82abc149cfb5e419526c62ec2cdeed1d2470f0 |
| prompt.txt | c4d6f198738b9bccb0c8ace65a2fe958f950713f2e7922f6b07f2c707786ef36 |
| stil/room009_core.png | fd37d46069b111b1f5c85bdfde9f429dbc5f8a7f8333efc9d24ab466fc6c2ba4 |
| resultat.png | 583e5a100700d38b537d1ec3c02125173eac44ed650369d5241ce91f9b8a4c41 |

SHA256 for prompt.txt over gjelder hele filen inkludert siste linjeskift. jobb.json lagrer samme promptsjekksum uten det siste linjeskiftet. Inputfilene er beholdt uendret.
