#!/usr/bin/env bash
set -euo pipefail

bookshelf_repo="snapetech-org/bookshelfng"
chaptarr_repo="snapetech-org/chaptarrng"
tag="${1:-}"

if [[ -z "$tag" && -r hook_payload ]]; then
  tag="$(tr -d '\r\n' < hook_payload)"
fi

if [[ "$tag" =~ ^main-v([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)$ ]]; then
  version="${BASH_REMATCH[1]}"
  release_base="https://github.com/${bookshelf_repo}/releases/download"
  source_rpm="bookshelfng-${version}-1.src.rpm"
  expected_payload="bookshelfng-${version}.tar.gz"
  package_info=""
elif [[ "$tag" =~ ^v([0-9]+\.[0-9]+\.[0-9]+)$ ]]; then
  version="${BASH_REMATCH[1]}"
  release_base="https://github.com/${chaptarr_repo}/releases/download"
  source_rpm="bookshelfng-${version}-1.src.rpm"
  expected_payload="ChaptarrNG-${version}-linux-x64.tar.gz"
  package_info="chaptarrng.package_info"
else
  echo 'COPR webhook payload must be a BookshelfNG main-vMAJOR.MINOR.PATCH.BUILD tag or a ChaptarrNG vMAJOR.MINOR.PATCH tag.' >&2
  exit 2
fi

resultdir="${COPR_RESULTDIR:-.}"
workdir="$(mktemp -d)"
trap 'rm -rf -- "$workdir"' EXIT

curl --fail --location --silent --show-error --retry 3 --retry-all-errors \
  --output "${workdir}/${source_rpm}" \
  "${release_base}/${tag}/${source_rpm}"
curl --fail --location --silent --show-error --retry 3 --retry-all-errors \
  --output "${workdir}/${source_rpm}.sha256" \
  "${release_base}/${tag}/${source_rpm}.sha256"

(cd "$workdir" && sha256sum --check "${source_rpm}.sha256")

mkdir -p "$resultdir"
resultdir="$(cd "$resultdir" && pwd -P)"
(
  cd "$resultdir"
  rpm2cpio "${workdir}/${source_rpm}" | cpio -idm --no-absolute-filenames
)

required_files=(
  bookshelfng.spec
  "$expected_payload"
  bookshelfng.service
  bookshelfng.env
  bookshelfng.sysusers
  bookshelfng.tmpfiles
)
if [[ -n "$package_info" ]]; then
  required_files+=("$package_info")
fi

for required_file in "${required_files[@]}"; do
  if [[ ! -f "${resultdir}/${required_file}" ]]; then
    echo "The COPR source RPM is missing ${required_file}." >&2
    exit 1
  fi
done

echo "Prepared the verified BookshelfNG package payload for release ${tag}."
