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
    assert cli._rooms("ingen") == set()


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


def test_gpt_layout_and_orders(tmp_path):
    from dighd import gpt

    # Hele lerretet, bare bildet i rommets sideforhold, eller feil
    assert gpt.detect_layout((1536, 1024), (320, 200)) == "lerret"
    assert gpt.detect_layout((1280, 800), (320, 200)) == "direkte"
    assert gpt.detect_layout((1024, 1024), (320, 200)) is None
    # Utsnitt som selv er 3:2 regnes som lerret
    assert gpt.detect_layout((1536, 1024), (384, 256)) == "lerret"

    rows = [
        ("rom002_del1av3", 2, "ny", ""),
        ("rom009", 9, "godkjent", ""),
        ("rom010", 10, "avvist", "forskjøvet 3 px"),
        ("rom011", 11, "sjekk", "kantlikhet 0,50"),
    ]
    with (tmp_path / "status.csv").open("w", encoding="utf-8") as f:
        f.write(",".join(gpt.STATUS_FIELDS) + "\n")
        for jobb, rom, status, kommentar in rows:
            row = {k: "" for k in gpt.STATUS_FIELDS}
            row.update(jobb=jobb, rom=rom, navn="x", status=status, kommentar=kommentar)
            row["del"] = "1/1"
            f.write(",".join(str(row[k]) for k in gpt.STATUS_FIELDS) + "\n")
    text = gpt.write_orders(tmp_path, batch=2, anchors=["room009_core.png"], messages=["Hei"]).read_text()
    # Avviste først, så nye. Sjekk-jobben kommer ikke med når køen er full.
    assert text.index("rom010") < text.index("rom002_del1av3")
    assert "1. `rom010`" in text and "rom011" not in text
    assert "Ferdige rom: 1 av 4 (9)" in text
    assert "stil/room009_core.png" in text and "- Hei" in text
    tasks = tmp_path / "oppgaver.md"
    tasks.write_text("1. Test på laptopen.\n", encoding="utf-8")
    text = gpt.write_orders(tmp_path, tasks=tasks).read_text()
    assert "## Kodeoppgaver" in text and "1. Test på laptopen." in text
    lst = gpt.write_list(tmp_path, batch=2).read_text()
    # Samme rekkefølge som ordren, delt i bestillinger, og ferdige jobber krysset av
    assert lst.index("## Bestilling 1") < lst.index("rom010") < lst.index("rom002_del1av3") < lst.index("## Bestilling 2")
    assert "- [x] `rom009`" in lst and "rom011" in lst.split("## Bestilling 2")[1]


def _texture(rng, w, h, sigma=2.0):
    """Kunstig bilde med former og farger, så kontrollen har noe å kjenne igjen."""
    from dighd import gpt
    import numpy as np

    a = np.stack([gpt.blur(rng.random((h, w)), sigma) for _ in range(3)], axis=-1)
    a = (a - a.min()) / (a.max() - a.min()) * 255
    return Image.fromarray(a.astype("uint8"))


def _fake_extract(tmp_path):
    """Et lite uttrekk: rom 5 (320 x 200) med ett stort objektbilde med gjennomsiktig hjørne og ett lite."""
    import json
    import numpy as np

    rng = np.random.default_rng(3)
    ex = tmp_path / "extract"
    (ex / "rooms").mkdir(parents=True)
    (ex / "objects").mkdir()
    room = _texture(rng, 320, 200)
    room.save(ex / "rooms" / "room005.png")
    Image.new("P", (320, 200)).save(ex / "rooms" / "room005_idx.png")
    big = _texture(rng, 220, 120, 1.5).convert("RGBA")
    for x in range(60):
        for y in range(40):
            big.putpixel((x, y), (255, 0, 255, 0))   # gjennomsiktig, fargen skal ikke synes
    big.save(ex / "objects" / "obj241_01.png")
    Image.new("P", (220, 120)).save(ex / "objects" / "obj241_01_idx.png")
    Image.new("RGBA", (20, 20), (9, 9, 9, 255)).save(ex / "objects" / "obj007_01.png")
    Image.new("P", (20, 20)).save(ex / "objects" / "obj007_01_idx.png")
    meta = {"game_md5_la0": "x", "rooms": {"5": {
        "name": "testrom", "width": 320, "height": 200, "palettes": 1, "zplane": False, "cycles": [],
        "objects": [{"id": 241, "x": 40, "y": 30, "w": 220, "h": 120, "states": ["01"]},
                    {"id": 7, "x": 10, "y": 10, "w": 20, "h": 20, "states": ["01"]}]}}}
    (ex / "rooms.json").write_text(json.dumps(meta))
    return ex, room, big


