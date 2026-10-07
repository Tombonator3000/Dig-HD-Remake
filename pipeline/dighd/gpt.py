"""Jobber for ChatGPT: pakking av oppgaver og mottak av ferdige bilder.

Arbeidsdeling: Claude (koden) lager jobbene og tar imot resultatene. ChatGPT lager
grafikken. Tom flytter filer mellom dem hvis ChatGPT ikke jobber direkte i repoet.

Hver jobb er ett lerret på 1536 x 1024 piksler (standardstørrelsen til ChatGPT sine
bilder, 3:2). Lerretet tilsvarer 384 x 256 originalpiksler i 4x, så et vanlig rom på
320 x 200 får en grå kant rundt seg, og bredere eller høyere rom deles i flere jobber
som overlapper. Da blir hver jobb nøyaktig 4x, uten omregning.

Store objektbilder (nærbilder, kart, paneler som spillet tegner over rommet) blir egne
jobber på samme måte: objektjobber med ID objNNN_SS. Referansen er objektbildet lagt over
rommets bakgrunn der spillet tegner det, så gjennomsiktige deler viser det som er bak.
Resultatet blir objects/objNNN_SS.png i nøyaktig 4x objektstørrelse.

Mottaket sjekker hvert resultat mot originalen:
  - forskyvning (fasekorrelasjon på hele bildet og i blokker, for å se zoom og vridning)
  - likhet i kanter (om formene er de samme)
  - fargeavvik
og låser fargene til originalen (de grove fargene fra originalen, detaljene fra ChatGPT).
Deler av samme rom sys sammen med myk overgang i overlappen.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

from .upscale import upscale_alpha

SCALE = 4
TILE = (384, 256)            # originalpiksler per jobb (gir 1536 x 1024 i 4x)
CANVAS = (TILE[0] * SCALE, TILE[1] * SCALE)
OVERLAP = 64                 # originalpiksler overlapp mellom deler
BORDER = (128, 128, 128)     # grå kant rundt bildet på lerretet

# Grenser for vurdering (originalpiksler). Kan justeres når vi ser ekte resultater.
OK_SHIFT, OK_BLOCK, OK_EDGES = 0.75, 1.0, 0.55
CHECK_SHIFT, CHECK_BLOCK, CHECK_EDGES = 1.5, 2.0, 0.40

# Objektbilder som er så store at de dekker mye av skjermen, blir egne jobber
BIG_AREA, BIG_W, BIG_H = 16000, 200, 150
# Store objekter som ikke blir jobber: ensfargede rutenett i inventaret (rom 93, icons)
SKIP_OBJECTS = {618: "rutenett i inventaret", 627: "rutenett i inventaret"}

PROMPT_BASE = """Task: faithful HD remaster of one background picture from the 1995 adventure game The Dig (LucasArts). This is a production asset. A game engine lays it exactly on top of the original picture, so the geometry must not change at all.

