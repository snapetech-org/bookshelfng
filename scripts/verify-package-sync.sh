#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(git -C "$script_dir/.." rev-parse --show-toplevel)"
work_dir="$(mktemp -d)"
trap 'rm -rf "$work_dir"' EXIT

unraid_url="${BOOKSHELFNG_UNRAID_GIT_URL:-https://github.com/snapetech-org/bookshelfng-unraid.git}"
unraid_branch="${BOOKSHELFNG_UNRAID_BRANCH:-main}"

if ! command -v rsync >/dev/null 2>&1; then
	echo "rsync is required to verify package repository sync." >&2
	exit 1
fi

for source_path in packaging/unraid/README.md; do
	if [[ ! -f "$repo_root/$source_path" ]]; then
		echo "Committed package source is missing $source_path." >&2
		exit 1
	fi
done

git clone --quiet --depth 1 --branch "$unraid_branch" "$unraid_url" "$work_dir/unraid"

check_tree() {
	local label="$1"
	local source_dir="$2"
	local target_dir="$3"
	shift 3
	local -a excludes=("$@")
	local changes

	changes="$(rsync --recursive --links --perms --checksum --omit-dir-times \
		--delete --dry-run --itemize-changes --out-format='%i %n%L' \
		"${excludes[@]}" "$source_dir/" "$target_dir/")"
	if [[ -n "$changes" ]]; then
		echo "$label package checkout differs from the committed package source:" >&2
		printf '%s\n' "$changes" >&2
		return 1
	fi
	echo "$label package checkout matches the committed package source."
}

check_file() {
	local label="$1"
	local source_file="$2"
	local target_file="$3"
	if [[ ! -f "$target_file" ]] || ! cmp -s "$source_file" "$target_file"; then
		echo "$label package file differs from the committed package source: ${source_file##*/}" >&2
		return 1
	fi
}

check_package_docs() {
	local source_docs="$repo_root/packaging/unraid/docs"
	local target_docs="$work_dir/unraid/docs"
	local target_manifest="$work_dir/unraid/.bookshelfng-package-doc-files"
	local expected_manifest="$work_dir/expected-package-doc-files"
	local package_doc

	: > "$expected_manifest"
	if [[ -d "$source_docs" ]]; then
		find "$source_docs" \( -type f -o -type l \) -printf '%P\n' | LC_ALL=C sort > "$expected_manifest"
	fi

	if [[ ! -f "$target_manifest" ]]; then
		echo "Unraid docs package manifest is missing from the companion repository." >&2
		return 1
	fi

	if ! diff -u "$expected_manifest" <(LC_ALL=C sort "$target_manifest"); then
		echo "Unraid docs package manifest differs from the committed package source." >&2
		return 1
	fi

	while IFS= read -r package_doc; do
		[[ -n "$package_doc" ]] || continue
		check_file "Unraid docs" "$source_docs/$package_doc" "$target_docs/$package_doc"
	done < "$expected_manifest"

	echo "Unraid docs package files match the committed package source."
}

# The Unraid repository also owns release notes outside the package source.
# Match exactly the paths managed by sync-unraid-package.sh.
for file in README.md ca_profile.xml; do
	check_file "Unraid" "$repo_root/packaging/unraid/$file" "$work_dir/unraid/$file"
done
check_tree "Unraid templates" "$repo_root/packaging/unraid/templates" "$work_dir/unraid/templates"
# The companion docs directory also contains source docs mirrored outside the
# Unraid package. Compare only package-owned paths from its explicit manifest.
check_package_docs
