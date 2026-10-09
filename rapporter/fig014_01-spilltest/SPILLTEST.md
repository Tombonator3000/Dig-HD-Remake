# fig014_01 integrert for spilltest

Utført av Codex 2026-10-09 etter Toms beskjed: «Integrer den først så jeg får testet ut i spillet». Dette er en testintegrasjon. Toms visuelle godkjenning gjenstår, og ark 2 til 4 er ikke startet.

## Pakken

Pilotarket fra commit 130b9dd er klippet ut med eksisterende gpt-inn. Eksisterende `_build_costumes` har pakket de 28 fargelåste RGBA-rutene med 28 originale indeksbilder. Ingen motor- eller pipelinekode er endret.

Den lokale, komplette testpakken ligger i `/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-pages/mods/gpt-boston-pilot`. Den inneholder de eksisterende 103 HD-rommene og 485 objektbildene pluss pilotrutene. 1176 eksisterende bildefiler er kontrollert byte for byte uendret. Alle nye ruter har riktig 4x størrelse og nøyaktig original alfamaske i 4x. Alle indeksbilder er byte for byte identiske med uttrekket.

`costumes/` ved denne rapporten inneholder bare tillegget på 28 ruter med indeksbilder. Det er ikke en komplett HD-pakke alene. `pakke-kontroll.json` lister størrelser og sjekksummer. `provenance.json` sporer utklippingen tilbake til arket.

## Faktisk nettleserkjøring

Den komplette testpakken er lest inn gjennom HD-mappevelgeren i Toms eksisterende Codex-nettleser på https://tombonator3000.github.io/Dig-HD-Web/. Spillfilene og lagrede spill er beholdt. Pakken huskes ved ny sideinnlasting. Den vises som 103 HD-rom, 234 MB. Private spillfiler og HD-bilder er ikke publisert på GitHub Pages.

Motoren startet i 1280 x 800. I rom 15 gjennomførte spillet mellomsekvensen hvor mannskapet tar av romdraktene. Boston Low vises der med nye HD-kroppsruter og HD-hode, mens rutene som ikke finnes i piloten og de andre figurene fortsatt har originalgrafikk. Bildene `boston-hd-rom15.jpg` og `boston-original-rom15.jpg` dokumenterer faktisk spillvisning. Knappen HD / klassisk byttet til originalgrafikk og tilbake i testøkten. Spillmenyen åpnet og lukket.

Den eksisterende kostymetesten ble også kjørt i nettleseren med kostyme 14, aktør 29 og 60 bilder per animasjon. Motorloggen bekreftet at den skiftet animasjon og retning. Den kunstige testaktøren fikk rosa skyggemerker også i klassisk modus. I den vanlige rom 15-sekvensen er disse merkene borte. Originale skyggemarkører og indeksbilder er bevart.

## Avgrensning og oppfølging

- Piloten dekker 8 stående kropper, 8 separate hoder og 12 ruter for gange mot høyre. Andre retninger, snakkeanimasjoner og andre kostymer er fortsatt originalgrafikk.
- HD-visning i motoren og bytte til originalgrafikk er kontrollert. Gange ved manuelle klikk i det direkte romhoppet lot seg ikke bekrefte gjennom automatiseringen. Dette er ikke dokumentert som en full spillbarhetstest eller en bevist feil i grafikken. Claude kan kontrollere romhoppets styring ved neste motortest.
- Et separat forsøk med den allerede installerte lokale Linux-motoren brukte en eldre binærfil som ikke utførte de nye rom- og kostymetestene. Det forsøket teller ikke som verifikasjon av piloten.
- Musikk og tale kunne ikke kontrolleres, fordi DIGMUSIC.BUN og DIGVOICE.BUN mangler i den lokale spillmappen.
- Offisiell hd-mod-gren og hovedgren er ikke endret. Toms neste handling er å prøve utseendet og si om ark 1 er godkjent før flere ark lages.

For å prøve i en annen nettleser: åpne spillsiden, velg den eksisterende spillmappen og den komplette testmappen nevnt over som HD-mappe. I Codex-nettleseren her er disse allerede lest inn. Normal start er spillsidens rotadresse; `?rom=15` er en rask scenevisning med mellomsekvens.
