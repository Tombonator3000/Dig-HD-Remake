# Logg

Alt som gjøres i prosjektet, med tidspunkt (norsk tid). Nyeste nederst.

## 2026-10-05 21:22
- Repo opprettet av Tom. Tre konseptbilder lastet opp (Maggie Robbins, Boston Low, Ludger Brink).

## 2026-10-06 19:40 til 20:15 (Claude)
- Sjekket etter AGENTS.md. Finnes ikke i repoet.
- Gikk gjennom Drive-mappen med spillfilene (DIG.LA0, DIG.LA1, DIGMUSIC.BUN, DIGVOICE.BUN, VIDEO/ med 55 SAN, 4 NUT og 2 TRS). Ingen exe, ingen `_other/`.
- Leste DIG.LA0: motorversjon 7.3.4 (9. okt 1995), data 7. nov 1995, 111 navngitte rom, 306 skriptplasser (303 i bruk), 332 kostymeplasser, 984 globale objekter. Engelsk utgave (ingen LANGUAGE.BND).
- Fant at DIG.LA1 (88 673 344 byte) har samme størrelse som filen thedig-textures er verifisert mot.
- Gikk gjennom thedig-textures (README, AGENTS.md, docs/la1-census.txt) og ScummVM sin SCUMM-kode (master, commit c909132) for å finne stedene en HD-fork må koble seg inn.
- La til:
  - `docs/ANALYSE.md`: full analyse av filer, omfang, metoder og første steg.
  - `docs/rom-oversikt.csv`: alle 111 rom med mål, z-plan, paletter og antall objektbilder, med tomme kolonner for prioritet og status.
  - `tools/la0_info.py`: leser DIG.LA0 og skriver ut versjon, grenser, MD5 og romliste.
  - `.gitignore`: holder spillfiler og uttrukket grafikk ute av git.
  - `log.md`, `memory.md`, `todo.md`.
- Ikke gjort: MD5 av DIG.LA0 er ikke kontrollert (fikk ikke byte-eksakt kopi via Drive-koblingen). DIG.LA1 og SAN-filene er ikke lastet ned eller kjørt gjennom uttrekk ennå.

## 2026-10-06 21:51 til 22:55 (Claude)
- Tom delte Drive-mappen via lenke en kort stund. Lastet ned DIG.LA0, DIG.LA1 og alle 61 filene i VIDEO/. Størrelsene stemmer.
- DIG.LA0 MD5 `d8323015ecb8b10bf53474f6e6b0ae33` (standardoppføringen i ScummVM). DIG.LA1 SHA-256 `8f2a0474...a957`, nøyaktig samme fil som thedig-textures er verifisert mot.
- La spillfilene i en egen gren `spilldata` (uten felles historikk med main), i tre commits for å holde hver push under grensen. Sjekksummer i `game/SHA256SUMS`. BUN-filene (musikk og tale) er over 100 MB og ligger bare på Drive.
- `tools/hent_spilldata.sh`: henter grenen inn i `game/` og sjekker sjekksummene.
- Pipeline `pipeline/` (pakke `dighd`):
  - `gamedata.py`: leser LA0 og LA1 (romnavn, størrelser, paletter, fargesykling, objektposisjoner, kostyme-ID fra DCOS).
  - `export.py`: rom og objekter som RGB og 8-bit indeksert, kostymeruter med de ekte fargene fra RGBS-blokken.
  - `upscale.py`: nearest, lanczos, lanczos-sharp, Real-ESRGAN og valgfri kommando.
  - `modpack.py`: bygger mod-mapper. Objekter skaleres i sammenheng med bakgrunnen. Egne HD-bilder kan brukes i stedet.
  - CLI: `dighd info|extract|build-mod|compare|san`. Tester i `pipeline/tests`.
- Eksportert: 111 rom, 642 objektbilder, 28 490 kostymeruter, 12 638 filmrammer.
- Funnet underveis: thedig-textures lagrer kostymeruter med svart palett og nummererer kostymer i filrekkefølge. Løst i egen eksport (RGBS-farger, DCOS-ID).
- ScummVM-patch `engine/patches/0001-dighd-hd-grafikk.patch` (ScummVM `c909132`): ny `engines/scumm/dighd.cpp` og små hooks i 14 filer. HD-bakgrunner, HD-objekter, HD-sprites, HD-filmrammer, fargejustering ved palettbytte, fargesykling beholdt, mus og peker i HD, test- og dumpvalg.
- `engine/build.sh`, `engine/run.sh`, `engine/test.sh`. Byggeskriptet er testet fra en ren checkout.
- Testet uten skjerm med en nearest-mod: 0 avvikende piksler for bakgrunner, objekter (rom 34 og 105) og uskalerte figurer. Skalerte figurer under 0,25 prosent (ventet). Filmrammer: rammenummeret er `_frame - 1`, etter rettingen er 198 av 198 rammer like.
- La til `README.md`, `AGENTS.md`, `docs/HD-MOTOR.md`. Oppdaterte `.gitignore` (work/, mods/, engine/scummvm/).

