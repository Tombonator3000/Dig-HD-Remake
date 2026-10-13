"""Exact SMAP drawing coverage, independent of any palette colour.

A room's transparent colour applies only to transparent strips. Opaque strips
may paint the same colour, and unwritten pixels in an extracted image happen to
be zero too. Two decoder runs with different initial buffers distinguish those
cases without changing any source indices or guessing from RGB/HD artwork.
"""
from pathlib import Path
import numpy as np
from PIL import Image
from . import gamedata as g


def smap_coverage(data: bytes, smap: int, width: int, height: int,
                  transparent: int, decode) -> np.ndarray:
    if width <= 0 or height <= 0 or width % 8:
        raise ValueError("SMAP dimensions must contain complete 8-pixel strips")
    a, b = bytearray(width * height), bytearray([255]) * (width * height)
    size = g.be32(data, smap + 4)
    for strip in range(width // 8):
        table = smap + 8 + strip * 4
        if table + 4 > smap + size:
            raise ValueError("SMAP strip table exceeds the chunk")
        offset = g.le32(data, table)
        if offset < 8 or offset >= size:
            raise ValueError("SMAP strip offset exceeds the chunk")
        decode(a, strip * 8, width, data, smap + offset, height, transparent)
        decode(b, strip * 8, width, data, smap + offset, height, transparent)
    return (np.frombuffer(a, np.uint8) == np.frombuffer(b, np.uint8)).reshape(height, width)


def export_object_coverage(data: bytes, rooms: dict, out: Path, decode,
                           room_filter: set[int] | None = None) -> int:
    written = 0
    for number, room in rooms.items():
        if room_filter and number not in room_filter:
            continue
        size = g.be32(data, room.offset + 4)
        trns = g.find_child(data, room.offset, size, b"TRNS")
        transparent = data[trns + 8] if trns is not None else 255
        for tag, obj, osize in g.children(data, room.offset + 8, room.offset + size):
            if tag != b"OBIM":
                continue
            header = g.find_child(data, obj, osize, b"IMHD")
            if header is None:
                continue
            oid = g.le16(data, header + 12)
            width, height = g.le16(data, header + 20), g.le16(data, header + 22)
            for state, image, isize in g.children(data, obj + 8, obj + osize):
                if state[:2] != b"IM" or state == b"IMHD":
                    continue
                smap = g.find_child(data, image, isize, b"SMAP")
                if smap is None:
                    continue  # BOMP transparency has its own unambiguous index.
                name = f"obj{oid:03d}_{state[2:].decode('latin1')}"
                path = out / "objects" / f"{name}.png"
                if not path.exists():
                    continue
                mask = smap_coverage(data, smap, width, height, transparent, decode)
                Image.fromarray(mask.astype(np.uint8) * 255).save(out / "objects" / f"{name}_mask.png")
                rgba = Image.open(path).convert("RGBA")
                rgba.putalpha(Image.fromarray(mask.astype(np.uint8) * 255))
                rgba.save(path)
                written += 1
    return written
