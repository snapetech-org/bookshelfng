#!/usr/bin/env bash
set -euo pipefail

release_ready="${BOOKSHELFNG_RELEASE_READY:-false}"
if [[ "${release_ready,,}" != "true" ]]; then
  echo "BookshelfNG release publishing is frozen until retirement acceptance is complete. Set BOOKSHELFNG_RELEASE_READY=true only after all migration, parity, rollback, and channel gates pass." >&2
  exit 1
fi
