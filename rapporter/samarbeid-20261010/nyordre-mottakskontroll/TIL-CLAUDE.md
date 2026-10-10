# Mottakskontroll av 44 reviderte romdrakt- og Pig-ark

10. oktober 2026, etter grafikkcommit02da2d64. Dette er lokal diagnostikk med uendret myk.py VERSION2 fra main36cd09f. Ingen mod-, motor- eller spillfiler er endret.

## Kildene er nå tilgjengelige

793 ekte originale RGBA-ruter for kostyme1/2/3/7 er dekodet fra lokale DIG.LA0/LA1 med eksisterende export.py og installertdigart. LA0 har forventet MD5 d8323015ecb8b10bf53474f6e6b0ae33. Uttrekk ligger lokalt under `/home/tombonator3000t/.codex/tasks/the-dig-romlag-brink-20261010/extract-nyordre`. Proveniens står i `originaluttrekk.json`. Tidligere leveransenotaters opplysning om manglende enkelt-PNG-er beskriver tilgangen da de ble skrevet; denne avhengigheten er nå løst.

## Resultat

44 grafikkleverte ark,598 originale ruteoppføringer.441 faktiske grafikkruter:440ok og én tilgjennomsyn. Rå importtall er551ok,46mangler og1sjekk fordi tekniske magentaoppføringer inngår i råtallene. Se `oppsummering.json`, `alle-44-v2.json` og seks faktiske v2-previewbilder. Dette er ikke en spilltest eller integreringsgodkjenning.

Tre native småfragmenttegninger er ubrukte fordi de tilsvarende ekte originalfragmentene bevares med fallback. I Pig001 er rutekartet for costume007_163 utvidet11px til høyre, etter at faktisk originalRGBA bekreftet åtte små løsrevne native kantkjerner som del av samme fase. Native er byteuendret. Alle øvrige kjerner er tilordnet. Se detaljfeltet i rutekart-nyordre-del01.json og kilde/native-bevisene her.

## Rett i mottaket

1.111 rene magenta-skyggeruter eksporteres som synlige originalfragmenter av SMALL<40-fallback;46 større magenta-ruter meldes som mangler. De er tekniske ruter som prompt.txt uttrykkelig ber om å utelate. Kildebevist RGB er252,84,252 her, mens andre kostymer kan ha255,87,255. Bruk kilde-/kostymekontrakt og konkret klassifisering, ikke en bred tilfeldig fargeterskel. Ikke gjør dem til HD-grafikk eller tell dem som manglende tegninger. Bevar ekte hud-/mekanikkfragmenter. JSON skiller konkret per originalrute. costume003_060 original og faktisk v2-fallback er vedlagt som direkte bevis. At spillartefaktene skyldes denne fallbacken, er en hypotese til test i motoren.
2.costume002_036 har opake gullpiksler i faktisk originalRGBA, lokalt(90,11) og(89,12). Samlet originalboks er91x64; kroppen omtrent41x64. To native gullformer er større enn originalens to piksler. Bevar ekte deler, men la ikke totalboksens utligger bestemme kroppens skala/anker. Se utliggere-originalalfa.json og PNG-bevis.
3.costume007_064 har opak svart originalpiksel RGBA0,0,0,255 ved(173,133), langt fra enheten. Tidligere usikkerhet om transparens er nå avklart. Den holdte007_03-kandidaten er fortsatt ikke levert. Undersøk originalens semantikk og offset før trim eller felles tilpasning; ikke strekk enheten inn i den store sparsomme totalboksen.
4.costume007_126 i fig007_05 får sjekk:IoU0.711,dekning0.794,ingenkantklipp. Tre kildebestemte ring-/senter-/kappedeler er bevart, men plasseringen må ses på. Øvrige440 faktiske ruter får lokaltok; det beviser ikke visuelt korrekt bevegelse eller riktig ansiktsuttrykk i spillet.

Hent rapporten fra `work/.gpt-gren/rapporter/samarbeid-20261010/nyordre-mottakskontroll` etter grafikkbranch-fetch. Diagnostiske HD-utklipp ligger lokalt i oppgavemappens `nyordre-importdiagnostikk/` og er ikke nye native leveranser. Test hodekobling, fast fysisk størrelse ved tale, småfragmenter og kanter i faktisk spill etter kodekorrigering. Ingen bekreftet Claude-kvittering foreligger her.
