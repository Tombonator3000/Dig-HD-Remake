#!/usr/bin/env bash
# Starter The Dig med en HD-mod i nettleseren, bare på denne maskinen.
#
# Bruk:  engine/run-web.sh [modnavn] [--port N] [--rom N] [--klassisk] [--gult] [flere ScummVM-valg]
#        engine/run-web.sh gpt --rom 22
#
# Legger nettleserversjonen (engine/build-web.sh), spillfilene og modden i work/nettleser og
# starter en webserver som bare lytter på 127.0.0.1. Åpne adressen skriptet skriver ut.
#
# Spillet og HD-grafikken tilhører Disney/Lucasfilm. Mappen work/nettleser og adressen skal aldri
# legges ut på en åpen adresse: ingen GitHub Pages, ingen publisering, ingen opplasting.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
SRC="${SCUMMVM_WEB_SRC:-$HERE/scummvm-web}"
WEB="$ROOT/work/nettleser"

MOD=gpt
if [ $# -gt 0 ] && [ "${1#-}" = "$1" ]; then MOD="$1"; shift; fi
PORT=8000 ROM="" KLASSISK=0 GULT=0
ARGS=()
while [ $# -gt 0 ]; do
	case "$1" in
	--port) PORT="$2"; shift 2 ;;
	--rom) ROM="$2"; shift 2 ;;
	--klassisk) KLASSISK=1; shift ;;
	--gult) GULT=1; shift ;;
	*) ARGS+=("$1"); shift ;;
	esac
done

DIST="$SRC/build-emscripten"
[ -f "$DIST/scummvm.wasm" ] || { echo "Fant ikke $DIST/scummvm.wasm. Kjør engine/build-web.sh først."; exit 1; }
[ -f "$ROOT/game/DIG.LA1" ] || { echo "Fant ikke spillfilene. Kjør tools/hent_spilldata.sh først."; exit 1; }
[ -d "$ROOT/mods/$MOD" ] || { echo "Fant ikke mods/$MOD. Hent den med tools/mod_gren.sh hent."; exit 1; }
[ -f "$ROOT/game/DIGMUSIC.BUN" ] || echo "Merk: DIGMUSIC.BUN mangler i game/, spillet blir uten musikk."
[ -f "$ROOT/game/DIGVOICE.BUN" ] || echo "Merk: DIGVOICE.BUN mangler i game/, spillet blir uten tale."

# Nettleserversjonen leser alt under /data over HTTP, med en index.json i hver mappe
# (backends/fs/emscripten/http-fs.cpp i ScummVM). Spillfilene og modden legges inn som lenker,
# så ingenting kopieres og ingenting skrives i game/ eller mods/.
rm -rf "$WEB"
mkdir -p "$WEB"
cp -r "$DIST/." "$WEB/"
cp "$HERE/web/index.html" "$HERE/web/scummvm.ini" "$WEB/"
mkdir -p "$WEB/data/games" "$WEB/data/mods"
cp -rs "$(cd "$ROOT/game" && pwd -P)" "$WEB/data/games/dig"
cp -rs "$(cd "$ROOT/mods/$MOD" && pwd -P)" "$WEB/data/mods/$MOD"
python3 "$SRC/dists/emscripten/build-make_http_index.py" "$WEB/data"

# Adressen med valgene
QUERY="$(python3 - "$MOD" "$ROM" "$KLASSISK" "$GULT" "${ARGS[@]}" <<'EOF'
import sys
from urllib.parse import urlencode
mod, rom, klassisk, gult, *args = sys.argv[1:]
q = []
if mod != "gpt":
    q.append(("mod", mod))
if rom:
    q.append(("rom", rom))
if klassisk == "1":
    q.append(("klassisk", "1"))
if gult == "1":
    q.append(("gult", "1"))
if args:
    q.append(("args", " ".join(args)))
print("?" + urlencode(q) if q else "")
EOF
)"

echo
echo "Åpne denne adressen i nettleseren (Chrome, Edge eller Firefox):"
echo
echo "    http://localhost:$PORT/$QUERY"
echo
echo "Bare på denne maskinen. Ikke del adressen eller mappen work/nettleser."
[ -n "$ROM" ] && echo "Hopper til rom $ROM (filmene hoppes over)."
echo "Ctrl+H: HD eller klassisk. Ctrl+Shift+H: gult felt der HD mangler. F5: spillmenyen. F11: fullskjerm."
exec python3 "$HERE/web/server.py" --port "$PORT" "$WEB"