def test_gpt_object_jobs_and_import(tmp_path):
    import json
    from PIL import ImageFilter
    from dighd import gpt

    ex, room, big = _fake_extract(tmp_path)
    work, done = tmp_path / "gpt", tmp_path / "gpt-ferdig"
    jobs = gpt.make_jobs(ex, work, notes={5: "Test note."})
    # Romjobben først, så det store objektbildet. Det lille blir ikke egen jobb.
    assert [j.id for j in jobs] == ["rom005", "obj241_01"]
    assert [r["type"] for r in gpt.read_status(work)] == ["rom", "objekt"]

    d = work / "jobber" / "obj241_01"
    data = json.loads((d / "jobb.json").read_text())
    assert data["type"] == "objekt" and data["objekt"] == 241 and data["tilstand"] == "01"
    assert data["objekt_i_rom"] == [40, 30, 220, 120] and data["region"] == [0, 0, 220, 120]
    ox, oy = (384 - 220) // 2, (256 - 120) // 2
    assert data["plassering"] == [ox, oy] and data["bilde_i_lerret"] == [ox * 4, oy * 4, 880, 480]
    room_job = json.loads((work / "jobber" / "rom005" / "jobb.json").read_text())
    assert room_job["type"] == "rom" and room_job["objekt"] is None

    # Samme lerret og kant som rommene, objektet i 4x på riktig sted
    ref = Image.open(d / "referanse.png")
    assert ref.size == (1536, 1024) and ref.getpixel((0, 0)) == gpt.BORDER

    def at(x, y):
        return ref.getpixel(((ox + x) * 4 + 2, (oy + y) * 4 + 2))

    # Gjennomsiktig del: rommet bak objektet. Synlig del: objektet.
    assert at(5, 5) == room.getpixel((40 + 5, 30 + 5))
    assert at(100, 80) == big.getpixel((100, 80))[:3]
    orig = Image.open(d / "original_1x.png")
    assert orig.size == (220, 120) and orig.getpixel((5, 5)) == room.getpixel((45, 35))
    prompt = (d / "prompt.txt").read_text()
    assert gpt.PROMPT_OBJECT in prompt and "Note for this room: Test note." in prompt
    assert prompt.startswith(gpt.PROMPT_BASE) and prompt.rstrip().endswith(gpt.PROMPT_STYLE)

    # Et riktig plassert, litt mykere resultat godkjennes og blir et HD-objekt i 4x
    ref.filter(ImageFilter.GaussianBlur(1.5)).save(d / "resultat.png")
    s = gpt.import_results(work, ex, done)
    assert s["ferdige_objekter"] == ["obj241_01"] and s["ferdige_rom"] == []
    assert (s["rom_totalt"], s["objekter_totalt"]) == (1, 1)
    status = {r["jobb"]: r for r in gpt.read_status(work)}
    assert status["obj241_01"]["status"] == "godkjent" and status["obj241_01"]["type"] == "objekt"
    hd = Image.open(done / "objects" / "obj241_01.png")
    assert hd.size == (880, 480) and hd.mode == "RGBA"
    assert hd.getpixel((5 * 4, 5 * 4))[3] == 0 and hd.getpixel((100 * 4, 80 * 4))[3] == 255
    assert not (done / "rooms" / "room005.png").exists()
    prov = json.loads((done / "provenance.json").read_text())["obj241_01"]
    assert prov["fil"] == "objects/obj241_01.png" and prov["storrelse"] == [880, 480]
    assert prov["type"] == "objekt" and prov["jobber"][0]["status"] == "godkjent"
    report = (work / "RAPPORT.md").read_text()
    assert "Ferdige rom: 0 av 1" in report and "Ferdige objekter: 1 av 1 (obj241_01)" in report
    orders = gpt.write_orders(work).read_text()
    assert "Ferdige rom: 0 av 1" in orders and "Ferdige objekter: 1 av 1 (obj241_01)" in orders
    assert "1. `rom005`" in orders

    # Modden: det godkjente objektbildet kommer med selv om rommet ikke har HD-bakgrunn
    m = modpack.build_mod(ex, tmp_path / "mod", scale=4, method="nearest", rooms=set(), own=done)
    assert m["rooms"] == [] and m["objects"] == ["obj241_01"]
    assert not (tmp_path / "mod" / "rooms" / "room005.png").exists()
    assert (tmp_path / "mod" / "objects" / "obj241_01_idx.png").exists()
    assert not (tmp_path / "mod" / "objects" / "obj007_01.png").exists()
    # Med rommet valgt: bakgrunnen og det lille objektet skaleres automatisk, det store er det egne
    m = modpack.build_mod(ex, tmp_path / "mod2", scale=4, method="nearest", rooms={5}, own=done)
    assert m["rooms"] == [5] and m["objects"] == ["obj007_01", "obj241_01"]
    assert Image.open(tmp_path / "mod2" / "objects" / "obj241_01.png").tobytes() == hd.tobytes()


