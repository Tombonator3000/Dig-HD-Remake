# Til Claude: siste grafikkleveranse og neste kontroll

Tom har bedt om flere grafikkagenter og tettere samarbeid på denne Kubuntu-maskinen. Codex lager og samordner grafikken. Claude eier kode, mottak, modbygging og spillkontroll. Tom godkjenner stil og utseende. Ingen mottakskvittering fra en aktiv Claude-chat er registrert ennå.

## Gjeldende leveranser

Dette dokumentet følger grafikkcommiten som inneholder Brink-del15 og del16. Bruk SHA256 i `../romlag-brink-20261010/brink/leveranser.json`, ikke et historisk commitnummer som siste status. 96 av208 Brink-ark er revidert. Ny romdrakt/Pig-ordre har44 av50 ark: Boston21/22, Maggie9/9, Brink10/10 og Pig4/9. Romlag har210 av230 leverte lag. Disse tellingene er grafikkleveranser, ikke integrasjon eller Toms godkjenning av alle serieark.

De ti nye arkene er fig073_04/05/06, fig016_28/30, fig048_07/08/09 og fig188_02/03. Root har sett kilde og grå native, kontrollert beskyttede originalfiler og bevist at hvert publisert rutekart er identisk med kartet brukt i faktisk VERSION2-import mot original-RGBA. Bevis og forhåndsvisninger ligger i `brink-kontroll-del15-16/`. 169 native hovedruter gir168 ok og én sjekk; syv ekte originalfragmenter tas fra originalen. Den blandede fragmentruten016_148 inneholder også teknisk magenta og krever særskilt håndtering, selv om importen melder ok.

## Kontroller dette først

1. Hent nyeste gpt-arbeid til din egen mottakscheckout. Kodegrunnlaget for diagnosene er main36cd09f, inkludert PR44. `tools/gpt_gren.sh hent` kopierer resultat og notat til work/gpt, men rapportene må leses fra work/.gpt-gren/rapporter/. Rutekartene ligger direkte under rapporter/romlag-brink-20261010/ slik myke-figurer finner dem.
2. Undersøk hodeanker med blandet teknisk magenta før du erklærer taleskalering og plassering rettet. costume016_264 har ekte9x9-hode og fem magentapiksler nederst i en9x64-boks. Faktisk v2 flytter hodet[-6,207], IoU0.033 og dekning0.066. `bakhode-mottaksfeil.json` og tidligere importbevis dokumenterer dette. Bevar indeks- og ankerinformasjonen, og skill teknisk magenta fra faktisk tegning ved måling og plassering.
3. Bevar ekte deler i blandede ruter. `brink-kontroll-del13/` viser016_483 med to ekte piksler og ni magentapiksler; `brink-kontroll-del15-16/` viser016_148 med én ekte blågrå piksel og tre magentapiksler. Ikke utelat hele ruten. Ren magenta kan ikke tolkes som figurinnhold.188_046 er derimot én ekte opak blågrå piksel uten magenta.
4. Se på det lille hodet costume048_123 i fig048_07: IoU0.784, dekning0.791, flytt[-6,-5]. Det har ingen magenta eller kunstig fotlinje. Avviket er eksplisitt beholdt i rapporten. Kontroller det sammen med den tilhørende hodeløse kroppen og munnfasene i motoren.
5. Kjør import og mål faktisk animasjon: stabil fysisk hode-/kroppsstørrelse, hode- og fotankere, forgrunnsdekning og rektangulære kanter. Lokalt grønt importresultat er ikke en spilltest.

## Originaler og nyordre

793 originale enkelt-PNG-er med indeksbilder for kostyme1/2/3/7 er nå dekodet isolert fra de lokale DIG.LA0/LA1-filene. Den tidligere mangelen på disse PNG-ene gjelder ikke lenger. `nyordre-mottakskontroll/` har proveniens og faktisk kontroll av alle44 leverte ark:440 synlige ruter ok, én Pig-rute til gjennomsyn og157 rene tekniske magentaruter.111 små magentaruter blir uriktig beholdt som fallback og46 større rapporteres manglende. Disse er tekniske oppføringer, ikke157 manglende grafikktegninger.

Maggie002_036 har to ekte fjerne gullpiksler, og Pig007_064 har én ekte opak svart utligger. Begge har kilde-PNG og alfa-/boksbevis i samme mappe. Pig007_163 sitt kart er kildebevist utvidet for å omfatte åtte ekte native randdeler; selve PNG-en er uendret. Pig007_126 har dekning0.794 og står til gjennomsyn. Ingen av disse kontrollene beviser motorplassering.

## Rom og tilbakeholdte kandidater

15 lag venter på tre bakgrunnsankere: rom032 er avvist og blokkerer lag032_01..07; rom077 er sjekk og blokkerer lag077_01..04; rom088_del7av9 er avvist og blokkerer fire lag for samme del. Bevis og de fem øvrige holdte lagene ligger i `romlag-kontroll/`.027_03_del2av3 har særlig en nesten tom veggblokk med svak korrelasjon som må vurderes før en ny bildeforskyvning bestilles.

Boston001_20 og Pig007_02/03/04/06/07 er fortsatt holdt. Native med feil skuldermerker, skjulte ansiktsdeler, lyspar, åpninger eller ringfaser leveres ikke som godkjent. Kandidatstatus er skilt fra leveransene.

## Filansvar og svar

Tre grafikkagenter arbeider i egne oppgavemapper med ulike kostymer. Root er eneste som kopierer leverte PNG-er, oppdaterer felles SHA/fremdrift og bruker grafikkens Git-indeks. Ingen beskyttede referanser eller jobbfiler endres. Native leveres byteidentisk, uten kreativ etterbehandling eller alfarydding. Arbeidsdeling står i `arbeidsdeling.json`.

Claude bruker egen kodecheckout og egen work/.gpt-gren. Ikke kjør en full gpt_runde eller `gpt_gren.sh send` i den aktive grafikkcheckouten; skriptets git add-A kan ta med andres pågående filer. Hent den andre partens push før egen publisering og bevar lokale endringer. Claude skriver ORDRE.md, status.csv, RAPPORT.md og retur.md; root skriver grafikk og leveransenotater. Grafikk går bare til gpt-arbeid.

Svar via repoet i `fra-claude/` med mottatt grafikkcommit, kodecommit, jobb og bilde-SHA, faktisk importresultat, modversjon, utførte spilltester og neste handling. `fra-claude-eksempel.json` er bare et tomt skjema. Dette dokumentet er tilgjengelig på samme maskin og i repoet, men er ikke en påstand om at Claude har lest eller utført det.
