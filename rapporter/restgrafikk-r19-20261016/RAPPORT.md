# Restgrafikk r19, arbeidsrapport 16. oktober 2026

Tom har bekreftet at oppdraget gjelder all restgrafikk i hele spillet. Arbeidet er ikke ferdig. Rapporten er et etterprøvbart mellomlager, ikke en utgivelse eller visuell godkjenning.

Kandidaten har 7097 nye HD-ruter. Den siste råopptellingen har 6944 originalruter uten HD, hvorav 6943 har minst 40 synlige originalpiksler. 712 av de manglende rutene er bekreftede palettmasker som motoren tegner som effekter, og krever ikke selvstendige HD-bilder. Disse er fortsatt med i råopptellingen, men skilles ut i semantic-coverage.json. Den integrerte grafikken er pakket som r19-AppImage 17. oktober 2026; se leveransestatus nederst.

## Kilder og metode

Godkjente pilotark i hovedark/boston.png, brink.png og maggie.png styrer menneskene. Originaldata fra DIG.LA1, indeksbilder, animasjonsvalg og spillkontekst bestemmer motiv, plassering og palett. Originale jobbfiler er bevart.

Prosjektbibliotekets losninger/grafikk/figurark-fast-storrelse.md ble lest. Prinsippet om opprinnelig geometri brukes, men bibliotekets PASS gjelder tidligere kilderevisjoner og er ikke visuell godkjenning her. Se https://github.com/Tombonator3000/prosjektbibliotek/blob/main/losninger/grafikk/figurark-fast-storrelse.md.

Verktøy: innebygd image_gen for nytegning, Python med Pillow, NumPy, OpenCV og eksisterende dighd.myk for mekanisk registrering. Faktiske native bildemål er registrert der de avviker fra ønsket størrelse. Modellnavn er ikke eksponert av verktøyet.

De fire kommunikasjonsportrettene beholder original identitet, uttrykk og signalforstyrrelser. Ken Borden og Cora Miles er kontrollert mot spillets offisielle manual: https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/6040/manuals/THE_DIG_Manual-English.pdf?t=1542756570.

## Det som er produsert og tatt inn i arbeidskandidaten

* Boston i romdrakt, tre nye ark og tilhørende småfragmenter.
* Boston ved gjenopplivingen i vannrommet, 17 nytegnede større poser og 6 småfragmenter. Paletten er hentet via AKPL i rom 32, ikke feilfarget eksportpalett.
* Manglende faser fra tidligere leverte stol-, robotarm-, Nexus-, Eye- og Lockup-ark.
* Spiralfaser med nytegnet materiale registrert mot originalens hull og fragmenter.
* Brink, Maggie, Ken og Cora på PDA, inkludert uttrykk og signalstøy. Støy uten figur er teknisk oppskalering av originalsignalet.
* 670 krystallfaser gjenbruker den eksisterende krystalltegningen, tilpasset originalens fasegeometri og farge. Brune matter rundt krystallene fjernes.
* 70 manglende nærbildefaser av Maggies bakhode, skulder og hånd. To ytterligere ruter er enkeltpiksler som er bevart som tekniske fragmenter. Kostyme 328 og 329 har identiske originale bilder, kontrollert før gjenbruk. To smale hudfragmenter bevarer originalformen teknisk. Manglende avklipte håndstrimler i to native faser gjenbruker en nytegnet nabofase. Dette står eksplisitt i maggie-registration.json.

57 nye ruter i Maggies vending i laboratoriet er registrert. De 38 første fasene deler en uendret bakfrafigur, mens bevegelsen i steinflatens originalsignal overføres mekanisk. De 19 vendingsposene er nytegnet hver for seg. Ansikter bruker native alfa; originalens pikselmaske klipper ikke kinn eller nese. Se labturn-registration.json.

872 originalruter i de fire MajMin-kostymene 95, 118, 266 og 267 er nå lest direkte fra spilldata. Dette er kildeklargjøring, ikke ferdig HD. Det finnes ingen publiserte indeksbilder for disse seriene. I stedet er alle 872 avkodede originalruter sammenlignet med de beskyttede originaljobbene: ingen RGB-avvik og ingen avvik i gjennomsiktighetsmaskene. Se codec16-job-reference-check.json.

