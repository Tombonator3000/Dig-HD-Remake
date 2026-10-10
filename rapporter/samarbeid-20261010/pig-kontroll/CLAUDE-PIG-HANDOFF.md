# Pig 007_02–09: kildekontroll og kandidater

Tre ark er klare til roots kontroll, fem holdes. 15 native arkforsøk og én separat lampereferanse er bevart. Root publiserer serialisert til `gpt-arbeid`. Denne agenten har ikke endret leveranser, fellesregistre eller Git.

Arbeidsmappe: `/home/tombonator3000t/.codex/tasks/the-dig-romlag-brink-20261010/agent-pig`.

## Valgte kandidater

| Jobb | Forsøk | Rader | Hovedruter | Native SHA256 |
|---|---:|---|---:|---|
| fig007_05 | 1 | 8, 9, 10, 1 | 28 | 6043eea7311d4199d245fd9a490175caf170a7a468ff402caf08436575c4c90c |
| fig007_08 | 3 | 2, 1, 2 | 5 | 198d1f0b9ae4cdef4cc2e4587257aa70f21af7cf932e23fbba60e56057b0cf9f |
| fig007_09 | 1 | 7, 1 | 8 | 20afac9c8e626d637164f36a5b251d2906c8f68f6b5b1d2f24c5710d286472fb |

005 har 41 ekte native komponenter gruppert til 28 kilderuter med dokumenterte separate ringer, senterskiver og kapper. Det er faktiske deler av samme originalfase, ikke nye objekter. Grå alfakompositt viser de transparente ringåpningene. Dreiningen mot loddrett og de seks originale frontglimtene er beholdt.

08 forsøk 3 erstatter forsøk 2. Den mørke ytre sideflaten i siste kildefaser er tilbake. Endene er lukket, og bare de to kildebestemte fasene har hvitt panelglimt. 09 har åtte baksidefaser uten hvitt glimt. Begge består streng alfakontroll uten unntak. Alle tre valgte kandidater består lokal kildekontroll og QA; dette er ikke Toms visuelle godkjenning.

`ready-native-batch.json` inneholder de tre valgte postene med nøyaktig fullprompt, refs, native sti, SHA, beskyttede kildehasher, manuell kontroll og eventuell kildegruppering. Tilsvarende `*-proven.batch.qa.json` og `*-source-proven-guide.png` viser kontrollen. `manifest.json` inneholder alle forsøk, også avviste og erstattede.

## Holdes

- **fig007_02, forsøk 5:** korreksjonen har redusert trepunktsrekken, men flere kapper/hengsler har fortsatt ekstra sterke røde punkter. Den ekte løse kappen i costume007_060 forsvant i forsøk 4 og er gjenopprettet i forsøk 5. Videre native retting må bevare alle ringer, senterskiver, kapper og begge glimt i 056.
- **fig007_03, forsøk 2:** flere grønne lamper fra 001-ankeret står fortsatt igjen. Kildepunktet i costume007_064 er utelatt. Avklar originalalfa og ruteboks med Claude før videre import; se nedenfor.
- **fig007_04, forsøk 1:** hele enheter arver fortsatt tre grønne kappepunkter der kilden viser svakere, fasebestemte indikatorer. Rett lampestatene nativt, og dokumenter deretter alle ekte delgrupper. Bevar de to glimtene i 098, hullene i 087/097 og småfragmentene 011/010.
- **fig007_06, forsøk 1:** flere kapper arver ekstra/sterkere grønne lamper. Sparsomme delruter, særlig 005/004/170, blir lengre og mer komplette kurver; gap og delgrenser trenger ny kildekontroll. Streng alfa rapporterer dessuten fem piksler over 16 utenfor fem piksler fra kjernen, maksimum 29. Ingen glødbegrunnelse er etablert for disse pikslene.
- **fig007_07, forsøk 1:** enkelte delvis forsvunne kilderinger blir hele ringer. costume007_191 blir en dekorert liten lyspærelignende gjenstand, og andre småfragmenter blir avrundet/fullført. Rett de konkrete delrutene nativt før gruppering og levering.

Rå sammenhengende komponenter er ikke det samme som antall kilderuter. Ark med ringer, senterskiver, løse kapper og sparsomme delruter skal ikke få vilkårlige sammenslåinger for å tvinge tellingen grønn.

## Claude: originalrute 064 og importrute

`costume007_064` har kildeboks `[88,4,174,134]` i original 1x og `[416,48,696,536]` i referanselerretet. En enslig RGB `(0,0,0)`-piksel ved 1x `(261,137)`, en 4 × 4-blokk ved `(1108,580)`, strekker boksen. Dette er bekreftet i både `original_1x.png` og `referanse.png`. Begge er flate RGB-bilder, og punktet er ikke magenta. Individuell original-RGBA mangler i brukt uttrekk, så faktisk runtime-alfa er uverifisert. Native 03 forsøk 2 har alfa 0 i denne blokken.

Kontroller dekoder, palett og alfa samt originalrutens offset og baseline før boksen trimmes, eller punktet bevares som synlig grafikk. Ikke strekk selve enheten slik at den fyller denne store, sparsomme boksen. Separat målebevis finnes i `fig007_03-064-source-pixel-proof.json/png`.

For de valgte kandidatene må importruten bruke korrekt originalruteordre og faktisk tilpassing per rute. Native arkets marginer, baseliner og størrelse er ikke eksakt originalgeometri. Når individuell original-RGBA finnes, kontroller pose, offset, alfa, faktisk størrelse og sammenheng mellom 007-arkene. Det er ikke utført full original-RGBA-import, integrering eller spilltest av denne agenten.

## Bevaring

Alle 32 beskyttede originalfiler er hashkontrollert uendret: `referanse.png`, `original_1x.png`, `prompt.txt` og `jobb.json` for de åtte jobbene. Hver fullprompt starter med jobbens `prompt.txt` ordrett. 007_01-ankeret er hashidentisk med den oppgitte native filen `exec-cbc7fcd8-e923-4ed6-8d5f-f1aca5a90752.png`.

Leveransebildene er uendrede native PNG-er. Ingen kreativ etterbehandling, ny alfa eller masker er brukt. Gråkompositter, ruteveiledninger og kildeutsnitt er diagnostikk. Den store lampereferansen er en kildekorrektiv prøve, ikke en separat leveranse eller en ny godkjent stil.
