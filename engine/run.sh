#!/usr/bin/env bash
# Starter The Dig med en HD-mod.
#
# Bruk:  engine/run.sh [modnavn] [flere ScummVM-valg]
#        engine/run.sh hd
#        engine/run.sh test-lanczos --fullscreen
#
# Modmappen er mods/<modnavn>. Spillfilene ligger i game/ (tools/hent_spilldata.sh).
# Musikk og tale: legg DIGMUSIC.BUN og DIGVOICE.BUN fra Drive i game/.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
SRC="${SCUMMVM_SRC:-$HERE/scummvm}"
MOD="${1:-hd}"
shift || true

[ -x "$SRC/scummvm" ] || { echo "Fant ikke $SRC/scummvm. Kjør engine/build.sh først."; exit 1; }
[ -f "$ROOT/game/DIG.LA1" ] || { echo "Fant ikke spillfilene. Kjør tools/hent_spilldata.sh først."; exit 1; }
[ -d "$ROOT/mods/$MOD" ] || { echo "Fant ikke mods/$MOD. Lag den med: dighd build-mod --name $MOD"; exit 1; }
[ -f "$ROOT/game/DIGMUSIC.BUN" ] || echo "Merk: DIGMUSIC.BUN mangler i game/, spillet blir uten musikk."
[ -f "$ROOT/game/DIGVOICE.BUN" ] || echo "Merk: DIGVOICE.BUN mangler i game/, spillet blir uten tale."

export DIGHD_MOD="$ROOT/mods/$MOD"
exec "$SRC/scummvm" --path="$ROOT/game" --gfx-mode=opengl --aspect-ratio "$@" dig