## 2026-10-06 23:16 til 23:35 (Claude)
- Tom ba om en bestilling til ChatGPT om trofast HD-grafikk, med Claude på koden og ChatGPT på grafikken, og om å se hvordan Jones og Moonstone gjorde det.
- Gikk gjennom Jonesinthefastlane (docs/HD_GRAPHICS.md, native/public/hd/prompts.md, README og provenance) og MOONSTONE (docs/hd-grafikk.md, log.md, todo.md). Jones brukte ChatGPT sitt innebygde bildeverktøy via Codex, med presise prompter, sporing og korrigeringsrunder. Moonstone har HD-infrastruktur (navngiving, grafikkliste, bryter, gult felt, plasseringssjekk), men ingen ferdig grafikk.
- Sjekket dagens bildeverktøy: sideforhold opptil 3:1, mål delelige med 16, standard 1536 x 1024, kvaliteten synker over 2560 x 1440, og geometri bevares ikke garantert.
- Nytt i pipelinen (`pipeline/dighd/gpt.py`, kommandoene `dighd gpt-pakke` og `dighd gpt-inn`):
  - Jobber på 1536 x 1024 som tilsvarer 384 x 256 originalpiksler i 4x. Vanlige rom får grå kant, brede og høye rom deles med 64 pikslers overlapp. 162 jobber for 106 rom (5 nesten tomme rom hoppet over).
  - Prompt på engelsk med bevar- og ikke-lister, romnotater fra `docs/gpt-romnotater.csv` (17 rom med symboler, krystaller, kart og liknende), delnotat og stilanker.
  - Mottak: sideforhold, forskyvning (fasekorrelasjon), forskyvning i blokker (zoom og flytting), kantlikhet, fargeavvik. Status godkjent, sjekk eller avvist, med `retur.md` og forslag til ny prompt. Fargelås mot originalen, sammensying av deler, `provenance.json`, `RAPPORT.md`, forhåndsvisninger. Innboks for manuelle leveranser.
  - Testet med kunstige svar: riktig plassert godkjennes, 3 piksler forskyvning og 3 prosent zoom avvises, 1 prosent zoom gir sjekk, feil sideforhold avvises, mindre bilde i 3:2 godkjennes, fargestikk på +30 rødt fjernes av fargelåsen, sammensydde deler er identiske med helt bilde.
- `docs/BESTILLING-CHATGPT.md`: bestillingen (roller, hva trofast betyr, jobbformat, rekkefølge med pilot og stilankere, arbeidsflyt for Codex og vanlig chat, kontroll, sporing, erfaringer fra Jones og Moonstone, tekst til ChatGPT-prosjektet).
- `docs/gpt-arbeid-AGENTS.md` og `tools/gpt_gren.sh` (send og hent). Laget den private grenen `gpt-arbeid` med alle jobbene, bestillingen og en egen AGENTS.md for ChatGPT. Rundturen hent og gpt-inn er testet og ryddet etterpå.
- Oppdatert AGENTS.md (roller, ChatGPT-kommandoer), README, memory og todo. Nye tester i pipeline (6 bestått).

## 2026-10-06 23:17 til 23:31 (Codex)
- Leste Claude-delingen og kontrollerte privat repo og åpen PR 1. Tok utgangspunkt i claude/analyse-hd, commit 70aed0523ff624cb6176d9b5911cdc1fdef0f336. Arbeidet ligger i egen kodegren codex/grafikkpilot-20261006.
- Hentet spilldata fra den eksisterende spilldatagrenen. Alle sjekksummer bestod. Eksporterte fem rom (19 rom- og objektbilder uten feil) og kostyme 14 (840 ruter med RGBS-farger).
- Laget bakgrunnskandidater for rom 9 og 22 med den innebygde ChatGPT-bildegeneratoren. Rom 9 fikk en ekstra generering for å korrigere et forskjøvet gulvhjørne. Generatorbildene på 1586x992 ble tilpasset teknisk til 1280x800 RGB uten beskjæring. Lagret fullstendige prompter og originalgeneratorbilder.
- Laget én Boston Low-stilreferanse fra kostyme 14 rute 1 og den eksisterende Boston-referansen. RGBA med ekte alfa, 713x2205. Den avviker fra originalsilhuetten og ble avvist som direkte spritesrute. Den ligger bare i concepts/.
- Bygde ScummVM fra den låste committen og uendret patch. libpng-utviklingsfiler ble pakket ut lokalt i work/build-deps/ fra Ubuntu-pakker. Ingen systempakker eller andre prosjekter ble endret.
- Kjørte 4 pipeline-tester, alle bestod, inkludert telling mot originale spilldata. Native SDL2/Wayland/OpenGL-kjøringer av rom 9 og 22 lastet de nye bakgrunnene i 1280x800 med 4 byte per piksel og avsluttet med exit 0. Inspiserte uredigerte motorbilder. Native nearest-kontroll ga 0 sterke pikselavvik etter motorens terskel.
- Første dummy-kjøringer ved bilde 60 endte i rom 2 fordi oppstartsskriptet overstyrte testhoppet. De er ikke regnet som godkjent romkontroll. Native hopp ved bilde 240 traff de bestilte rommene.
- Leveranse i separat privat grafikkdatagren grafikkdata/pilot-20261006, commit cf8e6a9f6e30d662f7c73076ef1e1810851ceceb. 23,9 MiB med to kandidater, testmod, kilde- og indeksbilder, Boston-konsept, prompter, hasher og kjøringslogger. Grafikkgrenen har ingen felles historikk med main. Ingen bildedata i kode-PR-en.
- La til tools/check_hd_art.py og tools/hent_grafikkpilot.sh, samt docs/GRAFIKKPILOT.md. Kontrollerte mål, format, indeks og alfasilhuett. Generatorstørrelse og Boston-silhuett avvises. Henting testet fra en fersk Git-arbeidsmappe; sjekksummer bestod; gjenbruk og avvisning av endrede lokale filer ble kontrollert uten overskriving.
- Oppdaterte README, romoversikten, prosjektminne og todo. Stil er foreløpig. Manuell masketest, obj171-tilstander, spritesanimasjon, hele brukerreisen og lyd gjenstår.

