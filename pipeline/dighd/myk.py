"""Mottak for figurark i den glatte stilen: ekte alfa, myke kanter og eget omriss.

Figurarkene ChatGPT/Codex tegner nå, følger ikke originalens piksler. Figurene er tegnet på nytt i en
annen størrelse og litt andre steder på arket, og kantene er myke. De kan ikke klippes ut med
originalens maske (det gamle mottaket i figur.py), for da kommer trappetrinnene tilbake. For hver
rute på arket gjør mottaket dette:

1. Finner delene av tegningen som hører til ruten: rutekartet grafikeren leverte (boksene rundt
   hver del), ellers rad og rekkefølge på arket.
2. Skalerer med én faktor per gruppe på arket, slik at figurene får originalens høyde, og
   tilpasser så hver rute til originalens omriss i bredde og høyde (innenfor FIT_RANGE). Grafikeren
   tegner rutene litt ulikt i størrelse og form; originalen er jevn. Når hver rute får originalens mål,
   skifter ikke figuren størrelse eller form mellom rutene (Tom 10. oktober: astronautene skiftet
   størrelse når de snakket). Tilpasningen brukes bare når den ikke dekker originalen tydelig dårligere.
3. Plasserer tegningen over originalruten i 4x der omrisset dekker originalen best, med fotfeste
   og midtpunkt som start.
4. Skriver costumes/costumeCCC_NNN_hd.png: ruten i 4x med en marg rundt (like stor på begge sider),
   med tegningens egen alfa.

Motoren legger bildet over HD-bakgrunnen med myke kanter, bak forgrunnen og under tekst og menyer
(docs/HD-MOTOR.md, myke figurer). Svært små originalruter (løsrevne hudflekker og lignende) som ikke
har en egen del på arket, skaleres mykt opp fra originalen, som grafikeren ba om.

Versjon 3 (11. oktober, etter Codex sine målinger):
- Tekniske magentapiksler i originalen (skyggemerker, motoren tegner dem som skygge) regnes ikke med
  i mål, plassering eller fragmenter. En rute med bare slike piksler får ikke noe HD-bilde.
- Små løsrevne utliggere langt fra resten av ruten (Pig 064 har én svart piksel 120 piksler unna)
  styrer ikke skala og fotfeste. De legges inn fra originalen der tegningen ikke har dem.
- Tilpasningen per rute brukes i en retning bare når tegningene i gruppen varierer mer i den retningen
  enn originalene. Ellers får munnstillingene samme hode (ingen «hodepuls»).
- Ruter kan tas fra egne rettingsark (fra-claude/mottak-per-rute.json på arbeidsbordet).
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path

import numpy as np
from PIL import Image

SCALE = 4
CORE = 128        # alfa for kjernen av en del av tegningen
REACH = 10        # myke kanter: piksler med alfa så langt utenfor kjernen hører til den
MIN_PAD = 2       # minste marg rundt ruten, i originalpiksler
MAX_PAD = 24      # største marg; det som stikker lenger ut, kuttes
SEARCH = 16       # hvor langt plasseringen prøves flyttet, i HD-piksler
SMALL = 40        # originalruter med færre synlige piksler regnes som fragmenter
GOOD_IOU = 0.6    # under dette er omrisset så ulikt originalen at ruten må ses på
GOOD_COVER = 0.8  # andel av originalens piksler tegningen må dekke
FIT_RANGE = 0.12  # hvor mye hver rute kan skaleres bort fra gruppens faktor, i bredde og høyde for seg
FIT_SLACK = 0.03  # tilpasningen brukes når snitt/union er høyst så mye dårligere enn med gruppens faktor
VERSION = 3       # økes når mottaket endres, så alle ark tas inn på nytt
FIT_SPREAD = 0.03 # tilpasning per rute i en retning bare når tegningene sprer mer enn originalene pluss dette
OUTLIER_GAP = 6   # en liten del av originalen så langt unna resten (originalpiksler) er en utligger
OUTLIER_MAX = 0.02  # ... og høyst denne andelen av rutens piksler (minst 4 piksler)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ------------------------------------------------------------------ originalens mål

def technical(rgba: np.ndarray) -> np.ndarray:
    """Tekniske magentapiksler (skyggemerker som 255,87,255 og 255,63,255): spillet tegner dem gjennom
    skyggetabellen, så de er ikke en del av figurens form."""
    r, g, b = (rgba[..., k].astype(np.int16) for k in range(3))
    return (rgba[..., 3] > 0) & (r >= 230) & (b >= 230) & (g <= 120)


def measure_mask(rgba: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Pikslene i originalruten som bestemmer mål og plassering, og utliggerne. Tekniske piksler er med
    i ingen av dem. En utligger er en del (8-naboer) med høyst OUTLIER_MAX av pikslene (minst 4) som
    ligger mer enn OUTLIER_GAP originalpiksler fra resten."""
    from scipy import ndimage

    real = (rgba[..., 3] > 0) & ~technical(rgba)
    total = int(real.sum())
    if total == 0:
        return real, np.zeros_like(real)
    lab, n = ndimage.label(real, structure=np.ones((3, 3), bool))
    if n <= 1:
        return real, np.zeros_like(real)
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    limit = max(4, OUTLIER_MAX * total)
    keep = np.isin(lab, [i + 1 for i in range(n) if sizes[i] > limit])
    if not keep.any():
        return real, np.zeros_like(real)
    dist = ndimage.distance_transform_edt(~keep)
    outlier = np.zeros_like(real)
    for i in range(n):
        if sizes[i] <= limit:
            comp = lab == i + 1
            if dist[comp].min() > OUTLIER_GAP:
                outlier |= comp
    return real & ~outlier, outlier


