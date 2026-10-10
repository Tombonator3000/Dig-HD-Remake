# Til Claude: siste grafikkleveranse og neste kontroll

Tom har bedt om flere grafikkagenter og tettere samarbeid på denne Kubuntu-maskinen. Codex lager og samordner grafikken. Claude eier kode, mottak, modbygging og spillkontroll. Tom godkjenner stil og utseende. Ingen mottakskvittering fra en aktiv Claude-chat er registrert ennå.

## Gjeldende leveranser

Dette dokumentet følger Brink/rom-del18. Bruk SHA256 i `../romlag-brink-20261010/brink/leveranser.json` som leveransefasit. 109 av 208 Brink-relaterte ark er revidert; enkelte kostymer inneholder også Boston eller gjenstander, så faktisk kilde bestemmer figur. Ny romdrakt/Pig-ordre har44 av50 ark: Boston21/22, Maggie9/9, Brink10/10 og Pig4/9. Romlag har210 av230 leverte lag. Tellingene er grafikkleveranser, ikke integrasjon eller Toms godkjenning av alle serieark.

De åtte nye figurarkene er fig137_01/02/04/05/06 og fig174_02/03/04. Root har sett kilde og grå native, kontrollert beskyttede originalfiler og bevist at hvert publisert rutekart er identisk med faktisk VERSION2-import mot original-RGBA. `brink-kontroll-del18/` viser 148 native hovedruter og 5 ekte originalfragmenter, totalt 153 importer ok. 174_02/03 viser Boston; 174_04 beholder ekte Boston/Brink-komposittpar. 137_03 er holdt for feil relative mål i en sammensatt originalrute. 048 er grafikklevert i alle 12 ark, med den tidligere dokumenterte lille hoderuten 048_123 til gjennomsyn.

Ny fargekontroll holder073_01a4 for for lyse bukser; forsøka5 retter fargen men gir to hoder til gjennomsyn og er også holdt. Det allerede publiserte073_05 har ujevn og for lys buksepalett i flere ruter og skal avvente fargeretting før visuell ferdigstatus.073 bruker faktisk mørk rust143/47/0 og107/35/7;048 har lysere original187/71/0 og155/55/11. Ikke normaliser disse kostymene til samme oransje. Se `PALETTE-REVIEW-ADDENDUM.md`.

## Kontroller dette først

1. Hent nyeste gpt-arbeid til din egen mottakscheckout. Kodegrunnlaget for diagnosene er main36cd09f, inkludert PR44. `tools/gpt_gren.sh hent` kopierer resultat og notat til work/gpt, men rapportene må leses fra work/.gpt-gren/rapporter/. Rutekartene ligger direkte under rapporter/romlag-brink-20261010/ slik myke-figurer finner dem.
2. Les `hodepuls-v2/TIL-CLAUDE.md` først: root-verifisert faktisk v2 skalerer hele hodet8,33prosent ulikt mellom munnfasene016_059/060/061 selv om nativehøyden er lik og gruppeskalaen felles. Originalene har ingen magenta. Dette er et separat spor til hodepuls, ikke runtimebekreftelse. Nytt levert eksempel fig137_06 har i tillegg 12 prosent forskjell i X-faktor mellom profilhodene 005/004 og munnfasene 003/002/094; se samme mappe.
3. Undersøk hodeanker med blandet teknisk magenta før du erklærer taleskalering og plassering rettet. costume016_264 har ekte9x9-hode og fem magentapiksler nederst i en9x64-boks. Faktisk v2 flytter hodet[-6,207], IoU0.033 og dekning0.066. `bakhode-mottaksfeil.json` og tidligere importbevis dokumenterer dette. Bevar indeks- og ankerinformasjonen, og skill teknisk magenta fra faktisk tegning ved måling og plassering.
4. Bevar ekte deler i blandede ruter. `brink-kontroll-del13/` viser016_483 med to ekte piksler og ni magentapiksler; `brink-kontroll-del15-16/` viser016_148 med én ekte blågrå piksel og tre magentapiksler. Ikke utelat hele ruten. Ren magenta kan ikke tolkes som figurinnhold.188_046 er derimot én ekte opak blågrå piksel uten magenta.
5. Se på det lille hodet costume048_123 i fig048_07: IoU0.784, dekning0.791, flytt[-6,-5]. Det har ingen magenta eller kunstig fotlinje. Avviket er eksplisitt beholdt i rapporten. Kontroller det sammen med den tilhørende hodeløse kroppen og munnfasene i motoren.
6. Kjør import og mål faktisk animasjon: stabil fysisk hode-/kroppsstørrelse, hode- og fotankere, forgrunnsdekning og rektangulære kanter. Lokalt grønt importresultat er ikke en spilltest.

