#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(git -C "$script_dir/.." rev-parse --show-toplevel)"
source_branch="$(git -C "$repo_root" branch --show-current)"
source_commit="${1:-}"

if [[ -z "$source_commit" ]]; then
	if [[ "$source_branch" != "main" ]]; then
		echo "Skipping Unraid package sync from '$source_branch'; only main may update the companion repository."
		exit 0
	fi
	source_commit="$(git -C "$repo_root" rev-parse HEAD)"
elif ! git -C "$repo_root" rev-parse --verify --quiet "$source_commit^{commit}" >/dev/null; then
	echo "Unraid sync source is not a commit in $repo_root: $source_commit" >&2
	exit 1
fi

# Worktree directory names are arbitrary, so identify the product from its Git remote.
origin_url="$(git -C "$repo_root" remote get-url origin 2>/dev/null || true)"
source_repo="${origin_url%/}"
source_repo="${source_repo##*/}"
source_repo="${source_repo%.git}"

case "$source_repo" in
	bookshelfng|chaptarrng) ;;
	*)
		echo "Unraid sync is not configured for the source repository '$source_repo'." >&2
		exit 1
		;;
esac

target_repo="${source_repo}-unraid"
override_name="${source_repo^^}_UNRAID_REPO"
target_dir="${!override_name:-$(dirname "$repo_root")/$target_repo}"
remote=origin
branch=main
source_path=packaging/unraid

if ! git -C "$repo_root" cat-file -e "$source_commit:$source_path" >/dev/null 2>&1; then
	echo "No committed Unraid package source exists at $source_path in $source_commit; cannot sync." >&2
	exit 1
fi

if ! command -v rsync >/dev/null 2>&1; then
	echo "rsync is required to sync the Unraid package." >&2
	exit 1
fi

if [[ ! -d "$target_dir" ]] || ! git -C "$target_dir" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
	echo "Unraid companion checkout not found at $target_dir; clone it or set $override_name." >&2
	exit 1
fi

remote_url="$(git -C "$target_dir" config --get "remote.$remote.url" 2>/dev/null || true)"
case "$remote_url" in
	"https://github.com/snapetech-org/$target_repo.git"|"https://github.com/snapetech-org/$target_repo"|"git@github.com:snapetech-org/$target_repo.git"|"git@github.com:snapetech-org/$target_repo"|"ssh://git@github.com/snapetech-org/$target_repo.git") ;;
	*)
		echo "Remote '$remote' must point to snapetech-org/$target_repo (found: ${remote_url:-missing})." >&2
		exit 1
		;;
esac

scratch_dir="$(mktemp -d "${TMPDIR:-/tmp}/${target_repo}-sync.XXXXXX")"
worktree_dir="$scratch_dir/worktree"
source_stage="$scratch_dir/source"
mkdir -p "$source_stage"

cleanup() {
	if [[ -d "$worktree_dir" ]]; then
		git -C "$target_dir" worktree remove --force "$worktree_dir" >/dev/null 2>&1 || true
	fi
	rm -rf -- "$scratch_dir"
}
trap cleanup EXIT

git -C "$target_dir" fetch --prune "$remote"
if ! git -C "$target_dir" show-ref --verify --quiet "refs/remotes/$remote/$branch"; then
	echo "Remote '$remote' has no '$branch' branch in $target_dir." >&2
	exit 1
fi

remote_head="$(git -C "$target_dir" rev-parse "refs/remotes/$remote/$branch")"
git -C "$target_dir" worktree add --detach "$worktree_dir" "$remote_head"

# Fetch the exact source commit selected by post-commit or pre-push. This lets a
# push from a topic-named local branch sync only when its destination is main.
git -C "$worktree_dir" fetch --no-tags "$repo_root" "$source_commit"
if ! git -C "$worktree_dir" cat-file -e "$source_commit^{commit}" >/dev/null 2>&1; then
	echo "Could not fetch source commit $source_commit into the Unraid checkout." >&2
	exit 1
fi

if ! git -C "$worktree_dir" merge-base --is-ancestor "$source_commit" HEAD; then
	short_source_commit="$(git -C "$repo_root" rev-parse --short "$source_commit")"
	git -C "$worktree_dir" merge --no-commit --no-ff --allow-unrelated-histories -X ours "$source_commit"
else
	short_source_commit="$(git -C "$repo_root" rev-parse --short "$source_commit")"
fi

git -C "$repo_root" archive --format=tar "$source_commit" "$source_path" | tar -xf - -C "$source_stage"
source_dir="$source_stage/$source_path"

for required_file in README.md ca_profile.xml "templates/$source_repo.xml"; do
	if [[ ! -f "$source_dir/$required_file" ]]; then
		echo "The committed Unraid package source is missing $source_path/$required_file." >&2
		exit 1
	fi
done

# The companion keeps its Unraid package README at the repository root. Keep
# the application repository's README alongside the code so it is mirrored too.
rsync --archive "$source_dir/README.md" "$worktree_dir/README.md"
rsync --archive "$source_dir/ca_profile.xml" "$worktree_dir/ca_profile.xml"
rsync --archive --delete "$source_dir/templates/" "$worktree_dir/templates/"
if [[ -d "$source_dir/docs" ]]; then
	rsync --archive --delete "$source_dir/docs/" "$worktree_dir/docs/"
elif [[ -d "$worktree_dir/docs" ]]; then
	rm -rf -- "$worktree_dir/docs"
fi

mkdir -p "$worktree_dir/docs/bookshelfng-source"
git -C "$worktree_dir" show "$source_commit:README.md" > "$worktree_dir/docs/bookshelfng-source/README.md"
source_unraid_note="release-notes/2026-09-27-unraid-user-installation-guidance.md"
if git -C "$worktree_dir" cat-file -e "$source_commit:$source_unraid_note" 2>/dev/null; then
	mkdir -p "$worktree_dir/docs/bookshelfng-source/release-notes"
	git -C "$worktree_dir" show "$source_commit:$source_unraid_note" > "$worktree_dir/docs/bookshelfng-source/$source_unraid_note"
fi

git -C "$worktree_dir" add --all
if ! git -C "$worktree_dir" diff --cached --quiet; then
	git -C "$worktree_dir" commit -m "chore: sync full source and Unraid package from $short_source_commit"
fi

new_head="$(git -C "$worktree_dir" rev-parse HEAD)"
if [[ "$new_head" != "$remote_head" ]]; then
	GIT_TERMINAL_PROMPT=0 git -C "$worktree_dir" push "$remote" "HEAD:refs/heads/$branch"
	echo "Synced source commit $short_source_commit and Unraid package to $target_dir ($branch)."
else
	echo "Unraid source and package are already synced at $target_dir ($branch)."
fi
