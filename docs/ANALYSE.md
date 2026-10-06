# The Dig HD Remake: analyse av filer, omfang og veien videre

Skrevet 6. oktober 2026. Grunnlaget er spillfilene i Drive-mappen, innholdet i dette repoet, kildekoden til ScummVM (master per 6. oktober 2026) og uttrekksverktøyet thedig-textures.

## Kort fortalt

- Drive-mappen har en komplett og uendret kopi av spilldataene. Det er den engelske standardutgaven, med data bygget 7. november 1995. Den kjører rett i ScummVM og passer med uttrekksverktøyene uten noen ombygging.
- DIG.LA1 i Drive-mappen er 88 673 344 byte. Det er nøyaktig samme størrelse som filen thedig-textures er testet byte for byte mot. Verktøyet skal derfor fungere på dine filer.
- Repoet har foreløpig bare tre konseptbilder. Ingen kode, ingen AGENTS.md.
- Dekompilering er ikke det vanskelige. Motoren finnes allerede i ScummVM, skriptene kan leses med descumm eller NUTCracker, og all grafikk kan trekkes ut. Det store arbeidet er selve HD-grafikken og en ScummVM-fork som viser den.
- Omfanget, målt i filene: 111 rom, 642 objektbilder, 331 kostymer med til sammen 28 490 ruter, og 55 SAN-filmer med 12 638 rammer.
- Det viktigste valget du må ta tidlig: trofast HD (samme utseende, bare skarpere) eller ny tegnestil som konseptbildene. Etter mitt anslag er det siste mange ganger så mye arbeid.

## 1. Hva som ligger i Drive-mappen

Mappen inneholder bare datafilene, ingen exe og ingen `_other/`-mappe. Det er alt ScummVM trenger.

| Fil | Størrelse | Hva det er |
| --- | --- | --- |
| `DIG.LA0` | 16 304 byte | Indeks: romnavn, grenser, kataloger over skript, lyd, kostymer og objekter |
| `DIG.LA1` | 88,7 MB | Alle rom: bakgrunner, objektbilder, z-planer, walkboxer, skript, AKOS-kostymer, paletter |
| `DIGMUSIC.BUN` | 261,6 MB | iMUSE-musikk |
| `DIGVOICE.BUN` | 130,1 MB | Tale |
| `VIDEO/*.SAN` | 55 filer, 178,6 MB | SMUSH-filmer og animerte scener. Størst er `SQ1.SAN` (50 MB, introen) |
| `VIDEO/FONT0-3.NUT` | 4 filer | Fonter for tekst i filmene |
| `VIDEO/DIG.TRS`, `VIDEO/DIGTXT.TRS` | 46 KB og 11 KB | Undertekster til filmene. ScummVM leser `digtxt.trs` i `smush_player.cpp` |

Totalt rundt 660 MB.

**Utgave:** Jeg har lest indeksen i `DIG.LA0`. Blokken MAXS sier motorversjon `7.3.4 (Oct 09 1995)` og dataversjon `Tue Nov 7 1995`. Det finnes ingen `LANGUAGE.BND`, så dette er den engelske utgaven. Filstørrelsen 16 304 byte stemmer med oppføringene for The Dig i ScummVM sin deteksjonstabell (`engines/scumm/scumm-md5.h`). Jeg fikk ikke en byte-eksakt kopi av LA0 gjennom Drive-koblingen, så MD5-summen er ikke kontrollert. Det gjør du lokalt med `tools/la0_info.py`, som sier fra hvis summen matcher standardoppføringen for The Dig i ScummVM (`d8323015ecb8b10bf53474f6e6b0ae33`).

**thedig-textures og NUT-filer:** Verktøyet nevner 6 NUT-filer fordi GOG-utgaven har to ekstra i `_other/`. Verktøyet leter etter alle `*.NUT` under spillmappen, så det fungerer fint med de fire du har.

## 2. Hva som ligger i repoet

Tre bilder lastet opp 5. oktober: modellark for Maggie Robbins, Boston Low og Ludger Brink i en ren tegneseriestil, med originalspriten ved siden av. Filnavnene viser at de kommer fra et Reddit-innlegg ("If The Dig were remastered, art by me"), og de er signert av tegneren. De ligger nå i `docs/konsept/`. De fungerer godt som stilmål, men tegningene er hans. Hvis prosjektet en gang skal vises fram, bør du spørre ham og kreditere ham.

Repoet er privat. Det er bra, men spillfilene og uttrukket grafikk skal likevel ikke inn i git. `.gitignore` er satt opp for det.

