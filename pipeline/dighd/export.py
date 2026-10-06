"""Eksport av originalgrafikk til PNG, klar for oppskalering.

For hvert rom og hvert objektbilde lages to filer:
  roomNNN.png       RGB (objekter: RGBA) med romets første palett. Dette er utgangspunktet for oppskalering.
  roomNNN_idx.png   8-bit indeksert med palett. Motoren bruker denne til å vite hvilke piksler
                    som fortsatt viser original bakgrunn, og til å fargekorrigere ved palettbytte.

Kostymeruter (AKOS) eksporteres som RGBA med fargene slått opp via AKPL og paletten
til rommet kostymen ligger i. Navnet bruker den ekte kostyme-ID-en fra DCOS-katalogen,
som er det motoren kjenner, ikke rekkefølgen i filen.

Dekoding gjøres av digart (thedig-textures), som er sjekket byte for byte mot ScummVM.
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

from . import gamedata


def _require_digart():
    try:
        from digart import akos, la1  # noqa: F401
    except ImportError as exc:  # pragma: no cover
        raise SystemExit("Mangler thedig-textures (digart). Installer med: pip install -e pipeline") from exc
    return la1, akos


def _indexed(index: bytes, w: int, h: int, palette: bytes, transparent: int | None) -> Image.Image:
    im = Image.frombytes("P", (w, h), index)
    im.putpalette(palette)
    if transparent is not None:
        im.info["transparency"] = transparent
    return im


def export_la1(game: Path, out: Path, rooms_filter: set[int] | None = None) -> dict:
    """Eksporterer rombakgrunner og objektbilder. Returnerer metadata som også skrives til rooms.json."""
    la1mod, _ = _require_digart()
    data = (game / "DIG.LA1").read_bytes()
    index = gamedata.read_index(game / "DIG.LA0")
    rooms = gamedata.read_rooms(game / "DIG.LA1")
    (out / "rooms").mkdir(parents=True, exist_ok=True)
    (out / "objects").mkdir(parents=True, exist_ok=True)

    # Hvilket rom hører hvert objekt til
    obj_room = {o.obj_id: r.number for r in rooms.values() for o in r.objects}
    errors: list = []
    written = 0
    for bmp in la1mod.iter_bitmaps(data, errors):
        if bmp.name.startswith("room"):
            num = int(bmp.name[4:])
            if rooms_filter and num not in rooms_filter:
                continue
            idx = _indexed(bmp.index, bmp.width, bmp.height, bmp.palette, None)
            idx.save(out / "rooms" / f"{bmp.name}_idx.png")
            idx.convert("RGB").save(out / "rooms" / f"{bmp.name}.png")
        else:
            obj_id = int(bmp.name[3:6])
            if rooms_filter and obj_room.get(obj_id) not in rooms_filter:
                continue
            idx = _indexed(bmp.index, bmp.width, bmp.height, bmp.palette, bmp.transparent)
            idx.save(out / "objects" / f"{bmp.name}_idx.png", transparency=bmp.transparent)
            idx.convert("RGBA").save(out / "objects" / f"{bmp.name}.png")
        written += 1

    meta = {
        "game_md5_la0": index.md5,
        "engine_version": index.engine_version,
        "rooms": {
            str(r.number): {
                "name": index.room_names.get(r.number, ""),
                "width": r.width,
                "height": r.height,
                "palettes": len(r.palettes),
                "zplane": r.has_zplane,
                "cycles": [list(c) for c in r.cycles],
                "objects": [
                    {"id": o.obj_id, "x": o.x, "y": o.y, "w": o.width, "h": o.height, "states": o.states}
                    for o in r.objects if o.states
                ],
            }
            for r in sorted(rooms.values(), key=lambda r: r.number)
            if not rooms_filter or r.number in rooms_filter
        },
        "errors": [str(e) for e in errors],
    }
    (out / "rooms.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    meta["written"] = written
    return meta


def export_costumes(game: Path, out: Path, costume_filter: set[int] | None = None) -> int:
    """Eksporterer alle AKOS-ruter som RGBA med riktige farger."""
    la1mod, akos = _require_digart()
    data = (game / "DIG.LA1").read_bytes()
    index = gamedata.read_index(game / "DIG.LA0")
    rooms = gamedata.read_rooms(game / "DIG.LA1")
    ids = gamedata.costume_ids(index, rooms)
    dest = out / "costumes"
    dest.mkdir(parents=True, exist_ok=True)

    errors: list = []
    written = 0
    file_no = 0
    meta: dict = {}
    for room_num, room_off in la1mod._iter_rooms(data, "LA1"):
        lflf_off = room_off - 8
        lflf_end = lflf_off + gamedata.be32(data, lflf_off + 4)
        palette = rooms[room_num].palettes[0] if rooms[room_num].palettes else bytes(768)
        for tag, c, size in gamedata.children(data, room_off, lflf_end):
            if tag != b"AKOS":
                continue
            cid = ids[file_no]
            file_no += 1
            if costume_filter and cid not in costume_filter:
                continue
            akpl_off = gamedata.find_child(data, c, size, b"AKPL")
            akpl = data[akpl_off + 8:akpl_off + gamedata.be32(data, akpl_off + 4)] if akpl_off else b""
            # RGBS har de "ekte" fargene for hver AKPL-plass. Motoren tilpasser dem til
            # rompaletten med remapActorPalette, så dette er fargene tegnerne mente.
            rgbs_off = gamedata.find_child(data, c, size, b"RGBS")
            rgbs = data[rgbs_off + 8:rgbs_off + gamedata.be32(data, rgbs_off + 4)] if rgbs_off else b""
            # Palett for _idx-bildene: kodeverdi -> ekte farge
            code_pal = bytearray(768)
            for code in range(256):
                if 3 * code + 3 <= len(rgbs):
                    code_pal[3 * code:3 * code + 3] = rgbs[3 * code:3 * code + 3]
                else:
                    pal_idx = akpl[code] if code < len(akpl) else code
                    code_pal[3 * code:3 * code + 3] = palette[3 * pal_idx:3 * pal_idx + 3]
            cels = []
            for cel in akos._process_costume(data, c, cid, errors, "AKOS"):
                rgba = bytearray(cel.width * cel.height * 4)
                for i, code in enumerate(cel.index):
                    if code == cel.transparent:
                        continue
                    if 3 * code + 3 <= len(rgbs):
                        rgba[4 * i:4 * i + 3] = rgbs[3 * code:3 * code + 3]
                    else:
                        pal_idx = akpl[code] if code < len(akpl) else code
                        rgba[4 * i:4 * i + 3] = palette[3 * pal_idx:3 * pal_idx + 3]
                    rgba[4 * i + 3] = 255
                Image.frombytes("RGBA", (cel.width, cel.height), bytes(rgba)).save(
                    dest / f"costume{cid:03d}_{cel.cel:03d}.png")
                # Kodene slik motoren ser dem, med de ekte fargene som palett. Motoren bruker
                # dette til å finne ut hvilken del av ruta en skjermpiksel kommer fra, og til
                # å fargejustere HD-pikslene når rommet er mørkere eller lysere.
                idx_im = _indexed(cel.index, cel.width, cel.height, bytes(code_pal), cel.transparent)
                idx_im.save(dest / f"costume{cid:03d}_{cel.cel:03d}_idx.png", transparency=cel.transparent)
                cels.append({"cel": cel.cel, "w": cel.width, "h": cel.height})
                written += 1
            meta[str(cid)] = {"room": room_num, "cels": cels}
    (out / "costumes.json").write_text(json.dumps(meta, indent=1))
    return written