def _masked(rgba: np.ndarray, mask: np.ndarray) -> np.ndarray:
    out = rgba.copy()
    out[~mask] = 0
    return out


# ------------------------------------------------------------------ leveranser og rutekart

def deliveries(gren: Path) -> list[dict]:
    """De leverte arkene i glatt stil: `leveranser` i rapporter/*/fremdrift.json på arbeidsgrenen.
    Hver har jobb, resultat (stien til PNG-en) og sha256. Senere oppføringer for samme jobb vinner."""
    out: dict[str, dict] = {}
    for f in sorted(gren.glob("rapporter/*/fremdrift.json")):
        for d in json.loads(f.read_text()).get("leveranser", []):
            if d.get("jobb") and d.get("resultat"):
                out[d["jobb"]] = d
    return list(out.values())


def _del_number(path: Path) -> tuple:
    m = re.search(r"(\d+)", path.stem)
    return (path.parent.name, int(m.group(1)) if m else 0, path.stem)


# Navnene grafikeren har brukt på boksen rundt delen av tegningen (x, y, b, h, alfa over 128)
BOX_KEYS = ("ny_diagnostisk_rekt_alfa128", "drawn_bbox_alpha128", "native_analyseboks_alfa128", "rect")


def _boxes(rows: list) -> dict[str, list[int]]:
    boxes = {}
    for r in rows:
        box = next((r[k] for k in BOX_KEYS if r.get(k)), None)
        if r.get("bilde") and box and len(box) == 4:
            boxes[r["bilde"]] = [int(v) for v in box]
    return boxes


def accepted_sources(gren: Path) -> dict[str, dict]:
    """Ark Claude har tatt imot fra egne kilder (fra-claude/mottak-per-rute.json på arbeidsbordet):
    jobb -> {"base_native": sti, "base_map": sti, "overrides": [{"bilde", "native_png",
    "native_analyseboks_alfa128"}]}. Samme form som grafikerens forslag (mottaksforslag-per-rute.json).
    For disse jobbene brukes base_native og kartet i stedet for leveransen, og hver rute i overrides
    tas fra sitt eget rettingsark."""
    f = gren / "fra-claude" / "mottak-per-rute.json"
    try:
        return json.loads(f.read_text()).get("jobs", {})
    except (OSError, json.JSONDecodeError):
        return {}


def load_map(path: Path, job: str) -> dict[str, list[int]]:
    """Et rutekart i en egen fil: enten jobb -> {"koblinger": [...]} eller koblingene rett i filen."""
    data = json.loads(path.read_text())
    if isinstance(data.get(job), dict):
        data = data[job]
    return _boxes(data.get("ruter") or data.get("entries") or data.get("koblinger") or [])


def route_maps(gren: Path) -> dict[str, dict[str, list[int]]]:
    """Rutekartene fra grafikeren: jobb -> rute (costumeCCC_NNN) -> boksen [x, y, b, h] rundt delen av
    tegningen med alfa over 128. Radene ligger under "ruter", "entries" eller "koblinger", boksen under et
    av navnene i BOX_KEYS. Senere deler (høyere nummer) vinner."""
    maps: dict[str, dict[str, list[int]]] = {}
    for f in sorted(gren.glob("rapporter/*/rutekart*.json"), key=_del_number):
        try:
            data = json.loads(f.read_text())
        except json.JSONDecodeError:
            continue
        for job, d in data.items():
            if not isinstance(d, dict):
                continue
            boxes = _boxes(d.get("ruter") or d.get("entries") or d.get("koblinger") or [])
            if boxes:
                maps[job] = boxes
    return maps


# ------------------------------------------------------------------ delene av tegningen

def parts(alpha: np.ndarray) -> tuple[np.ndarray, np.ndarray, list[dict]]:
    """Delene av tegningen: sammenhengende kjerner (alfa >= CORE), og for hver piksel med alfa hvilken
    kjerne den hører til (den nærmeste innen REACH piksler, 0 for ingen). Gir eiermatrisen, kjernene
    (nummer per piksel) og delene med nummer, areal, boks (x, y, b, h) og tyngdepunkt."""
    from scipy import ndimage

    core = alpha >= CORE
    lab, n = ndimage.label(core, structure=np.ones((3, 3), bool))
    if n == 0:
        return np.zeros(alpha.shape, np.int32), lab, []
    dist, (iy, ix) = ndimage.distance_transform_edt(~core, return_indices=True)
    owner = lab[iy, ix]
    owner[(alpha == 0) | (dist > REACH)] = 0
    found = []
    areas = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    centres = ndimage.center_of_mass(core, lab, range(1, n + 1))
    for i, sl in enumerate(ndimage.find_objects(lab), start=1):
        found.append({"nr": i, "areal": int(areas[i - 1]),
                      "boks": [sl[1].start, sl[0].start, sl[1].stop - sl[1].start, sl[0].stop - sl[0].start],
                      "senter": [float(centres[i - 1][1]), float(centres[i - 1][0])]})
    return owner, lab, found


