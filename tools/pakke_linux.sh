#!/usr/bin/env bash
# Lager den komplette Linux-pakken: én AppImage med ScummVM med HD-patchen, spillfilene,
# musikk og tale, og HD-modden. Pakken starter rett i spillet.
#
#   tools/pakke_linux.sh [utmappe]          standard out/linux
#
# Krever:
#   engine/scummvm/scummvm (eller SCUMMVM_SRC)   bygget med engine/build.sh
#   game/ med DIG.LA0, DIG.LA1, VIDEO/, DIGMUSIC.BUN, DIGVOICE.BUN   (tools/hent_spilldata.sh)
#   mods/gpt                                  (tools/mod_gren.sh hent)
#   LINUXDEPLOY og APPIMAGETOOL: stier til linuxdeploy og appimagetool. Uten dem lages bare
#   AppDir-mappen (den kan startes med AppDir/AppRun).
#
# Pakken inneholder spillet og skal bare ligge privat (release i dette repoet), aldri åpent.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="${SCUMMVM_SRC:-$ROOT/engine/scummvm}"
OUT="${1:-$ROOT/out/linux}"
APPDIR="$OUT/AppDir"
NAVN="TheDigHD-x86_64.AppImage"

[ -x "$SRC/scummvm" ] || { echo "Fant ikke $SRC/scummvm. Kjør engine/build.sh først."; exit 1; }
for f in DIG.LA0 DIG.LA1 DIGMUSIC.BUN DIGVOICE.BUN VIDEO/SQ1.SAN; do
	[ -f "$ROOT/game/$f" ] || { echo "Fant ikke game/$f. Kjør tools/hent_spilldata.sh først."; exit 1; }
done
[ -f "$ROOT/mods/gpt/mod.json" ] || { echo "Fant ikke mods/gpt. Kjør tools/mod_gren.sh hent først."; exit 1; }

echo "Sjekker spillfilene ..."
(cd "$ROOT/game" && sha256sum --quiet -c SHA256SUMS && sha256sum --quiet -c SHA256SUMS.lyd)
[ -f "$ROOT/mods/gpt/SHA256SUMS" ] && (cd "$ROOT/mods/gpt" && sha256sum --quiet -c SHA256SUMS)

rm -rf "$APPDIR"
DATA="$APPDIR/usr/share/the-dig-hd"
mkdir -p "$APPDIR/usr/bin" "$DATA/game" "$DATA/mods"

echo "Kopierer motoren, spillet, musikken, talen og HD-modden ..."
install -m 755 "$SRC/scummvm" "$APPDIR/usr/bin/scummvm"
strip "$APPDIR/usr/bin/scummvm" 2>/dev/null || true
cp -r "$ROOT/game/DIG.LA0" "$ROOT/game/DIG.LA1" "$ROOT/game/DIGMUSIC.BUN" "$ROOT/game/DIGVOICE.BUN" "$ROOT/game/VIDEO" "$DATA/game/"
cp -r "$ROOT/mods/gpt" "$DATA/mods/gpt"
rm -f "$DATA/mods/gpt/README.md"
# ScummVM sine temaer og hjelpefiler (menyene i ScummVM selv), samme liste som engine/build-pages.py
for name in achievements.dat classicmacfonts.dat encoding.dat gui-icons.dat helpdialog.zip macgui.dat \
	residualvm.zip scummclassic.zip scummmodern.zip scummremastered.zip shaders.dat translations.dat; do
	for dir in gui/themes dists/engine-data dists; do
		[ -f "$SRC/$dir/$name" ] && { cp "$SRC/$dir/$name" "$DATA/"; break; }
	done
done
cp "$SRC/COPYING" "$DATA/COPYING-ScummVM.txt"
cp "$SRC/COPYRIGHT" "$DATA/COPYRIGHT-ScummVM.txt"