## 3. Hva spillet består av

Tallene for rom kommer fra min lesing av `DIG.LA0`. Tallene for bilder og kostymer kommer fra LA1-tellingen i thedig-textures (`docs/la1-census.txt`), som er gjort på en fil med nøyaktig samme størrelse som din.

| Del | Antall | Kommentar |
| --- | --- | --- |
| Rom | 111 | 27 er bredere enn 320 piksler og ruller sideveis, 11 er høyere enn 200 |
| Rom med z-plan (forgrunnsmaske) | 61 | Maskene må skaleres sammen med bakgrunnen |
| Rom med flere paletter | 21 | Rom 10, 15, 19, 20, 23, 27, 31, 32, 33, 41, 48, 50, 68, 73, 75, 79, 82, 85, 88, 91, 106 |
| Objektbilder (OBIM) | 642 | 492 SMAP og 150 BOMP. Noen objekter har opptil 14 tilstander |
| Kostymer (AKOS) | 331 | 28 490 ruter, 58,5 MB av LA1 |
| Skript | 303 globale, 646 lokale | Pluss inn- og utgangsskript per rom og verbskript i 842 objekter |
| Globale objekter | 984 | |
| Tegnsett | 5 | Pluss 4 NUT-fonter for filmene |
| SAN-filmer | 55 | 12 638 rammer |

**Bakgrunnene i tall:** Til sammen er bakgrunnene 10,5 millioner piksler, altså like mye som 163 vanlige skjermbilder. Med 4x oppskalering blir det 167 megapiksler. De største rommene:

| Rom | Navn | Original | 4x |
| --- | --- | --- | --- |
| 23 | nexus | 1808 x 200 | 7232 x 800 |
| 104 | landercu | 1616 x 450 | 6464 x 1800 |
| 2 | cockpit | 976 x 200 | 3904 x 800 |
| 88 | tombot | 800 x 500 | 3200 x 2000 |
| 27 | powerrm | 512 x 780 | 2048 x 3120 |
| 80, 83, 94, 95 | trm...n (trikkekart) | 840 x 200 | 3360 x 800 |

Noen rom er nesten tomme fordi SAN-filmer tegner innholdet: 1 logo, 86 blanker, 93 icons, 103 lander og 104 landercu. De må behandles sammen med filmene.

Hele romlisten med mål, z-plan, paletter og antall objektbilder ligger i `docs/rom-oversikt.csv`. Kolonnene `prioritet`, `status` og `notat` er tomme og ment for å følge arbeidet rom for rom.

## 4. Dekompilering: hva som faktisk trengs

Det er ikke nødvendig å dekompilere `DIG.EXE`. ScummVM har en fullstendig gjenoppbygging av SCUMM v7-motoren, med SMUSH, AKOS og Digital iMUSE.

Det du trenger, er to ting:

1. **Skriptene**, for å forstå når objekter skifter tilstand, når paletten byttes og hvilken SAN-film som spilles hvor. `descumm -7` (fra scummvm-tools) eller `nutcracker` gir lesbar kode. Dette er oppslagsverk, ikke noe du skal endre.
2. **Grafikken**, som utgangspunkt for HD-versjonene. thedig-textures trekker ut alle bakgrunner, objektbilder, AKOS-ruter, SAN-rammer og NUT-tegn til PNG, med palett og et `manifest.json`. Hver fil er sjekket byte for byte mot ScummVM sin dekoder.

Praktisk om thedig-textures:

- Krever Python 3.12 og Pillow. `clang++` trengs bare for verifiseringen.
- Standardstien er en macOS-sti til GOG-utgaven, så bruk `--game STI`.
- Trenger 15 GB ledig plass når SAN-rammene er med, ellers 1 GB.
- Skriv utdata utenfor repoet, for eksempel `~/dig-out`.

## 5. HD-bakgrunner

**Oppløsning:** Bruk 4x, altså 1280 x 800 for et vanlig rom. Originalen er 320 x 200 vist på en 4:3-skjerm, så pikslene er litt høye. ScummVM retter dette ved å strekke bildet til 1280 x 960 når det vises. Hvis du maler i 1280 x 800 og lar strekkingen skje til slutt, blir alle koordinater eksakt 4 ganger originalen, og det gjør alt annet enklere.

**Fallgruver, i rekkefølge etter hvor mye de koster:**

