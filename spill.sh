#!/usr/bin/env bash
# Spill The Dig med HD-grafikken rett fra repoet.
#
#   ./spill.sh                 henter det som mangler, oppdaterer HD-modden og motoren, starter spillet
#   ./spill.sh --rom 22        starter i rom 22 (for å se på et bestemt rom)
#   ./spill.sh --klassisk      starter med originalgrafikken (Ctrl+H bytter underveis)
#   ./spill.sh --gult          farger gult der HD mangler (Ctrl+Shift+H slår av og på)
#   ./spill.sh --auto          fyller rom og objekter uten ChatGPT-bilde med automatisk oppskalering
#   ./spill.sh --fort          ingen henting eller bygging, bare start
#   ./spill.sh --fullskjerm    fullskjerm
#   ./spill.sh --programvare   uten OpenGL (hvis spillet ikke starter og sier "Could not load any graphics mode")
#
# Valg som ikke står over, sendes videre til ScummVM.
# Tastene i spillet: Ctrl+H (HD eller klassisk), Ctrl+Shift+H (gult felt), F5 (meny), Alt+S (skjermbilde).
# Hva du bør se etter: docs/SPILLTEST.md.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

ROM="" KLASSISK=0 GULT=0 AUTO=0 FORT=0
EKSTRA=()
while [ $# -gt 0 ]; do
	case "$1" in
	--rom) ROM="$2"; shift 2 ;;
	--klassisk) KLASSISK=1; shift ;;
	--gult) GULT=1; shift ;;
	--auto) AUTO=1; shift ;;
	--fort) FORT=1; shift ;;
	--fullskjerm) EKSTRA+=(--fullscreen); shift ;;
	--programvare) EKSTRA+=(--gfx-mode=surfacesdl); shift ;;
	-h|--help) sed -n '2,17p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
	*) EKSTRA+=("$1"); shift ;;
	esac
done

mangler=()
for cmd in git make sha256sum tar; do command -v "$cmd" >/dev/null 2>&1 || mangler+=("$cmd"); done
command -v c++ >/dev/null 2>&1 || command -v g++ >/dev/null 2>&1 || mangler+=("g++")
command -v sdl2-config >/dev/null 2>&1 || mangler+=("SDL2 (libsdl2-dev)")
pkg-config --exists libpng 2>/dev/null || [ -f /usr/include/png.h ] || mangler+=("libpng (libpng-dev)")
if [ ${#mangler[@]} -gt 0 ]; then
	echo "Mangler: ${mangler[*]}"
	echo "Ubuntu/Debian: sudo apt install build-essential git pkg-config libsdl2-dev libpng-dev zlib1g-dev"
	echo "Fedora: sudo dnf install gcc-c++ make git pkgconf SDL2-devel libpng-devel zlib-devel"
	exit 1
fi

steg() { printf '\n== %s\n' "$*"; }

# 1. Spillfilene (første gang)
if [ ! -f game/DIG.LA1 ]; then
	steg "Henter spillfilene"
	tools/hent_spilldata.sh
fi

# 2. Siste HD-mod fra grenen hd-mod
if [ "$FORT" = 0 ] || [ ! -f mods/gpt/mod.json ]; then
	steg "Henter siste HD-mod"
	tools/mod_gren.sh hent
fi

# 3. Motoren: bygges første gang og når patchen eller ScummVM-versjonen er endret
STEMPEL="$(cat engine/SCUMMVM_COMMIT engine/patches/*.patch | sha256sum | cut -c1-16)"
BYGD="$(cat engine/scummvm/.dighd-stempel 2>/dev/null || true)"
if [ ! -x engine/scummvm/scummvm ] || { [ "$FORT" = 0 ] && [ "$STEMPEL" != "$BYGD" ]; }; then
	steg "Bygger motoren (første gang tar det noen minutter)"
	engine/build.sh
	echo "$STEMPEL" > engine/scummvm/.dighd-stempel
fi

# 4. Automatisk oppskalering der ChatGPT ikke har levert ennå (valgfritt)
MOD=gpt
if [ "$AUTO" = 1 ]; then
	MOD=auto
	GPT_STEMPEL="$(sha256sum mods/gpt/SHA256SUMS | cut -c1-16)"
	if [ ! -f mods/auto/mod.json ] || [ "$(cat mods/auto/.gpt-stempel 2>/dev/null || true)" != "$GPT_STEMPEL" ]; then
		steg "Lager automatisk oppskalering for resten (første gang tar det 5 til 10 minutter)"
		if [ ! -x .venv/bin/dighd ]; then
			python3 -c 'import sys; sys.exit(sys.version_info < (3, 12))' || { echo "--auto krever Python 3.12 eller nyere."; exit 1; }
			python3 -m venv .venv
			.venv/bin/pip install -q -e "pipeline"
		fi
		[ -f work/extract/rooms.json ] || .venv/bin/dighd extract --only la1
		rm -rf mods/auto
		.venv/bin/dighd build-mod --name auto --method lanczos-sharp --egne mods/gpt
		echo "$GPT_STEMPEL" > mods/auto/.gpt-stempel
	fi
fi

# 5. Start
steg "Starter The Dig (mod: $MOD)"
[ -n "$ROM" ] && export DIGHD_TEST_ROOM="$ROM" DIGHD_TEST_AT="${DIGHD_TEST_AT:-240}" DIGHD_SKIP_VIDEO=1 && echo "Hopper til rom $ROM (filmer hoppes over)."
[ "$KLASSISK" = 1 ] && export DIGHD_CLASSIC=1
[ "$GULT" = 1 ] && export DIGHD_SHOW_MISSING=1
echo "Ctrl+H: HD eller klassisk. Ctrl+Shift+H: gult felt der HD mangler. Alt+S: skjermbilde."
exec engine/run.sh "$MOD" --subtitles "${EKSTRA[@]}"
