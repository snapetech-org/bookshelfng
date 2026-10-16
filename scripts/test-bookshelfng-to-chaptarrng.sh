#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
workdir="$(mktemp -d)"
trap 'rm -rf -- "$workdir"' EXIT

data_dir="$workdir/source config"
backup_dir="$workdir/backup location"
fakebin="$workdir/bin"
mkdir -p "$data_dir" "$backup_dir" "$fakebin"
printf 'fixture database\n' > "$data_dir/readarr.db"
printf '<Config><Port>8787</Port></Config>\n' > "$data_dir/config.xml"
mkdir -p "$data_dir/logs"
printf 'fixture log\n' > "$data_dir/logs/Readarr.debug.txt"

cat > "$fakebin/docker" <<'DOCKER'
#!/usr/bin/env bash
printf '%s\n' "$@" > "$DOCKER_ARGS_FILE"
DOCKER
chmod +x "$fakebin/docker"
export DOCKER_ARGS_FILE="$workdir/docker-args.txt"
export PATH="$fakebin:$PATH"

tool="$repo_root/scripts/bookshelfng-to-chaptarrng.sh"
image='ghcr.io/snapetech-org/chaptarrng:v0.9.973'

"$tool" preview --data-dir "$data_dir" --backup-dir "$backup_dir" --image "$image"
grep -Fxq -- '-preview-bookshelf-migration' "$DOCKER_ARGS_FILE"
grep -Fxq -- '-v' "$DOCKER_ARGS_FILE"
grep -Fxq -- "$data_dir:/config" "$DOCKER_ARGS_FILE"
grep -Fxq -- "$image" "$DOCKER_ARGS_FILE"

archive="$(find "$backup_dir" -maxdepth 1 -type f -name 'bookshelfng-preview-*.tar.gz' -print -quit)"
[[ -n "$archive" ]]
[[ "$(stat -c '%a' "$archive")" == 600 ]]
tar -tzf "$archive" | grep -Fxq 'source config/readarr.db'
tar -tzf "$archive" | grep -Fxq 'source config/config.xml'
tar -tzf "$archive" | grep -Fxq 'source config/logs/Readarr.debug.txt'

before_count="$(find "$backup_dir" -maxdepth 1 -type f -name '*.tar.gz' | wc -l)"
if "$tool" apply --data-dir "$data_dir" --backup-dir "$backup_dir" --image latest 2>/dev/null; then
  echo 'mutable image tag should have been rejected' >&2
  exit 1
fi
if "$tool" apply --data-dir "$data_dir" --backup-dir "$backup_dir" --image "$image" 2>/dev/null; then
  echo 'apply without explicit stopped-service confirmation should have been rejected' >&2
  exit 1
fi
after_count="$(find "$backup_dir" -maxdepth 1 -type f -name '*.tar.gz' | wc -l)"
[[ "$before_count" == "$after_count" ]]

"$tool" apply --data-dir "$data_dir" --backup-dir "$backup_dir" --image "$image" --confirm-stopped
grep -Fxq -- '-migrate-bookshelf' "$DOCKER_ARGS_FILE"
grep -Fxq -- '-confirm-bookshelf-service-stopped' "$DOCKER_ARGS_FILE"

printf 'rollback fixture\n' > "$data_dir/readarr.db.bookshelfng-backup-test.db"
"$tool" rollback-preview --data-dir "$data_dir" --backup-dir "$backup_dir" --image "$image" \
  --bookshelf-backup 'readarr.db.bookshelfng-backup-test.db'
grep -Fxq -- '-preview-bookshelf-restore' "$DOCKER_ARGS_FILE"
grep -Fxq -- '-bookshelf-backup=/config/readarr.db.bookshelfng-backup-test.db' "$DOCKER_ARGS_FILE"

if "$tool" rollback-preview --data-dir "$data_dir" --backup-dir "$backup_dir" --image "$image" \
  --bookshelf-backup '../readarr.db' 2>/dev/null; then
  echo 'rollback path traversal should have been rejected' >&2
  exit 1
fi

"$tool" rollback --data-dir "$data_dir" --backup-dir "$backup_dir" --image "$image" \
  --bookshelf-backup 'readarr.db.bookshelfng-backup-test.db' --confirm-stopped
grep -Fxq -- '-restore-bookshelf' "$DOCKER_ARGS_FILE"
grep -Fxq -- '-confirm-bookshelf-service-stopped' "$DOCKER_ARGS_FILE"

echo 'BookshelfNG to ChaptarrNG handoff helper checks passed.'