def _overlap(box_a: list[int], lab: np.ndarray, nr: int, box_b: list[int]) -> int:
    """Kjernepiksler i del nr som ligger i boks b."""
    x0, y0 = max(box_a[0], box_b[0]), max(box_a[1], box_b[1])
    x1 = min(box_a[0] + box_a[2], box_b[0] + box_b[2])
    y1 = min(box_a[1] + box_a[3], box_b[1] + box_b[3])
    if x1 <= x0 or y1 <= y0:
        return 0
    return int((lab[y0:y1, x0:x1] == nr).sum())


def assign_by_map(cels: list[dict], found: list[dict], core_lab: np.ndarray, boxes: dict[str, list[int]]
                  ) -> dict[str, list[int]]:
    """Delene til hver rute etter rutekartet: en del hører til ruten der boksen dekker mest av den,
    når boksen dekker minst halvparten."""
    out: dict[str, list[int]] = {c["bilde"]: [] for c in cels}
    for p in found:
        best, best_n = None, 0
        for c in cels:
            box = boxes.get(c["bilde"])
            if box:
                n = _overlap(p["boks"], core_lab, p["nr"], box)
                if n > best_n:
                    best, best_n = c["bilde"], n
        if best and best_n * 2 >= p["areal"]:
            out[best].append(p["nr"])
    return out


def _rows(items: list[tuple[float, float, float]]) -> list[list[int]]:
    """Grupperer (x, y, høyde) i rader etter y: ny rad når midten ligger mer enn en halv typisk høyde
    under forrige. Gir indeksene per rad, sortert etter x."""
    if not items:
        return []
    order = sorted(range(len(items)), key=lambda i: items[i][1])
    typical = float(np.median([h for _, _, h in items])) or 1.0
    rows: list[list[int]] = [[order[0]]]
    for i in order[1:]:
        if items[i][1] - items[rows[-1][-1]][1] > typical / 2:
            rows.append([])
        rows[-1].append(i)
    return [sorted(r, key=lambda i: items[i][0]) for r in rows]


def assign_by_rows(cels: list[dict], found: list[dict], min_area: int) -> dict[str, list[int]] | None:
    """Uten rutekart: rutene og de store delene i samme rader og samme rekkefølge. Gir None når
    antallet rader eller deler per rad ikke stemmer."""
    big = [p for p in found if p["areal"] >= min_area]
    cel_items = [(c["synlig"][0] + c["synlig"][2], c["synlig"][1] + c["synlig"][3],
                  c["synlig"][3] - c["synlig"][1]) for c in cels]  # x0+x1 og y0+y1: dobbel midte
    cel_items = [(x / 2, y / 2, h) for x, y, h in cel_items]
    part_items = [(p["senter"][0], p["boks"][1] + p["boks"][3] / 2, p["boks"][3]) for p in big]
    cr, pr = _rows(cel_items), _rows(part_items)
    if len(cr) != len(pr) or any(len(a) != len(b) for a, b in zip(cr, pr)):
        return None
    out = {c["bilde"]: [] for c in cels}
    for a, b in zip(cr, pr):
        for ci, pi in zip(a, b):
            out[cels[ci]["bilde"]].append(big[pi]["nr"])
    return out


# ------------------------------------------------------------------ tilpasning

def _premul_resize(rgba: np.ndarray, size: tuple[int, int]) -> np.ndarray:
    """Skalerer RGBA med forhåndsmultiplisert alfa (ingen mørke eller lyse rander) og Lanczos."""
    im = Image.fromarray(rgba, "RGBA").convert("RGBa").resize(size, Image.LANCZOS)
    return np.asarray(im.convert("RGBA"))


def _iou(a: np.ndarray, o: np.ndarray, ox: int, oy: int) -> tuple[float, float]:
    """Hvor godt masken a (plassert med øvre venstre hjørne i ox, oy) dekker originalmasken o:
    snitt over union, og andelen av o som dekkes."""
    ha, wa = a.shape
    ho, wo = o.shape
    x0, y0 = max(ox, 0), max(oy, 0)
    x1, y1 = min(ox + wa, wo), min(oy + ha, ho)
    inter = 0
    if x1 > x0 and y1 > y0:
        inter = int((a[y0 - oy:y1 - oy, x0 - ox:x1 - ox] & o[y0:y1, x0:x1]).sum())
    sa, so = int(a.sum()), int(o.sum())
    union = sa + so - inter
    return (inter / union if union else 0.0), (inter / so if so else 0.0)