def test_gpt_orders_with_objects(tmp_path):
    from dighd import gpt

    # Gammel status.csv uten kolonnen type: alt er romjobber
    old = ["jobb", "rom", "navn", "del", "status", "kommentar"]
    with (tmp_path / "status.csv").open("w", encoding="utf-8") as f:
        f.write(",".join(old) + "\nrom009,9,core,1/1,godkjent,\nrom010,10,x,1/1,ny,\n")
    assert [r["type"] for r in gpt.read_status(tmp_path)] == ["rom", "rom"]
    assert "Ferdige rom: 1 av 2 (9)" in gpt.write_orders(tmp_path).read_text()

    rows = [
        ("rom002_del1av3", "rom", 2, "ny", ""),
        ("rom003", "rom", 3, "ny", ""),
        ("obj060_01", "objekt", 3, "ny", ""),
        ("rom009", "rom", 9, "godkjent", ""),
        ("obj050_01", "objekt", 9, "ny", ""),
        ("obj050_02", "objekt", 9, "godkjent", ""),
        ("rom010", "rom", 10, "avvist", "forskjøvet 3 px"),
        ("rom011", "rom", 11, "sjekk", "kantlikhet 0,50"),
    ]
    with (tmp_path / "status.csv").open("w", encoding="utf-8") as f:
        f.write(",".join(gpt.STATUS_FIELDS) + "\n")
        for jobb, typ, rom, status, kommentar in rows:
            row = {k: "" for k in gpt.STATUS_FIELDS}
            row.update(jobb=jobb, type=typ, rom=rom, navn="x", status=status, kommentar=kommentar)
            row["del"] = "1/1"
            f.write(",".join(str(row[k]) for k in gpt.STATUS_FIELDS) + "\n")
    text = gpt.write_orders(tmp_path, batch=10).read_text()
    # Avviste, så nye objektjobber i ferdige rom, så nye etter romnummer (rom før objekt), så sjekk
    order = ["rom010", "obj050_01", "rom002_del1av3", "rom003", "obj060_01", "rom011"]
    pos = [text.index(f"`{j}`") for j in order]
    assert pos == sorted(pos)
    assert "Ferdige rom: 1 av 5 (9)" in text and "Ferdige objekter: 1 av 3 (obj050_02)" in text
    assert "`obj050_01` (rom 9, x, objekt 50 tilstand 01, del 1/1)" in text


def test_gpt_object_notes_and_states(tmp_path):
    from dighd import gpt
    import numpy as np
    from PIL import Image

    notes_csv = tmp_path / "notater.csv"
    notes_csv.write_text('rom,navn,notat\n28,shardcu,"Hands."\nobj241,shardcu,"No hands."\n', encoding="utf-8")
    notes = gpt.read_notes(notes_csv)
    assert notes == {28: "Hands.", "obj241": "No hands."}
    p = gpt._prompt(28, notes, 1, 1, is_object=True, obj_key="obj241")
    assert "No hands." in p and "Hands." not in p.replace("No hands.", "")
    assert gpt._prompt(28, notes, 1, 1, is_object=True, obj_key="obj999", later_state=True).endswith(gpt.PROMPT_STATE)

    # Senere tilstand: likt område tas fra første tilstand, forskjellen fra det nye bildet
    a = np.zeros((40, 40), np.uint8)
    b = a.copy()
    b[10:20, 10:20] = 7
    Image.fromarray(a, "L").convert("P").save(tmp_path / "base_idx.png")
    Image.fromarray(b, "L").convert("P").save(tmp_path / "ny_idx.png")
    base = np.full((160, 160, 3), 100, np.uint8)
    new = np.full((160, 160, 3), 200, np.uint8)
    out = gpt.match_state(new, base, tmp_path / "ny_idx.png", tmp_path / "base_idx.png")
    assert out[60, 60, 0] == 200          # midt i det som er forskjellig
    assert out[150, 150, 0] == 100        # langt unna: som første tilstand
    assert out[5, 5, 0] == 100
