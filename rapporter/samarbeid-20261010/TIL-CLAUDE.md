# Til Claude: grafikkmottak og arbeidsdeling 10. oktober 2026

Tom har bedt oss bruke flere grafikkagenter og samarbeide tettere med deg. Codex samordner grafikkleveransene. Du eier kode, mottak, kontrollresultater og modbygging. Tom godkjenner utseende og stil.

Dette dokumentet er klargjort for publisering i `gpt-arbeid`. Det er ikke en bekreftelse på at en aktiv Claude-chat har lest det. Les dokumentet direkte fra din hentede `work/.gpt-gren/rapporter/samarbeid-20261010/`, ettersom `tools/gpt_gren.sh hent` kopierer resultater og notater til `work/gpt`, men ikke rapportmappen.

## Bekreftet leveransesnapshot

Grafikkgren: `Tombonator3000/Dig-HD-Remake`, `gpt-arbeid`, commit `2ecb21869437980d5fd98e849ede831cb8c63703`. Kodegrunnlag: `main`, commit `36cd09f13eb0201cff190d8d0c99c788a8bcaa6b`, som inneholder flettet PR 44 og `myke-figurer` versjon 2. Senere lokale kandidater er ikke inkludert i dette snapshotet.

| Arbeid | Grafikklevert og pushet | Gjenstår |
| --- | ---: | ---: |
| Romlag | 210 av 230 | 20 |
| Korrigert vanlig Brink | 73 av 208 | 135 |
| Boston i romdrakt, kostyme 1 | 7 av 22 | 15 |
| Maggie i romdrakt, kostyme 2 | 0 av 9 | 9 |
| Brink i romdrakt, kostyme 3 | 10 av 10 | 0 |
| Pig, kostyme 7 | 1 av 9 | 8 |

Den nye ordren for kostyme 1, 2, 3 og 7 er dermed grafikklevert for 18 av 50 ark. Tom har uttrykkelig godkjent første Boston-romdraktprøve, første Brink-romdraktprøve og det korrigerte vanlige Brink-utseendet som grunnlag for videre produksjon. Det betyr ikke at alle senere ark er spilltestet eller visuelt godkjent.

De 18 nye ordrenes jobbnavn og SHA-256 finnes i vedlagte `leveranse-snapshot.json`. Leveransene er generatorens native PNG-filer med ekte alfa. Kildearkene `referanse.png`, `original_1x.png`, `prompt.txt` og `jobb.json` er beholdt uendret.

## Slik finner mottaket riktig materiale

Den eksisterende kodeflyten er `tools/gpt_runde.sh`, som henter grenen med `tools/gpt_gren.sh hent`, kjører `dighd gpt-inn` og `dighd myke-figurer`, og sender ordre, status og returer tilbake. Dette er dokumentert og kildekontrollert. Ingen aktiv halvtimekjøring er bekreftet på Kubuntu-maskinen i denne undersøkelsen.

`pipeline/dighd/myk.py` leser bare ett nivå under rapportmappen:

- `rapporter/*/fremdrift.json`, med `leveranser`, `jobb`, `resultat` og `sha256`.
- `rapporter/*/rutekart*.json`, med `ruter`, `entries` eller `koblinger` og en støttet bokskolonne.

De korrigerte romdraktarkenes aktuelle SHA-er står også i `rapporter/andre-figurer-hd-20261009/fremdrift.json`. De tilsvarende rutekartene ligger direkte under `rapporter/romlag-brink-20261010/`, blant annet `rutekart-nyordre-del*.json`. Den underordnede `nyordre/`-mappen er ekstra dokumentasjon, ikke eneste inngang til mottaket. Vanlig Brink er også ført i `rapporter/romlag-brink-20261010/fremdrift.json`.

Bruk den nye SHA-en, ikke en tidligere avvist versjon av samme jobb. Avvisningene i `docs/gpt-avvisninger.csv` er knyttet til gammel bildechecksum. Kontroller at gammel eksport blir fjernet når en rute faktisk avvises eller mangler, slik at gammel grafikk ikke skjuler manglende mottak.

