# Pikselkanter i Boston Low-sprites

Tom avviste stilprøven fra e459337 med et eksempel som viste trappetrinn langs ansikt, armer, ben og støvler. Det er levert en ny enkeltfigur og et nytt stilark med egne glatte konturer. Ingen motorkode er endret av grafikeren.

## Bekreftede funn

1. pipeline/dighd/figur.py, finish_cels, bruker gpt._with_alpha etter utklipp og clean_edges.
2. pipeline/dighd/gpt.py, _with_alpha, erstatter HD-bildets alfa med upscale_alpha fra originalruten.
3. pipeline/dighd/upscale.py, upscale_alpha, bruker Image.NEAREST. costume014_773 blir 164 x 248 fra 41 x 62, med bare alfa 0 og 255. Alfamasken i den leverte stilprøven er identisk med originalens maske i 4x. Nye detaljer inni figuren endrer derfor ikke den grove ytterkanten.
4. Motorens kSrcCel-gren i engine/patches/0001-dighd-hd-grafikk.patch på main har if (ha < 128). Under grensen brukes originalens flatCol; over grensen brukes HD-fargen. Mellomnivåer blandes ikke med scenen bak. Den tegnede figurens opprinnelige kildeområder er fortsatt i originaloppløsning.

Funksjonene er lest i den lokale Pages-kopien og alfagrensen er også bekreftet i patchen fra origin/main, commit d1ebb643b188b508938e59b477d58b7bd23232b8. Dette er kildekode- og filkontroll, ikke en ny kjøring av motoren.

## Krav til en eventuell integrasjon

- Bevar den nye tegnede alfakanten gjennom eksporten. Ikke legg originalens nærmeste-nabo-maske over den ferdige tegningen.
- Behold originalens indeksbilder, animasjonsrekkefølge, ankerpunkt, gangflate, skript og klikkoppførsel.
- Mottaket må tilpasse den nye tegningen til hver originalrutes størrelse og plassering. Det nye stilarket kan ikke klippes blindt med de gamle rektanglene.
- Vurder hvordan motoren kan blande myke kantpiksler mot riktig bakgrunn, også der en glatt kontur avviker litt fra originalens trappetrinn. Den eksisterende alfagrensen alene gir ikke myke kanter.
- Bevar masker foran figuren, figurlag, palettbytter og originale skyggeeffekter. En ny HD-kontur må ikke skinne gjennom forgrunnsobjekter eller menyer.
- Kontroller først én rute på lys og mørk bakgrunn i motoren, deretter hele gangrekken. Sammenlign størrelse, fotfeste, omriss, ansikt, klær og flimmer ved normal spillefart. Test HD/klassisk-bytte og okklusjon før flere figurer bestilles.

## Status

Nye PNG-filer og deres gjennomsiktighet er kontrollert som grafikkfiler. Spillintegrasjon, animasjonsflimmer og endret kantkomposisjon er ikke testet. Toms stilvalg gjenstår. Ark 2 til 4 og andre figurjobber skal ikke produseres automatisk på grunnlag av denne stiltesten.
