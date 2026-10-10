# Konkret importspor for hodepuls

Faktisk VERSION2 bruker ulik anisotrop høydefaktor på tre munnfaser i fig016_37. Original059 er8x12;060 og061 er8x13. Alle tre nativehoder er68piksler høye. Felles gruppeskala er0.7164, men place_fitted godtar Y0.7059 for059 og0.7647 for060/061. Det strekker hele hodet8,33prosent mellom fasene. De faktiske originalene har ingen magenta, så dette tilfellet er uavhengig av den allerede dokumenterte magenta-ankerfeilen.

Root har kontrollert kilde-PNG, importverdier og at diagnostikkens myk.py er byteidentisk med origin/main. fit_scales ved linje236 bruker originalens hele synlige boks; place_fitted ved linje250 og importanropet ved linje412 tillater per-rute-tilpasning selv om en gruppeskala finnes. Vurder stabil hodegeometri og gruppeankere på tvers av munnfaser, og verifiser faktisk animasjon etter kodeendring. Ikke endre originalatferd eller maskere vekk ekte kildedeler.

Dette er reprodusert importdiagnostikk, ikke motorvideo eller bevis for eneste årsak. Selve fig016_37 er fortsatt holdt for et separat feiltegnet buksesår. Ingen kodeendring er utført av grafikkagentene.
