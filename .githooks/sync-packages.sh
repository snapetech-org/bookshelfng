#!/usr/bin/env bash
set -uo pipefail

trigger="${1:-manual}"
source_commit="${2:-}"
repo_root="$(git rev-parse --show-toplevel)"
origin_url="$(git -C "$repo_root" remote get-url origin 2>/dev/null || true)"
source_repo="${origin_url%/}"
source_repo="${source_repo##*/}"
source_repo="${source_repo%.git}"
overall_status=0

if [[ "$source_repo" == "bookshelfng-unraid" || "$source_repo" == "chaptarrng-unraid" ]]; then
	echo "Skipping source sync inside the Unraid companion repository '$source_repo'."
	exit 0
fi

# Git exports the current repository context to hooks. Clear it before the
# package scripts run Git commands against their separate checkouts.
while IFS= read -r git_environment_variable; do
	unset "$git_environment_variable"
done < <(git -C "$repo_root" rev-parse --local-env-vars)

echo "Running Unraid source and package sync ($trigger)."

for script in sync-unraid-package.sh; do
	sync_script="$repo_root/scripts/$script"
	if [[ ! -f "$sync_script" ]]; then
		echo "Package sync script not found: $sync_script" >&2
		overall_status=1
		continue
	fi

	if [[ -n "$source_commit" ]]; then
		if bash "$sync_script" "$source_commit"; then
			:
		else
			sync_status=$?
			echo "Unraid sync failed: $script (exit $sync_status)." >&2
			overall_status=1
		fi
	elif bash "$sync_script"; then
		:
	else
		sync_status=$?
		echo "Unraid sync failed: $script (exit $sync_status)." >&2
		overall_status=1
	fi
done

if [[ "$overall_status" -ne 0 ]]; then
	echo "Unraid source and package sync did not complete; $trigger is failing." >&2
fi

exit "$overall_status"
