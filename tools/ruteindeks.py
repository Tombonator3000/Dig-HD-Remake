#!/usr/bin/env python3
"""Lager manglende indeksbilder (costumeCCC_NNN_idx.png) for myke ruter i en mod, uten dekoderne.

Motoren bruker en myk rute (costumeCCC_NNN_hd.png) bare når indeksbildet finnes. Uten thedig-textures
kan de lages fra originalrutene (RGBA, laget fra original_1x.png og rekt i jobbmappene på arbeidsbordet)
og fargetabellen i kostymets eksisterende indeksbilder: hver farge får den indeksen den oftest har der.

Kostymer der fargetabellen har like farger med ulik indeks (kodek 5 og 16 tegnes med kodene som
palettindekser), kan få feil kode. Skriptet skriver hvor mange piksler i de eksisterende bildene som
ville fått feil indeks; er tallet høyt, la kostymet være (--hopp-over).

Bruk: tools/ruteindeks.py MODMAPPE ORIGINALRUTER [--hopp-over 229,230]
"""
import argparse
import collections
from pathlib import Path

import numpy as np
from PIL import Image


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("mod", type=Path, help="modmappen (med costumes/)")
    ap.add_argument("ruter", type=Path, help="mappe med originalrutene costumeCCC_NNN.png (RGBA)")
    ap.add_argument("--hopp-over", default="", help="kostymer som ikke får nye indeksbilder")
    a = ap.parse_args()
    skip = {int(x) for x in a.hopp_over.split(",") if x.strip()}
    cos_dir = a.mod / "costumes"
    missing: dict[str, list[str]] = collections.defaultdict(list)
    for hd in sorted(cos_dir.glob("costume*_*_hd.png")):
        base = hd.name[:-7]
        if not (cos_dir / f"{base}_idx.png").exists():
            missing[base[:10]].append(base)
    for cos, bases in sorted(missing.items()):
        if int(cos[7:]) in skip:
            print(f"{cos}: hoppet over ({len(bases)} ruter)")
            continue
        existing = sorted(cos_dir.glob(f"{cos}_*_idx.png"))
        if not existing:
            print(f"{cos}: ingen eksisterende indeksbilder, hoppet over")
            continue
        first = Image.open(existing[0])
        pal, transparent = first.getpalette()[:768], first.info.get("transparency")
        colours = np.array(pal).reshape(-1, 3)
        votes: dict[tuple, collections.Counter] = collections.defaultdict(collections.Counter)
        for e in existing:
            arr = np.asarray(Image.open(e))
            codes, counts = np.unique(arr[arr != transparent], return_counts=True)
            for k, n in zip(codes, counts):
                votes[tuple(colours[k])][int(k)] += int(n)
        lut = {col: v.most_common(1)[0][0] for col, v in votes.items()}
        wrong = sum(n for col, v in votes.items() for k, n in v.items() if k != lut[col])
        total = sum(sum(v.values()) for v in votes.values())
        made = 0
        for base in bases:
            src = a.ruter / f"{base}.png"
            if not src.exists():
                continue
            rgba = np.asarray(Image.open(src).convert("RGBA"))
            out = np.full(rgba.shape[:2], transparent, np.uint8)
            for y, x in zip(*np.nonzero(rgba[..., 3] > 0)):
                col = tuple(int(v) for v in rgba[y, x, :3])
                if col not in lut:
                    d = ((colours - np.array(col)) ** 2).sum(1)
                    d[transparent] = 1 << 30
                    lut[col] = int(d.argmin())
                out[y, x] = lut[col]
            im = Image.fromarray(out, "P")
            im.putpalette(pal)
            im.save(cos_dir / f"{base}_idx.png", transparency=transparent)
            made += 1
        print(f"{cos}: {made} indeksbilder laget, {wrong} av {total} piksler i de eksisterende ville fått feil indeks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
