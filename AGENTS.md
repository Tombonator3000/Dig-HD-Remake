# AGENTS.md

Instrukser for alle KI-agenter som jobber i dette repoet (Claude, Codex, ChatGPT).

## Før du starter

1. Les `memory.md` (faste fakta og beslutninger).
2. Les `todo.md`, særlig `## Neste`.
3. Les de siste oppføringene i `log.md`.
4. Les `STATUS.md` hvis du skal endre noe som er testet eller rapportert der.

## Mens du jobber

- Logg alt du gjør nederst i `log.md` med dato og klokkeslett i norsk tid, og hvem du er: `## 2026-10-06 23:50 (Claude)`, så punkter.
- Kryss av og legg til punkter i `todo.md` underveis.
- Oppdater `memory.md` når en beslutning eller et fast faktum endrer seg.
- Oppdater `STATUS.md` når noe nytt virker, er testet eller har fått en kjent begrensning.

## Stil

- Dokumentasjon og logg på norsk. Kode og kommentarer kan være på norsk eller engelsk, som filen rundt.
- Ingen emoji og ingen tankestreker. Skriv vanlig og direkte, uten fyllord og salgsspråk.
- Si hva som er testet og hvordan. Det som ikke er testet, står som ikke testet.

## Regler

- Spillfiler (`*.LA0`, `*.LA1`, `*.BUN`, `*.SAN`, `*.NUT`, `*.TRS`) og alt som lages fra dem (`work/`, `mods/`, HD-bilder) skal aldri inn i `main` eller kodegrener. De ligger i egne private grener (se under).
- Repoet er privat. *The Dig* tilhører Disney/Lucasfilm. Ingenting fra spillet deles.
- Konseptbildene i `docs/konsept/` er laget av en Reddit-tegner. Spør og krediter før noe vises offentlig.
- Kjør testene før du committer endringer i pipelinen eller motoren.
- Kodeendringer går via PR mot `main` og flettes når CI er grønn. Logg, status, todo og minne kan committes rett i `main`.

## Roller

- Claude: all kode (pipeline, motor, test, verktøy for ChatGPT-jobbene) og kontrollen av grafikken.
- ChatGPT: HD-grafikken, etter `docs/BESTILLING-CHATGPT.md`. Jobber bare i grenen `gpt-arbeid`.
- Tom: godkjenner stil og resultater.

## Oppsett

```sh
tools/hent_spilldata.sh          # spillfilene til game/
python3 -m venv .venv && . .venv/bin/activate
pip install -e "pipeline[dev,uttrekk]"   # dighd (uttrekk: dekoderne dighd extract trenger)
dighd extract                    # originalgrafikk til work/extract
engine/build.sh                  # ScummVM med patchen til engine/scummvm
```

## Kommandoer

```sh
cd pipeline && pytest            # etter endringer i pipelinen (game-testen hoppes over uten game/)
pytest -m "not game"             # det CI kjører
engine/test.sh                   # etter endringer i patchen: 0 avvik for bakgrunner og uskalerte figurer
engine/run.sh gpt                # spill med HD-modden i mods/gpt
```

## ChatGPT-runder

En runde, kjøres jevnlig (omtrent hver halvtime når ChatGPT leverer):

```sh
tools/gpt_runde.sh [--beskjed "tekst til ChatGPT"]
```

Den henter grenen `gpt-arbeid`, kjører kontrollen, bygger modden av alle godkjente rom når noe nytt er godkjent, publiserer den i `hd-mod`, skriver ny `ORDRE.md` og sender status, rapport og retur tilbake. Etterpå: se på forhåndsvisningene av nye godkjente bilder i `work/gpt/forhandsvisning/<jobb>.png` før du rapporterer til Tom.

Enkeltsteg:

```sh
dighd gpt-pakke                  # jobbene i work/gpt (referanse, prompt, metadata)
tools/gpt_gren.sh send|hent      # jobber, status og ordre til og fra grenen gpt-arbeid
dighd gpt-inn                    # plassering, fargelås, sammensying, RAPPORT.md og retur.md
dighd gpt-ordre                  # ORDRE.md med de neste jobbene
dighd build-mod --name gpt --egne work/gpt-ferdig
tools/mod_gren.sh send|hent      # modden til og fra grenen hd-mod
```

Romnotater til promptene: `docs/gpt-romnotater.csv`. Grensene for godkjenning står øverst i `pipeline/dighd/gpt.py`. AGENTS.md for ChatGPT i grenen `gpt-arbeid` lages fra `docs/gpt-arbeid-AGENTS.md`.

## Arbeid med motoren

- Patchen ligger i `engine/patches/`. Gjør endringer i `engine/scummvm`, og lag patchen på nytt med
  `git -C engine/scummvm add -N engines/scumm/dighd.cpp engines/scumm/dighd.h && git -C engine/scummvm diff > engine/patches/0001-dighd-hd-grafikk.patch`.
- ScummVM-versjonen er låst i `engine/SCUMMVM_COMMIT`. Bytt den bare sammen med en test av patchen.
- Filnavn i mod-mappen må stemme med det motoren leter etter (se `docs/HD-MOTOR.md`). Kostyme-ID er ID-en fra DCOS-katalogen, ikke rekkefølgen i filen.

## Grener

| Gren | Innhold |
| --- | --- |
| `main` | Kode og dokumentasjon |
| `spilldata` | Spillfilene med sjekksummer |
| `gpt-arbeid` | Arbeidsbordet med ChatGPT |
| `hd-mod` | Siste ferdige HD-mod (én commit som erstattes) |
| `grafikkdata/pilot-20261006` | Grafikkpiloten fra Codex |
