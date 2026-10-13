# Sam & Max og The Dig: sammenligning av faktisk arbeidsmetode

Kontrollert 13. oktober 2026. Sam & Max er bare lest. Ingen generering, import, commit eller endring der. Rapporten gjelder et øyeblikksbilde mens grafikkarbeidet i begge prosjekter pågår.

**Konklusjon:** Sam & Max har en mer presis og konsekvent grafikkproduksjon på flere konkrete punkter. Særlig hovedark, felles rommastere, små tilstandsforskjeller og kontroll av hode/kropp er bedre gjennomført i de undersøkte leveransene. Dette støtter brukerens inntrykk. Det beviser ikke at Sam & Max fungerer bedre i spillet: den kontrollerte `hd-mod`-grenen inneholder bare README og SHA256SUMS, og de siste grafikkrapportene sier uttrykkelig at import og spilltest ikke er utført. The Dig har langt mer faktisk motor- og pakketesting. Den beste løsningen er å kombinere Sam & Max sin grafikkdisiplin med The Dig sin runtime-kontroll.

## Kontrollerte revisjoner

| Prosjekt/del | Eksakt revisjon | Faktisk status |
| --- | --- | --- |
| Sam & Max grafikk | `2266b26769b2ab43429f85220aaf52dd47282e99` | Lokal `work/.gpt-gren`, `gpt-arbeid`; samme SHA kontrollert med `git ls-remote`. Bestilling 23 publisert. Nyere lokale bestillinger er under arbeid. |
| Sam & Max kode | `3df35f636f123584e4a8d454871fb9318f995d35` | `origin/main`, samme SHA kontrollert mot GitHub. |
| Sam & Max mod | `396177a19568ef4de64679251b745c4e4978c539` | Bare `README.md` og `SHA256SUMS`; ingen aktiv HD-grafikk. |
| The Dig grafikk | `e68fe83e8e1fb89abcf8c83c3ad4f65046e585e3` | `gpt-arbeid`; samme SHA på GitHub. r12 er lokale kandidater og endringer i denne rapportmappen. |
| The Dig kode/mod | `c41d9466e5842cb08d8c2f4ef27cdc8d21f4e50d` | Publisert mod er `113523ba12fd10fbf2a9ff49b3823cd9aa8095c6`. r12-koden er separat lokal kandidat. |

Sam & Maxs hovedcheckout står på den eldre `uttrekk-v6`-grenen (`1b2b8114`). Den er ikke grunnlaget for vurderingen av dagens grafikk. `STATUS.md` og `ORDRE.md` i grafikkgrenen henger etter: nyere `todo.md`, logg, godkjenningsmanifest og faktiske bilder viser godkjent pilot og videre produksjon. Loggen ved 21:06 sier alle 76 rombakgrunner er levert som grafikk, ikke som en testet mod. Hovedark og pilot er dokumentert godkjent av Tom; senere enkeltbilder er ikke automatisk individuelt godkjent.

## Det som faktisk er bedre

