# Integrasjon av r20 og r21, 18. oktober 2026

PR67 er flettet til hd-mod29cff6583dc45ec21bcccb5da0eb16afafa379a5. Den legger221 nye HD-ruter og105 omtegnede canyon-ruter inn i spillet.196 av de nye rutene er Nexus-dørfaser,25 er canyon-ruter. De105 eldre canyon-rutenes indeksreferansepaletter er rettet uten endrede indeksverdier. Lokalt bruker kjor-rettet-spill.sh den hentede hd-leveranse-mappen med samme mod.

Publisert r19 er brukt som grunnlag. Eksisterende modflett legger til442 filer og erstatter210 filer i105 eksplisitte kostymeenheter. Ingen filer slettes. De øvrige r19-ressursene og alle55 HD-filmer er bevart. Alle44 993 manifestfiler og652 leveransefiler er kontrollert etter pull. Ingen motor- eller pipelinekode er endret.

11 native motorprøver på den sammenslåtte modden viser alle196 nye Nexus-faser og alle130 canyon-ruter.543 fullomtegningskontroller etter oppstart har ingen avvik. Prøvene bruker originalanimasjoner i isolerte spilltilstander. Naturlig canyon-inngang og full gjennomspilling er fortsatt ikke kontrollert. Toms visuelle godkjenning av alle nye bilder gjenstår.

Linux-bygg39112677913 fra kode7b2f4398 og fast mod29cff6583 er grønt, inkludert pakkestart/grafikkvalg og Debian12 uten byggepakker. Pakken er publisert og den faktiske nedlastingen kontrollert: 2140813816 byte, SHA-256 f6c9786ca4f0ebb5f980e1761c79151e643d68a619f7cb0c37aff7b5f3cbe326. Alle44 993 mod-manifestfiler og652 leveransefiler stemmer. Standard AppRun, intro, tekst og HD/klassisk-bytte består550 oppdateringer/fem kontroller. Pakkens egen motor viser alle196 nye Nexus-faser og130 canyon-ruter,543 omtegningskontroller etter oppstart uten avvik. Motorkilden og oppskriften i eksisterende kildearkiv er kontrollert byteidentiske med gjeldende patcher og låst motorcommit og kan gjenbrukes.

Grafikkgrunnlaget er gpt-arbeid c1dc0d07. Integrasjonsrapport, eksplisitt filmanifest, publiseringskontroll og native logger ligger i grafikkgrenen under rapporter/integrering-r20-r21-20261018. Prosjektbibliotekets publisert-mod-er-fasit er brukt og kontrollert mot den faktiske leveransen.

De6 011 manglende faktiske bildene og øvrige eldre figurfeil gjenstår. Denne integrasjonen er ikke en ferdigmelding for all restgrafikken. Vanlige lagringer og innstillinger er ikke endret av testene.