52 dialogruter i kostyme 331 er registrert fra 20 valgte representanter blant 21 nytegnede deler. Originalens munn- og øyeposer velger passende tegning. Små originale forskyvninger overføres med et felt begrenset til 3 originalpiksler. Ingen gamle ansiktspiksler legges over de nye. Høyre arm og stein bruker ett felles nytegnet grunnlag. De tre delte kildeparene 24/25, 30/31 og 42/41 får samme samlede originalfelt før registrering, så de møtes ved samme bevegelse og størrelse. Se labtalk-registration.json. Dette er kontrollert gjenbruk, ikke 52 uavhengig nytegnede portretter. Den sammenhengende figuren er også forankret til originalens nedre kant med en liten felles vertikal tilpasning av hode og torso. Dette retter et avklipt skjorteparti som omtegningskontrollen alene ikke oppdaget. Se maggie331-nedre-kant-rettet.png.

## Nye serier og tekniske fragmenter

Bibliotekets kostymer 266 og 267 har 511 nye ruter. Alle 247 ruter i 266 og 222 små ruter i 267 er tekniske detaljer, glimt og oppdateringsstriper som bevarer originalsignalet med myk oppskalering. De 42 større rutene i 267 gjenbruker det malte HD-rommet og overfører originalens endring i lys og fase. Dette gjelder bildene i krystallkabinettets søyler, kuler og pyramideformer. Det er ikke 511 nye selvstendige illustrasjoner. Se library-registration.json og library-three-images-comparison.png.

Lynserien 95 har 180 ruter, hvorav 70 større faser gjenbruker den malte HD-himmelen med originalens lysendring, og 110 er små tekniske signalfragmenter. Alle 180 ble faktisk sett i de seks endelige motortestene. Kameraet i dette rommet begynner 104 originalpiksler inn i scenen. Testaktøren bruker samme forskyvning før plasseringene registreres, så lynet ligger over himmel og sjø. Tidlig test med aktøren ved 0,0 ga feil bakgrunnsutsnitt og er ikke leveransen. Se lightning-registration.json og context_r19_connect.py.

Svømmeserien 118 har 181 ruter. 143 større figurer, boblegrupper eller vannkomposisjoner er nytegnet på 18 ark. Vannfragment 001 gjenbruker den nye skumtegningen i 062, og den siste fjerne stående profilen 180 gjenbruker sidefiguren fra det godkjente Boston-pilotarket. De øvrige 36 rutene er små originale fragmenter. Hele kroppen registreres samlet mot originalens kroppspalett; hode og torso transformeres aldri hver for seg. Bobler registreres separat rundt originalens små boblekjerner og har begrenset diameter. Kombinerte skum- og figurutsnitt beholder hele komposisjonen. Fire feiltolkede bakfrafigurer i andre ark ble omtegnet forfra før import. Se swim-registration.json, prompter/ og boston118-i-spill.png. Alle 181 ruter ble sett samlet over tre endelige testplasseringer. Testen er en tvungen visning i rom 33, ikke bevis på den normale spillsekvensens iscenesettelse.

Ytterligere 3 810 små originalfragmenter er behandlet med den eksisterende SMALL-metoden i dighd.myk. Både jobbinventaret og avkodet original må ha under 40 synlige piksler. Publiserte indeksbilder kontrolleres for identiske pikselindekser før gjenbruk, og publiserte filer overskrives ikke. Disse rutene er teknisk oppskalering med original palett og form, ikke nytegnet HD-kunst. Kostyme 169 rute 070 ble utelatt fordi avkodingen har 142 synlige piksler, selv om jobbinventaret telte den som liten. Se small-fragment-registration.json. Dette skillet er viktig når totaltallet vurderes.

## Kontroller og begrensninger

Rotte- og felleserien 183 har 194 nye ruter. Fire ark med åtte rotteposer hver gir 171 faser. Ett eget ark gir 19 faser med dyr under ribbeinsfellen og fire fragmenter som gjenbruker det nye malte stangmaterialet mot originalens fragmentform. Rom 68 palett 1 og AKPL bekrefter dyrets farger. Skyggekode 13 tegnes ikke som rosa kunst. Originalskriptene bruker shadow mode 1, ikke en synlig magenta skygge. En walkthrough ble brukt for å avklare ribbeinsfellens funksjon: https://gamefaqs.gamespot.com/pc/9487-the-dig/faqs/39833. Se rat183-plan.json, rat183-registration.json, rat183-trap-registration.json og prompter/rat183*.txt.

Første registreringsforsøk klippet dyrets hode og kropp med originalens grove kontur og feiltolket sammensatte felleruter. Dette ble forkastet før levering. Dyret bruker nå den nytegnede alfaformen og ett samlet, begrenset bevegelsesfelt. Felle og stang har egne referanser. Alle 194 nye ruter ble faktisk sett samlet over de endelige, tvungne animasjonsvalgene med korrekt rompalett og høyre kamerautsitt. De fire siste stangfragmentene ble kontrollert på nytt etter materialretting. Tester med venstre kamerautsitt så ingen nye ruter og teller ikke som vellykket visning. Testen er ikke en full naturlig gjennomspilling av fellepuslespillet.

