"""Bygg videre på den publiserte HD-modden i stedet for å erstatte den.

Den publiserte modden i grenen hd-mod er fasit. Codex har lagt inn rettinger (r3 til r12) som bare
finnes der og ikke kan bygges på nytt fra arbeidsbordet. En runde legger derfor bare til det nye:

- en enhet som ikke finnes i den publiserte modden, tas fra kandidaten (den nye byggingen);
- en enhet som finnes publisert uten bilde (bare _idx eller _mask), får kandidatens bilde, mens de
  publiserte filene står;
- en enhet som finnes begge steder, beholdes som publisert, med mindre den står i --erstatt;
- ingenting slettes, med mindre enheten står i --fjern.

En enhet er alle filene for samme bilde: room022.png og room022_idx.png er rom 22, og
costume014_003.png, costume014_003_hd.png og costume014_003_idx.png er rute 3 i kostyme 14.
Fontene er én enhet. En filmramme er sin egen enhet.

sjekk sammenligner en mod som skal publiseres med sjekksummene til den publiserte, og stopper hvis
filer forsvinner eller endres uten at enheten står som erstattet eller fjernet i siste runde i
mod.json. Nye filer er alltid greit.

Bare standardbiblioteket, så tools/mod_gren.sh kan kjøre filen direkte med python3:

  python3 modflett.py flett --publisert DIR --kandidat DIR --ut DIR [--erstatt MØNSTER] [--fjern MØNSTER]
  python3 modflett.py sjekk --publisert SHA256SUMS --ut DIR [--tving]

Mønstrene gjelder enhetene, for eksempel 'costumes/costume004_*' eller 'objects/obj187_01'.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

META = ("mod.json", "README.md", "SHA256SUMS")
INGEN_ENDRING = 3  # utgangskode fra flett når ingenting er lagt til, erstattet eller fjernet

_UNIT = re.compile(r"^(rooms|objects|costumes)/(.+?)(_idx|_hd|_mask)?\.png$")


def unit_of(rel: str) -> str:
    """Enheten en fil i modden hører til (se toppen av filen)."""
    m = _UNIT.match(rel)
    if m:
        return f"{m.group(1)}/{m.group(2)}"
    if rel.startswith("fonts/"):
        return "fonts"
    return rel


def is_image(rel: str) -> bool:
    """Et HD-bilde motoren tegner (ikke indeksbildet eller dekningsmasken)."""
    m = _UNIT.match(rel)
    return m.group(3) in (None, "_hd") if m else True


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def file_hashes(root: Path) -> dict[str, str]:
    """Alle filene i en mod-mappe (uten mod.json, README.md og SHA256SUMS), sti -> sha256."""
    out = {}
    for p in root.rglob("*"):
        rel = p.relative_to(root).as_posix()
        if p.is_file() and rel not in META and not rel.startswith(".git/"):
            out[rel] = _sha256(p)
    return out


def read_sums(path: Path) -> dict[str, str]:
    """En SHA256SUMS-fil (formatet til sha256sum) som sti -> sha256, uten mod.json, README.md og SHA256SUMS."""
    out = {}
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        digest, name = line.split(maxsplit=1)
        name = name.lstrip("*")
        name = name[2:] if name.startswith("./") else name
        if name not in META:
            out[name] = digest
    return out


def _units(hashes: dict[str, str]) -> dict[str, dict[str, str]]:
    units: dict[str, dict[str, str]] = {}
    for rel, digest in hashes.items():
        units.setdefault(unit_of(rel), {})[rel] = digest
    return units


def _matches(unit: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatchcase(unit, pat) for pat in patterns)


def _copy(src_root: Path, dst_root: Path, rels) -> None:
    for rel in rels:
        dst = dst_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_root / rel, dst)


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text()) if path.is_file() else {}


def flett(published: Path, candidate: Path, out: Path, replace: list[str] | None = None,
          remove: list[str] | None = None) -> dict:
    """Lager out som den publiserte modden pluss det nye fra kandidaten. Gir en rapport per enhet."""
    replace, remove = replace or [], remove or []
    if not (published / "mod.json").is_file():
        raise FileNotFoundError(f"Fant ikke {published / 'mod.json'}")
    if not (candidate / "mod.json").is_file():
        raise FileNotFoundError(f"Fant ikke {candidate / 'mod.json'}")
    if out.resolve() in (published.resolve(), candidate.resolve()):
        raise ValueError("--ut må være en egen mappe")
    pub_hashes, cand_hashes = file_hashes(published), file_hashes(candidate)
    pub, cand = _units(pub_hashes), _units(cand_hashes)

    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(published, out)
    files = dict(pub_hashes)
    rep = {"lagt_til": [], "fylt": [], "erstattet": [], "fjernet": [], "ulik_beholdt": [], "lik": 0}

    def drop(rels) -> None:
        for rel in rels:
            (out / rel).unlink()
            del files[rel]

    for unit in sorted(set(pub) | set(cand)):
        old, new = pub.get(unit), cand.get(unit)
        if _matches(unit, remove):
            if old is not None:
                drop(old)
                rep["fjernet"].append(unit)
            continue
        if new is None:
            continue
        if old is None:
            _copy(candidate, out, new)
            files.update(new)
            rep["lagt_til"].append(unit)
        elif old == new:
            rep["lik"] += 1
        elif _matches(unit, replace):
            drop(old)
            _copy(candidate, out, new)
            files.update(new)
            rep["erstattet"].append(unit)
        elif not any(is_image(rel) for rel in old) and any(is_image(rel) for rel in new):
            extra = {rel: d for rel, d in new.items() if rel not in old}
            _copy(candidate, out, extra)
            files.update(extra)
            rep["fylt"].append(unit)
        else:
            rep["ulik_beholdt"].append(unit)

    manifest = _read_json(published / "mod.json")
    cand_manifest = _read_json(candidate / "mod.json")
    for key in ("rooms", "objects", "costumes"):
        if key in cand_manifest or key in manifest:
            manifest[key] = sorted(set(manifest.get(key, [])) | set(cand_manifest.get(key, [])))
    now = datetime.now(timezone.utc).isoformat()
    per_kind: dict[str, int] = {}
    for unit in rep["lagt_til"] + rep["fylt"]:
        kind = unit.split("/", 1)[0]
        per_kind[kind] = per_kind.get(kind, 0) + 1
    manifest.setdefault("runder", []).append({
        "tid": now,
        "grunnlag": manifest.get("created"),
        "kandidat": cand_manifest.get("created"),
        "lagt_til": len(rep["lagt_til"]) + len(rep["fylt"]),
        "lagt_til_per_type": per_kind,
        "erstattet": rep["erstattet"],
        "fjernet": rep["fjernet"],
        "ulik_beholdt": len(rep["ulik_beholdt"]),
    })
    manifest["created"] = now
    (out / "mod.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False))
    rep["endringer"] = len(rep["lagt_til"]) + len(rep["fylt"]) + len(rep["erstattet"]) + len(rep["fjernet"])
    readme = out / "README.md"
    if rep["endringer"] and readme.is_file():
        with readme.open("a") as f:
            f.write(f"\nRunde {now[:16].replace('T', ' ')} UTC: {len(rep['lagt_til']) + len(rep['fylt'])} nye "
                    f"enheter, {len(rep['erstattet'])} erstattet og {len(rep['fjernet'])} fjernet "
                    f"(runder i mod.json).\n")

    # Sjekksummene stemmer med innholdet med en gang (tools/mod_gren.sh send lager dem på nytt).
    for name in ("mod.json", "README.md"):
        if (out / name).is_file():
            files[name] = _sha256(out / name)
    (out / "SHA256SUMS").write_text("".join(f"{files[rel]}  {rel}\n" for rel in sorted(files)))
    return rep


def sjekk(published_sums: Path, mod: Path, force: bool = False) -> tuple[bool, str]:
    """Om mod kan erstatte den publiserte modden (sjekksummene i published_sums), og en melding."""
    pub = read_sums(published_sums)
    new = file_hashes(mod)
    rounds = _read_json(mod / "mod.json").get("runder") or []
    allowed = set(rounds[-1].get("erstattet", []) + rounds[-1].get("fjernet", [])) if rounds else set()
    removed = sorted(r for r in pub if r not in new and unit_of(r) not in allowed)
    changed = sorted(r for r in pub if r in new and new[r] != pub[r] and unit_of(r) not in allowed)
    added = [r for r in new if r not in pub]
    on_purpose = sum(1 for r in pub if unit_of(r) in allowed and new.get(r) != pub[r])
    lines = [f"Mot den publiserte modden: {len(added)} nye filer, {len(changed)} endret, {len(removed)} borte"
             f" og {on_purpose} erstattet eller fjernet med vilje."]
    for label, rows in (("Borte", removed), ("Endret", changed)):
        if rows:
            lines.append(f"{label}: " + ", ".join(rows[:8]) + (f" og {len(rows) - 8} til" if len(rows) > 8 else ""))
    ok = not (removed or changed)
    if not ok:
        if force:
            lines.append("--tving: publiserer likevel.")
        else:
            lines.append("Stopper. Den publiserte modden er fasit (Codex sine rettinger finnes bare der). Bygg videre "
                         "på den med dighd flett-mod (tools/gpt_runde.sh gjør det), og bruk --erstatt eller --fjern "
                         "for det som skal endres. --tving bare når Tom vil erstatte hele modden.")
    return ok or force, "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser("flett", help="den publiserte modden pluss det nye fra kandidaten")
    p.add_argument("--publisert", required=True, help="den publiserte modden (tools/mod_gren.sh hent DIR)")
    p.add_argument("--kandidat", required=True, help="den nye byggingen (dighd build-mod)")
    p.add_argument("--ut", required=True, help="mappen som lages (for eksempel mods/gpt)")
    p.add_argument("--erstatt", action="append", default=[], help="enheter der kandidaten skal erstatte den "
                   "publiserte, for eksempel 'costumes/costume004_*' (kan gjentas)")
    p.add_argument("--fjern", action="append", default=[], help="enheter som skal ut av modden (kan gjentas)")
    p.add_argument("--rapport", help="skriv rapporten med alle enhetene som JSON hit")
    p = sub.add_parser("sjekk", help="stopp hvis en mod mister eller endrer filer mot den publiserte")
    p.add_argument("--publisert", required=True, help="SHA256SUMS fra den publiserte modden")
    p.add_argument("--ut", required=True, help="modden som skal publiseres")
    p.add_argument("--tving", action="store_true", help="publiser likevel (bare når Tom vil erstatte hele modden)")
    a = ap.parse_args(argv)

    if a.command == "sjekk":
        ok, msg = sjekk(Path(a.publisert), Path(a.ut), a.tving)
        print(msg)
        return 0 if ok else 1
    rep = flett(Path(a.publisert), Path(a.kandidat), Path(a.ut), a.erstatt, a.fjern)
    if a.rapport:
        Path(a.rapport).parent.mkdir(parents=True, exist_ok=True)
        Path(a.rapport).write_text(json.dumps(rep, indent=1, ensure_ascii=False))
    print(f"Flettet inn i den publiserte modden: {len(rep['lagt_til'])} nye enheter, {len(rep['fylt'])} fylt "
          f"(hadde bare indeksbilde), {len(rep['erstattet'])} erstattet, {len(rep['fjernet'])} fjernet. "
          f"{len(rep['ulik_beholdt'])} er ulike i kandidaten, men står som publisert (--erstatt tar dem inn). -> {a.ut}")
    for label in ("lagt_til", "fylt", "erstattet", "fjernet"):
        if rep[label]:
            rows = rep[label]
            print(f"  {label}: " + ", ".join(rows[:10]) + (f" og {len(rows) - 10} til" if len(rows) > 10 else ""))
    return 0 if rep["endringer"] else INGEN_ENDRING


if __name__ == "__main__":
    sys.exit(main())
