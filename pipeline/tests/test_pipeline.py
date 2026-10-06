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


def test_gpt_tiles_shift_and_judge():
    from dighd import gpt
    import numpy as np

    # Vanlig rom: én jobb med grå kant, nøyaktig 4x på lerretet
    assert gpt.plan_tiles(320, 200) == [(0, 0, 320, 200, 32, 28)]
    # Bredt rom: flere deler som dekker hele bredden og overlapper
    tiles = gpt.plan_tiles(976, 200)
    assert len(tiles) == 3 and tiles[0][0] == 0 and tiles[-1][0] + tiles[-1][2] == 976
    assert all(t[2] == 384 for t in tiles)
    # Høyt rom deles i høyden
    assert len(gpt.plan_tiles(320, 528)) == 3

    # Fasekorrelasjon finner en kjent forskyvning med riktig fortegn
    rng = np.random.default_rng(0)
    base = gpt.blur(rng.random((96, 128)), 1.5)
    moved = np.roll(base, (2, -3), axis=(0, 1))
    dx, dy, _ = gpt.phase_shift(base, moved)
    assert abs(dx + 3) < 0.3 and abs(dy - 2) < 0.3

    assert gpt.judge({"skift_x": 0.1, "skift_y": 0.0, "blokk_maks": 0.3, "kantlikhet": 0.8})[0] == "godkjent"
    assert gpt.judge({"skift_x": 0.0, "skift_y": 0.0, "blokk_maks": 1.4, "kantlikhet": 0.8})[0] == "sjekk"
    assert gpt.judge({"skift_x": 3.0, "skift_y": 0.0, "blokk_maks": 3.0, "kantlikhet": 0.5})[0] == "avvist"


def test_gpt_lock_and_stitch():
    from dighd import gpt
    import numpy as np

    # Fargelås fjerner et fargestikk, men beholder fin detalj
    rng = np.random.default_rng(1)
    orig = np.full((64, 64, 3), 100.0)
    detail = rng.normal(0, 8, (64, 64, 3))
    cand = orig + 40 + detail
    locked = gpt.lock_colors(cand, orig, sigma=6, strength=1.0)
    assert abs(locked.mean() - 100) < 1.5
    assert locked.std() > 5

    # To like deler sys sammen uten skjøt
    W, H = 600, 200
    full = rng.random((H * gpt.SCALE, W * gpt.SCALE, 3)) * 255
    parts = []
    for x, y, w, h, _, _ in gpt.plan_tiles(W, H):
        parts.append(((x, y, w, h), full[y * 4:(y + h) * 4, x * 4:(x + w) * 4]))
    out = gpt._stitch(W, H, parts)
    assert np.abs(out.astype(float) - full).max() <= 1.0
