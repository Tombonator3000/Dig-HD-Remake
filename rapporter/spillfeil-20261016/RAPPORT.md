# Rettingskandidat 16. oktober 2026

Kandidaten svarer på Toms tretten skjermbilder og presiseringene om sonden i HD og Boston som gjenoppliver skapningen ved vannet. Skjermbildene er feilreferanser. Godkjente hovedark for Boston, Maggie og Brink fra 15. oktober er stilfasit, med SHA-256 i `leveranse.json`. Nye figurbilder ble generert med de faktiske hovedarkfilene som bildereferanser. Native masterfiler er bevart under `produksjon/`.

| Funn | Rettet i kandidaten |
| --- | --- |
| Boston/Maggie-hals og Brink-ansikt | Nye hodeark, kildestyrte retninger, fast hodeskala og halsfeste i hovedkostymene. Syke Brink-varianter beholder grå hud og blondt hår. |
| Undersøkelsen av døde Brink | Kostyme 59/60, 18 nye sceneruter og separate hoder. Hodeløse kroppsruter forblir hodeløse. |
| Glass og inventory viser gamle piksler | Ny motorpatch registrerer faktisk maling og palettmasker; HD-transformasjon bruker skyggelagets tabell uten å kopiere gammel tekstur. |
| Røde krystaller med rammer, blå størrelseshopp | 360 kildestyrte omriss. Bakgrunnsmatte fjernet, hjørner registrert og kantene klippet direkte i HD. |
| Sonden mangler kroppen | 225 ruter i kostyme 78 til 83 får en ugjennomsiktig mørk kropp rundt mintpanelene. |
| Museum spire, trappetrinn | Motoren jevner også over maskens grensepiksler. Kontroll ved kamera 160, 360 og 548. |
| Engraved rods | Grønne, røde, lilla og gylne fasetter med geometrisk spiss ende, inkludert rødt variantikon og valgte/deaktiverte tilstander. Både `_hd.png` og reservebilder er erstattet. |
| Brink med solbriller ved gjenoppstandelse | Nye hoder og 40 kroppsruter i kostyme 67, samt separate hoder i 73, etter godkjent Brink-ark. |
| Skilpaddeskjelett | 52 deler registrert til originalens form og beinpalett. Fargetilpasningen teller ikke lenger tekniske skyggemasker som bein. |
| Boston ser ut som en annen ved vannet | 19 ruter i kostyme 103 etter Boston-arket. Korrigert kildepalett fra original AKPL og rom 32 palett 0. |

## Kontroll

- 2223 erstatningsfiler, med før-/etterhash i `OVERRIDES.json`. Originalens indeksverdier er uendret. Kostyme 103 korrigerer bare den feilaktige RGBS-paletten i 20 indeksfiler.
- 77 native tilfeller, 656 sammenligninger med full nytegning, null avvik etter innlasting av testscenen.
- 13 ekstra native tilfeller for museum, sondevarianter, gjenoppstandelse, Boston ved vannet, skjelett og krystaller. Alle kontroller av nytegning består.
- Eksakt nearest-inventar og nearest-krystaller er identiske med originalvisningen. Et konstant HD-testbilde har én farge gjennom inventory. Gammel motor ga 23 farger i samme test, fordi gammel tekstur skinte gjennom.
- Registreringsscriptet lager 627 utsnitt fra originale AKSQ-delgrupper og separate stålag. Ingen ståhoder har glippe større enn ett originalpiksel. Delgrupper er ikke det samme som komplette animasjoner over tid. Kontaktarkene brukes til visuell kontroll; scriptet avgjør ikke figuridentitet eller tegnestil.
- Hele patchrekken passer på låst ScummVM-kilde og gir byteidentiske filer med det kompilerte bygget. Pipeline: 50 bestått, 2 hoppet over, 2 game-tester ikke valgt.
- Skjelettet er kontrollert fra kopiert PDA-lagring. Direkte introhopp gir en uinitialisert original skyggetabell, med feil hvite skygger også i klassisk visning, og er derfor ikke fargefasit.
- Et eksisterende introhopp-avvik ved bilde 20 er registrert separat. Romtestene begynner etter innlasting, fra bilde 100. Gammel motor viste samme oppstartsavvik.

Skjermbilder, målinger og kontaktark finnes under `spillkontroll/`. Den opprinnelige release-modden er kontrollert mot sine sjekksummer for alle erstattede filer og er ikke endret. Lagringer ble kopiert før test; ordinære lagringer og innstillinger er ikke endret av testene.

## Produksjon og videre kontroll

`verktoy/` har de faktiske import- og registreringsscriptene. De bruker et arbeidsområde med `kode`, `kandidat-mod`, `testing` og `grafikk`; sett `DIGHD_WORKSPACE` til arbeidsområdets rot. Basemod/spillsti i scriptene peker på den bevarte lokale releasekopien og må tilpasses ved reproduksjon på en annen maskin. `inspect_assets.py` og `geometry.py` lager metadata fra egne spillfiler før `register_heads.py`. Hoder/scener importeres før `import_more.py`; bein, krystaller og sonde har egne importører. Native masterfiler skal ikke overskrives av nye genereringer.

Promptgrunnlaget var: nøyaktig originale positurer og ruterekkefølge, godkjente hovedark for figuridentitet, samme klær og tegnestil, ugjennomsiktig kropp med transparent bakgrunn, bevisst hodeløse deler bevart, ingen fotorealisme eller solbriller. Sonden bruker originalens mørke doble kjegleform med mintpaneler. Stavikonene bruker originalens segmentplassering, men kantete krystallfasetter og spiss ende etter Toms bestilling. Kildeskjermbilder og produksjonsreferanser ligger separat.

Dette er en lokal kandidat for Toms visuelle vurdering. Hovedarkgodkjenningen godkjenner ikke automatisk nye animasjonsruter. Full gjennomspilling, Windows, fysisk mobil og 32-bit OpenGL er ikke kontrollert. Den installerte AppImage-filen og offentlig Linux-release er ikke oppdatert i denne jobben. En separat lokal starter ligger i oppgavens arbeidsområde.
