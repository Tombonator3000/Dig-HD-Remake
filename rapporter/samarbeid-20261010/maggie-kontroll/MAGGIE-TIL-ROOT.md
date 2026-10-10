Ni Maggie-romdraktark er klare til root-kontroll. Nativebilder er produsert med den innebygde bildegeneratoren og beholdt byteuendret. Kostyme, poser og fargefelt er kontrollert mot hvert RGB-kildeark, og Maggies ansikt/hår mot hennes egen konseptreferanse. Boston-konseptet brukes bare til tegnestil.

| Jobb | Forsøk | Hovedruter | Utelatte magentaoppføringer | Native deler | SHA256 |
|---|---:|---|---:|---:|---|
| fig002_01 | 4 | 7+1 | 0 | 8 | cb6c8bbedd7cbbf19c636a4d8d260100fe71f3eea1e7e15bc0084e5ded32f6bc |
| fig002_02 | 1 | 7+7+5 | 0 | 20 | 7468e4039ea88d65bcac3f8105f8e5e85d3fb8264024bee885da62fd7f675f83 |
| fig002_03 | 1 | 7+7+7 | 0 | 21 | a65a6e4dd9612937bc8571601de17bf2ce531e733d9a5d776c4a6fb0f2501edf |
| fig002_04 | 2 | 2+4+3 | 6 | 9 | e484f965e8c463f84974bc607c24ef9bddc3b5ae4dcedc06bd441fc188ec9ffb |
| fig002_05 | 2 | 4+3 | 14 | 10 | 0d0e50653f9877f809226f4ff9901c4a79198c3e508b7a18fff22fac6235647f |
| fig002_06 | 1 | 1+1 | 6 | 2 | 6228803ddef5a33c26ad087724c07cd21064140f924b30eb92ef6e5af991adc8 |
| fig002_07 | 2 | 1+1+3 | 2 | 7 | f15a5b3cc2ca1bdf78aa78f6e68bd4f1db9d371f83e634e4658689a7d7ceb08b |
| fig002_08 | 1 | 2+1 | 4 | 3 | 6731e92d9217d474a6d343d867e0bb9c5446f9c376c8ad94e5eeda94ab6cdde6 |
| fig002_09 | 2 | 1 | 9 | 1 | 36e102520d9358bc9a7a607cf3ad02babee0d4bc73cb24a794398a3178465287 |

Totalt 75 hovedruter, 41 utelatte tekniske magentaoppføringer og 81 native kjernedeler. Ekstra kjernedeler er en liten hanskepiksel i02, tre kildestøttede visirbiter i05 og de to ekte gullkomponentene i07. Alle native deler er tilordnet én gang i v2-rutekartdiagnostikken. Dette er ikke full import eller spilltest.

QA passerer antall og alfa for alle ni.01 har et presist, kildedokumentert visirunntak i tre små områder;05 har et smalt visirunntak for16 piksler på bakfase7. De øvrige arkene passerer uten restalfa-unntak. Ikke utvid unntakene til generell tåke eller kroppskanter. Visirbevis: fig002_01-visirbevis.png/json og fig002_05-visirbevis.png.

fig002_07/costume002_036: første kilde har kropp[80,48,164,256] og to gullpiksler ved[440,92,4,4]/[436,96,4,4], RGB172/124/0; originalens hele boks er[80,48,364,256]. Native har kropp[51,37,214,323], to separate gullkomponenter[451,87,11,11]/[440,98,10,11] og helboks[51,37,411,323]. Begge ekte gullkomponenter er bevart og knyttet til første rute. De er større enn4x-kildens piksler. Mottak må kontrollere at utliggere ikke drar kroppens skala eller anker. Se source_loose_components i fig002_07.json, fig002_07-kilde-utliggerbevis.png/json og det komplette rutekartet.

Originale enkelt-PNG-er for kostyme002 mangler i Codex-uttrekket. RGB-kildeark og metadata er tilgjengelige; ingen påstand om original-PNG-import, fysisk ankerpass, stabil hodeskalering i runtime eller spilltest. Native figurstørrelser er større enn kildens omtrent256px, særlig08; mottakets fysiske rutetilpasning er nødvendig. Tallene er i batch-summary.json.

Root kontrollerer og leverer. Bruk spesifikasjonen i denne agentmappen, ikke de innledende perjobbfilene i overordnet taskmappe: fig002_XX.json, .qa.json, -visuell.json, -rutekart.json og -rutekart-mottak-v2.json. For hvert valgt forsøk finnes også fig002_XX-forsokN.json og -native-gray.png. Nativepath/SHA følger spesifikasjonen og batch-summary.json. Reelle holdte forsøk og årsaker står i avviste-forsok.json. Alle fire beskyttede kildefiler per jobb er hashverifisert uendret, og hvert generert prompt beholder original prompt.txt som ordrett prefiks.

Ingen kodeendring, Git-mutasjon, felles fremdrift eller levering er utført av denne underagenten. Claude-overleveringen ble tidligere utarbeidet i agent-claude og publisert av root; ingen verifisert kvittering fra aktiv Claude-UI foreligger.
