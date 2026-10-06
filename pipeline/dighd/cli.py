"""Kommandolinje for HD-pipelinen.

  dighd info                         Sjekker spillfilene og viser nøkkeltall
  dighd extract                      Eksporterer rom, objekter og kostymer til work/extract
  dighd build-mod --name test        Lager en mod-mappe for HD-motoren
  dighd compare --room 22            Lager et sammenligningsbilde av oppskaleringsmetoder
  dighd san                          Trekker ut filmrammer (via thedig-textures)
  dighd gpt-pakke                    Lager jobber for ChatGPT i work/gpt (rom og store objektbilder)
  dighd gpt-inn                      Tar imot bilder fra ChatGPT, sjekker dem og lager HD-rom og HD-objekter
  dighd gpt-ordre                    Skriver ORDRE.md med neste jobber til ChatGPT
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from . import export, gamedata, gpt, modpack
from .upscale import METHODS

KNOWN_LA0_MD5 = "d8323015ecb8b10bf53474f6e6b0ae33"


def _repo_root() -> Path:
    here = Path.cwd().resolve()
    for p in [here, *here.parents]:
        if (p / "tools" / "hent_spilldata.sh").exists():
            return p
    return here


def _rooms(arg: str | None) -> set[int] | None:
    """Romliste fra kommandolinjen. Uten liste betyr alle rom, og "ingen" betyr ingen rom."""
    if not arg:
        return None
    if arg.strip().lower() == "ingen":
        return set()
    out: set[int] = set()
    for part in arg.split(","):
        if "-" in part:
            a, b = part.split("-")
            out.update(range(int(a), int(b) + 1))
        elif part.strip():
            out.add(int(part))
    return out


def cmd_info(a) -> int:
    game = Path(a.game)
    idx = gamedata.read_index(game / "DIG.LA0")
    rooms = gamedata.read_rooms(game / "DIG.LA1")
    ok = idx.md5 == KNOWN_LA0_MD5
    print(f"Spillmappe:   {game}")
    print(f"DIG.LA0 MD5:  {idx.md5} ({'standardutgaven' if ok else 'ukjent utgave'})")
    print(f"Motor/data:   {idx.engine_version} / {idx.data_version}")
    print(f"Rom:          {len(rooms)} (z-plan: {sum(r.has_zplane for r in rooms.values())}, "
          f"flere paletter: {sum(len(r.palettes) > 1 for r in rooms.values())}, "
          f"fargesykling: {sum(1 for r in rooms.values() if r.cycles)})")
    print(f"Objektbilder: {sum(len(o.states) for r in rooms.values() for o in r.objects)}")
    print(f"Kostymer:     {sum(len(r.akos_offsets) for r in rooms.values())}")
    films = sorted((game / "VIDEO").glob("*.SAN"))
    print(f"Filmer:       {len(films)}")
    return 0 if ok else 1


def cmd_extract(a) -> int:
    game, out = Path(a.game), Path(a.out)
    rooms = _rooms(a.rooms)
    parts = a.only.split(",") if a.only else ["la1", "akos"]
    if "la1" in parts:
        meta = export.export_la1(game, out, rooms)
        print(f"Rom og objekter: {meta['written']} bilder -> {out}")
        if meta["errors"]:
            print(f"  {len(meta['errors'])} feil, se rooms.json")
    if "akos" in parts:
        n = export.export_costumes(game, out, _rooms(a.costumes))
        print(f"Kostymeruter: {n} bilder -> {out / 'costumes'}")
    return 0


def _upscale_kw(a) -> dict:
    return {"tool": a.tool, "model": a.model, "cmd": a.cmd}


def cmd_build_mod(a) -> int:
    out = Path(a.out) if a.out else Path(a.mods) / a.name
    costumes = {-1} if a.kostymer == "alle" else _rooms(a.kostymer)
    modpack.build_mod(Path(a.extract), out, scale=a.scale, method=a.method, rooms=_rooms(a.rooms),
                      own=Path(a.egne) if a.egne else None, with_objects=not a.uten_objekter,
                      costumes=costumes, films=a.filmer.split(",") if a.filmer else None,
                      san=Path(a.san), **_upscale_kw(a))
    return 0


def cmd_compare(a) -> int:
    methods = a.methods.split(",")
    out = Path(a.out or f"work/compare/room{a.room:03d}.png")
    modpack.compare_sheet(Path(a.extract), a.room, methods, a.scale, out, **_upscale_kw(a))
    print(f"Sammenligning ({', '.join(methods)}) -> {out}")
    return 0


def cmd_san(a) -> int:
    """Kjører thedig-textures for filmer. Verktøyet forventer en macOS-sti, så vi lager en snarvei."""
    game = Path(a.game).resolve()
    shim = Path(a.out).resolve().parent / ".bundle" / "TheDig.app" / "Contents" / "Resources" / "game"
    shim.mkdir(parents=True, exist_ok=True)
    link = shim / "game"
    if link.is_symlink() or link.exists():
        link.unlink()
    link.symlink_to(game)
    argv = ["thedig-textures", "extract", "--game", str(shim.parents[2]), "--out", a.out, "--only", "san", "--force"]
    print("Kjører:", " ".join(argv))
    return subprocess.call(argv)


def cmd_gpt_pakke(a) -> int:
    notes = gpt.read_notes(Path(a.notater)) if a.notater else {}
    jobs = gpt.make_jobs(Path(a.extract), Path(a.ut), _rooms(a.rooms), notes)
    n_obj = sum(j.type == "objekt" for j in jobs)
    print(f"{len(jobs)} jobber ({len(jobs) - n_obj} for rom, {n_obj} for store objektbilder) -> "
          f"{Path(a.ut) / 'jobber'} (oversikt i JOBBER.md, status i status.csv)")
    return 0


def cmd_gpt_inn(a) -> int:
    s = gpt.import_results(Path(a.fra), Path(a.extract), Path(a.ut), sigma=a.sigma, strength=a.styrke,
                           only_approved=a.bare_godkjente)
    print("Status:", ", ".join(f"{k} {v}" for k, v in sorted(s["status"].items())))
    print(f"Ferdige rom ({len(s['ferdige_rom'])} av {s['rom_totalt']}):",
          ", ".join(map(str, s["ferdige_rom"])) or "ingen")
    print(f"Ferdige objekter ({len(s['ferdige_objekter'])} av {s['objekter_totalt']}):",
          ", ".join(s["ferdige_objekter"]) or "ingen")
    for line in s["venter"]:
        print("  venter:", line)
    print(f"Rapport: {Path(a.fra) / 'RAPPORT.md'}. Bruk resultatet med: dighd build-mod --egne {a.ut}")
    return 0


def cmd_gpt_ordre(a) -> int:
    anchors = sorted(p.name for p in Path(a.stil).glob("*.png")) if a.stil and Path(a.stil).is_dir() else []
    path = gpt.write_orders(Path(a.fra), batch=a.antall, anchors=anchors, messages=a.beskjed or None)
    print(f"Ordre skrevet: {path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    root = _repo_root()
    ap = argparse.ArgumentParser(prog="dighd", description="HD-pipeline for The Dig")
    ap.add_argument("--game", default=str(root / "game"), help="mappe med DIG.LA0, DIG.LA1 og VIDEO (standard: game/)")
    sub = ap.add_subparsers(dest="command", required=True)

    sub.add_parser("info", help="sjekk spillfilene")

    p = sub.add_parser("extract", help="eksporter originalgrafikk")
    p.add_argument("--out", default=str(root / "work" / "extract"))
    p.add_argument("--only", help="la1, akos (kommaseparert). Standard: begge")
    p.add_argument("--rooms", help="for eksempel 22,24 eller 20-30")
    p.add_argument("--costumes", help="kostyme-ID-er, for eksempel 1-10")

    def up(p):
        p.add_argument("--method", default="lanczos", choices=METHODS)
        p.add_argument("--scale", type=int, default=4)
        p.add_argument("--tool", help="sti til realesrgan-ncnn-vulkan")
        p.add_argument("--model", default="realesrgan-x4plus")
        p.add_argument("--cmd", help="kommandomal for metoden cmd, med {inn} {ut} {skala}")
        p.add_argument("--extract", default=str(root / "work" / "extract"))

    p = sub.add_parser("build-mod", help="lag mod-mappe for HD-motoren")
    up(p)
    p.add_argument("--name", default="hd")
    p.add_argument("--mods", default=str(root / "mods"))
    p.add_argument("--out", help="overstyr målmappe")
    p.add_argument("--rooms", help="for eksempel 22,24 eller 20-30, eller 'ingen' (standard: alle)")
    p.add_argument("--egne", help="mappe med egne HD-bilder (rooms/, objects/) som brukes i stedet. Egne "
                   "objektbilder tas med også for rom utenfor --rooms, men da uten bakgrunn")
    p.add_argument("--uten-objekter", action="store_true", help="bare bakgrunner")
    p.add_argument("--kostymer", help="kostyme-ID-er som skal skaleres, for eksempel 14-18, eller 'alle'")
    p.add_argument("--filmer", help="filmer som skal skaleres, for eksempel SQ1,TRAM1, eller 'alle' (tar mye plass)")
    p.add_argument("--san", default=str(root / "work" / "san"), help="utdata fra dighd san")

    p = sub.add_parser("compare", help="sammenlign oppskaleringsmetoder på ett rom")
    up(p)
    p.add_argument("--room", type=int, required=True)
    p.add_argument("--methods", default="nearest,lanczos,lanczos-sharp")
    p.add_argument("--out")

    p = sub.add_parser("san", help="trekk ut filmrammer med thedig-textures")
    p.add_argument("--out", default=str(root / "work" / "san"))

    p = sub.add_parser("gpt-pakke", help="lag jobber for ChatGPT (referansebilder og prompter)")
    p.add_argument("--extract", default=str(root / "work" / "extract"))
    p.add_argument("--ut", default=str(root / "work" / "gpt"))
    p.add_argument("--rooms", help="for eksempel 22,24 eller 20-30 (standard: alle)")
    p.add_argument("--notater", default=str(root / "docs" / "gpt-romnotater.csv"), help="CSV med rom,notat")

    p = sub.add_parser("gpt-inn", help="ta imot bilder fra ChatGPT, sjekk dem og lag HD-rom")
    p.add_argument("--extract", default=str(root / "work" / "extract"))
    p.add_argument("--fra", default=str(root / "work" / "gpt"))
    p.add_argument("--ut", default=str(root / "work" / "gpt-ferdig"))
    p.add_argument("--sigma", type=float, default=6.0, help="hvor grove fargene som låses til originalen er (HD-piksler)")
    p.add_argument("--styrke", type=float, default=1.0, help="fargelås 0 til 1 (0 = av)")
    p.add_argument("--bare-godkjente", action="store_true", help="ikke bruk jobber med status sjekk")

    p = sub.add_parser("gpt-ordre", help="skriv ORDRE.md med neste jobber til ChatGPT")
    p.add_argument("--fra", default=str(root / "work" / "gpt"))
    p.add_argument("--stil", default=str(root / "work" / ".gpt-gren" / "stil"), help="mappe med stilankere")
    p.add_argument("--antall", type=int, default=10)
    p.add_argument("--beskjed", action="append", help="beskjed til ChatGPT (kan gjentas)")

    a = ap.parse_args(argv)
    return {"info": cmd_info, "extract": cmd_extract, "build-mod": cmd_build_mod,
            "compare": cmd_compare, "san": cmd_san, "gpt-pakke": cmd_gpt_pakke,
            "gpt-inn": cmd_gpt_inn, "gpt-ordre": cmd_gpt_ordre}[a.command](a)


if __name__ == "__main__":
    sys.exit(main())
