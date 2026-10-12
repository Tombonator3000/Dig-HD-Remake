# HD-sjekkliste for The Dig

Kontrollgrunnlag: Linux 20261013-r10, kontrollert mot faktisk AppImage og jobbfilene 13. oktober 2026. R9s øvrige ressurser er uendret; rom 32 er rettet og testet på nytt i r10. Opprinnelig restansetelling er fra r8. Sjekklisten skal oppdateres med leveransereferanse når et punkt er utført. En resultatfil er ikke det samme som godkjent og integrert grafikk.

## Overordnet dekning

- [x] Alle 106 rombakgrunner følger med i r8.
- [x] Alle 149 inventarikoner følger med i r8. Dette beviser ikke at hele plukkeforløpet er kontrollert.
- [x] Alle 15 krystalltilstander i rom 50 følger med og er runtime-kontrollert i r8. Se rapporter/krystaller-rod-20261012/LEVERANSE.md.
- [ ] Figurer og animasjoner: ved denne tellingen har 1297 av 4032 bestilte figurark resultatfil. 2735 har ingen resultatfil. Tallene omfatter også fragmenter og tekniske lag; motiv og faktisk behov må vurderes før nytegning.
- [x] Små romobjekter: de 20 manglende lagjobbene er levert og 31 objektbilder er integrert i r9. Alle 236 lagjobber har nå resultatfil. Brukerens visuelle KS føres separat nedenfor.
- [ ] SAN-mellomsekvenser: ingen HD-filmrammer i r8. Egen senere bestilling, ikke del av denne runden.
- [ ] PIG: samme konstruksjon gjennom hele serien må kontrolleres og rettes mot nyeste formfasit. Se TODO.md og rapporter/feilrapport-20261012/.
- [ ] Plukkegrafikk: kontroller gjenstand i rom, markering, plukking, peker, inventar og bruk som én sammenhengende kjede.
- [x] Gullstaven i rod-nærbildet: ny glatt stav/hånd og korrigert grunnpalett i r9. Alle tre obj884-tilstander er kontrollert i AppImage.
- [ ] Gullstaven: brukerens visuelle KS og godkjenning av r9/r10.
- [x] Rom 32: søylemotivet rettet til inngravering i stein, uten dusj, utstikkende armatur eller vannstråle. Romanker og syv lagkontekster er rettet. Åtte tester og 16 opptegningskontroller i faktisk r10-AppImage er bestått.
- [ ] Rom 32: brukerens visuelle KS og godkjenning av r10. Se rapporter/rom032-inngravering-20261013/LEVERANSE.md.

## Bestilt nå: små romobjekter

Før teknisk avkryssing: kilde/motiv avklart, råtegninger lagret, plassering og tilstander kontrollert, importert i faktisk pakke og sett i avgrenset romtest. R9 ble levert med fire tekniske atlas med separat genererte detaljer; se DETAIL-ATLAS.json. I r10 er alle syv rom32-lag oppdatert til tekniske atlas med korrigert romanker og uendrede HD-objekter. Samlet er ni av de 20 nåværende jobblerretene tekniske atlas. Se rapporter/rom032-inngravering-20261013/LAYER-CONTEXTS.json. Kolonnene skiller tegning fra integrasjon og kontroll.

| Jobb | Rom | Objektbilder | Grafikk levert | Importert | Romtest i AppImage | Bruker-KS |
| --- | --- | --- | --- | --- | --- | --- |
| lag023_03_del3av6 | 23 | obj178_02, obj179_03 | [x] | [x] | [x] | [ ] |
| lag025_01_del1av3 | 25 | obj217_01, obj218_01, obj219_01 | [x] | [x] | [x] | [ ] |
| lag026_03_del2av3 | 26 | obj224_01, obj226_01, obj227_01 | [x] | [x] | [x] | [ ] |
| lag027_03_del2av8 | 27 | obj231_02 | [x] | [x] | [x] | [ ] |
| lag032_01 | 32 | obj256_01 | [x] | [x] | [x] | [ ] |
| lag032_02 | 32 | obj256_02 | [x] | [x] | [x] | [ ] |
| lag032_03 | 32 | obj256_03 | [x] | [x] | [x] | [ ] |
| lag032_04 | 32 | obj256_04 | [x] | [x] | [x] | [ ] |
| lag032_05 | 32 | obj257_01 | [x] | [x] | [x] | [ ] |
| lag032_06 | 32 | obj256_05 | [x] | [x] | [x] | [ ] |
| lag032_07 | 32 | obj257_02 | [x] | [x] | [x] | [ ] |
| lag077_01 | 77 | obj525_01, obj527_01, obj529_01 | [x] | [x] | [x] | [ ] |
| lag077_02 | 77 | obj530_01, obj531_01 | [x] | [x] | [x] | [ ] |
| lag077_03 | 77 | obj532_01 | [x] | [x] | [x] | [ ] |
| lag077_04 | 77 | obj533_01 | [x] | [x] | [x] | [ ] |
| lag088_01_del7av9 | 88 | obj579_01, obj581_01 | [x] | [x] | [x] | [ ] |
| lag088_02_del7av9 | 88 | obj582_01 | [x] | [x] | [x] | [ ] |
| lag088_03_del7av9 | 88 | obj585_01 | [x] | [x] | [x] | [ ] |
| lag088_04_del7av9 | 88 | obj587_01 | [x] | [x] | [x] | [ ] |
| lag090_01 | 90 | obj593_01, obj594_01, obj595_01 | [x] | [x] | [x] | [ ] |

31 objektoppføringer inngår i de 20 jobbene. Bevar øvrige r8-ressurser. Detaljer, kildehasher, prompter og resultater føres i rapporter/smarom-gullstav-20261012/.

Ekstra visuell KS: lag027_03_del2av8, lag032_05 og lag032_07. Automatiske kontrollutslag er bevart og begrunnet i notat.md. De to lag032-jobbene inneholder adskilte bakgrunns-/fossilstriper og bør kontrolleres i den normale gåterekken, ikke bare som tvangsatte enkeltobjekter. Ingen bruker-KS er automatisk krysset av. Se rapporter/smarom-gullstav-20261012/LEVERANSE.md.
