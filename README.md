# The Dig HD r12

Komplett HD-mod fra r11 med de kontrollerte r12-rettingene. Krever motorrettingene fra PR #51.

Produksjon, kildegrunnlag, metodeanalyse og kontroll: grafikkgrenen gpt-arbeid, rapporter/spillfeil-r12-20261013.

Dette er en integrert og teknisk kontrollert leveranse. Hele spillet er ikke gjennomspilt, og Toms visuelle godkjenning av alle nye bilder gjenstår.

## Komprimert HD-intro, SQ1

`san/SQ1.ivf` inneholder hele oppstartsintroen: 3772 bilder i 1280 x 800, 12 bilder per sekund, 5 minutter og 14,33 sekunder. AnimeSR v2, deretter VP8-komprimering til 22,78 MB i stedet for 4,27 GB med PNG-mastere (99,47 prosent mindre).

Krever motoren med komprimert HD-video og libvpx (Dig-HD-Remake PR #59, nettleser PR Dig-HD-Web #4). Original `VIDEO/SQ1.SAN` og spillets lydfiler må fortsatt være tilgjengelige; de styrer timing, lyd og undertekster. Videoen har bare bildeflaten. Visningen følger motorens eksisterende HD-flate. Motoren faller tilbake til PNG eller originalbildet hvis videoen mangler eller feiler. Ingen andre publiserte bilder er endret. Produksjonsdata og sjekksummer: `san/SQ1.json` og `SHA256SUMS`.

Kontrollert: alle 3772 videobilder dekodes, hele introen kjørt i Linux-motoren uten skjerm, tekst tegnes over HD-bildene, bytte til/fra klassisk grafikk og avbrudd med Escape. Full visuell godkjenning i bevegelse og kontroll på Windows/mobil gjenstår.

## Resten av HD-filmene, 16. oktober 2026

Alle de resterende 54 SAN-filene er behandlet i nummerrekkefølge fra SQ2, deretter de navngitte spillsekvensene. De gir 8866 nye rammer i 1280 x 800 og 86.66 MB komprimert VP8-video. Sammen med SQ1 finnes nå alle 55 filmer og 12 638 rammer, 109.43 MB video i alt. Ingen PNG-videorammer er lagt til.

SQ3 beholder 14 fps, SQ19A 15 fps; øvrige filmer er 12 fps. SQ14SC07 har en tom første SAN-ramme som er bevart uten å forskyve de 32 bildene etter den. Motoren følger fortsatt SAN-rammenummeret og original lyd, tekst og skript. Den tidligere godkjente SQ5-masteren og den publiserte SQ1-filen er beholdt.

Alle nye filmer er dekodet i sin helhet, og dimensjoner, antall, tidsstempler og komprimering er kontrollert. Sju effektsekvenser fikk høyere bitrate for å nå SSIM minst 0,98 mot AnimeSR-masteren. Ett original/HD-bilde per film er sett på; full visuell kontroll i bevegelse og i alle spilltilstander gjenstår. Rapport og produksjonsrekkefølge: `san/VIDEO-HD.json`; hver film har egen JSON og SHA-256 i `SHA256SUMS`. Alle tidligere publiserte grafikkfiler er bevart.

Runde 2026-10-16 10:15 UTC: 0 nye enheter, 2194 erstattet og 0 fjernet (runder i mod.json).

16. oktober: r16-rettingene fra rapporter/spillfeil-20261016 er integrert etter Toms bestilling. 2223 grafikkfiler registrert; alle 55 publiserte HD-filmer beholdes. Motorpatch0006 kreves.

Runde 2026-10-16 11:39 UTC: 661 nye enheter, 88 erstattet og 0 fjernet (runder i mod.json).

16. oktober: r17 retter øvrige krystallåser, fjernvann, dowel og scepter-ikoner. Alle r16-rettinger og55 HD-filmer bevart. Full gjennomspilling og Toms visuelle godkjenning av alle nye ruter gjenstår.
