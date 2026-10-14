"""Runden bygger videre på den publiserte modden og mister ikke Codex sine rettinger (modflett)."""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

import pytest

from dighd import modflett
from dighd.modflett import INGEN_ENDRING, flett, is_image, sjekk, unit_of

REPO = Path(__file__).resolve().parents[2]

# Den publiserte modden: Codex sine bilder, et rom, en rute med bare indeksbilde og r12-felt i mod.json
PUBLISERT = {
    "rooms/room022.png": b"codex rom 22",
    "rooms/room022_idx.png": b"idx 22",
    "costumes/costume016_001_hd.png": b"codex brink",
    "costumes/costume016_001_idx.png": b"idx 16-1",
    "costumes/costume008_010_idx.png": b"idx 8-10",
    "objects/obj187_01.png": b"codex sparks",
    "objects/obj187_01_idx.png": b"idx 187",
    "objects/obj187_01_mask.png": b"maske 187",
    "fonts/map.txt": b"kart",
    "fonts/exo2.png": b"skrift",
    "README.md": b"# The Dig HD r12\n",
}

# En ny bygging fra arbeidsbordet: eldre versjoner av det Codex har rettet, og to nye ruter
KANDIDAT = {
    "rooms/room022.png": b"claude rom 22",
    "rooms/room022_idx.png": b"idx 22",
    "costumes/costume016_001_hd.png": b"eldre brink",
    "costumes/costume016_001_idx.png": b"idx 16-1",
    "costumes/costume008_010.png": b"ny mannskapsrute",
    "costumes/costume008_010_idx.png": b"idx 8-10 kandidat",
    "costumes/costume004_000_hd.png": b"robotarm",
    "costumes/costume004_000_idx.png": b"idx 4-0",
    "objects/obj187_01.png": b"gammel sparks",
    "objects/obj187_01_idx.png": b"idx 187",
    "fonts/map.txt": b"kart",
    "fonts/exo2.png": b"skrift",
}


def make_mod(root: Path, files: dict[str, bytes], manifest: dict | None = None, sums: bool = False) -> Path:
    for rel, data in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    (root / "mod.json").write_text(json.dumps(manifest if manifest is not None else
                                              {"format": 1, "created": "kandidat", "rooms": [22], "objects": ["obj187_01"],
                                               "costumes": ["costume004", "costume008", "costume016"]}))
    if sums:
        write_sums(root)
    return root


def write_sums(root: Path) -> Path:
    rows = sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and p.name != "SHA256SUMS")
    (root / "SHA256SUMS").write_text("".join(f"{hashlib.sha256((root / r).read_bytes()).hexdigest()}  {r}\n"
                                             for r in rows))
    return root / "SHA256SUMS"


def published(tmp_path: Path) -> Path:
    return make_mod(tmp_path / "publisert", PUBLISERT,
                    {"format": 1, "created": "2026-10-13T19:56:29+00:00", "rooms": [22], "objects": ["obj187_01"],
                     "costumes": ["costume008", "costume016"], "r12": {"human_visual_approval": False}}, sums=True)


def test_unit_groups_the_files_of_one_image():
    assert unit_of("costumes/costume014_003_hd.png") == "costumes/costume014_003"
    assert unit_of("costumes/costume014_003_idx.png") == "costumes/costume014_003"
    assert unit_of("costumes/costume014_003.png") == "costumes/costume014_003"
    assert unit_of("objects/obj775_0A_mask.png") == "objects/obj775_0A"
    assert unit_of("rooms/room022_idx.png") == "rooms/room022"
    assert unit_of("fonts/exo2.txt") == "fonts"
    assert unit_of("san/SQ1/00012.png") == "san/SQ1/00012.png"
    assert is_image("costumes/costume014_003_hd.png") and is_image("rooms/room022.png")
    assert not is_image("costumes/costume014_003_idx.png") and not is_image("objects/obj187_01_mask.png")