def best_offset(a: np.ndarray, o: np.ndarray, start: tuple[int, int]) -> tuple[int, int, float, float]:
    """Plasseringen av a over o med best snitt over union, søkt rundt start: grovt med steg 2,
    så fint rundt det beste. Gir (ox, oy, snitt over union, dekning)."""
    best = (start[0], start[1], *_iou(a, o, *start))
    for dy in range(-SEARCH, SEARCH + 1, 2):
        for dx in range(-SEARCH, SEARCH + 1, 2):
            v = _iou(a, o, start[0] + dx, start[1] + dy)
            if v[0] > best[2]:
                best = (start[0] + dx, start[1] + dy, *v)
    cx, cy = best[0], best[1]
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            v = _iou(a, o, cx + dx, cy + dy)
            if v[0] > best[2]:
                best = (cx + dx, cy + dy, *v)
    return best


def _bottom(mask: np.ndarray) -> int:
    rows = np.nonzero(mask.any(axis=1))[0]
    return int(rows[-1]) if len(rows) else mask.shape[0] - 1


def _centre_x(mask: np.ndarray) -> float:
    xs = np.nonzero(mask)[1]
    return float(xs.mean()) if len(xs) else mask.shape[1] / 2


def fit_scales(drawing: np.ndarray, original: np.ndarray, scale: float,
               fit: tuple = (True, True)) -> tuple[float, float]:
    """Faktorene i bredde og høyde som gir tegningens kjerne samme mål som originalens omriss i 4x,
    hver holdt innenfor FIT_RANGE fra gruppens faktor. fit: per retning True (tilpasses per rute),
    et tall (fast faktor for hele gruppen) eller False (gruppens faktor)."""
    core = drawing[..., 3] >= CORE
    if not core.any() or not (original[..., 3] > 0).any():
        return scale, scale
    ys, xs = np.nonzero(core)
    oy, ox = np.nonzero(original[..., 3] > 0)
    dw, dh = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
    ow, oh = (ox.max() - ox.min() + 1) * SCALE, (oy.max() - oy.min() + 1) * SCALE
    lo, hi = scale * (1 - FIT_RANGE), scale * (1 + FIT_RANGE)
    def one(f, ratio):
        if f is True:
            return float(min(hi, max(lo, ratio)))
        return float(f) if f else scale
    return one(fit[0], ow / dw), one(fit[1], oh / dh)


def place_fitted(drawing: np.ndarray, original: np.ndarray, scale: float,
                 fit: tuple = (True, True)) -> dict:
    """Som place(), men med originalens mål (fit_scales) når det ikke dekker originalen tydelig dårligere
    enn gruppens faktor. Rapporten sier hvilken som ble brukt (tilpasset). Er begge retningene faste
    for gruppen (tall i fit), brukes de alltid, så alle rutene i gruppen får samme faktorer."""
    if all(f is not True for f in fit):
        sx, sy = fit_scales(drawing, original, scale, fit)
        r = place(drawing, original, sx, sy)
        r["tilpasset"] = bool(abs(sx - scale) >= 1e-3 or abs(sy - scale) >= 1e-3)
        r["skala_xy"] = [round(sx, 4), round(sy, 4)] if r["tilpasset"] else None
        return r
    plain = place(drawing, original, scale)
    sx, sy = fit_scales(drawing, original, scale, fit)
    if abs(sx - scale) < 1e-3 and abs(sy - scale) < 1e-3:
        plain["tilpasset"] = False
        return plain
    fitted = place(drawing, original, sx, sy)
    if fitted["snitt_union"] >= plain["snitt_union"] - FIT_SLACK and not (fitted["kuttet"] and not plain["kuttet"]):
        fitted["tilpasset"] = True
        fitted["skala_xy"] = [round(sx, 4), round(sy, 4)]
        return fitted
    plain["tilpasset"] = False
    return plain


def place(drawing: np.ndarray, original: np.ndarray, scale: float, scale_y: float | None = None) -> dict:
    """Skalerer tegningen (RGBA, bare denne rutens deler) og legger den over originalruten (RGBA i 1x).
    scale_y: egen faktor i høyden (ellers samme som scale).
    Gir bildet med marg (RGBA, (w + 2 * margx) * 4 x (h + 2 * margy) * 4), margene og målene."""
    h, w = original.shape[:2]
    o4 = np.repeat(np.repeat(original[..., 3] > 0, SCALE, axis=0), SCALE, axis=1)
    nh = max(1, round(drawing.shape[0] * (scale if scale_y is None else scale_y)))
    nw = max(1, round(drawing.shape[1] * scale))
    scaled = _premul_resize(drawing, (nw, nh))
    a = scaled[..., 3] >= CORE
    # Start: samme fotlinje og samme midtpunkt
    start = (round(_centre_x(o4) - _centre_x(a)), _bottom(o4) - _bottom(a))
    ox, oy, iou, cover = best_offset(a, o4, start)
    # Margen: det tegningen stikker utenfor ruten, rundet opp til hele originalpiksler, likt på begge
    # sider (motoren speilvender bildet rundt ruten)
    vis = scaled[..., 3] > 0
    ys, xs = np.nonzero(vis)
    if len(xs):
        left, right = -(ox + xs.min()), ox + xs.max() + 1 - w * SCALE
        top, bottom = -(oy + ys.min()), oy + ys.max() + 1 - h * SCALE
    else:
        left = right = top = bottom = 0
    padx = min(MAX_PAD, max(MIN_PAD, math.ceil(max(left, right, 0) / SCALE) + 1))
    pady = min(MAX_PAD, max(MIN_PAD, math.ceil(max(top, bottom, 0) / SCALE) + 1))
    W, H = (w + 2 * padx) * SCALE, (h + 2 * pady) * SCALE
    canvas = np.zeros((H, W, 4), np.uint8)
    px, py = padx * SCALE + ox, pady * SCALE + oy
    x0, y0 = max(px, 0), max(py, 0)
    x1, y1 = min(px + nw, W), min(py + nh, H)
    if x1 > x0 and y1 > y0:
        canvas[y0:y1, x0:x1] = scaled[y0 - py:y1 - py, x0 - px:x1 - px]
    return {"bilde": canvas, "margx": padx, "margy": pady, "flytt": [ox, oy], "snitt_union": round(iou, 3),
            "dekning": round(cover, 3), "kuttet": bool(max(left, right, top, bottom) > MAX_PAD * SCALE)}


