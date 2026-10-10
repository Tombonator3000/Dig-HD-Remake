# The Dig HD Remake: ny chat etter avvist stil

Tom ba 10. oktober 2026 om en ny chat i prosjektet **The DIG HD REMAKE** fordi de siste figurene har feil uttrykk. Fortsett oppdraget der, med en kort og kontrollert kontekst. Serieproduksjonen i den gamle chatten er avbrutt. Dette er en overlevering, ingen ny grafikkleveranse eller spillgodkjenning.

## Siste menneskelige beskjed

«dette er helt feil look ??? begynner å bli feil .. start ny chat i prosjekt The DIG HD REMAKE og fortsett så vi ungår at feil oppstår i for lang chat»

De to vedlagte figurarkene er **avviste eksempler**, ikke stilankere:

- `avvist-flygende-figur.png`: blond figur i oransje skjorte og beige bukse, to flygende stillinger.
- `avvist-graaharet-figur.png`: gråhåret figur i oransje skjorte og beige bukse, 17 stillinger.
- `prosjektvalg.png` viser hvilket Codex-prosjekt Tom ønsket.

Arkene viser en rundere, mer volumrendret malestil enn konseptets tegnede uttrykk, og ulik figuridentitet. Røde/gule prikker og kanter er synlige i vedleggsvisningen. Undersøk faktisk RGB, alfa og vanlig komposisjon før årsaken fastslås. Det er ikke bevist her at vedleggene er byteidentiske med en bestemt jobbleveranse. Ikke anta jobbnummer, ikke slett eller erstatt andre filer blindt.

## Visuell autoritet og neste arbeid

Start med å **se på bildene**, ikke bare lese promptene:

1. `rapporter/boston-konsept-glatte-kanter-20261009/konsept-main.webp`, uendret kopi av `docs/konsept/boston-low.webp` fra main d1ebb643. Dette er det opprinnelige konseptet: tegnet 2D, tydelige mørke konturer, bevisste skyggeflater og karakteristisk kantet ansikt. Glatte konturer skal ikke bli plastaktig, generisk volumrendring.
2. `rapporter/boston-konsept-glatte-kanter-20261009/boston-gang-hoyre.png` og `boston-28-ruter.png`, stilprøven i bdae1ae som Tom svarte «Mye mye bedre! Lag de andre sånn med så mye detaljer også» til.
3. Originalene for den aktuelle figuren/kostymet. Boston-stilen gir ikke tillatelse til å endre en annen figurs hår, alder, klær, proporsjoner eller identitet. En stilreferanse er ikke nytt motivinnhold.

Tidligere genererte `brink-stilanker.png`, `maggie-stilanker.png` og første ark for hvert kostyme er historiske kandidater. De er **ikke** selvstendig bevis på Toms visuelle godkjenning. Auditer dem før videre gjenbruk. De siste avviste arkene skal aldri brukes som anker for nye ark.

Fortsett først med å identifisere de viste kandidatene og sammenligne dem med konseptet og originalene. Lag én avgrenset korrigert stilprøve for den berørte figuren og vis den sammen med referansen før ny masseproduksjon. Denne korrigeringsbeskjeden gjelder feilutseendet Tom nå har vist. Den er ikke en tillatelse til å endre alle andre prompter eller spillets kode. Antallskontroll og RGBA-format alene beviser ikke riktig uttrykk. Bruk normal visning på lys, mørk og grønn bakgrunn; kontroller klær, ansikt, hår, retninger, avkuttede kropper og alle små reelle deler.

## Autorisert oppdrag og arbeidsgren

Tom har bestilt Boston, Brink og Maggie med alle kostymevarianter, UI/logoer/ikoner/inventory og deretter «Lag resten av grafikk og sprites». De nåværende øvrige figurarkene og 230 romlag er dermed bestilt. SAN-filmene er utsatt. Ikke be om samme omfang igjen. Claude skriver koden, Tom godkjenner.

Bruk den eksisterende grafikkcheckouten:

`/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk`

Remote er private `Tombonator3000/Dig-HD-Remake`. **Bare gpt-arbeid**, aldri main, nye grafikkgrener eller PR-er. Les gjeldende AGENTS.md, ORDRE.md, BESTILLING.md og relevante deler av GRAFIKKLISTE.md fra origin/gpt-arbeid etter fetch. Bevar lokale endringer. Prosjektmappen `/home/tombonator3000t/Dokumenter/ChatGPT/The DIG HD REMAKE` er ved overleveringen et tomt Git-repo på master uten remote. Ikke forveksle den med grafikkcheckouten, og ikke begynn å levere grafikk på master der.

Bevar referanse.png, original_1x.png, prompt.txt og jobb.json. Claude eier kode, status.csv, RAPPORT.md og retur.md. Andre checkout-er og prosjekter skal ikke endres.

