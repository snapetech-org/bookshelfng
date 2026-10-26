#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
guard="$repo_root/scripts/require-bookshelfng-release-ready.sh"
build_workflow="$repo_root/.github/workflows/build.yml"
distribution_workflow="$repo_root/.github/workflows/release-distribution.yml"
publication_workflow="$repo_root/.github/workflows/release-publication.yml"
bridge_workflow="$repo_root/.github/workflows/chaptarrng-release-bridge.yml"

if env -u BOOKSHELFNG_RELEASE_READY bash "$guard" >/dev/null 2>&1; then
  echo 'The BookshelfNG release gate must reject an unset readiness variable.' >&2
  exit 1
fi

if BOOKSHELFNG_RELEASE_READY=false bash "$guard" >/dev/null 2>&1; then
  echo 'The BookshelfNG release gate must reject false.' >&2
  exit 1
fi

if BOOKSHELFNG_RELEASE_READY=1 bash "$guard" >/dev/null 2>&1; then
  echo 'The BookshelfNG release gate must reject non-boolean truthy values.' >&2
  exit 1
fi

BOOKSHELFNG_RELEASE_READY=true bash "$guard"
BOOKSHELFNG_RELEASE_READY=TRUE bash "$guard"

grep -Fq 'bash scripts/test-bookshelfng-release-readiness-gate.sh' "$build_workflow"
grep -Fq 'bash scripts/require-bookshelfng-release-ready.sh' "$build_workflow"
grep -Fq 'vars.BOOKSHELFNG_RELEASE_READY == '\''true'\''' "$build_workflow"
grep -Fq 'releases/download/v${pkgver}/BookshelfNG-v${pkgver}-linux-x64.tar.gz' "$repo_root/packaging/aur/PKGBUILD"
grep -Fq 'BookshelfNG-v${pkgver}-linux-x64' "$repo_root/packaging/aur/PKGBUILD"
if grep -Fq 'releases/download/main-v${pkgver}' "$repo_root/packaging/aur/PKGBUILD"; then
  echo 'The future AUR recipe must resolve the new v<version> release tag.' >&2
  exit 1
fi
tag_publish_condition="github.event_name == 'push' && startsWith(github.ref, 'refs/tags/v') && vars.BOOKSHELFNG_RELEASE_READY == 'true'"
if [[ "$(grep -Fc "$tag_publish_condition" "$build_workflow")" -ne 3 ]]; then
  echo 'Every BookshelfNG tag build and image publication job must check the release readiness gate.' >&2
  exit 1
fi
grep -Fq "github.event.workflow_run.conclusion == 'success'" "$publication_workflow"
grep -Fq "github.event.workflow_run.event == 'push'" "$publication_workflow"
grep -Fq "startsWith(github.event.workflow_run.head_branch, 'v')" "$publication_workflow"
grep -Fq "github.event.workflow_run.head_repository.full_name == github.repository" "$publication_workflow"
grep -Fq "vars.BOOKSHELFNG_RELEASE_READY == 'true'" "$publication_workflow"
grep -Fq '.path == ".github/workflows/build.yml"' "$publication_workflow"
grep -Fq 'gh release view "$RELEASE_TAG" --repo "$GITHUB_REPOSITORY"' "$publication_workflow"
grep -Fq 'gh release upload "$TAG" --repo "$GITHUB_REPOSITORY" --clobber "${release_files[@]}"' "$publication_workflow"
grep -Fq 'gh release edit "$TAG" --repo "$GITHUB_REPOSITORY" --draft=false' "$publication_workflow"
checkout_line="$(grep -nF 'actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1' "$publication_workflow" | head -n 1 | cut -d: -f1)"
runtime_pack_line="$(grep -nF '      - name: Find reusable runtime-pack artifact' "$publication_workflow" | cut -d: -f1)"
if [[ -z "$checkout_line" || -z "$runtime_pack_line" || "$checkout_line" -ge "$runtime_pack_line" ]]; then
  echo 'The release preflight must check out the validated tag before inspecting reusable runtime-pack artifacts.' >&2
  exit 1
fi
grep -Fq '          ref: ${{ steps.validate.outputs.tag }}' "$publication_workflow"
grep -Fq '          fetch-depth: 0' "$publication_workflow"
prepare_contents_permission="$(awk '/^  prepare:$/ { in_prepare = 1 } /^  build:$/ { in_prepare = 0 } in_prepare && /^      contents:/ { print $2 }' "$publication_workflow")"
if [[ "$prepare_contents_permission" != write ]]; then
  echo 'The release preflight needs write access to list draft releases.' >&2
  exit 1
fi
grep -Fq '.tagName == $tag and .isDraft == true and .isPrerelease == false' "$publication_workflow"
if grep -Fq 'releases/tags/$RELEASE_TAG' "$publication_workflow"; then
  echo 'The release publisher must resolve draft releases through the authenticated GitHub CLI.' >&2
  exit 1
fi
grep -Fq 'needs: [prepare]' "$publication_workflow"
grep -Fq 'needs: [prepare, build]' "$publication_workflow"
grep -Fq 'needs: [prepare, publish-assets]' "$publication_workflow"
grep -Fq 'vars.BOOKSHELFNG_RELEASE_READY || '\''false'\''' "$distribution_workflow"
grep -Fq 'if [[ "${BOOKSHELFNG_RELEASE_READY,,}" != true ]]; then' "$distribution_workflow"
grep -Fq 'BookshelfNG release distribution is frozen until retirement acceptance is complete.' "$distribution_workflow"
grep -Fq 'vars.BOOKSHELFNG_RELEASE_READY || '\''false'\''' "$bridge_workflow"
grep -Fq '"${BRIDGE_ENABLED,,}" == true && "${RELEASE_READY,,}" == true' "$bridge_workflow"

echo 'BookshelfNG release and bridge publication gates fail closed.'
