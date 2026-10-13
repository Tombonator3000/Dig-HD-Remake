# Visuell kontroll av r12, 13. oktober 2026

Dette er en kontroll av konkrete r12-kandidater i den faktiske motoren med kopierte lagringer. Det er ikke en full gjennomspilling eller Toms visuelle godkjenning. Automatiske skjermavvik og visuell riktighet er ført hver for seg i `QA-VISUELL-R12.json`.

## Brink: avvist import og retting

Den første hodeimporten hadde feil retning og for store hoder i gangfasene. Beviset `qa-visuell/final-brink-mismatches.png` sammenligner de samme spillrammene med originalen. Dette ble behandlet som en leveringsfeil selv om alle automatiske redraw-kontroller var null.

Alle filer fra denne deskriptorstyrte importen ble gjenopprettet fra den bevarte r11-pakken. Deretter er **709 hodecels** for ståing, gange og tale i kostyme 15, 16 og 17 koblet til retningen i originalens AKCH-data. Fordelingen er 226, 228 og 255. Tilknytningen står eksplisitt i `BRINK-HODER-REGISTRERING.json`. Ingen generell gjetting ut fra hårfarge eller bildebeskrivelse brukes for retning. Samme retning har fast hodeskala gjennom tale; kroppen og originalens posisjon beholdes.

`qa-visuell/final-brink15-explicit-contact.png`, `final-brink16-explicit-contact.png` og `final-brink17-explicit-contact.png` viser retningene og gangfasene etter rettingen. Sykeutgavene bruker det grå, magrere ansiktet. De spesielle handlingene utenfor denne familien bruker foreløpig r11-hodene. De er ikke rapportert som ferdig rettet. Det ligger **ingen** avviste hodefiler for kostyme 48, 73, 188, 223, 305 eller 306 i `mod-overrides`, og ingen ekstra hodefiler for 15/16/17 utenfor den eksplisitte listen.

## Riktig spillpalett

Originalskriptet `room038-LSCR-28630785` velger kostyme 15/16/17 etter `bitvar18` og `bitvar19`, og setter `shadowMode(1)` med hensikt. `room105-LSCR-85186826` bruker kostyme 17 under samtalen om Brinks krystallmaskin. Både rom 38 og 105 er derfor relevante, men en syntetisk testaktør kan arve andre egenskaper fra en lagring. Den kontrollerte isolerte aktøren er 29.

Kostymene har hjemrom 7. En blind hjemromspalett ville vært feil for to av fargeoppføringene. Eksisterende RGBS-palett for kostyme 17 avvek også betydelig fra de fargene spillet faktisk bruker. **1343 indeksbilder** i kostyme 16 og 17 har derfor fått palettmetadata fra originalens AKPL via **rom 105, palett 0**. Alle selve indeksbytes og gjennomsiktighetsverdier er bevart og kontrollert. `BRINK-PALETT-KONTROLL.json` inneholder per-fil kontrollsum for indeksene og sluttfilen.

Den isolerte før/etter-testen i rom 105, `qa-visuell/final-brink17-palette-comparison.png`, viser at den gule huddriften i profil forsvinner. Grå sykehoder beholdes. Klærnes eksisterende skadevarianter er ikke nytegnet eller slått sammen ut fra gjetting. Kontrollen bruker aktør 29 og de faktiske r12-filene etter importen.

## De fem bryterkrystallene

20 kontroller kjører kostyme 120, 146, 165, 185 og 207 i hvert sitt rom, med hele chore 6, 7, 8 og 9. Alle har null avvik mellom delvis og full redraw. `qa-visuell/final-switches-contact.png` viser alle fem i de fire tilstandene. `final-switch120-phases.png` viser seks tidspunkter i hver fase for kostyme 120. De kontrollerte bildene har klare kanter uten den tidligere store blobskyggen. Av/på og bleking er fortsatt animert. Hver eneste kodede cel er ikke manuelt vurdert isolert.

## Energi 175: full fase og riktig deling

Den gamle generiske diamanten er avvist, med historisk bevis i `qa-visuell/final-energy175-comparison.png`. Sluttkandidaten bruker fasespesifikk grafikk. Originalskriptet setter aktør 6 til `(160,100)` i rom 65, chore 6. Effekten brer seg over den øvre fasetterte delen av rommet.

En gjenværende loddrett diamant skyldtes at originalens sammenhengende fase på **281×145** var delt i cel 0 (256 piksler) og cel 1 (25 piksler), men ble importert som to selvstendige former. Originalposisjonene er `(24,0)` og `(280,0)`. De to originaldelene er satt sammen som kilde for en ny fullbredde master med innebygd bildeverktøy. Denne deles først etter produksjon, nøyaktig ved x=256. Cel 13 har en egen master fra sin bredere lyspuls; 2 og 14 er opprinnelige 1×1 tekniske blanke og får transparent HD. Det er ikke strukket en gammel 256-pikslers del over hele fasen.

