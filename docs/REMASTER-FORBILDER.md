# Hvordan LucasArts og Double Fine laget sine remastere

Dato: 10. oktober 2026. Forfatter: Claude. Utfyller del 2 i `HD-REMASTER-METODE.md`.

Gjennomgang av de fem offisielle remasterne av LucasArts-eventyrene: The Secret of Monkey Island Special Edition (LucasArts 2009), Monkey Island 2 Special Edition (LucasArts 2010), Grim Fandango Remastered (Double Fine 2015), Day of the Tentacle Remastered (Double Fine 2016) og Full Throttle Remastered (Double Fine 2017). Først hva de gjorde, så hva som ble kritisert, og til slutt hva vi tar med til The Dig.

Alt under er hentet fra kildene nederst. Der noe er vår tolkning, står det.

## 1. Hva de gjorde

### Motoren: originalen kjører under

Double Fine og Shiny Shoe (GDC 2017) lot det originale SCUMM-spillet kjøre urørt under. Et nytt lag leser tilstanden (rom, figurer, kostymer, animasjoner) og tegner den på nytt i HD. De beskrev tre måter å påvirke spillet på, i økende risiko:

1. Lese tilstand (state snooping): bare se hva spillet gjør og tegne det annerledes.
2. Endre tilstand (state mutation): skrive verdier inn i spillet, for eksempel for ny input.
3. Lappe skriptkoden (bytecode patching): bare når det ikke finnes annen vei.

Feilene ble delt i to lister: feil som fantes i originalen, og feil som bare finnes i remasteren. Prinsippene var å holde seg tro mot den kunstneriske intensjonen, øke detaljnivået, modernisere forsiktig, rette originalfeil og legge til ekstramateriale.

Grim Fandango var et annet tilfelle (GrimE-motoren, 3D-figurer på forhåndsrendrede bakgrunner). Der fikk figurene ny belysning i sanntid med skygger, mens spillogikken ble beholdt. Teamet unngikk endringer som gikk så dypt at de kunne knekke spillet, og brukte arbeid fra fansen (ScummVM og ResidualVM og en pek-og-klikk-mod som forfatteren delte koden til).

### Grafikken: nytegnet for hånd, med originalen som fasit

- DOTT: alt tegnet på nytt for hånd. Kunstteamet ble ledet av Yujin Keim sammen med Larry Ahern og Peter Chan fra originalen, og Matt Hansen malte bakgrunnene. Over 100 bakgrunner og rundt 10 000 animasjonsbilder.
- Full Throttle: Yujin Keim kalte det kuratorarbeid, "purisme fremfor revisjonisme". Nær 200 bakgrunner ble malt på nytt av rundt et dusin malere, i en malerisk stil med harde kanter og tre valører, og utvidet til bredere format. Over 8 000 animasjonsbilder ble tegnet på nytt av rundt 30 tegnere. Først laget de master-figurark for hver figur sammen med Larry Ahern, så tegnet alle etter dem.
- Tim Schafer om Full Throttle: målet var å fjerne gjenstander, komprimering og gammel teknologi, så spillet ser ut slik folk husker det.
- Monkey Island SE: LucasArts tegnet figurer og bakgrunner på nytt, scene for scene og gåte for gåte som originalen. Figurene var en nytolkning basert på flere spill og covere.
- Grim Fandango: de originale høyoppløste figurteksturene var borte og ble malt på nytt fra grunnen. Der en detalj var uklar (et merke på en hatt), gikk tegnerne til konseptkunsten og brukte skjønn. Bakgrunnene ble bare litt oppdatert.

### Filmene i Full Throttle

Trevor Diem har beskrevet hele løypa:
- De originale SAN-filene (320x200, 10 bilder i sekundet) var fasiten, trukket ut med eget verktøy.
- Et arkiv på 67 GB med gamle kildefiler ble indeksert med sjekksummer. Et eget verktøy fant hvilke kildefiler hvert filmbilde var laget av, ved visuell sammenligning.
- Tre spor: håndtegnede bilder (samme løype som DOTT), 3D (gamle scenefiler hentet inn i 3ds Max og så Maya, med ny toonskygge og rigg som fjernet forvrengte armer) og lyd.
- Tidsdata ble funnet ved å kjøre det originale avspillingsprogrammet i DOSBox.
- Bildene ble laget i 4440x2400 og satt sammen automatisk. OpenCV-maltreff og en chat-bot holdt oversikt.
- Problemer de selv nevner: lyden ble først hørt etter siste koding, lagringsplassen eksploderte, og hver runde tok lang tid.

### Lyd

