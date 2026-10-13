# Kildetro levering etter r12-kontrollen

Sam & Max-sammenligningen er brukt på de berørte The Dig-familiene. Den endrer kontrollmetoden, ikke spillets malte science fiction-stil.

1. Identifiser objekt og tilstand fra originalens rom, skript, palett og hele relevante hendelse. Kontroller generert stilanker mot kilden før bruk. Tidligere avviste motiver er feilbevis.
2. Behandle en animasjon eller objektfamilie samlet. Gi hver kildecelle en eksplisitt kobling til master, rute, beskjæring og SHA. Et ressursnummer eller en modulooperasjon velger ikke motiv.
3. Behold én felles rommaster ved panorama og én stabil figuridentitet. Kontroller hode/kropp, hånd/redskap og syk/frisk tilstand samlet. Kontroller alle relevante retninger og munnfaser.
4. Små og ensfargede celler utelates bare når de er dokumentert tomme eller tekniske. De 66 smale bryterglimtene i denne runden viste at bredde under fem piksler ikke betyr at grafikken kan fjernes.
5. Skill faseoversikt fra avspilling: eksportens AKCH-ruteliste er deduplisert. Den bevarer ikke repetisjoner, timing eller alle tømminger av lag. Bruk motorens originale AKSQ-avspilling i sekvenskontrollen.
6. Kontroller original og HD i samme virkelige palett og tilstand. En tvunget aktør kan arve shadowMode eller fargesykling fra lagringen. Avklar dette før et bilde tegnes om.
7. Mål geometri og masker, se deretter bildene i motoren og til sist i pakken som leveres. Teknisk pass, visuelt kontrollert kandidat, publisert pakke og Toms godkjenning er forskjellige resultater.

For denne runden er alle originale saves bevart. Sam & Max-repoet er bare lest.

## Bevar rettingene ved neste ombygging

r12 ligger som registrerte runtime-overstyringer i `mod-overrides`, med komplett SHA-manifest. De beskyttede referansene og gamle bestillingsarkene er ikke skrevet om. Den generelle `gpt_runde.sh` importerer ikke denne rapportmappen automatisk. Ved en ny full modbygging må `verktoy/apply-overrides.py /absolutt/sti/til/mods/gpt` kjøres etter standardimporten, og hele moddens sjekksummer og spillkontroll gjentas før publisering. Dette er et eksplisitt leveringssteg, ikke en påstand om at den automatiske pipelinen er oppgradert. Hvis nyere godkjent grafikk bevisst erstatter r12-filer, må manifestet revideres før import, slik at gamle rettinger ikke overskriver nyere arbeid.
