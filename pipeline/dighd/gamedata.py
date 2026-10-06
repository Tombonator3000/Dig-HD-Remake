"""Leser strukturen i DIG.LA0 og DIG.LA1 (SCUMM v7).

Dette er bare det HD-arbeidet trenger: romnavn, romstørrelser, paletter,
fargesykling, hvor objektene står, og hvilken kostyme-ID hver AKOS-blokk har.
Selve bildedekodingen gjøres av digart (thedig-textures), som er verifisert
mot ScummVM.

Blokkformat: 4 byte tagg + 4 byte størrelse (big endian, inkludert hodet).
I LA1 er det ingen utfylling til partall (neste = start + størrelse).
"""
from __future__ import annotations

import struct
from dataclasses import dataclass, field
from pathlib import Path


def be32(d: bytes, o: int) -> int:
    return struct.unpack_from(">I", d, o)[0]


def le16(d: bytes, o: int) -> int:
    return struct.unpack_from("<H", d, o)[0]


def le16s(d: bytes, o: int) -> int:
    return struct.unpack_from("<h", d, o)[0]


def le32(d: bytes, o: int) -> int:
    return struct.unpack_from("<I", d, o)[0]


def children(d: bytes, start: int, end: int):
    """Gir (tagg, offset, størrelse) for blokkene mellom start og end."""
    p = start
    while p + 8 <= end:
        tag = d[p:p + 4]
        size = be32(d, p + 4)
        if size < 8 or p + size > end:
            break
        yield tag, p, size
        p += size


def find_child(d: bytes, start: int, size: int, tag: bytes) -> int | None:
    for t, o, _ in children(d, start + 8, start + size):
        if t == tag:
            return o
    return None


# ---------------------------------------------------------------- LA0

@dataclass
class Index:
    room_names: dict[int, str]
    maxs: dict[str, int]
    engine_version: str
    data_version: str
    costume_dir: list[tuple[int, int]]  # (rom, offset) per kostyme-ID
    md5: str = ""


MAXS_FIELDS = [
    "variables", "bit_variables", "unknown", "global_objects", "local_objects",
    "new_names", "verbs", "fl_objects", "inventory", "arrays", "rooms",
    "scripts", "sounds", "charsets", "costumes",
]


def _directory(body: bytes) -> list[tuple[int, int]]:
    n = le16(body, 0)
    rooms = body[2:2 + n]
    offs = [le32(body, 2 + n + 4 * i) for i in range(n)]
    return list(zip(rooms, offs))


def read_index(path: Path) -> Index:
    import hashlib
    d = Path(path).read_bytes()
    names: dict[int, str] = {}
    maxs: dict[str, int] = {}
    ev = dv = ""
    cos: list[tuple[int, int]] = []
    p = 0
    while p + 8 <= len(d):
        tag, size = d[p:p + 4], be32(d, p + 4)
        body = d[p + 8:p + size]
        if tag == b"RNAM":
            q = 0
            while q < len(body) and body[q] != 0:
                raw = bytes(b ^ 0xFF for b in body[q + 1:q + 10])
                names[body[q]] = raw.split(b"\x00")[0].decode("latin1")
                q += 10
        elif tag == b"MAXS":
            ev = body[:50].split(b"\x00")[0].decode("latin1")
            dv = " ".join(body[50:100].replace(b"\x00", b" ").decode("latin1").split())
            maxs = dict(zip(MAXS_FIELDS, struct.unpack_from("<15H", body, 100)))
        elif tag == b"DCOS":
            cos = _directory(body)
        if size < 8:
            break
        p += size
    return Index(names, maxs, ev, dv, cos, hashlib.md5(d).hexdigest())


# ---------------------------------------------------------------- LA1

@dataclass
class ObjectImage:
    obj_id: int
    x: int
    y: int
    width: int
    height: int
    states: list[str]  # "01", "02", ... (heksadesimalt, som IMxx-taggene)