Tilpassede stilprompter og avgrensede korreksjoner er allerede autorisert for de 54 hovedkostymene. For øvrige figurark, romlag og gamle rom-/objektreturer gjelder fortsatt prompt.txt ordrett, bortsett fra den konkrete stilrettingen i den siste menneskelige beskjeden. En tidligere bredere forespørsel om 43 kildebundne korrigeringsprompter har ikke fått svar: `rapporter/resten-grafikk-20261009/korreksjonsforslag/LES-MEG.md`. Ikke spør om dette på nytt rutinemessig og ikke anta en generell tillatelse.

Bruk innebygd ChatGPT-bildegenerator. Ikke bytt til en betalt ekstern tjeneste. Bevar generatorens native PNG/alfa og noter faktisk modellnavn bare hvis verktøyet bekrefter det. Ingen kreativ etterbehandling, hard originalmaske eller skjult restalfasletting for å få en kontroll til å bestå.

## Verifisert leveransestatus før stilretting

Siste grafikkcommit er **83a11a14d17afcfd02c89109e8d28d1ab123281b**, pushet til origin/gpt-arbeid. Les fremdriftsfilene på nytt; dette er et øyeblikksbilde:

- Hovedfigurer: 509/509 ark, 7683 originaloppføringer, 320 små originalfragmenter med fallback. `rapporter/hovedfigurer-hd-20261009/fremdrift.json`.
- Øvrige figurer: 769/3523 ark, 4203/20799 originaloppføringer. 2754 ark gjenstår. `rapporter/andre-figurer-hd-20261009/fremdrift.json`.
- Til sammen 1278/4032 figurark er grafikklevert. Denne tekniske leveransestatusen skal ikke omtales som Toms godkjenning av alle stiler.
- Nye romlag: 184/230 grafikklevert. 31 har kontrollavvik og 15 venter på korrigerte/godkjente romankere. `rapporter/resten-grafikk-20261009/leveranser-lag.json` og tilhørende rapporter.
- Rom/objekter og UI er levert tidligere med dokumenterte returer. UI-leveransen er 88fb2f2f; inventarark krever riktig registrering, lag079_05/06 har kjente kontrollpunkter.
- 337 øvrige kandidater står som tilbakeholdt. Se `rapporter/andre-figurer-hd-20261009/tilbakeholdte-kandidater.json`. Rå native forsøk er ikke leveranser.

Ingen ny integrasjon eller animasjonstest er utført for de senere arkene. Kartene er diagnostikk, ikke sikre motorankere. Historiske kodefunn om hard alfa/masker må kontrolleres mot aktuell kode av Claude. Ikke gjør motorendringer her.

## Uferdig lokalt arbeid og sikker gjenopptakelse

Hjelpeskript og registrerte native forsøk finnes i:

`/home/tombonator3000t/.codex/tasks/the-dig-resten-20261009`

Se `lokal-snapshot.json` i denne rapportmappen. Det skiller planlagte kall, sikkert registrerte utfall og allerede leverte jobber. De tidligere exec-cellene 7, 12 og 25 var utilgjengelige etter avbruddet; et forsøk på å stoppe dem returnerte «exec cell not found». Underliggende allerede sendte bildekall kan ha fullført eller fullføre lokalt. Ingen av disse senere rå filene skal leveres automatisk. Ikke påstå at alle eksterne kall er kansellert, og ikke resubmitter blindt.

Batch 161 er bare forberedt, ikke sendt til bildegeneratoren. `originalrader.json` har en lokal endring fra denne forberedelsen. Rundt 37 eldre uregistrerte hovedfigurpromptfiler er også lokale. Bevar alt. Ikke reset/clean, ikke git add -A, ikke gjenoppta de gamle produksjonsløkkene før stilen er rettet.

Gruppe 91 leverte fig169_02/03/04/05/06/07/09, fig170_02, fig193_02 og fig202_03. Gruppe 90 har særskilt merknad om at fig166_19/20 kan være funksjonelle røde masker; Claude må kontrollere funksjonen før import. Noen tidligere leverte ark har egne advisories for utfylte åpninger. Les notat og tilbakeholdelsesgrunn, ikke bare antall.

Rutinesjekken `the-dig-nye-grafikkbestillinger` er fortsatt lesende og skal flyttes til den nye chatten. Den skal ikke produsere eller gi duplikatvarsler om egne leveranser. Kontrollfil: `/home/tombonator3000t/.codex/automations/the-dig-nye-grafikkbestillinger/dig-monitor-state.json`. Siste sjekk fant ingen nye ordre-, kontroll- eller returendringer gjennom grafikkcommit 83a11a14.

Den gamle chatten skal ikke produsere parallelt. Behold historikk, native forsøk og tidligere leveranser til etterprøving.
