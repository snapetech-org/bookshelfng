#!/usr/bin/env bash
set -euo pipefail

: "${HARDCOVER_DIGEST:?The pushed Hardcover image digest is required}"
: "${HARDCOVER_VERSION_TAG:?The versioned Hardcover release tag is required}"
: "${GITHUB_REPOSITORY:?GitHub Actions repository context is required}"

aliases=(hardcover main master latest stable "$HARDCOVER_VERSION_TAG")
images=("ghcr.io/$GITHUB_REPOSITORY" "docker.io/snapetech/bookshelfng")

for image in "${images[@]}"; do
	for tag in "${aliases[@]}"; do
		reference="$image:$tag"
		actual_digest="$(docker buildx imagetools inspect \
			--format '{{json .Manifest}}' "$reference" | jq -er '.digest')"
		if [[ "$actual_digest" != "$HARDCOVER_DIGEST" ]]; then
			echo "$reference resolves to $actual_digest; expected $HARDCOVER_DIGEST." >&2
			exit 1
		fi
		printf '%s -> %s\n' "$reference" "$actual_digest"
	done
done