def from_original(original: np.ndarray) -> dict:
    """Et fragment uten egen del på arket: originalruten skalert mykt opp (forhåndsmultiplisert Lanczos),
    med minste marg."""
    h, w = original.shape[:2]
    pad = MIN_PAD
    padded = np.zeros((h + 2 * pad, w + 2 * pad, 4), np.uint8)
    padded[pad:pad + h, pad:pad + w] = _masked(original, ~technical(original))
    big = _premul_resize(padded, ((w + 2 * pad) * SCALE, (h + 2 * pad) * SCALE))
    return {"bilde": big, "margx": pad, "margy": pad, "flytt": [0, 0], "snitt_union": None, "dekning": None,
            "kuttet": False}


def add_outliers(r: dict, original: np.ndarray, outlier: np.ndarray) -> int:
    """Legger utliggerne fra originalen (mykt skalert, på originalens plass) inn i bildet der tegningen
    ikke har noe. Gir antall originalpiksler som ble lagt inn."""
    if not outlier.any():
        return 0
    frag = from_original(_masked(original, outlier))["bilde"]  # marg MIN_PAD
    canvas = r["bilde"]
    dx, dy = (r["margx"] - MIN_PAD) * SCALE, (r["margy"] - MIN_PAD) * SCALE
    H, W = canvas.shape[:2]
    fh, fw = frag.shape[:2]
    x0, y0 = max(dx, 0), max(dy, 0)
    x1, y1 = min(dx + fw, W), min(dy + fh, H)
    if x1 <= x0 or y1 <= y0:
        return 0
    under = frag[y0 - dy:y1 - dy, x0 - dx:x1 - dx].astype(np.float32) / 255
    over = canvas[y0:y1, x0:x1].astype(np.float32) / 255
    a_o, a_u = over[..., 3:], under[..., 3:]
    a = a_o + a_u * (1 - a_o)
    rgb = np.where(a > 0, (over[..., :3] * a_o + under[..., :3] * a_u * (1 - a_o)) / np.maximum(a, 1e-6), 0)
    canvas[y0:y1, x0:x1] = np.clip(np.concatenate([rgb, a], axis=2) * 255 + 0.5, 0, 255).astype(np.uint8)
    return int(outlier.sum())


