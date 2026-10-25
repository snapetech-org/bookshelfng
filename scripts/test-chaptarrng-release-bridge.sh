#!/usr/bin/env bash
# These checks match literal GitHub Actions expressions in the workflow file.
# shellcheck disable=SC2016
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
workflow="$repo_root/.github/workflows/chaptarrng-release-bridge.yml"

required_lines=(
  "TARGET_REPOSITORY: snapetech-org/chaptarrng"
  'BRIDGE_ENABLED: ${{ vars.CHAPTARRNG_MIGRATION_BRIDGE_ENABLED || '\''false'\'' }}'
  'RELEASE_READY: ${{ vars.BOOKSHELFNG_RELEASE_READY || '\''false'\'' }}'
  'if [[ "${BRIDGE_ENABLED,,}" == true && "${RELEASE_READY,,}" == true ]]; then enabled=true; fi'
  "PUBLISH_GHCR_ALIASES: 'false'"
  "PUBLISH_LEGACY_ALIASES: 'true'"
  'source_tag="ghcr.io/snapetech/chaptarrng:${VERSION}"'
  'SOURCE_IMAGE: ghcr.io/snapetech/chaptarrng@'
  'image="ghcr.io/snapetech/chaptarrng:${VERSION}"'
  'repository: ghcr.io/snapetech/chaptarrng'
  'grep -Fq "image: \"ghcr.io/snapetech/chaptarrng@${digest}\""'
  'matching-refs/tags/bookshelfng-bridge-${tag}-'
  'grep -Fqx "refs/tags/bookshelfng-bridge-${tag}-$1" <<< "$marker_refs"'
)

for expected in "${required_lines[@]}"; do
  if ! grep -Fq "$expected" "$workflow"; then
    echo "ChaptarrNG bridge is missing required release contract: $expected" >&2
    exit 1
  fi
done

if grep -Fq 'fetch-depth: 0' "$workflow"; then
  echo 'The bridge must not fetch full Git history for release markers or publisher tags.' >&2
  exit 1
fi

discover_job="$(sed -n '/^  discover-release:/,/^  publisher-credentials:/p' "$workflow")"
if grep -Fq 'actions/checkout' <<< "$discover_job"; then
  echo 'Release discovery must use the read-only GitHub API instead of cloning the repository.' >&2
  exit 1
fi

grep -Fq "if: github.ref == 'refs/heads/main' && needs.discover-release.outputs.ready == 'true' && needs.discover-release.outputs.enabled == 'true'" "$workflow"
grep -Fq 'needs: [discover-release]' "$workflow"

[[ "$(grep -Fc "PUBLISH_LEGACY_ALIASES: 'true'" "$workflow")" -eq 1 ]]
grep -Fq 'delegated to the separately scoped personal-account bridge' "$workflow"
if grep -Eq 'publish-ghcr-aliases|outputs\.ghcr|for channel in ghcr ' "$workflow"; then
  echo 'The BookshelfNG organization workflow must not publish personal-account GHCR aliases.' >&2
  exit 1
fi

if grep -Fq 'ghcr.io/snapetech-org/chaptarrng' "$workflow"; then
  echo 'The bridge must use the existing public ChaptarrNG package namespace.' >&2
  exit 1
fi

echo 'ChaptarrNG release bridge image identity tests passed.'
