# Move a BookshelfNG installation to ChaptarrNG

BookshelfNG `0.4.21.71` is tagged as the final source release; its GitHub
release is still being prepared, and `0.4.21.70` is the latest published
version. The `.70` release includes a source-side handoff helper that archives
BookshelfNG appdata and invokes the standard ChaptarrNG migration commands.
ChaptarrNG `v0.9.975` is the matching published release used in the examples
below. Keep its image tag versioned or use an immutable digest.

This process does not make every old installation automatically transferable.
The converter supports the exact BookshelfNG migration-158 SQLite schema.
Older schemas, PostgreSQL, two populated Bookshelf databases, and several
external settings and installation-channel upgrades are not covered. The
release bridge remains disabled by default. Read the limits below before
changing a running installation.

## What the helper does

`scripts/bookshelfng-to-chaptarrng.sh` is a Bash wrapper for Linux or macOS
with Docker and `tar` available. It:

1. Checks for a regular `readarr.db` or `audioarr.db` in the appdata directory.
   It refuses two non-empty source databases because it cannot merge them.
2. Creates a mode-`0600` compressed archive of the full appdata directory in a
   backup directory you choose outside appdata.
3. Runs the requested preview, apply, rollback-preview, or rollback command in
   the versioned standard ChaptarrNG image.

The helper never chooses media types for ambiguous books. It does not copy
media or download folders mounted outside appdata, capture environment
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
  https://raw.githubusercontent.com/snapetech-org/bookshelfng/main-v0.4.21.70/scripts/bookshelfng-to-chaptarrng.sh
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

## Preview and resolve media choices

Preview with the same standard ChaptarrNG release you plan to run after
migration:

```sh
./bookshelfng-to-chaptarrng.sh preview \
  --data-dir /path/to/bookshelfng-config \
  --backup-dir /path/to/separate-backup-volume \
  --image ghcr.io/snapetech-org/chaptarrng:v0.9.975
```

The script creates another full appdata archive before invoking ChaptarrNG.
Preview stages the conversion and checks every source table and row without
promoting the target database. If BookshelfNG records do not identify a single
target format, preview stops and writes
`readarr.db.bookshelf-media-review.json` beside the database. Review every
listed book and create `readarr.db.bookshelf-media-map.json` with a
`mediaType` of `audiobook`, `ebook`, or `both` for each required book. The
review can include book titles and author names; keep it private.

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
  --image ghcr.io/snapetech-org/chaptarrng:v0.9.975 \
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
path also detects a supported BookshelfNG database, but use preview and the
explicit apply command first so you can review ambiguous books.

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
  --image ghcr.io/snapetech-org/chaptarrng:v0.9.975 \
  --bookshelf-backup readarr.db.bookshelfng-backup-<timestamp>-<id>.db
```

After rollback-preview passes, restore the BookshelfNG database:

```sh
./bookshelfng-to-chaptarrng.sh rollback \
  --data-dir /path/to/bookshelfng-config \
  --backup-dir /path/to/separate-backup-volume \
  --image ghcr.io/snapetech-org/chaptarrng:v0.9.975 \
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
schema. It requires operator media mappings where the source database is
ambiguous. Older BookshelfNG schemas, PostgreSQL conversion, full provider and
environment parity, every installation channel, and rollback on every
real-world deployment have not been established. Unsupported database
lineages fail closed; do not bypass the check by renaming or editing the
database. See the [consolidation report](maintainers/chaptarr-consolidation.md)
for evidence and the remaining feature and channel inventory.