- Schafer fant de gamle opptakene i arkivet på Skywalker Ranch: stemmene på DAT-bånd og musikken på spolebånd. Musikken i Full Throttle ble mikset litt lavere.
- DOTT spilte MIDI-musikken gjennom en synth av Sound Canvas-typen.
- Grim Fandango: Peter McConnell spilte inn deler av musikken på nytt med Melbourne Symphony Orchestra, med de gamle Pro Tools-øktene som referanse.
- Monkey Island SE fikk stemmer og ny musikk. MI2 SE fjernet pausen etter hver replikk, så dialogen flyter bedre.

### Valg for spilleren

- DOTT: grafikk, lyd og grensesnitt kan byttes mellom klassisk og ny hver for seg. Nytt verbhjul rundt objektet, med den gamle verbraden som valg. Inventaret som eget lag.
- Monkey Island SE: F10 byttet mellom klassisk og ny. MI2 SE: bytte av grafikk, og direkte kontroll som alternativ.
- Full Throttle: F1 byttet mellom klassisk og ny.
- Grim Fandango: 4:3 med kunst på sidene i stedet for svarte felt, eller 16:9 strukket. Ny pek-og-klikk-styring ved siden av den gamle tankstyringen.

### Ekstramateriale

Utviklerkommentarer som spilles av på bestemte steder (DOTT, Grim, Full Throttle, MI2 SE), og gallerier med konseptkunst (156 bilder i DOTT, 98 i Grim). MI SE fikk et hintsystem.

## 2. Hva som ble kritisert

- **Figurer og bakgrunn på ulikt nivå.** Grim Fandango: skarpe nye figurer på bakgrunner som var nesten urørte. Anmeldere la merke til at figurene stakk seg ut.
- **Nytolkning av figurene.** Monkey Island SE ble kritisert for Guybrush sitt nye hår og et utseende som ikke var helt originalt; noen anmeldere byttet tilbake til klassisk grafikk på grunn av det. Nye tegninger som må følge gamle bevegelser, så stive ut.
- **Låste kombinasjoner.** MI SE lot ikke spilleren kombinere klassisk styring med ny grafikk, eller nye stemmer med gammel grafikk. DOTT løste det med uavhengige brytere.
- **Grensesnitt som skjuler ledetråder.** MI SE la verb og inventar i egne menyer. En anmelder mente det svekket ordspillgåtene, som er avhengige av at man ser inventaret og rommet samtidig.
- **Gamle begrensninger blir synligere.** Eurogamer om DOTT: dithering og lav bildefrekvens i animasjonene synes bedre i HD. Mixnmojo mente den enkle, lite detaljerte stilen noen steder ser ut som forstørrede små bilder.
- **Strukket bilde.** 16:9-valget i Grim gjorde figurene for brede.
- **Lyd og stabilitet.** Grim: lyd i mellomsekvenser kom ut av takt og ble kuttet, og noen krasj. Ingen automatisk lagring.

## 3. Hva vi tar med til The Dig

Vurderingen her er vår egen.

