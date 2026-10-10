# Mottak på samme Kubuntu-maskin

Tom har bedt om flere grafikkagenter og raskere samarbeid med Claude. Tre agenter lager ulike kostymer i egne oppgavemapper. Root er eneste som endrer leverte jobbfiler, felles fremdrift og grafikkens Git-indeks. Claude har kode, offisiell mottakskontroll og spilltest.

Grafikkcheckout: `/home/tombonator3000t/Documents/Codex/Dig-HD-Remake-gpt-grafikk`, gren `gpt-arbeid`. Claude bruker sin egen kodecheckout og `work/.gpt-gren`. Tom trenger ikke flytte filer mellom oss på samme maskin.

1. Les `mottaksko.json` for siste samlede leveranse, jobbnavn, bildehash og kontrollfiler. Bruk commiten som inneholder manifestet som grafikkcommit.
2. Hent grafikken med den vanlige mottaksflyten fra egen kodecheckout. Rapporter og rutekart må leses fra `work/.gpt-gren/rapporter/`; `gpt_gren.sh hent` kopierer bare resultat/notat for eksisterende jobber.
3. Kontroller de prioriterte importfeilene i `TIL-CLAUDE.md`: teknisk magenta som blir synlig, ulik skalering mellom munnfaser og magenta som forstyrrer hodeanker. Ny grafikk er ikke bevis på at disse kodefeilene er rettet.
4. Svar i `fra-claude/` med faktisk mottatt grafikkcommit, kodecommit, jobb og bildehash, importresultat, modversjon og utført spillkontroll. `fra-claude-eksempel.json` er bare skjema.

Lokale grafikkontroller er kilde-, alfa-, telle- og isolerte importkontroller. De erstatter ikke motorens plassering, animasjon eller Toms visuelle godkjenning. Ingen aktiv Claude-chat har kvittert for mottak hittil.

Ikke kjør `gpt_gren.sh send` i den aktive grafikkcheckouten. Den bruker `git add -A`, som kan ta med uvedkommende arbeidsfiler. Bevar andres lokale endringer og beskyttede originaler. Grafikk publiseres bare til `gpt-arbeid`.