@dataclass
class Room:
    number: int
    offset: int
    width: int = 0
    height: int = 0
    palettes: list[bytes] = field(default_factory=list)
    cycles: list[tuple[int, int, int, int]] = field(default_factory=list)  # (start, slutt, forsinkelse, flagg)
    has_zplane: bool = False
    objects: list[ObjectImage] = field(default_factory=list)
    akos_offsets: list[int] = field(default_factory=list)  # relativt til ROOM-blokken


def _palettes(d: bytes, pals: int) -> list[bytes]:
    wrap = find_child(d, pals, be32(d, pals + 4), b"WRAP")
    if wrap is None:
        return []
    offs = find_child(d, wrap, be32(d, wrap + 4), b"OFFS")
    if offs is None:
        return []
    n = (be32(d, offs + 4) - 8) // 4
    base = offs + 8
    return [d[base + le32(d, base + 4 * i):base + le32(d, base + 4 * i) + 768] for i in range(n)]


def _cycles(body: bytes) -> list[tuple[int, int, int, int]]:
    """CYCL i v6+: [id, 2 ukjente, forsinkelse BE16, flagg BE16, start, slutt] ... 0."""
    out = []
    p = 0
    while p < len(body) and body[p] != 0:
        if p + 9 >= len(body):
            break
        delay = struct.unpack_from(">H", body, p + 3)[0]
        flags = struct.unpack_from(">H", body, p + 5)[0]
        start, end = body[p + 7], body[p + 8]
        if delay and start < end:
            out.append((start, end, delay, flags))
        p += 9
    return out


def read_rooms(path: Path) -> dict[int, Room]:
    d = Path(path).read_bytes()
    if d[:4] != b"LECF" or d[8:12] != b"LOFF":
        raise ValueError("Ikke en SCUMM v7 LA1-fil")
    rooms: dict[int, Room] = {}
    n = d[16]
    for i in range(n):
        num = d[17 + 5 * i]
        off = le32(d, 18 + 5 * i)
        room = Room(num, off)
        rsize = be32(d, off + 4)
        lflf_end = off - 8 + be32(d, off - 4)
        for tag, c, size in children(d, off + 8, off + rsize):
            if tag == b"RMHD":
                room.width, room.height = le16(d, c + 12), le16(d, c + 14)
            elif tag == b"PALS":
                room.palettes = _palettes(d, c)
            elif tag == b"CYCL":
                room.cycles = _cycles(d[c + 8:c + size])
            elif tag == b"RMIM":
                im00 = find_child(d, c, size, b"IM00")
                if im00 is not None:
                    room.has_zplane = find_child(d, im00, be32(d, im00 + 4), b"ZP01") is not None
            elif tag == b"OBIM":
                imhd = find_child(d, c, size, b"IMHD")
                if imhd is None:
                    continue
                h = imhd + 8
                states = [t[2:4].decode("latin1") for t, _, _ in children(d, c + 8, c + size)
                          if t[:2] == b"IM" and t != b"IMHD"]
                room.objects.append(ObjectImage(le16(d, h + 4), le16s(d, h + 8), le16s(d, h + 10),
                                                le16(d, h + 12), le16(d, h + 14), states))
        # AKOS ligger i LFLF etter ROOM-blokken
        for tag, c, _ in children(d, off, lflf_end):
            if tag == b"AKOS":
                room.akos_offsets.append(c - off)
        rooms[num] = room
    return rooms


def costume_ids(index: Index, rooms: dict[int, Room]) -> list[int]:
    """Kostyme-ID for hver AKOS-blokk i filrekkefølge (samme rekkefølge som digart bruker).

    DCOS-katalogen sier (rom, offset) per kostyme-ID. Offset er relativt til ROOM-blokken.
    """
    by_pos = {(r, o): cid for cid, (r, o) in enumerate(index.costume_dir) if r != 0}
    ids = []
    for num in sorted(rooms, key=lambda n: rooms[n].offset):
        for o in rooms[num].akos_offsets:
            ids.append(by_pos.get((num, o), -1))
    return ids