| Lærdom | Hos dem | Hos oss nå | Tiltak |
| --- | --- | --- | --- |
| Originalen kjører under, et lag tegner på nytt | GDC: lese tilstand, endre tilstand, lappe skript | DigHD leser kilden til hver piksel (lese tilstand). Avslutning via menyen og Esc-vakten endrer tilstand. Ingen skriptlapper | Hold den rekkefølgen. Skriv i HD-MOTOR.md hvilken type hver endring er, og lapp aldri skript uten Toms ja |
| To feillister | Originalfeil og remasterfeil | Blandet i todo | Merk funn som `[original]` eller `[HD]`. F5 og HEAP er en originaltekst; assert etter romhopp var vår |
| Master-figurark først | Full Throttle med Larry Ahern | Én referanse per figur er planen i metoden, men Codex fikk «mannskapet i romdrakt» og tegnet tre like kvinner | Lag ett godkjent hovedark for Boston, Brink, Maggie og Pig (forfra, profil, bakfra, i drakt og uten). Tom godkjenner. Alle figurjobber for disse må bruke det |
| Purisme, ikke revisjon | «Purism over revisionism», MI SE kritisert for nytt hår | Godkjent glatt stil, originalen bestemmer form | Ingen ny frisyre, alder eller kroppsform. Avvik krever Toms ja per rute |
| Figurer og rom på samme nivå | Grim: skarpe figurer på gamle bakgrunner | HD-rom fra Codex og myke figurer fra egne ark | Kontroller i spillbilde, ikke enkeltbilde: samme kantmykhet, lysretning og metning på figur og rom |
| Nye tegninger på gamle bevegelser | MI SE så stiv ut, DOTT viste lav bildefrekvens | Fast størrelse per rute (myk.py v2) | Ingen nye mellombilder som endrer tempoet. Sjekk hele animasjoner i bevegelse (animasjonsforhåndsvisningen i todo) |
| Fjern gjenstander, ikke design | Schafer: bort med komprimering og gammel teknologi | Dithering og harde pikselkanter fjernes allerede | Dithering i rommene tegnes som jevne flater. Mønstre som er en del av motivet beholdes |
| Uavhengige brytere | DOTT: grafikk, lyd og UI hver for seg | HD av og på i menyen (F5, HD Graphics) og Ctrl+H | Senere: egne valg for HD-skrift og myke figurer. Ikke nye knapper rundt nettsiden |
| UI som ikke skjuler ledetråder | MI SE-kritikken | The Dig har ingen verbrad | Behold samhandlingen. Inventaret må vise det samme som før |
| Riktig sideforhold | Grim: 4:3 med sidekunst, strukket 16:9 kritisert | Aldri strekk | Mulig senere: sidekunst i stedet for svarte felt, valgfritt |
| Filmene: originalen som fasit | SAN-filer, sjekksumindeks, maltreff, lyd testet for sent | Filmene venter | Når de tas: trekk ut alle SAN-bilder med sjekksum, finn gjentatte bilder automatisk, test med lyd fra første runde, og planlegg lagringsplass (PNG-komprimering) |
| Lyden er allerede god | Grim og DOTT laget ny musikk | The Dig har iMUSE med orkestermusikk og tale fra CD | Ikke rør musikken. Sjekk bare at tale og undertekst går i takt i HD |
| Lete etter kilder | Arkivet på Skywalker Ranch, konseptkunst for uklare detaljer | Spillfilene og stilankre. Konseptbildene i `docs/konsept/` er fra en Reddit-tegner | Uklare detaljer avgjøres fra originalbildet og Toms valg, og noteres. Konseptbildene brukes ikke uten tillatelse og kreditering |
| Ekstramateriale | Kommentarer, gallerier, hint | Ingen | Lav prioritet. Hint og kommentarer endrer ikke spillet, men tas først når spillet er ferdig |

Det viktigste for oss nå, i rekkefølge:
1. Master-figurark for Boston, Brink, Maggie og Pig, godkjent av Tom, før Codex tegner flere figurark for dem.
2. Kontroll av figurer mot rom i ekte spillbilde (samme detaljnivå), som del av den visuelle godkjenningen.
3. Feilene merkes som original eller HD.

## Kilder

- Franzke og Cooke, GDC 2017, Remastering Day of the Tentacle and Grim Fandango: https://www.p1xelcoder.com/resources/GDC_2017_Remastering_DotT_and_Grim.pdf
- Double Fine, Day of the Tentacle Remastered: https://www.doublefine.com/games/day-of-the-tentacle-remastered
- Wikipedia, Day of the Tentacle: https://en.wikipedia.org/wiki/Day_of_the_Tentacle
- Mixnmojo, anmeldelse av DOTT Remastered: https://mixnmojo.com/features/reviews/Day-of-the-Tentacle-Remastered
- Game Developer, Full Throttle Remastered: Curating a classic: https://www.gamedeveloper.com/art/full-throttle-remastered-curating-a-classic
- PC Gamer, Tim Schafer om Full Throttle: https://www.pcgamer.com/uk/tim-schafer-on-making-full-throttle-and-remastering-it-for-a-new-generation
- Game Developer, The Full Throttle Remastered FMV pipeline del 1: https://gamedeveloper.com/programming/the-full-throttle-remastered-fmv-pipeline-part-1
- Game Developer, The Full Throttle Remastered FMV pipeline del 2: https://www.gamedeveloper.com/programming/the-full-throttle-remastered-fmv-pipeline-part-2
- Kotaku, The crazy journey to save Grim Fandango: https://kotaku.com/the-crazy-journey-to-save-grim-fandango-1655133550
- Gaming Trend, anmeldelse av Grim Fandango Remastered: https://gamingtrend.com/reviews/grim-fandango-remastered-a-bumpy-trip-through-the-land-of-the-dead
- PopMatters, anmeldelse av Monkey Island SE: https://popmatters.com/review/109354-the-secret-of-monkey-island-special-edition
- RPGFan, anmeldelse av Monkey Island SE: https://www.rpgfan.com/review/the-secret-of-monkey-island-special-edition
- bit-tech, anmeldelse av Monkey Island 2 SE: https://bit-tech.net/reviews/gaming/pc/monkey-island-2-special-edition-review/1
- Kildene i del 2 av `HD-REMASTER-METODE.md` (Craig Derrick om verbmenyen i MI SE, Shacknews om DOTT).
