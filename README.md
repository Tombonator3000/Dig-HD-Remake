# The Dig HD r12

Komplett HD-mod fra r11 med de kontrollerte r12-rettingene. Krever motorrettingene fra PR #51.

Produksjon, kildegrunnlag, metodeanalyse og kontroll: grafikkgrenen gpt-arbeid, rapporter/spillfeil-r12-20261013.

Dette er en integrert og teknisk kontrollert leveranse. Hele spillet er ikke gjennomspilt, og Toms visuelle godkjenning av alle nye bilder gjenstår.

## Komprimert HD-intro, SQ1

`san/SQ1.ivf` inneholder hele oppstartsintroen: 3772 bilder i 1280 x 800, 12 bilder per sekund, 5 minutter og 14,33 sekunder. AnimeSR v2, deretter VP8-komprimering til 22,78 MB i stedet for 4,27 GB med PNG-mastere (99,47 prosent mindre).

Krever motoren med komprimert HD-video og libvpx. Original `VIDEO/SQ1.SAN` og spillets lydfiler må fortsatt være tilgjengelige; de styrer timing, lyd og undertekster. Videoen har bare bildeflaten. Motoren viser riktig 4:3-sideforhold og faller tilbake til PNG eller originalbildet hvis videoen mangler eller feiler. Ingen andre publiserte bilder er endret. Produksjonsdata og sjekksummer: `san/SQ1.json` og `SHA256SUMS`.

Kontrollert: alle 3772 videobilder dekodes, hele introen kjørt i Linux-motoren uten skjerm, tekst tegnes over HD-bildene, bytte til/fra klassisk grafikk og avbrudd med Escape. Full visuell godkjenning i bevegelse og kontroll på Windows/mobil gjenstår.
