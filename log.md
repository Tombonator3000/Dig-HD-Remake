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