Input: the attached image is the original low-resolution artwork enlarged 4x with hard pixel edges. It sits on a plain gray (#808080) border. The border is only padding.

Do:
- Repaint the picture inside the gray border in high resolution with clean, natural detail: smooth gradients instead of dithering and color banding, crisp edges, believable texture in rock, metal, sky, water and light.
- Keep the original look: the same painted and pre-rendered 1990s LucasArts style, the same colors, light direction, shadows, mood and contrast.
- Keep every shape exactly where it is: outlines, horizon, edges, doorways, machines, stars and highlights must line up with the original pixels.

Do not:
- Do not move, zoom, crop, rotate, mirror or reframe anything. Do not extend the picture into the gray border. Keep the border plain gray (#808080).
- Do not add, remove or replace anything: no new objects, people, creatures, text, symbols or details. Do not fix or reinterpret anything.
- Copy symbols, glyphs, markings and engravings exactly in shape and position.
- No photorealism, no modern 3D look, no film grain, no vignette, no frame, no watermark, no signature.

Output: one image, exactly 1536 x 1024 pixels, with the same layout as the input."""

PROMPT_STYLE = """If a second image is attached, it is an already approved HD picture from the same game. Match its level of detail and brushwork, but take all content, shapes and colors from the first image."""

PROMPT_TILE = """This is part {part} of {parts} of a larger scene. The other parts are made separately and joined afterwards, so keep the edges of the picture natural, with no vignette, frame or fading."""

PROMPT_STATE = """This picture is one of several states of the same image in the game, and the game switches between them. If a second image is attached, it is the approved HD version of the first state. Copy everything that looks the same in both from that second image, so the states match exactly, and only paint the parts that differ."""

PROMPT_OBJECT = """This picture is a large image that the game draws on top of the room, such as a close-up, a map or a panel. Treat it as a background picture and follow all the rules above."""


@dataclass
class Job:
    id: str
    rom: int
    navn: str
    del_nr: int
    deler: int
    rom_storrelse: tuple[int, int]
    region: tuple[int, int, int, int]      # x, y, w, h i bildet: rommet, eller objektbildet (originalpiksler)
    plassering: tuple[int, int]            # hvor regionen ligger på 384 x 256-lerretet
    skala: int = SCALE
    lerret: tuple[int, int] = CANVAS
    type: str = "rom"                      # "rom" eller "objekt"
    objekt: int | None = None              # objekt-ID (bare objektjobber)
    tilstand: str | None = None            # tilstand som i filnavnet, for eksempel "01"
    objekt_i_rom: tuple[int, int, int, int] | None = None   # objektbildets x, y, b, h i rommet

    @property
    def bilde(self) -> str:
        """HD-bildet jobben hører til: roomNNN eller objNNN_SS."""
        if self.type == "objekt":
            return f"obj{self.objekt:03d}_{self.tilstand}"
        return f"room{self.rom:03d}"

    @property
    def storrelse(self) -> tuple[int, int]:
        """Størrelsen på hele bildet (rommet eller objektbildet) i originalpiksler."""
        if self.type == "objekt":
            return (self.objekt_i_rom[2], self.objekt_i_rom[3])
        return (self.rom_storrelse[0], self.rom_storrelse[1])


def _load_job(data: dict) -> Job:
    """Leser jobb.json. Jobber laget før objektjobbene fantes, har ikke type og er romjobber."""
    in_room = data.get("objekt_i_rom")
    return Job(data["id"], data["rom"], data["navn"], data["del_nr"], data["deler"],
               tuple(data["rom_storrelse"]), tuple(data["region"]), tuple(data["plassering"]),
               type=data.get("type") or "rom", objekt=data.get("objekt"), tilstand=data.get("tilstand"),
               objekt_i_rom=tuple(in_room) if in_room else None)


def _order(job: Job) -> tuple:
    """Etter rom, romjobbene før objektjobbene i samme rom, så objekt, tilstand og del."""
    return (job.rom, job.type != "rom", job.objekt or 0, job.tilstand or "", job.del_nr)


# ---------------------------------------------------------------- planlegging

def _positions(size: int, tile: int, overlap: int) -> list[int]:
    if size <= tile:
        return [0]
    n = math.ceil((size - overlap) / (tile - overlap))
    n = max(n, 2)
    return [round(i * (size - tile) / (n - 1)) for i in range(n)]


def plan_tiles(width: int, height: int) -> list[tuple[int, int, int, int, int, int]]:
    """Gir (x, y, w, h, ox, oy) for hver del av et rom."""
    out = []
    for y in _positions(height, TILE[1], OVERLAP):
        for x in _positions(width, TILE[0], OVERLAP):
            w, h = min(width, TILE[0]), min(height, TILE[1])
            ox, oy = (TILE[0] - w) // 2, (TILE[1] - h) // 2
            out.append((x, y, w, h, ox, oy))
    return out


def _is_nearly_empty(im: Image.Image) -> bool:
    colors = im.getcolors(maxcolors=4096)
    return colors is not None and len(colors) < 6


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_notes(path: Path | None) -> dict[int | str, str]:
    """Romnotater (rom = nummer) og objektnotater (rom = objNNN, for eksempel obj241)."""
    if not path or not path.exists():
        return {}
    notes: dict[int | str, str] = {}
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key, note = row.get("rom", "").strip().lower(), row.get("notat", "").strip()
            if not note:
                continue
            if key.isdigit():
                notes[int(key)] = note
            elif re.fullmatch(r"obj\d+", key):
                notes[f"obj{int(key[3:]):03d}"] = note
    return notes


def is_big_object(width: int, height: int) -> bool:
    """Objektbilder som dekker mye av skjermen (nærbilder, kart, paneler) blir egne jobber."""
    return width * height >= BIG_AREA or width >= BIG_W or height >= BIG_H


def object_in_room(room: Image.Image | None, obj: Image.Image, x: int, y: int) -> Image.Image:
    """Objektbildet lagt over rommet der spillet tegner det.

    Gjennomsiktighet: objNNN_SS.png er RGBA med alfa 0 der objNNN_SS_idx.png har fargen som er
    merket gjennomsiktig. Der vises rommet bak. Utenfor rommet (noen UI-objekter er større
    enn rommet sitt) er det svart, som på skjermen.
    """
    obj = obj.convert("RGBA")
    if room is None:
        back = Image.new("RGBA", obj.size, (0, 0, 0, 255))
    else:
        # crop fyller det som ligger utenfor rommet med svart
        back = room.convert("RGB").crop((x, y, x + obj.width, y + obj.height)).convert("RGBA")
    back.alpha_composite(obj)
    return back.convert("RGB")


def _prompt(num: int, notes: dict, part: int, parts: int, is_object: bool = False,
            obj_key: str | None = None, later_state: bool = False) -> str:
    prompt = PROMPT_BASE
    if is_object:
        prompt += "\n\n" + PROMPT_OBJECT
    if obj_key and obj_key in notes:
        # Objektet har eget notat. Romnotatet beskriver rommet bak og kan være feil for objektet.
        prompt += "\n\nNote for this picture: " + notes[obj_key]
    elif num in notes:
        prompt += "\n\nNote for this room: " + notes[num]
    if parts > 1:
        prompt += "\n\n" + PROMPT_TILE.format(part=part, parts=parts)
    return prompt + "\n\n" + (PROMPT_STATE if later_state else PROMPT_STYLE)


def _write_job(jobs_dir: Path, job: Job, image: Image.Image, prompt: str, style_ref: Path | None) -> None:
    """Skriver referanse.png, original_1x.png, prompt.txt og jobb.json for én jobb."""
    x, y, w, h = job.region
    ox, oy = job.plassering
    d = jobs_dir / job.id
    d.mkdir(parents=True, exist_ok=True)
    canvas = Image.new("RGB", CANVAS, BORDER)
    part = image.crop((x, y, x + w, y + h)).resize((w * SCALE, h * SCALE), Image.NEAREST)
    canvas.paste(part, (ox * SCALE, oy * SCALE))
    canvas.save(d / "referanse.png")
    # Originalutsnittet i 1x, til kontroll og til ChatGPT hvis den vil se det
    image.crop((x, y, x + w, y + h)).save(d / "original_1x.png")
    (d / "prompt.txt").write_text(prompt + "\n", encoding="utf-8")

    data = asdict(job)
    data.update({
        "laget": time.strftime("%Y-%m-%d %H:%M"),
        "sha256_referanse": _sha(d / "referanse.png"),
        "sha256_prompt": hashlib.sha256(prompt.encode()).hexdigest(),
        "bilde_i_lerret": [ox * SCALE, oy * SCALE, w * SCALE, h * SCALE],
        "stilreferanse": style_ref.name if style_ref else None,
    })
    (d / "jobb.json").write_text(json.dumps(data, indent=1, ensure_ascii=False))


def make_jobs(extract: Path, out: Path, rooms: set[int] | None = None, notes: dict[int, str] | None = None,
              style_ref: Path | None = None) -> list[Job]:
    meta = json.loads((extract / "rooms.json").read_text())
    jobs_dir = out / "jobber"
    jobs_dir.mkdir(parents=True, exist_ok=True)
    notes = notes or {}
    jobs: list[Job] = []
    skipped = []
    for key, info in sorted(meta["rooms"].items(), key=lambda kv: int(kv[0])):
        num = int(key)
        if rooms and num not in rooms:
            continue
        src = extract / "rooms" / f"room{num:03d}.png"
        room = Image.open(src).convert("RGB") if src.exists() else None
        if room is not None and _is_nearly_empty(room):
            skipped.append(f"rom {num} ({info['name']}): nesten tomt (under 6 farger)")
        elif room is not None:
            tiles = plan_tiles(room.width, room.height)
            for i, (x, y, w, h, ox, oy) in enumerate(tiles):
                jid = f"rom{num:03d}" if len(tiles) == 1 else f"rom{num:03d}_del{i + 1}av{len(tiles)}"
                job = Job(jid, num, info["name"], i + 1, len(tiles), (room.width, room.height),
                          (x, y, w, h), (ox, oy))
                _write_job(jobs_dir, job, room, _prompt(num, notes, i + 1, len(tiles)), style_ref)
                jobs.append(job)
        # Store objektbilder i rommet, også når selve rommet er hoppet over
        jobs += _object_jobs(extract, jobs_dir, num, info, room, notes, style_ref)

    _write_status(out, jobs, {})
    _write_overview(out, jobs, skipped)
    return jobs


def _object_jobs(extract: Path, jobs_dir: Path, num: int, info: dict, room: Image.Image | None,
                 notes: dict[int, str], style_ref: Path | None) -> list[Job]:
    jobs = []
    for obj in info["objects"]:
        if obj["id"] in SKIP_OBJECTS:
            continue
        for state in obj["states"]:
            name = f"obj{obj['id']:03d}_{state}"
            src = extract / "objects" / f"{name}.png"
            if not src.exists():
                continue
            im = Image.open(src)
            if not is_big_object(im.width, im.height):
                continue
            image = object_in_room(room, im, obj["x"], obj["y"])
            tiles = plan_tiles(image.width, image.height)
            for i, (x, y, w, h, ox, oy) in enumerate(tiles):
                jid = name if len(tiles) == 1 else f"{name}_del{i + 1}av{len(tiles)}"
                job = Job(jid, num, info["name"], i + 1, len(tiles), (info["width"], info["height"]),
                          (x, y, w, h), (ox, oy), type="objekt", objekt=obj["id"], tilstand=state,
                          objekt_i_rom=(obj["x"], obj["y"], image.width, image.height))
                prompt = _prompt(num, notes, i + 1, len(tiles), is_object=True, obj_key=f"obj{obj['id']:03d}",
                                 later_state=state != min(obj["states"]))
                _write_job(jobs_dir, job, image, prompt, style_ref)
                jobs.append(job)
    return jobs


def _write_overview(out: Path, jobs: list[Job], skipped: list[str]) -> None:
    n_obj = sum(j.type == "objekt" for j in jobs)
    lines = ["# Jobbliste", "",
             f"{len(jobs)} jobber: {len(jobs) - n_obj} for rom og {n_obj} for store objektbilder. "
             "Status oppdateres i `status.csv` av `dighd gpt-inn`.", "",
             "Objektjobbene (`objNNN_SS`) er store bilder som spillet tegner over rommet (nærbilder, kart, paneler). "
             "Utsnittet er da en del av objektbildet, ikke av rommet.", "",
             "| Jobb | Type | Rom | Navn | Del | Utsnitt (x, y, b, h) |", "| --- | --- | --- | --- | --- | --- |"]
    for j in jobs:
        lines.append(f"| {j.id} | {j.type} | {j.rom} | {j.navn} | {j.del_nr} av {j.deler} | "
                     f"{', '.join(map(str, j.region))} |")
    if skipped:
        lines += ["", "Hoppet over:", ""] + [f"- {s}" for s in skipped]
    (out / "JOBBER.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


STATUS_FIELDS = ["jobb", "type", "rom", "navn", "del", "status", "skift_x", "skift_y", "blokk_maks", "kantlikhet",
                 "fargeavvik", "kommentar"]


def _write_status(out: Path, jobs: list[Job], results: dict[str, dict]) -> None:
    with (out / "status.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=STATUS_FIELDS)
        w.writeheader()
        for j in jobs:
            r = results.get(j.id, {})
            w.writerow({"jobb": j.id, "type": j.type, "rom": j.rom, "navn": j.navn, "del": f"{j.del_nr}/{j.deler}",
                        "status": r.get("status", "ny"), "skift_x": r.get("skift_x", ""),
                        "skift_y": r.get("skift_y", ""), "blokk_maks": r.get("blokk_maks", ""),
                        "kantlikhet": r.get("kantlikhet", ""), "fargeavvik": r.get("fargeavvik", ""),
                        "kommentar": r.get("kommentar", "")})


# ---------------------------------------------------------------- bildeanalyse

def _lum(a: np.ndarray) -> np.ndarray:
    return a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114


def _box(a: np.ndarray, r: int, axis: int) -> np.ndarray:
    if r <= 0:
        return a
    pad = [(0, 0)] * a.ndim
    pad[axis] = (r + 1, r)
    p = np.pad(a, pad, mode="edge")
    c = np.cumsum(p, axis=axis)
    n = a.shape[axis]
    hi = np.take(c, np.arange(2 * r + 1, 2 * r + 1 + n), axis=axis)
    lo = np.take(c, np.arange(0, n), axis=axis)
    return (hi - lo) / (2 * r + 1)


def blur(a: np.ndarray, sigma: float) -> np.ndarray:
    """Tilnærmet gaussisk uskarphet med tre bokseuskarpheter (rask, bare numpy)."""
    if sigma <= 0:
        return a
    r = max(1, int(round(math.sqrt(12 * sigma * sigma / 3 + 1) - 1) // 2))
    out = a.astype(np.float64)
    for _ in range(3):
        out = _box(_box(out, r, 0), r, 1)
    return out


def phase_shift(ref: np.ndarray, img: np.ndarray) -> tuple[float, float, float]:
    """Hvor mye `img` er forskjøvet i forhold til `ref` (dx, dy) og hvor tydelig toppen er."""
    h, w = ref.shape
    win = np.outer(np.hanning(h), np.hanning(w))
    a = np.fft.fft2((ref - ref.mean()) * win)
    b = np.fft.fft2((img - img.mean()) * win)
    r = b * np.conj(a)
    r /= np.abs(r) + 1e-9
    c = np.fft.ifft2(r).real
    py, px = np.unravel_index(np.argmax(c), c.shape)
    peak = c[py, px]

    def sub(cm, c0, cp):
        d = cm - 2 * c0 + cp
        return 0.0 if abs(d) < 1e-12 else 0.5 * (cm - cp) / d

    dy = py + sub(c[(py - 1) % h, px], peak, c[(py + 1) % h, px])
    dx = px + sub(c[py, (px - 1) % w], peak, c[py, (px + 1) % w])
    if dy > h / 2:
        dy -= h
    if dx > w / 2:
        dx -= w
    return float(dx), float(dy), float(peak)


def _edges(l: np.ndarray) -> np.ndarray:
    gy, gx = np.gradient(blur(l, 0.8))
    return np.hypot(gx, gy)


def compare(original: Image.Image, candidate_4x: Image.Image) -> dict:
    """Sammenligner et 4x-resultat med originalutsnittet (1x). Alle mål i originalpiksler."""
    w, h = original.size
    small = candidate_4x.resize((w, h), Image.BOX)
    o = np.asarray(original.convert("RGB"), dtype=np.float64)
    s = np.asarray(small.convert("RGB"), dtype=np.float64)
    lo, ls = _lum(o), _lum(s)
    eo, es = _edges(lo), _edges(ls)
    dx, dy, _ = phase_shift(eo, es)

    # Forskyvning i blokker: avslører zoom, vridning og ting som er flyttet
    block_max = 0.0
    bw, bh = max(48, w // 3), max(48, h // 2)
    if w >= 2 * 48 or h >= 2 * 48:
        for by in range(0, max(1, h - bh + 1), bh):
            for bx in range(0, max(1, w - bw + 1), bw):
                a, b = eo[by:by + bh, bx:bx + bw], es[by:by + bh, bx:bx + bw]
                if a.std() < 1e-3 or b.std() < 1e-3:
                    continue
                bdx, bdy, _ = phase_shift(a, b)
                block_max = max(block_max, math.hypot(bdx, bdy))
    corr = float(np.corrcoef(eo.ravel(), es.ravel())[0, 1]) if eo.std() > 0 and es.std() > 0 else 0.0
    color = float(np.abs(blur(o, 2.0) - blur(s, 2.0)).mean())
    return {"skift_x": round(dx, 2), "skift_y": round(dy, 2), "blokk_maks": round(block_max, 2),
            "kantlikhet": round(corr, 3), "fargeavvik": round(color, 1)}


def judge(m: dict) -> tuple[str, str]:
    shift = math.hypot(m["skift_x"], m["skift_y"])
    if shift <= OK_SHIFT and m["blokk_maks"] <= OK_BLOCK and m["kantlikhet"] >= OK_EDGES:
        return "godkjent", ""
    reasons = []
    if shift > OK_SHIFT:
        reasons.append(f"forskjøvet {m['skift_x']:+.1f}, {m['skift_y']:+.1f} originalpiksler")
    if m["blokk_maks"] > OK_BLOCK:
        reasons.append(f"deler av bildet er flyttet eller zoomet (opptil {m['blokk_maks']:.1f} px)")
    if m["kantlikhet"] < OK_EDGES:
        reasons.append(f"formene ligner for lite på originalen (kantlikhet {m['kantlikhet']:.2f})")
    if shift <= CHECK_SHIFT and m["blokk_maks"] <= CHECK_BLOCK and m["kantlikhet"] >= CHECK_EDGES:
        return "sjekk", "; ".join(reasons)
    return "avvist", "; ".join(reasons)


def lock_colors(candidate: np.ndarray, original_4x: np.ndarray, sigma: float, strength: float) -> np.ndarray:
    """Beholder detaljene fra ChatGPT, men tar de grove fargene fra originalen."""
    if strength <= 0:
        return candidate
    diff = blur(original_4x, sigma) - blur(candidate, sigma)
    return np.clip(candidate + strength * diff, 0, 255)


# ---------------------------------------------------------------- mottak

def detect_layout(size: tuple[int, int], region: tuple[int, int]) -> str | None:
    """Gjenkjenner hvordan et resultat er levert.

    "lerret": hele 1536 x 1024-lerretet med grå kant (3:2), slik referanse.png er.
    "direkte": bare bildet, i samme sideforhold som utsnittet (16:10 for vanlige rom).
    Er utsnittet selv 3:2, er de to like, og lerret brukes (da er det ingen kant).
    """
    aspect = size[0] / size[1]
    canvas = CANVAS[0] / CANVAS[1]
    own = region[0] / region[1]
    if abs(aspect - canvas) / canvas <= 0.02:
        return "lerret"
    if abs(aspect - own) / own <= 0.02:
        return "direkte"
    return None


def _find_result(d: Path) -> Path | None:
    for name in ("resultat.png", "resultat.webp", "resultat.jpg", "resultat.jpeg"):
        if (d / name).exists():
            return d / name
    return None


def import_results(work: Path, extract: Path, out: Path, *, sigma: float = 6.0, strength: float = 1.0,
                   only_approved: bool = False) -> dict:
    jobs_dir = work / "jobber"
    _take_inbox(work / "innboks", jobs_dir)
    preview_dir = work / "forhandsvisning"
    preview_dir.mkdir(parents=True, exist_ok=True)
    (out / "rooms").mkdir(parents=True, exist_ok=True)
    (out / "objects").mkdir(parents=True, exist_ok=True)

    entries = sorted(((_load_job(json.loads(jf.read_text())), jf.parent) for jf in jobs_dir.glob("*/jobb.json")),
                     key=lambda e: _order(e[0]))
    jobs: list[Job] = []
    results: dict[str, dict] = {}
    # Delene til hvert HD-bilde (roomNNN eller objNNN_SS), i jobbrekkefølge
    tiles: dict[str, list[tuple[Job, np.ndarray | None]]] = {}
    for job, d in entries:
        jobs.append(job)
        res_path = _find_result(d)
        if not res_path:
            tiles.setdefault(job.bilde, []).append((job, None))
            continue
        res = Image.open(res_path).convert("RGB")
        x, y, w, h = job.region
        ox, oy = job.plassering
        r = {"resultat": res_path.name, "storrelse": list(res.size), "sha256_resultat": _sha(res_path)}
        layout = detect_layout(res.size, (w, h))
        if layout is None:
            r.update(status="avvist", kommentar=f"feil sideforhold {res.width}x{res.height}: skal være 3:2 som "
                     f"referanse.png (1536x1024) eller {w}:{h} som utsnittet (for eksempel {w * SCALE}x{h * SCALE})")
            results[job.id] = r
            _write_return(d, r)
            tiles.setdefault(job.bilde, []).append((job, None))
            continue
        r["format"] = layout
        if layout == "lerret":
            sx, sy = res.width / CANVAS[0], res.height / CANVAS[1]
            box = (ox * SCALE * sx, oy * SCALE * sy, (ox + w) * SCALE * sx, (oy + h) * SCALE * sy)
            part = res.crop(tuple(round(v) for v in box)).resize((w * SCALE, h * SCALE), Image.LANCZOS)
        else:
            part = res.resize((w * SCALE, h * SCALE), Image.LANCZOS)
        if min(res.width / (w * SCALE), res.height / (h * SCALE)) < 0.6:
            r["merknad"] = "lav oppløsning fra generatoren"
        original = Image.open(d / "original_1x.png").convert("RGB")
        m = compare(original, part)
        status, why = judge(m)
        r.update(m, status=status, kommentar=why)
        orig4 = np.asarray(original.resize((w * SCALE, h * SCALE), Image.LANCZOS), dtype=np.float64)
        locked = lock_colors(np.asarray(part, dtype=np.float64), orig4, sigma, strength)
        results[job.id] = r
        _write_return(d, r)
        _preview(preview_dir / f"{job.id}.png", original, part, locked)
        keep = status == "godkjent" or (status == "sjekk" and not only_approved)
        tiles.setdefault(job.bilde, []).append((job, locked if keep else None))

    _write_status(work, jobs, results)

    provenance = {}
    done_rooms, done_objects, incomplete = [], [], []
    first_state = {}
    for j in jobs:
        if j.type == "objekt":
            first_state[j.objekt] = min(first_state.get(j.objekt, j.tilstand), j.tilstand)
    finished: dict[str, np.ndarray] = {}
    for name, parts in tiles.items():
        first = parts[0][0]
        base = f"obj{first.objekt:03d}_{first_state[first.objekt]}" if first.type == "objekt" else None
        if base and base != name and base not in finished and all(t is not None for _, t in parts):
            # Senere tilstander venter på den første, så de kan bli like der bildene er like
            incomplete.append(f"{name} (rom {first.rom}): venter på {base}")
            continue
        if any(t is None for _, t in parts):
            have = sum(t is not None for _, t in parts)
            if have:
                label = f"rom {first.rom}" if first.type == "rom" else f"{name} (rom {first.rom})"
                incomplete.append(f"{label}: {have} av {len(parts)} deler klare")
            continue
        W, H = first.storrelse
        img = _stitch(W, H, [(j.region, t) for j, t in parts])
        made_by = [{"jobb": j.id, **results[j.id],
                    **{k: v for k, v in json.loads((jobs_dir / j.id / "jobb.json").read_text()).items()
                       if k in ("sha256_referanse", "sha256_prompt", "laget", "stilreferanse")}}
                   for j, _ in parts]
        if first.type == "objekt":
            same_as = None
            if base != name:
                img = match_state(img, finished[base], extract / "objects" / f"{name}_idx.png",
                                  extract / "objects" / f"{base}_idx.png")
                same_as = base
            finished[name] = img
            dest = out / "objects" / f"{name}.png"
            _with_alpha(img, extract / "objects" / f"{name}.png").save(dest)
            done_objects.append(name)
            provenance[name] = {
                "fil": f"objects/{name}.png", "sha256": _sha(dest), "storrelse": [W * SCALE, H * SCALE],
                "type": "objekt", "rom": first.rom, "objekt": first.objekt, "tilstand": first.tilstand,
                "fargelås": {"sigma": sigma, "styrke": strength}, "jobber": made_by,
            }
            if same_as:
                provenance[name]["likt_med"] = same_as
        else:
            dest = out / "rooms" / f"{name}.png"
            Image.fromarray(img).save(dest)
            done_rooms.append(first.rom)
            provenance[name] = {
                "fil": f"rooms/{name}.png", "sha256": _sha(dest), "storrelse": [W * SCALE, H * SCALE],
                "fargelås": {"sigma": sigma, "styrke": strength}, "jobber": made_by,
            }

    prov_path = out / "provenance.json"
    old = json.loads(prov_path.read_text()) if prov_path.exists() else {}
    old.update(provenance)
    prov_path.write_text(json.dumps(old, indent=1, ensure_ascii=False))
    summary = _report(work, jobs, results, sorted(done_rooms), sorted(done_objects), incomplete)
    return summary


def match_state(img: np.ndarray, base_hd: np.ndarray, idx: Path, base_idx: Path, grow: int = 2,
                feather: float = 3.0) -> np.ndarray:
    """Gjør en senere tilstand lik den første der originalbildene er like.

    Der indeksbildene er like (med en margin på `grow` originalpiksler), brukes HD-bildet til den
    første tilstanden. Bare det som er forskjellig, tas fra ChatGPT-bildet for denne tilstanden.
    Overgangen mykes opp med `feather` HD-piksler. Da skifter ikke hender og bakgrunn utseende
    når spillet bytter tilstand.
    """
    a, b = np.asarray(Image.open(idx)), np.asarray(Image.open(base_idx))
    if a.shape != b.shape or base_hd.shape != img.shape:
        return img
    diff = Image.fromarray(((a != b) * 255).astype(np.uint8))
    if grow:
        diff = diff.filter(ImageFilter.MaxFilter(2 * grow + 1))
    mask = np.asarray(diff.resize((img.shape[1], img.shape[0]), Image.NEAREST), dtype=np.float64) / 255
    if feather:
        mask = np.clip(blur(mask, feather), 0, 1)
    out = base_hd.astype(np.float64) * (1 - mask[..., None]) + img.astype(np.float64) * mask[..., None]
    return np.clip(np.rint(out), 0, 255).astype(np.uint8)


def _with_alpha(img: np.ndarray, original: Path) -> Image.Image:
    """HD-objektbildet som RGBA med gjennomsiktigheten fra originalen (skarpe kanter, som i modden)."""
    hd = Image.fromarray(img).convert("RGBA")
    if original.exists():
        o = Image.open(original).convert("RGBA")
        if (o.width * SCALE, o.height * SCALE) == hd.size:
            hd.putalpha(upscale_alpha(o.getchannel("A"), SCALE))
    return hd


def _take_inbox(inbox: Path, jobs_dir: Path) -> None:
    """Bilder lagt i work/gpt/innboks/ med jobbnavnet (for eksempel rom022.png) flyttes inn i jobben."""
    if not inbox.is_dir():
        return
    for f in sorted(inbox.iterdir()):
        if f.suffix.lower() not in (".png", ".webp", ".jpg", ".jpeg") or not (jobs_dir / f.stem).is_dir():
            continue
        d = jobs_dir / f.stem
        old = _find_result(d)
        if old:
            old.rename(d / f"forrige_{time.strftime('%Y%m%d_%H%M%S')}{old.suffix}")
        f.rename(d / f"resultat{f.suffix.lower()}")


def _write_return(d: Path, r: dict) -> None:
    ret = d / "retur.md"
    if r["status"] == "godkjent":
        if ret.exists():
            ret.unlink()
        return
    text = [f"# {d.name}: {r['status']}", "", f"Grunn: {r.get('kommentar') or 'se status.csv'}", "",
            "Forslag til nytt forsøk (lim inn sammen med referanse.png):", "", "```text",
            "Precise correction of the attached HD picture. The previous result did not line up with the original. "
            "Start again from referanse.png and keep every outline, edge and object at exactly the same pixel position "
            "as in that image. Do not zoom, shift, crop or reframe. Keep the gray border plain gray. "
            "Same size 1536 x 1024.", "```"]
    ret.write_text("\n".join(text) + "\n", encoding="utf-8")


def _preview(path: Path, original: Image.Image, part: Image.Image, locked: np.ndarray) -> None:
    w, h = part.size
    a = original.resize((w, h), Image.NEAREST)
    c = Image.fromarray(locked.astype(np.uint8))
    sheet = Image.new("RGB", (w * 3 + 16, h), (24, 24, 28))
    for i, im in enumerate((a, part, c)):
        sheet.paste(im, (i * (w + 8), 0))
    if sheet.width > 2400:
        sheet = sheet.resize((2400, round(sheet.height * 2400 / sheet.width)), Image.LANCZOS)
    sheet.save(path)


def _stitch(W: int, H: int, parts: list[tuple[tuple[int, int, int, int], np.ndarray]]) -> np.ndarray:
    acc = np.zeros((H * SCALE, W * SCALE, 3))
    wsum = np.zeros((H * SCALE, W * SCALE, 1))
    ramp = OVERLAP * SCALE
    for (x, y, w, h), img in parts:
        wx = np.ones(w * SCALE)
        wy = np.ones(h * SCALE)
        idx = np.arange(w * SCALE) + 0.5
        if x > 0:
            wx = np.minimum(wx, idx / ramp)
        if x + w < W:
            wx = np.minimum(wx, (w * SCALE - idx) / ramp)
        idy = np.arange(h * SCALE) + 0.5
        if y > 0:
            wy = np.minimum(wy, idy / ramp)
        if y + h < H:
            wy = np.minimum(wy, (h * SCALE - idy) / ramp)
        weight = np.clip(np.outer(wy, wx), 1e-4, 1)[..., None]
        acc[y * SCALE:(y + h) * SCALE, x * SCALE:(x + w) * SCALE] += img * weight
        wsum[y * SCALE:(y + h) * SCALE, x * SCALE:(x + w) * SCALE] += weight
    return np.clip(acc / np.maximum(wsum, 1e-9), 0, 255).astype(np.uint8)


def _done_line(label: str, done: list, total: int) -> str:
    return f"Ferdige {label}: {len(done)} av {total}" + (f" ({', '.join(map(str, done))})" if done else "")


def _report(work: Path, jobs: list[Job], results: dict[str, dict], done_rooms: list[int], done_objects: list[str],
            incomplete: list[str]) -> dict:
    counts: dict[str, int] = {}
    by_type: dict[tuple[str, str], int] = {}
    for j in jobs:
        s = results.get(j.id, {}).get("status", "ny")
        counts[s] = counts.get(s, 0) + 1
        by_type[(j.type, s)] = by_type.get((j.type, s), 0) + 1
    rooms_total = len({j.rom for j in jobs if j.type == "rom"})
    objects_total = len({j.bilde for j in jobs if j.type == "objekt"})
    lines = ["# Rapport fra gpt-inn", "", time.strftime("Laget %Y-%m-%d %H:%M"), "",
             "| Status | Romjobber | Objektjobber |", "| --- | --- | --- |"]
    lines += [f"| {s} | {by_type.get(('rom', s), 0)} | {by_type.get(('objekt', s), 0)} |" for s in sorted(counts)]
    lines += ["", f"- {_done_line('rom', done_rooms, rooms_total)}",
              f"- {_done_line('objekter', done_objects, objects_total)}"]
    if incomplete:
        lines += ["", "Bilder som venter på flere deler:", ""] + [f"- {s}" for s in incomplete]
    bad = [(j, results[j.id]) for j in jobs if results.get(j.id, {}).get("status") in ("avvist", "sjekk")]
    if bad:
        lines += ["", "Må sees på (se `retur.md` i jobbmappen):", "", "| Jobb | Status | Grunn |", "| --- | --- | --- |"]
        lines += [f"| {j.id} | {r['status']} | {r.get('kommentar', '')} |" for j, r in bad]
    lines += ["", "Forhåndsvisning per jobb i `forhandsvisning/`: original 4x, ChatGPT, etter fargelås."]
    (work / "RAPPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"status": counts, "ferdige_rom": done_rooms, "ferdige_objekter": done_objects,
            "rom_totalt": rooms_total, "objekter_totalt": objects_total, "venter": incomplete}


# ---------------------------------------------------------------- ordre til ChatGPT

def read_status(work: Path) -> list[dict]:
    """Leser status.csv. Eldre filer uten kolonnen type har bare romjobber."""
    path = work / "status.csv"
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["type"] = (r.get("type") or "").strip() or "rom"
    return rows


_OBJ_ID = re.compile(r"obj(\d+)_([0-9A-Za-z]+)")


def _image_of(row: dict) -> str:
    """HD-bildet en rad i status.csv hører til: roomNNN eller objNNN_SS (jobb-ID uten delnummer)."""
    m = _OBJ_ID.match(row["jobb"]) if row["type"] == "objekt" else None
    if m:
        return m.group(0)
    return row["jobb"] if row["type"] == "objekt" else f"room{int(row['rom']):03d}"


def work_queue(rows: list[dict]) -> list[dict]:
    """Alle jobber som ikke er godkjent, i den rekkefølgen ChatGPT skal ta dem.

    Avviste først. Så nye etter romnummer, romjobbene før objektjobbene i samme rom; objektjobber
    i rom som allerede er ferdige, kommer først blant de nye, så rommet blir helt ferdig. Til slutt
    de som er godtatt foreløpig, men kan bli bedre (sjekk).
    """
    room_rows = [r for r in rows if r["type"] == "rom"]
    rooms_done = {int(r["rom"]) for r in room_rows} - {int(r["rom"]) for r in room_rows if r["status"] != "godkjent"}
    retry = [r for r in rows if r["status"] == "avvist"]
    fresh = sorted((r for r in rows if r["status"] == "ny"),
                   key=lambda r: (not (r["type"] == "objekt" and int(r["rom"]) in rooms_done),
                                  int(r["rom"]), r["type"] != "rom"))
    better = [r for r in rows if r["status"] == "sjekk"]
    return retry + fresh + better


def write_list(work: Path, batch: int = 10) -> Path:
    """Skriver GRAFIKKLISTE.md: alt ChatGPT skal lage, i rekkefølge og delt i bestillinger.

    Bestilling 1 er det samme som står i ORDRE.md. Når den er levert, tar ChatGPT neste
    bestilling uten å vente på ny ordre.
    """
    rows = read_status(work)
    queue = work_queue(rows)
    done = [r for r in rows if r["status"] == "godkjent"]
    room_rows = [r for r in rows if r["type"] == "rom"]
    obj_rows = [r for r in rows if r["type"] == "objekt"]
    rooms_all = {int(r["rom"]) for r in room_rows}
    rooms_done = rooms_all - {int(r["rom"]) for r in room_rows if r["status"] != "godkjent"}
    objects_all = {_image_of(r) for r in obj_rows}
    objects_done = objects_all - {_image_of(r) for r in obj_rows if r["status"] != "godkjent"}

    def label(r: dict) -> str:
        what = f"rom {r['rom']} {r['navn']}"
        m = _OBJ_ID.match(r["jobb"]) if r["type"] == "objekt" else None
        if m:
            what += f", objekt {int(m.group(1))} tilstand {m.group(2)}"
        if r["del"] not in ("1/1", ""):
            what += f", del {r['del']}"
        note = {"avvist": " (avvist, les retur.md)", "sjekk": " (kan bli bedre)"}.get(r["status"], "")
        return f"`{r['jobb']}` ({what}){note}"

    lines = ["# Grafikkliste", "", time.strftime("Oppdatert %Y-%m-%d %H:%M (norsk tid)"), "",
             "Alt som skal lages til The Dig HD Remake, i den rekkefølgen det skal lages. "
             "Bestilling 1 er det samme som står i `ORDRE.md`. Når en bestilling er levert, tar du neste "
             "uten å vente på ny ordre. Hopp over jobber som er krysset av.", "",
             "## Oversikt", "",
             "| Del | Ferdig | Totalt | Når |", "| --- | --- | --- | --- |",
             f"| Rombakgrunner | {len(rooms_done)} | {len(rooms_all)} | Nå, bestillingene under ({len(room_rows)} jobber, brede og høye rom er delt) |",
             f"| Store objektbilder (nærbilder, kart, trikken) | {len(objects_done)} | {len(objects_all)} | Nå, sammen med rommene |",
             "| Andre objektbilder (610) | 0 | 610 | Senere, egen bestilling når rommene er ferdige |",
             "| Figurer (modellark for Boston, Maggie og Brink) | 0 | 3 | Senere, egen bestilling |",
             "| Filmrammer (12 638) | 0 | 12 638 | Senere, egen bestilling |", ""]
    for i in range(0, len(queue), batch):
        part = queue[i:i + batch]
        n = i // batch + 1
        rooms = sorted({int(r["rom"]) for r in part})
        lines += [f"## Bestilling {n}" + (" (nå, samme som ORDRE.md)" if n == 1 else ""), "",
                  f"Rom {', '.join(map(str, rooms))}.", ""]
        lines += [f"- [ ] {label(r)}" for r in part]
        lines.append("")
    if not queue:
        lines += ["## Bestillinger", "", "Alle jobber er levert og godkjent.", ""]
    lines += ["## Ferdig", ""]
    lines += [f"- [x] `{r['jobb']}` (rom {r['rom']} {r['navn']})" for r in done] or ["Ingen ennå."]
    path = work / "GRAFIKKLISTE.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_orders(work: Path, batch: int = 10, anchors: list[str] | None = None,
                 messages: list[str] | None = None, tasks: Path | None = None) -> Path:
    """Skriver ORDRE.md: status, neste jobber og beskjeder. ChatGPT leser denne først."""
    rows = read_status(work)
    counts: dict[str, int] = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    room_rows = [r for r in rows if r["type"] == "rom"]
    obj_rows = [r for r in rows if r["type"] == "objekt"]
    # Et rom er ferdig når romjobbene er godkjent, uavhengig av objektene
    rooms_all = {int(r["rom"]) for r in room_rows}
    rooms_done = sorted(rooms_all - {int(r["rom"]) for r in room_rows if r["status"] != "godkjent"})
    objects_all = {_image_of(r) for r in obj_rows}
    objects_done = sorted(objects_all - {_image_of(r) for r in obj_rows if r["status"] != "godkjent"})

    queue = work_queue(rows)[:batch]

    lines = ["# Ordre fra Claude", "", time.strftime("Oppdatert %Y-%m-%d %H:%M (norsk tid)"), "",
             "Les denne filen før du starter. Den erstatter tidligere ordre.", "",
             "## Status", "",
             f"- Jobber: {len(rows)}. " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())),
             f"- {_done_line('rom', rooms_done, len(rooms_all))}"]
    if obj_rows:
        lines.append(f"- {_done_line('objekter', objects_done, len(objects_all))}")
    lines += ["", "## Gjør disse nå", ""]
    if not queue:
        lines.append("Alle jobber er levert. Vent på ny bestilling.")
    for i, r in enumerate(queue, 1):
        why = ""
        if r["status"] == "avvist":
            why = f" Avvist: {r['kommentar']}. Les retur.md."
        elif r["status"] == "sjekk":
            why = f" Godtatt foreløpig, men kan bli bedre: {r['kommentar']}."
        what = f"rom {r['rom']}, {r['navn']}"
        m = _OBJ_ID.match(r["jobb"]) if r["type"] == "objekt" else None
        if m:
            what += f", objekt {int(m.group(1))} tilstand {m.group(2)}"
            states = sorted({_OBJ_ID.match(o["jobb"]).group(2) for o in obj_rows
                             if _OBJ_ID.match(o["jobb"]) and _OBJ_ID.match(o["jobb"]).group(1) == m.group(1)})
            if m.group(2) != states[0]:
                first = f"obj{m.group(1)}_{states[0]}"
                why += (f" Legg ved `jobber/{first}/resultat.png` som bilde to (ikke stilankeret), så tilstandene "
                        f"blir like. Lag denne etter {first}.")
        lines.append(f"{i}. `{r['jobb']}` ({what}, del {r['del']}).{why}")
    if queue:
        lines += ["", "Når disse er levert, fortsett med bestilling 2 i `GRAFIKKLISTE.md` uten å vente på ny ordre."]
    lines += ["", "## Stilankere", ""]
    if anchors:
        lines += [f"- `stil/{a}`" for a in anchors]
        lines += ["", "Legg ved det ankeret som ligner mest på rommet som bilde to."]
    else:
        lines.append("Ingen ennå.")
    lines += ["", "## Leveringsformat", "",
              "Begge formatene godtas av kontrollen:", "",
              "- `resultat.png` på 1536 x 1024 med samme grå kant som `referanse.png`.",
              "- `resultat.png` med bare bildet, i samme sideforhold som utsnittet (16:10 for vanlige rom, "
              "minst 1280 x 800). Slik pilotbildene ble levert.", "",
              "Objektjobbene (`objNNN_SS`) er store bilder som spillet tegner over rommet (nærbilder, kart, "
              "paneler). De lages og leveres på samme måte. Utsnittet er da objektbildet, så leverer du bare "
              "bildet, skal det ha objektets sideforhold (se `bilde_i_lerret` i `jobb.json`).", "",
              "Skriv `notat.md` i jobbmappen. Commit 5 til 10 jobber om gangen i grenen `gpt-arbeid` og push.", ""]
    if messages:
        lines += ["## Beskjeder", ""] + [f"- {m}" for m in messages] + [""]
    if tasks and tasks.exists() and tasks.read_text(encoding="utf-8").strip():
        lines += ["## Kodeoppgaver", "", tasks.read_text(encoding="utf-8").strip(), ""]
    lines += ["## Neste sjekk", "", "Claude henter grenen omtrent hver halvtime, kontrollerer leveransene, "
              "oppdaterer `status.csv`, `RAPPORT.md` og `retur.md`, og skriver ny ordre her."]
    path = work / "ORDRE.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