1. **Objekter må passe på bakgrunnen.** Dører, lys og maskiner er egne objektbilder som tegnes oppå bakgrunnen. Skaleres de hver for seg, får de andre detaljer og synes tydelig. Sett sammen bakgrunn og alle objekttilstander til ett bilde, skaler samlet, og klipp ut igjen med den originale masken skalert 4x.
2. **21 rom bytter palett.** Da må HD-bildet enten finnes i flere varianter, eller så må fargene byttes i en shader. Lag en løsning for dette før du skalerer de rommene.
3. **Fargesykling (CYCL).** Når bildet går fra 256 farger til full farge, slutter fargesyklingen å virke. Det gjelder blant annet vann og energieffekter. Ta vare på hvilke palettindekser som sykles, og tegn de områdene som eget lag.
4. **Z-planer.** 61 rom har forgrunnsmasker. De skaleres med nærmeste nabo, eksakt 4x, aldri med utjevning.
5. **Walkboxer og klikksoner endres ikke.** Spillogikken skal fortsatt tro at rommet er 320 x 200.

**Oppskalering:** Real-ESRGAN eller en pikselkunstmodell fra OpenModelDB gir et trofast resultat raskt. Stable Diffusion med ControlNet (tile eller lineart) og lav denoise kan gi et mer "nymalt" uttrykk, men avviker mer fra originalen og må kontrolleres rom for rom. Test tre metoder på fem rom før du velger.

## 6. HD-sprites

331 kostymer med 28 490 ruter er mye, men tallet inkluderer også effekter og småting. Hovedpersonene står for en stor del.

- **Trofast HD:** Kan i stor grad automatiseres. Skaler alle ruter for én figur med samme modell og innstillinger, ellers flimrer figuren mellom rutene. Kantene må ha ren gjennomsiktighet (alfa 0 eller 255), ellers får figuren en mørk rand.
- **Ny tegnestil, som konseptbildene:** Til sammenligning brukte Double Fine over 30 tegnere på å tegne over 8000 animasjonsrammer på nytt til Full Throttle Remastered. Med KI kan du komme et stykke på vei med en modell trent på ett modellark per figur, men det er svært vanskelig å holde figuren lik fra ramme til ramme. Regn med mye manuelt etterarbeid.
- **Uansett stil:** Behold ankerpunkter og animasjonstiming fra AKOS. HD-ruten erstatter bare pikslene, og forskyvningen ganges med 4 når den tegnes. Da fungerer gange, snuing og leppesynk som før.
- **Fargeomkobling:** Spillet kan endre farger på figurer (mørke rom, skygger). I full farge må det gjøres som fargemultiplikasjon eller med oppslag på den originale palettindeksen.

Konseptbildene dekker de tre hovedpersonene. Det gjør dem til et naturlig første forsøk: Boston Low sin gangsyklus og snakkeanimasjon i ny stil viser raskt om den veien er realistisk.

## 7. Mellomsekvenser (SAN)

55 filer, 12 638 rammer. De faller i to grupper, og skriptene viser hvilken gruppe hver fil hører til:

- **Rene filmer**, som introen (`SQ1.SAN`, 50 MB). De fleste `SQ`-filene ser ut til å være slike sekvenser. Disse kan skaleres opp som video (rammene ut som PNG, og en videomodell som tar hensyn til naborammene, ellers flimrer det) og spilles av som MP4 eller WebM i stedet for SAN.
- **Filmer som er en del av spillet**, trolig trikketurene (`TRAM1-5`, `RTRAM1-5`) og filer som `ASTTUN`, `DARKCAVE` og `ALCOVE`. Hvis skriptene styrer dem mens spillet går, bør de fortsatt kjøres som SAN, med HD-rammer byttet inn én og én.

Undertekstene ligger i `DIGTXT.TRS` og tegnes av motoren oppå bildet, så de skal ikke ligge i de oppskalerte rammene.

## 8. Motoren: en ScummVM-fork

ScummVM har ingen støtte for å bytte ut grafikk i SCUMM-spill. Du må lage en fork. Den gode nyheten er at ScummVM allerede har et forbilde: Mac-utgavene av Loom og Indiana Jones 3 tegnes til en egen flate på 640 x 400 (`_macScreen` i `scumm.cpp` og `mac_drawStripToScreen` i `gfx_mac.cpp`), der spillbildet skaleres 2x og tekst tegnes i full oppløsning. En HD-fork kan følge samme mønster med en 32-bits flate på 1280 x 800.

