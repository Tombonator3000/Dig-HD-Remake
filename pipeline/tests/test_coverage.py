"""Drawing coverage contracts plus optional real SMAP decoder regressions."""
import json
import struct
from types import SimpleNamespace

import numpy as np
from PIL import Image
import pytest

from dighd.coverage import export_object_coverage, smap_coverage
from dighd.modpack import build_mod


def chunk(tag, body):
    return tag + struct.pack(">I", 8 + len(body)) + body


def fixture_smap(transparent_strip_colour):
    # Opaque RAW256 paints black 0 and even room-transparent colour 5.
    raw = bytes([1, 0, 5, 1, 2, 3, 4, 254, 255])
    # HT4, no colour changes: all eight pixels have the same colour.
    translucent = bytes([44, transparent_strip_colour, 0, 0, 0, 0])
    return chunk(b"SMAP", struct.pack("<II", 16, 16 + len(raw)) + raw + translucent)


def test_decoder_writes_are_coverage_even_for_both_buffer_sentinels():
    """No digart dependency: verify its callback contract at nonzero offsets.

    The decoder is deliberately a write oracle, not a reimplementation of SMAP.
    Black, 255, and the transparent index may all be actual writes. Unwritten
    pixels must stay clear, including in later rows and in the second strip.
    """
    data = b"prefix" + fixture_smap(5)
    calls = []

    def draw(buf, x, stride, source, offset, height, transparent):
        assert (stride, height, transparent) == (16, 2, 5)
        assert source is data
        assert offset == (22 if x == 0 else 31)
        calls.append((x, buf[0]))
        if x == 0:
            buf[0], buf[stride + 7] = 0, 255
        else:
            buf[8], buf[stride + 15] = 5, 0

    mask = smap_coverage(data, 6, 16, 2, 5, draw)
    expected = np.zeros((2, 16), dtype=bool)
    expected[0, [0, 8]] = True
    expected[1, [7, 15]] = True
    np.testing.assert_array_equal(mask, expected)
    assert calls == [(0, 0), (0, 255), (8, 0), (8, 0)]


def test_real_decoder_opaque_black_is_not_lost_with_transparent_strip():
    decode = pytest.importorskip("digart.la1")._decompress_bitmap
    mask = smap_coverage(fixture_smap(5), 0, 16, 1, 5, decode)
    assert np.all(mask[0, :8])
    assert not np.any(mask[0, 8:])


def test_real_decoder_black_in_transparent_strip_is_a_drawn_colour():
    decode = pytest.importorskip("digart.la1")._decompress_bitmap
    mask = smap_coverage(fixture_smap(0), 0, 16, 1, 5, decode)
    assert np.all(mask)


def test_broken_strip_table_is_rejected_before_decoding():
    with pytest.raises(ValueError, match="table"):
        smap_coverage(chunk(b"SMAP", b""), 0, 8, 1, 5, None)


@pytest.mark.parametrize("offset", [0, 18])
def test_broken_strip_offset_is_rejected_before_decoding(offset):
    data = chunk(b"SMAP", struct.pack("<I", offset) + bytes(6))
    with pytest.raises(ValueError, match="offset"):
        smap_coverage(data, 0, 8, 1, 5, None)


@pytest.mark.parametrize("width,height", [(0, 1), (7, 1), (8, 0)])
def test_partial_or_empty_strips_are_rejected(width, height):
    with pytest.raises(ValueError, match="dimensions"):
        smap_coverage(b"", 0, width, height, 5, None)


def test_export_uses_room_transparency_repairs_alpha_and_preserves_indices(tmp_path):
    header = bytearray(16)
    struct.pack_into("<H", header, 4, 537)
    struct.pack_into("<HH", header, 12, 16, 1)
    object_chunk = chunk(b"OBIM", chunk(b"IMHD", header) +
                         chunk(b"IM01", fixture_smap(5)) +
                         chunk(b"IM02", chunk(b"BOMP", b"")))
    data = chunk(b"ROOM", chunk(b"TRNS", bytes([5])) + object_chunk)
    rooms = {79: SimpleNamespace(offset=0)}
    objects = tmp_path / "objects"
    objects.mkdir()
    Image.new("RGBA", (16, 1), (0, 0, 0, 0)).save(objects / "obj537_01.png")
    idx = Image.new("P", (16, 1))
    idx.save(objects / "obj537_01_idx.png")
    idx_bytes = (objects / "obj537_01_idx.png").read_bytes()

    def draw(buf, x, stride, source, offset, height, transparent):
        assert (stride, height, transparent) == (16, 1, 5)
        # Opaque first strip writes black; second strip leaves the buffer alone.
        if x == 0:
            buf[:8] = bytes(8)

    assert export_object_coverage(data, rooms, tmp_path, draw, {25}) == 0
    assert not list(objects.glob("*_mask.png"))
    assert export_object_coverage(data, rooms, tmp_path, draw, {79}) == 1
    expected = np.array([[255] * 8 + [0] * 8], dtype=np.uint8)
    np.testing.assert_array_equal(np.asarray(Image.open(objects / "obj537_01_mask.png")), expected)
    np.testing.assert_array_equal(np.asarray(Image.open(objects / "obj537_01.png"))[:, :, 3], expected)
    assert (objects / "obj537_01_idx.png").read_bytes() == idx_bytes
    assert not (objects / "obj537_02_mask.png").exists()


@pytest.mark.parametrize("selected_rooms", [{79}, set()], ids=["room-and-objects", "own-object-only"])
def test_mod_keeps_source_coverage_and_removes_stale_mask(tmp_path, selected_rooms):
    extract, own, out = (tmp_path / name for name in ("extract", "own", "mod"))
    for folder in (extract / "rooms", extract / "objects", own / "objects"):
        folder.mkdir(parents=True)
    Image.new("RGB", (16, 1), "white").save(extract / "rooms" / "room079.png")
    Image.new("P", (16, 1)).save(extract / "rooms" / "room079_idx.png")
    Image.new("RGBA", (16, 1), "black").save(extract / "objects" / "obj537_01.png")
    Image.new("P", (16, 1)).save(extract / "objects" / "obj537_01_idx.png")
    Image.new("RGBA", (64, 4), "black").save(own / "objects" / "obj537_01.png")
    source_mask = extract / "objects" / "obj537_01_mask.png"
    Image.fromarray(np.array([[255] * 8 + [0] * 8], dtype=np.uint8)).save(source_mask)
    (extract / "rooms.json").write_text(json.dumps({"rooms": {"79": {
        "name": "PDA fixture", "width": 16, "height": 1,
        "objects": [{"id": 537, "x": 0, "y": 0, "states": ["01"]}],
    }}}))

    kwargs = dict(scale=4, method="nearest", rooms=selected_rooms, own=own, text_font=False)
    manifest = build_mod(extract, out, **kwargs)
    assert manifest["objects"] == ["obj537_01"]
    dest = out / "objects" / source_mask.name
    assert dest.read_bytes() == source_mask.read_bytes()
    # A legacy extraction must not inherit a different source's coverage.
    source_mask.unlink()
    build_mod(extract, out, **kwargs)
    assert not dest.exists()
