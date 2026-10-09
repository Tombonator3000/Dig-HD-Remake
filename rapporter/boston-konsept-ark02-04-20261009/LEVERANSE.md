# Boston Low: ark 2 til 4 i den godkjente tegnede stilen

Tom godkjente 9. oktober 2026 den nye glatte Boston-tegningen med «Mye mye bedre! Lag de andre sånn med så mye detaljer også». Resten av den bestilte Boston-piloten er nå tegnet i denne retningen.

| Jobb | Innhold | Ruter | Bildeforsøk |
| --- | --- | --- | --- |
| fig014_02 | Gange mot venstre og snakking mot høyre og venstre | 62 | 2 |
| fig014_03 | Hoder i de seks øvrige retningene | 127 | 1 |
| fig014_04 | Gange mot kamera | 12 | 2 |
| Sum | Tre nye ark | 201 | 5 |

Hvert resultat ligger i jobber/<jobb>/resultat.png med notat.md ved siden av. Alle tre er 1536 x 1024 RGBA og identiske med det valgte bildet fra den innebygde ChatGPT-bildegeneratoren. Eksakt modellnavn ble ikke vist.

## Stil og referanser

Den godkjente store tegningen og det nye 28-ruters arket fra bdae1ae69d322a334bd9f01691961c5f14ed1d2e ble brukt som stilreferanser. Hver jobbs referanse.png ble brukt som pose- og rekkefølgeguide. Dette viderefører det nye tegnede ansiktet, grå tinninger, mørk grønnblå skjorte, oransje bukser, klare skyggeflater og glatte konturer.

Den gamle leveransen i jobber/fig014_01/resultat.png er ikke erstattet. For et sammenhengende nytt sett skal Claude bruke rapporter/boston-konsept-glatte-kanter-20261009/boston-28-ruter.png som ark 1. Da har den nye stilrunden 28 + 201 = 229 tegnede ruter totalt. Toms godkjenning gjelder stilretningen; de tre nye arkene har ikke fått separat vurdering.

## Kontroller

- Målt antall separate figurområder og radfordeling mot jobb.json: 62, 127 og 12.
- Kontrollert 1536 x 1024, RGBA, filhash og at generatorens native alfa er bevart.
- Visuell inspeksjon av alle ark på lys, mørk og grønn bakgrunn i visuell-kontroll.png.
- Sammenlignet representative kropp-, ansikt- og hodeutsnitt med den godkjente store tegningen i detaljkontroll.png.
- Kontrollert at referanse.png, original_1x.png, prompt.txt og jobb.json er uendret i alle tre jobber.

Ingen original pikselmaske, nærmeste-nabo-oppskalering, fargelås eller kantvask er lagt over de nye PNG-filene. Bildene er ikke etterbehandlet med et annet bildeverktøy.

Filkontrollen måler svært svak restalfa utenfor figurene. Med de diagnostiske boksene i rutekart.json er høyeste alfa utenfor boksene 10 av 255; bakgrunnspikslene er ellers i hovedsak helt gjennomsiktige. De viste kontrollbildene bruker PNG-alfakanalen, og viser ingen tydelig fargematte. Full native alfa er beholdt. Rutekartets bokser med to pikslers marg er ikke lossless eksportbokser.

## Import og neste steg

Dette er ferdige tegninger til mottak og vurdering, ikke en bekreftet spillintegrasjon. Størrelse og plassering avviker fra de gamle utklippsrektanglene. Ikke kjør dem blindt gjennom det gamle mottaket, som legger tilbake originalens grove alfamaske.

TIL-CLAUDE.md beskriver tilpasningen og hva som må kontrolleres. Pose- og munnfaser, hodefeste, fotfeste, riktig bakgrunnsblanding og animasjonsflimmer må testes i motoren. Ingen motor- eller spillkode er endret her. status.csv, RAPPORT.md og returer er overlatt til Claude.

## Sporing

- prompt-fig014_02.txt, prompt-fig014_03.txt og prompt-fig014_04.txt er de nye stilpromptene.
- prompt-fig014_02-antall.txt og prompt-fig014_04-antall.txt dokumenterer de to smale antallskorreksjonene.
- sporing.json har valgte kilder, forsøk, filhash og originalfilenes sjekksummer.
- filkontroll.json har mål, alfa og antallskontroll.
- rutekart.json har original rute-ID, retning, animasjon, lag, rekkefølge og målt ny bildeboks.
- SHA256SUMS har sjekksummer for leverte filer.

Tillatelsen til nye stilprompter gjelder denne Boston-piloten. Øvrige figurer, de 236 lagjobbene, de tre ikonarkene og generelle korrigeringsprompter for andre jobber er ikke bestilt av denne beskjeden. Alt leveres bare i det private repoets gpt-arbeid.
