"""Tester for HD-pipelinen.

Vanlige tester trenger ikke spillfilene. Tester merket `game` bruker game/ og kjøres med:
    pytest -m game
"""
import struct
from pathlib import Path

import pytest
from PIL import Image

from dighd import cli, gamedata, modpack, upscale

ROOT = Path(__file__).resolve().parents[2]
GAME = ROOT / "game"


def _block(tag: bytes, body: bytes) -> bytes:
    return tag + struct.pack(">I", len(body) + 8) + body


def test_index_parsing_and_helpers(tmp_path):
    # Lager en liten LA0 med romnavn, MAXS og en kostymekatalog
    rnam = b"".join(bytes([n]) + bytes(c ^ 0xFF for c in name.ljust(9, b"\0")) for n, name in [(1, b"logo"), (22, b"beach")]) + b"\0"
    maxs = b"7.3.4".ljust(50, b"\0") + b"data".ljust(50, b"\0") + struct.pack("<15H", *range(15)) + bytes(8)
    dcos = struct.pack("<H", 3) + bytes([0, 22, 22]) + struct.pack("<3I", 0, 100, 200)
    la0 = tmp_path / "DIG.LA0"
    la0.write_bytes(_block(b"RNAM", rnam) + _block(b"MAXS", maxs) + _block(b"DCOS", dcos))

    idx = gamedata.read_index(la0)
    assert idx.room_names == {1: "logo", 22: "beach"}
    assert idx.engine_version == "7.3.4"
    assert idx.maxs["rooms"] == 10 and idx.maxs["costumes"] == 14
    assert idx.costume_dir == [(0, 0), (22, 100), (22, 200)]

    # Kostyme-ID-er følger katalogen, ikke rekkefølgen i filen
    room = gamedata.Room(22, offset=1000, akos_offsets=[200, 100])
    assert gamedata.costume_ids(idx, {22: room}) == [2, 1]

    assert cli._rooms("22,24") == {22, 24}
    assert cli._rooms("20-22,30") == {20, 21, 22, 30}
    assert cli._rooms(None) is None


def test_upscale_and_alpha():
    im = Image.new("RGB", (10, 6), (200, 40, 10))
    for method in ("nearest", "lanczos", "lanczos-sharp"):
        out = upscale.upscale(im, 4, method)
        assert out.size == (40, 24)
        assert out.getpixel((20, 12)) == (200, 40, 10) or method != "nearest"
    alpha = Image.new("L", (3, 3), 0)
    alpha.putpixel((1, 1), 255)
    big = upscale.upscale_alpha(alpha, 4)
    assert big.size == (12, 12)
    assert set(big.tobytes()) == {0, 255}  # skarpe kanter, ingen halvgjennomsiktighet
    with pytest.raises(SystemExit):
        upscale.upscale(im, 4, "finnesikke")


def test_bleed_and_object_context():
    # En rød prikk på gjennomsiktig bakgrunn: bleed skal farge naboene røde
    cel = Image.new("RGBA", (5, 5), (0, 0, 0, 0))
    cel.putpixel((2, 2), (255, 0, 0, 255))
    filled = modpack._bleed(cel)
    assert filled.getpixel((1, 2)) == (255, 0, 0)

    # Objekt skalert i sammenheng med bakgrunnen: riktig størrelse og alfa fra originalen
    room = Image.new("RGB", (40, 30), (0, 0, 255))
    obj = Image.new("RGBA", (8, 6), (0, 255, 0, 255))
    obj.putpixel((0, 0), (0, 0, 0, 0))
    hd = modpack._upscale_object_in_context(room, obj, 10, 10, 4, "nearest")
    assert hd.size == (32, 24)
    assert hd.getpixel((0, 0))[3] == 0 and hd.getpixel((10, 10)) == (0, 255, 0, 255)


@pytest.mark.game
def test_real_game_files():
    if not (GAME / "DIG.LA1").exists():
        pytest.skip("game/ mangler, kjør tools/hent_spilldata.sh")
    idx = gamedata.read_index(GAME / "DIG.LA0")
    rooms = gamedata.read_rooms(GAME / "DIG.LA1")
    assert idx.md5 == cli.KNOWN_LA0_MD5
    assert len(rooms) == 111
    assert sum(r.has_zplane for r in rooms.values()) == 61
    assert sum(len(r.palettes) > 1 for r in rooms.values()) == 21
    assert sum(len(o.states) for r in rooms.values() for o in r.objects) == 642
    ids = gamedata.costume_ids(idx, rooms)
    assert len(ids) == 331 and -1 not in ids
    assert (rooms[2].width, rooms[2].height) == (976, 200)
