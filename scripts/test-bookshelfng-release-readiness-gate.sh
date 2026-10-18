#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
guard="$repo_root/scripts/require-bookshelfng-release-ready.sh"
build_workflow="$repo_root/.github/workflows/build.yml"
distribution_workflow="$repo_root/.github/workflows/release-distribution.yml"
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
tag_publish_condition="if: github.event_name == 'push' && startsWith(github.ref, 'refs/tags/main-') && vars.BOOKSHELFNG_RELEASE_READY == 'true'"
if [[ "$(grep -Fc "$tag_publish_condition" "$build_workflow")" -ne 4 ]]; then
  echo 'Every BookshelfNG tag publication job must check the release readiness gate.' >&2
  exit 1
fi
grep -Fq 'vars.BOOKSHELFNG_RELEASE_READY || '\''false'\''' "$distribution_workflow"
grep -Fq 'if [[ "${BOOKSHELFNG_RELEASE_READY,,}" != true ]]; then' "$distribution_workflow"
grep -Fq 'BookshelfNG release distribution is frozen until retirement acceptance is complete.' "$distribution_workflow"
grep -Fq 'vars.BOOKSHELFNG_RELEASE_READY || '\''false'\''' "$bridge_workflow"
grep -Fq '"${BRIDGE_ENABLED,,}" == true && "${RELEASE_READY,,}" == true' "$bridge_workflow"

echo 'BookshelfNG release and bridge publication gates fail closed.'
