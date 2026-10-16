# R18, 16. oktober 2026

Tom bekreftet at de nye feilbildene er fra publisert AppImage. Rapporten bevarer hans motiver og de godkjente pilotarkene som fasit. R18 er ikke publisert som AppImage; gjeldende utgitte distro er fortsatt r16.

## Rettet i kandidaten

1. Boston/Maggie/Brink: halskontakt og hodefarger. Hovedkostymenes ansikt/hår er ikke flyttet i halsrettingen. Brink16/17 får ikke ekstra manuell avmetning oppå spillets fargetilpasning. Egen tale-/gestgrafikk38/47/48/188 bruker de samme pilotavledede hodeatlasene. Motor-PR65 gir alle nedskalerte deler aktørens faktiske skala.
2. To separate måner148/149 foran hverandre. Faktisk AKPL-/rompalett er brukt, ikke råfarger. De to genererte måneteksturene er skilt med sammenhengende alfaflater, ikke et fast midtkutt. Originaleffekt150 beholder sitt motiv, sine indeksverdier og timing, men får mekanisk jevnere alfa for å unngå gamle pikselbiter over månene.
3. Plateau55 har mer malte detaljer i fjell og plante. Utgravd åpning387 og jordtilstandene388 deler ny bakgrunnstekstur; uendrede deler av objektrektanglene samsvarer med rommet.
4. Figurkontroll utvidet til tale-/handlingslag og kontaktbredde.17 relevante kostymer,1511 sammensatte poseringer, ingen flagget halsavstand eller for smal kontakt. Mulige lagpar er ikke bevis for hvert tidsforløp i spillet.
5. Gangflaten til tram er objekt890 i rom80, med samme tegning i554/983.197 geometriske bildepunkt-treff lokaliserte Toms screenshot. Blå tramflate og kildegeometri beholdes. Gangflaten er tegnet tydeligere i samme lys og farge som scenen.
6. Nest136 er nå en mørk kjempeedderkoppsilhuett, ikke mus.70 ruter, samme kildeplassering og størrelse. De åtte tegnede gangfasene gjenbrukes over kildeserien; full naturlig hendelsesovergang er ikke visuelt godkjent av Tom.
7. Rist356/357 er tettet av organisk bøss.357_02 er fortsatt original HD-tilstand med åpen rist og rennende vann. Første genererte ristmaster med feil uttrykk er ikke importert; ny lukket tilstand bruker grottens malte stil.
8. Alle56 ruter for laser233/234/235 er lyse stråler. Kontaktpunkter/retninger følger originalens lyse strålepiksler, uten rør eller endestykker.

Pole178 fra r17 er også med:285 ruter registrert med kropp og lang stav hver for seg. Stavens lengde bestemmer ikke figurens størrelse.

## Leveranse og kontroll

2223 PNG-overstyringer:1830 myke HD-ruter,256 indeksbilder og137 vanlige bilder. Indeksverdiene er bevart; enkelte PNG-paletter er rettet til faktisk spillkontekst. Reproduksjonsskript står i `verktoy`, mastere i `produksjon`, referanser i `referanser` og native skjermbilder/kontroller i `kontroll`.

Modflett oppå ferdig r17:1741 eksisterende filer erstattet og473 lagt til, uten slettinger eller utilsiktede endringer. Alle55 filmer er byteidentiske. SHA256SUMS er oppdatert i leveransen. Noen overstyringer er identiske med publiserte filer og gir derfor ingen diff.

- 77 figurtilfeller,656 nytegningskontroller, null avvik.
- 13 ekstra regresjonstilfeller,330 kontroller, null avvik.
- 18 skala-/retningskombinasjoner mot gammel/ny motor,252 kontroller, null nytegningsavvik. Originale aktørpiksler og fullstørrelse-HD innenfor originalrutene er identiske.
- Seks native kontroller av den ferdig flettede leveransen,116 kontroller, null avvik.
- Tre patchstakktester og eksakt gjenskaping av motorens kildefiler består. Nettleserrepoet har samme patch i PR6.

En tidlig test traff en sporadisk avslutningsfeil i gammel motor etter ferdig frame220; separat gjentakelse og senere komplette kjøringer avsluttet normalt. Årsaken er ikke bevist. En kunstig romhopp-test fra en lagring med uforenlige manusvariabler traff originalens walkbox-feil; korrekt lagringskontekst ble brukt i sluttkontrollen.

Full gjennomspilling, alle naturlige overgangsfaser, ny pakket AppImage, mobil/Windows og Toms visuelle godkjenning gjenstår. Automatiske avstandsmål godkjenner ikke identitet eller stil.

## Siste atlasopprydding

Ekstra native kontroll av variantene38/47/48/188 viste en løs atlasrest over Maggies hode i47. Frakoblede små alfakomponenter er fjernet fra895 hoderuter uten å flytte eller endre den største ansikts-/hodeflaten. Dette omfatter også svært små løse kantpiksler. Indeksbilder, kropp og animasjonstiming er uendret. Varianten er kontrollert på nytt i native motor.

Tom bekrefter at tram-punktet gjelder gangbroen fra steinkanten inn i den blå kulen. En normal tram-call-test kalte riktig knapp859, men innstigningsklikket kom mens trammen fortsatt var underveis og traff derfor ingen inngang. Dette er ikke en bestått full innstigningstest; tvungne sluttstilstander er kontrollert separat.

Etter alfaoppryddingen er alle1511 sammensatte poseringer kontrollert igjen, uten flagg. Hele native figurregresjonen er også gjentatt på integrert leveranse:77 tilfeller/656 kontroller, null avvik.

## Alle navngitte figurkostymer

Alle60 navngitte menneske-/romdraktkostymer er inventarisert.52 gir2422 sammensatte poseringer. Én beregnet kombinasjon i137 er allerede44,56 originalpiksler fra hverandre i originalen; tvungen native kontroll viser samme løse ekstrahode i både original og HD. Det er ikke en ny HD-halsforskyvning. Kontrollverktøyet rapporterer slike kildepar separat, i stedet for å flytte originalens animasjonsdeler for å få et falskt treff. Ingen nye avstands-/kontaktavvik er flagget i de øvrige kildebaserte parene.

De resterende åtte kostymene har ingen målbar separat hode-/kroppskombinasjon. De er registrert som hele figurer, med representative utsnitt for68,173,72,69,37,70,221 og8. Dette er automatisk kilde-/registreringskontroll og et visuelt utvalg, ikke en full visuell godkjenning av hvert animasjonsbilde. Se kontroll/alle-menneskekostymer og hele-figurvarianter.png.
