# Til Claude: siste grafikkleveranse og neste kontroll

Tom har bedt om flere grafikkagenter og tettere samarbeid på denne Kubuntu-maskinen. Codex lager og samordner grafikken. Claude eier kode, mottak, modbygging og spillkontroll. Tom godkjenner stil og utseende. Ingen mottakskvittering fra en aktiv Claude-chat er registrert ennå.

Les `START-HER.md` og `mottaksko.json` for raskt lokalt mottak. `mottak-diagnose/KJOR-LOKALT.md` har en faktisk kjørt diagnosekommando som kan gjentas mot Claudes egen kode uten å endre native eller modfiler.

## Gjeldende leveranser

Dette dokumentet følger Brink-del24. Bruk SHA256 i `../romlag-brink-20261010/brink/leveranser.json` som leveransefasit. 141 av 208 Brink-relaterte ark er revidert; enkelte kostymer inneholder også Boston eller gjenstander, så faktisk kilde bestemmer figur. Ny romdrakt/Pig-ordre har44 av50 ark: Boston21/22, Maggie9/9, Brink10/10 og Pig4/9. Romlag har210 av230 leverte lag. Tellingene er grafikkleveranser, ikke integrasjon eller Toms godkjenning av alle serieark.

Del24 inneholder 3 jobber: fig138_01, fig173_05, fig229_18. 3 øker revisjonsdekningen. Root har sett kildene og native på grå bakgrunn, kontrollert original-RGBA og beskyttede filer, og sammenlignet publisert rutekart med faktisk VERSION2-import. `brink-kontroll-del24/` har 37 native tegninger, 1 ekte originalfragmenter og 0 rene tekniske markører. Alle 38 importoppføringer rapporteres ok. Dette er isolert importkontroll; motorplassering og animasjon må fortsatt kontrolleres av Claude. Tidligere leveranser og konkrete importavvik ligger fortsatt i de navngitte kontrollmappene nedenfor. Samme commit dokumenterer kildekontroll av fig138_02, fig229_08. Disse 2 jobbene er HOLD, uten nye leverte PNG-er, og øker ikke dekningstallene.

Fig073_05 er nå rettet til mørk rust gjennom native forsøk4 uten å endre armstillinger; alle13importer ok. Fig073_01 er levert som forsøk6 med mørke bukser og to mindre, like høye separate hoder. Faktisk hode-IoU er0.780/0.783 og dekning0.977/0.986; dette krever fortsatt animasjonskontroll. Tidligere073_01-forsøk med for lyse bukser eller for store hoder er beholdt lokalt som holdte kandidater.073 bruker faktisk mørk rust143/47/0 og107/35/7;048 har lysere original187/71/0 og155/55/11. Ikke normaliser kostymene til samme oransje.

## Kontroller dette først

1. Hent nyeste gpt-arbeid til din egen mottakscheckout. Kodegrunnlaget for diagnosene er main36cd09f, inkludert PR44. `tools/gpt_gren.sh hent` kopierer resultat og notat til work/gpt, men rapportene må leses fra work/.gpt-gren/rapporter/. Rutekartene ligger direkte under rapporter/romlag-brink-20261010/ slik myke-figurer finner dem.
2. Les `hodepuls-v2/TIL-CLAUDE.md` først: root-verifisert faktisk v2 skalerer hele hodet8,33prosent ulikt mellom munnfasene016_059/060/061 selv om nativehøyden er lik og gruppeskalaen felles. Originalene har ingen magenta. Dette er et separat spor til hodepuls, ikke runtimebekreftelse. Nytt levert eksempel fig137_06 har i tillegg 12 prosent forskjell i X-faktor mellom profilhodene 005/004 og munnfasene 003/002/094; se samme mappe.
3. Undersøk hodeanker med blandet teknisk magenta før du erklærer taleskalering og plassering rettet. costume016_264 har ekte9x9-hode og fem magentapiksler nederst i en9x64-boks. Faktisk v2 flytter hodet[-6,207], IoU0.033 og dekning0.066. `bakhode-mottaksfeil.json` og tidligere importbevis dokumenterer dette. Bevar indeks- og ankerinformasjonen, og skill teknisk magenta fra faktisk tegning ved måling og plassering.
4. Bevar ekte deler i blandede ruter. `brink-kontroll-del13/` viser016_483 med to ekte piksler og ni magentapiksler; `brink-kontroll-del15-16/` viser016_148 med én ekte blågrå piksel og tre magentapiksler. Ikke utelat hele ruten. Ren magenta kan ikke tolkes som figurinnhold. Nytt konkret eksempel i `brink-kontroll-del19/magenta-root-verifisert.json`: costume230_002 er fire opake [255,63,255]-markørpiksler. Native har null sterk magenta. VERSION2 lager likevel276synlige magentapiksler,64med alfa minst128, og status ok fra originalfallback. Ikke kall dette manglende grafikk.188_046 er derimot én ekte opak blågrå piksel uten magenta.
5. Se på det lille hodet costume048_123 i fig048_07: IoU0.784, dekning0.791, flytt[-6,-5]. Det har ingen magenta eller kunstig fotlinje. Avviket er eksplisitt beholdt i rapporten. Kontroller det sammen med den tilhørende hodeløse kroppen og munnfasene i motoren.
6. Nytt kontrolltilfelle fig229_19 er HOLD: original-Brink er264px høy i allefirefaser, native343/342/342/342px, men faktisk VERSION2-eksport gir269/252/271/294px ved alfa minst128. Dette gir16,7prosent spenn mellom107 og109 selv om alle oppføringer står ok. Root har kontrollert source/native/import-SHA, høyder og allefire kontaktpaneler. Kilde109-effekten er også for kort relativt til personene, så grafikken er holdt; malte hoder skal ikke krympes for å kompensere for fit. Se `brink-kontroll-hold/fig229_19-root-verifisert-HOLD.json`. Dette er måling av faktisk import, ikke en motorvideo.
7. Kjør import og mål faktisk animasjon: stabil fysisk hode-/kroppsstørrelse, hode- og fotankere, forgrunnsdekning og rektangulære kanter. Lokalt grønt importresultat er ikke en spilltest.

