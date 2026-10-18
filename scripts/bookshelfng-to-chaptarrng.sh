#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
  cat <<'USAGE'
Usage:
  bookshelfng-to-chaptarrng.sh snapshot --data-dir PATH --backup-dir PATH
  bookshelfng-to-chaptarrng.sh preview  --data-dir PATH --backup-dir PATH --image IMAGE [--provider-mode goodreads|native-hardcover]
  bookshelfng-to-chaptarrng.sh apply   --data-dir PATH --backup-dir PATH --image IMAGE --confirm-stopped [--provider-mode goodreads|native-hardcover]
  bookshelfng-to-chaptarrng.sh rollback-preview --data-dir PATH --backup-dir PATH --image IMAGE --bookshelf-backup FILE
  bookshelfng-to-chaptarrng.sh rollback --data-dir PATH --backup-dir PATH --image IMAGE --bookshelf-backup FILE --confirm-stopped

IMAGE must be a versioned ghcr.io/snapetech-org/chaptarrng:vMAJOR.MINOR.PATCH
tag or an immutable sha256 digest. Every action first archives the complete
BookshelfNG appdata directory outside that directory. The provider mode is
passed only to the temporary ChaptarrNG migration container; configure the
same mode in the permanent replacement container after migration.
USAGE
}

fail() {
  printf 'Error: %s\n' "$*" >&2
  exit 2
}

action="${1:-}"
[[ -n "$action" ]] || { usage >&2; exit 2; }
shift

case "$action" in
  snapshot|preview|apply|rollback-preview|rollback) ;;
  -h|--help|help) usage; exit 0 ;;
  *) usage >&2; fail "unknown action: $action" ;;
esac

data_dir=""
backup_dir=""
image=""
bookshelf_backup=""
confirm_stopped=false
provider_mode="goodreads"
provider_mode_set=false