## 2026-10-06 23:32 (Codex, overlevering)
- Grafikkdata og kodegren er pushet til det private repoet. PR 2 er opprettet som utkast mot claude/analyse-hd: https://github.com/Tombonator3000/Dig-HD-Remake/pull/2
- La overlevering med filplassering, kjøringsstatus og resterende grafikkontroller i Claudes PR 1: https://github.com/Tombonator3000/Dig-HD-Remake/pull/1#issuecomment-6025842984
- Henting fra en fersk Git-arbeidsmappe bestod. Endrede lokale filer ble avvist og bevart. Ingen PR er flettet.

## 2026-10-06 23:36 til 23:45 (Claude)
- Tom ba om at ChatGPT lager grafikk fortløpende, at Claude sjekker repoet jevnlig, fortsetter konverteringen og gir ordre hele tiden.
- Leste overleveringen fra Codex i PR 1 og PR 2. Flettet PR 2 (grafikkpiloten) inn i `claude/analyse-hd` (commit c7e3338).
- Rettet funnet fra Codex sin gjennomgang i `tools/la0_info.py`: blokkstørrelse 0 ga evig løkke. Blokker under 8 byte eller forbi filslutt merkes nå som skadet, og lesingen stopper (commit 287d309).
- Kontrollerte pilotbildene for rom 9 og 22 med `dighd gpt-inn`: forskyvning 0,73 og 0,25 px, begge godkjent. Så på bildene: trofaste, samme motiv og farger med mer detalj. Godkjent som stilankere på vegne av Tom, lagt i `stil/` i `gpt-arbeid`.
- Nytt i pipelinen: `detect_layout` (godtar hele lerretet eller bare bildet i utsnittets sideforhold, slik piloten ble levert) og `write_orders` med kommandoen `dighd gpt-ordre`, som skriver `ORDRE.md` med status, de neste 10 jobbene (avviste først), stilankere, leveringsformat og beskjeder.
- Nye verktøy: `tools/gpt_runde.sh` (hele runden: hent, kontroll, bygg mod når noe nytt er godkjent, publiser, ny ordre, send) og `tools/mod_gren.sh` (modden til og fra den private grenen `hd-mod`, én commit med SHA256SUMS som erstattes hver gang). `tools/gpt_gren.sh` sender nå også `ORDRE.md`, gjenoppretter jobbene hvis `work/gpt/jobber` mangler, og tar bare med forhåndsvisninger for jobber med `retur.md`.
- Rettet i `gpt_runde.sh`: `cat | sha256sum` med pipefail stoppet skriptet uten melding når filen manglet.
- Første runde kjørt 23:43: 2 godkjent, 160 nye. Modden med rom 9 og 22 publisert i `hd-mod` (3,2 MB). `ORDRE.md` sendt til `gpt-arbeid` med rom 2 (tre deler), rom 3 til 8 og første del av rom 10.
- Oppdatert `docs/gpt-arbeid-AGENTS.md` og `docs/BESTILLING-CHATGPT.md`: les `ORDRE.md` først, ingen egne grener eller PR-er, begge leveringsformater godtas.

## 2026-10-06 23:45 til 23:52 (Claude)
- Tom ba om å rydde repoet med README, status og todo slik som i de andre prosjektene (Moonstone og Jones).
- Skrev README på nytt: kort om prosjektet, statustabell, spille med HD, lage HD selv, samarbeidet med ChatGPT, test, grener, mapper, dokumentasjon og opphavsrett.
- Ny `STATUS.md`: HD-dekning (2 av 106 rom, 0 av 642 objekter, 0 av 28 490 ruter, 0 av 12 638 filmrammer), hva som virker og hvordan det er testet, kjente begrensninger og grener.
- Skrev `AGENTS.md` på nytt etter mønster fra Moonstone: Før du starter, Mens du jobber, Stil, Regler, Roller, Oppsett, Kommandoer, ChatGPT-runder, Arbeid med motoren og Grener.
- `todo.md` med `## Neste` øverst og ferdige punkter nederst. `memory.md` oppdatert med ordreflyten, `hd-mod`, piloten og ny plassering av konseptbildene.
- Flyttet de tre konseptbildene fra roten til `docs/konsept/` med lesbare navn (ludger-brink.jpeg, maggie-robbins.webp, boston-low.webp). Rettet henvisningene.
- La til NumPy i avhengighetene til pipelinen (brukes av `gpt.py`, manglet i `pyproject.toml`). Ny test for leveringsformat og ordre. 7 tester bestått.
- Ny CI (`.github/workflows/test.yml`): installerer pipelinen, kjører `pytest -m "not game"` og stopper hvis spillfiler eller `work/` og `mods/` er sjekket inn.
- Pushet to commits til `claude/analyse-hd` (9076632 og 8440b5c). CI grønn. PR 2 står som flettet. Oppdatert tittel og beskrivelse på PR 1. Fletting av PR 1 inn i `main` ble stoppet av tillatelsene her, så den er lagt til Tom i `todo.md`.
- Neste ChatGPT-runde er satt opp til kl. 00:21.