## Originaler og nyordre

793 originale enkelt-PNG-er med indeksbilder for kostyme1/2/3/7 er nå dekodet isolert fra de lokale DIG.LA0/LA1-filene. Den tidligere mangelen på disse PNG-ene gjelder ikke lenger. `nyordre-mottakskontroll/` har proveniens og faktisk kontroll av alle44 leverte ark:440 synlige ruter ok, én Pig-rute til gjennomsyn og157 rene tekniske magentaruter.111 små magentaruter blir uriktig beholdt som fallback og46 større rapporteres manglende. Disse er tekniske oppføringer, ikke157 manglende grafikktegninger.

Maggie002_036 har to ekte fjerne gullpiksler, og Pig007_064 har én ekte opak svart utligger. Begge har kilde-PNG og alfa-/boksbevis i samme mappe. Pig007_163 sitt kart er kildebevist utvidet for å omfatte åtte ekte native randdeler; selve PNG-en er uendret. Pig007_126 har dekning0.794 og står til gjennomsyn. Ingen av disse kontrollene beviser motorplassering.

## Rom og tilbakeholdte kandidater

Bakgrunnsankrene rom032 og rom077 er nå revidert og grafikklevert byteidentisk, med lokal `_evaluate` uten manuelle overstyringer. Rom032 viser igjen tynne vannstriper under venstre bue. Ny rom077 bevarer øyas omriss og spirenes plassering. Se `romanker-kontroll/` og `../romlag-brink-20261010/romanker/leveranser.json`. Dette åpner ikke avhengige lag automatisk: 15 lag venter fortsatt på mottakskontroll av rom032, rom077 og rom088_del7av9. Rom088-forsøk er holdt fordi den svarte kantens form først var feil og neste forsøk flyttet motivet. De fem øvrige holdte lagene ligger i `romlag-kontroll/`; lag027_03_del2av8 har en nesten tom veggblokk med svak korrelasjon som må vurderes før ny bildeforskyvning bestilles.

Boston001_20 og Pig007_02/03/04/06/07 er fortsatt holdt. Native med feil skuldermerker, skjulte ansiktsdeler, lyspar, åpninger eller ringfaser leveres ikke som godkjent. Kandidatstatus er skilt fra leveransene.

## Nye kildekontroller under neste levering

Fig229_08 har en nyoppdaget detaljfeil i den allerede leverte native: originalens lille rosebrune lårfelt er blitt en brun/oransje lommeklaff. Resultatfilen er bevart byteidentisk, og erstatningforsøk2 er holdt fordi detaljen fortsatt er feil og restalfa øker. Ikke bruk arket som stilanker for buksedetaljen. Se `brink-kontroll-hold/fig229_08-publisert-detaljfeil-og-erstatning-HOLD.json`.

Lag025-forsøk9/10 og lag026-forsøk7 er stabil HOLD med konkret kildebevis. Lag025s grønne tegn kommer fra rombakgrunnen; objektmaskene218/219 inneholder bare blå stolpepiksler, så grønn objekt-QA beviser ikke tegnenes form. Lag026 må endre nøyaktig42 opake blå originalpiksler i tre statustilstander, ikke lage nye neonpinner. Originalt synlig rom gjennom gjennomsiktige objektmasker skal bevares. Se de nye STABIL-HOLD- og TIL-CLAUDE-filene i `romlag-kontroll/`.

## Filansvar og svar

Tre grafikkagenter arbeider i egne oppgavemapper med ulike kostymer. Root er eneste som kopierer leverte PNG-er, oppdaterer felles SHA/fremdrift og bruker grafikkens Git-indeks. Ingen beskyttede referanser eller jobbfiler endres. Native leveres byteidentisk, uten kreativ etterbehandling eller alfarydding. Arbeidsdeling står i `arbeidsdeling.json`.

Claude bruker egen kodecheckout og egen work/.gpt-gren. Ikke kjør en full gpt_runde eller `gpt_gren.sh send` i den aktive grafikkcheckouten; skriptets git add-A kan ta med andres pågående filer. Hent den andre partens push før egen publisering og bevar lokale endringer. Claude skriver ORDRE.md, status.csv, RAPPORT.md og retur.md; root skriver grafikk og leveransenotater. Grafikk går bare til gpt-arbeid.

Svar via repoet i `fra-claude/` med mottatt grafikkcommit, kodecommit, jobb og bilde-SHA, faktisk importresultat, modversjon, utførte spilltester og neste handling. `fra-claude-eksempel.json` er bare et tomt skjema. Dette dokumentet er tilgjengelig på samme maskin og i repoet, men er ikke en påstand om at Claude har lest eller utført det.
