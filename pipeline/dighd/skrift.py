"""HD-skrift for teksten i spillet.

Motoren tegner bokstavene med en ekte skrift i stedet for å skalere de små
pikselbokstavene. Hver bokstav fylles inn i boksen til originalbokstaven, så
plassering, størrelse og linjebrudd blir som i originalen. Kanten eller skyggen
lager motoren selv ut fra originalen.

Modden får:
  fonts/map.txt            "<spillskrift> <mappe>" per linje. Spillskriftene er
                           tegnsettnumrene (CHAR-ressursene) og 100 + n for FONTn.NUT.
  fonts/<mappe>/NNN.png    hvit RGBA med dekning i alfa, beskåret til blekket,
                           ett bilde per tegnkode 33..126.

Skriften er Exo 2 (SIL Open Font License 1.1, se skrifter/exo2/OFL.txt).
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SKRIFTER = Path(__file__).parent / "skrifter"

# Mappe i modden -> skriftfil. Tykkelsen er i forhold til bokstavhøyden,
# for motoren strekker bokstaven til originalboksen.
VARIANTER = {
    "exo2": "exo2/exo-2-latin-700-normal.woff",
    "exo2-600": "exo2/exo-2-latin-600-normal.woff",
}

# Spillskrift -> mappe. Spillskrifter som ikke står her tegnes som før (xBR).
KART = {
    0: "exo2", 1: "exo2", 2: "exo2", 3: "exo2", 4: "exo2", 5: "exo2",
    100: "exo2", 101: "exo2", 102: "exo2", 103: "exo2",
}

STR = 96          # punktstørrelse når bokstavene tegnes
TEGN = range(33, 127)


def tegn_bokstav(font: ImageFont.FreeTypeFont, ch: str) -> Image.Image | None:
    pad = STR // 2
    img = Image.new("L", (STR * 2 + pad * 2, STR * 2 + pad * 2), 0)
    ImageDraw.Draw(img).text((pad, pad), ch, font=font, fill=255)
    box = img.getbbox()
    if not box:
        return None
    alfa = img.crop(box)
    hvit = Image.new("L", alfa.size, 255)
    return Image.merge("RGBA", (hvit, hvit, hvit, alfa))


def lag_skrift(out: Path, kart: dict[int, str] | None = None) -> dict:
    """Skriv fonts/ i modden `out`. Returnerer antall bokstaver per mappe."""
    kart = KART if kart is None else kart
    fonts = out / "fonts"
    fonts.mkdir(parents=True, exist_ok=True)
    antall = {}
    for mappe in sorted(set(kart.values())):
        font = ImageFont.truetype(str(SKRIFTER / VARIANTER[mappe]), STR)
        d = fonts / mappe
        d.mkdir(exist_ok=True)
        n = 0
        for c in TEGN:
            g = tegn_bokstav(font, chr(c))
            if g is not None:
                g.save(d / f"{c:03d}.png", optimize=True)
                n += 1
        antall[mappe] = n
    linjer = ["# HD-skrift: <spillskrift> <mappe>. 0-9 er tegnsettene, 100 + n er FONTn.NUT.",
              "# Skriften er Exo 2, SIL Open Font License 1.1."]
    linjer += [f"{k} {v}" for k, v in sorted(kart.items())]
    (fonts / "map.txt").write_text("\n".join(linjer) + "\n")
    (fonts / "OFL.txt").write_bytes((SKRIFTER / "exo2" / "OFL.txt").read_bytes())
    return antall
