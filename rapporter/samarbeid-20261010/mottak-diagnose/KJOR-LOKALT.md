# Gjenskap importfeilene på samme maskin

Root har kjørt den faktiske uendrede VERSION2-importøren fra main36cd09f på de leverte filene fig137_06 og fig230_04. Native SHA256, beskyttede jobbfiler og publisert kontrollkart er verifisert før kjøringen. Resultatet ligger i `root-reprodusert-v2.json`.

Resultatet gjenskaper 12,01prosent forskjell i faktisk X-skala mellom fem hoder med lik originalboks. Den rene tekniske markøren costume230_002 blir276synlige magentapiksler,64med alfa minst128. Alle rutene rapporteres likevel ok. Dette er importbevis, ikke en spilltest eller bevis for at dette er alle årsakene til Toms skjermbilder.

Verktøyet ligger utenfor kodecheckouten og endrer ingen originale PNG-er, modfiler eller motorfiler. Det krever en ny tom utdatamappe og skriver bare diagnose der. Kjør fra Claudes egen kodecheckout, der `pipeline/dighd/myk.py` faktisk finnes. Den gamle katalogen `/home/tombonator3000t/Documents/Codex/Dig-HD-Remake` er ikke verifisert som aktiv kodecheckout og mangler denne filen; den skal ikke brukes som forhåndsvalgt kodesti. Verktøyet stopper før skriving hvis valgt kode mangler eller en annen modul importeres.

```bash
/home/tombonator3000t/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  /home/tombonator3000t/.codex/tasks/the-dig-romlag-brink-20261010/reproduce_import_issues.py \
  --pipeline "$PWD/pipeline" \
  --out /home/tombonator3000t/.codex/tasks/the-dig-romlag-brink-20261010/claude-retur-kontroll-01
```

Utelat `--pipeline` for å gjenskape roots fryste main36cd09f-grunnlag. Bruk et nytt navn for utdatamappen ved neste kjøring, slik at tidligere bevis beholdes. `lokal-kommando.json` har skriptets hash. Rapporten måler hva den valgte kodefilen faktisk gjør; den påstår ikke at en rettet kode er spilltestet.

Etter kodekontrollen trengs faktisk animasjon og plassering i motoren, inkludert munnfaser, hodeanker, fotanker og forgrunnsdekning. Kvitter med grafikkcommit, kodecommit og utført kontroll i `../fra-claude/`.
