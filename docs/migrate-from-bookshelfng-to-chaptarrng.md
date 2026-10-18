# Move a BookshelfNG installation to ChaptarrNG

BookshelfNG `0.4.21.71` is the final published source release. It includes a
source-side handoff helper that archives BookshelfNG appdata and invokes the
standard ChaptarrNG migration commands. ChaptarrNG `v0.9.977` is the latest
public release used in the examples below. Keep its image tag versioned or use
an immutable digest. ChaptarrNG releases are frozen until the full retirement
acceptance gates close. PR #128 merged release and distribution workflows that
fail closed unless `CHAPTARRNG_RELEASE_READY=true`; the repository variable is
unset. ChaptarrNG `.978` is a source version bump, not a release.

BookshelfNG releases are frozen too. PR #148 merged its fail-closed publishing gate to `main` as `c6b4642`; its tagged image/release workflows, manual distribution retries, and legacy bridge require `BOOKSHELFNG_RELEASE_READY=true`, which remains unset. Neither application's release gate enables the other's publishing paths.

The published converter accepts the exact BookshelfNG migration-158 SQLite schema and rejects versions before migration 14; upgrade older installs to BookshelfNG `.71` first. PR #126 merged a version-aware guard and migration-1 rollback fixture into ChaptarrNG `main`, but it is not in `.977`. Run [39132760214](https://github.com/snapetech-org/chaptarrng/actions/runs/39132760214) on `9c051d3d` reported NUnit source line 162 in `should_preview_convert_and_restore_a_current_bookshelf_postgres_schema`. The fixture seeds `BookImportMinimumMatchPercent` with that exact casing but the check queried lowercase, identifying a fixture expectation error. ChaptarrNG commit [b5bd9527](https://github.com/snapetech-org/chaptarrng/commit/b5bd9527) corrects the three retained-config checks. Exact-head run [39133225495](https://github.com/snapetech-org/chaptarrng/actions/runs/39133225495) passed all 3 synthetic PostgreSQL migration cases and Linux, macOS, and Windows platform validation. The candidate remains unsupported for operator data.

ChaptarrNG PR #127 merged to `main` as `b3089a39`, adding supplemental
catalogs, per-field metadata preferences, and exact ISBN, ASIN, provider-ID, or
title/author recovery of unmapped files. Linux, macOS, Windows, PostgreSQL
migration, CodeQL, dependency/security, and release-note checks passed on its
exact head. Its source changes are not in the public `.977` image; provider and
settings migration still need acceptance against converted operator data. The
four provider-dispatch CodeQL findings on an earlier head were reviewed as
false positives and dismissed with a rationale.

ChaptarrNG PR #129 merged to `main` as `949ae3dd` with the opt-in M4B settings,
track order and chapter titles, original-track fallback, and move/copy source
handling. Its clean head passed the full hosted Linux, macOS, and Windows
suites, PostgreSQL migration validation, CodeQL, dependency/security, and
release-note checks. A synthetic two-track smoke against the `.977` image's
m4b-tool produced AAC at 44.1 kHz stereo and preserved the supplied chapter
titles and offsets. This checks the external converter and sidecar format, not
the new importer end to end. Focused importer tests cover merge selection,
chapter/tag behavior, and fallback with a mocked converter. Representative
files and the full converter-to-import flow remain open, and the source change
is not in public `.977`.

ChaptarrNG PR #130 merged to `main` as `9f1ae60b`. When no explicit
`BookMatchingStrictness` is set, ChaptarrNG maps BookshelfNG's numeric
`BookImportMinimumMatchPercent` to the closest mode: 50–66 to Aggressive,
67–82 to Balanced, and 83–99 to Strict. An explicit Chaptarr mode takes
precedence, but invalid legacy values still fail closed. The source `Config`
row is retained and the migration report identifies the mapping as a lossy
approximation. The algorithms have different semantics, so matching behavior
on converted libraries still needs acceptance. This change is not in public
`.977`.

