# Notat: rom002_del3av3

Status: Kandidat til kontroll. Ikke bekreftet trofast.

Dato: 2026-10-07T08:46:39+02:00 (Europe/Oslo).
Verktøy: image_gen.imagegen, innebygd ChatGPT bildegenerering. Verktøyet oppga ikke modellnavn eller modellversjon.
Antall forsøk: 2. Levert bilde er forsøk 1.
Prompt: Gjeldende prompt.txt ble brukt ordrett, inkludert avsluttende linjeskift. Referanse.png var bilde 1, og stil/room009_core.png var bilde 2.
Resultatet er kopiert uendret fra generatoren. Ingen etterbehandling, beskjæring, fargelås eller reparasjon av gråkanten er utført.

Generert kilde: /home/tombonator3000t/.codex/generated_images/01a105a8-96c5-7003-8874-45f031b6d721/exec-c4823492-5edf-4949-9b22-b355796c0a8f.png
PNG størrelse: 1536 x 1024, hele lerretet. PNG strukturen kunne leses og verifiseres.

Visuell sammenligning med referanse.png:
Asteroidens silhuett og plassering følger hovedformen i referansen. Begge forsøk fikk flere små stjerner og blå dis. Flere stjerner er skarpere og større, og venstre kant på asteroiden er lysere. Noen kratere er omtolket. Dette bryter kravet om å bevare innhold og lys. Forsøk 1 er beholdt som det beste sammenligningsgrunnlaget. Bør ikke integreres før avvikene er avklart.
Den grå kanten er svakt teksturert og har fargevariasjon. Den er ikke bevart som jevn #808080.

Skrivebeskyttet geometrikontroll:
Kun eksisterende compare, judge og deres analysefunksjoner ble kjørt i minnet mot original_1x.png. Utsnittet ble hentet fra bilde_i_lerret i jobb.json. Dette endrer ingen leveranser eller status. dighd gpt-inn ble ikke kjørt.
Analysefil: pipeline/dighd/gpt.py fra canonical main, Git blob ca8a4eb967bb563197ae798c0cb44ed070417fd7.
Analysefil SHA256: 4960f0c53451492fc4e778b99e1dc364f45de1e45ca5ee0e03957586b4f65003

| Måling | Resultat |
| --- | --- |
| Skift x, originalpiksler | 0.03 |
| Skift y, originalpiksler | -0.01 |
| Største blokkskift, originalpiksler | 0.18 |
| Kantlikhet | 0.916 |
| Fargeavvik | 8.9 |
| Format | lerret |
| Dom fra analysefunksjonen | godkjent |

Denne automatiske dommen gjelder grov geometri. Den bekrefter ikke nøyaktige graveringer, fravær av nye stjerner eller korrekt gråkant, og er ingen godkjenning fra Claude eller Tom.
Paddingkontroll: 342298 av 344064 piksler utenfor bildeutsnittet avviker fra RGB 128,128,128. Kanalverdier i kanten: 106 til 142.

Sjekksummer av filene som faktisk ble brukt:

| Fil | SHA256 |
| --- | --- |
| referanse.png | 0ff8db94a2c81643ef80ff6ff9871fb743d3a5bb0538ede07c864ff942a21ac8 |
| original_1x.png | 7011c3644b4a722820e7fe986cbb0b1cb313626d2fe090b26fee1254f59ab7b4 |
| prompt.txt | f55577dfaea711bf35684cb30fb2f0e2834d87baf68a409987ab410a4a3ee4fe |
| stil/room009_core.png | fd37d46069b111b1f5c85bdfde9f429dbc5f8a7f8333efc9d24ab466fc6c2ba4 |
| resultat.png | f02e1ace5176a0673468bcdb4a99c2ccebd3ee75e26f0625afd2719f3f7b5177 |

SHA256 for prompt.txt over gjelder hele filen inkludert siste linjeskift. jobb.json lagrer samme promptsjekksum uten det siste linjeskiftet. Inputfilene er beholdt uendret.

Begrenset stjerneprøve:
Svart bakgrunn i delutsnitt [0, 0, 70, 200] målt i originalpiksler. Kandidaten ble bare analysert i minnet etter BOX nedskalering til 1x. Med terskel maks RGB over 40 ble sammenhengende lyspunkter i 8 naboretninger telt: referanse 10, kandidat 96. 10 kandidatpunktgrupper hadde et referansepunkt innen 1 originalpiksel, og 86 hadde ikke det. Dette er terskelavhengig diagnostikk av bare ett delutsnitt, ikke bevis for at alle stjerner er bevart. Forskjellene kan også påvirkes av endret lysstyrke.
Det store antallet ekstra lyspunkter støtter det synlige avviket med nye stjerner i denne kandidaten.
