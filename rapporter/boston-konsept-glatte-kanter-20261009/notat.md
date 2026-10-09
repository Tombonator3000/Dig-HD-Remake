# Boston Low: ny stilprøve med glatte konturer

Tom avviste den forrige stilprøven, levert i e459337, fordi den hadde mange synlige pikselkanter og ikke lignet konseptet godt nok. Vedlagt eksempel fra Tom er bevart som avvist-eksempel-fra-tom.png.

## Ny grafikk

- boston-gang-hoyre.png: én nytegnet figur i 1024 x 1536, med gjennomsiktig bakgrunn.
- boston-28-ruter.png: 8 stående kropper uten hode, 8 separate hoder og 12 gangruter mot høyre. 1536 x 1024, RGBA.
- Konseptet på main er den visuelle autoriteten: docs/konsept/boston-low.webp, commit d1ebb643b188b508938e59b477d58b7bd23232b8. Uendret kopi som konsept-main.webp.
- Uttrykket er tegnet i 2D med mørke konturer, tydelige skyggeflater, kantet ansikt, grå tinninger, mørk grønnblå skjorte, oransje bukse og mørke støvler.
- Generatorens egne glatte konturer og alfakanaler er bevart. Ingen av de nye bildene er klippet med originalens grovere pikselmaske eller etterredigert med et bildeprogram.

Verktøy: innebygd image_gen. Modellnavn ble ikke oppgitt. Ett forsøk på enkeltfiguren og ett på figurarket. For arket ble 3072 x 2048 bedt om, men verktøyet returnerte 1536 x 1024. Arket er beholdt i faktisk levert størrelse, uten oppskalering.

De to promptene ligger som prompt-enkeltfigur.txt og prompt-figurark.txt. De er skrevet for denne særskilte stilkorrigeringen etter Toms beskjed, og er ikke den opprinnelige jobbprompten ordrett. jobber/fig014_01/prompt.txt er uendret. Dette innebærer ingen generell tillatelse til å endre promptene i andre jobber.

## Kontroll

Begge nye bilder er RGBA med ekte gjennomsiktighet og mange mellomnivåer i alfa, ikke bare 0 og 255. Figurarket har 28 adskilte vesentlige figurområder ved alfa minst 128 og areal minst 100 piksler. Fordelingen 8 kropper, 8 hoder og 12 gangbilder er også kontrollert visuelt.

PNG-filene er vist i en nettleser på lys, mørk og grønn bakgrunn. Sammenligningen er lagret som visuell-kontroll.png. Dette er en visning av grafikkfilene, ikke et skjermbilde fra spillet. Originale PNG-filer er ikke endret for å lage visningen.

filkontroll.json viser faktisk størrelse, format, alfa og sjekksummer. ark-kontroll.json viser opptellingen. sporing.json dokumenterer referanser, verktøy, omfang og beskyttede filer.

## Viktig før bruk i spillet

Den gamle utklippingen legger tilbake originalens pikselmaske i 4x med nærmeste nabo. Dermed kan en glatt tegning få nye trappetrinn. Motorens figurtegning bruker også en hard alfagrense på 128, uten myk blanding mot bakgrunnen. Se TIL-CLAUDE.md med kildepekerne og hva som må kontrolleres ved en integrasjon.

Dette er nye stilkandidater, ikke ferdige erstatninger i modden. Figurarket har nye konturer og enkelte endrede proporsjoner og plasseringer. Det må tilpasses og kontrolleres mot spillets ruterektangler før import. Det er ikke kjørt gjennom gpt-inn, fordi det ville gjeninnføre masken som Tom avviste. Ingen ny påstand om teknisk godkjenning, flimmerfri animasjon eller fungerende integrasjon gis.

Tom vurderer denne stilen før videre produksjon. Den eksisterende jobbleveransen, modden, status.csv, RAPPORT.md, referanse.png, original_1x.png, prompt.txt og jobb.json er bevart.

Konseptbildet er ifølge repoets AGENTS.md laget av en Reddit-tegner og signert. Navnet er ikke bekreftet. Materialet brukes privat som stilreferanse.
