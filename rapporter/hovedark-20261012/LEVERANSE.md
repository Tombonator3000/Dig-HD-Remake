# Fire hovedark til visuell godkjenning

12. oktober 2026. Arbeid etter ORDRE.md og den oppdaterte scumm-hd-remake-skillen.

[Samlet oversikt](OVERSIKT.png). [Alfakontroll på lys, mørk og grønn bakgrunn](KONTROLL-LYS-MORK-GRONN.png).

| Hovedark | Innhold | Status |
| --- | --- | --- |
| [Boston](../../hovedark/boston.png) | Forfra, profil og bakfra i planetklær og EVA-drakt, samt ansiktsnærbilde | Kandidat til Toms godkjenning |
| [Maggie](../../hovedark/maggie.png) | Samme visninger, egen identitet og kildebestemt kjeledress | Kandidat til Toms godkjenning |
| [Brink](../../hovedark/brink.png) | Frisk normalvariant, grå jakke og blondt hår; samme visninger | Kandidat til Toms godkjenning |
| [Robotarm](../../hovedark/robotarm.png) | To kildestyrte sammenstillinger og fire komponentstudier | Kandidat til Toms godkjenning |

Alle fire er generatorens native RGBA-PNG på 1536 x 1024. Filene er kopiert byteidentisk, uten retusjering, restalfasletting eller originalmasker. Verktøyet bekrefter ikke eksakt modellnavn. Åtte bildekall, inkludert retting av bakgrunnsalfa, oppfunnet Brink-emblem og ulikt manøvreringsutstyr. Se [manifestet](leveranse.json), [kildeanalysen](ANALYSE.md) og promptene i `prompter/`.

## Utført kontroll

- Originale kostymer, konseptene og godkjent Boston-/Brink-stil er sammenlignet visuelt med kandidatene. Maggie-konseptet brukes som identitetsgrunnlag, ikke det eldre uavklart godkjente genererte ankeret.
- Hver person har sitt eget ansikt og hår i begge drakter. Hode og kropp ses samlet på hovedarket. Normal Brink holdes adskilt fra skadet, død eller gjenopplivet variant.
- Samlekontrollen fant ulikt MMU-utstyr. Maggie og Brink ble korrigert mot samme front-/bakkonstruksjon som Boston. Perspektivforkorting, små sømdetaljer og det virkelige utstyrets kontaktpunkter må fortsatt sjekkes mot hver originalrute ved animasjonsproduksjon. Hovedarkene er ikke presise tekniske konstruksjonstegninger.
- Robotarmen er sammenlignet med originalark fra kostyme004/005 og rom002. Åpen ramme, lyse lange seksjoner, gul bøyle, kabel og rødt merke er bevart. Hele armens mekaniske kontakt mellom spritebitene må kontrolleres i motoren når animasjonene tegnes på nytt.
- Faktisk alfakomposisjon er sett på hvit, mørk og grønn bakgrunn. RGBA, bildestørrelse, transparent bakgrunn og byteidentisk native-kopi er målt. Alfaens maksimum er254 i native-filene og er bevart. Farget RGB under null alfa er ikke synlig i korrekt komposisjon.
- Beskyttede kildefiler og tidligere lokale arbeidsfiler kontrolleres mot [grunnlag.json](grunnlag.json); resultatet føres i [filkontroll.json](filkontroll.json).

## Gjenstående godkjenning og produksjon

ORDRE.md sier: «Tom godkjenner hovedarkene. Etterpå legges riktig hovedark ved som bilde to i alle nye figurark for den personen eller gjenstanden». Hovedarkene er derfor ikke aktivert som godkjente produksjonsankere. Tom er bedt om konkret visuell vurdering av disse fire filene.

Neste avhengige steg etter godkjenning: tegn robotarmens kostyme004/005 på nytt med godkjent hovedark, følg de aktuelle originalrutene og før eksplisitte rutekart. Videre personkostymer bruker riktig godkjent personark. Eksisterende PIG-grafikk og Toms nyere PIG-feilrapport er bevart.

Ingen nye animasjonsruter er importert, ingen motor er endret og ingen ny spillpakke er bygget. Hovedarkene teller ikke som ferdige HD-cels og endrer ikke sprite-fremdrift eller Claudes kontrollfiler. Hele HD-prosjektet er fortsatt uferdig. Faktisk animasjon, hode/kropp i motoren og pakkekontroll gjenstår for de senere avledede arkene.

Arbeidslogg: samtaler og repo kontrollert, gjeldende regler hentet til gpt-arbeid, motivanalyse utført, fire manglende hovedark laget og revidert, native-filer og proveniens lagret. Kun denne leveransens filer inngår i grafikkcommiten.