## Originaler og nyordre

793 originale enkelt-PNG-er med indeksbilder for kostyme1/2/3/7 er nå dekodet isolert fra de lokale DIG.LA0/LA1-filene. Den tidligere mangelen på disse PNG-ene gjelder ikke lenger. `nyordre-mottakskontroll/` har proveniens og faktisk kontroll av alle44 leverte ark:440 synlige ruter ok, én Pig-rute til gjennomsyn og157 rene tekniske magentaruter.111 små magentaruter blir uriktig beholdt som fallback og46 større rapporteres manglende. Disse er tekniske oppføringer, ikke157 manglende grafikktegninger.

Maggie002_036 har to ekte fjerne gullpiksler, og Pig007_064 har én ekte opak svart utligger. Begge har kilde-PNG og alfa-/boksbevis i samme mappe. Pig007_163 sitt kart er kildebevist utvidet for å omfatte åtte ekte native randdeler; selve PNG-en er uendret. Pig007_126 har dekning0.794 og står til gjennomsyn. Ingen av disse kontrollene beviser motorplassering.

## Rom og tilbakeholdte kandidater

Bakgrunnsankrene rom032 og rom077 er nå revidert og grafikklevert byteidentisk, med lokal `_evaluate` uten manuelle overstyringer. Rom032 viser igjen tynne vannstriper under venstre bue. Ny rom077 bevarer øyas omriss og spirenes plassering. Se `romanker-kontroll/` og `../romlag-brink-20261010/romanker/leveranser.json`. Dette åpner ikke avhengige lag automatisk: 15 lag venter fortsatt på mottakskontroll av rom032, rom077 og rom088_del7av9. Rom088-forsøk er holdt fordi den svarte kantens form først var feil og neste forsøk flyttet motivet. De fem øvrige holdte lagene ligger i `romlag-kontroll/`; lag027_03_del2av8 har en nesten tom veggblokk med svak korrelasjon som må vurderes før ny bildeforskyvning bestilles.

Boston001_20 og Pig007_02/03/04/06/07 er fortsatt holdt. Native med feil skuldermerker, skjulte ansiktsdeler, lyspar, åpninger eller ringfaser leveres ikke som godkjent. Kandidatstatus er skilt fra leveransene.

## Filansvar og svar

Tre grafikkagenter arbeider i egne oppgavemapper med ulike kostymer. Root er eneste som kopierer leverte PNG-er, oppdaterer felles SHA/fremdrift og bruker grafikkens Git-indeks. Ingen beskyttede referanser eller jobbfiler endres. Native leveres byteidentisk, uten kreativ etterbehandling eller alfarydding. Arbeidsdeling står i `arbeidsdeling.json`.

Claude bruker egen kodecheckout og egen work/.gpt-gren. Ikke kjør en full gpt_runde eller `gpt_gren.sh send` i den aktive grafikkcheckouten; skriptets git add-A kan ta med andres pågående filer. Hent den andre partens push før egen publisering og bevar lokale endringer. Claude skriver ORDRE.md, status.csv, RAPPORT.md og retur.md; root skriver grafikk og leveransenotater. Grafikk går bare til gpt-arbeid.

Svar via repoet i `fra-claude/` med mottatt grafikkcommit, kodecommit, jobb og bilde-SHA, faktisk importresultat, modversjon, utførte spilltester og neste handling. `fra-claude-eksempel.json` er bare et tomt skjema. Dette dokumentet er tilgjengelig på samme maskin og i repoet, men er ikke en påstand om at Claude har lest eller utført det.
