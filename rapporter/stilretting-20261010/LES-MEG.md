# Stilretting etter Toms avvisning

10. oktober 2026. Én ny Boston-prøve er laget med det opprinnelige konseptet og den direkte godkjente glatte Boston-prøven som visuell autoritet. Se `sammenligning.png`. Prøven er et avgrenset grunnlag for Toms vurdering før ny serieproduksjon.

## Ny prøve

`boston-stilprove.png` viser Boston i huk, vendt mot venstre. Posen kommer fra `costume014_289` i `jobber/fig014_16`, ikke fra et av de avviste arkene. Originalutvalget er dokumentert i `utvalg.json` og vist i `boston-original-costume014_289.png`. Navnet Boston Low er bekreftet i denne jobbens metadata.

Ansiktet er kantet, håret er brunt med grå tinninger, skjorten er mørk grønnblå, buksen oransje og støvlene mørke. Figuren bruker tegnede konturer, fine indre streker og kontrollerte skyggeflater. Prøven er vist ved siden av konseptet, den godkjente Boston-figuren og originalposen, og på lys, mørk og grønn bakgrunn i `stilprove-tre-bakgrunner.png`. Ansikt, hår, klær, retning, hender, støvler og ytterkonturer er kontrollert visuelt. Ingen synlig farget glorie eller sterke røde/gule prikker ble sett ved vanlig alfakomposisjon.

Verktøy: innebygd ChatGPT-bildegenerator. Ett bildeforsøk. Verktøyet bekrefter ikke et eksakt modellnavn. Prompten er bevart i `prompt-stilprove.txt`. 1024 x 1024 ble foreslått; faktisk native resultat er 1254 x 1254 RGBA. Filen er kopiert byteidentisk med native alfa, uten oppskalering, bakgrunnsfjerning, maskering eller annen kreativ etterbehandling. Sammenligningsbildene er separate visninger laget med vanlig alfakomposisjon. `filkontroll.json` inneholder størrelse, alfa og sha256.

Denne prøven erstatter ingen `resultat.png`, oppdaterer ingen leveransetelling og er ikke et ferdig figurark. Posen, proporsjonene og fotpunktene er ikke kontrollert ved import. Spillintegrasjon, animasjon og flimmer er ikke testet. Tom har ikke vurdert denne nye prøven ennå. Serieproduksjonen er ikke startet igjen.

## De avviste vedleggene er sporet

| Vedlegg i overleveringen | Sikkert registrert forsøk | Status og innholdsavvik |
| --- | --- | --- |
| `avvist-graaharet-figur.png` | `fig103_02`, forsøk 1, native `exec-b001966d-2dbb-40c9-80ee-3490cc5702ac.png` | Allerede tilbakeholdt. Native arket viser 7,7,3 større former der kildekontrollen krever 7,10,3. Tre reelle faser mangler. Figuren er ikke navngitt i jobbmetadataene. |
| `avvist-flygende-figur.png` | `fig170_04`, forsøk 1, native `exec-d3b4026e-780e-486a-bc5a-68cf771eacbb.png` | Allerede tilbakeholdt. De store blå plattform-/oppløsningsformene i originalen er utelatt, og en hel mann er funnet på rundt den lille synlige figuren. |

Sporingen bygger på faktisk bildeinnhold og forsøksregistreringene i det lokale taskområdet. Vedleggene er ikke byteidentiske med native PNG. De har imidlertid identisk alfa i hver piksel, samme mål, og vanlig komposisjon avviker med høyst 1 av 255 per fargekanal på alle tre bakgrunner. Dette, sammen med registreringene, identifiserer forsøkene. Begge native sha256 stemmer med de eksisterende oppføringene i `tilbakeholdte-kandidater.json`. Ingen av disse jobbene står i `leveranser` i den gjeldende fremdriftsfilen for øvrige figurer.

Røde og gule prikker i vedleggsvisningen er undersøkt i faktisk RGB/alfa. De rent røde og gule flekkene ligger i nesten gjennomsiktige piksler, hovedsakelig alfa 1 av 255. De sterke prikkene i råvisningen er ikke synlige ved vanlig komposisjon på de tre bakgrunnene. Dette er en observasjon av filene og visningen, ikke et bevist funn om årsaken i spillmotoren. Ingen piksler eller rester er slettet. Se `avviste-vanlig-komposisjon.png` og `kildekontroll.json`.

## Uavklart kildegrunnlag

`fig103_02/referanse.png` og `original_1x.png` viser nesten hele kroppen i et smalt felt av varme hudtoner, også der kandidaten har fått hår, skjorte og bukse. Kildedataene i denne jobben bekrefter ikke kandidatens grå hår og beige bukse. `fig103_01/resultat.png` er en tidligere generert kandidat og er ikke en selvstendig visuell autoritet. Jobb 103 kan derfor ikke få en ny, antatt identitet bare ved å kopiere Boston eller et eldre ark. Fargemønsteret er dokumentert, men det er ikke påvist at pipelinen eller palettvalget er feil. Claude må avklare den faktiske figuren, palettbruken og eventuelle effektlag mot originalspillet før produksjonskorrigering av dette arket.

Den nye prøven bruker derfor et sikkert navngitt Boston-kostyme for å kontrollere selve tegnestilen. Den er ikke presentert som en rettet leveranse for jobb 103 eller 170. Den konkrete menneskelige stilrettingen og den eksisterende tillatelsen for de 54 hovedkostymene dekker prøveprompten. Ingen av de øvrige opprinnelige jobbpromptene er endret, og de 43 tidligere foreslåtte korrigeringspromptene er ikke tatt i bruk.

## Bevaring og neste steg

Arbeidet er utført i grafikkcheckouten på `gpt-arbeid`, etter fetch og fast-forward til `5f018d7380ae227d81c4aabe3dc2fe813f23158f`. Alle eksisterende lokale endringer og uregistrerte filer er bevart. `referanse.png`, `original_1x.png`, `prompt.txt` og `jobb.json` for de to berørte jobbene og kildejobben er hashregistrert og uendret. `status.csv`, `RAPPORT.md`, `retur.md`, motorkode og øvrige checkout-er er ikke endret. Senere native kandidater fra de avbrutte produksjonsløkkene er ikke levert.

Rutinesjekkens lagrede `target_thread_id` er allerede denne nye chatten, `01a1245d-6acb-71d0-93d5-85b7e61fd829`. Den beholder sin lesende prompt og er ikke opprettet på nytt eller endret i denne økten.

Tom vurderer det konkrete uttrykket i denne nye prøven før mer figurproduksjon. Omfanget for resten av den bestilte grafikken er fortsatt autorisert. Deretter må et komplett korrigert ark kontrolleres mot alle reelle kildedeler og importeres av Claude før videre serieproduksjon bygger på det. Spørsmålet om en bredere generell promptendring gjentas ikke.
