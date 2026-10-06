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