`ENERGI175-SAMLET-REGISTRERING.json` bevarer kilder, mål, koblinger og kontrollsummer. Gjeldende importør er arbeidsområdets `stage-energy175-seam.py`, kjørt **etter** `stage-energy-phases.py`; arkivkopi ligger i `produksjon/importer-energy175-samlet.py`. Prompt og begge genererte masterfiler ligger i `produksjon/energy175-samlet-*` og `energy175-013-*`.

`final-energy175-seam` kjører 240 bilder og 24 kontroller uten redraw-avvik. Faktisk HD-frame 120 og ni ulike tidspunkter er visuelt kontrollert. Den løse side-diamanten er borte, og feltet er sammenhengende med originalens hovedgeometri. Se `spillkontroll/energi175-samlet-slutt.png` og `energi175-sluttfaser.png`.

## Energi 35 og lysbro 152/168

De siste faktiske bildene fra `final-phase-dais35`, `final-bridge152` og `final-bridge168` er kontrollert. De viser lys, glød og energilinjer; den tidligere innførte kvinne-/klesfiguren vises ikke i disse kontrollerte fasene. Bevis ligger i `spillkontroll/energi35-slutt.png`, `lysbro152-slutt.png` og `lysbro168-slutt.png`. Dette er utvalgte bildefaser, ikke en ny påstand om full historie-gjennomspilling.

## Museum 119: sluttkontroll mot originalmaske

Tidligere normal/myk kandidat hadde trappede forgrunnssnitt. Hovedoppgaven har siden innført mykere overgang bare på den synlige siden av originalens z-maske, med null z-plane-lekkasje. `MUSEUM119-KONTROLL.json` dokumenterer original ENCD, kostyme 119, bevegelsesformel og zclip 3, samt testene ved kamera x=160,360,548.

Sluttbildene ved x=160 og x=548 er sett på nytt. Bakgrunnen er HD og følger forgrunnsåpningene. Den lyse fjellstripen ved gulvet finnes i originalens åpning og skal bevares; den tidligere observasjonen var ikke i seg selv bevis på en feil. Se `spillkontroll/museum119-slutt-x160.png` og `museum119-slutt-x548.png`. Den tidligere åpne statusen for masketilpasning erstattes av en bestått visuell stikkprøve av disse sluttbildene.

## Brink 310 og 312

Begge nye handlingskostymene er kjørt gjennom chore 6, med HD-ansikt, grå syk hud, grå jakke og oransje bukser. Det ble ikke observert pikselfallback i de vurderte posene. Disse er syntetiske aktørtester. Den komplette historieovergangen fra vanlig stående Brink til handlingen er ikke spilt gjennom i denne kontrollen.

## Gjenta kontrollene

Arbeidsområdet er `/home/tombonator3000t/.codex/tasks/the-dig-r12-20261013`. `qa-final-batch.py` inneholder den opprinnelige testmatrisen; `qa/final-batch-plan.json` og resultatfilene bevarer kommandoer og logger. `stage-brink-heads.py` er gjeldende importør, også arkivert som `produksjon/importer-brink-hoder-kildekoblet.py`.

Alle testtilfeller har egne kopierte saves under `qa/final-*`. Det bevarte utgangspunktet for save 6 er uendret, SHA-256 `12c26a281d50bc2afd0a950f6f288ea26c79b11063723dc3466cbf19c37db742`.

Siste kontroll bruker den faktiske kandidatmodden etter palettrettingen: kostyme 16 og 17 i rom 105, aktør 29, 520 bilder hver. Begge har 43 kontroller uten redraw-avvik. `qa-visuell/brink-final-rom105.png` viser den ferdige kandidaten. De 709 aktive hodefilene er byteidentiske i kandidatmodden og `mod-overrides`.

Brukerens aktive `dig.s06` har siden fått en annen kontrollsum (`5abf1172f1fecccac35c0ae4127a4411dc6c859746483a58f743edfb3dbbb5dd` ved sluttkontrollen). Testene har bare skrevet egne kopier. Vi påstår derfor ikke at brukeren har latt samme lagringsnummer stå uendret under arbeidet.

## Sluttkontroll av Brinks hender

Kostyme 16 og 17 er sammenlignet med klassisk originalvisning i rom 105 i de samme posene. Originalhendene har varme beige/rosa toner også i sykeutgavene. Kostyme 17 er i tillegg kontrollert med spillets aktør 5 og dens shadowMode 1; denne forskjellen fjerner den syntetiske aktørens magenta testskygge, men gjør ikke de vanlige hudfargene grå. Motorens shadowMode 1 behandler palettverdi 13 som bakgrunnsskygge, ikke som en generell desaturering av hud.

Det er derfor ikke påvist en ytterligere palettfeil som gjør hendene varme. Hender og klær er beholdt. De nye sykehodene er grå i tråd med brukerens bestilling. `spillkontroll/brink-hender-original-og-hd.png` og `brink17-aktør5-hender.png` viser sammenligningen. Original- og HD-kontrollene med aktør 5 har begge 20 redraw-kontroller med null avvik.
