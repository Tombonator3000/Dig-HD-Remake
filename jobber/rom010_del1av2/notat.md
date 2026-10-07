# Notat: rom010_del1av2

Status: Kandidat til kontroll. Ikke bekreftet trofast.

Dato: 2026-10-07T08:52:17+02:00 (Europe/Oslo).
Verktøy: image_gen.imagegen, innebygd ChatGPT bildegenerering. Verktøyet oppga ikke modellnavn eller modellversjon.
Antall forsøk: 2. Levert bilde er forsøk 2.
Prompt: Gjeldende prompt.txt ble brukt ordrett, inkludert avsluttende linjeskift. Referanse.png var bilde 1, og stil/room022_beach.png var bilde 2.
Resultatet er kopiert uendret fra generatoren. Ingen etterbehandling, beskjæring, fargelås eller reparasjon av gråkanten er utført.

Generert kilde: /home/tombonator3000t/.codex/generated_images/01a105a8-96c5-7003-8874-45f031b6d721/exec-628e8a46-5b4a-4847-b305-124e66982653.png
PNG størrelse: 1536 x 1024, hele lerretet. PNG strukturen kunne leses og verifiseres.

Visuell sammenligning med referanse.png:
De store steinveggene og planetens plassering følger hovedformen i referansen. Begge forsøk fikk flere lyspunkter og stjerner, samt sterkere rød steinglød enn originalen. Planetens små detaljer er også tolket på nytt. Forsøk 2 er beholdt fordi det virker litt roligere enn forsøk 1. Dette er fortsatt et tydelig avvik fra kravet om samme innhold og lys. Bør ikke integreres før avvikene er avklart.
Den grå kanten er svakt teksturert og har fargevariasjon. Den er ikke bevart som jevn #808080.

Skrivebeskyttet geometrikontroll:
Kun eksisterende compare, judge og deres analysefunksjoner ble kjørt i minnet mot original_1x.png. Utsnittet ble hentet fra bilde_i_lerret i jobb.json. Dette endrer ingen leveranser eller status. dighd gpt-inn ble ikke kjørt.
Analysefil: pipeline/dighd/gpt.py fra canonical main, Git blob ca8a4eb967bb563197ae798c0cb44ed070417fd7.
Analysefil SHA256: 4960f0c53451492fc4e778b99e1dc364f45de1e45ca5ee0e03957586b4f65003.

| Måling | Resultat |
| --- | --- |
| Skift x, originalpiksler | 0.01 |
| Skift y, originalpiksler | 0.03 |
| Største blokkskift, originalpiksler | 0.15 |
| Kantlikhet | 0.966 |
| Fargeavvik | 9.8 |
| Format | lerret |
| Dom fra analysefunksjonen | godkjent |

Denne automatiske dommen gjelder grov geometri. Den bekrefter ikke nøyaktige overflateformer, fravær av nye stjerner, korrekt lys eller korrekt gråkant, og er ingen godkjenning fra Claude eller Tom.
Paddingkontroll: 259101 av 262144 piksler utenfor bildeutsnittet avviker fra RGB 128,128,128. Kanalverdier i kanten: 114 til 139.

Sjekksummer av filene som faktisk ble brukt:

| Fil | SHA256 |
| --- | --- |
| referanse.png | f74264c7b3305661a733cbe2839999d923c1ae5938dade7b733a40f38d8e8eae |
| original_1x.png | 857d04777090fd74c2a7c3c255dfdb5c4026103de1973d9acf36a1471cebd752 |
| prompt.txt | 89329a16363ea55f409b091037451057093f9a8a50dfd487f16b1520195bb2a3 |
| stil/room022_beach.png | 08796e71cd07d91b4a6773cc383c8589bd1f69f491d7e20c8f9f01b2f296f39f |
| resultat.png | 4de1113e64fa8401ea3583056f54d0d70cf51b0ba64becd7d6b1ff7d8ae3e9b5 |

SHA256 for prompt.txt over gjelder hele filen inkludert siste linjeskift. jobb.json lagrer samme promptsjekksum uten det siste linjeskiftet. Inputfilene er beholdt uendret.
