#!/usr/bin/env bash
# Henter spillfilene fra grenen "spilldata" inn i game/ og sjekker sjekksummene.
# Bruk: tools/hent_spilldata.sh            (fra roten av repoet)
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

echo "Henter grenen spilldata ..."
git fetch --depth 1 origin "+refs/heads/spilldata:refs/remotes/origin/spilldata"

echo "Pakker ut til game/ ..."
mkdir -p game
git archive refs/remotes/origin/spilldata game | tar -x -C "$ROOT"

# Musikk og tale ligger i deler på 90 MB (GitHubs grense er 100 MB per fil)
for f in DIGMUSIC DIGVOICE; do
	if ls game/$f.BUN.[0-9][0-9][0-9] >/dev/null 2>&1; then
		echo "Setter sammen $f.BUN ..."
		cat game/$f.BUN.[0-9][0-9][0-9] > game/$f.BUN
		rm game/$f.BUN.[0-9][0-9][0-9]
	fi
done

echo "Sjekker sjekksummer ..."
(cd game && sha256sum --quiet -c SHA256SUMS)
[ -f game/SHA256SUMS.lyd ] && (cd game && sha256sum --quiet -c SHA256SUMS.lyd)
echo "Ferdig. Spillfilene, musikken og talen ligger i $ROOT/game"
