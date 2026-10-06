#!/usr/bin/env python3
"""Leser indeksfilen DIG.LA0 fra The Dig (SCUMM v7) og skriver ut det viktigste.

Bruk:
    python3 tools/la0_info.py STI/TIL/DIG.LA0            # oversikt
    python3 tools/la0_info.py STI/TIL/DIG.LA0 --json     # alt som JSON
    python3 tools/la0_info.py STI/TIL/DIG.LA0 --rooms    # bare romlisten (CSV)

Skriptet leser filen og endrer ingenting. Det trenger bare standardbiblioteket.

Format (bekreftet mot ScummVM engines/scumm/resource.cpp):
  Blokker: 4 byte tagg + 4 byte storrelse (big endian, inkludert hodet).
  RNAM:    oppforinger med 1 byte romnummer + 9 byte navn XOR 0xFF, avsluttet med 0.
  MAXS:    50 byte motorversjon, 50 byte dataversjon, deretter 15 x uint16 LE.
  D*:      kataloger med uint16 LE antall forst.
"""
import argparse
import hashlib
import json
import struct
import sys

KNOWN = {b"RNAM", b"MAXS", b"DROO", b"DSCR", b"DSOU", b"DCOS", b"DCHR", b"DOBJ", b"AARY", b"ANAM"}
MAXS_FIELDS = [
    "variables", "bit_variables", "unknown", "global_objects", "local_objects",
    "new_names", "verbs", "fl_objects", "inventory", "arrays", "rooms",
    "scripts", "sounds", "charsets", "costumes",
]
# Kjente MD5-summer for DIG.LA0 med storrelse 16304 fra ScummVM sin scumm-md5.h
KNOWN_MD5 = {
    "d8323015ecb8b10bf53474f6e6b0ae33": "standardoppforingen for The Dig i ScummVM (ikke lokalisert)",
    "3221ab85c833fbc0e6cf54ad55b4c082": "hebraisk",
    "ebdd2fbc995a321605375dc57766db79": "russisk med undertekster",
}


def walk_blocks(data):
    """Gar gjennom blokkene. Hvis en tagg er ukjent, leter den etter neste kjente tagg."""
    pos, blocks = 0, []
    while pos + 8 <= len(data):
        tag = data[pos:pos + 4]
        if tag not in KNOWN:
            nxt = min((i for i in (data.find(t, pos + 1) for t in KNOWN) if i > 0), default=-1)
            if nxt < 0:
                break
            blocks.append(("RESYNC", pos, nxt - pos))
            pos = nxt
            continue
        size = struct.unpack(">I", data[pos + 4:pos + 8])[0]
        if size < 8 or pos + size > len(data):
            # Skadet blokkhode: en størrelse under 8 ville gitt evig løkke, og en for stor
            # ville lest forbi slutten av filen. Lagre resten som ukjent og stopp.
            blocks.append(("SKADET", pos, len(data) - pos))
            break
        blocks.append((tag.decode(), pos, size))
        pos += size
    return blocks


def parse(data):
    out = {"size": len(data), "md5": hashlib.md5(data).hexdigest(), "blocks": [], "directories": {}}
    out["md5_match"] = KNOWN_MD5.get(out["md5"], "ukjent (eller filen er endret)")
    for tag, pos, size in walk_blocks(data):
        out["blocks"].append({"tag": tag, "offset": pos, "size": size})
        body = data[pos + 8:pos + size]
        if tag == "RNAM":
            rooms, p = [], 0
            while p < len(body) and body[p] != 0:
                name = bytes(b ^ 0xFF for b in body[p + 1:p + 10]).split(b"\x00")[0].decode("latin1")
                rooms.append({"room": body[p], "name": name})
                p += 10
            out["rooms"] = sorted(rooms, key=lambda r: r["room"])
        elif tag == "MAXS":
            out["engine_version"] = body[:50].split(b"\x00")[0].decode("latin1")
            out["data_version"] = " ".join(body[50:100].replace(b"\x00", b" ").decode("latin1").split())
            out["maxs"] = dict(zip(MAXS_FIELDS, struct.unpack("<15H", body[100:130])))
        elif tag in ("DROO", "DSCR", "DSOU", "DCOS", "DCHR", "DOBJ", "ANAM"):
            out["directories"][tag] = struct.unpack("<H", body[:2])[0]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("la0")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--rooms", action="store_true")
    args = ap.parse_args()
    info = parse(open(args.la0, "rb").read())
    if args.json:
        json.dump(info, sys.stdout, indent=1, ensure_ascii=False)
        print()
        return
    if args.rooms:
        print("rom,navn")
        for r in info.get("rooms", []):
            print(f"{r['room']},{r['name']}")
        return
    print(f"Fil: {args.la0}  ({info['size']} byte)")
    print(f"MD5: {info['md5']}  -> {info['md5_match']}")
    print(f"Motorversjon: {info.get('engine_version', '?')}")
    print(f"Dataversjon:  {info.get('data_version', '?')}")
    for k, v in info.get("maxs", {}).items():
        print(f"  {k:15} {v}")
    print("Kataloger (antall plasser):", ", ".join(f"{k}={v}" for k, v in info["directories"].items()))
    resync = [b for b in info["blocks"] if b["tag"] in ("RESYNC", "SKADET")]
    if resync:
        print(f"Advarsel: {len(resync)} ukjente omrader i filen. Filen kan vaere skadet.")
    print(f"Navngitte rom: {len(info.get('rooms', []))}")


if __name__ == "__main__":
    main()