1. **Identitet låses før serier.** Sam og Max har navngitte hovedark, fem visninger, eksplisitt godkjenning og referanser videre i figurjobbene. Kontaktarket `sam-kropp-hode-kontaktark.png` viser hode og kropp sammen i profil, front og bakfra. Det er en konkret kontroll mot problemet The Dig har hatt med feil person, for stort hode og uforenlige figurdeler. Bildene er tydelig gjenkjennelige og sammenhengende. De er fortsatt tolkninger med rundere former enn originalpikslene.
2. **Brede rom kommer fra én master.** Kontorets to utsnitt og senere panoramapar klippes fra samme nytegning. Det gir identisk overlapp og hindrer at vinduer, fjell, lys og perspektiv endrer seg ved skjøten. Hele kontorets original/HD-kontaktark ble visuelt sett i denne kontrollen; hovedgeometri, gjenstander og plassering følger originalen. Renere streker og mer modellering er et stilvalg, ikke pikselidentitet.
3. **Tilstandsfamilier behandles samlet og lokalt.** Bestilling 23 har ni TV-tilstander fra samme kasse og samme grunnrom. Forskjellene i øyne, munn og indikator undersøkes eksplisitt. Rapporten dokumenterer og retter konkrete feil som først gikk gjennom den generelle kontrollen. `b-tv-familie.png` ble sett: de ulike munnfasene følger kildefamilien og holder resten stabilt. Figurenes nøyaktige identitet er fortsatt uavklart, og rapporten gjetter ikke navn.
4. **Små lysformer spores enkeltvis.** Bestilling 14 viser 144 originalgrupper ved siden av sine HD-utgaver i `a-obj599_01-slutt-komponent-qa.png`. Ulike klaser har egne former og lokale farger. Dette er mer kildespesifikt enn å velge blant noen få generiske lysbilder for mange ulike kildeceller.
5. **Kontrollen måler det grafikeren faktisk leverer.** `verktoy/sjekk_leveranse.py` måler størrelse, sentrum og omriss per figurdel, samt størrelsesspredning innen animasjon/retning/lag. Sam & Max `myk.py` versjon 4 rapporterer også tegnet størrelse mot 4x og flagger mer enn 12 prosent avvik fra gruppen før normalisering. The Digs eksisterende `myk.py` har selve tilpasningen, men mangler dette ekstra rapportsteget.
6. **Teknisk OK kan avvises visuelt.** Sam & Max rom049 ble forkastet etter flere genereringer selv med teknisk OK, fordi nye polygoner og gradienter endret originalen. Den senere vektorleveransen var et uttrykkelig valgt unntak for et flatt grafisk rom. Metoden skal ikke automatisk brukes på The Digs malte scener.

## Begrensninger og forskjeller

- Sam & Max er et tegneseriespill. Renere konturer og flater gir raskt et mer presist inntrykk. The Dig må beholde sitt malte science fiction-uttrykk og myke lys. Kopier kontrollmetoden, ikke tegnestilen.
- Sam & Max sine nye leveranser er ikke sett i motoren. Max-kontaktarket merker selv avspilling med 100 ms per fase som diagnose, ikke original timing. Det kan fremdeles komme import-, palett-, maskerings- og skalafeil.
- Egenkontrollen er en indikator. Den hopper over figurflater med under 20 synlige originalpiksler. Ny kjøring i denne analysen ga Sam **7 av 7** målte ruter OK på et ark med 9 ruter, og Max **26 av 26** på et ark med 28 ruter. Små øye-/blinkdeler trenger derfor egen kontroll. TV-lag `lag007_09_del1av2` ga OK: skift 0,05, blokk 0,08 og kantlikhet 0,97.
- Sam & Max har selv dokumentert at blokk-FFT kan gi store falske skift ved filtrering uten translasjon. Tallene må suppleres med meningskontroll og konkrete kontaktpunkter. Høy kantlikhet kan også bestå for feil motiv.
- The Dig r12 har dokumenterte motorårsaker som bedre nytegning alene ikke løser: glassets palettmaske overskrev figurens eiermerke, og PDA-objekter mistet ugjennomsiktige svarte piksler og delte indeks med bakgrunnen. Nytt glass-skjermbilde ble sett her og har intakt Boston bak glasset. Dette er The Digs styrke: kontroll gjennom faktisk renderer, ikke bare ferdige PNG-filer.

## Endringer gjennomført etter sammenligningen

Sam & Max-analysen og revisjonene over er bevart som undersøkt øyeblikksbilde. Følgende gjelder den senere, ferdig iscenesatte r12-kandidaten; den tidlige heuristiske importen er ikke leveringsgrunnlaget.

