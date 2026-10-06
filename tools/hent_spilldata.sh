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

echo "Sjekker sjekksummer ..."
(cd game && sha256sum --quiet -c SHA256SUMS)
echo "Ferdig. Spillfilene ligger i $ROOT/game"
echo "Musikk og tale (DIGMUSIC.BUN, DIGVOICE.BUN) må legges i game/ manuelt fra Drive hvis du vil spille med lyd."