while (($#)); do
  case "$1" in
    --data-dir)
      (($# >= 2)) || fail '--data-dir needs a path'
      data_dir="$2"
      shift 2
      ;;
    --backup-dir)
      (($# >= 2)) || fail '--backup-dir needs a path'
      backup_dir="$2"
      shift 2
      ;;
    --image)
      (($# >= 2)) || fail '--image needs an image reference'
      image="$2"
      shift 2
      ;;
    --bookshelf-backup)
      (($# >= 2)) || fail '--bookshelf-backup needs a file name'
      bookshelf_backup="$2"
      shift 2
      ;;
    --provider-mode)
      (($# >= 2)) || fail '--provider-mode needs goodreads or native-hardcover'
      provider_mode="$2"
      provider_mode_set=true
      shift 2
      ;;
    --confirm-stopped)
      confirm_stopped=true
      shift
      ;;
    -h|--help|help)
      usage
      exit 0
      ;;
    *) fail "unknown option: $1" ;;
  esac
done

[[ -n "$data_dir" ]] || fail '--data-dir is required'
[[ "$data_dir" == /* ]] || fail '--data-dir must be an absolute path'
[[ -d "$data_dir" ]] || fail "data directory does not exist: $data_dir"
data_dir="$(cd -- "$data_dir" && pwd -P)"
[[ "$data_dir" != / ]] || fail 'refusing to archive the filesystem root'

if [[ -s "$data_dir/readarr.db" && -s "$data_dir/audioarr.db" ]]; then
  fail 'both BookshelfNG databases contain data; this tool will not merge two libraries'
fi

readarr_populated=false
audioarr_populated=false
if [[ -f "$data_dir/readarr.db" && ! -L "$data_dir/readarr.db" && -s "$data_dir/readarr.db" ]]; then
  readarr_populated=true
fi
if [[ -f "$data_dir/audioarr.db" && ! -L "$data_dir/audioarr.db" && -s "$data_dir/audioarr.db" ]]; then
  audioarr_populated=true
fi

if [[ "$readarr_populated" == true ]]; then
  source_database="$data_dir/readarr.db"
elif [[ "$audioarr_populated" == true ]]; then
  source_database="$data_dir/audioarr.db"
else
  fail 'data directory must contain a non-empty regular readarr.db or audioarr.db file'
fi

[[ -n "$backup_dir" ]] || fail '--backup-dir is required so you can choose a separate backup location'
mkdir -p -- "$backup_dir"
backup_dir="$(cd -- "$backup_dir" && pwd -P)"
case "$backup_dir/" in
  "$data_dir/"*) fail '--backup-dir must be outside the BookshelfNG data directory' ;;
esac

case "$action" in
  snapshot) ;;
  preview|apply|rollback-preview|rollback)
    [[ -n "$image" ]] || fail '--image is required for migration commands'
    if [[ ! "$image" =~ ^ghcr\.io/snapetech-org/chaptarrng:v[0-9]+\.[0-9]+\.[0-9]+$ &&
          ! "$image" =~ ^ghcr\.io/snapetech-org/chaptarrng@sha256:[a-fA-F0-9]{64}$ ]]; then
      fail '--image must be a versioned ChaptarrNG release tag or an immutable sha256 digest'
    fi
    command -v docker >/dev/null 2>&1 || fail 'docker is required for migration commands'
    ;;
esac

case "$action" in
  apply|rollback)
    [[ "$confirm_stopped" == true ]] || fail "$action requires --confirm-stopped after stopping every process using this data directory"
    ;;
esac

case "$provider_mode" in
  goodreads|native-hardcover) ;;
  *) fail '--provider-mode must be goodreads or native-hardcover' ;;
esac

case "$action" in
  preview|apply) ;;
  *) [[ "$provider_mode_set" == false ]] || fail '--provider-mode applies only to preview and apply' ;;
esac

case "$action" in
  rollback-preview|rollback)
    [[ -n "$bookshelf_backup" ]] || fail '--bookshelf-backup is required for rollback commands'
    [[ "$bookshelf_backup" != */* && "$bookshelf_backup" != '.' && "$bookshelf_backup" != '..' ]] ||
      fail '--bookshelf-backup must be the name of a file directly inside --data-dir'
    [[ -f "$data_dir/$bookshelf_backup" && ! -L "$data_dir/$bookshelf_backup" ]] ||
      fail "BookshelfNG backup is not a regular file in the data directory: $bookshelf_backup"
    ;;
esac

command -v tar >/dev/null 2>&1 || fail 'tar is required to create the appdata archive'
data_parent="$(dirname -- "$data_dir")"
data_name="$(basename -- "$data_dir")"
timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
archive="$backup_dir/bookshelfng-${action}-${timestamp}-$$.tar.gz"
[[ ! -e "$archive" ]] || fail "backup archive already exists: $archive"

umask 077
if ! tar -czpf "$archive" -C "$data_parent" -- "$data_name"; then
  rm -f -- "$archive"
  fail 'could not create the appdata archive; no ChaptarrNG command was run'
fi
chmod 600 "$archive"
printf 'Appdata archive: %s\n' "$archive"
printf 'Database selected for the ChaptarrNG handoff: %s\n' "$(basename -- "$source_database")"

[[ "$action" != snapshot ]] || exit 0

container_args=(run --rm --pull=always)
if [[ "$action" == preview || "$action" == apply ]]; then
  if [[ "$provider_mode" == native-hardcover ]]; then
    container_args+=(-e HARDCOVER=true -e HARDCOVER_NATIVE=true)
    printf 'Provider mode for conversion: native Hardcover\n'
  else
    container_args+=(-e HARDCOVER=false -e HARDCOVER_NATIVE=false)
    printf 'Provider mode for conversion: Goodreads\n'
  fi
fi
container_args+=(-v "$data_dir:/config" "$image" dotnet /app/Chaptarr.dll)
case "$action" in
  preview)
    container_args+=(-preview-bookshelf-migration -data=/config)
    ;;
  apply)
    container_args+=(-migrate-bookshelf -confirm-bookshelf-service-stopped -data=/config)
    ;;
  rollback-preview)
    container_args+=(-preview-bookshelf-restore "-bookshelf-backup=/config/$bookshelf_backup" -data=/config)
    ;;
  rollback)
    container_args+=(-restore-bookshelf -confirm-bookshelf-service-stopped "-bookshelf-backup=/config/$bookshelf_backup" -data=/config)
    ;;
esac

exec docker "${container_args[@]}"
