#!/usr/bin/env bash
# Kjører spillet uten skjerm og sjekker at HD-grafikken havner på riktig sted.
#
# Lager en mod med "nearest" (hver piksel blir en blokk). Da skal HD-bildet være
# likt originalen skalert opp. Motoren sammenligner selv og skriver hvor mange
# piksler som avviker kraftig, og om skjermen er lik hele skjermen bygget på nytt.
# Fargesyklede områder og HD-tekst telles for seg (de er jevnet ut med vilje, se
# docs/HD-MOTOR.md).
# Bilder av skjermen lagres i work/test-dumps.
#
# Bruk: engine/test.sh [antall bilder, standard 3000]
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
SRC="${SCUMMVM_SRC:-$HERE/scummvm}"
FRAMES="${1:-3000}"
OUT="$ROOT/work/test-dumps"

[ -d "$ROOT/mods/test-nearest" ] || dighd build-mod --name test-nearest --method nearest --kostymer 1-20

rm -rf "$OUT"
mkdir -p "$OUT" "$ROOT/work/test-home"
export HOME="$ROOT/work/test-home" XDG_CONFIG_HOME="$ROOT/work/test-home/.config" XDG_DATA_HOME="$ROOT/work/test-home/.local/share"
export SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy
export DIGHD_MOD="$ROOT/mods/test-nearest" DIGHD_VERIFY=1 DIGHD_SKIP_VIDEO=1
export DIGHD_DUMP_DIR="$OUT" DIGHD_DUMP_EVERY=250 DIGHD_QUIT_AT="$FRAMES"

timeout 600 "$SRC/scummvm" --path="$ROOT/game" --debuglevel=1 dig > "$OUT/scummvm.log" 2>&1 || true
grep -E "DigHD: (verify|screen|room)" "$OUT/scummvm.log" || { echo "Ingen DigHD-linjer i loggen, se $OUT/scummvm.log"; exit 1; }
echo "Bilder: $OUT"