## Konkret mottaksfeil: løst bakhode plasseres ved skyggefotlinjen

Grafikkagenten har prøvd faktisk versjon 2-import av den nye kandidaten til `fig016_12`. Kandidatens native SHA-256 er `ec2fb6500e8caf807cbeec8c8648d4c65a71a48c825d841aece83a67ecace1e7`. Arket har 16 synlige figur-/hodedeler og ett reelt originalfragment. Importen gir 16 ruter `ok` og én `sjekk`.

Originalruten `costume016_264.png` er et løst bakhode i en RGBA-rute på 9 × 64 originalpiksler. Uavhengig pikselmåling viser:

| Måling | Resultat i originalpiksler |
| --- | --- |
| Boks for alle piksler med alfa minst 128 | `[0, 0, 9, 64]` |
| Fem tekniske magentapiksler, RGB `[255, 87, 255]` | `[1, 63, 5, 1]` |
| De øvrige 71 hodepikslene | `[0, 0, 9, 9]` |

Den faktiske importen av dette hodet gir `flytt_hd: [-6, 207]`, snitt over union `0.033` og dekning `0.066`. Hodet havner nede ved den tekniske skyggefotlinjen. Dette kan ikke rettes ved å tegne hodet nederst i figurarket. Vurder kildeboks, målhøyde og plasseringsgrunnlag i mottaket med teknisk magenta skilt fra faktisk figurinnhold. Bevar originalens indeks- og ankerinformasjon.

Reproduserbart bevis finnes på denne Kubuntu-maskinen:

```text
/home/tombonator3000t/.codex/tasks/the-dig-romlag-brink-20261010/agent-brink/fig016_12-forsok1.import-v2.json
/home/tombonator3000t/.codex/tasks/the-dig-romlag-brink-20261010/agent-brink/import-v2/fig016_12-forsok1/myk_fig016_12.png
/home/tombonator3000t/.codex/tasks/the-dig-hovedfigurer-20261009/extract/costumes/costume016_264.png
```

`bakhode-mottaksfeil.json` ved siden av dette dokumentet inneholder den målte ruten og kodegrunnlaget. Grafikkandidaten skal behandles som kandidat til root har publisert den. En vellykket teknisk import er heller ikke en motor- eller animasjonstest.

En retting må samtidig bevare legitime atskilte effekter. Boston `fig001_06` og `fig001_07` inneholder små grå partikler fra originalen. De er ikke magentamarkører og skal ikke kastes eller telles som nye figurer. Rutekartets analyseboks omfatter alle delene som tilhører samme originalrute. Dokumentasjon ligger i `nyordre/fig001_06-partikkelbevis.*`, `nyordre/fig001_07-partikkelbevis.*` og de tilhørende rutekartene og v2-mottakskontrollene.

Originale enkelt-PNG-er og indeksbilder for kostyme 1, 2, 3 og 7 mangler i Codex' dekodede uttrekk. Her har vi jobbens RGB-kildeark og metadata, og har kontrollert native deler og tilordning. Full import mot originale enkelt-PNG-er og motorvisning er ikke dermed verifisert. Bruk ditt korrekte uttrekk ved mottaket; ikke tolk en diagnostisk fargenøkkel fra RGB-arket som bevis på original alfa.

## Romankere som blokkerer 15 lag

| Påkrevd bakgrunnsanker | Nåværende kontrollstatus | Lag som venter |
| --- | --- | --- |
| `jobber/rom032/resultat.png` | avvist | `lag032_01` til `lag032_07` |
| `jobber/rom077/resultat.png` | sjekk | `lag077_01` til `lag077_04` |
| `jobber/rom088_del7av9/resultat.png` | avvist | `lag088_01_del7av9` til `lag088_04_del7av9` |

Vi trenger et korrigert og godkjent anker med bekreftet checksum, eller en konkret kontrollbeskjed som avklarer ankeret. Ikke meld disse 15 lagene som produksjonsklare før avhengigheten er løst. En egen agent arbeider isolert med de fem andre tilbakeholdte lagene; dette dokumentet endrer ikke deres leveransestatus.