def test_published_units_stay_and_only_new_ones_are_added(tmp_path):
    pub = published(tmp_path)
    cand = make_mod(tmp_path / "kandidat", KANDIDAT)
    out = tmp_path / "ut"
    rep = flett(pub, cand, out)

    # Codex sine rettinger står, også masken kandidaten ikke har
    assert (out / "rooms/room022.png").read_bytes() == b"codex rom 22"
    assert (out / "costumes/costume016_001_hd.png").read_bytes() == b"codex brink"
    assert (out / "objects/obj187_01.png").read_bytes() == b"codex sparks"
    assert (out / "objects/obj187_01_mask.png").read_bytes() == b"maske 187"
    # Ny rute legges til, og en rute som bare hadde indeksbilde, får bildet uten at indeksbildet byttes
    assert (out / "costumes/costume004_000_hd.png").read_bytes() == b"robotarm"
    assert (out / "costumes/costume008_010.png").read_bytes() == b"ny mannskapsrute"
    assert (out / "costumes/costume008_010_idx.png").read_bytes() == b"idx 8-10"

    assert rep["lagt_til"] == ["costumes/costume004_000"]
    assert rep["fylt"] == ["costumes/costume008_010"]
    assert rep["ulik_beholdt"] == ["costumes/costume016_001", "objects/obj187_01", "rooms/room022"]
    assert rep["erstattet"] == rep["fjernet"] == [] and rep["lik"] == 1 and rep["endringer"] == 2

    manifest = json.loads((out / "mod.json").read_text())
    assert manifest["r12"] == {"human_visual_approval": False}
    assert manifest["costumes"] == ["costume004", "costume008", "costume016"]
    runde = manifest["runder"][-1]
    assert runde["grunnlag"] == "2026-10-13T19:56:29+00:00" and runde["lagt_til"] == 2
    assert runde["lagt_til_per_type"] == {"costumes": 2} and runde["ulik_beholdt"] == 3
    assert manifest["created"] != runde["grunnlag"]
    assert (out / "README.md").read_text().startswith("# The Dig HD r12\n")
    assert "2 nye enheter" in (out / "README.md").read_text()

    # SHA256SUMS stemmer med innholdet (sha256sum -c i tools/mod_gren.sh hent)
    sums = modflett.read_sums(out / "SHA256SUMS")
    assert sums == modflett.file_hashes(out)
    assert "mod.json" in (out / "SHA256SUMS").read_text()
    # Den publiserte mappen er ikke rørt
    assert (pub / "costumes/costume008_010.png").exists() is False


def test_replace_takes_the_whole_unit_and_leaves_no_old_soft_cel(tmp_path):
    pub = published(tmp_path)
    files = dict(KANDIDAT)
    del files["costumes/costume016_001_hd.png"]
    files["costumes/costume016_001.png"] = b"ny brink uten myk kant"
    cand = make_mod(tmp_path / "kandidat", files)
    rep = flett(pub, cand, tmp_path / "ut", replace=["costumes/costume016_*"])
    out = tmp_path / "ut"
    # Motoren bruker _hd.png før den vanlige, så den gamle myke ruten må bort
    assert not (out / "costumes/costume016_001_hd.png").exists()
    assert (out / "costumes/costume016_001.png").read_bytes() == b"ny brink uten myk kant"
    assert rep["erstattet"] == ["costumes/costume016_001"]
    assert json.loads((out / "mod.json").read_text())["runder"][-1]["erstattet"] == ["costumes/costume016_001"]


def test_remove_takes_units_out_even_when_the_candidate_has_them(tmp_path):
    pub = published(tmp_path)
    cand = make_mod(tmp_path / "kandidat", KANDIDAT)
    rep = flett(pub, cand, tmp_path / "ut", remove=["objects/obj187_*", "costumes/costume004_000", "rooms/room022"])
    out = tmp_path / "ut"
    assert not list((out / "objects").glob("obj187_01*"))
    assert not (out / "rooms/room022.png").exists()
    assert not (out / "costumes/costume004_000_hd.png").exists()
    assert rep["fjernet"] == ["objects/obj187_01", "rooms/room022"]


def test_check_stops_a_build_from_scratch_and_passes_the_merge(tmp_path):
    pub = published(tmp_path)
    sums = pub / "SHA256SUMS"
    cand = make_mod(tmp_path / "kandidat", KANDIDAT)

    ok, msg = sjekk(sums, cand)
    assert not ok and "Stopper" in msg and "objects/obj187_01_mask.png" in msg
    ok, msg = sjekk(sums, cand, force=True)
    assert ok and "--tving" in msg

    out = tmp_path / "ut"
    flett(pub, cand, out)
    ok, msg = sjekk(sums, out)
    assert ok, msg
    assert "3 nye filer, 0 endret, 0 borte" in msg  # robotarmen (bilde og indeks) og mannskapsruten

    # En publisert fil som forsvinner etterpå, stoppes
    (out / "rooms/room022_idx.png").unlink()
    ok, msg = sjekk(sums, out)
    assert not ok and "rooms/room022_idx.png" in msg


