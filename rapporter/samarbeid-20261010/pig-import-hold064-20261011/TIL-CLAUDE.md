# Pig 064: konkret importfeil til Claude

Behold **IMPORT-HOLD 064**. Stabilt `fig007_03` forsøk 2 har kompakt beholder og løs kappe, men mangler originalens fjerne svarte punkt. Faktisk uendret VERSION 2-import er reprodusert pikselidentisk: 888×592, IoU 0.010, dekning 0.079, flytt `[-251,-24]`, skala XY `[2.5876,2.3103]`, klippet figur. Dette er ikke godkjent spillgrafikk.

Originalen 174×134 har 1271 synlige piksler: kropp 1053 px i `[10,6,51,48]`, kappe 216 px i `[0,0,19,15]`, mørk 1 px ved `[54,23]` og fullt opak svart 1 px ved `[173,133]`. Kropp+kap+nærprikk dekker 61×54. Begge punktene er ekte kildeinnhold. Nativekroppen er `[458,70,219,203]`, kappen `[412,41,83,70]`; union 265×232.

`pipeline/dighd/myk.py` VERSION 2 bruker alle synlige kildepiksler til mål og anker:

- Linje 370–389: 064 er egen radgruppe. Fjernpunktet utvider høyden 54→134; gruppeskalaen blir `134*4/232=2.3103448`.
- Linje 243–247: full bredde 174 presser X-fit til `1.12*2.3103448=2.5875862`.
- Linje 278: det isolerte punktets y133 styrer bunnankeret. Søket ±16 px kan ikke rette dette.
- Linje 416: fallback gjelder bare hele ruter under 40 px uten nativekomponenter. 064 har 1271 px og 2 nativekomponenter; ingen fallback er utført. Fjernpunktets forventede eksportboks `[788,560,4,4]` har null piksler med alfa≥128.

Kontroll kun i minnet: å utelate bare fjernpunktet fra målmasken gir skala 0.9310, IoU 0.891, dekning 0.951 og ingen klipping. Bare redusert skala mot den uendrede målmasken gir fortsatt IoU 0.000 fordi bunnankeret blir feil. Den kontrafaktiske masken er merket diagnostisk; den er ikke endret original eller levering.

**Neste kodehandling:** skill full kildecanvas fra komponentene brukt til fitting. Par kropp+kap med native, og beregn mål/anker fra disse. Bevar ekte små kildefragmenter separat på kildeposisjon med eksplisitt proveniens når native mangler dem. Behold full canvas 174×134 og myk nativealfa. Ikke slett små detaljer generelt, strekk kroppen eller mal i native. Verifiser faktisk eksport av 064 og øvrige 17 faser før HOLD oppheves.

Ett avgrenset generatorforsøk på å gjeninnføre punktet ble **avvist**: feil prikkposisjon og nye kontrollstriper. Se `avvist03correction.json`. Stabilt forsøk 2 er uendret og holdes utenfor automatisk mottaksledger. Ingen flere forsøk.

Proveniens (SHA256):

- Kodecommit `36cd09f13eb0201cff190d8d0c99c788a8bcaa6b`; myk.py `7cb20ae673d0576a0f51ecc62f18a289c9c3f1e5b79cff6b9b0cd521f44b6176` (bytekontrollert mot commit).
- Original `b2a9b5740d560221e473d19f466ac31c4baf34057695edc0b8605cd4e88d2f2e`: `/home/tombonator3000t/.codex/tasks/the-dig-romlag-brink-20261010/extract-nyordre/costumes/costume007_064.png`.
- Native `03a44bb00993f6682721fbbded92701c7ff8f93309f56925ee198966e3a1d61e`: `/home/tombonator3000t/.codex/tasks/the-dig-romlag-brink-20261010/pig-serie-godkjent-20261011/agent01/fig007_03-attempt2-native.png`.
- Faktisk import `65c4c81ba589d50c3ee96ec85a3637d9a6f631c9f0a4a1796a47b29cf4c0e2b4`: `/home/tombonator3000t/.codex/tasks/the-dig-romlag-brink-20261010/pig-serie-godkjent-20261011/isolert-import/fig007_03-03a44bb00993/costumes/costume007_064_hd.png`.

Detaljer og fullstendige målinger: `/home/tombonator3000t/.codex/tasks/the-dig-romlag-brink-20261010/pig-serie-godkjent-20261011/agent01/diagnose.json`. Visuell diagnose: `/home/tombonator3000t/.codex/tasks/the-dig-romlag-brink-20261010/pig-serie-godkjent-20261011/agent01/064-importdiagnose.png`. Lesende reproduksjon: `/home/tombonator3000t/.codex/tasks/the-dig-romlag-brink-20261010/pig-serie-godkjent-20261011/agent01/diagnose064.py` med Python 3/numpy/scipy/Pillow. Ingen repo-, original-, native- eller masterendring. Runtime er ikke testet.


Nativekandidaten i denne mappen er HOLD og står ikke i automatisk mottaksledger. Den er byteidentisk med generatoroutput, ikke en original eller ferdig spillimport. Hele serien produseres fortsatt; se ../TIL-CLAUDE.md. Ingen kodeendring er gjort av Codex.