## Arbeidsdeling uten samtidig filskriving

Grafikkagentene lager hver sin tildelte jobb i egne kataloger under `/home/tombonator3000t/.codex/tasks/the-dig-romlag-brink-20261010/`. De endrer ikke felles leveranseoversikter, Git-indeks eller jobbenes beskyttede filer. Codex-root kontrollerer resultatene, kopierer godkjente native filer, oppdaterer SHA-er og rutekart, og er eneste grafikkagent som committer og pusher til `gpt-arbeid`.

Claude bruker sin egen kodecheckout og egen `work/.gpt-gren`. Ikke kjør `tools/gpt_gren.sh send` eller en full kontrollrunde i den aktive grafikkcheckouten `/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk`. Skriptets `git add -A` ville også kunne ta med pågående grafikkarbeid. Ikke bruk den eldre `/home/tombonator3000t/Documents/Codex/Dig-HD-Remake`-mappen uten først å kontrollere branch og lokal tilstand; den var en gammel `gpt-arbeid`-checkout ved undersøkelsen, med uversjonerte arbeidsmapper.

Claude eier `ORDRE.md`, `status.csv`, `RAPPORT.md` og `jobber/*/retur.md`. Grafikeren eier `resultat.png`, `notat.md` og sine leveranserapporter. Begge henter den andre partens push før egen publisering og avbryter ved en reell konflikt uten reset, clean eller overskriving. Del ikke samme Git-indeks.

## Neste handling og kvittering

Hent den publiserte grafikkcommiten og kontroller de nye arkene med koden fra main som inneholder PR 44. Undersøk bakhoderuten over før du kaller plassering og størrelse ferdig. Ta deretter inn gyldige leveranser i din vanlige kontrollrunde, vurder de tre blokkerte romankerne, og test hodekobling, tale uten skalapulsing, partikkeleffekter og figurkanter i faktisk spilltilstand.

Svar gjennom den eksisterende repo-kanalen. En kort kvittering kan legges i `rapporter/samarbeid-20261010/fra-claude/` med mottatt grafikkcommit, kodecommit, jobbnavn og bilde-SHA, importresultat, eventuell eksport-/modcommit, utførte spilltester og neste handling. `fra-claude-eksempel.json` viser feltene, men er et tomt eksempel og skal ikke tolkes som mottatt eller bestått kontroll. Tom har ikke bedt om en ny betalt tjeneste, ny Claude-prosess eller ny automasjon.


## Oppdatert med ekte originalRGBA

Se [mottakskontroll av44ark](nyordre-mottakskontroll/TIL-CLAUDE.md). Manglende originaler for kostyme1/2/3/7 er nå dekodet isolert. Lokalt v2-mottak gir440synlige ruterok og1Pig-rute tilgjennomsyn, samt157tekniske magentaruter som må håndteres særskilt. Faktisk originalalfa for begge utliggerne er avklart. Rutekartet for007_163 er utvidet kildebevist, uten å endre nativegrafikk. Ingen spilltest eller mottakskvittering er påstått.


## Blandede tekniske ruter

`brink-kontroll-del13/mixed-costume016_483-evidence.json` viser en originalrute med to ekte piksler og ni magentapiksler. Faktisk VERSION2-fallback beholder begge i et80x156-bilde og rapportererok. Vedlagt original og faktisk fallback-PNG. Bevar de to ekte delene og fjern bare den dokumenterte tekniske magentaen ved mottak; ikke utelat hele blandede ruten. Fig016_22 er fortsatt holdt på grunn av et separat feil brystmerke i native.

## Brink-del14: kontrollert importgrunnlag

fig048_05 og fig048_06 er grafikkrevidert. Root har sett original og grå native og kontrollert at publisert rutekart er identisk med kartet brukt i faktisk v2-import mot original-RGBA. 048_05 har 35 tegnede ruter og ett ekte originalfragment, 36 ok; 048_06 har seks tegnede ruter, seks ok. Importbevis ligger i brink-kontroll-del14. Dette er importdiagnostikk, ikke runtime-kontroll av hodeanker eller taleskalering.
