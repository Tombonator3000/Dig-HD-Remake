# Til Claude: siste grafikkleveranse og neste kontroll

Tom har bedt om flere grafikkagenter og tettere samarbeid på denne Kubuntu-maskinen. Codex lager og samordner grafikken. Claude eier kode, mottak, modbygging og spillkontroll. Tom godkjenner stil og utseende. Ingen mottakskvittering fra en aktiv Claude-chat er registrert ennå.

## Gjeldende leveranser

Dette dokumentet følger Brink-del17. Bruk SHA256 i `../romlag-brink-20261010/brink/leveranser.json` som leveransefasit.101 av208 Brink-relaterte ark er revidert; enkelte kostymer inneholder også Boston eller gjenstander, så faktisk kilde bestemmer figur. Ny romdrakt/Pig-ordre har44 av50 ark: Boston21/22, Maggie9/9, Brink10/10 og Pig4/9. Romlag har210 av230 leverte lag. Tellingene er grafikkleveranser, ikke integrasjon eller Toms godkjenning av alle serieark.

De fem nye arkene er fig016_35, fig048_10/11/12 og fig174_01. Root har sett kilde og grå native, kontrollert beskyttede originalfiler og bevist at hvert publisert rutekart er identisk med faktisk VERSION2-import mot original-RGBA. `brink-kontroll-del17/` viser68native hovedruter+5ekte originalfragmenter,73importer ok.174_01 viser Boston og bruker Toms godkjente plain Boston-ansikt.048 er nå grafikklevert i alle12ark, med den tidligere dokumenterte lille hoderuten048_123 til gjennomsyn.

Ny fargekontroll holder073_01a4 for for lyse bukser; forsøka5 retter fargen men gir to hoder til gjennomsyn og er også holdt. Det allerede publiserte073_05 har ujevn og for lys buksepalett i flere ruter og skal avvente fargeretting før visuell ferdigstatus.073 bruker faktisk mørk rust143/47/0 og107/35/7;048 har lysere original187/71/0 og155/55/11. Ikke normaliser disse kostymene til samme oransje. Se `PALETTE-REVIEW-ADDENDUM.md`.

## Kontroller dette først

1. Hent nyeste gpt-arbeid til din egen mottakscheckout. Kodegrunnlaget for diagnosene er main36cd09f, inkludert PR44. `tools/gpt_gren.sh hent` kopierer resultat og notat til work/gpt, men rapportene må leses fra work/.gpt-gren/rapporter/. Rutekartene ligger direkte under rapporter/romlag-brink-20261010/ slik myke-figurer finner dem.
2. Les `hodepuls-v2/TIL-CLAUDE.md` først: root-verifisert faktisk v2 skalerer hele hodet8,33prosent ulikt mellom munnfasene016_059/060/061 selv om nativehøyden er lik og gruppeskalaen felles. Originalene har ingen magenta. Dette er et separat spor til hodepuls, ikke runtimebekreftelse.
3. Undersøk hodeanker med blandet teknisk magenta før du erklærer taleskalering og plassering rettet. costume016_264 har ekte9x9-hode og fem magentapiksler nederst i en9x64-boks. Faktisk v2 flytter hodet[-6,207], IoU0.033 og dekning0.066. `bakhode-mottaksfeil.json` og tidligere importbevis dokumenterer dette. Bevar indeks- og ankerinformasjonen, og skill teknisk magenta fra faktisk tegning ved måling og plassering.
4. Bevar ekte deler i blandede ruter. `brink-kontroll-del13/` viser016_483 med to ekte piksler og ni magentapiksler; `brink-kontroll-del15-16/` viser016_148 med én ekte blågrå piksel og tre magentapiksler. Ikke utelat hele ruten. Ren magenta kan ikke tolkes som figurinnhold.188_046 er derimot én ekte opak blågrå piksel uten magenta.
5. Se på det lille hodet costume048_123 i fig048_07: IoU0.784, dekning0.791, flytt[-6,-5]. Det har ingen magenta eller kunstig fotlinje. Avviket er eksplisitt beholdt i rapporten. Kontroller det sammen med den tilhørende hodeløse kroppen og munnfasene i motoren.
6. Kjør import og mål faktisk animasjon: stabil fysisk hode-/kroppsstørrelse, hode- og fotankere, forgrunnsdekning og rektangulære kanter. Lokalt grønt importresultat er ikke en spilltest.

## Originaler og nyordre

793 originale enkelt-PNG-er med indeksbilder for kostyme1/2/3/7 er nå dekodet isolert fra de lokale DIG.LA0/LA1-filene. Den tidligere mangelen på disse PNG-ene gjelder ikke lenger. `nyordre-mottakskontroll/` har proveniens og faktisk kontroll av alle44 leverte ark:440 synlige ruter ok, én Pig-rute til gjennomsyn og157 rene tekniske magentaruter.111 små magentaruter blir uriktig beholdt som fallback og46 større rapporteres manglende. Disse er tekniske oppføringer, ikke157 manglende grafikktegninger.

Maggie002_036 har to ekte fjerne gullpiksler, og Pig007_064 har én ekte opak svart utligger. Begge har kilde-PNG og alfa-/boksbevis i samme mappe. Pig007_163 sitt kart er kildebevist utvidet for å omfatte åtte ekte native randdeler; selve PNG-en er uendret. Pig007_126 har dekning0.794 og står til gjennomsyn. Ingen av disse kontrollene beviser motorplassering.

## Rom og tilbakeholdte kandidater

15 lag venter på tre bakgrunnsankere (root har et rettet vannforsøk for rom032 til separat kontroll, ennå ikke levert): rom032 er avvist og blokkerer lag032_01..07; rom077 er sjekk og blokkerer lag077_01..04; rom088_del7av9 er avvist og blokkerer fire lag for samme del. Bevis og de fem øvrige holdte lagene ligger i `romlag-kontroll/`.lag027_03_del2av8 har særlig en nesten tom veggblokk med svak korrelasjon som må vurderes før en ny bildeforskyvning bestilles.

Boston001_20 og Pig007_02/03/04/06/07 er fortsatt holdt. Native med feil skuldermerker, skjulte ansiktsdeler, lyspar, åpninger eller ringfaser leveres ikke som godkjent. Kandidatstatus er skilt fra leveransene.

## Filansvar og svar

Tre grafikkagenter arbeider i egne oppgavemapper med ulike kostymer. Root er eneste som kopierer leverte PNG-er, oppdaterer felles SHA/fremdrift og bruker grafikkens Git-indeks. Ingen beskyttede referanser eller jobbfiler endres. Native leveres byteidentisk, uten kreativ etterbehandling eller alfarydding. Arbeidsdeling står i `arbeidsdeling.json`.

Claude bruker egen kodecheckout og egen work/.gpt-gren. Ikke kjør en full gpt_runde eller `gpt_gren.sh send` i den aktive grafikkcheckouten; skriptets git add-A kan ta med andres pågående filer. Hent den andre partens push før egen publisering og bevar lokale endringer. Claude skriver ORDRE.md, status.csv, RAPPORT.md og retur.md; root skriver grafikk og leveransenotater. Grafikk går bare til gpt-arbeid.

Svar via repoet i `fra-claude/` med mottatt grafikkcommit, kodecommit, jobb og bilde-SHA, faktisk importresultat, modversjon, utførte spilltester og neste handling. `fra-claude-eksempel.json` er bare et tomt skjema. Dette dokumentet er tilgjengelig på samme maskin og i repoet, men er ikke en påstand om at Claude har lest eller utført det.
