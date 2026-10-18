# Move a BookshelfNG installation to ChaptarrNG

BookshelfNG `0.4.21.71` is the final published source release. It includes a
source-side handoff helper that archives BookshelfNG appdata and invokes the
standard ChaptarrNG migration commands. ChaptarrNG `v0.9.976` is the matching
published release used in the examples
below. Keep its image tag versioned or use an immutable digest.

This process does not make every old installation automatically transferable.
The converter supports the exact BookshelfNG migration-158 SQLite schema.
Older schemas, PostgreSQL, two populated Bookshelf databases, and several
external settings and installation-channel upgrades are not covered. The
release bridge remains disabled by default. Read the limits below before
changing a running installation.

If you are on an earlier BookshelfNG release, update to `0.4.21.71` first
and let it complete its database migration before replacing the application.
Stop BookshelfNG when it is idle, then run the ChaptarrNG preview against the
resulting migration-158 SQLite database. ChaptarrNG does not run BookshelfNG's
older database migrations. PostgreSQL BookshelfNG databases require a separate
manual migration path and are not accepted by the current converter.

The helper archives appdata, including `plugins/Bookshelf.Diagnostics.dll`,
but it does not capture environment variables. If the optional diagnostics
module was installed and enabled, preserve its endpoint, token, and enable
variables in the ChaptarrNG deployment. ChaptarrNG retains that explicit
choice only when the old plugin marker is present; see its
[optional diagnostics guide](https://github.com/snapetech-org/chaptarrng/blob/main/docs/OPTIONAL_DIAGNOSTICS.md).

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
  --image ghcr.io/snapetech-org/chaptarrng:v0.9.976
```

The script creates another full appdata archive before invoking ChaptarrNG.
Preview stages the conversion and checks every source table and row without
promoting the target database. If BookshelfNG records do not identify a single
target format, preview writes `readarr.db.bookshelf-media-review.json` beside
the database and keeps those books in both ChaptarrNG catalogs without
monitoring. This lets conversion continue without guessing which format to
search. The file contains book titles and author names; keep it private.

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
  --image ghcr.io/snapetech-org/chaptarrng:v0.9.976 \
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
  --image ghcr.io/snapetech-org/chaptarrng:v0.9.976 \
  --bookshelf-backup readarr.db.bookshelfng-backup-<timestamp>-<id>.db
```

After rollback-preview passes, restore the BookshelfNG database:

```sh
./bookshelfng-to-chaptarrng.sh rollback \
  --data-dir /path/to/bookshelfng-config \
  --backup-dir /path/to/separate-backup-volume \
  --image ghcr.io/snapetech-org/chaptarrng:v0.9.976 \
  --bookshelf-backup readarr.db.bookshelfng-backup-<timestamp>-<id>.db \
  --confirm-stopped
```

Before rollback, preview the exact backup you intend to restore. Rollback
preserves the current ChaptarrNG database, including changes since conversion,
as a separate backup. Start only BookshelfNG after a successful restore.

## Install-channel notes and support limits

The helper handles appdata; it does not change how an installation receives
updates. Mutable registry aliases, pinned image digests, native packages,
Windows installers, Helm, and offline archives each have different update
steps. The candidate release bridge is gated and disabled by default, so do
not assume an existing BookshelfNG package or image will redirect itself.
Keep the old installer or image reference available until the migration has
been verified and rollback is no longer needed.

The verified converter input is the exact BookshelfNG migration-158 SQLite
schema. Ambiguous formats are retained in both catalogs without monitoring
until the operator classifies them; the converter does not infer their true
type. Older BookshelfNG schemas, PostgreSQL conversion, full provider and
environment parity, every installation channel, and rollback on every
real-world deployment have not been established. Unsupported database
lineages fail closed; do not bypass the check by renaming or editing the
database. See the [consolidation report](maintainers/chaptarr-consolidation.md)
for evidence and the remaining feature and channel inventory.