Update an earlier BookshelfNG release to `0.4.21.71` and let it finish its
database migration before replacing the application. This brings the source
to migration 158, which ChaptarrNG `.977` accepts. For a database before
migration 14 that cannot be upgraded through BookshelfNG, do not switch to
ChaptarrNG `.977` while the release freeze is active. Stop BookshelfNG when it
is idle, then run preview before switching. PostgreSQL BookshelfNG databases
are not accepted by a published ChaptarrNG converter. Do not use the
unreleased PostgreSQL candidate with operator data; retain the source database
while exact-head CI and populated-data acceptance remain open.

The helper archives appdata, including `plugins/Bookshelf.Diagnostics.dll`,
but it does not capture environment variables. If the optional diagnostics
module was installed and enabled, preserve its endpoint, token, and enable
variables in the ChaptarrNG deployment. ChaptarrNG retains that explicit
choice only when the old plugin marker is present; see its
[optional diagnostics guide](https://github.com/snapetech-org/chaptarrng/blob/main/docs/OPTIONAL_DIAGNOSTICS.md).

The appdata archive does not include the BookshelfNG M4B merge environment
variables either. The public ChaptarrNG `v0.9.977` image does not honor
`BOOKSHELF_M4B_MERGE`, `BOOKSHELF_M4B_AAC_BITRATE_KBPS`, or
`BOOKSHELF_FFMPEG_PATH`. PR #129 merged the source compatibility implementation
to ChaptarrNG `main`, but it is not in a published build. Keep the merge opt-in
unset after switching until the ChaptarrNG
[migration guide](https://github.com/snapetech-org/chaptarrng/blob/main/docs/MIGRATE_FROM_BOOKSHELFNG.md)
documents a release containing it and the remaining acceptance gates close.

Native Hardcover databases need the same provider mode during preview and apply. BookshelfNG commonly stores Hardcover work, author, edition, and series IDs as bare numbers. The ChaptarrNG candidate interprets them as Hardcover when `HARDCOVER=true` and `HARDCOVER_NATIVE` is not `false`; otherwise numeric IDs keep Goodreads identity. The helper candidate exposes `--provider-mode native-hardcover|goodreads`. These changes are not in the published `.71` helper or ChaptarrNG `.977` image. Exact-head validation on commit b5bd9527 passed all 3 synthetic PostgreSQL migration cases and Linux, macOS, and Windows platform validation; converted-data acceptance remains open. Do not use those published builds for native Hardcover migration until the release-freeze gates close.

## What the helper does

`scripts/bookshelfng-to-chaptarrng.sh` is a Bash wrapper for Linux or macOS
with Docker and `tar` available. It:

1. Checks for a regular `readarr.db` or `audioarr.db` in the appdata directory.
   It refuses two non-empty source databases because it cannot merge them.
2. Creates a mode-`0600` compressed archive of the full appdata directory in a
   backup directory you choose outside appdata.
3. Runs the requested preview, apply, rollback-preview, or rollback command in
   the versioned standard ChaptarrNG image.

The helper does not classify ambiguous books. ChaptarrNG keeps records with
unknown formats in both catalogs, unmonitored, and writes a private review
file; operators can supply a media map before conversion or review and classify
the records after startup. The helper does not copy media or download folders
mounted outside appdata, capture environment
variables or Compose/Unraid settings, or redirect a package, updater, pinned
image, or previously downloaded installer. Preserve existing media and
download mount paths when possible; copy those volumes separately if you are
moving them to another host. The appdata archive can contain API keys, provider
credentials, and library metadata, so keep it in private storage and do not
upload or share it.

## Prepare and snapshot

Install the last BookshelfNG release and choose a backup directory on separate
storage with enough room for the appdata archive. Stop BookshelfNG and every
other process using its data directory before taking the snapshot.

Download the helper from the final release:

```sh
curl --fail --location --output bookshelfng-to-chaptarrng.sh \
  https://raw.githubusercontent.com/snapetech-org/bookshelfng/main-v0.4.21.71/scripts/bookshelfng-to-chaptarrng.sh
chmod +x bookshelfng-to-chaptarrng.sh
```

Create an independent archive first:

```sh
./bookshelfng-to-chaptarrng.sh snapshot \
  --data-dir /path/to/bookshelfng-config \
  --backup-dir /path/to/separate-backup-volume
```

Keep a copy of the install settings too. Record the container image/tag,
container and host ports, `/config`, media and download mounts, PUID/PGID,
timezone, URL base, reverse-proxy settings, and any values supplied outside
`config.xml` or the database.

## Preview and review media choices

Preview with the same standard ChaptarrNG release you plan to run after
migration:

```sh
./bookshelfng-to-chaptarrng.sh preview \
  --data-dir /path/to/bookshelfng-config \
  --backup-dir /path/to/separate-backup-volume \
  --image ghcr.io/snapetech-org/chaptarrng:v0.9.977
```

The script creates another full appdata archive before invoking ChaptarrNG.
Preview stages the conversion and checks every source table and row without
promoting the target database. If BookshelfNG records do not identify a single
target format, preview writes `readarr.db.bookshelf-media-review.json` beside
the database and keeps those books in both ChaptarrNG catalogs without
monitoring. This lets conversion continue without guessing which format to
search. The file contains book titles and author names; keep it private.

The helper downloaded from the published `.71` tag does not expose provider
mode and runs the converter in Goodreads mode. Native Hardcover conversion is
not supported by that helper or the public `.977` image. The current source
candidate adds `--provider-mode native-hardcover` to preview and apply; use it
only after the ChaptarrNG importer and helper candidate have passed hosted and
converted-data acceptance and are distributed in a supported build. Use the
same mode for preview and apply, then configure the replacement container with
native Hardcover enabled.

To choose formats before conversion, save a complete, source-matched
`readarr.db.bookshelf-media-map.json`. Set each `mediaType` to `audiobook`,
`ebook`, `both`, or `both-unmonitored`. A work with one selected audiobook and
one selected ebook edition is preserved in both formats. Multiple selected
editions of the same format stop conversion before promotion. Without a map,
review and classify the unresolved records in ChaptarrNG after startup.

If the database changes after review, preview rejects missing or stale map
entries. Update the map using the new review file and run preview again. Do
not guess from a filename or apply a technical test map as a real library
classification.

## Apply the conversion

After preview passes, keep the source service stopped and run:

```sh
./bookshelfng-to-chaptarrng.sh apply \
  --data-dir /path/to/bookshelfng-config \
  --backup-dir /path/to/separate-backup-volume \
  --image ghcr.io/snapetech-org/chaptarrng:v0.9.977 \
  --confirm-stopped
```

The explicit flag is required because apply replaces the active database only
after ChaptarrNG has staged and validated its native database. ChaptarrNG also
retains a SQLite source backup next to the database. Keep both that backup and
the independent appdata archive until the migrated installation has been
checked. Do not run BookshelfNG and ChaptarrNG against the same data directory
at the same time.

Update the container or service to the standard ChaptarrNG image, preserving
the old appdata, media, download, and port mappings. ChaptarrNG's fresh-install
default port is `8789`; migrated `config.xml` retains the old application port,
so preserve the matching host/container mapping. The normal ChaptarrNG startup
path also detects a supported BookshelfNG database. Preview first to inspect
the conversion report and generated media-review file.

After startup, verify the health check and existing UI address. Inspect the
library, roots, profiles, indexers, download clients, notifications, API
settings, reverse proxy, SeerrNG connection, and recent logs. Conversion
coverage does not prove every provider credential or external integration has
the same behavior.

## Roll back

Stop every process using the data directory. Use the retained ChaptarrNG
source backup filename shown in the logs:

```sh
./bookshelfng-to-chaptarrng.sh rollback-preview \
  --data-dir /path/to/bookshelfng-config \
  --backup-dir /path/to/separate-backup-volume \
  --image ghcr.io/snapetech-org/chaptarrng:v0.9.977 \
  --bookshelf-backup readarr.db.bookshelfng-backup-<timestamp>-<id>.db
```

After rollback-preview passes, restore the BookshelfNG database:

```sh
./bookshelfng-to-chaptarrng.sh rollback \
  --data-dir /path/to/bookshelfng-config \
  --backup-dir /path/to/separate-backup-volume \
  --image ghcr.io/snapetech-org/chaptarrng:v0.9.977 \
  --bookshelf-backup readarr.db.bookshelfng-backup-<timestamp>-<id>.db \
  --confirm-stopped
```

Before rollback, preview the exact backup you intend to restore. Rollback
preserves the current ChaptarrNG database, including changes since conversion,
as a separate backup. Start only BookshelfNG after a successful restore.

## Published image handoff smoke test (2026-10-18)

An isolated Linux/amd64 Docker rehearsal started the published BookshelfNG `.71`
image with `/config`, `/data`, and `/download` mounts and generated an empty
migration-158 database. After stopping it, ChaptarrNG `.977` used the same mounts
and automatically converted the database to migration 120 while retaining the
original source backup. Both databases passed SQLite integrity checks. Rollback
preview and apply restored migration 158, and the BookshelfNG image started
again on port 8787. A post-conversion setting remained in the retained ChaptarrNG
backup. This is an empty-database image-switch rehearsal, not an Unraid Community
Apps update test or evidence from populated operator data.

## Install-channel notes and support limits

The helper handles appdata; it does not change how an installation receives
updates. Mutable registry aliases, pinned image digests, native packages,
Windows installers, Helm, and offline archives each have different update
steps. The candidate release bridge is gated and disabled by default, so do
not assume an existing BookshelfNG package or image will redirect itself.
Keep the old installer or image reference available until the migration has
been verified and rollback is no longer needed.

The published `.977` converter accepts the exact BookshelfNG migration-158
SQLite schema and bundles the SQLite upgrade chain. Its table guard rejects
versions before migration 14. PR #126 merged a version-aware fix and synthetic
migration-1 rollback fixture into ChaptarrNG `main`; hosted Linux, macOS,
Windows, and PostgreSQL migration checks passed, but the source fix is not in
`.977`. Releases are frozen until all retirement acceptance gates close.
Populated synthetic migration-22 evidence covers conversion and rollback,
source-unchanged preview, and refusal of a future schema. This does not
establish older-schema behavior on real data or PostgreSQL source conversion.
Run [39132760214](https://github.com/snapetech-org/chaptarrng/actions/runs/39132760214) on `9c051d3d` reported NUnit source line 162 in `should_preview_convert_and_restore_a_current_bookshelf_postgres_schema`. The fixture seeds `BookImportMinimumMatchPercent` with that exact casing but the check queried lowercase, identifying a fixture expectation error. ChaptarrNG commit [b5bd9527](https://github.com/snapetech-org/chaptarrng/commit/b5bd9527) corrects the three retained-config checks. Exact-head run [39133225495](https://github.com/snapetech-org/chaptarrng/actions/runs/39133225495) passed all 3 synthetic PostgreSQL migration cases and Linux, macOS, and Windows platform validation. The candidate remains unsupported for operator data.
Ambiguous formats are retained in both catalogs without monitoring until the
operator classifies them; the converter does not infer their true type. Full
provider and environment parity, every installation channel, and rollback on
every real-world deployment have not been established. Unsupported database
lineages fail closed; do not bypass the check by renaming or editing the
database. See the [consolidation report](maintainers/chaptarr-consolidation.md)
for evidence and the remaining feature and channel inventory.

BookshelfNG's `BookImportMinimumMatchPercent` defaults to 70 and accepts values
from 50 through 99. It affects both fuzzy title parsing and import acceptance.
ChaptarrNG `main` maps 50–66 to Aggressive, 67–82 to Balanced, and 83–99 to
Strict when there is no explicit `BookMatchingStrictness`; an explicit mode
takes precedence. Invalid legacy values fail closed. The source `Config` row
is retained, and the migration report labels the mode translation as a lossy
approximation. These modes do not reproduce the legacy fuzzy-search algorithm,
so validate matching behavior on converted operator data before relying on
automatic matches. The source change is not in public `.977`.