def test_check_allows_what_the_last_round_replaced_or_removed(tmp_path):
    pub = published(tmp_path)
    cand = make_mod(tmp_path / "kandidat", KANDIDAT)
    out = tmp_path / "ut"
    flett(pub, cand, out, replace=["rooms/room022"], remove=["objects/obj187_01"])
    ok, msg = sjekk(pub / "SHA256SUMS", out)
    assert ok, msg
    # Men ikke det en eldre runde erstattet: bare siste runde teller
    second = tmp_path / "ut2"
    flett(out, cand, second)
    shutil.copy2(cand / "costumes/costume016_001_hd.png", second / "costumes/costume016_001_hd.png")
    ok, _ = sjekk(write_sums(out), second)
    assert not ok


def test_nothing_new_gives_its_own_exit_code(tmp_path, capsys):
    pub = published(tmp_path)
    cand = make_mod(tmp_path / "kandidat", KANDIDAT)
    first = tmp_path / "ut"
    assert modflett.main(["flett", "--publisert", str(pub), "--kandidat", str(cand), "--ut", str(first)]) == 0
    again = modflett.main(["flett", "--publisert", str(first), "--kandidat", str(cand), "--ut", str(tmp_path / "ut2"),
                           "--rapport", str(tmp_path / "rapport.json")])
    assert again == INGEN_ENDRING
    assert json.loads((tmp_path / "rapport.json").read_text())["endringer"] == 0
    assert "0 nye enheter" in capsys.readouterr().out


def test_out_must_be_its_own_folder(tmp_path):
    pub = published(tmp_path)
    cand = make_mod(tmp_path / "kandidat", KANDIDAT)
    with pytest.raises(ValueError):
        flett(pub, cand, pub)


def _git(*args, cwd):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


@pytest.mark.skipif(shutil.which("git") is None or shutil.which("bash") is None, reason="trenger git og bash")
def test_mod_gren_send_stops_a_mod_that_loses_published_files(tmp_path):
    """tools/mod_gren.sh mot et lokalt repo: første publisering, en bygging fra null som stoppes, og en flettet."""
    origin = tmp_path / "origin.git"
    _git("init", "-q", "--bare", str(origin), cwd=tmp_path)
    _git("config", "uploadpack.allowFilter", "true", cwd=origin)
    repo = tmp_path / "repo"
    (repo / "tools").mkdir(parents=True)
    (repo / "pipeline" / "dighd").mkdir(parents=True)
    (repo / "work").mkdir()
    shutil.copy2(REPO / "tools" / "mod_gren.sh", repo / "tools")
    shutil.copy2(REPO / "pipeline" / "dighd" / "modflett.py", repo / "pipeline" / "dighd")
    _git("init", "-q", cwd=repo)
    _git("remote", "add", "origin", origin.as_uri(), cwd=repo)

    def gren(*args):
        return subprocess.run(["bash", "tools/mod_gren.sh", *args], cwd=repo, capture_output=True, text=True)

    first = make_mod(tmp_path / "forste", PUBLISERT, {"format": 1, "created": "r12"})
    r = gren("send", str(first))
    assert r.returncode == 0, r.stdout + r.stderr
    assert "finnes ikke ennå" in r.stdout

    scratch = make_mod(tmp_path / "fra-null", KANDIDAT)
    r = gren("send", str(scratch))
    assert r.returncode == 1 and "Stopper" in r.stdout, r.stdout + r.stderr

    r = gren("hent", str(tmp_path / "publisert"))
    assert r.returncode == 0, r.stdout + r.stderr
    flett(tmp_path / "publisert", scratch, tmp_path / "flettet")
    r = gren("send", str(tmp_path / "flettet"))
    assert r.returncode == 0, r.stdout + r.stderr

    r = gren("hent", str(tmp_path / "igjen"))
    assert r.returncode == 0, r.stdout + r.stderr
    igjen = tmp_path / "igjen"
    assert (igjen / "costumes/costume004_000_hd.png").read_bytes() == b"robotarm"
    assert (igjen / "costumes/costume016_001_hd.png").read_bytes() == b"codex brink"
    assert (igjen / "README.md").read_text().startswith("# The Dig HD r12\n")
    # Arbeidskopien er ikke blitt en delvis klone av at sjekksummene ble hentet uten bildene
    promisor = subprocess.run(["git", "config", "--get", "remote.origin.promisor"], cwd=repo, capture_output=True)
    assert promisor.returncode != 0
