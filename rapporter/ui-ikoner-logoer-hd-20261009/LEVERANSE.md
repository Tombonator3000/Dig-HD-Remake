# HD for logoer, inventar og grensesnitt

Tom bestilte 9. oktober 2026: «hd oppgrader alt av logoer ikoner inventory o.l». Denne leveransen dekker inventaret, handlingstegn og markører på ikonarkene, håndcomputerens grensesnitt og de tre identifiserte logomotivene. Dette er en grafikkleveranse på gpt-arbeid. Claude står for mottak og motor, Tom godkjenner utseendet.

## Levert

| Område | Filer | Dekning |
| --- | --- | --- |
| Inventar og handlingstegn | jobber/ikon01 til ikon03/resultat.png og notat.md | 143 inventarikonbilder, med vanlige, markerte og nedtonede tilstander, samt 6 fargeknapper fra rom 107. Til sammen 149 oppføringer. |
| Håndcomputer | jobber/lag079_01 til lag079_06/resultat.png og notat.md | Alle de 20 små UI-objektbildene i disse jobbene: PenUltimate-logoen, kontaktportretter, hjelp, tilbake, telefon, tastatur, lander og indikator. |
| Glatte, frilagte inventarikoner | assets/ikon01-rgba.png til ikon03-rgba.png | De samme 149 oppføringene i RGBA, med generatorens egne konturer. Tilpasset import kreves. |
| Fargeknapper | assets/seks-fargeknapper-rgba.png | Alternativ med seks tydelige, sammenhengende sekskanter i originalens fargerekkefølge. |
| LucasArts | assets/lucasarts-logo-rgba.png | Frilagt HD-versjon av logoen i starten av SQ1.SAN. Originalens lilla L, vertikale LUCAS, Arts, gullfigur og registreringsmerke er bevart som motiv. |
| THE DIG | assets/the-dig-logo-rgba.png | Frilagt HD-logo til grensesnittbruk. Eksisterende jobber/rom106/resultat.png er bevart og er fortsatt tittelskjermens ordinære leveranse. |

Alle ni ordinære resultater og seks tilleggsark er 1536 x 1024. De seks tilleggsarkene er RGBA med faktisk gjennomsiktighet. PNG-filene er kopiert byteidentisk fra bildeverktøyet. Ingen genererte tegninger er etterbehandlet med Python, malt om eller beskåret i denne leveransen.

25 bildeforsøk totalt. Den første LucasArts-prøven hadde feil lerretsformat og ble forkastet. Syv av ni valgte ordinære resultater består lokal helbildekontroll. lag079_05 får sjekk, lag079_06 får avvist i samme kontroll. Se vurderingen nedenfor. De offisielle status.csv, RAPPORT.md og retur.md er ikke endret.

## Hva som er kontrollert

- Eksisterende prompt.txt er brukt ordrett for alle ordinære jobb- og returforsøk. referanse.png er første bilde og jobbens stilbilde er bilde to.
- 36 beskyttede filer, fire per ordinær jobb, har uendrede SHA-256-summer. Summene finnes i kontroll/originalfiler-sha256.json.
- Alle 169 objektoppføringer finnes i leveransen. Den ordinære enkeltobjektkontrollen har målbar omrissinformasjon for 166. obj650_02, obj688_01 og obj688_02 mangler tilstrekkelig signal i denne kontrollen. De er også sett ved visuell sammenligning; fravær av måling er ikke et automatisk bestått resultat.
- Samtlige målbare enkeltobjekter er innenfor kontrollens omrissgrense. De valgte ikonarkenes globale kantlikhet er 0,982, 0,991 og 0,983.
- RGBA-arkenes antall og radfordeling er kontrollert: 55, 56 og 38 oppføringer. Et diagnostisk rutekart med 149 unike objekt- og tilstandsnavn følger med.
- De frilagte ikonene, logoene og fargeknappene er faktisk gjengitt i nettleser på lys, mørk eller mørkeblå, og grønn bakgrunn. Se kontroll/rgba-kontroll.png og kontroll/ikoner-rgba-kontroll.png. Bildeverktøyets innebygde forhåndsvisning viser farger også under usynlige piksler; nettleserbildene viser PNG-enes faktiske alfa.

Kontrollen er kjørt med uendret gpt._evaluate fra origin/main 35197b785a70bea1048823a8cfa2659634e774f6, mot originalobjekter lest fra spillets DIG.LA1. DIG.LA1 SHA-256 er 8f2a0474dfe2d99c37b8182b08d8bb79afe95388df5c9d608ae3bb267536a957. Verktøyet er den innebygde ChatGPT-bildegeneratoren image_gen; eksakt modellnavn oppgis ikke av verktøyet.

## Forhold som må følges opp ved mottak

lag079_05 har et globalt blokkavvik på 1,09 originalpiksler. lag079_06 har 2,88. Begge jobbene har også vært kontrollert på de faktiske UI-rektanglene, som er det mottaket skal klippe ut. Alle fem slike utsnitt består den lokale prøven for samlet forskyvning og kantlikhet. Utsnittene er for små til blokkprøven, så dette avklarer ikke alle lokale deformasjoner. Det viser at helbildeavviket alene ikke beskriver kvaliteten i de eksporterte UI-utsnittene. Det overstyrer ikke gpt-inn. Claude må kontrollere disse to lagene før de settes inn. Rå forsøk på hele håndcomputeren skal ikke erstatte godkjent hånd eller apparatbakgrunn.

Portrettene på håndcomputeren varierer fortsatt i detaljnivå. Enkelte beholder et tydeligere pikselpreg enn de frilagte inventarportrettene. Dette er oppført i notatene, ikke skjult som ferdig spillgodkjenning.

Frileggingen av ikonene flyttet og skalerte motivene på arkene. Originale jobb.json skal derfor ikke brukes direkte på tilleggsarkene. rutekart.json angir foreslåtte kildeceller og originalens mål, men er ikke et ferdig, spillgodkjent atlas. Kontroller normal, markert og nedtonet tilstand sammen. Små forskjeller i malt detalj mellom tilstander må samordnes ved mottak.

De seks fargeknappene blir fortsatt diffuse i de ordinære ikon03-forsøkene. Det særskilte alternativet har en tydeligere kontur og kraftigere kant enn originalen. Velg og tilpass dette som et sammenhengende sett, ikke som seks uavhengige nye knapper.

Gåteglyfer og de små illustrerte tavlene er visuelt sammenlignet, men automatisk kantlikhet beviser ikke semantisk identitet. Kontroller de utskårne symbolene ved faktisk størrelse før spillgodkjenning.

## Dekning og avgrensning

De to ensfargede inventarrutenettene obj618_01 og obj627_01 trenger geometrisk oppskalering i mottaket, ikke nye malte symboler. De er bevisst utenfor ikonarkene i eksisterende jobboppsett. Menytekst og undertekster tegnes som tekst av motoren; eksisterende xBR-tekstvei er beholdt.

Spillverdens dører, maskindeler, kartmarkører i landskapet og øvrige romlag inngår ikke automatisk i denne UI-leveransen. Håndcomputerens seks lag er den konkrete UI-delen av den større lagbestillingen. Hele introfilmen er heller ikke oppskalert; LucasArts-logoen er levert som separat grafikkressurs.

Ingen nye filer her er satt inn i offisiell hd-mod, kjørt i spillmotoren eller godkjent visuelt av Tom. Les TIL-CLAUDE.md for neste konkrete handling.