1. **Brink: fra bildegjetting til eksplisitt retning.** Den tidlige importen valgte retning med en 24×28-bildedeskriptor og munn med mørke pikslers andel. Den er forkastet og bevart separat som `stage-brink-heads-rejected-descriptor.py`. Sluttimporten knytter 709 hoder til originalens AKCH-retning og kontrollerte munnfaser. De spesielle handlingsrutene som manglet eget sikkert grunnlag, er tilbakeført til tidligere grafikk, ikke gitt gjetningsbaserte hoder. `BRINK-IMPORT-SLUTTKONTROLL.json` kontrollerer 2565 grunnfiler og finner ingen rester av forkastede erstatninger. Frisk/syk tilstand og originalens rom 105-palett er undersøkt separat; `BRINK-PALETT-KONTROLL.json` bevarer faktiske pikselindekser. Dette er konkret import- og palettbevis, ikke automatisk godkjenning av hvert bilde.
2. **Energi: fra gjenbrukte former til dokumenterte kildefaser.** Den første versjonen fordelte mange celler på seks masterformer, delvis med `cel % 3`. Sluttstegene velger ikke lenger form på den måten. Sluttmanifestet har 72 eksplisitte oppføringer: 40 sentrale faser i kostyme 35 og hele kostyme 175 på 32 cels (30 tegnede faser, 2 tekniske markører). Alle har navngitt kilde/master eller begrunnet markørstatus. De samtidige 175_000/001 er deler av én felles master, og den avvikende 175_013 har eget kildebilde. Se `ENERGI-FASE-REGISTRERING.json` og `ENERGI175-SAMLET-REGISTRERING.json`. De øvrige små pulser og stråler bruker en stabil master innen sin kildefamilie, med originalens form, plassering og animasjonsstyring. De sentrale dias-/brosekvensene og linsen 238 er sett i kandidatens originalkontekst av ansvarlig produksjonsagent. Dekningsmanifestet skiller dette fra full gjennomspilling.
3. **Små lysruter kontrolleres også.** Audit fant 66 ekte lysglimt som en tidligere bredde-/høyderegel feilaktig hadde gjort tomme i bryterfamiliene 120/146/165/185/207. Alle er nå behandlet som kildestyrt lys, med samme riktige lysmaster og originalens utslipp og omriss. Alle 66 er observert som HD i originalsekvensene under isolert runtime. Ti kjøringer ga 80 full-redraw-kontroller med 0 avvik. De øvrige 185 bryterbildene og alle 251 indeksmaskene er bevart. Dette er den konkrete forbedringen som følger av Sam & Max-observasjonen om små komponenter.
4. **Glassets faktiske hull er lukket.** Audit fant den synlige, manglende sluseruten 074_004 blant de tekniske maskene. Den er produsert fra originalens 42×73-glassribber med riktig rompalett, mens ensfargede skygge-/palettmasker er bevart som masker. Den lille linsen 238 og rapporterte hull-/platåobjekter har separate kilde- og importspor. Museum 119 har kontroll av panorama, parallax og original z-maske.

5. **Fildekning følges helt til synlig objekt.** Faktisk ny lagring 6 avslørte at sparksaktøren hadde HD, mens det grove lysfeltet lå bakt inn i objekt 187. Å erstatte aktørrutene alene ga ingen synlig endring. Sluttleveransen retter derfor objekt 187 med original SMAP-dekning og ny kildebasert lysgrafikk; aktørrutene er tilbakeført. 480 runtimeframes gir åtte kontroller uten nytegningsavvik, og den faktiske scenen er visuelt sett. Dette er et konkret eksempel på hvorfor filantall alene ikke avgjør om HD er levert.

## Praktiske forbedringer videre

