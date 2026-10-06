#!/usr/bin/env bash
# Synker ChatGPT-jobbene (work/gpt) med den private grenen gpt-arbeid.
#
#   tools/gpt_gren.sh send   Legger jobbene, status, rapport og bestillingen inn i grenen og pusher
#   tools/gpt_gren.sh hent   Henter grenen og kopierer ChatGPT sine resultater og notater til work/gpt
#
# Vanlig runde: dighd gpt-pakke, send, (ChatGPT jobber), hent, dighd gpt-inn, send.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
WORK="$ROOT/work/gpt"
TREE="$ROOT/work/.gpt-gren"
BRANCH=gpt-arbeid

ensure_tree() {
	if [ -d "$TREE/.git" ] || [ -f "$TREE/.git" ]; then
		git -C "$TREE" fetch -q origin "+refs/heads/$BRANCH:refs/remotes/origin/$BRANCH" 2>/dev/null && git -C "$TREE" merge -q --ff-only "origin/$BRANCH" 2>/dev/null || true
		return
	fi
	git -C "$ROOT" worktree prune
	if git -C "$ROOT" fetch -q origin "+refs/heads/$BRANCH:refs/remotes/origin/$BRANCH" 2>/dev/null; then
		git -C "$ROOT" worktree add -q -B "$BRANCH" "$TREE" "origin/$BRANCH"
	else
		git -C "$ROOT" worktree add -q --orphan -b "$BRANCH" "$TREE"
	fi
}

copy_jobs_out() {
	# Jobbfiler og Claude sine filer ut til grenen. Resultater og notater fra ChatGPT røres ikke.
	mkdir -p "$TREE/jobber" "$TREE/stil"
	[ -f "$TREE/stil/.gitkeep" ] || touch "$TREE/stil/.gitkeep"
	for d in "$WORK"/jobber/*/; do
		id="$(basename "$d")"
		mkdir -p "$TREE/jobber/$id"
		for f in referanse.png original_1x.png prompt.txt jobb.json; do
			cp "$d/$f" "$TREE/jobber/$id/$f"
		done
		if [ -f "$d/retur.md" ]; then cp "$d/retur.md" "$TREE/jobber/$id/retur.md"; else rm -f "$TREE/jobber/$id/retur.md"; fi
	done
	for f in JOBBER.md status.csv RAPPORT.md; do
		[ -f "$WORK/$f" ] && cp "$WORK/$f" "$TREE/$f"
	done
	cp "$ROOT/docs/BESTILLING-CHATGPT.md" "$TREE/BESTILLING.md"
	cp "$ROOT/docs/gpt-arbeid-AGENTS.md" "$TREE/AGENTS.md"
	[ -f "$TREE/README.md" ] || printf '# gpt-arbeid\n\nArbeidsbordet for HD-grafikken. Les AGENTS.md og BESTILLING.md.\n' > "$TREE/README.md"
}

copy_results_in() {
	n=0
	for d in "$TREE"/jobber/*/; do
		id="$(basename "$d")"
		[ -d "$WORK/jobber/$id" ] || continue
		for f in "$d"resultat.* "$d"notat.md; do
			[ -f "$f" ] || continue
			if ! cmp -s "$f" "$WORK/jobber/$id/$(basename "$f")"; then
				cp "$f" "$WORK/jobber/$id/"
				n=$((n + 1))
			fi
		done
	done
	echo "Hentet $n nye eller endrede filer fra ChatGPT."
}

case "${1:-}" in
send)
	[ -d "$WORK/jobber" ] || { echo "Ingen jobber i $WORK. Kjør dighd gpt-pakke først."; exit 1; }
	ensure_tree
	copy_jobs_out
	git -C "$TREE" add -A
	if git -C "$TREE" diff --cached --quiet; then
		echo "Ingen endringer å sende."
	else
		git -C "$TREE" commit -q -m "Claude: jobber og status $(date '+%Y-%m-%d %H:%M')"
		git -C "$TREE" push -q -u origin "$BRANCH"
		echo "Sendt til grenen $BRANCH."
	fi
	;;
hent)
	ensure_tree
	copy_results_in
	echo "Kjør nå: dighd gpt-inn"
	;;
*)
	echo "Bruk: tools/gpt_gren.sh send|hent"
	exit 1
	;;
esac
