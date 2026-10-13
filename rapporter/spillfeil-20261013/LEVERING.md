# r11, 13. oktober 2026

1157 HD-ruter er korrigert/komplettert, og motorfeilene i inventory og luftsluse er rettet. PR49 er flettet etter grønne CI-tester. De to dørene i bilde3/4 går til ulike transportrom i originalen; forbindelsene er beholdt.

Windows x64 er kompilert fra samme låste ScummVM-kilde. Seks målscener gjennom Windows-programmet og startfilen, og en ekstra kjøring av den faktisk utpakkede ZIP-pakken, er bestått gjennom Wine10 på Kubuntu. 2314 endrede grafikkfiler er sjekksumidentiske i grafikkgrenen, Linux-staging og Windows-ZIP. Fysisk Windows er ikke testet.

Native Kubuntu-pakke er testet, men krever glibc2.43. Den generelle Linux-nedlastingen bygges derfor gjennom repoets eksisterende Ubuntu22.04-arbeidsflyt med den komplette r11-modden, og kontrolleres separat. Denne forskjellen er registrert før offentlig r11-Linux-levering.

Originale lagringer og urelaterte arbeidsfiler er bevart. Toms lagring5 er kopiert for testing. Tidligere opprydding fjernet de gamle godkjente testbyggene; aktivt spill blir ikke avsluttet av denne oppgaven.

Dette er teknisk QA og kandidatgjennomgang av de berørte scenene, ikke en full gjennomspilling eller Toms endelige visuelle godkjenning.

Den første Ubuntu22.04-byggingen startet før hele mod-opplastingen var ferdig og brukte derfor gammel mod. Dette bygget er forkastet som r11-levering. PR50 låser mod-SHA ved byggestart; direkte hentetest av113523ba12fd10fbf2a9ff49b3823cd9aa8095c6 har verifisert hele SHA256SUMS og alle2314endrede filer. Den nye byggingen kontrolleres etterpå.
