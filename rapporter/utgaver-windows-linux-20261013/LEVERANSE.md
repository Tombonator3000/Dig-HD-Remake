# Windows- og Linux-utgaver, 13. oktober 2026

Tom ba om å slette gamle testprogrammer på Kubuntu, levere Windows og Linux fra repoet og beholde kun nyeste Linux-bygg. Arbeidet er avgrenset til The Dig HD.

## Nedlasting

- [Windows x64 ZIP, r10](https://github.com/Tombonator3000/Dig-HD-Remake/releases/download/windows/TheDigHD-Windows-x64.zip), 1 525 275 123 byte. Pakk ut hele filen og dobbeltklikk `Start The Dig HD.cmd`.
- [Linux x86_64 AppImage, r10](https://github.com/Tombonator3000/Dig-HD-Remake/releases/download/linux/TheDigHD-x86_64.AppImage), 1 485 552 120 byte. Gjør filen kjørbar og start den.
- [Motorens komplette kildekode](https://github.com/Tombonator3000/Dig-HD-Remake/releases/download/windows/TheDigHD-r10-engine-source.tar.gz), inkludert byggeskript og kildefingeravtrykk.

Windows SHA256: `16ddceec8ec3eb49caba1d224b9a3bff7a05f39c1e0662ae4a88e1f77c756a2a`.

Linux SHA256: `d8769b180ee9c8acf532de03b36d2058f19badd3b7383d56d66323a26fc6ed68`.

Begge er publisert. Offentlige nedlastingsadresser svarte HTTP 200 med riktig størrelse; offentlige sjekksumfiler og GitHubs asset-digester samsvarer med lokale filer. Linux r10 var allerede siste rettede pakke og er beholdt uendret.

## Windows-pakken og kontroll

Motoren er kompilert som et Windows x64-program fra samme ScummVM-kildegrunnlag som Linux r10. 411 kildefiler i SCUMM-delen er hashkontrollert mot den eksisterende motorens kilde. Alle 25 445 spill- og HD-modfiler er identiske med faktisk r10-AppImage. SDL2 og MinGW-trådbiblioteket følger med; PNG og zlib er lenket inn. Lisensfiler følger pakken.

Seks tester via Windows-startfilen i Wine 10 på Kubuntu bestod: rom 22, 32, 50, 88 og de to utvalgte rom32-objektene. 32 tegnekontroller ga null avvik. De to objektene ble bekreftet tegnet med HD-bilder. Rom 22 ved bilde 100 er pikselidentisk på Linux og Windows.

ZIP-filen bestod CRC-kontroll og SHA256-kontroll av alle 25 559 utpakkede innholdsfiler. Den faktiske utpakkede pakken startet fra en mappe med mellomrom, opprettet nye innstillinger og kjørte med standard grafikkvalg: tre nye tegnekontroller uten avvik. Ingen manglende tale-/musikkbundle ble rapportert. Windows-innstillinger og lagrede spill ligger i `%APPDATA%\TheDigHD`.

Den faktiske Linux-AppImage bestod en ny oppstartstest med fem tegnekontroller uten avvik etter oppryddingen. Brukerens fire lagringsfiler ble kontrollert og bevart under slettingen.

## Opprydding

- Tolv stier til eldre AppImage-filer, syv eldre skrivebordssnarveier og syv foreldede skrivebordssjekksummer er fjernet. Den siste r2-hardlenken lå i en egen publiseringsmappe og er også slettet.
- Den gamle utpakkede testmappen på skrivebordet, med 25 636 filer, og r2-les-meg-filen er fjernet. Kildepatcher og leveransebevis er bevart i Windows-pakken og eksisterende rapporter.
- Omtrent 12.02 GB eldre pakker og testmappe er fjernet. Hardlenker er regnet én gang. Ny Windows-ZIP, motorens kildearkiv og kontrollbevis beholdes lokalt; midlertidige bygg-, Wine- og utpakkingsmapper fra denne kjøringen er ryddet.
- 24 eldre repo-assets, inkludert ni AppImage-versjoner, er slettet. Linux-utgivelsen har nå bare r10-AppImage, gjeldende sjekksum og gjeldende les-meg-fil.
- En forsinket planlagt Linux-jobb, `38376147504`, ble kansellert før publisering fordi den ville erstattet r10 med samme eldre hd-mod-grunnlag. Utgivelsesteksten har nå markøren nattjobben bruker for å hoppe over dette grunnlaget. Arbeidsflyten er fortsatt aktiv.

Bare rapportmappen og denne øktens loggoppføring committes i `gpt-arbeid`. Lokalt grafikkarbeid, referanser, kildecheckout-er og andre spill er bevart.

## Begrensninger

Windows er testet via Wine, ikke på en fysisk Windows-PC. Full gjennomspilling og ny visuell godkjenning fra Tom er ikke utført. PIG-/plukkegrafikkpunktene i TODO står fortsatt åpne. Dette er r10-pakking, ikke nye grafikkrettinger.

Detaljer ligger i JSON-rapportene i denne mappen. Hjelpeskriptene viser denne kjøringens fremgangsmåte; midlertidige mapper er ryddet og finnes ikke lenger.