## 2026-10-06 23:53 til 2026-10-07 00:45 (Claude)
- Tom ga full autonomi: flette og hente der det trengs, gi ordre til ChatGPT om bilder og kodehjelp, og bruke flere agenter.
- Flettet PR 1 inn i `main` (5c6a5c7). `main` er nå hovedgrenen lokalt og på GitHub.
- ChatGPT leverte rom 22 på nytt, rom 2 del 1 og rom 28 (laget fra en eldre utgave av `gpt-arbeid`, uten stilankere). Alle tre godkjent av kontrollen. Så på bildene:
  - Rom 2 del 1: trofast, men flere stjerner enn originalen.
  - Rom 28: tavla med symbolene følger originalen tett. Noen små symboler er tolket litt fritt.
  - Rom 22: bakken ved den oransje veggen er blitt blank som vann og fargeavviket er 15 mot 8,5 i piloten. Satte `resultat.png` tilbake til piloten og la den nye som `alternativ_forsok2.png` med forklaring i `notat.md`.
- Kjørte motoren uten skjerm i rom 22 og 28 med modden. Fant at objekt 241 (tavla, 320 x 200) dekker nesten hele rom 28, så HD-bakgrunnen synes bare i 185 piksler. 32 objektbilder er så store at de fungerer som bakgrunner.
- Satte to agenter på jobb samtidig i hver sin arbeidskopi:
  - PR 3 (objektjobber): de store objektbildene blir ChatGPT-jobber `objNNN_SS`, med objektet lagt over rommet på samme lerret som romjobbene. `status.csv` har kolonnen `type`. `gpt-inn` skriver godkjente objekter til `work/gpt-ferdig/objects/` i 4x med alfa fra originalen. RAPPORT og ORDRE teller rom og objekter hver for seg. `build-mod` tar med egne objektbilder også for rom uten HD-bakgrunn. Kontrollert mot ekte data: romjobbene har samme SHA-256 som før, og `gpt-inn` gir byte for byte samme HD-rom.
  - PR 4 (motor): Ctrl+H bytter mellom HD og klassisk grafikk, Ctrl+Shift+H farger gult der HD mangler. `DIGHD_CLASSIC=1`, `DIGHD_SHOW_MISSING=1` og testvariabelen `DIGHD_TEST_KEYS`. `engine/test.sh` gir fortsatt 0 avvik. Klassisk dump er lik originalen i rom 22 og 28. Farten er den samme som før. Patchen gjelder rent på ScummVM c9091321. Ikke prøvd med ekte tastatur.
- Gikk gjennom begge PR-ene og flettet dem (2089ed4 og 41fbeea) etter grønn CI. Ryddet bort agentenes arbeidskopier og grener.
- Så gjennom alle 32 store objektbilder. Rettet etter funnene:
  - Tok ut de to ensfargede rutenettene i inventaret (obj618 og obj627, rom 93). Det gir 30 objektjobber.
  - Objekter kan få eget notat (`objNNN` i `docs/gpt-romnotater.csv`). Notater for obj241 (tavla uten hender), obj547 (håndholdt maskin med tom skjerm) og obj097 (kartmerker).
  - Objekter med flere tilstander (obj884 og obj886): senere tilstander ber om første tilstand som bilde to, og `gpt-inn` tar alt som er likt fra den godkjente første tilstanden (`match_state`), så hånden ikke skifter utseende når spillet bytter bilde.
- Kodeoppgaver til Codex: ny fil `docs/gpt-kodeoppgaver.md` som kommer med i ORDRE.md (`dighd gpt-ordre --oppgaver`). Første oppgave er test på laptopen med skjerm og tastatur, med rapport i `rapporter/` i `gpt-arbeid`.
- Kjørte `dighd gpt-pakke` (192 jobber: 162 rom, 30 objekter) og en runde. Ny ORDRE.md sendt: obj241_01 først, så rom 2 del 2 og 3, rom 3 til 8 og rom 10 del 1. Modden med rom 9, 22 og 28 ligger i `hd-mod`.
- 10 tester bestått. Oppdatert README, STATUS.md, AGENTS.md, todo.md og memory.md.

## 2026-10-07 00:45 (Claude)
- Planlagt runde (satt til 00:21, kom inn 00:43). Ingen nye leveranser i `gpt-arbeid` siden 00:41.
- `tools/gpt_runde.sh` lar nå ORDRE.md stå når ingenting nytt er kommet inn og ingen ny beskjed er gitt, så beskjeder ChatGPT ikke har lest ennå, ikke blir borte. Kjørt: ORDRE.md uendret.

## 2026-10-07 01:16 til 02:25 (Claude)
- Planlagt runde 01:16: ingen nye leveranser fra ChatGPT siden 23:43. ORDRE.md står som før.
- Brukte ventetiden på motoren. En agent i egen arbeidskopi laget PR 7:
  - Undertekster over HD-filmrammer: SmushPlayer tegner teksten også i et invertert lag fra DigHD, og pikslene som blir like, vises som originalpiksler over HD-rammen. Teksten står på samme sted som i originalen og blir aldri gul.
  - Filmrammene bygges med kilde per piksel, så dumpene og `DIGHD_VERIFY` viser det som faktisk er på skjermen. Dumpen heter `frame_NNNNNN_FILM_RRRRR.png` under film.
  - Kodek 5 kontrollert: indeksbilder med gjennomsiktig indeks 255 ble avvist av PNG-leseren i ScummVM, så ingen av de 14 124 rutene med kodek 5 og 150 objektbilder i rom 93 og 107 fikk HD. Rettet. Nå 30 kostymer med HD i 15 rom, 0 avvik i 135 dumper.
  - Rettet en krasj i `compose` ved fade etter skifte fra rom med HD-bakgrunn til rom uten (sett mellom rom 79 og 92), og svart HD der spillet viser en lys farge.
  - `engine/test.sh` gir 0 avvik for bakgrunner og uskalerte figurer. Patchen gjelder rent på c9091321.
