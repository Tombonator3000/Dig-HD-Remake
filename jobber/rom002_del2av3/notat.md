# Notat: rom002_del2av3

Status: Kandidat til kontroll. Ikke bekreftet trofast.

Dato: 2026-10-07T08:46:39+02:00 (Europe/Oslo).
Verktøy: image_gen.imagegen, innebygd ChatGPT bildegenerering. Verktøyet oppga ikke modellnavn eller modellversjon.
Antall forsøk: 2. Levert bilde er forsøk 1.
Prompt: Gjeldende prompt.txt ble brukt ordrett, inkludert avsluttende linjeskift. Referanse.png var bilde 1, og stil/room009_core.png var bilde 2.
Resultatet er kopiert uendret fra generatoren. Ingen etterbehandling, beskjæring, fargelås eller reparasjon av gråkanten er utført.

Generert kilde: /home/tombonator3000t/.codex/generated_images/01a105a8-96c5-7003-8874-45f031b6d721/exec-5a3c8cb0-3a43-4793-8771-4f95cf6ff065.png
PNG størrelse: 1536 x 1024, hele lerretet. PNG strukturen kunne leses og verifiseres.

Visuell sammenligning med referanse.png:
Solen og romskipdelen følger omtrent originalens plassering og hovedform. Begge forsøk fikk flere små stjerner og tydeligere blå dis enn referansen. Enkelte stjerner ble også større og mer markerte. Dette bryter kravet om å bevare innholdet. Forsøk 1 er beholdt som det beste sammenligningsgrunnlaget. Bør ikke integreres før avvikene er avklart.
Den grå kanten er svakt teksturert og har fargevariasjon. Den er ikke bevart som jevn #808080.

Skrivebeskyttet geometrikontroll:
Kun eksisterende compare, judge og deres analysefunksjoner ble kjørt i minnet mot original_1x.png. Utsnittet ble hentet fra bilde_i_lerret i jobb.json. Dette endrer ingen leveranser eller status. dighd gpt-inn ble ikke kjørt.
Analysefil: pipeline/dighd/gpt.py fra canonical main, Git blob ca8a4eb967bb563197ae798c0cb44ed070417fd7.
Analysefil SHA256: 4960f0c53451492fc4e778b99e1dc364f45de1e45ca5ee0e03957586b4f65003

| Måling | Resultat |
| --- | --- |
| Skift x, originalpiksler | -0.03 |
| Skift y, originalpiksler | -0.02 |
| Største blokkskift, originalpiksler | 0.07 |
| Kantlikhet | 0.980 |
| Fargeavvik | 5.2 |
| Format | lerret |
| Dom fra analysefunksjonen | godkjent |

Denne automatiske dommen gjelder grov geometri. Den bekrefter ikke nøyaktige graveringer, fravær av nye stjerner eller korrekt gråkant, og er ingen godkjenning fra Claude eller Tom.
Paddingkontroll: 343980 av 344064 piksler utenfor bildeutsnittet avviker fra RGB 128,128,128. Kanalverdier i kanten: 100 til 131.

Sjekksummer av filene som faktisk ble brukt:

| Fil | SHA256 |
| --- | --- |
| referanse.png | f40964cb92924f212ebda7a247d1292cfa2ecdc2d95a3cf4d8c0295429d11ae1 |
| original_1x.png | 52b0f70c48c2e148206c5fa6d7694be3bf29799f979e0d1798181c86b45f239b |
| prompt.txt | 5d85b2d12e6e01eca5b38e4c3b729d99aae0d07998eb5ab889e19637697b7017 |
| stil/room009_core.png | fd37d46069b111b1f5c85bdfde9f429dbc5f8a7f8333efc9d24ab466fc6c2ba4 |
| resultat.png | 9c3eca5bb4bd9c0a852dd8b7175c6a90d665e6aa81b2ac7a7b973fff516a157c |

SHA256 for prompt.txt over gjelder hele filen inkludert siste linjeskift. jobb.json lagrer samme promptsjekksum uten det siste linjeskiftet. Inputfilene er beholdt uendret.

Begrenset stjerneprøve:
Svart bakgrunn i delutsnitt [100, 90, 300, 190] målt i originalpiksler. Kandidaten ble bare analysert i minnet etter BOX nedskalering til 1x. Med terskel maks RGB over 40 ble sammenhengende lyspunkter i 8 naboretninger telt: referanse 10, kandidat 94. 10 kandidatpunktgrupper hadde et referansepunkt innen 1 originalpiksel, og 84 hadde ikke det. Dette er terskelavhengig diagnostikk av bare ett delutsnitt, ikke bevis for at alle stjerner er bevart. Forskjellene kan også påvirkes av endret lysstyrke.
Det store antallet ekstra lyspunkter støtter det synlige avviket med nye stjerner i denne kandidaten.
