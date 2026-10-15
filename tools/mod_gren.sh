#!/usr/bin/env bash
# Publiserer eller henter den ferdige HD-modden via grenen hd-mod.
#
#   tools/mod_gren.sh send [modmappe] [--tving]   Legger mods/gpt (standard) i grenen hd-mod som én commit og pusher
#   tools/mod_gren.sh hent [modmappe]             Henter grenen hd-mod til mods/gpt (standard)
#
# Grenen inneholder bare siste versjon (én commit som erstattes), så repoet ikke vokser for hver runde.
# Den publiserte modden er fasit: Codex sine rettinger (r3 til r12) finnes bare der. send stopper derfor
# hvis modden mister eller endrer filer mot den publiserte uten at enheten står som erstattet eller
# fjernet i mod.json. Det står der når modden er laget med dighd flett-mod, slik tools/gpt_runde.sh
# gjør. --tving hopper over sjekken, bare når Tom vil erstatte hele modden.
# Kjør spillet etterpå med: engine/run.sh gpt
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
BRANCH=hd-mod
CMD="${1:-}"
[ $# -gt 0 ] && shift
MOD="$ROOT/mods/gpt"
TVING=()
for arg in "$@"; do
	case "$arg" in
	--tving) TVING=(--tving) ;;
	*) MOD="$arg" ;;
	esac
done

# Skriver sjekksummene til den publiserte modden til fil $1 uten å hente bildene: bare trærne, i en
# egen tom git-mappe, så arbeidskopien ikke blir en delvis klone. Gir 0 når de er hentet, 2 når
# grenen ikke finnes ennå og 1 ved andre feil.
published_sums() {
	local url tmp rc
	url="$(git -C "$ROOT" remote get-url origin)"
	git ls-remote --exit-code --heads "$url" "$BRANCH" >/dev/null
	rc=$?
	[ "$rc" -eq 0 ] || { [ "$rc" -eq 2 ] && return 2; return 1; }
	tmp="$(mktemp -d)"
	git -C "$tmp" init -q
	git -C "$tmp" remote add origin "$url"
	rc=1
	if git -C "$tmp" fetch -q --depth 1 --filter=blob:none origin "refs/heads/$BRANCH" &&
		git -C "$tmp" cat-file -p FETCH_HEAD:SHA256SUMS > "$1"; then
		rc=0
	fi
	rm -rf "$tmp"
	return "$rc"
}

case "$CMD" in
send)
	[ -f "$MOD/mod.json" ] || { echo "Fant ikke $MOD/mod.json. Bygg modden først."; exit 1; }
	SUMS="$(mktemp)"
	set +e
	published_sums "$SUMS"
	rc=$?
	set -e
	case "$rc" in
	0)
		if ! python3 "$ROOT/pipeline/dighd/modflett.py" sjekk --publisert "$SUMS" --ut "$MOD" "${TVING[@]}"; then
			rm -f "$SUMS"
			exit 1
		fi
		;;
	2) echo "Grenen $BRANCH finnes ikke ennå, så det er ingenting å sammenligne med." ;;
	*)
		rm -f "$SUMS"
		echo "Fikk ikke hentet sjekksummene til den publiserte modden. Stopper uten å publisere."
		exit 1
		;;
	esac
	rm -f "$SUMS"
	TMP="$(mktemp -d "$ROOT/work/.mod-gren.XXXXXX")"
	trap 'rm -rf "$TMP"' EXIT
	git -C "$TMP" init -q
	git -C "$TMP" checkout -q -b "$BRANCH"
	cp -r "$MOD"/. "$TMP/"
	# README først, så den er med i sjekksummene. En README som følger med modden, beholdes.
	[ -f "$TMP/README.md" ] || printf '# hd-mod\n\nSiste HD-mod for The Dig HD Remake. Hentes med tools/mod_gren.sh hent.\n' > "$TMP/README.md"
	(cd "$TMP" && find . -path ./.git -prune -o -type f -print | sort | sed 's|^\./||' | grep -v '^SHA256SUMS$' | xargs sha256sum > SHA256SUMS)
	git -C "$TMP" add -A
	git -C "$TMP" -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -q -m "HD-mod $(date '+%Y-%m-%d %H:%M')"
	git -C "$TMP" push -q -f "$(git -C "$ROOT" remote get-url origin)" "$BRANCH:$BRANCH"
	echo "Modden er publisert i grenen $BRANCH ($(du -sh "$MOD" | cut -f1))."
	;;
hent)
	# A release pins the asset revision before compiling. A later update to
	# hd-mod must not change the graphics halfway through that build.
	if [ -n "${HD_MOD_REF:-}" ]; then
		git -C "$ROOT" fetch -q --depth 1 origin "$HD_MOD_REF"
		git -C "$ROOT" update-ref "refs/remotes/origin/$BRANCH" FETCH_HEAD
	else
		git -C "$ROOT" fetch -q --depth 1 origin "+refs/heads/$BRANCH:refs/remotes/origin/$BRANCH"
	fi
	rm -rf "$MOD"
	mkdir -p "$MOD"
	git -C "$ROOT" archive "refs/remotes/origin/$BRANCH" | tar -x -C "$MOD"
	(cd "$MOD" && sha256sum --quiet -c SHA256SUMS)
	echo "Modden er hentet til $MOD og sjekksummene stemmer. Start med: engine/run.sh $(basename "$MOD")"
	;;
*)
	echo "Bruk: tools/mod_gren.sh send [modmappe] [--tving] | hent [modmappe]"
	exit 1
	;;
esac