25 videre ruter gjenbruker eksisterende HD-bilder helt uendret etter sammenligning av identiske originale RGBA-piksler og bildemål. Dette omfatter 18 Boston-faser fra den nye svømmeserien, to eksisterende Boston-utsnitt, to steinfragmenter og tre beinfragmenter. Elleve andre nøyaktige originaltreff ble avvist fordi den tilgjengelige HD-figuren hadde brun skjorte og beige bukse, som avviker fra pilotarket. En kilde som finnes er ikke automatisk riktig grafikk. Se identical-source-registration.json.

24 av disse 25 gjenbruksrutene ble sett i motortestene. Beinfragmentet 212_002 er fortsatt ikke observert; en stabil skjermbuffer er ikke bevis for den rutens visning. Den eksakte originale RGBA-likheten og den uendrede HD-kopien er likevel kontrollert. Se kontroller/r19-identical*-results.json.

Brinks spadeserie 46 har 15 nye selvstendige tegninger på to ark. global174 identifiserer aktør 5 som Brink og setter kostyme 46 i rom 15 før han begynner å grave. Derfor brukes AKPL gjennom rom 15 palett 0, i stedet for jobbeksportens feilaktige brunfarger. Det godkjente pilotarket hovedark/brink.png styrer identitet og klær. Hode, kropp og spade transformeres som én figur per pose, og den nytegnede alfaformen beholdes. Fysiske pikselindekser er uendret. Se brink46-plan.json, brink46-registration.json, brink46-preview.png og prompter/brink46*.txt.

Testhopp til rom 15 ble avbrutt av spillets eksisterende tilbakevending til rommet i lagringen og så ingen nye ruter. Derfor testes spadeserien isolert i rom 23. Alle 20 palettkodene som brukes av figuren er byteidentiske mellom rom 15 palett 0 og rom 23 palett 0, kontrollert mot originale spilldata og lagret i brink46-plan.json. Den isolerte testen er ikke en full avspilling av Brinks fallsekvens.

Alle 15 nye Brink-ruter ble faktisk sett i den isolerte testen uten avvik mellom løpende skjermbuffer og full omtegning. Se kontroller/r19-brink46-isolated-results.json og kontroller/brink46-i-spill.png. Dette er teknisk kontroll, ikke Toms visuelle godkjenning.

Trikkapslene har 394 nye HD-ruter i åtte kostymer. Fem nye ark med åtte blå kapseltegninger hver gir 378 fasebilder. De siste 16 manglende rutene i 92, 122 og 166 gjenbruker allerede publiserte HD-tegninger i samme kostyme. Originalens geometri og utsnitt styrer plasseringen; et begrenset, glatt bevegelsesfelt tilpasser den nytegnede overflaten. Alle 394 ruter ble faktisk sett samlet i isolerte tester av ankomst og avgang. Enkelttester uten nye ruter er beholdt som negative dekningstester og teller ikke som vellykket visning. Det tvungne testoppsettet kan vise en ekstra kapsel ved siden av rommets vanlige kapsel og beviser ikke normal iscenesettelse. Se tram-art-registration.json, tram-art-preview.png og kontroller/r19-tram*-results.json.

822 originalruter i trikkostymene er palettmasker. AKPL-koder, opprinnelige romskript og AKOS-animasjonene bekrefter at samtlige brukes i skyggeanimasjonene 9 til 11 med shadow mode 3, mens de egentlige kapseltegningene bruker 6 til 8. 712 maskefiler mangler HD i råinventaret. De telles ikke som nytegnet kunst og fylles ikke med tomme lokkefiler. Se tram-mask-classification.json, tram-chore-classification.json og semantic-coverage.json. Originalskriptene ble lest lokalt med offisielle ScummVM Tools, revisjon 8665aa1d3221a6cc884026f5ed7144fac512e0e9. Komplette spillskript er ikke lagt i repoet. Noen andre skript gir dekompileringsfeil; dokumentasjonen bygger på de konkrete relevante kommandoene, ikke på en påstand om feilfri dekoding av hele spillet.

Prosjektbibliotekets losninger/testing/logg-over-det-som-mangler-hd.md brukes for å skille faktisk tegnede ruter fra råinventaret. losninger/grafikk/scumm-v6-kostymer-skygge-og-soppelruter.md ga bakgrunn om palettmasker, men dens v6-spesifikke regler er ikke overført ukritisk til Dig v7. Klassifiseringen over er kontrollert mot dette spillets egne data og motorens palettmaskekode.