- Så på dumpene (undertekst over filmramme i introen, kodek 5-figurer i rom 40) og flettet PR 7 (0a49408) etter grønn CI. Slettet testmoddene (470 MB) og agentens arbeidskopi.
- Runde 02:20: fortsatt ingen nye leveranser.
- Åpent: farger i uttrekket for kodek 5 når skuespillerpaletten ikke er satt. Lagt i todo.

## 2026-10-07 02:52 til 04:50 (Claude)
- Planlagt runde 02:52: ingen nye leveranser fra ChatGPT (siste 23:43). Tok neste punkt i motorlista med en agent i egen arbeidskopi.
- PR 8: fargesyklede områder i HD-bakgrunner og HD-objekter vises nå med HD-bildet og følger syklingen. Forholdet mellom nåværende og opprinnelig farge per indeks interpoleres med en kvadratisk B-spline fra 3 x 3 originalpiksler, også for naboene til syklede piksler. Metodene ble prøvd i Python på rom 22 først: forhold per piksel ga rutenett, bilineær ga stjernemønstre, kubisk og uskarphet ga mindre bevegelse, uten naboring ble det harde kanter.
- Ved palettendring bygges nå bare piksler med endret farge på nytt. Ett syklingssteg i rom 22 tar 2,0 ms mot 7,8 ms før. Hele skjermen tar 9,0 ms mot 7,8 ms.
- `DIGHD_VERIFY` sjekker også at skjermen er lik hele skjermen bygget på nytt, og teller syklede piksler for seg. Ny `DIGHD_BENCH`. `engine/test.sh`: 0 avvik. Patchen gjelder rent på c9091321. Ikke testet med ekte skjerm.
- Så på vannet i rom 22 i seks rammer før og etter: før grove 4x4-blokker, nå HD med bevegelse. Flettet PR 8 (ec978cb) etter grønn CI.
- Runde 04:47: fortsatt ingen nye leveranser.

## 2026-10-07 05:19 til 06:55 (Claude)
- Planlagt runde 05:19: ingen nye leveranser fra ChatGPT (siste 23:43). Tok HD-tekst fra motorlista med en agent i egen arbeidskopi.
- PR 9: all tekst vises i HD. Dialogen og menyene bruker fire tegnsett i DIG.LA1 (`CharsetRendererV7`), ikke NUT-fonter; filmene bruker FONT0 til FONT3.NUT. Begge tegnerne melder hver glyf til DigHD, som husker den per bufferpiksel og legger HD-glyfen over bildet som er under teksten. Bare piksler som fortsatt har verdien glyfen skrev, får glyf, så ingen tekst står igjen.
- Skalerer: nearest, Scale4x og xBR 4x prøvd på alle 8 fontene. xBR valgt (jevne rundinger, myke kanter). Glyfene lages med pikslene fra nabotegn i samme farge, ellers fikk kanten hakk mellom bokstavene. `DIGHD_TEXT` velger skalerer.
- Testet uten skjerm i rom 2 og introen: med `nearest` 0 avvik i teksten i 45 dumper, plasseringen stemmer i 47 av 47, klassisk modus og gult felt riktige. `engine/test.sh`: 0 avvik. Ingen målbar tidsøkning i rom 2, omtrent 0,5 ms mer per filmbilde med tekst.
- Så på nærbilder av dialogen i rom 2 og en filmundertekst før og etter, og flettet PR 9 (804cb3c) etter grønn CI.
- Funnet av agenten: når et banner eller hovedmenyen ligger over en figur, skinner HD-figuren svakt gjennom boksen. Feilen fantes fra før. Lagt i todo.
- Runde 06:53: fortsatt ingen nye leveranser.

## 2026-10-07 07:25 til 08:25 (Claude)
- Planlagt runde 07:25: ingen nye leveranser fra ChatGPT. Tok feilen der figurer skinte gjennom bannere og menyer med en agent i egen arbeidskopi.
- PR 10: en piksel får HD-figur bare når den faktisk viser figuren. Hver piksel en kostymerute tegner, merkes med tegningen og verdien ruten skrev, og merket gjelder bare så lenge verdien står der. `markRectAsDirty` tar bort merkene (unntatt skuespillerens eget rektangel, tekst og blast-objekter), og merkene lagres og legges tilbake med bannere. Volumbanneret og hovedmenyen over en astronaut er nå like originalen (før 241 og 691 avvikende piksler). Gult felt gir 0 gule piksler i banneret og i tekst over figurer uten HD (før 1082 og 303). `engine/test.sh`: 0 avvik, samme tid. Så på før- og etterbildene og flettet PR 10 (725fb24).
- Tom spurte etter liste og ordre over grafikken ChatGPT skal lage. Ny `GRAFIKKLISTE.md` (`dighd gpt-ordre` skriver den sammen med ORDRE.md): oversikt over alt som skal lages og alle 188 gjenstående jobber i prioritert rekkefølge, delt i 19 bestillinger på 10. Bestilling 1 er det samme som ORDRE.md. ChatGPT skal ta neste bestilling uten å vente på ny ordre. Sendt til `gpt-arbeid` sammen med ny ORDRE.md og oppdatert AGENTS.md for grenen.

