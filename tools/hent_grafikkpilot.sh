#!/usr/bin/env bash
# Henter den private grafikkpiloten til work/ uten å skrive over lokale endringer.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
DEST="$ROOT/work/graphics-pilot-20261006"
ART_BRANCH="grafikkdata/pilot-20261006"
ART_COMMIT="cf8e6a9f6e30d662f7c73076ef1e1810851ceceb"

if [ -e "$DEST" ]; then
    [ -f "$DEST/SHA256SUMS" ] || { echo "Målmappen finnes allerede uten manifest. Bevar den og velg en annen arbeidsmappe."; exit 1; }
    (cd "$DEST" && sha256sum --quiet -c SHA256SUMS)
    echo "Grafikkpiloten finnes allerede og sjekksummene stemmer: $DEST"
    exit 0
fi

mkdir -p "$ROOT/work"
TASK_TMP="$(mktemp -d "$ROOT/work/.grafikkpilot-20261006.XXXXXX")"
trap 'rm -rf "$TASK_TMP"' EXIT
git -C "$ROOT" fetch --depth 1 origin "refs/heads/$ART_BRANCH"
[ "$(git -C "$ROOT" rev-parse FETCH_HEAD)" = "$ART_COMMIT" ] || {
    echo "Grafikkgrenen har en annen commit enn den kontrollerte pakken. Avbryter."
    exit 1
}
git -C "$ROOT" archive "$ART_COMMIT" | tar -x -C "$TASK_TMP"
(cd "$TASK_TMP" && sha256sum --quiet -c SHA256SUMS)
mv -T "$TASK_TMP" "$DEST"
trap - EXIT
echo "Grafikkpilot hentet og sjekket: $DEST"
echo "Les docs/GRAFIKKPILOT.md for kontroll og kjøring."
