# Til Claude: HD for inventar, markører, logoer og håndcomputer

Tom har nå uttrykkelig bestilt HD for logoer, ikoner, inventory og tilsvarende UI. De tre ikonarkene og håndcomputerens seks UI-lag er derfor bestilt i samtalen. Øvrige romlag er ikke automatisk omfattet. Grafikken ligger bare på gpt-arbeid. Ingen kode er endret.

## Ordinært mottak

Hent resultat.png og notat.md for ikon01, ikon02, ikon03 og lag079_01 til lag079_06. Alle er 1536 x 1024 og følger eksisterende jobb.json. De beskyttede inputfilene er uendret. Se leveranse.json for valgte forsøk og sjekksummer.

Syv av ni helbilder består lokal gpt-kontroll. lag079_05 får sjekk, lag079_06 får avvist på globalt blokkavvik. Alle målbare enkeltobjekter består omrissgrensen. For de to siste lagene er de fem faktiske UI-utsnittene dessuten kontrollert separat og består samlet forskyvning og kantlikhet. Små utsnitt har ingen blokkprøve. Se kontroll/ui-objektutsnitt-kontroll.json og kontroller avviket før import. Ikke overstyr avvisningen uten å undersøke hva den måler.

Eksporter kun de 20 objektbildene som lag079-jobbene lister. Apparathus, hånd og bakgrunn skal fortsatt komme fra eksisterende HD-bilder. Unngå at små forskjeller i tegnet hånd mellom lagene blir synlige i spillet. Portrettkvaliteten varierer og skal vurderes i faktisk skjermstørrelse.

## Glatte inventarkonturer

assets/ikon01-rgba.png, ikon02-rgba.png og ikon03-rgba.png har ekte native alfa og alle 149 oppføringer. De er visuelt kontrollert på flere bakgrunner. Bruk disse ved tilpasset import dersom du vil beholde glatte silhuetter.

Frileggingen endret pakkingen. Bruk rutekart.json som diagnostisk forslag til 149 kildeceller, og registrer hvert motiv mot originalobjektets størrelse og synlige alfaboks. Originale jobb.json beskriver RGB-hovedleveransene, ikke de frilagte arkene. Ikke strekk hvert motiv vilkårlig til å fylle rektangelet. Samordne skala, anker og felles malte partier mellom normal, markert og nedtonet tilstand. Bevar hele antialias-kanten innenfor cellen.

Ikke legg originalens nærmeste-nabo-maske i 4x over nye konturer. Mottak og motor må bevare kontinuerlig alfa eller gjøre en kontrollert antialias-sammensetting. En hard alfagrense på 128 kan gjeninnføre synlige trapper. Bevar originale indeksbilder for palettlogikk og klassisk visning. Fargesatte markeringer og nedtonede ikoner skal fortsatt skifte korrekt.

De seks fargeknappene obj807_01, obj808_01, obj809_01, obj810_01, obj811_01 og obj872_01 har et skarpere alternativ i assets/seks-fargeknapper-rgba.png. Referanse og rektangler ligger i kilder/seks-fargeknapper.json. Rekkefølgen er blå, gul, lilla, grønn, rødoransje og elfenben. Alternativets kant er tydeligere enn originalens. Tilpass som ett sett, uten å endre knapperekkefølge, klikkflater eller spilltilstand.

## Markører

Handlingstegn, piler og kryssmarkører finnes på ikonarkene. Kontroller hvilke objekt-ID-er cursorCommand faktisk velger. Motorens updateCursor i gjeldende origin/main-patch skalerer fortsatt indeksbufferen med x/n og y/n. Den laster ikke disse nye RGBA-bildene som markørgrafikk. Koble til riktig objekt og tilstand, og bevar opprinnelig hotspot i originalkoordinater. Test både vanlig peker og aktiv inventargjenstand. Ikke flytt hotspot til det nye bildets sentrum.

## Logoer

- Tittelskjermen: behold eksisterende jobber/rom106/resultat.png som ordinær romleveranse. Den nye frilagte assets/the-dig-logo-rgba.png er en egen UI-ressurs med endret størrelse på motivet. Den skal registreres og skaleres til den konkrete bruken, ikke erstatte rom106 direkte.
- Oppstart: assets/lucasarts-logo-rgba.png er tegnet fra SQ1.SAN, nullbasert ramme 60. Kilderektangelet i originalrammen er x=120, y=48, bredde=80, høyde=96. kilder/sq1-frame00060.png dokumenterer sammenhengen. Dette er referanseutsnittet, ikke et kontrollert endelig overlayanker. Bevar original inn- og uttoning. Moddformatet har en san/SQ1/NNNNN.png-vei per ramme, men ingen ny logo-overlaykode er lagt til her. Sett ikke logoen på samtlige filmrammer.
- PenUltimate: obj551_01 er levert gjennom lag079_01. Bevar skrivemåte og plassering på apparatets skjerm.

## Spillkontroll før Tom prøver

Åpne inventaret fra normal spillflyt. Direkte romhopp til rom 93 er ingen gyldig inventartest. Kontroller utklipp, markering, nedtoning, valg av gjenstand, hotspot og retur til spillet. Kontroller håndcomputerens sider og knapper, oppstartslogoens uttoning og bytte HD/klassisk. Sjekk gåteglyfene ved faktisk størrelse. Skriv faktiske resultater i RAPPORT.md og eventuelle returer; ikke regn lokal filkontroll som spillgodkjenning.

LEVERANSE.md forklarer dekning, forsøk og gjenværende kontrollpunkter. Alle genererte PNG-filer i leveransen er byteidentiske med generatorutdataene.