## 2026-10-07 08:51 til 10:15 (Claude)
- Planlagt runde 08:51: ingen nye leveranser fra ChatGPT. Tok kodek 16 og fargene for kodek 5 med en agent i egen arbeidskopi.
- PR 12: kostymene med kodek 16 (95 lyn i rom 30, 96 spøkelse i rom 31, 118 Boston Low som svømmer i rom 33, 266 og 267 i biblioteket i rom 92) får HD-sprites. Funnet: ScummVM tegner kodek 16 alltid, og kodek 5 uten satt skuespillerpalett, med kodene rett som palettindekser. Uttrekket farger nå kodek 5 og 16 med rompaletten der kostymet vises (`docs/kostymefarger.csv` for 35 målte, ellers jevneste palett). 149 kostymer endret, kodek 1 byte for byte likt. Andel figurpiksler med HD gikk fra 12 til 100 prosent til 96 til 100 prosent. Ny testkrok `DIGHD_TEST_COSTUME`. Så på biblioteket med kostyme 267 og flettet PR 12 (74d9f8e). Kjørte `dighd extract --only akos` på nytt i hovedkopien.
- Tom ba om å kunne spille og teste rett fra repoet. Nytt `./spill.sh` i roten: sjekker pakkene, henter spillfilene og siste HD-mod, bygger motoren første gang og når patchen er endret (stempel i `engine/scummvm/.dighd-stempel`), og starter spillet med undertekster. Valg: `--rom N` (hopper over filmene), `--klassisk`, `--gult`, `--auto` (automatisk oppskalering av resten med ChatGPT-bildene oppå), `--fort`, `--fullskjerm`, `--programvare` (uten OpenGL). Ny `docs/SPILLTEST.md` med valg, taster og hva Tom bør se etter.
- Testet fra en fersk `git clone`: spillfilene og modden ble hentet, motoren bygget fra bunnen, og spillet startet i rom 22 med HD-bakgrunnen og HD-vannet (uten skjerm, OpenGL finnes ikke her, så `--programvare`). Funnet underveis: testhoppet virker ikke mens introfilmen går, så `--rom` hopper over filmene. `--auto`-modden bygget på 86 sekunder (174 MB), og rom 9, 22 og 28 er byte for byte ChatGPT-bildene.

## 2026-10-07 10:15 til 10:25 (Claude)
- Flettet PR 13 (`./spill.sh`). Runden 10:15 fant tre leveranser fra ChatGPT (09:46, 09:59 og 10:07, etter at Tom startet den med ordren): 60 jobber godkjent, 36 av 106 rom og 8 av 30 store objekter ferdige. rom111 avvist av kontrollen (blokker opptil 4,4 px), rom101 til sjekk (1,6 px).
- Så gjennom alle 42 nye HD-bilder side om side med originalen, og nærbilder av gåtedetaljene: inngraveringene i rom 102 og panelet i rom 107 er trofaste.
- Funnet: obj097 (kartet i rom 11) har gjort de små grønne merkene om til krøllete tegn i en ny rund skive. Rom 11 under har gjort de samme merkene om til grønne steiner i en skive (originalen har en svak bue der). Godtok rom 11, avviste obj097 og ba om at den lages lik rom 11 der.
- Ny manuell avvisning i pipelinen: `docs/gpt-avvisninger.csv` (jobb, sjekksum for resultatet, grunn, forslag til ny prompt). Gjelder bare den leveransen, så en ny blir kontrollert vanlig. Bilder som ikke lenger er ferdige, fjernes fra `work/gpt-ferdig` og provenance, så de ikke kommer med i modden. Ny test, 13 bestått.
- Ny runde: modden med 37 rom publisert i `hd-mod` (81 MB). Ny ORDRE.md med obj097 og rom111 først, så rom 25 til 27.

## 2026-10-07 10:53 til 11:05 (Claude)
- Planlagt runde 10:53: tre nye leveranser fra ChatGPT (10:43, 10:50 og 10:56). 98 jobber godkjent, 53 av 106 rom og 10 av 30 store objekter ferdige. Leveransen 10:56 (rom 39 til 44) kom etter hentingen og tas neste runde.
- Så gjennom alle 20 nye eller endrede HD-bilder mot originalen. Nærbilder: inngraveringene i rom 35 er trofaste. Ny obj097 stemmer nå med rom 11 (grønne steiner i skiven), godkjent.
- rom111 er levert på nytt og fortsatt avvist av kontrollen (blokker opptil 6,8 px). rom101 står fortsatt til sjekk.
- Modden med 54 rom publisert i `hd-mod` (127 MB).
- Tom spurte om å spille fra repoet i nettleseren. Svarte at det går lokalt (ScummVM i WebAssembly på localhost), men ikke på en åpen adresse, fordi spillfilene og grafikken tilhører Disney/Lucasfilm. Satte en agent på nettleserversjonen.

