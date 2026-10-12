# Fire manglende hovedark, 12. oktober 2026

Ordregrunnlag: ORDRE.md, Claude 11. oktober. Hovedark for Boston, Maggie, Brink og robotarmen mangler. Pig har et eksisterende hovedark og nyere feilrapport; det røres ikke her. SAN-filmene er utsatt.

Samtaler kontrollert: «The Dig HD: rett figurstilen og fortsett», «Fiks The Dig HD-grafikk og hakking» og den eldre overleveringen. R3 er rapportert levert fra den separate feilrettingen. Det er ikke en godkjenning av all tidligere grafikk.

Gjeldende remake-skill er lest fra main eb7c0b07, docs/skills/scumm-hd-remake/SKILL.md. Den vedlagte source-faithful-production og lokal imagegen brukes også. Grafikkgrenen er oppdatert til 6c173a85 etter at en grunn historikk ble hentet dypere. Lokale filer er bevart.

## Identitet og kilde

- Boston: kostyme 014 på planeten, 001 i EVA-drakt. Kort brunt hår med grå sider, kantet ansikt, mørk kortermet skjorte, oransjebrun bukse, mørke støvler. Godkjent glatt Boston-prøve er stil- og identitetsanker; konseptet bekrefter figurens særpreg.
- Maggie: kostyme 018 på planeten, 002 i EVA-drakt. Mørk kort bobfrisyre, oransje kjeledress med oppbrettede ermer, hvit undertrøye, mørke støvler. Originalkonsept og originalruter er identitetsgrunnlag. Det eldre Maggie-stilankeret har ikke selvstendig dokumentert menneskelig godkjenning og brukes ikke som autoritet.
- Brink: kostyme 015 på planeten, 003 i EVA-drakt. Kort blondt hår, kantet ansikt, grå jakke over mørk skjorte, oransjebrun bukse, mørke støvler. Godkjent Brink-anker 10. oktober bekrefter frisk normalvariant. Død/skadet/gjenopplivet Brink er egne tilstander og skal ikke blandes inn i dette normalarket.
- EVA-utstyr: originale 001/002/003 viser hvit drakt, gullkantet visir og stort rektangulært manøvreringsutstyr. Personen inne i hjelmen skal beholde sitt eget ansikt og hår. Røde og gule utstyrsdetaljer holdes adskilt fra tekniske magentamarkører på sprites.
- Robotarm: kostyme 004/005 i rom 002, armen som håndterer Pig på romfergen. Originalark 004_01, 004_03, 005_01 og 005_02 og originalrom 002_del1av3 viser feste, lange lyse metallseksjoner, ledd, gul bøyle/kabel og rødt merke. Løse spritebiter er deler av samme mekanisme, ikke nye våpen. Et hovedark må bevare formen i de viste perspektivene; uleselig innvendig mekanikk skal ikke oppfinnes.

## Leveransetype og kontroll

Dette er hovedark til visuell vurdering, ikke motorens animasjonsruter. De teller derfor ikke som nye leverte figurjobber eller HD-cels. Nye ark sammenlignes med original og riktig stilanker, med hode/kropp samlet på hovedarket. Native bilder og alfa bevares uten kreativ etterbehandling. Prompt, referansehash og resultatsha føres i manifestet.

ORDRE.md krever at Tom godkjenner hovedarkene før de brukes som bilde to i nye person- og robotarmserier. Serieproduksjon og runtimeimport av disse nye referansene venter derfor på denne konkrete vurderingen. Dette er ikke en ny godkjenningsrunde for omfanget.

Ingen spilltest eller ny pakke bygges for et referanseark som ikke er importert i spillet. Full animasjonskontroll i faktisk motor gjenstår når de avledede figurarkene er produsert og tatt imot. Beskyttede kildefiler og alle tidligere lokale endringer kontrolleres mot grunnlag.json før commit.