def _spread(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    mid = float(np.median(values)) or 1.0
    return (max(values) - min(values)) / mid


def sheet_scale(pairs: list[tuple[int, int]]) -> float | None:
    """Én skala for arket: veid median av originalhøyde i 4x delt på tegnet høyde, over rutene som
    er minst 12 originalpiksler høye (ellers alle). pairs: (originalhøyde, tegnet høyde)."""
    use = [(o, n) for o, n in pairs if o >= 12 and n > 0] or [(o, n) for o, n in pairs if n > 0]
    if not use:
        return None
    ratios = sorted((o * SCALE / n, o) for o, n in use)
    total, acc = sum(w for _, w in ratios), 0.0
    for r, w in ratios:
        acc += w
        if acc * 2 >= total:
            return r
    return ratios[-1][0]


# ------------------------------------------------------------------ et ark

def _override_part(img: np.ndarray, box: list[int]) -> np.ndarray | None:
    """Delen av et rettingsark som hører til én rute: delene (kjerner med myke kanter) som for det
    meste ligger i boksen. Gir RGBA beskåret til delene, eller None."""
    owner, core_lab, found = parts(img[..., 3])
    nrs = [p["nr"] for p in found if _overlap(p["boks"], core_lab, p["nr"], box) * 2 >= p["areal"]]
    if not nrs:
        return None
    own = np.isin(owner, nrs)
    ys, xs = np.nonzero(own)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    part = img[y0:y1, x0:x1].copy()
    part[~own[y0:y1, x0:x1]] = 0
    return part


def import_sheet(sheet: np.ndarray, cels: list[dict], boxes: dict[str, list[int]] | None, extract: Path,
                 out: Path, overrides: dict[str, tuple[np.ndarray, list[int]]] | None = None) -> dict:
    """Tar inn ett ark (RGBA) med rutene fra jobb.json. Skriver costumes/<rute>_hd.png i out og gir en
    rapport per rute og for arket. overrides: rute -> (rettingsark RGBA, boks); de rutene tas fra
    rettingsarket i stedet for arket, med egen skala som gir originalens høyde."""
    overrides = overrides or {}
    owner, core_lab, found = parts(sheet[..., 3])
    originals: dict[str, np.ndarray] = {}
    for c in cels:
        p = extract / "costumes" / f"{c['bilde']}.png"
        if p.exists():
            with Image.open(p) as im:
                originals[c["bilde"]] = np.asarray(im.convert("RGBA"))
    masks = {b: measure_mask(o) for b, o in originals.items()}
    visible = {b: int(masks[b][0].sum() + masks[b][1].sum()) for b in originals}
    fit_orig = {b: _masked(o, masks[b][0]) for b, o in originals.items()}

    how = "rutekart"
    taken = assign_by_map(cels, found, core_lab, boxes) if boxes else None
    if taken is None or not any(taken.values()):
        sizes = sorted(visible.values())
        small = SMALL if any(v >= SMALL for v in sizes) else 1
        big_cels = [c for c in cels if visible.get(c["bilde"], 0) >= small]
        areas = sorted((p["areal"] for p in found), reverse=True)
        # De store delene: like mange som de store rutene
        min_area = areas[len(big_cels) - 1] if 0 < len(big_cels) <= len(areas) else 1
        taken = assign_by_rows(big_cels, found, min_area)
        how = "rader"
        if taken is None:
            return {"metode": "ingen", "feil": "fant ikke samme rader og antall deler som rutene; trenger rutekart",
                    "ruter": {}}
        for c in cels:
            taken.setdefault(c["bilde"], [])

    # Skalaen: grafikeren tegner hodene større enn kroppene i forhold til originalen, og radene på
    # arket litt ulikt. Rutene deles derfor i grupper (samme animasjon og lag, samme rad på arket),
    # og hver gruppe får én skala som gir originalens høyde. Innen gruppen pulserer ikke figuren.
    info: dict[str, dict] = {}
    for c in cels:
        b = c["bilde"]
        nrs = taken.get(b) or []
        if b in overrides or not nrs or b not in originals or not masks[b][0].any():
            continue
        m = masks[b][0]
        rows = np.nonzero(m.any(axis=1))[0]
        cols = np.nonzero(m.any(axis=0))[0]
        mask = np.isin(core_lab, nrs)
        ys, xs = np.nonzero(mask)
        info[b] = {"oh": int(rows[-1] - rows[0] + 1), "ow": int(cols[-1] - cols[0] + 1),
                   "nh": int(ys.max() - ys.min() + 1), "nw": int(xs.max() - xs.min() + 1),
                   "x": float(xs.mean()), "y": float((ys.min() + ys.max()) / 2)}
    names = list(info)
    sheet_rows = _rows([(info[b]["x"], info[b]["y"], info[b]["nh"]) for b in names])
    row_of = {names[i]: r for r, members in enumerate(sheet_rows) for i in members}
    by_name = {c["bilde"]: c for c in cels}
    groups: dict[tuple, list[str]] = {}
    for b in names:
        c = by_name[b]
        groups.setdefault((c.get("animasjon"), c.get("lag"), row_of[b]), []).append(b)
    overall = sheet_scale([(info[b]["oh"], info[b]["nh"]) for b in names])
    if overall is None:
        if not overrides:
            return {"metode": how, "feil": "ingen ruter med deler på arket", "ruter": {}}
        overall = 1.0  # bare ruter fra rettingsark, de har egen skala
    scale_of: dict[str, float] = {}
    fit_of: dict[str, tuple[bool, bool]] = {}
    pending_fit: dict[tuple, tuple] = {}
    for key, members in groups.items():
        # Tilpasning per rute i en retning bare når tegningene sprer mer enn originalene der. Ellers er
        # forskjellen originalens egen (en åpen munn er én piksel lengre), og hele gruppen får én fast
        # faktor i den retningen (medianen), så hodet ikke strekkes ulikt mellom munnstillingene.
        pending_fit[key] = (
            _spread([info[b]["nw"] for b in members]) > _spread([info[b]["ow"] for b in members]) + FIT_SPREAD,
            _spread([info[b]["nh"] for b in members]) > _spread([info[b]["oh"] for b in members]) + FIT_SPREAD)
        if max(info[b]["oh"] for b in members) >= 8:
            g = sheet_scale([(info[b]["oh"], info[b]["nh"]) for b in members])
        else:
            # Bare små ruter: skalaen til rutene i samme lag på arket
            same = [b for b in names if by_name[b].get("lag") == key[1] and info[b]["oh"] >= 8]
            g = sheet_scale([(info[b]["oh"], info[b]["nh"]) for b in same]) if same else None
        for b in members:
            scale_of[b] = g or overall
        g = g or overall
        lo, hi = g * (1 - FIT_RANGE), g * (1 + FIT_RANGE)
        fx, fy = pending_fit[key]
        gx = float(min(hi, max(lo, np.median([info[b]["ow"] * SCALE / info[b]["nw"] for b in members]))))
        gy = float(min(hi, max(lo, np.median([info[b]["oh"] * SCALE / info[b]["nh"] for b in members]))))
        for b in members:
            fit_of[b] = (True if fx else gx, True if fy else gy)

    (out / "costumes").mkdir(parents=True, exist_ok=True)
    report: dict[str, dict] = {}
    for c in cels:
        b = c["bilde"]
        o = originals.get(b)
        dest = out / "costumes" / f"{b}_hd.png"
        if o is None or not (o[..., 3] > 0).any():
            report[b] = {"status": "tom", "grunn": "originalruten har ingen synlige piksler"}
            continue
        if not visible.get(b):
            # Bare tekniske piksler (skyggemerker): ingen HD, motoren viser originalen
            dest.unlink(missing_ok=True)
            report[b] = {"status": "teknisk", "grunn": "bare tekniske magentapiksler (skyggemerker)"}
            continue
        nrs = taken.get(b) or []
        part = None
        own_scale = None
        if b in overrides:
            img, box = overrides[b]
            part = _override_part(img, box)
            if part is not None and masks[b][0].any():
                rows = np.nonzero(masks[b][0].any(axis=1))[0]
                ys = np.nonzero((part[..., 3] >= CORE).any(axis=1))[0]
                if len(ys):
                    own_scale = (rows[-1] - rows[0] + 1) * SCALE / (ys[-1] - ys[0] + 1)
        elif nrs:
            own = np.isin(owner, nrs)
            ys, xs = np.nonzero(own)
            y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
            part = sheet[y0:y1, x0:x1].copy()
            part[~own[y0:y1, x0:x1]] = 0
        if part is not None and masks[b][0].any():
            scale = own_scale or scale_of.get(b, overall)
            r = place_fitted(part, fit_orig[b], scale, (False, False) if b in overrides else fit_of.get(b, (True, True)))
            added = add_outliers(r, o, masks[b][1])
            ok = r["snitt_union"] >= GOOD_IOU and r["dekning"] >= GOOD_COVER and not r["kuttet"]
            status = "ok" if ok else "sjekk"
            kilde = "rettingsark" if b in overrides else "arket"
            if added:
                kilde += f" og {added} utliggerpiksler fra originalen"
            scale_of[b] = scale
        elif visible[b] < SMALL:
            r = from_original(o)
            status, kilde = "ok", "originalen (fragment)"
        else:
            report[b] = {"status": "mangler", "grunn": "ingen del på arket for ruten"}
            continue
        Image.fromarray(r["bilde"], "RGBA").save(dest, optimize=True)
        report[b] = {"status": status, "kilde": kilde, "fil": f"costumes/{b}_hd.png", "sha256": _sha(dest),
                     "storrelse": [r["bilde"].shape[1], r["bilde"].shape[0]], "marg": [r["margx"], r["margy"]],
                     "flytt_hd": r["flytt"], "snitt_union": r["snitt_union"], "dekning": r["dekning"],
                     "deler": len(nrs), "skala": round(scale_of.get(b, overall), 4), "tilpasset": r.get("tilpasset", False),
                     "skala_xy": r.get("skala_xy"), "kostyme": c.get("kostyme"), "rute": c.get("rute"),
                     "animasjon": c.get("animasjon"), "retning": c.get("retning"), "lag": c.get("lag")}
    return {"metode": how, "skala": round(overall, 4), "grupper": len(groups), "deler_paa_arket": len(found),
            "ruter": report}


def preview(sheet_report: dict, extract: Path, out_dir: Path, name: str, columns: int = 8) -> Path | None:
    """Kontaktark: for hver rute originalen i 4x og den nye ruten over den på grått, med originalens
    omriss i rødt. Lagres som out_dir/myk_<navn>.png."""
    tiles = []
    for b, r in sheet_report.get("ruter", {}).items():
        if not r.get("fil"):
            continue
        with Image.open(extract / "costumes" / f"{b}.png") as im:
            o = im.convert("RGBA")
        with Image.open(r["_sti"]) as im:
            n = im.convert("RGBA")
        mx, my = r["marg"]
        bg = Image.new("RGBA", n.size, (128, 128, 128, 255))
        o4 = o.resize((o.width * SCALE, o.height * SCALE), Image.NEAREST)
        left = bg.copy()
        left.alpha_composite(o4, (mx * SCALE, my * SCALE))
        right = bg.copy()
        right.alpha_composite(n)
        edge = np.asarray(o4)[..., 3] > 0
        ring = edge & ~(np.roll(edge, 1, 0) & np.roll(edge, -1, 0) & np.roll(edge, 1, 1) & np.roll(edge, -1, 1))
        ra = np.asarray(right).copy()
        ys, xs = np.nonzero(ring)
        ra[ys + my * SCALE, xs + mx * SCALE] = (255, 40, 40, 255)
        tile = Image.new("RGBA", (n.width * 2 + 4, n.height), (60, 60, 60, 255))
        tile.paste(left, (0, 0))
        tile.paste(Image.fromarray(ra), (n.width + 4, 0))
        tiles.append(tile)
    if not tiles:
        return None
    tw = max(t.width for t in tiles) + 8
    th = max(t.height for t in tiles) + 8
    rows = math.ceil(len(tiles) / columns)
    sheet = Image.new("RGB", (tw * min(columns, len(tiles)), th * rows), (30, 30, 30))
    for i, t in enumerate(tiles):
        sheet.paste(t.convert("RGB"), ((i % columns) * tw, (i // columns) * th))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / f"myk_{name}.png"
    sheet.save(dest)
    return dest


# ------------------------------------------------------------------ alle leverte ark

def rejected_sheet(rejections: dict[str, dict] | None, job: str, sha: str) -> dict | None:
    """Avvisningen for arket (docs/gpt-avvisninger.csv, status avvist) når den gjelder denne leveransen
    (samme sha256 eller "*"), ellers None."""
    r = (rejections or {}).get(job)
    if not r or (r.get("status") or "avvist").strip() != "avvist":
        return None
    want = (r.get("sha256_resultat") or "").strip()
    return r if want in ("*", sha) else None


def import_all(gren: Path, extract: Path, out: Path, only: set[str] | None = None,
               previews: Path | None = None, rejections: dict[str, dict] | None = None) -> dict:
    """Tar inn alle leverte ark i glatt stil fra arbeidsgrenen (gren: work/.gpt-gren). Skriver de myke
    rutene til out/costumes og rapporten til out/myke.json. Gir rapporten.
    rejections: avvisningene (gpt.read_rejections). Et avvist ark tas ikke inn, og rutene det ga før,
    slettes, så motoren viser originalen til et nytt ark er godkjent."""
    maps = route_maps(gren)
    accepted = accepted_sources(gren)
    result: dict = {"versjon": VERSION, "ark": {}, "ruter_ok": 0, "ruter_sjekk": 0, "ruter_mangler": 0,
                    "ruter_teknisk": 0}
    # Ark som er tatt inn før med samme bilde, jobb, rutekart og versjon, tas ikke inn på nytt
    try:
        before = json.loads((out / "myke.json").read_text()).get("ark", {})
    except (OSError, json.JSONDecodeError):
        before = {}
    todo = {d["jobb"]: d for d in deliveries(gren)}
    for job, a in accepted.items():
        todo[job] = {"jobb": job, "resultat": a["base_native"], "sha256": a.get("base_sha256")}
    for d in sorted(todo.values(), key=lambda d: d["jobb"]):
        job = d["jobb"]
        if only and job not in only:
            continue
        src = gren / d["resultat"]
        meta_path = gren / "jobber" / job / "jobb.json"
        acc = accepted.get(job)
        overrides: dict[str, tuple[np.ndarray, list[int]]] = {}
        extra: list = []
        if acc:
            if acc.get("base_map"):
                maps[job] = load_map(gren / acc["base_map"], job)
            for ov in acc.get("overrides", []):
                p = gren / ov["native_png"]
                if p.exists():
                    with Image.open(p) as im:
                        overrides[ov["bilde"]] = (np.asarray(im.convert("RGBA")), [int(v) for v in ov["native_analyseboks_alfa128"]])
                    extra.append([ov["bilde"], _sha(p), ov["native_analyseboks_alfa128"]])
        if not src.exists() or not meta_path.exists():
            result["ark"][job] = {"feil": f"mangler {src.name if not src.exists() else 'jobb.json'}"}
            continue
        sha = _sha(src)
        if d.get("sha256") and d["sha256"] != sha:
            result["ark"][job] = {"feil": "sha256 stemmer ikke med leveransen", "resultat": d["resultat"]}
            continue
        why = rejected_sheet(rejections, job, sha)
        if why:
            for r in (before.get(job) or {}).get("ruter", {}).values():
                if r.get("fil"):
                    (out / r["fil"]).unlink(missing_ok=True)
            result["ark"][job] = {"avvist": (why.get("grunn") or "").strip(), "resultat": d["resultat"], "sha256": sha}
            continue
        meta = json.loads(meta_path.read_text())
        if meta.get("type") != "figur":
            continue
        key = hashlib.sha256(json.dumps([VERSION, sha, meta.get("ruter"), maps.get(job), extra], sort_keys=True)
                             .encode()).hexdigest()
        old = before.get(job)
        if old and old.get("nokkel") == key and all((out / r["fil"]).exists()
                                                     for r in old.get("ruter", {}).values() if r.get("fil")):
            rep = old
        else:
            with Image.open(src) as im:
                sheet = np.asarray(im.convert("RGBA"))
            rep = import_sheet(sheet, meta.get("ruter") or [], maps.get(job), extract, out, overrides)
            rep.update({"resultat": d["resultat"], "sha256": sha, "nokkel": key})
            if extra:
                rep["rettinger"] = extra
        fresh = rep is not old
        if previews is not None and rep.get("ruter") and (fresh or not (previews / f"myk_{job}.png").exists()):
            for b, r in rep["ruter"].items():
                if r.get("fil"):
                    r["_sti"] = str(out / r["fil"])
            p = preview(rep, extract, previews, job)
            for r in rep["ruter"].values():
                r.pop("_sti", None)
            if p:
                rep["forhandsvisning"] = p.name
        result["ark"][job] = rep
        for r in rep.get("ruter", {}).values():
            field = {"ok": "ruter_ok", "sjekk": "ruter_sjekk", "mangler": "ruter_mangler",
                     "teknisk": "ruter_teknisk"}.get(r["status"])
            if field:
                result[field] += 1
    out.mkdir(parents=True, exist_ok=True)
    (out / "myke.json").write_text(json.dumps(result, ensure_ascii=False, indent=1))
    return result
