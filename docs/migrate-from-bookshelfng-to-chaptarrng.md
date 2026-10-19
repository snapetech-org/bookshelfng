# Move a BookshelfNG installation to ChaptarrNG

BookshelfNG `0.4.21.71` is the final published source release. It includes a
source-side handoff helper that archives BookshelfNG appdata and invokes the
standard ChaptarrNG migration commands. ChaptarrNG `v0.9.977` is the latest
public release used in the examples below. Keep its image tag versioned or use
an immutable digest. ChaptarrNG releases are frozen until the full retirement
acceptance gates close. PR #128 merged release and distribution workflows that
fail closed unless `CHAPTARRNG_RELEASE_READY=true`; the repository variable is
unset. ChaptarrNG `.978` is a source version bump, not a release.

**Migration decision: keep BookshelfNG in service; do not start a conversion.**
The published BookshelfNG `.71` source and ChaptarrNG `.977` converter support
preview of the exact SQLite migration-158 schema. Both retirement and
publishing gates remain open, so `.977` is not approved for migration and
unpublished `.978` source is not approved for production cutover. A schema
preview leaves the source database unchanged, though it may write a report;
it does not make an apply eligible. Wait for a supported destination build and
closed acceptance gates before stopping or replacing BookshelfNG.

**Provider identity warning:** the published `.977` importer maps bare numeric
IDs to Goodreads regardless of `HARDCOVER`. A native Hardcover database can
therefore pass structural checks while acquiring the wrong provider identity;
do not apply `.977` to native Hardcover data. The unpublished candidate
requires an explicit provider mode.

On 2026-10-19, candidate build `0.9.978.0` passed preview, apply, rollback
preview, and rollback on a disposable copy of populated migration-158 SQLite
data with `HARDCOVER=true` and networking disabled. Preview did not change the
source database. Apply passed integrity and foreign-key checks; rollback
preview left the converted database and source backup unchanged; explicit
rollback restored a byte-identical source backup and retained the converted
database separately. The private source snapshot remained unchanged. This
verifies one candidate SQLite round trip, not cutover readiness, ambiguous-media
classification, older schemas, PostgreSQL operator data, feature parity, or
installation-channel continuity.

BookshelfNG `main` at `9a04c2eb2` adds
`GET /api/v1/book/{id}/editions/catalog` and advertises `editionCatalog` for
SeerrNG. The unpublished ChaptarrNG PR #131 now implements the same route and
capability; this work remains source-only.

ChaptarrNG PR #132 merged format-specific root setup to source `main` as
`0f1fea44`, but that Quickstart change is not in the published `.977` release.

BookshelfNG releases are frozen too. PR #148 merged its fail-closed publishing gate to `main` as `c6b4642`; its tagged image/release workflows, manual distribution retries, and legacy bridge require `BOOKSHELFNG_RELEASE_READY=true`, which remains unset. Neither application's release gate enables the other's publishing paths.

For BookshelfNG `0.4.21.71` with a SQLite migration-158 database, use the
public ChaptarrNG `.977` converter for a read-only preview. If BookshelfNG
is older, finish upgrading it to `0.4.21.71` first. PostgreSQL source
databases and unpublished converter candidates are outside the published
path. A passing preview is not retirement acceptance or permission to
discard the source backup.

