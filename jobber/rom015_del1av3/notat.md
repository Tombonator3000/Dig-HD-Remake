# Notat: rom015_del1av3

Status: Kandidat til kontroll. Ikke bekreftet trofast.

Dato: 2026-10-07T09:09:27+02:00 (Europe/Oslo).
Verktøy: image_gen.imagegen, innebygd ChatGPT bildegenerering. Modellnavn og modellversjon ble ikke oppgitt.
Antall forsøk: 2. Valgt forsøk: 2.
Bilde 2 var stil/room022_beach.png i forsøk 1 og stil/room009_core.png i valgt forsøk 2.
Gjeldende prompt.txt ble brukt ordrett, inkludert avsluttende linjeskift. Referanse.png var bilde 1.
Resultatet er kopiert uendret fra generatoren. Ingen etterbehandling, fargelås eller kantreparasjon.
Generert kilde: /home/tombonator3000t/.codex/generated_images/01a105a8-96c5-7003-8874-45f031b6d721/exec-1e2d4f03-13d2-459a-a3a3-f94a4beeee93.png
PNG størrelse: 1536 x 1024. PNG strukturen kunne dekodes og verifiseres.

Visuell kontroll:
Pyramidens kant og de store månene ligger omtrent som i referansen. Stjerneglans er sterkere og har skarpere stråler. Månens mørke side og kraterdetaljer er fortolket, og steinflatens riss er tydeligere. Andre forsøk er valgt med lavere fargeavvik, 5,2 mot 6,7, og flere posisjonstreff i en begrenset stjerneprobe.
Stjerneprobe: originalutsnitt x260,y0,x320,y190, kandidaten redusert til 1x med BOX. Ved maxRGB over 40 og 8-sammenhengende lyspunktøyer var det 163 referansepunkter, 171 i forsøk 1 og 169 i forsøk 2. Henholdsvis 149 og 155 kandidatpunkter lå innen 1 originalpiksel fra referansepunktene. De øvrige 22 og 14 hadde alle en 3 x 3 referansenabo med maxRGB minst 30. Ved terskel 60 var punktantallene 50 i referansen og 45/52 i forsøkene. Resultatet er terskelavhengig og kan skyldes forsterket lysstyrke og endret komponentdeling. Proben bekrefter ikke nye posisjoner og godkjenner ikke hele stjernefeltet. Stjernene, månedetaljene og rissene må kontrolleres videre før integrasjon.
Gråkanten er teksturert og ikke jevn #808080.

Skrivebeskyttet geometrikontroll:
compare/judge fra canonical pipeline/dighd/gpt.py, Git blob ca8a4eb967bb563197ae798c0cb44ed070417fd7, ble kjørt i minnet mot original_1x.png med metadatautsnittet. dighd gpt-inn ble ikke kjørt.
Skift x/y: -0.04/0.00 originalpiksler. Blokk maksimum: 0.37. Kantlikhet: 0.925. Fargeavvik: 5.2. Format: lerret. Automatisk dom: godkjent.
Dommen gjelder grov geometri og er ingen trofastgodkjenning eller godkjenning fra Claude/Tom.
Gråkant: 261775 av 262144 piksler avviker fra RGB 128,128,128. Kanalverdier: 109 til 138.

| Fil | SHA256 |
| --- | --- |
| referanse.png | a8654b56cd810b6ea3707ad18db876b89ebf14dec21e11712977fab15ea789bc |
| original_1x.png | 0d3d856e6d25d9bf385fec2d212a0542ca6030463c011a4a10483f6582167868 |
| prompt.txt | 1d2af6b504387b45886c897ee0c6a0ed70e5c43916886fff90e0f66d7eb59751 |
| stil/room022_beach.png | 08796e71cd07d91b4a6773cc383c8589bd1f69f491d7e20c8f9f01b2f296f39f |
| stil/room009_core.png | fd37d46069b111b1f5c85bdfde9f429dbc5f8a7f8333efc9d24ab466fc6c2ba4 |
| resultat.png | c5d7c9c9820dfd34813246b23f45f0d4a7563f16e2c2421684f12c45855bea18 |

Promptsjekksummen over gjelder hele filen med siste linjeskift. Metadata bruker samme tekst uten siste linjeskift. Inputfilene er beholdt uendret.
