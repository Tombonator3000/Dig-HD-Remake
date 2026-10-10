# Lag026 stabil HOLD

Jobb: `lag026_03_del2av3`. Ett nytt kildebundet lokalt forsøk, nr. 7. Ingen ekstra retting fordi flere samtidige form- og plasseringsfeil gjenstår. Kandidaten er ikke levert eller spilltestet.

## Native og kontroll

- Native: `/home/tombonator3000t/.codex/generated_images/01a125af-b7da-7411-85ba-a0097552f497/exec-b7eda0b0-27c3-48da-be67-2b4b4fb136f4.png`
- SHA256: `ce62f5f45dfeb8680949fb0778e0787c2d81cb4e574c5a132b2925d9eda23fc7`
- Byteidentisk sikkerhetskopi: `/home/tombonator3000t/.codex/tasks/the-dig-romlag-brink-20261010/agent-lag026-rootnext/held-native-attempt7.png`
- Verktøy: innebygd ChatGPT imagegen. Eksakt modellversjon er ikke eksponert.
- Fryst QA: uendret main `4cff08145f0760d9e7765bcec6f6c9a371e196bb`, gpt.py SHA256 `e929e066bc0331e3763de41ff3463e1e1859e01b1a6966f8591561d27969780e`.
- QA: avvist, obj227 kantlikhet -0.231. Obj224/226 gir null og er derfor ikke bekreftet riktige. Helrommets kantlikhet er 0.902, blokkavvik 0.67; dette overstyrer ikke objektavviket.

## Fysisk kildekontroll

Flere samtidige mekanismeavvik etter den ene avgrensede kildebundne rettingen: avrundede neonstolper erstatter kildens flate blå tilstandsflater, antall og x-plassering av synlige flater er feil, original blåflate for obj226 og obj227 mangler ved faktisk kildested. Obj224 er en enkelt rett stolpe fremfor kildens kontiguous trappede flate med to lysere nedre striper. Obj227-utklippet viser én forskjøvet stolpe fremfor både den ekte objektflaten og romstripen bak transparent område.

Den beskyttede kildekompositten er byte for byte lik originalt rom026 pluss de tre faktiske RGBA-objektene på deres oppgitte plasseringer. Den avviker fra rommet på nøyaktig 42 piksler, lik 13 + 13 + 16 opake objektpiksler. Dette er blå tilstandsflater, ikke tre komplette nye mekaniske tapper. De to ekstra blå formene til høyre er ekte romgrafikk. Objekt227s andre synlige blå stripe ligger i transparent område av objektet og må ikke fjernes. Rektanglene for 224 og 226 overlapper, men de opake kildeflatene overlapper ikke.

Faktisk kildegeometri på 1536-lerretet:

| Objekt | Opake kildepiksler | Opak totalboks, x0 y0 x1 y1 |
|---|---:|---|
| obj224_01 | 13 | 776 764 792 780 |
| obj226_01 | 13 | 756 756 768 776 |
| obj227_01 | 16 | 800 752 812 780 |

Full original, godkjent rom, begge nativebilder, faktisk RGBA, urørt kildeutsnitt, alle tre nøyaktige objektutklipp og QA-visning er sett fysisk. `attempt7-descriptive-blue-source-footprint.json` gir en supplerende fargebeskrivelse fra faktiske originalpalettgrenser, ingen godkjenningsterskel. Ingen native-piksler eller alfa er endret; utsnitt/annotasjoner er bare diagnostikk.

## Neste handling til Claude

Behold originale obj224_01/obj226_01/obj227_01 som fallback frem til korrekte HD-tilstander foreligger. Kontroller den opake flaten for hver tilstand separat fra romgrafikk som ligger bak transparent område, og ta hensyn til overlappende rektangler 224/226. En helromskontroll eller null objektresultat bekrefter ikke disse små tilstandene. Ingen ny produksjonsløkke er startet.

Alle fire beskyttede kildefiler er uendret. Full prompt med ordrett kildeprefiks, referansestier og SHA, faktisk original-RGBA med SHA, native og all QA ligger ved `manifest.json`. Felles leveranser, fremdrift, kode, statusfiler og Git er ikke endret.
