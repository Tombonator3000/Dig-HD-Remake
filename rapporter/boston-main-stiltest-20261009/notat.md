# Boston Low: stilprøve fra konseptet på main

Tom ba 9. oktober 2026 om en test med Boston Low i stilen til eksempelgrafikken på main. Dette er en separat kandidat med de samme 28 rutene som fig014_01: 8 stående kropper, 8 separate hoder og 12 gangruter mot høyre.

## Bildearbeid

- Redigeringsgrunnlag: jobber/fig014_01/referanse.png.
- Bilde to: docs/konsept/boston-low.webp fra main, commit d1ebb643b188b508938e59b477d58b7bd23232b8. En uendret kopi ligger her som boston-low-main.webp.
- Prompt: jobber/fig014_01/prompt.txt ordrett, inkludert avsluttende linjeskift. Den nøyaktige teksten ligger i prompt-brukt.txt. Ingen tillegg eller korrigeringsprompt.
- Verktøy: innebygd image_gen. Verktøyet oppga ikke et bestemt modellnavn.
- Forsøk: 1. PNG, 1536 x 1024.
- Uttrykk: kantet ansikt, tydelige tegnede skyggeflater og grått hår ved tinningene fra konseptet. Poser, størrelse og plassering følger originalarket.

Konseptbildet er ifølge repoets AGENTS.md laget av en Reddit-tegner og signert i kildebildet. Navnet er ikke bekreftet. Det brukes her som privat stilreferanse.

## Lokal teknisk kontroll

Prosjektets eksisterende gpt-inn er kjørt på en separat kopi av denne ene jobben. Den offisielle status.csv, RAPPORT.md og jobbmappen er ikke endret av stiltesten. Teknisk status godkjent betyr at kontrollgrensene er bestått, og er ikke Toms godkjenning av denne nye stilen.

| Måling | Resultat |
| --- | --- |
| Lokal teknisk status | godkjent, 28 av 28 ruter |
| Forskyvning, originalpiksler | x 0,03, y -0,04 |
| Største lokale forskyvning | 0,20 originalpiksler |
| Kantlikhet for hele arket | 0,989 |
| Laveste omrissoverlapp | 0,847, grense 0,80 |
| Laveste kantlikhet per rute | 0,732, grense 0,50 |
| Laveste dekning | 0,938 |
| Flimmerkontroll | 11 nabopar, høyeste ekstra forskjell 19,8, grense 30 |

Den turkise bakgrunnen og den grå kanten har svak fargevariasjon i genereringen. Rutene klippes ut med originalens alfamaske av den eksisterende pipelinen. Alle 28 utklipp er kontrollert som RGBA med nøyaktig 4x størrelse og identisk alfa med originalen skalert 4x. De 28 indeksbildene er byteidentiske med originalene.

## Filer og bruk

- resultat.png: det genererte arket, uten etterredigering.
- costumes/: 28 utklipte RGBA-ruter etter prosjektets fargelås og kantbehandling, samt 28 originale indeksbilder. Dette er et tillegg til en full HD-pakke, ikke en komplett pakke for nettleserens mappeimport.
- kontroll-sammenligning.png: original 4x, nytt ark og resultat etter fargelås, fra venstre mot høyre. Laget av eksisterende gpt-inn.
- kontroll.json: målinger og kontroll av alle rutenes format, alfa og indeksbilder.
- provenance.json og stiltest.json: filnavn, kilder, innstillinger og sjekksummer.
- prompt-brukt.txt: prompten som ble sendt til bildeverktøyet.

Den eksisterende fig014_01/resultat.png er bevart. Repoets ordre fra 09:50 sier at den tidligere piloten er godtatt og satt i HD-modden; denne alternative stilprøven erstatter den ikke automatisk. Den nye kandidaten er ikke installert i spillet eller testet i motoren. Tom vurderer stilen før en eventuell utskifting eller produksjon av flere ark.

SHA256 for nytt resultat.png: b92254a65d63c193ae9d67f8af2241d941475a72764c67ad06c9cbcf2797f61a.
