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

2218 PNG-overstyringer:1825 myke HD-ruter,256 indeksbilder og137 vanlige bilder. Indeksverdiene er bevart; enkelte PNG-paletter er rettet til faktisk spillkontekst. Reproduksjonsskript står i `verktoy`, mastere i `produksjon`, referanser i `referanser` og native skjermbilder/kontroller i `kontroll`.

Modflett oppå ferdig r17:1736 eksisterende filer erstattet og473 lagt til, uten slettinger eller utilsiktede endringer. Alle55 filmer er byteidentiske. SHA256SUMS er oppdatert i leveransen. Noen overstyringer er identiske med publiserte filer og gir derfor ingen diff.

- 77 figurtilfeller,656 nytegningskontroller, null avvik.
- 13 ekstra regresjonstilfeller,330 kontroller, null avvik.
- 18 skala-/retningskombinasjoner mot gammel/ny motor,252 kontroller, null nytegningsavvik. Originale aktørpiksler og fullstørrelse-HD innenfor originalrutene er identiske.
- Seks native kontroller av den ferdig flettede leveransen,116 kontroller, null avvik.
- Tre patchstakktester og eksakt gjenskaping av motorens kildefiler består. Nettleserrepoet har samme patch i PR6.

En tidlig test traff en sporadisk avslutningsfeil i gammel motor etter ferdig frame220; separat gjentakelse og senere komplette kjøringer avsluttet normalt. Årsaken er ikke bevist. En kunstig romhopp-test fra en lagring med uforenlige manusvariabler traff originalens walkbox-feil; korrekt lagringskontekst ble brukt i sluttkontrollen.

Full gjennomspilling, alle naturlige overgangsfaser, ny pakket AppImage, mobil/Windows og Toms visuelle godkjenning gjenstår. Automatiske avstandsmål godkjenner ikke identitet eller stil.
