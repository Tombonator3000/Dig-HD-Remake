"""Gjør motorens liste over det som er vist uten HD om til en prioritert oversikt.

Motoren skriver dighd-uten-hd.txt i lagringsmappen mens spillet spilles (DigHD, se docs/HD-MOTOR.md):
én linje per bilde og rom med type, id, rom, bilder (hvor mange bilder det sto på skjermen uten HD),
piksler (flest originalpiksler i ett bilde) og når det ble sett først. Oversikten samler rutene per
kostyme og sorterer etter hvor mye de ble vist, så det som synes mest, kan bestilles først.

  dighd mangler ~/.local/share/the-dig-hd/saves/dighd-uten-hd.txt [--ut work/mangler.md]
"""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


def read_log(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        f = line.split("\t")
        if len(f) < 6:
            continue
        try:
            rows.append({"type": f[0], "id": f[1], "rom": int(f[2]), "bilder": int(f[3]), "piksler": int(f[4]),
                         "forst": f[5]})
        except ValueError:
            continue
    return rows


def read_figures(path: Path | None) -> dict[int, tuple[str, str]]:
    """docs/figurer.csv: kostyme -> (figur, hva)."""
    if not path or not path.is_file():
        return {}
    with path.open(encoding="utf-8") as f:
        return {int(r["kostyme"]): (r.get("figur") or "", r.get("hva") or "") for r in csv.DictReader(f)}


def ranges(nums) -> str:
    """[1, 2, 3, 7] -> '1-3, 7'"""
    nums = sorted(set(nums))
    out, start = [], None
    for i, n in enumerate(nums):
        if start is None:
            start = n
        if i + 1 == len(nums) or nums[i + 1] != n + 1:
            out.append(str(start) if start == n else f"{start}-{n}")
            start = None
    return ", ".join(out)


def summarize(rows: list[dict], figures: dict[int, tuple[str, str]] | None = None) -> dict:
    figures = figures or {}
    costumes: dict[int, dict] = defaultdict(lambda: {"ruter": set(), "rom": set(), "bilder": 0, "piksler": 0,
                                                     "forst": None})
    others = defaultdict(list)
    for r in rows:
        if r["type"] == "rute" and r["id"].startswith("costume"):
            cid, cel = (int(x) for x in r["id"][len("costume"):].split("_"))
            c = costumes[cid]
            c["ruter"].add(cel)
            c["rom"].add(r["rom"])
            c["bilder"] += r["bilder"]
            c["piksler"] = max(c["piksler"], r["piksler"])
            seen = [v for v in (c["forst"], r["forst"]) if v]
            c["forst"] = min(seen) if seen else None
        else:
            others[r["type"]].append(r)
    kost = []
    for cid, c in costumes.items():
        figur, hva = figures.get(cid, ("", ""))
        kost.append({"kostyme": cid, "figur": figur, "hva": hva, "ruter": sorted(c["ruter"]), "rom": sorted(c["rom"]),
                     "bilder": c["bilder"], "piksler": c["piksler"], "forst": c["forst"]})
    kost.sort(key=lambda k: (-k["bilder"], k["kostyme"]))
    for rows_ in others.values():
        rows_.sort(key=lambda r: (-r["bilder"], r["id"]))
    return {"kostymer": kost, "objekt": others.get("objekt", []), "rom": others.get("rom", []),
            "film": others.get("film", [])}


def markdown(s: dict) -> str:
    out = ["# Vist uten HD", ""]
    n_cels = sum(len(k["ruter"]) for k in s["kostymer"])
    out.append(f"{n_cels} figurruter i {len(s['kostymer'])} kostymer, {len(s['objekt'])} objektbilder, "
               f"{len(s['rom'])} rom og {len(s['film'])} filmer ble vist uten HD. Sortert etter hvor mange bilder "
               "(frames) de sto på skjermen; piksler er flest originalpiksler i ett bilde.")
    if s["kostymer"]:
        out += ["", "## Figurer", "", "| Kostyme | Figur | Ruter | Rom | Bilder | Piksler |", "| --- | --- | --- | --- | --- | --- |"]
        for k in s["kostymer"]:
            figur = " ".join(x for x in (k["figur"], f"({k['hva']})" if k["hva"] else "") if x)
            out.append(f"| {k['kostyme']} | {figur} | {len(k['ruter'])}: {ranges(k['ruter'])} | "
                       f"{', '.join(map(str, k['rom']))} | {k['bilder']} | {k['piksler']} |")
    for label, key in (("Objektbilder", "objekt"), ("Rombakgrunner", "rom"), ("Filmer", "film")):
        if s[key]:
            out += ["", f"## {label}", "", "| Id | Rom | Bilder | Piksler | Sett først |", "| --- | --- | --- | --- | --- |"]
            out += [f"| {r['id']} | {r['rom']} | {r['bilder']} | {r['piksler']} | {r['forst']} |" for r in s[key]]
    return "\n".join(out) + "\n"
