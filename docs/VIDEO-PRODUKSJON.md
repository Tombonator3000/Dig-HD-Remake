# Produksjon av de resterende HD-filmene

16. oktober 2026. Leveranse: [PR 60 mot hd-mod](https://github.com/Tombonator3000/Dig-HD-Remake/pull/60).

Alle 54 resterende SAN-filer er behandlet, én om gangen i rekkefølgen nedenfor. 8866 nye rammer i 1280 x 800 og 86.66 MB VP8/IVF. Med publisert SQ1 er alle 55 filmer og 12 638 rammer produsert, 109.43 MB video i alt. Ingen PNG-videorammer er lagt i repoet.

Køen tok SQ-numrene i naturlig nummerrekkefølge, deretter øvrige filnavn. Original SAN styrer fortsatt avspilling, lyd, undertekster og skript. SQ3 har 14 fps og SQ19A 15 fps; resten har 12 fps.

## Metode og kontroll

- AnimeSR v2 FP32, 4x, åtte oppvarmingsrammer per klipp. Den offisielle inferensen brukes med en skrivekø på maksimalt seks CPU-rammer.
- Klipp oppdages ved minst 20/255 i gjennomsnittlig RGB-endring mellom originalrammene. Den tidligere godkjente SQ5-masteren med manuelle klipp er gjenbrukt. SQ1 er uendret.
- SQ14SC07 har 33 SAN-rammer, men bare 32 bilder fra FFmpeg: første SAN-ramme er tom. Denne plassen bevares med første palettfarge, og de neste bildene får indeks 1 til 32.
- Alle nye IVF-filer er dekodet i sin helhet med FFmpeg; dimensjoner, rammeantall, synlige pakker og sammenhengende tidsstempler er kontrollert.
- SSIM mot AnimeSR-masteren i YUV420P er minst 0,98, lavest 0,980303. Sju effektsekvenser ble kodet om med høyere bitrate.
- Motorens faktiske DigHDVideo-dekoder har lest alle 8866 nye rammer i RGB32, prøvd de første fem per film i RGB565, gjentatte rammer og hopp bakover. Alt bestått.
- Nettleserens faktiske filfilter godtar alle 54 nye filmnavn.
- Ett original/HD-bilde midt i hver film er sett på, og lokale kontaktark har fem prøver per film. Full visuell kontroll i bevegelse og alle spilltilstander er ikke gjort.

PNG-mellomfiler slettes etter godkjent teknisk kontroll av hver video. Bare komprimert video og metadata leveres. Lokale sammenligningsbilder og logg beholdes. Alle tidligere publiserte rom, objekter, figurruter og SQ1-filer er bevart; sjekksummene er kontrollert.

## Levering

PR 60 legger bare til IVF-filer og JSON-rapporter under san/, samt oppdatert rotmanifest, README og SHA256SUMS. Motoren trenger ingen ny kode. Nettleseren henter filmene når datagrenen oppdateres. Linux-pakken må bygges på nytt etter fletting; den publiserte pakken fra tidligere i dag inneholder fortsatt bare SQ1 i HD.

Produksjonsrapporten følger datagrenen som san/VIDEO-HD.json, med én JSON per film. Produksjonskø og verktøy ligger i denne lokale arbeidsmappen under resultater/video-ko og verktoy.

## Produksjonsrekkefølge

| Nr. | Film | Rammer | Fps | Video MB | SSIM |
| --- | --- | --- | --- | --- | --- |
| 1 | SQ2 | 1100 | 12 | 7.99 | 0.991495 |
| 2 | SQ3 | 883 | 14 | 7.21 | 0.986983 |
| 3 | SQ4 | 172 | 12 | 1.55 | 0.984631 |
| 4 | SQ5 | 169 | 12 | 1.64 | 0.985003 |
| 5 | SQ6 | 58 | 12 | 0.50 | 0.989592 |
| 6 | SQ6SC3 | 13 | 12 | 0.17 | 0.990153 |
| 7 | SQ7 | 86 | 12 | 3.10 | 0.984804 |
| 8 | SQ8A | 130 | 12 | 0.80 | 0.990824 |
| 9 | SQ8A1 | 66 | 12 | 0.56 | 0.989367 |
| 10 | SQ8B | 48 | 12 | 0.24 | 0.993101 |
| 11 | SQ8C | 77 | 12 | 0.47 | 0.992382 |
| 12 | SQ9 | 553 | 12 | 3.90 | 0.990017 |
| 13 | SQ10 | 203 | 12 | 3.79 | 0.983051 |
| 14 | SQ11 | 69 | 12 | 0.58 | 0.988680 |
| 15 | SQ12A | 51 | 12 | 0.46 | 0.989650 |
| 16 | SQ12B | 88 | 12 | 1.95 | 0.986436 |
| 17 | SQ13 | 182 | 12 | 1.57 | 0.982713 |
| 18 | SQ14B | 190 | 12 | 1.56 | 0.991061 |
| 19 | SQ14SC04 | 48 | 12 | 0.17 | 0.994257 |
| 20 | SQ14SC07 | 33 | 12 | 0.19 | 0.989801 |
| 21 | SQ14SC11 | 24 | 12 | 0.12 | 0.993684 |
| 22 | SQ14SC14 | 13 | 12 | 0.17 | 0.993242 |
| 23 | SQ14SC16 | 43 | 12 | 0.48 | 0.985851 |
| 24 | SQ14SC19 | 53 | 12 | 2.03 | 0.986229 |
| 25 | SQ14SC22 | 199 | 12 | 0.87 | 0.992118 |
| 26 | SQ15A | 49 | 12 | 1.85 | 0.986736 |
| 27 | SQ15B | 84 | 12 | 3.42 | 0.987391 |
| 28 | SQ17 | 806 | 12 | 6.10 | 0.982083 |
| 29 | SQ18A | 110 | 12 | 0.93 | 0.992250 |
| 30 | SQ18B | 141 | 12 | 0.95 | 0.993715 |
| 31 | SQ18SC15 | 94 | 12 | 0.86 | 0.993337 |
| 32 | SQ19A | 97 | 15 | 0.73 | 0.990317 |
| 33 | SQ19B | 231 | 12 | 2.27 | 0.990500 |
| 34 | SQ19C | 124 | 12 | 1.13 | 0.991078 |
| 35 | ALCOVE | 66 | 12 | 0.55 | 0.993649 |
| 36 | ASTTUN | 253 | 12 | 2.56 | 0.990557 |
| 37 | DARKCAVE | 461 | 12 | 3.90 | 0.993945 |
| 38 | M1 | 91 | 12 | 1.00 | 0.988986 |
| 39 | M2 | 84 | 12 | 0.95 | 0.989407 |
| 40 | NEXUSPAN | 95 | 12 | 0.92 | 0.988133 |
| 41 | PIGOUT | 76 | 12 | 0.81 | 0.980303 |
| 42 | RTRAM1 | 149 | 12 | 1.57 | 0.989059 |
| 43 | RTRAM2 | 119 | 12 | 1.24 | 0.985988 |
| 44 | RTRAM3 | 100 | 12 | 1.08 | 0.986276 |
| 45 | RTRAM4 | 100 | 12 | 1.04 | 0.990733 |
| 46 | RTRAM5 | 112 | 12 | 1.25 | 0.986954 |
| 47 | SKY | 47 | 12 | 1.02 | 0.981341 |
| 48 | TOMBDWN1 | 90 | 12 | 1.02 | 0.989682 |
| 49 | TOMBDWN2 | 90 | 12 | 1.02 | 0.989173 |
| 50 | TRAM1 | 100 | 12 | 1.10 | 0.987719 |
| 51 | TRAM2 | 112 | 12 | 1.23 | 0.990256 |
| 52 | TRAM3 | 148 | 12 | 1.47 | 0.991194 |
| 53 | TRAM4 | 121 | 12 | 0.85 | 0.992611 |
| 54 | TRAM5 | 165 | 12 | 1.75 | 0.989376 |