## 2026-10-07 11:05 til 12:25 (Claude)
- Agent laget nettleserversjonen (PR 15): `./spill.sh --nettleser` bygger ScummVM med HD-patchen for WebAssembly etter ScummVM sin egen oppskrift (Emscripten 4.0.10 i `engine/emsdk`, kilde i `engine/scummvm-web`) og serverer den fra `work/nettleser` på http://localhost:8000. Serveren lytter bare på 127.0.0.1, og siden nekter å starte utenfor localhost. Patchen er uendret. Valg i adressen: `?rom=22`, `?klassisk=1`, `?gult=1`, `?mod=auto`.
- Testet av agenten i Chromium uten skjerm: hele flyten fra en kopi uten mod og motor, intro med HD-tekst, rom 22 og 9 i HD, Ctrl+H, Ctrl+Shift+H, F5, lagring og lasting etter omlasting. Nearest-kontrollen ga samme avvik som den vanlige motoren. 1200 bilder i rom 22 tok 12,0 s mot 11,5 s. Så på skjermbildet av rom 22 og flettet PR 15 (b998343).
- Runde 12:05: seks nye leveranser fra ChatGPT (11:36 til 12:10). 172 jobber godkjent, 103 av 106 rom og 29 av 30 store objekter ferdige. Avvist av kontrollen: rom050 (28 px), rom079 og obj547 (7 px). Rom 88 venter på del 2 til 9, som kom etter hentingen. Modden med 104 rom publisert i `hd-mod` (235 MB).
- Så gjennom alle 69 nye HD-bilder side om side med originalen. Nærbilder: symbolpanelene i rom 69 og 76 er trofaste, spirene på verdenskartet (rom 77) står der de skal, og hånden i obj884 er lik i alle tre tilstandene. Ingenting avvist ved gjennomsyn.
- Ny ORDRE.md med beskjed om det som gjenstår (rom 50, 79, obj547, rom 88) og om at jobbene med status sjekk kan bli bedre.

## 2026-10-07 12:14 til 13:40 (Claude)
- Runde 12:14: rom 88 del 2 til 9 kom inn, men del 6 til 9 er avvist (forskjøvet opptil 23 px, del 7 med kantlikhet 0,08). Del 7: ChatGPT malte over det svarte feltet øverst i alle fem forsøkene. Rom 50: hånden og staven er flyttet. La inn presis retur for begge i `docs/gpt-avvisninger.csv` og sendte beskjed.
- Agent laget neste bestilling (PR 16): lagjobber `lagNNN_KK` for de mindre objektbildene, der rommet tegnes med et sett objekttilstander på plass og objektene klippes ut etterpå, med samme deler som romjobbene og det godkjente HD-rommet som bilde to. Overlappende objekter får hvert sitt lag, og store objektbilder som små objekter ligger oppå, er med som underlag. Inventaret blir ikonark `ikonNN`. 236 lagjobber dekker 460 objektbilder, og 3 ikonark dekker 149 ikoner; i alt 639 av 642 objektbilder. `gpt-inn` kontrollerer hvert objekt for seg (mangler eller tegnet om). Rom- og objektjobbene er byte for byte uendret. 16 tester bestått. Så på referansebilder for et lag og et ikonark, og flettet PR 16 (12455c2).
- Kjørte `dighd gpt-pakke` (431 jobber) og en runde. Ny ORDRE.md med de avviste romjobbene først og så lagjobbene. 25 bestillinger i GRAFIKKLISTE.md.
- Så gjennom de oppdaterte bildene: obj884 (hånden lik i alle tre tilstandene), obj886, rom 72, 79 (hansken beholdt), 90, obj547 og obj557. Alle trofaste.
- ChatGPT leverte rom 111 på nytt 12:38, dårligere enn 11:09 (4,6 mot 1,4 px), og rommet falt ut av modden. Satte 11:09-versjonen tilbake og la den nye som `alternativ_1238.png`. Nå 104 av 106 rom (mangler 50 og 88) og 30 av 30 store objekter. Modden publisert (238 MB).

## 2026-10-07 13:41 til 14:05 (Claude)
- Planlagt runde (satt til 12:58, kom 13:41): ingen nye leveranser.
- `gpt-inn` tar nå vare på den beste godtatte leveransen per jobb i `work/gpt/beste/`. Kommer det en ny leveranse som er dårligere (avvist mot godtatt, eller sjekk mot godkjent), brukes den forrige, og kommentaren sier at den nye var dårligere. Avvises den forrige ved gjennomsyn, slettes den. Kontrollen per leveranse er flyttet til `_evaluate`. Ny test, 17 bestått. Med ekte data: status og alle HD-bilder byte for byte uendret, 187 godtatte leveranser lagret.

## 2026-10-07 14:27 til 16:30 (Claude)
- Planlagt runde 14:27: ingen nye leveranser fra ChatGPT siden 12:38. Tok punktet om å kontrollere de nye rommene i motoren med en agent.
- PR 18: nytt `tools/romtest.sh` kjører motoren uten skjerm i hvert rom (også med kameraet over hele store rom) og skriver rapport, CSV, kontaktark med HD og original side om side og nærbilder av avvik, figurer og sømmer. Alle 111 rom kjørt med modden (226 kjøringer, 25 minutter): 110 lastet, ingen krasj eller heng etter rettingen, HD-bakgrunnen brukt i alle 104 rom som har den, ingen forskjøvne HD-bilder, og figurene går bak det samme i HD som i originalen. Rettet i testkrokene: hopp til rom 93 krasjet (assert i `clampCameraPos`), `DIGHD_TEST_CAMX` ble overstyrt (ny `DIGHD_TEST_CAMY`), og ny logglinje `whole screen`. `engine/test.sh`: 0 avvik. Flettet PR 18 (04b1a13). Rapporten fra kjøringen ligger i `work/romtest-siste/`.
- Funn i ChatGPT-bilder, sett i nærbilder: i rom 32 er vannet som renner ned under buen blitt en utskåret steinbue. Avvist med presist forslag. obj547 (hånden har en annen form) og obj343, obj347, obj355 og obj886 (synlig søm mot HD-rommet, fordi objektjobbene ble laget uten HD-rommet som bilde to) satt til sjekk med forslag om å legge ved HD-rommet.
- Ny kolonne `status` i `docs/gpt-avvisninger.csv`: avvist (tas ut av modden) eller sjekk (brukes til et bedre kommer, men skal gjøres om). Ny test, 18 bestått. Modden: 103 rom (rom 32 ute til det er gjort om) og 30 store objekter.

