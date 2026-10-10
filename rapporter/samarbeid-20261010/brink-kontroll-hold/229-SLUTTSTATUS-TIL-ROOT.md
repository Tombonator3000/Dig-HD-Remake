# Kostyme 229 – status til root

Alle 22 ark har avgrensede forsøk. De 40 nativeforsøkene er bevart med SHA, faktiske referanser og ordrett promptprefiks. De fire beskyttede filene er kontrollert uendret for alle 22 jobber. Underagenten har ikke skrevet i fellesrepo, Git, leveranser, motor eller fremdrift.

Fem ark er tidligere publisert av root: 01, 02, 08, 11 og 12. Dette er historisk levering. Root retter nå buksedetaljen i 08; bare donorens overkropp kan brukes som fysisk stilreferanse. Ark 18, forsøk 2, er til roots endelige kontroll av høyde og utseende. De 16 øvrige arkene er HOLD.

| Ark | Siste forsøk | Status | Faktisk import av siste forsøk | SHA |
|---|---:|---|---|---|
| fig229_01 | 3 | historisk publisert av root | {"ok": 4} | b3b25af37e53 |
| fig229_02 | 3 | historisk publisert av root | {"ok": 4} | 5495810c8977 |
| fig229_03 | 5 | HOLD | Ikke utført på visuelt avvist kandidat | 2c8d0fac9445 |
| fig229_04 | 2 | HOLD | Ikke utført på visuelt avvist kandidat | 6f2ce4f7c3e7 |
| fig229_05 | 3 | HOLD | Ikke utført på visuelt avvist kandidat | 833b38ab3ebd |
| fig229_06 | 2 | HOLD | Ikke utført på visuelt avvist kandidat | 96acbbd74978 |
| fig229_07 | 3 | HOLD | {"sjekk": 2, "ok": 3} | b1a66424b972 |
| fig229_08 | 1 | historisk publisert av root; root retter buksedetalj | {"ok": 4} | fb01557d321c |
| fig229_09 | 1 | HOLD | Ikke utført på visuelt avvist kandidat | d1447a1b9979 |
| fig229_10 | 1 | HOLD | Ikke utført på visuelt avvist kandidat | b22c4418a7fb |
| fig229_11 | 1 | historisk publisert av root | {"ok": 5} | 57cbafb1be60 |
| fig229_12 | 1 | historisk publisert av root | {"ok": 20} | 82f61c648c74 |
| fig229_13 | 1 | HOLD | Ikke utført på visuelt avvist kandidat | 2135a745287e |
| fig229_14 | 1 | HOLD | Ikke utført på visuelt avvist kandidat | e4a2f40dd989 |
| fig229_15 | 1 | HOLD | Ikke utført på visuelt avvist kandidat | d05247f70337 |
| fig229_16 | 2 | HOLD | Ikke utført på visuelt avvist kandidat | 114c70618e30 |
| fig229_17 | 2 | HOLD | Ikke utført på visuelt avvist kandidat | 48a0ac599453 |
| fig229_18 | 2 | root vurderer forsøk 2; egen READY ikke satt | {"ok": 13} | 38fe7d02fd62 |
| fig229_19 | 1 | HOLD | {"ok": 4} | d5a0290b0e99 |
| fig229_20 | 2 | HOLD | Ikke utført på visuelt avvist kandidat | 330f4b6a64ff |
| fig229_21 | 1 | HOLD | Ikke utført på visuelt avvist kandidat | 456fd17cab64 |
| fig229_22 | 1 | HOLD | {"ok": 5, "sjekk": 1} | d6e61baf498a |

Den gamle pakken `batch-16-18-til-root.*` er historikk og skal ikke leveres. Lokalretting av 16 la merker på Boston og endret effektalfa. Lokalretting av 17 fjernet ekte fasegrenser. Lokalretting av 20 skalerte og flyttet hele komposittene. Disse rettingene er avvist etter ett forsøk hver; utgangskandidatene er bevart. Ark 21 holdes for feil lårform. Ark 22 holdes for en tettere siste fadingfase og endret komponentform i 119; faktisk import ga fem ok og én sjekk i 120, mens ekte fallback 121 var ok.

Ark 18, forsøk 2, er vurderbart: 13 faktiske importer er ok, og alle 22 nativekomponenter er mappet én gang. Arket har 12 hovedruter i radene [5,4,3], samt ekte originalfragment 098. Rosefargen i lårfeltet er forbedret; mørk rand er fortsatt tydelig. Resten er ikke pikselidentisk: core-IoU utenfor feltene er 0,97995 og gjennomsnittlig RGB-avvik er 9,23. Root har sett alle 13 kilde-/importpar og vurdert rose og størrelse som akseptabelt med eksplisitt begrensning om randen. Endelig høydekontroll gjenstår; ingen videre retting av 18.

Aktuelle bevis:

- `fig229_18-attempt2-root-review.json` peker på stabil spesifikasjon, QA, 13 faktiske importer og kart med identiske testede bokser.
- `fig229_18-thigh-original-native-evidence.json` og `.png` viser originalenes 3×5-felt og nøyaktige 1×3-lysstripe, RGBA [183,103,75,255].
- `fig229_18-attempt2-edit-preservation-diagnostic.json`, fire `thigh-XXX-8x.png` og seks `import-contact-part*.png` viser lokalrettingen.
- `fig229_19-root-export-measurement-addendum.json` dokumenterer roots direkte eksporthøyder 269, 252, 271 og 294 px: 16,7 % spenn ved uendret kildehøyde på 264 px. Dette skal ikke kompenseres ved å male eller krympe hodet.
- `fig229_22-component-source-native-evidence.json` og tre importpaneler viser avvikene i siste fase, selv om antall og alfa er teknisk kontrollert.

`229-sluttstatus.json` inneholder alle 22 arkenes siste SHA, stier, QA, faktiske importstatus, klassifiserte kilder og årsaker til HOLD. Alle forsøk, referanser og originaler er beholdt. Ingen bekreftet Claude-kvittering eller motor-/spilltest foreligger.
