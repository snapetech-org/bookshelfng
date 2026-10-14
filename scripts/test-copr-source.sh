#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
work="$(mktemp -d "${TMPDIR:-/tmp}/bookshelfng-copr-source-test.XXXXXX")"
trap 'rm -rf -- "$work"' EXIT
mkdir -p "$work/bin"

cat > "$work/bin/curl" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
output=""
while (($#)); do
  case "$1" in
    --output) output="$2"; shift 2 ;;
    *) shift ;;
  esac
done
[[ -n "$output" ]]
if [[ "$output" == *.sha256 ]]; then
  source_file="${output%.sha256}"
  digest="$(sha256sum "$source_file" | cut -d ' ' -f1)"
  if [[ "${COPR_FIXTURE_BAD_CHECKSUM:-false}" == true ]]; then digest="$(printf '0%.0s' {1..64})"; fi
  printf '%s  %s\n' "$digest" "$(basename "$source_file")" > "$output"
else
  printf 'fixture source rpm\n' > "$output"
fi
SH

cat > "$work/bin/rpm2cpio" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
cat -- "$1"
SH

cat > "$work/bin/cpio" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
cat >/dev/null
tag="${COPR_FIXTURE_TAG:-}"
if [[ "$tag" =~ ^main-v([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)$ ]]; then
  version="${BASH_REMATCH[1]}"
  files=(bookshelfng.spec "bookshelfng-${version}.tar.gz" bookshelfng.service bookshelfng.env bookshelfng.sysusers bookshelfng.tmpfiles)
elif [[ "$tag" =~ ^v([0-9]+\.[0-9]+\.[0-9]+)$ ]]; then
  version="${BASH_REMATCH[1]}"
  files=(bookshelfng.spec "ChaptarrNG-${version}-linux-x64.tar.gz" bookshelfng.service bookshelfng.env bookshelfng.sysusers bookshelfng.tmpfiles chaptarrng.package_info)
else
  exit 1
fi
if [[ "${COPR_FIXTURE_MISSING_PACKAGE_INFO:-false}" == true ]]; then
  files=("${files[@]/chaptarrng.package_info}")
fi
for file in "${files[@]}"; do
  [[ -n "$file" ]] && printf 'fixture source file\n' > "$file"
done
SH
chmod +x "$work/bin/curl" "$work/bin/rpm2cpio" "$work/bin/cpio"

run_valid_case() {
  local tag="$1"
  local output="$2"
  mkdir -p "$output"
  PATH="$work/bin:$PATH" \
    COPR_FIXTURE_TAG="$tag" \
    COPR_RESULTDIR="$output" \
    bash "$repo_root/packaging/rpm/copr-source.sh" "$tag" > "$output/result.log"
}

run_valid_case main-v1.2.3.4 "$work/legacy"
test -s "$work/legacy/bookshelfng-1.2.3.4.tar.gz"
run_valid_case v1.2.3 "$work/chaptarr"
test -s "$work/chaptarr/ChaptarrNG-1.2.3-linux-x64.tar.gz"
test -s "$work/chaptarr/chaptarrng.package_info"

if PATH="$work/bin:$PATH" bash "$repo_root/packaging/rpm/copr-source.sh" v1.2; then
  echo 'The COPR source script accepted a malformed release tag.' >&2
  exit 1
fi

if PATH="$work/bin:$PATH" COPR_FIXTURE_TAG=v1.2.4 COPR_FIXTURE_BAD_CHECKSUM=true COPR_RESULTDIR="$work/bad-checksum" \
  bash "$repo_root/packaging/rpm/copr-source.sh" v1.2.4 > /dev/null 2>&1; then
  echo 'The COPR source script accepted a source RPM with an invalid checksum.' >&2
  exit 1
fi

if PATH="$work/bin:$PATH" COPR_FIXTURE_TAG=v1.2.5 COPR_FIXTURE_MISSING_PACKAGE_INFO=true COPR_RESULTDIR="$work/missing-info" \
  bash "$repo_root/packaging/rpm/copr-source.sh" v1.2.5 > /dev/null 2>&1; then
  echo 'The COPR source script accepted a ChaptarrNG RPM missing package metadata.' >&2
  exit 1
fi

echo 'COPR source bridge tests passed.'
