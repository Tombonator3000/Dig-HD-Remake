# R22 ferdig for integrering, 18. oktober 2026

Alle 48 utvalgte manglende Boston-ruter er nå nytegnet og har bestått samme formkontroll. De seks tidligere holdte rutene ble tegnet enkeltvis med godkjent Boston-hovedark som referanse. Seks enkelttegninger pluss én skulderrettelse er lagt til de ni tidligere kallene, totalt 16 bildeverktøykall. Ingen kontrollgrenser er senket. registration.json og ADDITIONS.json beskriver de 48 ferdige rutene og 96 nye filer.

91 eldre små originalfragmenter med høyst 72 synlige kildepiksler er eksportert på nytt med eksisterende myk.from_original og riktig AKPL gjennom rom32 palett0. De er palettrettede originalfragmenter, ikke 91 nye KI-tegninger. Deres 182 eksplisitte erstatningsfiler står i REPLACEMENTS.json, med uendrede indeksverdier og gamle/nye kontrollsummer i fragments.json. De feilfargede fragmentene langs vannflaten er borte i den nye prøven.

Ny motoravspilling i rom32 viser alle 48 nye ruter og totalt 138 HD-ruter fra kostyme100. Én liten fysisk kilderute ble ikke observert i denne animasjonen. 47 fullomtegningskontroller etter oppstart gir null avvik. Ingen motorfeil. kneeling-scene.png, rising-scene.png og standing-scene.png er fornyet etter siste tegning og palettretting. Dette er styrt motoravspilling, ikke en naturlig gjennomspilling eller Toms visuelle godkjenning.

Arbeidsrestlisten er nå 5963. Publisert restliste oppdateres når integreringen er kontrollert. Senere integrerings- og distribusjonsbevis føres i rapporter/integrering-r22-20261018. Den historiske statusen under er bevart for sporbarhet.

---

# R22: Boston kommer opp av vannet

18. oktober 2026. 42 nye HD-ruter er laget og klargjort med 42 originale indeksreferanser. Leveransen ligger i `mod-tillegg/costumes`, med kontrollsummer i `ADDITIONS.json`. Kun nye ruter er med. Publisert hd-mod og distro er ikke endret i denne runden.

## Hvorfor dette ble prioritert

Tom ba om det mest kritiske fra restlisten. En hovedperson som skifter identitet i en obligatorisk handlingssekvens har høyere visuell betydning enn et stort antall uavklarte effektruter. Rom 32 har dessuten tidligere meldt figurfeil. Denne konkrete serien er Boston som kommer tilbake fra undervannshulen og reiser seg, ikke gjenopplivingen av skilpadden. Identiteten er kontrollert mot rom32 LSCR2000, aktør3, kostyme100, animasjon6, start59,144 og overgang tilbake til kostyme14.

Se GRUNNLAG.md for kilde og palett. Den gamle RGBS-forhåndsvisningen hadde lyst hår og oransje skjorte. Tegnegrunnlaget ble rekonstruert fra kostymets AKPL gjennom rom32 palett0. Ingen beskyttede jobbfiler er endret. Godkjent Boston-hovedark følger alle tegnekall.

## Tegning og kontroll

Innebygd image_gen ble brukt. Modellnavn ble ikke oppgitt. Seks ark med åtte originale poser ble tegnet, med to nye forsøk på det første arket og ett forsøk på bakgrunnsuttrekk. Totalt ni bildeverktøykall. Bakgrunnsuttrekket er ikke valgt til levering. Fargeskjæret som først så synlig ut i bildeforhåndsvisningen ligger i usynlig RGB; eksporten bruker den faktiske alfakanalen og premultiplisert skalering.

40 ruter fra ark02 til06 besto formkontrollen direkte. Tredje versjon av ark01 gir to brukbare ruter. De seks øvrige rutene 084,071,070,064,060,033 holdes utenfor etter tre forsøk. De har for store avvik i forholdet mellom hode, vannlinje og hule bølgeringer. De skal nytegnes, ikke godkjennes ved å senke kontrollgrensen.

Hver levert rute er én hel tegning. Hodet er ikke flyttet eller skalert uavhengig av kroppen. Minimum overlapp mot originalalfa er 0,6486 og største akseavvik mot felles skala er 11,13 prosent. Disse målene er tekniske grenser, ikke Toms visuelle godkjenning. Rutekart, opprinnelig geometri, kildesjekksummer og valgt originalrute står i registration.json. Alle indeksverdier er uendret, og riktig rompalett er lagret i de nye indeksreferansene.

## Test i motoren

Kandidaten bygger på publisert hd-mod 29cff6583dc45ec21bcccb5da0eb16afafa379a5 og inneholder bare disse 84 tilleggsfilene. Test i lokal motor med rom32, palett0 og animasjon6 observerte alle 42 nye HD-ruter. 47 opptegningskontroller etter oppstart hadde null avvik. Ingen motorfeil ble funnet. Loggen er native-boston100.log.gz og resultatene qa.json. kneeling-scene.png, rising-scene.png og standing-scene.png er faktiske skjermbilder fra testen.

Dette er styrt motoravspilling, ikke en naturlig gjennomspilling eller test av ny distribusjon. Eksisterende små ruter og andre romaktører ble ikke omtegnet. Enkelte små gamle fargede fragmenter er fremdeles synlige rundt vannflaten under testen. Denne leveransen erklærer derfor ikke hele vannsekvensen ferdig eller alle tidligere feil rettet. Seks utvalgte ruter trenger fortsatt nytegning.

## Status

- Nye ferdige tegninger for innhenting:42.
- Nye filer: 84, ingen erstatninger.
- Kandidatens restliste: 5969, publisert restliste fortsatt 6011.
- Ny AppImage: ikke laget i denne runden.
- Tom har ikke visuelt godkjent de nye rutene.

Kilde fra prosjektbiblioteket: `losninger/grafikk/figurark-fast-storrelse.md`. Løsningen er merket PASS for opphavsprosjektet; tilpasset her med helfigurregistrering, separat alfakontroll og faktisk motoravspilling. Kildens mål beviser ikke at alle tegninger er semantisk riktige.
