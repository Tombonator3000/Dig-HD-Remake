# Notat: rom011

Status: Kandidat til kontroll. Ikke bekreftet trofast.

Dato: 2026-10-07T09:00:17+02:00 (Europe/Oslo).
Verktøy: image_gen.imagegen, innebygd ChatGPT bildegenerering. Modellnavn og modellversjon ble ikke oppgitt.
Antall forsøk: 2. Valgt forsøk: 2.
Bilde 2 var stil/room009_core.png i forsøk 1 og stil/room022_beach.png i valgt forsøk 2.
Gjeldende prompt.txt ble brukt ordrett, inkludert avsluttende linjeskift. Referanse.png var bilde 1.
Resultatet er kopiert uendret fra generatoren. Ingen etterbehandling, fargelås eller kantreparasjon.
Generert kilde: /home/tombonator3000t/.codex/generated_images/01a105a8-96c5-7003-8874-45f031b6d721/exec-a8f12b21-bc28-447e-973c-c4bc0f6024a8.png
PNG størrelse: 1536 x 1024. PNG strukturen kunne dekodes og verifiseres.

Visuell kontroll:
Hovedoppsettet følger referansen. Den lille steinen ved høyre oppstående stein er rundere, og de grønne tegnene er tolket om. Små riss og flatestruktur er også tolket på nytt. Forsøk 2 er valgt fordi blokkskiftet var mindre (0.16 mot 0.42), fargeavviket lavere (7.8 mot 8.4) og samlet skift mindre. Kantlikheten er litt lavere enn i forsøk 1 (0.935 mot 0.950). Tegnenes nøyaktighet og den lille steinformen må avklares før integrasjon.
Gråkanten er teksturert og ikke jevn #808080.

Skrivebeskyttet geometrikontroll:
compare/judge fra canonical pipeline/dighd/gpt.py, Git blob ca8a4eb967bb563197ae798c0cb44ed070417fd7, ble kjørt i minnet mot original_1x.png med metadatautsnittet. dighd gpt-inn ble ikke kjørt.
Skift x/y: -0.00/-0.03 originalpiksler. Blokk maksimum: 0.16. Kantlikhet: 0.935. Fargeavvik: 7.8. Format: lerret. Automatisk dom: godkjent.
Dommen gjelder grov geometri og er ingen trofastgodkjenning eller godkjenning fra Claude/Tom.
Gråkant: 547174 av 548864 piksler avviker fra RGB 128,128,128. Kanalverdier: 102 til 147.

| Fil | SHA256 |
| --- | --- |
| referanse.png | b4383ee7c4131821f931b1d23d87e983fbcff7a39aa57aca55f364aa399452f5 |
| original_1x.png | 4eacc23db66eb159a7ea7e5c29cb3f60b4cc5aa5bc2cc77cd00933a10907ec95 |
| prompt.txt | c4d6f198738b9bccb0c8ace65a2fe958f950713f2e7922f6b07f2c707786ef36 |
| stil/room009_core.png | fd37d46069b111b1f5c85bdfde9f429dbc5f8a7f8333efc9d24ab466fc6c2ba4 |
| stil/room022_beach.png | 08796e71cd07d91b4a6773cc383c8589bd1f69f491d7e20c8f9f01b2f296f39f |
| resultat.png | 3480c199b110010416d88eabfa1c8cb20c07823441b2dda9bf6146d5c7b42a85 |

Promptsjekksummen over gjelder hele filen med siste linjeskift. Metadata bruker samme tekst uten siste linjeskift. Inputfilene er beholdt uendret.