1. Behold identitetsgrunnlag per figur og tilstand, med faktisk retning og kropp/hode samlet. Grå hud hos syk Brink må holde sammen med ansikt, hender og klær gjennom tilstandene.
2. Bruk Sam & Maxs størrelses-/grupperapport som tillegg til The Digs import. Legg vekt på feste for hode, hånd/redskap og fotlinje. Små ruter som måleskriptet utelater må ha en egen kontroll; størrelse alene avgjør aldri om en rute er teknisk.
3. Bevar én rommaster og én variantfamilie for glass, linse og bryter. Endre bare det originaltilstanden endrer, og kontroller alle fem lysbroene samlet.
4. Bruk `DEKNING-R12.json` sitt skille mellom faktisk kunst, tom original, palettmaske og bevisst filtrert mørk komponent. Utvid fasebevisene med full runtime-tidslinje; den eksisterende AKOS-dekningslisten alene bevarer ikke ventetider, alle repetisjoner, betingelser eller tømming av lag.
5. Behold siste leveringstrinn: faktisk scene og kopiert lagring, avspilling, original/HD-bytte, riktig palett og masker, deretter den nedlastbare pakken med samme SHA. Kandidatens bevis og den endelige utgivelsens bevis må holdes atskilt.

## Direkte spor til bevisene

Sam & Max-lenker under er låst til revisjonen som ble undersøkt:

- [Grafikkregler](https://github.com/Tombonator3000/Sam-Max-HD/blob/2266b26769b2ab43429f85220aaf52dd47282e99/AGENTS.md), [analysen](https://github.com/Tombonator3000/Sam-Max-HD/blob/2266b26769b2ab43429f85220aaf52dd47282e99/ANALYSE.md), [egenkontrollen](https://github.com/Tombonator3000/Sam-Max-HD/blob/2266b26769b2ab43429f85220aaf52dd47282e99/verktoy/sjekk_leveranse.py).
- [TV-familiens rapport](https://github.com/Tombonator3000/Sam-Max-HD/blob/2266b26769b2ab43429f85220aaf52dd47282e99/rapporter/bestilling023-20261013/RAPPORT.md), [TV original/HD](https://github.com/Tombonator3000/Sam-Max-HD/blob/2266b26769b2ab43429f85220aaf52dd47282e99/rapporter/bestilling023-20261013/b-tv-familie.png).
- [Sam samlet](https://github.com/Tombonator3000/Sam-Max-HD/blob/2266b26769b2ab43429f85220aaf52dd47282e99/rapporter/stilpilot-fortsettelse-20261013/sam-kropp-hode-kontaktark.png), [Max-gange](https://github.com/Tombonator3000/Sam-Max-HD/blob/2266b26769b2ab43429f85220aaf52dd47282e99/rapporter/stilpilot-fortsettelse-20261013/max-gange-kontaktark.png), [kontoret original/HD](https://github.com/Tombonator3000/Sam-Max-HD/blob/2266b26769b2ab43429f85220aaf52dd47282e99/rapporter/stilpilot-fortsettelse-20261013/kontor-helrom-kontaktark.png).
- [Farge-/lysgrupper original/HD](https://github.com/Tombonator3000/Sam-Max-HD/blob/2266b26769b2ab43429f85220aaf52dd47282e99/rapporter/bestilling014-20261013/a-obj599_01-slutt-komponent-qa.png), [kontrollens FFT-begrensning](https://github.com/Tombonator3000/Sam-Max-HD/blob/2266b26769b2ab43429f85220aaf52dd47282e99/rapporter/kontroll-fft-20261013/RAPPORT.md).
- The Dig undersøkt lokalt: `/home/tombonator3000t/.codex/tasks/the-dig-r12-20261013/stage-brink-heads.py`, `stage-actions.py`, `stage-energy-v2.py`, `brink-head-import-preview.png`, `qa/dais15-light-final/frame_000120_room015.png`, `qa/glass-fixed/frame_000120_room025.png`, samt `code/docs/HD-RETTINGER-r12-20261013.md`.

Dette er en metodevurdering og visuelle stikkprøver, ikke en komplett kvalitetsrangering av alle rutene i begge spill. Ingen Sam & Max-filer ble skrevet eller endret.
