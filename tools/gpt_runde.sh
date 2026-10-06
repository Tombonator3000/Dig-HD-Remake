#!/usr/bin/env bash
# Én runde i samarbeidet med ChatGPT. Claude kjører denne jevnlig.
#
#   1. Setter opp det som mangler (spillfiler, pipeline, uttrekk, jobber)
#   2. Henter nye bilder fra grenen gpt-arbeid
#   3. Kontrollerer dem (dighd gpt-inn) og lager HD-rom og HD-objekter
#   4. Bygger modden mods/gpt av de godkjente rommene og objektbildene og publiserer den i grenen hd-mod
#   5. Skriver ny ORDRE.md og sender status, rapport og retur tilbake til grenen
#
# Bruk: tools/gpt_runde.sh [--beskjed "tekst til ChatGPT"] ...
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
BESKJED=()
while [ $# -gt 0 ]; do
	case "$1" in
	--beskjed) BESKJED+=(--beskjed "$2"); shift 2 ;;
	*) echo "Ukjent valg: $1"; exit 1 ;;
	esac
done

# 1. Oppsett
[ -f game/DIG.LA1 ] || tools/hent_spilldata.sh
if ! command -v dighd >/dev/null 2>&1; then
	[ -x .venv/bin/dighd ] || { python3 -m venv .venv && .venv/bin/pip install -q -e "pipeline[dev]"; }
	export PATH="$ROOT/.venv/bin:$PATH"
fi
[ -f work/extract/rooms.json ] || dighd extract --only la1

# 2. Hent
before="$(sha256sum work/gpt-ferdig/provenance.json 2>/dev/null || true)"
tools/gpt_gren.sh hent

# 3. Kontroller
dighd gpt-inn
after="$(sha256sum work/gpt-ferdig/provenance.json 2>/dev/null || true)"

# 4. Mod, bare når noe nytt er godkjent. Rommene med HD-bakgrunn velges med --rooms.
#    Godkjente objektbilder i work/gpt-ferdig/objects kommer med uansett, også i rom
#    uten HD-bakgrunn (de får ingen automatisk oppskalert bakgrunn).
if [ "$before" != "$after" ] && [ -d work/gpt-ferdig ]; then
	rooms="$(ls work/gpt-ferdig/rooms 2>/dev/null | sed -n 's/^room0*\([0-9][0-9]*\)\.png$/\1/p' | paste -sd, - || true)"
	objects="$(ls work/gpt-ferdig/objects 2>/dev/null | grep -c '^obj.*\.png$' || true)"
	if [ -n "$rooms" ] || [ "${objects:-0}" -gt 0 ]; then
		rm -rf mods/gpt
		dighd build-mod --name gpt --method lanczos-sharp --rooms "${rooms:-ingen}" --egne work/gpt-ferdig
		tools/mod_gren.sh send mods/gpt
	fi
else
	echo "Ingen nye godkjente rom eller objekter denne runden."
fi

# 5. Ordre og status tilbake
dighd gpt-ordre "${BESKJED[@]}"
tools/gpt_gren.sh send
echo "Runden er ferdig. Rapport: work/gpt/RAPPORT.md, ordre: work/gpt/ORDRE.md"