## 2026-10-07 17:09 til 18:30 (Claude)
- Planlagt runde 17:09: ingen nye leveranser fra ChatGPT siden 12:38. Tok figurene med en agent.
- PR 20: figurark `figCCC_KK` for kostymene. Rutene i en animasjon står på ett ark i 4x på en flat bakgrunnsfarge som ikke finnes i kostymet, og klippes ut til `costumes/costumeCCC_NNN.png` med alfa fra originalen. Kontroll per rute (dekning, omriss, kantlikhet) og flimmer mellom nabo-ruter. Kantpiksler som er dratt mot bakgrunnsfargen, fylles innenfra, ellers fikk figuren en turkis glorie i spillet. `build-mod --egne` tar med egne kostymeruter, og `gpt_runde.sh` tar med godkjente figurruter.
- Hovedpersonene funnet fra skriptene og animasjonene i AKOS: Boston Low kostyme 14 (gis 140 ganger i 36 rom), Maggie Robbins 18, Ludger Brink 15 med variantene 16 og 17. Alle 331 kostymer etter hvor mye de vises i `docs/figurer.csv`. Alle kostymer gir 4031 ark; de tre hovedkostymene 114.
- Pilot: 4 ark med 229 ruter av Boston Low (stående, gange mot høyre, venstre og mot oss, snakkehoder), i ordren rett etter de avviste jobbene. Så på referansen for ark 1 og flettet PR 20 (0015571). Kjørte `gpt-pakke` (435 jobber) og sendte ny ordre med beskjed om piloten. 22 tester bestått, de 431 gamle jobbene byte for byte uendret. Grensene for flimmer er bare prøvd på kunstige ark og justeres etter de første ekte leveransene.

## 2026-10-07 19:07 til 20:50 (Claude)
- Planlagt runde 19:07: ingen nye leveranser fra ChatGPT siden 12:38. Tok objektbytte i romtesten med en agent.
- PR 21: testkroken `DIGHD_TEST_OBJSTATE` setter objekttilstander etter testhoppet (liste som `884:2,886:1`, eller `alle` som går gjennom alle tilstandene i rommet), og `tools/romtest.sh --objekter` lager rapport, `objekter.csv` og nærbilder per objekt og tilstand. Alle 111 rom: 489 tilstander, HD brukt i 406, alle 30 ChatGPT-objektene brukt i alle tilstandene, 57 tilstander dekket av et annet objekt (rom 89 og 100). Rettet en assert ved objekter med bare BOMP-bilde (rom 107). `engine/test.sh`: 0 avvik. Flettet PR 21 (e8999f6).
- Agenten fant en lys strek langs kanten av obj547. Målte alle 133 HD-bilder: 64 har en tydelig lysere ytterrad, nesten alltid nederst (opptil 70 fargetrinn), fordi ChatGPT lar den grå kanten på lerretet blø noen piksler inn. Ny `repair_edges` i `gpt-inn`: på sider som grenser mot den grå kanten, byttes ytterrader som skiller seg tydelig fra raden 8 piksler inn med den nærmeste gode raden. Etter ny kjøring: 5 igjen over grensen (rett over), ingen status endret. Ny test, 23 bestått.
- Modden bygget på nytt med de rettede kantene og publisert i `hd-mod` (103 rom, 485 objektbilder, 236 MB).

## 2026-10-07 21:14 (Claude)
- Tom ba om stopp til han sier start igjen. Slettet den planlagte runden 21:20; ingen planlagte runder står igjen. Ingen agenter kjører. Ordren i `gpt-arbeid` står som den er.

## 2026-10-09 04:44 (Codex)
- Tom ba om å spille direkte fra GitHub Pages med HD-grafikk. Laget ny, separat inngang under engine/pages og en pakker som bare tar motoren, ScummVM-temaene og tilhørende GPL-kildekode. Ingen spill- eller HD-filer i kodegrenen eller nettsidepakken.
- GitHub avviste Pages for det private spillrepoet (HTTP 422, abonnementet støtter det ikke). Opprettet derfor det offentlige motorrepoet Tombonator3000/Dig-HD-Web. Spillrepoet og alle grafikkgrener beholdes private.
- Spillmappen og HD-pakken velges én gang i nettsiden og lagres lokalt i IndexedDB. Virtuelle /data-adresser besvares fra lokal lagring, også manglende spillfiler; temaer lastes under riktig Pages-prefiks. Lagring i spillet er separat og beholdes når filpakken fjernes.
- Bygget den låste ScummVM-commiten med uendret HD-patch og Emscripten 4.0.10. Filtestene: 4 bestått. Chromium uten skjerm: faktisk rom 22 i 1280 x 800 HD, rom 9, mappevalg og filer etter omlasting, HD/klassisk-knapp, spillmeny og et ekte dig.s01-lagret spill som beholdes etter nettleserlukking. Ingen spill- eller HD-HTTP-forespørsler. Musikk og tale ikke testet, BUN-filene mangler lokalt.
- Nettsiden bygges og publiseres av GitHub Actions. Kontroll av den publiserte adressen gjenstår. Full gjennomspilling og mobiltest ikke utført.
- Lasting kontrollert etter lukking av nettleseren: startet i rom 9, lastet det navngitte spillet fra F5-menyen og kom tilbake til rom 22 med HD.
