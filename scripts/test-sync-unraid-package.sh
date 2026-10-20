#!/usr/bin/env bash
set -euo pipefail

source_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
origin="$(git -C "$source_root" remote get-url origin)"
case "$origin" in
  *bookshelfng-unraid.git|*bookshelfng-unraid|*bookshelfng.git|*bookshelfng) project=bookshelfng ;;
  *chaptarrng-unraid.git|*chaptarrng-unraid|*chaptarrng.git|*chaptarrng) project=chaptarrng ;;
  *) echo "Unrecognized package source repository." >&2; exit 2 ;;
esac

work="$(mktemp -d "${TMPDIR:-/tmp}/${project}-unraid-hook.XXXXXX")"
trap 'rm -rf -- "$work"' EXIT
repo="$work/$project"
mkdir -p "$repo/scripts"
cp "$source_root/scripts/sync-unraid-package.sh" "$repo/scripts/"
git -C "$repo" init --quiet --initial-branch=codex/hook-test
git -C "$repo" remote add origin "https://github.com/snapetech-org/${project}.git"
git -C "$repo" config user.name 'Package Hook Test'
git -C "$repo" config user.email 'package-hook-test@example.invalid'
git -C "$repo" add scripts/sync-unraid-package.sh
git -C "$repo" commit --quiet -m 'test fixture'

feature_output="$(cd "$repo" && bash scripts/sync-unraid-package.sh)"
grep -Fq "Skipping Unraid package sync from 'codex/hook-test'" <<< "$feature_output"
[[ ! -e "$work/${project}-unraid" ]]

git -C "$repo" switch --quiet --create main
main_output="$(cd "$repo" && bash scripts/sync-unraid-package.sh 2>&1 || true)"
grep -Fq 'No committed Unraid package source' <<< "$main_output"
if grep -Fq 'Skipping Unraid package sync' <<< "$main_output"; then
  echo 'The main branch was incorrectly skipped.' >&2
  exit 1
fi

echo 'Unraid package hook branch guard tests passed.'
