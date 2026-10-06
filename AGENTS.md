# AGENTS.md

Instrukser for KI-agenter som jobber i dette repoet.

## Faste regler

- Logg alt du gjør i `log.md` med dato og klokkeslett (norsk tid), nyeste nederst.
- Hold `memory.md` (faste fakta og beslutninger) og `todo.md` oppdatert.
- Skriv dokumentasjon på norsk, uten emoji og uten tankestreker. Skriv vanlig og direkte.
- Spillfiler (`*.LA0`, `*.LA1`, `*.BUN`, `*.SAN`, `*.NUT`, `*.TRS`) og alt som lages fra dem (`work/`, `mods/`) skal aldri inn i `main`. Spillfilene ligger i grenen `spilldata`.

## Oppsett

```sh
tools/hent_spilldata.sh          # spillfilene til game/
pip install -e "pipeline[dev]"   # dighd
dighd extract                    # originalgrafikk til work/extract
engine/build.sh                  # ScummVM med patchen til engine/scummvm
```

## Kommandoer

```sh
cd pipeline && pytest            # etter endringer i pipelinen
pytest -m game                   # mot ekte spillfiler
engine/test.sh                   # etter endringer i patchen: avvik skal være 0 for bakgrunner og uskalerte figurer
```

## Arbeid med motoren

- Patchen ligger i `engine/patches/`. Gjør endringer i `engine/scummvm`, og lag patchen på nytt med
  `git -C engine/scummvm add -N engines/scumm/dighd.cpp engines/scumm/dighd.h && git -C engine/scummvm diff > engine/patches/0001-dighd-hd-grafikk.patch`.
- ScummVM-versjonen er låst i `engine/SCUMMVM_COMMIT`. Bytt den bare sammen med en test av patchen.
- Filnavn i mod-mappen må stemme med det motoren leter etter (se `docs/HD-MOTOR.md`). Kostyme-ID er ID-en fra DCOS-katalogen, ikke rekkefølgen i filen.