**Prinsipp:** Spillogikken jobber som før i 320 x 200 og 256 farger. Hver gang motoren tegner bakgrunn, objekt eller figur, tegner forken det samme i HD-flaten. Finnes det en HD-fil i mod-mappen, brukes den. Hvis ikke, brukes originalpikslene skalert 4x. Da kan HD-grafikken legges inn litt etter litt, og spillet kan spilles hele veien. En hurtigtast bytter mellom klassisk og HD, slik Double Fine gjorde.

**Stedene i koden der det må kobles inn** (ScummVM master, commit `c909132`, 6. oktober 2026):

| Fil | Funksjon | Hva den gjør |
| --- | --- | --- |
| `engines/scumm/gfx.cpp` | `Gdi::drawBitmap` | Tegner bakgrunnsstriper og objektbilder |
| `engines/scumm/gfx.cpp` | `redrawBGStrip`, `drawStripToScreen` | Gjentegning og sluttkomposisjon til skjermen |
| `engines/scumm/object.cpp` | `drawRoomObject`, `drawObject` | Velger objekttilstand og tegner objekter |
| `engines/scumm/akos.cpp` | `AkosRenderer::drawLimb`, `paintCelMajMin`, `paintCelByleRLE`, `paintCelCDATRLE` | Tegner kostymeruter |
| `engines/scumm/palette.cpp` | `initCycl`, `cyclePalette`, `setCurrentPalette` | Fargesykling og palettbytte |
| `engines/scumm/smush/smush_player.cpp` | `SmushPlayer::play`, `handleFrame`, `updateScreen` | Filmavspilling |
| `engines/scumm/gfx_mac.cpp` | `mac_drawStripToScreen` | Forbildet for komposisjon i høyere oppløsning |

**Filnavn i mod-mappen:** Bruk ID-ene fra `manifest.json` i thedig-textures. Da bruker uttrekk, oppskalering og motor de samme navnene, og ingenting må oversettes manuelt.

## 9. Valget du må ta

| | A: Trofast HD | B: Ny tegnestil |
| --- | --- | --- |
| Utseende | Samme som originalen, skarpere | Som konseptbildene |
| Bakgrunner | KI-oppskalering pluss retusj | Må males på nytt, KI kan hjelpe |
| Figurer | Kan i stor grad automatiseres | Ny tegning av alle viktige animasjoner |
| Arbeid (mitt anslag) | Uker for en prototype, måneder for alt | Mange ganger så mye som A |
| Risiko | Middels | Høy, særlig for figurer |

Motoren er den samme for begge. Mitt råd er å bygge forken og en full A-versjon først. Den gir et spillbart HD-spill, og alt B trenger av motor og verktøy er da på plass. Parallelt kan du teste B på Boston Low og ett rom for å se om det holder.

## 10. Første steg

1. Kopier Drive-mappen til laptopen, for eksempel `~/Games/TheDig`. Kjør `python3 tools/la0_info.py ~/Games/TheDig/DIG.LA0` og sjekk at MD5 matcher standardoppføringen.
2. Start spillet i ScummVM for å bekrefte at filene er hele.
3. Kjør thedig-textures: `thedig-textures extract --game ~/Games/TheDig --out ~/dig-out`. Kjør gjerne `make verify` også.
4. Dekompiler skriptene med `nutcracker` eller `descumm -7` til `~/dig-out/scripts`.
5. Fork ScummVM, bygg på Linux og lag bakgrunnsbytte for ett rom. Gode kandidater ut fra målene: rom 22 (beach) eller 24 (view), som er 320 x 200 med z-plan, én palett og to objektbilder. Deretter et rullende rom som 34 (museum, 544 x 200) eller 25 (airlock, 736 x 200).
6. Stiltest: fem rom gjennom tre oppskaleringsmetoder, og Boston Low sin gangsyklus i ny stil.
7. Distribusjon, hvis det blir aktuelt: del bare forken og verktøyene. Grafikken genereres lokalt fra brukerens eget spill. Disney/Lucasfilm eier The Dig, og ferdig HD-grafikk er avledet av deres verk.

## Kilder

- ScummVM, SCUMM-motoren: https://github.com/scummvm/scummvm/tree/master/engines/scumm
- ScummVM deteksjonstabell: https://github.com/scummvm/scummvm/blob/master/engines/scumm/scumm-md5.h
- thedig-textures (uttrekk og LA1-telling): https://github.com/felipe-dos-santos81/thedig-textures
- NUTCracker: https://github.com/BLooperZ/nutcracker
- scummvm-tools (descumm): https://github.com/scummvm/scummvm-tools
- Full Throttle Remastered, om grafikkarbeidet: https://www.gamedeveloper.com/art/full-throttle-remastered-curating-a-classic