# Hva pakken er bygget av
{
	echo "The Dig HD for Linux"
	echo "Bygget: $(date -u '+%Y-%m-%d %H:%M UTC')"
	echo "ScummVM: $(cat "$ROOT/engine/SCUMMVM_COMMIT") med engine/patches/"
	echo "Dig-HD-Remake: $(git -C "$ROOT" rev-parse --short HEAD 2>/dev/null || echo ukjent)"
	echo "HD-mod laget: $(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("created", "ukjent"))' "$ROOT/mods/gpt/mod.json")"
} > "$DATA/BYGG.txt"

# Oppstarten: rett i spillet, med innstillinger og lagrede spill i hjemmemappen
cat > "$OUT/AppRun" <<'EOF'
#!/bin/sh
# The Dig HD: starter spillet rett, med HD-grafikk, musikk og tale.
# Innstillinger: ~/.config/the-dig-hd/scummvm.ini. Lagrede spill: ~/.local/share/the-dig-hd/saves.
# F5 i spillet: menyen, der HD Graphics velger HD eller originalgrafikk.
HERE="$(dirname "$(readlink -f "$0")")"
DATA="$HERE/usr/share/the-dig-hd"
CONF="${XDG_CONFIG_HOME:-$HOME/.config}/the-dig-hd"
SAVES="${XDG_DATA_HOME:-$HOME/.local/share}/the-dig-hd/saves"
mkdir -p "$CONF" "$SAVES"
if [ ! -f "$CONF/scummvm.ini" ]; then
	cat > "$CONF/scummvm.ini" <<INI
[scummvm]
fullscreen=true
aspect_ratio=true
subtitles=true
gui_return_to_launcher_at_exit=false
confirm_exit=false

[dig]
description=The Dig HD
engineid=scumm
gameid=dig
subtitles=true
INI
fi
export DIGHD_MOD="${DIGHD_MOD:-$DATA/mods/gpt}"
export LD_LIBRARY_PATH="$HERE/usr/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
exec "$HERE/usr/bin/scummvm" --config="$CONF/scummvm.ini" --path="$DATA/game" --savepath="$SAVES" \
	--themepath="$DATA" --extrapath="$DATA" "$@" dig
EOF
chmod 755 "$OUT/AppRun"

cat > "$OUT/the-dig-hd.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=The Dig HD
Comment=The Dig med HD-grafikk, musikk og tale
Exec=the-dig-hd
Icon=the-dig-hd
Categories=Game;AdventureGame;
Terminal=false
EOF
cp "$SRC/icons/scummvm.svg" "$OUT/the-dig-hd.svg"

if [ -z "${LINUXDEPLOY:-}" ] || [ -z "${APPIMAGETOOL:-}" ]; then
	cp "$OUT/AppRun" "$OUT/the-dig-hd.desktop" "$OUT/the-dig-hd.svg" "$APPDIR/"
	echo "Ferdig: $APPDIR (uten LINUXDEPLOY og APPIMAGETOOL blir det ingen AppImage). Start med $APPDIR/AppRun"
	exit 0
fi

echo "Tar med bibliotekene motoren trenger (linuxdeploy) ..."
"$LINUXDEPLOY" --appdir "$APPDIR" --executable "$APPDIR/usr/bin/scummvm" \
	--desktop-file "$OUT/the-dig-hd.desktop" --icon-file "$OUT/the-dig-hd.svg" \
	--custom-apprun "$OUT/AppRun" > "$OUT/linuxdeploy.log" 2>&1 \
	|| { tail -20 "$OUT/linuxdeploy.log"; exit 1; }
cmp -s "$OUT/AppRun" "$APPDIR/AppRun" || { echo "AppRun i AppDir er ikke vår"; exit 1; }

echo "Lager AppImage ..."
rm -f "$OUT/$NAVN"
ARCH=x86_64 "$APPIMAGETOOL" --no-appstream "$APPDIR" "$OUT/$NAVN" > "$OUT/appimagetool.log" 2>&1 \
	|| { tail -20 "$OUT/appimagetool.log"; exit 1; }
(cd "$OUT" && sha256sum "$NAVN" > "$NAVN.sha256")
echo "Ferdig: $OUT/$NAVN ($(du -h "$OUT/$NAVN" | cut -f1))"
