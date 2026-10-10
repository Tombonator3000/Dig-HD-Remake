# Kildeavklaring for røde effektflater

Kontrollert 10. oktober 2026. Gjelder fig092_07 til fig092_26 og fig122_12 til fig122_20. Dette er innen bestilt grafikkarbeid, ikke en forespørsel om ny omfangsgodkjenning.

Kildene viser i store områder ensfargede røde flater med gjennomsiktige dråpehull og tynne streker. De første blå kulene i kostymene er derimot flerfargede og har synlig materiale. Måling av de faktiske kildefargene og SHA256 står i maskelignende-kilder.json. Ingen av originalfilene er endret.

Forsøkene for fig092_07 til fig092_26 består ikke kildetrohet. De tolker stilankeret som motiv og fyller flere originale tomrom med blå kuler eller nye innfatninger. De er tilbakeholdt selv der antall og alfamåling består. Fig122_12 til fig122_20 er ikke sendt til generatoren, for å unngå å gjenta den samme feilen.

Det er ikke fastslått om flatene er synlig rød grafikk, skyggemasker, andre effektkoder eller et palettvalg som trenger runtime-kontroll. docs/HD-MOTOR.md på main, kildecommit 35197b785a70bea1048823a8cfa2659634e774f6, dokumenterer at kostymers farger kan avhenge av rompalett, kodek og skyggetabell, og at spesialeffekter kan beholdes som originalpiksler. Det beviser ikke hvilken funksjon disse konkrete flatene har.

Claude: kontroller de aktuelle rutene i deres faktiske animasjon med palettindekser, valgt rompalett og eventuell skyggemodus. Oppgi om det skal tegnes synlig grafikk, bevares en effektmaske eller leveres et korrigert visuelt kildegrunnlag. Bevar eksisterende referanse.png, original_1x.png, prompt.txt og jobb.json. Ved behov kan korrigert grunnlag legges som nye referansefiler. Originale hull og delruter skal ikke erstattes av kuler på grunnlag av stilankeret alene.

Resten av produksjonen fortsetter. Dette er grafikkontroll og kildeanalyse; ingen kode er endret, og ingen runtime-test er utført her.
