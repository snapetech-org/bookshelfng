# Move a BookshelfNG installation to ChaptarrNG

BookshelfNG `0.4.21.71` remains its final public release; ChaptarrNG `v0.9.977` remains the latest public release. ChaptarrNG `main` and application code are at [`6fc744ef`](https://github.com/snapetech-org/chaptarrng/commit/6fc744ef3db7aba815e7669f3794260c236a5a2a). Current source includes the disabled-by-default BookshelfNG issue [#114](https://github.com/snapetech-org/bookshelfng/issues/114) author-path setting and migration support, format-specific metadata-profile refresh, Calibre English language compatibility, whole-author path updates on folder moves, and the reviewed book-file organization/transfer port. These changes remain unpublished in `.977`. Exact-head Build [39542301711](https://github.com/snapetech-org/chaptarrng/actions/runs/39542301711) for `6fc744ef` passed Linux and PostgreSQL migration; macOS and Windows lanes are still running. CodeQL, security analysis, Semgrep, Trivy, and dependency submission passed. Focused fixtures pass author/migration 11/11, configuration persistence 1/1, format-profile refresh 5/5, Calibre language 4/4, Calibre proxy/series 6/6, Hardcover metadata/search 45/45, book-file move planning 15/15, and whole-author move paths 3/3. No release, tag, package, image, installer, or migration bridge has been published. Representative operator-data migration and rollback, complete feature/data acceptance, provider and SeerrNG workflows, installed update-channel handoff, and operator acceptance remain open; keep BookshelfNG in service.

The current source includes staged migration and rollback, provider and backup
compatibility, and a Windows installer candidate that keeps the legacy service
registration until ChaptarrNG passes its health check. A previous exact-head Windows Build passed installer construction, source-change
detection, service upgrade and rollback, cleanup, and selected-data-directory
checks. The previous new-head attempt exposed a Windows path-normalization test
fixture issue; the corrected fixture passes locally (8/8). Exact-head Build
[39535222684](https://github.com/snapetech-org/chaptarrng/actions/runs/39535222684)
is now running the platform builds and installer checks. These changes
are not in public `.977` and do not authorize a production cutover.

The schema-v4 audit pins BookshelfNG source `2811718076d84777a1b1132e4e5d2abd21231229` to ChaptarrNG target `6fc744ef3db7aba815e7669f3794260c236a5a2a`. It covers 732 post-fork commits (723 absent from pinned upstream history) and 1,119 changed paths: 85 reviewed mappings and 714 reviewed dispositions (177 retained, 133 equivalent, 233 ported, and 171 non-runtime retirements). Another 405 paths remain open (136 without mapped targets and 269 requiring semantic review). Recent passes dispositioned backup/restore, optional diagnostics, the BookshelfNG migration controller, six historical SQLite migration paths, author refresh, book-added handling, format-scoped media moves, author profile refresh, Calibre language compatibility, and edition metadata and selection, format-aware author/book operations, Calibre proxy behavior, native Hardcover metadata/search, book-file organization and move behavior, and series scoping, repository/cutoff search semantics, and API resource/backup behavior, release-search responses, and guarded command routes, and metadata-profile schema behavior using source and fixture evidence. Path-level coverage is not feature-parity proof, and no runtime retirement is approved.

**Migration decision: keep BookshelfNG in service; do not start a conversion.**
The published BookshelfNG `.71` source and ChaptarrNG `.977` converter support
preview of the exact SQLite migration-158 schema. Both retirement and
publishing gates remain open, so `.977` is not approved for migration and
unpublished `.978` source is not approved for production cutover. A schema
preview leaves the source database unchanged, though it may write a report;
it does not make an apply eligible. Wait for a supported destination build and
closed acceptance gates before stopping or replacing BookshelfNG.

The BookshelfNG Windows WPF installer still installs BookshelfNG. Merged
ChaptarrNG PR #131 adds an unpublished migration-only WPF installer for one
SQLite database using the standard `NT AUTHORITY\LocalService` account. It
fails closed on custom service accounts, PostgreSQL, and multiple databases;
it checks preview immutability for the database, WAL, and rollback journal
(SQLite rebuilds its transient `-shm` index) and attempts rollback after a
failed service handoff. The exact-head Windows Build passed the installer
fingerprint and a synthetic service upgrade, failed-upgrade automatic rollback,
explicit restore, and selected-data-directory checks. This is hosted fixture
coverage, not operator-data or custom-service acceptance; do not use it for a
production cutover.

**Provider identity warning:** the published `.977` importer maps bare numeric
IDs to Goodreads regardless of `HARDCOVER`. A native Hardcover database can
therefore pass structural checks while acquiring the wrong provider identity;
do not apply `.977` to native Hardcover data. The merged source implementation
requires an explicit provider mode, but it is not included in `.977`.

On 2026-10-19, candidate build `0.9.978.0` passed preview, apply, rollback
preview, and rollback against a task-scoped copy of populated migration-158
SQLite data with `HARDCOVER=true`. The live BookshelfNG service remained
running; candidate commands targeted only the separate copy, and network
access was not blocked for those commands. Preview did not change the source
copy. Apply passed integrity and foreign-key checks; rollback
preview left the converted database and source backup unchanged; explicit
rollback restored a byte-identical source backup and retained the converted
database separately. The private source snapshot remained unchanged. This
verifies one candidate SQLite round trip, not cutover readiness, ambiguous-media
classification, older schemas, PostgreSQL operator data, feature parity, or
installation-channel continuity.

The `.978` Linux app artifact from Build
[39267876585](https://github.com/snapetech-org/chaptarrng/actions/runs/39267876585)
also started against a fresh converted schema-121 copy using the published
`.977` runtime image, empty scratch mounts for configured media roots, and an
internal-only network; `/ping` returned HTTP 200. This verifies candidate app
startup with converted data, not candidate image packaging or an installed
image switch.

## Portable encrypted backups

Current ChaptarrNG `main` also accepts raw SQLite Bookshelf backup uploads
whose filename ends in `.db` or the legacy `.xml` suffix. `.xml` is only a
filename compatibility suffix; the content must still be SQLite. This upload
support is not in public `v0.9.977`, and a successful restore upload does not
approve a BookshelfNG migration or cutover.

Merged but unpublished ChaptarrNG application code at
`b7e900d49648269d5118bbfba44289c0200b095b` can import and export portable
BookshelfNG `BKSENC01` `.enc` backups using the same passphrase. The portable
format was introduced earlier in the branch. The implementation was
cross-checked against BookshelfNG's source; ChaptarrNG tests cover round
trips, wrong passphrases, tampering, truncation, malformed files, and cleanup.
The merged source restore UI accepts the `.enc` file and
prompts for its passphrase. Exact-head Build
[39267876585](https://github.com/snapetech-org/chaptarrng/actions/runs/39267876585)
passed Linux, macOS, Windows, PostgreSQL migration, release-note, and native
runner receipt checks. CodeQL, security analysis, and dependency review also
passed. Two earlier Build attempts exposed compile and test-fixture issues;
the `38be9422` exact-head run includes their fixes. At that checkpoint the candidate at
`b7e900d49648269d5118bbfba44289c0200b095b` passed Build
[39292223717](https://github.com/snapetech-org/chaptarrng/actions/runs/39292223717)
on Linux, macOS, and Windows, including PostgreSQL migration smoke,
release-note contract, native-runner receipt reconciliation, and the Linux
pinned-tool M4B smoke. CodeQL, security/secret scan, dependency review, and
NuGet submission passed; disposable-fork validation was skipped by its gate.
The prior PR head was docs-only commit
`93213b677a0bbb256aaf782c389a4f1a3d9c2ee7`; exact-head Build
[39316535744](https://github.com/snapetech-org/chaptarrng/actions/runs/39316535744)
passed in full attempt 3 on Linux, macOS, and Windows. PostgreSQL migration,
release-note contract, and native-runner receipt reconciliation also passed.
Application-code commit `0e881d921dd55aa89e12747557ccaadbb2352a21`
passed exact-head Build [39313568727](https://github.com/snapetech-org/chaptarrng/actions/runs/39313568727)
on Linux, Windows, and macOS, including PostgreSQL migration, release-note,
receipt, and Linux pinned-tool M4B checks. CodeQL, security/dependency,
dependency review, analysis, NuGet submission, and Helm identity checks passed;
disposable-fork validation was skipped by its gate. The merged source remains
unreleased and the migration acceptance gates remain open.

This support is not in ChaptarrNG `v0.9.977`, so `.977` cannot restore or export
these portable files. ChaptarrNG's scheduled `.zip.enc` files use a separate
format and are not interchangeable. Keep BookshelfNG running and retain a
separate appdata/database backup; portable backup compatibility does not approve
production cutover or close the remaining parity and rollback gates. See the
[candidate backup guide](https://github.com/snapetech-org/chaptarrng/blob/main/docs/BOOKSHELFNG_ENCRYPTED_BACKUPS.md).

BookshelfNG source snapshot `6e1a62e12` includes an Editions and Narrations
book-details tab backed by `GET /api/v1/book/{id}/editions/catalog`.
ChaptarrNG `main` now includes that tab and the series narrator comparison;
PR #131 code snapshot `8b4c6e23` integrates current `main` with the migration
and rollback changes. Local translation, type, targeted ESLint/Stylelint,
and release-note preview checks pass. Its release-note contract, dependency
review, security scan, and NuGet checks pass. CodeQL
[39205449712](https://github.com/snapetech-org/chaptarrng/actions/runs/39205449712)
passes; cross-platform Build
[39205452341](https://github.com/snapetech-org/chaptarrng/actions/runs/39205452341) passed Linux, macOS, Windows, PostgreSQL migration, release-note, and native-runner receipt checks. This UI remains source-only in public ChaptarrNG `.977`.

**Prior PR #131 application-code validation (2026-10-19):** Snapshot `0612cb4c90b75818e5349eb868cc0638825de02a` passed exact-head Build [39239940373](https://github.com/snapetech-org/chaptarrng/actions/runs/39239940373): Linux, macOS, and Windows tests, PostgreSQL migration smoke, native-runner receipt reconciliation, and release-note contract passed. CodeQL [39239934583](https://github.com/snapetech-org/chaptarrng/actions/runs/39239934583), security [39239940344](https://github.com/snapetech-org/chaptarrng/actions/runs/39239940344), NuGet submission [39239932165](https://github.com/snapetech-org/chaptarrng/actions/runs/39239932165), and dependency review [39239940313](https://github.com/snapetech-org/chaptarrng/actions/runs/39239940313) passed. Disposable-fork validation [39239940512](https://github.com/snapetech-org/chaptarrng/actions/runs/39239940512) was skipped by its external-fork gate. SeerrNG's adapter and request-route suite at source commit `b810153c` passed 4 files / 283 tests. The Linux artifact also passed the earlier empty-library API and authorization smoke. A populated source-build smoke for later code is recorded below.

Follow-up request lifecycle probe (2026-10-19): then-draft ChaptarrNG PR #131 commit `d97136040e5f76f6aa0b140d5c0ed74f8de7501e` added [`integration/seerrng-request-lifecycle.mjs`](https://github.com/snapetech-org/chaptarrng/blob/d97136040e5f76f6aa0b140d5c0ed74f8de7501e/integration/seerrng-request-lifecycle.mjs), wired into `integration/seerrng-smoke.compose.yml`. It passed against the prebuilt Linux candidate `0.9.978.0` from Build [39239940373](https://github.com/snapetech-org/chaptarrng/actions/runs/39239940373) (application snapshot `0612cb4c90b75818e5349eb868cc0638825de02a`) and SeerrNG source `b810153c`: the real `ReadarrAPI` adapter created, polled, and cancelled a synthetic unavailable-author import, and ChaptarrNG returned terminal `Failed` / `Cancelled by user`. `node --check`, Prettier, and Compose configuration validation passed. The earlier Compose run used a temporary runtime image. A follow-up source-build run on 2026-10-19 built through the checked-in `Dockerfile.build` from ChaptarrNG PR #131 head `7cfb5d87` and passed both scripts after the harness prepared its disposable `/books` volume as UID/GID `99:100`. The populated migration source-build smoke below now covers converted records on later code. Successful fulfillment, retries, availability/history, unchanged production settings, and operator acceptance remain open.

### Populated migration-to-SeerrNG source smoke (2026-10-19)

ChaptarrNG candidate commit `12f290bde5c04d29202775c0e9eeafb5fc20608f` was
built through its checked-in `Dockerfile.build` with SeerrNG at commit
`fdc439aa9`. The Compose harness seeded named disposable volumes with the
shared BookshelfNG migration-158 fixture, one synthetic audiobook and ebook,
and tiny `.m4b`/`.epub` placeholders. ChaptarrNG's normal startup converted
the database to schema 121 and retained the schema-158 source backup. With
`HARDCOVER=true`, the target config saved `HardcoverEnabled=true`.

SeerrNG's real `ReadarrAPI` read both migrated formats and checked their
Hardcover identities. Capability discovery, restricted service-key denial of
administrative and unrelated commands, and the pending add/poll/cancel flow
also passed. The importer suite passed 43/43 and Compose configuration,
`node --check`, and Prettier checks passed. These are synthetic placeholders,
not valid media. A separate real-tool importer check passed all six synthetic multipart M4B
cases on candidate `12f290bd`; Linux CI now runs it in a pinned tool image.
This does not establish operator-data correctness, pre-migration-14 or
PostgreSQL operator-data support, representative M4B media compatibility and restart/resume, full request fulfillment, installed rollback, or channel handoff. No release or
bridge was published; the release freeze remains active.

### Exact-head artifact repeat (2026-10-19)

The Linux artifact from exact-head Build [39316535744](https://github.com/snapetech-org/chaptarrng/actions/runs/39316535744), for then-draft PR #131 head `93213b677a0bbb256aaf782c389a4f1a3d9c2ee7`, was run through the checked-in SeerrNG Compose smoke on 2026-10-19. SeerrNG server code was rebuilt at commit `22f3bbc5874752b50a3b1206ca0bd3ebe0309f95` in a disposable worktree. The harness used a task-tagged runtime image based on the public `.977` image with the candidate app artifact copied in; it did not build or publish a candidate image.

Against a disposable populated migration-158 database, ChaptarrNG `0.9.978.0` accepted SeerrNG's restricted key for the audiobook and ebook library capabilities, denied administrative and unrelated command access, and passed SeerrNG's real `ReadarrAPI` pending-import create, poll, and cancel flow. The task's containers, volumes, temporary image, and worktree were removed after the run. This repeat strengthens synthetic API and request-lifecycle evidence; it does not validate image packaging, successful acquisition, operator data, live settings, installed rollback, or update channels.

### Provider configuration before migration

Merged ChaptarrNG source now includes compatibility ports
for BookshelfNG's OAuth-backed Goodreads bookshelf and owned-book import lists
and bookshelf/owned-book write notifications, alongside the Hardcover
public-list and reading-status provider. It carries complete saved credentials
and settings forward, blocks missing or partial credentials for OAuth-only
providers, and keeps public shelves available without OAuth when a valid
numeric user ID is saved. Preview omits all settings values and credentials.

Merged PR #131 source checks every configured indexer, download client, import list,
notification, and metadata provider against a matching Chaptarr implementation
and settings contract. It preserves a row's settings only when the contract and
serialized fields are supported. Unsupported implementations, contracts, or
fields are disabled in the staged target and reported as blockers before
promotion, without exposing credential values. This protects the source backup
and prevents a partially compatible provider from starting with default
settings. A matching contract still does not prove the saved credentials work
with the live provider; test those connections and behaviors using representative
converted data before approving a cutover.

This source compatibility does not prove Goodreads accepts a saved credential.
Goodreads stopped issuing new developer keys and announced API retirement, so
existing-account API behavior remains an acceptance gate. The OAuth provider
port is not in published ChaptarrNG `v0.9.977`; do not apply migration to
operator data while the release freeze is active. See the [Goodreads API
deprecation notice](https://www.goodreads.com/topic/show/21788520-api-deprecation).

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
rollback fixture into ChaptarrNG `main`, but they are not in `.977`. Earlier migration candidate checkpoint [PR #131](https://github.com/snapetech-org/chaptarrng/pull/131)
was draft at that time; it merged on 2026-10-20 as `d2bcba79`. Exact-head run
[39196795646](https://github.com/snapetech-org/chaptarrng/actions/runs/39196795646)
passed on head 2c0401fc: Linux, macOS, and Windows build/tests, PostgreSQL
migration fixtures, release-note validation, CodeQL, dependency/secret scans,
NuGet submission, and runner-receipt reconciliation. The previous run found
four Windows media-move fixtures that used POSIX-only paths; native temporary
paths fixed them. Disposable-fork validation was skipped by its gate. Fifty-two
focused importer, catalog, and capability tests pass locally. The populated
migration-158 SQLite copy passed preview, apply, restore preview, and rollback
with native Hardcover mode; network access was not blocked for those
candidate commands. This is not broad operator acceptance. Ambiguous media,
PostgreSQL operator data, feature parity, real
installed rollback, SeerrNG workflows, and installer/channel acceptance remain
open. The merged source remains unpublished and unsupported for operator cutover;
the [fixture evidence](https://github.com/snapetech-org/chaptarrng/blob/main/docs/maintainers/BOOKSHELFNG_MIGRATION_FIXTURE_EVIDENCE.md).

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
The then-draft PR #131 candidate `12f290bd` passed the six-case
tool-enabled synthetic importer smoke 6/6 in the checked-in Debian Bookworm
image with `m4b-tool` 0.5.2 and `mp4v2` 2.1.1. Successful cases check tag
ordering, chapter titles and offsets, metadata, registration, and Move/Copy
source handling. Failure cases verify fallback to separate original-track
imports in both modes when FFprobe cannot read a source and when `m4b-tool`
fails after a controlled FFmpeg conversion error. Linux CI now runs these
six cases through `integration/Dockerfile.m4b-test`. Synthetic embedded-chapter Move/Copy and TagLib-write cases pass on c4fa; representative M4B files and restart/resume remain open; the source change is not
in public `.977`.

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

Native Hardcover databases need the same provider mode during preview and apply. BookshelfNG commonly stores Hardcover work, author, edition, and series IDs as bare numbers. The merged ChaptarrNG source interprets them as Hardcover when `HARDCOVER=true` and `HARDCOVER_NATIVE` is not `false`; set `HARDCOVER=false` for a Goodreads-primary database. If the mode is unset or invalid, the merged ChaptarrNG source fails closed when it encounters a bare numeric ID rather than silently assigning Goodreads identity. The current-source helper requires `--provider-mode native-hardcover|goodreads` for both preview and apply. Native Hardcover also requires a versioned ChaptarrNG image tag `v0.9.978` or newer; `.977` and digest-only references are rejected because the helper cannot verify provider-mode support from a digest. BookshelfNG's `latest`, `main`, and `hardcover` Docker tags use native Hardcover mode; `softcover` uses Goodreads mode. Merged ChaptarrNG source includes matching compatibility image targets for those mutable aliases, but the targets have not been published or enabled. These changes are not in the published `.71` helper or ChaptarrNG `.977` image. Exact-head validation on commit b5bd9527 passed all 4 synthetic PostgreSQL migration cases, including normal-startup conversion with backup retention; Linux, macOS, and Windows platform validation also passed; converted-data acceptance remains open. Do not use those published builds for native Hardcover migration until the release-freeze gates close.

The appdata archive does not capture API-authentication environment variables.
Current ChaptarrNG `main` preserves the legacy
`BOOKSHELF_ALLOW_API_KEY_QUERY=false` switch when
`CHAPTARR__AUTH__ALLOWAPIKEYQUERY` is unset, and accepts
`BOOKSHELF_SEERRNG_API_KEY` when `CHAPTARR__AUTH__SEERRAPIKEY` is unset. An
explicit ChaptarrNG value takes precedence. The legacy SeerrNG credential
keeps the restricted book-service policy: it cannot read global configuration
or health routes, and book-file and history requests must include one positive
`bookId`. These environment fallbacks are source-only and are not in public
ChaptarrNG `v0.9.977`; preserve the variables in the deployment configuration,
but do not treat their presence as approval to cut over.

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
establish operator-data or install-channel acceptance. The merged ChaptarrNG
source fails closed if provider mode is missing or invalid, and its
compatibility image targets and alias bridge passed hosted regression scripts; local BuildKit target checks also passed. The actual GHCR images and alias dispatch were not built or published. This synthetic rehearsal does not establish operator-data or installer acceptance. No release or image aliases were published. See [ChaptarrNG PR #131](https://github.com/snapetech-org/chaptarrng/pull/131).

## What the helper does

ChaptarrNG `main` now also carries a host-side Docker handoff helper at
[`scripts/bookshelfng-to-chaptarrng.sh`](https://github.com/snapetech-org/chaptarrng/blob/83f66c36b4de225b63c5be833516ac571459a144/scripts/bookshelfng-to-chaptarrng.sh). Its helper checks cover backup-path containment, symlink aliases, and provider-mode and rollback safeguards. The release workflow will include it in future Linux standalone archives after publication is approved; it is not in public `.977` and does not authorize cutover.

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
   the versioned standard ChaptarrNG image. Current-source preview and apply
   require an explicit `--provider-mode`; the helper refuses to guess whether
   bare numeric provider IDs mean Goodreads or native Hardcover.

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

Merged ChaptarrNG source adds a separate BookOrbit Book
Dock notification destination. Its API client has mock coverage for streaming,
redirect refusal, credential and file rejection, and partial batches. An
isolated BookOrbit v3.2.0 live contract run passed initial setup, login, Book
Dock access, EPUB upload and listing, and unsupported-file rejection. This
confirms upload admission, not BookOrbit's downstream processing of a
production book or a transition using real BookshelfNG users and settings. The
source is in [PR #131](https://github.com/snapetech-org/chaptarrng/pull/131)
and is not included in public ChaptarrNG `v0.9.977`.

After a supported ChaptarrNG build containing BookOrbit is published, add and test a
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
not supported by that helper or the public `.977` image. The current-source
helper requires `--provider-mode goodreads` or `--provider-mode native-hardcover`
for preview and apply. For native Hardcover it also requires a versioned image
tag `v0.9.978` or newer and rejects digest references because their capability
cannot be verified. Use native mode only after the ChaptarrNG importer and
helper candidate have passed hosted and converted-data acceptance and are
distributed in a supported build. Use the same mode for preview and apply,
then configure the replacement container with native Hardcover enabled.

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
Earlier synthetic PostgreSQL snapshot [`43bc6363`](https://github.com/snapetech-org/chaptarrng/commit/43bc6363) passed four migration cases plus Linux, macOS, and Windows validation. The later exact-head run [39175250100](https://github.com/snapetech-org/chaptarrng/actions/runs/39175250100) on PR head `e4db2d46` passed the platform suites, all 4 PostgreSQL fixture cases, release-note and receipt checks, CodeQL, dependency review, secret scan, and NuGet submission. That PostgreSQL test remains limited to one migration-158 synthetic schema and does not establish operator-data acceptance; PostgreSQL conversion remains unsupported in published releases. See [ChaptarrNG PR #131](https://github.com/snapetech-org/chaptarrng/pull/131) and the [fixture evidence](https://github.com/snapetech-org/chaptarrng/blob/main/docs/maintainers/BOOKSHELFNG_MIGRATION_FIXTURE_EVIDENCE.md).
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
[maintainer readiness report](maintainers/chaptarr-consolidation.md) for the current status.