kontroller/ inneholder råresultater fra isolerte spillmotortester. Skjermbufferen sammenlignes med full omtegning. Ruter som faktisk ble tegnet registreres. En test uten synlig HD-figur teller ikke som figurtest, selv om skjermbufferen er stabil. Tidlige tester med feil kameraposisjon er bevart som diagnostikk; senere sentrerte tester viser den faktiske dekningen.

base-preservation.json kontrollerer alle 30 378 publiserte r18-filer mot Git-innholdet. Alle publiserte filer er bevart bortsett fra to dokumenterte HD-erstatninger i OVERRIDES.json. Startrutene 330_000 og 330_001 er klippet fra samme nye tegning som resten av vendingen, slik at en eldre fotografisk tegning ikke blinker frem i starten. Originale indeksfiler er uendret. ADDITIONS.json er hashmanifestet for tilleggene.

Dette er ikke en full gjennomspilling. Flere tekniske tester dekker bare utvalgte animasjonsvalg. Hode, kropp og stil må vurderes samlet gjennom overgangene. Tom har ikke visuelt godkjent disse nye arkene. Krystalltester som bare viser en eller to faser beviser ikke hele seriens visuelle kvalitet.

## Gjenstående arbeid

dekning-arbeid.json er den konkrete listen over fysisk manglende bilder. Den må suppleres med gjennomgang av allerede eksisterende figurark: opptellingen fanger ikke opp ferdige filer med feil identitet, klær eller hodeplassering. Kontrollen av gjenbruk avdekket slike eldre referanser, blant annet kostyme 170 og 57, som trenger egen retting før grafikkpakken kan kalles konsekvent. Neste arbeid omfatter øvrige nærbilder, figurer, skapninger, mekanismer og effekter. Noen eksporterte paletter viser tekniske farger eller masker. Disse må avklares i original spillkontekst før nytegning; de skal ikke males bokstavelig som nakne figurer eller røde kjøretøy.

verktoy/ bevarer registreringsoppskrifter. Sett DIGHD_WORKSPACE til arbeidsroten med kode/, grafikk/, hd-leveranse/, kandidat-r19/ og testing/source/ ved reproduksjon. Skriptene er arbeidsverktøy og krever kildedataene som rapporten viser til. Ikke kjør import_r19.py ukritisk over senere rettede spiralfaser.

## Integrert 17. oktober 2026

Tom ba om integrasjon, pull og ny distro. Data-PR66 er flettet til hd-mod 630cadb3ebb398ac8ade1f4e1ea759f8a783cd5a. Integrasjonen legger til alle 14173 manifestfiler og gjør bare de to dokumenterte Maggie-erstatningene. Alle tidligere ressurser og 55 HD-filmer er bevart. Se integration-r19.json. Nye kontroller på integrert mod viser Brink46 (15 ruter), trikkapsel270 (30), rotte183 (37) og Maggie331 (52) uten omtegningsavvik. Det første Maggie-testhoppet gikk til feil rom og så ingen nye ruter; korrekt rom111 er testet separat. Linux-distro bygges og kontrolleres separat; dette er ikke en ferdigmelding for all restgrafikken.

## Linux-distro publisert og kontrollert

Linux-bygg39027347179 består begge pakketestene, inkludert Debian12. Faktisk nedlastet AppImage:2123475448 byte, SHA25647b04c1bc468cb4dccd35cc33a6241504ea0cefaac6b87d144cd963c652c9b7a. Kode c2c9b8e0 og hd-mod630cadb3. Alle44551 mod-manifestfiler og hele tilleggspartiet stemmer, uten ekstra filer. Standard AppRun-oppstart, intro, tekst og HD/klassisk-bytte gir null omtegningsavvik over550 oppdateringer. Pakkens egen motor viser også Brink15, Maggie52, kapsel30 og rotte37 ruter i isolerte tester, alle bestått. Tvungen surfacesdl/vindusoppstart feilet før spillinitialisering i lokal hodeløs SDL; ordinær oppstart og CI består. Se distro-r19-kontroll.json og distro-r19-bygg.json. Ingen vanlige lagringer er berørt.

Eksakt motorkilde med gjeldende patch0007 er også oppdatert i releasen. Nedlasting: https://github.com/Tombonator3000/Dig-HD-Remake/releases/tag/linux. Hele restgrafikken er fortsatt uferdig. Videre produksjon bør starte fra publisert r19; de arkiverte r19-oppskriftene og basiskontrollene er knyttet til sitt opprinnelige r18-grunnlag og skal ikke kjøres ukritisk over den nye modden.