The published converter accepts the exact BookshelfNG migration-158 SQLite
schema and rejects versions before migration 14; upgrade older installs to
BookshelfNG .71 first. PR #126 merged a version-aware guard and migration-1
rollback fixture into ChaptarrNG `main`, but they are not in `.977`. Current migration candidate [PR #131](https://github.com/snapetech-org/chaptarrng/pull/131) remains draft. Earlier exact-head run [39175250100](https://github.com/snapetech-org/chaptarrng/actions/runs/39175250100) passed on PR head `e4db2d46` (CI merge candidate `724029a2`): Linux, macOS, and Windows suites; the 4/4 PostgreSQL fixture; release-note and runner-receipt validation; CodeQL; dependency review; secret scan; and NuGet submission. The final Linux artifact refused conversion without provider mode, preserved Goodreads and Hardcover identities with explicit modes, converted during normal startup, served the synthetic author and both format records, and restored the source byte-for-byte on rollback. A SeerrNG restricted-key smoke passed on an earlier head. These checks do not establish operator-data, feature-parity, or install-channel acceptance. The candidate adds older SQLite, one-schema PostgreSQL, native Hardcover, and BookOrbit support, but remains unsupported for operator data; see the [fixture evidence](https://github.com/snapetech-org/chaptarrng/blob/2f8c3b7f/docs/maintainers/BOOKSHELFNG_MIGRATION_FIXTURE_EVIDENCE.md).

A local AUR BookshelfNG-identity .977 package candidate passed an isolated,
network-disabled pacman upgrade from the published .71 package and downgrade
back, preserving an environment override and synthetic data canary. The
installed candidate also passed preview, conversion to ChaptarrNG migration
120, restore to BookshelfNG migration 158, and SQLite integrity/foreign-key
checks against a synthetic populated database.

A follow-up rehearsal booted systemd in an isolated Arch container. The public
`.71` package started against the fixture; pacman then upgraded the active
service to the local `.977` candidate. Its hooks stopped BookshelfNG and
restarted ChaptarrNG, whose normal startup converted the database to migration
120. Restore preview and apply returned it to migration 158 and retained the
converted database as a backup. Pacman downgrade restored `.71`, and the
BookshelfNG service started against the restored database. The environment
override and data canary survived; integrity and foreign-key checks passed.
`systemd-networkd-wait-online` was masked only inside the network-isolated test
container. Representative operator data and host-specific settings remain
open. The candidate is unpublished; check the
[package status](https://github.com/snapetech-org/chaptarrng/blob/main/packaging/README.md)
for channel acceptance.


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
titles and offsets. This checks the external converter and sidecar format.
ChaptarrNG draft PR #131 at commit `bdd7518f` adds a six-case tool-enabled
synthetic importer smoke that passed locally in an isolated Linux container
with `m4b-tool` 0.5.2, `mp4v2` 2.1.1, and FFmpeg/FFprobe 6.1.1. Successful
cases check tag ordering, chapter titles and offsets, metadata, registration,
and Move/Copy source handling. Failure cases verify fallback to separate
original-track imports in both modes when FFprobe cannot read a source and
when `m4b-tool` fails after a controlled FFmpeg conversion error. Representative
files, embedded chapters, and restart/resume remain open; the source change
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

Native Hardcover databases need the same provider mode during preview and apply. BookshelfNG commonly stores Hardcover work, author, edition, and series IDs as bare numbers. The ChaptarrNG candidate interprets them as Hardcover when `HARDCOVER=true` and `HARDCOVER_NATIVE` is not `false`; set `HARDCOVER=false` for a Goodreads-primary database. If the mode is unset or invalid, the current ChaptarrNG candidate fails closed when it encounters a bare numeric ID rather than silently assigning Goodreads identity. The helper candidate exposes `--provider-mode native-hardcover|goodreads`. BookshelfNG's `latest`, `main`, and `hardcover` Docker tags use native Hardcover mode; `softcover` uses Goodreads mode. ChaptarrNG is adding matching compatibility image targets for those mutable aliases, but the targets have not been published or enabled. These changes are not in the published `.71` helper or ChaptarrNG `.977` image. Exact-head validation on commit b5bd9527 passed all 4 synthetic PostgreSQL migration cases, including normal-startup conversion with backup retention; Linux, macOS, and Windows platform validation also passed; converted-data acceptance remains open. Do not use those published builds for native Hardcover migration until the release-freeze gates close.

## Populated SQLite rehearsal (2026-10-18)

The public ChaptarrNG `v0.9.977` Linux/amd64 image passed preview, explicit
apply, restore preview, and rollback against a private populated migration-158
SQLite snapshot. The live BookshelfNG service and database were not used as the
test target. Preview left the snapshot bytes unchanged and produced private
media-review artifacts; no media map was supplied, so ambiguous format
choices remain for operator review.

Apply reached Chaptarr migration v120 and retained a migration-158 source
backup matching the input snapshot's logical contents. Rollback restored the
source database with matching logical contents and retained the converted
database as a separate ChaptarrNG backup. The source, converted, and restored
databases passed SQLite integrity and foreign-key checks. No user data or
database files were committed. This is evidence for one populated SQLite
schema and image; older schemas, PostgreSQL, installer handoffs, and feature
parity remain open.

## Candidate populated SQLite rehearsal (2026-10-19)

An unpublished ChaptarrNG candidate build reporting `0.9.978.0` completed
preview, explicit apply, rollback preview, and explicit rollback on a
disposable copy of populated migration-158 SQLite data. The test used
`HARDCOVER=true`, disabled network access, and did not touch the original
BookshelfNG service or snapshot.

Migration preview left the source unchanged. Apply passed integrity and
foreign-key checks and retained the schema-158 source backup. Rollback preview
left both databases unchanged. Explicit rollback restored a byte-identical
copy of the retained source backup and preserved the converted database
separately. Private database contents, identifiers, counts, and hashes are
omitted.

This validates one candidate migration-158 SQLite round trip. It does not
classify ambiguous formats, validate older schemas or PostgreSQL operator
data, establish full feature parity, or authorize a production switch. Keep
the BookshelfNG service in place until every retirement gate closes.

## Provider-mode image-switch and rollback rehearsal (2026-10-18)

A second isolated rehearsal used a populated synthetic migration-158 database
served by the public BookshelfNG `.71` Hardcover image. It exposed a provider
mode handoff hazard: the prior ChaptarrNG candidate, started without the
source's `HARDCOVER=true`, mapped bare numeric IDs into Goodreads fields. The
same image switch with `HARDCOVER=true` preserved author `hc:9001`, book
`hc:9002`, and editions `hc:9003` and `hc:9004` in Hardcover fields; the
converted database passed SQLite integrity and foreign-key checks and served
the author and both format-specific books through the API.

Rollback preview left the converted database and source backup hashes
unchanged. Explicit rollback restored the BookshelfNG schema-158 database
byte-for-byte, retained the ChaptarrNG database as a separate backup, and the
released `.71` Hardcover image reopened the restored database and served the
source records. This is synthetic handoff and rollback evidence; it does not
establish operator-data or install-channel acceptance. The current ChaptarrNG
candidate fails closed if provider mode is missing or invalid, and its
compatibility image targets and alias bridge passed hosted regression scripts; local BuildKit target checks also passed. The actual GHCR images and alias dispatch were not built or published. This synthetic rehearsal does not establish operator-data or installer acceptance. No release or image aliases were published. See [ChaptarrNG PR #131](https://github.com/snapetech-org/chaptarrng/pull/131).

## What the helper does

`scripts/bookshelfng-to-chaptarrng.sh` is a Bash wrapper for Linux or macOS
with Docker and `tar` available. It:

1. The published `.71` helper requires a regular `readarr.db` or `audioarr.db`
   and refuses two non-empty source databases. Its printed selection can name
   a zero-byte `readarr.db` when a populated `audioarr.db` is beside it; the
   helper passes the whole appdata directory to ChaptarrNG, whose resolver
   ignores zero-byte legacy files and selects the populated database. The
   current BookshelfNG `main` helper selects the sole non-empty regular file
   before archiving, but that fix from PR #154 is not in the published `.71`
   tag. Do not treat an empty-only database file as a valid migration source.
2. Creates a mode-`0600` compressed archive of the full appdata directory in a
   backup directory you choose outside appdata.
3. Runs the requested preview, apply, rollback-preview, or rollback command in
   the versioned standard ChaptarrNG image.

Each BookshelfNG installation uses one active database. If these files belong
to two independently operated installations, migrate each installation from
its own appdata directory and keep the ChaptarrNG instances separate. If both
database files are non-empty in one appdata directory, the helper stops before
creating a migration archive or starting ChaptarrNG. Keep the original appdata
intact, identify which installation owns each database and its settings, and
make separate working copies before migrating them separately. This workflow
does not merge libraries or shared settings; if ownership cannot be established,
stop for manual reconciliation.

If the goal is one combined library, first use the
[two-instance consolidation runbook](../README.md#one-instance-for-ebooks-and-audiobooks)
to move tracked media into the BookshelfNG instance you are keeping and import
or rescan it there. That workflow does not merge database history, profiles,
monitoring, or settings. Keep both original appdata backups until the selected
BookshelfNG library is verified, then migrate its single database to
ChaptarrNG.

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

## BookLore and BookOrbit handoff

The converter preserves a BookshelfNG BookLore notification row, including its
provider identity, saved settings and credentials, and `OnReleaseImport`
trigger. It keeps the source row in the retained backup. It cannot infer that a
saved BookLore URL or account belongs to a BookOrbit server, so it does not
rewrite this connection.

The current ChaptarrNG retirement candidate adds a separate BookOrbit Book
Dock notification destination. Its API client has mock coverage for streaming,
redirect refusal, credential and file rejection, and partial batches. An
isolated BookOrbit v3.2.0 live contract run passed initial setup, login, Book
Dock access, EPUB upload and listing, and unsupported-file rejection. This
confirms upload admission, not BookOrbit's downstream processing of a
production book or a transition using real BookshelfNG users and settings. The
candidate is [PR #131](https://github.com/snapetech-org/chaptarrng/pull/131)
and is not included in public ChaptarrNG `v0.9.977`.

After a ChaptarrNG build containing BookOrbit is available, add and test a
separate BookOrbit connection in **Settings > Connect**. Keep the migrated
BookLore connection until imported files appear in BookOrbit as expected; then
disable or remove the old connection if it is no longer needed. For a partially
rejected batch, inspect Book Dock before retrying because successful earlier
uploads remain there.

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

## Apply after acceptance gates close

> **Do not run this apply step during the current release freeze.** Apply and
> normal ChaptarrNG startup against BookshelfNG appdata are not approved until
> migration, parity, rollback, and installation-channel acceptance close.

After the gates close and conversion is approved, keep the source service
stopped and run:

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

After approved conversion, update the container or service to the standard ChaptarrNG image, preserving
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

A local Fedora 44 RPM transaction upgraded the published BookshelfNG `.71`
package to a `.977` bridge candidate and downgraded back while preserving
config/data canaries. It used `rpm --nodeps` and a mocked `systemctl`; it did
not run a real service or migrate a database. The current legacy COPR repo has
no package entries for Fedora 43, 44, 45, or Rawhide x86_64, so live DNF/COPR
acceptance remains open. See the [distribution status](distribution.md).

The published `.977` converter accepts the exact BookshelfNG migration-158
SQLite schema and bundles the SQLite upgrade chain. Its table guard rejects
versions before migration 14. PR #126 merged a version-aware fix and synthetic
migration-1 rollback fixture into ChaptarrNG `main`; hosted Linux, macOS,
Windows, and PostgreSQL migration checks passed, but the source fix is not in
`.977`. Releases are frozen until all retirement acceptance gates close.
Populated synthetic migration-22 evidence covers conversion and rollback,
source-unchanged preview, and refusal of a future schema. This does not
establish older-schema behavior on real data or PostgreSQL source conversion.
Earlier synthetic PostgreSQL snapshot [`43bc6363`](https://github.com/snapetech-org/chaptarrng/commit/43bc6363) passed four migration cases plus Linux, macOS, and Windows validation. The later exact-head run [39175250100](https://github.com/snapetech-org/chaptarrng/actions/runs/39175250100) on PR head `e4db2d46` passed the platform suites, all 4 PostgreSQL fixture cases, release-note and receipt checks, CodeQL, dependency review, secret scan, and NuGet submission. That PostgreSQL test remains limited to one migration-158 synthetic schema and does not establish operator-data acceptance; PostgreSQL conversion remains unsupported in published releases. See [ChaptarrNG PR #131](https://github.com/snapetech-org/chaptarrng/pull/131) and the [fixture evidence](https://github.com/snapetech-org/chaptarrng/blob/2f8c3b7f/docs/maintainers/BOOKSHELFNG_MIGRATION_FIXTURE_EVIDENCE.md).
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
