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
package_path=packaging/unraid
source_manifest_path=.bookshelfng-source-files
source_commit_path=.bookshelfng-source-commit
package_docs_manifest_path=.bookshelfng-package-doc-files
renamed_readme=docs/bookshelfng-source/README.md
renamed_unraid_note=docs/bookshelfng-source/release-notes/2026-09-27-unraid-user-installation-guidance.md
source_unraid_note=release-notes/2026-09-27-unraid-user-installation-guidance.md

if ! git -C "$repo_root" cat-file -e "$source_commit:$package_path" >/dev/null 2>&1; then
	echo "No committed Unraid package source exists at $package_path in $source_commit; cannot sync." >&2
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
new_manifest="$scratch_dir/source-files"
new_package_docs_manifest="$scratch_dir/package-doc-files"
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
git -C "$repo_root" archive --format=tar "$source_commit" | tar -xf - -C "$source_stage"

# The Unraid repository owns its root README and legacy installation note.
# Mirror the application README and the colliding source note under docs instead.
: > "$new_manifest"
declare -A new_source_files=()
while IFS= read -r -d '' source_path; do
	case "$source_path" in
		README.md|ca_profile.xml|templates/*|docs/installation.md|docs/bookshelfng-source/*|"$source_unraid_note"|"$source_manifest_path"|"$source_commit_path"|"$package_docs_manifest_path") continue ;;
	esac
	new_source_files["$source_path"]=1
	printf '%s\n' "$source_path" >> "$new_manifest"
done < <(git -C "$repo_root" ls-tree -r -z --name-only "$source_commit")

if [[ -f "$worktree_dir/$source_manifest_path" ]]; then
	while IFS= read -r old_source_path; do
		if [[ -n "$old_source_path" && -z "${new_source_files[$old_source_path]+present}" ]]; then
			git -C "$worktree_dir" rm --ignore-unmatch -- "$old_source_path" >/dev/null
		fi
	done < "$worktree_dir/$source_manifest_path"
fi

if [[ -s "$new_manifest" ]]; then
	rsync --archive --relative --files-from="$new_manifest" "$source_stage/" "$worktree_dir/"
fi

: > "$new_package_docs_manifest"
declare -A new_package_doc_files=()
if [[ -d "$source_stage/$package_path/docs" ]]; then
	while IFS= read -r -d '' package_doc_file; do
		package_doc_path="${package_doc_file#"$source_stage/$package_path/docs/"}"
		new_package_doc_files["$package_doc_path"]=1
		printf '%s\n' "$package_doc_path" >> "$new_package_docs_manifest"
	done < <(find "$source_stage/$package_path/docs" \( -type f -o -type l \) -print0)
fi

if [[ -f "$worktree_dir/$package_docs_manifest_path" ]]; then
	while IFS= read -r old_package_doc_path; do
		if [[ -n "$old_package_doc_path" && -z "${new_package_doc_files[$old_package_doc_path]+present}" ]]; then
			git -C "$worktree_dir" rm --ignore-unmatch -- "docs/$old_package_doc_path" >/dev/null
		fi
	done < "$worktree_dir/$package_docs_manifest_path"
fi

source_dir="$source_stage/$package_path"
for required_file in README.md ca_profile.xml "templates/$source_repo.xml"; do
	if [[ ! -f "$source_dir/$required_file" ]]; then
		echo "The committed Unraid package source is missing $package_path/$required_file." >&2
		exit 1
	fi
done

rsync --archive "$source_dir/README.md" "$worktree_dir/README.md"
rsync --archive "$source_dir/ca_profile.xml" "$worktree_dir/ca_profile.xml"
rsync --archive --delete "$source_dir/templates/" "$worktree_dir/templates/"
if [[ -s "$new_package_docs_manifest" ]]; then
	rsync --archive --relative --files-from="$new_package_docs_manifest" "$source_dir/docs/" "$worktree_dir/docs/"
fi

mkdir -p "$(dirname "$worktree_dir/$renamed_readme")"
rsync --archive "$source_stage/README.md" "$worktree_dir/$renamed_readme"
if [[ -f "$source_stage/$source_unraid_note" ]]; then
	mkdir -p "$(dirname "$worktree_dir/$renamed_unraid_note")"
	rsync --archive "$source_stage/$source_unraid_note" "$worktree_dir/$renamed_unraid_note"
fi
cp "$new_manifest" "$worktree_dir/$source_manifest_path"
cp "$new_package_docs_manifest" "$worktree_dir/$package_docs_manifest_path"
printf '%s\n' "$source_commit" > "$worktree_dir/$source_commit_path"

git -C "$worktree_dir" add --all
if ! git -C "$worktree_dir" diff --cached --quiet; then
	short_source_commit="$(git -C "$repo_root" rev-parse --short "$source_commit")"
	git -C "$worktree_dir" -c core.hooksPath=/dev/null commit \
		-m "chore: sync full source and Unraid package from $short_source_commit" \
		-m "release-note: none"
fi

new_head="$(git -C "$worktree_dir" rev-parse HEAD)"
if [[ "$new_head" != "$remote_head" ]]; then
	GIT_TERMINAL_PROMPT=0 git -C "$worktree_dir" -c core.hooksPath=/dev/null push "$remote" "HEAD:refs/heads/$branch"
	echo "Synced source commit $(git -C "$repo_root" rev-parse --short "$source_commit") and Unraid package to $target_dir ($branch)."
else
	echo "Unraid source and package are already synced at $target_dir ($branch)."
fi
