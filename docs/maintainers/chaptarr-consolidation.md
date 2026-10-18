# BookshelfNG retirement and ChaptarrNG consolidation

## Current status — 2026-10-18

BookshelfNG `0.4.21.71` is the published final source release. Its issue #114
request is closed; the `.71` release contains the optional new-author path
setting and the source-side appdata archive helper. ChaptarrNG `v0.9.977` is
published with preview, apply, rollback, automatic startup conversion, an
embedded source migration chain, and a safe fallback for records whose media
format cannot be inferred. ChaptarrNG
`v0.9.974` and later initialize missing new-author roots from configured
format defaults without replacing explicit values or rewriting existing
authors and files.

The public ChaptarrNG `v0.9.977` supports BookshelfNG migration-158 SQLite and
applies the embedded source chain to a disposable copy before conversion. Its
table guard rejects schemas before migration 14 because they still use
`Blacklist`. PR #126 merged a version-aware fix and synthetic migration-1
rollback fixture into `main`; hosted Linux, macOS, Windows, and PostgreSQL
migration checks passed. The source fix is not in `.977`, and releases remain
frozen until the retirement gates close. The populated synthetic v22 fixture
passes local and hosted validation but is not evidence from real older-schema
operator data. A populated Linux/amd64 rehearsal of the final schema accounted
for all 127,177 rows across 39 source tables. Its 81 media choices were
technical test inputs,
not reviewed classifications. The published `.976` converter now keeps
unresolved works in both catalogs, unmonitored, and writes a private review
file; operators still need to classify those works. The `.976` release
workflow passed Linux, macOS, Windows, and PostgreSQL migration validation.
ChaptarrNG `.977` packages an optional aggregate-only diagnostics module that
preserves an existing BookshelfNG opt-in only when both the legacy flag and
archived plugin marker are present. Its Linux, macOS, and Windows artifact
checks passed; testing environment transfer on an installed migration remains
open. This remains bounded evidence: older-schema behavior on real data, PostgreSQL
source conversion, two populated BookshelfNG databases, every
provider/environment contract,
rollback on operator data, full feature parity, and each package-channel
upgrade remain open.

The current ChaptarrNG retirement branch adds PostgreSQL migration for one migration-158 source schema and native Hardcover identity handling. Run [39132760214](https://github.com/snapetech-org/chaptarrng/actions/runs/39132760214) on `9c051d3d` reported NUnit source line 162 in `should_preview_convert_and_restore_a_current_bookshelf_postgres_schema`. The fixture seeds `BookImportMinimumMatchPercent` with that exact casing but the check queried the key in lowercase, identifying a fixture expectation error. ChaptarrNG commit [b5bd9527](https://github.com/snapetech-org/chaptarrng/commit/b5bd9527) corrects the three retained-config checks; exact-head run [39133225495](https://github.com/snapetech-org/chaptarrng/actions/runs/39133225495) is running. The candidate remains unsupported for operator data; provider, database, feature, and channel acceptance gates remain open.

The migration bridge is disabled. ChaptarrNG AUR `0.9.977-1` is published;
BookshelfNG's public AUR identity remains at `0.4.21.71-1` on the BookshelfNG
payload. COPR built `chaptarrng 0.9.977-1` successfully for Fedora 43, 44, 45,
and Rawhide x86_64; the legacy COPR trigger was skipped. ChaptarrNG Chocolatey
`.977` built and passed the hosted package-transition smoke, but its publish
returned HTTP 403 and the live feed has no `chaptarrng` entry. The BookshelfNG
Chocolatey identity remains public at `0.4.21.70`. GHCR published the standard
`.977` image but did not redirect legacy aliases. See the maintained
[retirement status page](https://github.com/snapetech-org/chaptarrng/blob/main/docs/BOOKSHELFNG_RETIREMENT.md)
and the user-facing
[migration guide](../migrate-from-bookshelfng-to-chaptarrng.md) for the current
channel checklist and operator procedure.

ChaptarrNG `v0.9.977` remains the latest public release; `.978` is a source
version bump. PR #128 merged release and distribution workflows that fail
closed unless `CHAPTARRNG_RELEASE_READY=true`, and the repository variable is
unset. Do not publish a release, package, image, or channel update while
retirement acceptance remains open. BookshelfNG PR #148 merged its fail-closed publisher gate to `main` as `c6b4642`; its tag-triggered image/release jobs, manual distribution retries, and legacy bridge require `BOOKSHELFNG_RELEASE_READY=true`, which remains unset. PR #127
merged to ChaptarrNG `main` as `b3089a39`. It adds selectable supplemental
catalogs, per-field preferences, and exact cross-catalog recovery for unmapped files through ISBN, ASIN,
provider IDs, and normalized title/author evidence. Linux, macOS, Windows,
PostgreSQL migration, CodeQL, dependency/security, and release-note checks
passed on its exact head. Four provider-dispatch CodeQL findings on an earlier
head were reviewed and dismissed as false positives because they route only to
allowlisted public APIs. The merged source is not in public `.977` and has not
closed settings or converted-operator-data acceptance.

ChaptarrNG PR #129 merged to `main` as `949ae3dd`. Its clean head
`a671f4b3` passed hosted Linux, macOS, Windows, PostgreSQL migration, CodeQL,
dependency/security, and release-note checks. It ports the opt-in M4B merge
settings, tagged track ordering and chapter titles, original-track fallback,
and source cleanup only after successful move-mode import; copy mode retains
the sources. A synthetic two-track smoke using the `.977` toolchain produced
AAC at 44.1 kHz stereo and preserved the supplied chapter titles and offsets.
That validates m4b-tool and its sidecar format, not the new importer end to
end or representative library media. Focused importer tests cover selection,
chapter/tag behavior, and fallback with a mocked converter. The source change is not in public
`.977`; representative-media acceptance remains open. Neither merge closes
real-data migration/rollback, settings parity, full feature parity, or
installer/channel acceptance.

ChaptarrNG PR #130 merged to `main` as `9f1ae60b`; hosted Linux, macOS,
Windows, PostgreSQL migration, CodeQL, dependency/security, and release-note
checks passed. When no explicit `BookMatchingStrictness` is configured, the
converter maps legacy `BookImportMinimumMatchPercent` values 50–66 to
Aggressive, 67–82 to Balanced, and 83–99 to Strict; an explicit mode takes
precedence, invalid legacy values fail closed, and the original source row is
preserved. The report identifies this as a lossy approximation between
different algorithms. Converted-data acceptance remains open, and the change
is not in public `.977`.

The tracked path-level inventory was regenerated against BookshelfNG `main`
`abc4e4fa` and ChaptarrNG `main` `9f1ae60b`. It covers 540 reachable post-fork
commits (531 absent from the pinned Bookshelf lineage ref) and 1,091
net-changed paths: 437 have no same-name mapped target, 493 differ and need
review, 155 are identical, four are text-equivalent after branding/newline
normalization, and two were deleted in BookshelfNG. This target includes
ChaptarrNG PRs #127, #129, and #130, now merged. The source changes remain unpublished
because the retirement release gate is closed. These counts identify a review queue;
path or text similarity does not prove that behavior is equivalent or safely
retired.

The detailed investigation below records historical candidate revisions and
their test evidence. Its pinned source counts and older release/channel rows
are snapshots, not current publication status. BookshelfNG issue #144 remains
open; full feature and channel acceptance is not complete.

At the GitHub security audit for this work, neither repository had open
CodeQL or Dependabot alerts. Secret scanning is disabled on both repositories,
so there is no server-side secret-alert inventory. The release workflows and
local dependency checks are recorded separately from this migration evidence.

## Historical investigation snapshot — 2026-10-14

Status at that snapshot: implementation and validation in progress; **not safe
to redirect releases**. AI-assisted investigation and implementation by
Codex. Confidence was high for one populated migration-158 SQLite run,
moderate for broader conversion behavior, and low for retirement readiness.

> The inventory, branch names, pull-request states, migration target version,
> and release-channel observations below are evidence recorded on October 14.
> They are retained as history; the current status above supersedes them.

The generated path inventory is pinned to BookshelfNG `main`
`5d696fb0b3cba552fa12b912a825954e2473e0e6` and ChaptarrNG PR #100
`561bf3954d0bb2bcc3beb546accdec76f26718e4`. It covers 426 reachable
post-fork commits (417 absent from the pinned Bookshelf lineage ref) and
1,045 net-changed paths: 422 unmapped, 473 different, 144 identical, four
text-equivalent after normalization, and two deleted. These path-level states
are an audit queue, not a semantic parity result.

At this review, BookshelfNG `main` is `5d696fb0`; ChaptarrNG `main` is
`6731a436`, compared with upstream `develop` at `e67374f4`. ChaptarrNG `main`
is 606 commits ahead and zero behind upstream across 1,485 net-changed paths.
The PR #100 candidate is 25 commits ahead of ChaptarrNG `main`, zero behind,
with 359 changed paths. Open ChaptarrNG product, security, and validation PRs
#78, #100, #103, and #105–#109, along with open dependency updates, remain in
the cumulative upstream retirement gate. The integration branch
`codex/bookshelf-consolidation-integrated-20261014` is at PR head
`561bf3954d0bb2bcc3beb546accdec76f26718e4`. The importer is wired into
ordinary ChaptarrNG startup and uses the same standard product as fresh
installs. It is under review as [ChaptarrNG PR
#100](https://github.com/snapetech-org/chaptarrng/pull/100), but is not merged
or released; BookshelfNG is not ready to retire.

The local focused migration fixtures pass 23/23. The full Release-mode Core
suite passed 4,065 tests with 0 failures and 3 skipped on the same .NET
application sources as current PR #100 head; its latest commit changes only
the validation engine and its tests. A hosted Windows run on the preceding
head failed four migration/rollback tests. The validation engine now extracts
only a safe exception type and method frame, with regression coverage proving
that exception text, paths, and values stay redacted. Exact-head hosted checks,
including a Windows rerun, are queued. Local results do not close the hosted
platform gate.

ChaptarrNG PRs #73, #76, and #77 merged on October 13, 2026. BookshelfNG PR
#112 and SeerrNG PR #203 also merged. The current local candidate and its new
hosted checks are separate from those earlier merges. BookshelfNG PR #128 is
open at `5743d1a610e8d1fd7e66c104df0e00fdaa5ee812`, PR #130 is open at
`094ac1a0a30687523fa6111dbf01286e5a7fff04`, and SeerrNG PR #280 is open at
`e844689d277bec83befd855536980b68d5045ceb`. Their required hosted checks are
queued. The conversion and channel evidence below records what has actually
been tested and what remains open.

## Populated database proof — 2026-10-14

On 2026-10-14, preview, explicit apply, and ordinary startup passed on
separate copies of one real populated BookshelfNG migration-158 SQLite
database using the ordinary ChaptarrNG Linux/amd64 image. The preview left the
source hash unchanged and accounted for all 127,177 source rows: 124,015 were
transformed and 3,162 volatile rows were deliberately reset. The retained
backup matched all 39 source table definitions and every source row. The
promoted native v119 database passed SQLite integrity and foreign-key checks.
Normal startup served the UI and preserved the existing port, URL base, API
key, SSL setting, and Docker image-pull update mechanism. The live BookshelfNG
service was not changed.

Eighty-one books needed an explicit media choice because the source did not
identify a single target format. The choices used for the technical apply
exercise were not reviewed as correct classifications. ChaptarrNG `v0.9.976`
keeps unresolved records in both catalogs without monitoring and writes a
private review file, so an operator map is no longer required to continue.
This run proves one exact populated SQLite schema and its standard-image path. It does not prove older schemas,
PostgreSQL, every provider or setting, rollback on a real populated deployment, all client
behavior, feature parity, or any published package-channel bridge.

## Pinned evidence and preservation

- Historical BookshelfNG code inventory: `9b0847973610f166523e155d3977049566d40745`,
  which was 30 commits ahead and zero behind `origin/main` at
  `ace06bc2766d26c8c5951563dd22679a486870bb`. Later documentation-only
  commits refresh the report without changing this source-code comparison.
- Historical ChaptarrNG integration base `683924daadf3201a467913c2ac4207eda6e61ea8`
  was 318 commits ahead and 3 behind its then-current main. The former
  candidate snapshot `1141c79687302366463bf87fed4565c4cc76090c` has been
  superseded; the current PR #100 head is `561bf3954d0bb2bcc3beb546accdec76f26718e4`,
  and its complete source-path comparison is in the regenerated inventory
  below.
  ChaptarrNG PR #73 merged as `5d8fffae` after all 14 reported checks passed.
  Its earlier Windows failures were resolved before merge. BookshelfNG PR #112
  merged as `7f7e07f0` with 10 successful checks and 4 skipped checks.
  ChaptarrNG PR #76 merged as `b2827c7a`; 13 checks passed, while receipt
  reconciliation exposed source-fingerprint drift. The platform receipts were
  captured after frontend CSS-module generation changed two tracked declaration
  files and created one untracked declaration; the PostgreSQL receipt used the
  clean committed tree. ChaptarrNG PR #77 merged as `ee2efc55` on October 13,
  moving the frontend build after receipt export and adding a workflow-order
  regression check. Current integration-branch hosted checks are a separate
  pending validation.

  The focused converter coordinator fixture passes 5/5 and the current
  populated importer/startup fixture passes 5/5. The fixture exercises mixed
  media and profile mapping, edition cover/link and narrator data,
  edition/file/history and series links, settings, users and notifications,
  orphan-ID reservation, restart idempotence, and safe refusal paths. The
  full Release-mode Core suite passed 4,065 tests with 0 failures and 3 skipped
  on the same .NET application sources as the current integration head.
  Twenty-three focused migration fixtures include
  rollback after a post-migration write. A self-contained Linux x64
  artifact with the production UI and updater converted the populated
  synthetic fixture on the isolated agentic VM through normal startup,
  retained a source backup identical at the table-definition and row level,
  reached migration v119, served the UI assets, and restarted without
  duplicating records. The target passed integrity and foreign-key checks and
  listened only on 127.0.0.1. Seven BookLore proxy tests passed, and the
  explicit live contract test passed against official BookLore v2.4.0: login
  succeeded, multipart upload returned 200 with an empty body, and the exact
  file bytes appeared in BookDrop. This proves API upload and file placement,
  not processing of a valid production book by BookLore. Separate focused
  reruns passed 16 migration-safety cases, 29 metadata/ranking/series cases,
  and 29 rename/path cases. A hosted Windows run on the prior PR #100 head
  failed four migration/rollback tests; the current exact-head hosted rerun is
  queued.
- ChaptarrNG feature snapshot: `24b340fffc43eb0883995a21665d3d051eb66abe`.
  Its historical comparison against `origin/main` at `660cc034` showed 317
  commits ahead and 4 behind across 703 paths. PR #76 later integrated the
  maintained backlog into main at `b2827c7a`; PRs #69–#75 are also merged.
  The remaining feature and migration blockers are tracked in the itemized
  guide below. PR #77 merged as `ee2efc55` with the receipt-fingerprint
  correction.
  ChaptarrNG's itemized cumulative blocker table is in its
  [fork feature guide](https://github.com/snapetech-org/chaptarrng/blob/main/docs/FORK_FEATURES.md#itemized-active-and-unreleased-chaptarrng-blockers).
- SeerrNG PR [#203](https://github.com/snapetech-org/seerrng/pull/203) at source
  head `dc6fe6e203ab25374581f2c24e2c858d919a549d` was squash-merged into
  `main` at `97aa148bed3a72cc02ca11f9f9d3341c230cceeb` on October 13, 2026.
  The final hosted run passed all four unit shards, lint/build, Playwright, six
  Cypress shards, docs, i18n, native validation, CodeQL, GitGuardian, and
  release-note checks; image and deployment jobs were skipped for the PR. Its
  VM smoke used an empty Chaptarr library, so it does not prove populated
  Bookshelf identity, request, or history continuity.
- Unraid companion: `bookshelfng-unraid` is being reviewed from branch
  `codex/bookshelfng-retirement-bridge-20261014`, based on `d96e097`. Its
  candidate keeps the Bookshelf container/template identity, port `8787`,
  `/config`, `/data`, `/download`, and PUID/PGID/TZ, while changing the image to
  `ghcr.io/snapetech/chaptarrng:latest`. It has not been merged or exercised
  through Unraid Community Applications. The separate ChaptarrNG Unraid
  listing remains the fresh-install path.
- YunoHost companion repos are separate package identities: BookshelfNG uses
  app id `bookshelfng` and port `8787`; ChaptarrNG uses `chaptarrng` and port
  `8789`. The Bookshelf package is on its historical `testing` branch, so its
  installed-app update path must be proven rather than inferred from the
  Chaptarr package.
- The BookshelfNG Helm chart is `charts/bookshelfng` and serves port `8787`;
  ChaptarrNG has no matching chart. A bridge must preserve the Helm release,
  service, StatefulSet, and PVC identities and use a single writer during
  SQLite conversion.
- BookshelfNG branch: `codex/bookshelf-chaptarr-consolidation-20261012`.
- The latest published BookshelfNG release is `main-v0.4.21.69` (not a draft);
  ChaptarrNG candidate version is `0.9.969`. The `.69` archive is the source
  schema baseline used for the read-only lineage tests.
- The generated [inventory](chaptarr-consolidation-inventory.json) records
  every reachable commit after the parent of the first fork commit
  `bde894431`, including maintenance and merged work. At BookshelfNG main
  `abc4e4fa` and ChaptarrNG main `9f1ae60b`, it contains 540 commits (531
  absent from the pinned Bookshelf lineage ref `3ac41f7`) and 1,091
  net-changed paths: 437 without a mapped Chaptarr path, 493 different mapped
  files requiring review, 155 identical files, four text-equivalent files
  after branding/newline normalization, and two deleted source paths. The
  inventory compares committed trees; current report edits are not included.
  These are path-level review states, not feature-parity counts.

Regenerate the tracked-source inventory with:

```sh
python3 scripts/audit-chaptarr-consolidation.py \
  --chaptarr /path/to/chaptarrng-candidate \
  --source abc4e4fa8a86e1affc3f44ce9bdb24c869d7da07 \
  --target 9f1ae60baf759bc361073fd0aee27e17a4c7f60f \
  --upstream refs/remotes/audit-bookshelf/develop \
  --output docs/maintainers/chaptarr-consolidation-inventory.json
```

## Hard compatibility boundaries

1. **Database migrations are unrelated.** BookshelfNG has 46 migration
   classes whose version attributes range from 1 through 158. The Chaptarr
   baseline at PR #73 has its own rebased migration history (113 numbered
   classes, versions 1 through 114, with version 103 absent). The current
   integration candidate has 117 numbered migration files through version
   119; it removes the conflicting version 108 migration and carries that
   schema repair at version 117, then applies versions 118 and 119. Never copy
   `VersionInfo` into a Chaptarr database or run its numbered migrations
   against BookshelfNG's schema.
2. **Filename detection is not schema conversion.** Chaptarr's
   `PathExtensions.GetDatabase()` returns an existing `chaptarr.db`; if it is
   absent, it chooses the first existing legacy file in `readarr.db`, then
   `audioarr.db` order. The resolver does not inspect file size or schema, or
   reject multiple legacy files. `DatabaseRestorationService.Validate()` checks
   SQLite integrity and Chaptarr's dual-root columns for backup restore
   candidates; that restore check does not validate the path selected for
   ordinary startup. A startup lineage check is still needed before migrations
   or maintenance can modify an old database. Separate-directory discovery and
   populated conversion remain open.
3. **Identity changes.** BookshelfNG has one book row with multiple formats;
   Chaptarr has provider-scoped identity and media-type-specific behavior.
   Its native Hardcover mode stores many primary provider IDs as bare numeric
   values. The current ChaptarrNG migration candidate uses the same explicit
   mode (`HARDCOVER=true`, unless `HARDCOVER_NATIVE=false`) to route those
   values to Hardcover, and otherwise retains the Goodreads interpretation;
   preview reports the selected dialect. The source-side helper candidate has
   a `--provider-mode` option for applying one choice consistently. These
   changes still need hosted and converted-data validation. Durable
   old-to-new author/book/edition/file maps and compatibility for existing
   clients referring to numeric local IDs remain separate acceptance work.
4. **Port changes.** BookshelfNG uses 8787; ChaptarrNG uses 8789. The legacy
   distribution must retain 8787, URL base, TLS settings and reverse-proxy paths.
5. **Updater ownership.** BookshelfNG's `ReadarrCloudRequestBuilder` queries
   `https://readarr.servarr.com/v1/` with a TODO to create its own endpoint.
   Changing Snapetech GitHub releases cannot redirect those installed clients.
   A package/container upgrade or one-time bridge installation is necessary
   for installations without a Snapetech-controlled update subscription.
6. **Immutable pins remain immutable.** Digest-pinned containers, fixed version
   tags, offline machines, manual archives and disabled updaters cannot be
   silently upgraded. Never overwrite old release assets or version tags.
7. **Configuration aliases are incomplete.** Current Chaptarr bootstrap maps
   `Readarr:Postgres` and `Audioarr:Postgres` into the native configuration,
   while application, authentication, server and update options bind from
   `Chaptarr:*`. Audit and translate BookshelfNG `Readarr__*` settings plus
   `BOOKSHELF_ALLOW_API_KEY_QUERY`, `BOOKSHELF_SEERRNG_API_KEY`,
   `BOOKSHELF_METADATA_SOURCES`, `BOOKSHELF_M4B_MERGE`, and `METADATA_URL`.
   Retain TLS, URL base, custom ports, proxy trust and all secrets with native
   precedence. Existing `apikey` query clients must continue working only where
   the old Bookshelf installation allowed them; do not change Chaptarr's global
   default for unrelated installs.

## Database conversion contract — required, incomplete

The released `.69` baseline databases are real application-created but empty.
The fixture generator also seeds one linked synthetic author, book, ebook and
audiobook editions/files, series, profile/root-folder settings, user, history,
notification, and blocklist rows into the released schema. The BookshelfNG
binary can read the synthetic author and book through its API, and SQLite
integrity and foreign-key checks pass. This proves source-schema readability,
not conversion. Conversion must build a new native Chaptarr database and keep
the Bookshelf database recoverable until the new instance has passed startup
and library checks.

| BookshelfNG data | ChaptarrNG destination | Required conversion rule |
| --- | --- | --- |
| `Authors` plus `AuthorMetadata` | `Authors` and provider identity columns | Merge provider identities without treating bare IDs from different catalogs as equal; translate ebook/audiobook roots, profiles, monitoring and tags separately |
| One `Books` row with `SeriesBookLink` relationships | One or more media-specific `Books` rows plus `SeriesBookLink` rows | Split when ebook and audiobook identity or monitoring differs; persist an old-author/book to new-author/book map before converting dependents |
| `Editions` and their provider IDs | Media-scoped `Editions` and provider ID fields | Preserve ISBN, ASIN, language, format, publisher, release date and narrator data; map each old edition to its new ID without assuming title equality means identity |
| `BookFiles`, `ExtraFiles`, and Calibre links | `BookFiles`, `ExtraFiles`, and Calibre metadata | Preserve every path, size, timestamp, part, quality, chapter/duration metadata, and Calibre association; never delete or move library files during conversion |
| `Users` | Native `Users` | Preserve identifier, username, and the legacy SHA-256 password hash; Chaptarr revalidates that hash on first login and upgrades it to salted PBKDF2, which must be proven with a populated fixture |
| Quality/metadata profiles, root folders, naming, indexers, download clients, notifications, and `Config` | Native settings and profile tables | Use explicit key-by-key aliases and per-setting defaults; preserve secrets only through the documented credential path and never log them. Do not drop unsupported profile settings such as `PreferredEditionTerms` or `PreferredSeries`; add native support or halt conversion |
| `History`, `DownloadHistory`, `MetadataFiles`, `Blocklist`, and import-list state | Native history, metadata-file, blocklist, and import-list tables | Map author/book/edition/file IDs through the durable identity map; define which cache and event rows are safe to retain, rebuild, or reset |
| `VersionInfo`, commands, scheduled tasks, transient import state, FTS/index tables | Native migration history and rebuilt derived state | Never copy source migration rows or queued work; run only Chaptarr migrations, then rebuild FTS and other derived indexes from converted records |

Every one of the source's 39 tables needs an explicit preserve, transform,
rebuild, or deliberate-reset disposition; no table may disappear by omission.

The published `v0.9.977` converter is SQLite-only, supports the exact
migration-158 Bookshelf schema, and bundles the embedded source migration
chain. Its table guard rejects schemas before migration 14 because they still
use `Blacklist`. PR #126 merged a version-aware fix and synthetic migration-1
rollback fixture into `main`, with hosted Linux, macOS, Windows, and PostgreSQL
migration checks passed. The fix is not in `.977`; no release will be cut
until the retirement gates close. The populated synthetic v22 fixture
validates source upgrade, conversion, preview immutability, and rollback. This
does not establish real-data support for older schemas. The populated fixture validates a subset
of table dispositions; complete provider/configuration coverage, PostgreSQL
import, and automatic discovery of a separate Bookshelf data directory remain
open.

The first-pass disposition below names every table in the released `.69`
schema. Some mappings now exist in the local candidate, but each remains open
until populated fixtures and real-data checks validate its semantics.

| BookshelfNG source tables | Proposed ChaptarrNG disposition | Required checks |
| --- | --- | --- |
| `AuthorMetadata` | Transform into native `Authors` metadata and provider identity columns | Preserve all populated metadata and qualify provider IDs; retain ambiguous identities for review. |
| `Authors` | Transform into native `Authors`, joining `AuthorMetadata` and translating common and format-specific paths, profiles, monitoring, tags, and add options | Preserve local identity aliases and both format settings independently. |
| `Books`, `Editions` | Transform into media-specific native `Books` and `Editions`; split one source book when ebook and audiobook state differs | Preserve every ISBN/ASIN, provider ID, edition property, cover/link metadata, narrator data and monitored state; map source book and edition IDs to all target rows. |
| `Series`, `SeriesBookLink` | Transform into native `Series` and duplicate links only where a source book splits across media | Preserve series identifiers, primary status, positions and ordering without duplicate logical links. |
| `BookFiles`, `ExtraFiles`, `MetadataFiles` | Preserve file paths and metadata while remapping author, book, edition and file foreign keys | Confirm every path/size/timestamp/part and Calibre reference; never move or delete media. |
| `Users` | Preserve username, identifier and legacy password hash in native `Users` | Prove legacy login and one-time salted-hash upgrade; never copy fixture or production credentials into logs. |
| `Config` | Transform with explicit key aliases and native precedence | Account for every key, secret-bearing setting, URL base, port, TLS, proxy and environment alias; fail on unknown security-sensitive keys. |
| `QualityProfiles`, `MetadataProfiles`, `QualityDefinitions`, `NamingConfig`, `RootFolders`, `Tags` | Transform into native profiles, roots, naming and tags; derive per-format settings from the source's shared values and overrides | Preserve cutoffs, formats, language, naming, Calibre settings and fallback behavior; add support or halt if preferred terms/series cannot be represented. |
| `CustomFilters`, `CustomFormats`, `DelayProfiles`, `ReleaseProfiles`, `RemotePathMappings`, `Indexers`, `DownloadClients`, `Metadata`, `Notifications`, `ImportLists` | Transform settings/contracts and foreign keys into native integration tables | Preserve enablement, tags, priorities, credentials, protocol/category and trigger behavior; unknown contracts must be reported, not dropped. |
| `Blocklist`, `History`, `DownloadHistory`, `PendingReleases`, `ImportListExclusions` | Preserve user-visible history and pending work with target identity mapping | Preserve event meaning and provider/book references; validate pending rows before allowing acquisition to resume. |
| `Commands`, `ScheduledTasks`, `DownloadClientStatus`, `IndexerStatus`, `ImportListStatus`, `NotificationStatus`, `VersionInfo` | Deliberately reset transient queues/health/task state and rebuild target migration history | Never copy source commands or migration versions; let Chaptarr initialize its own scheduled tasks and schema. |

The released `.69` SQLite schema is not a table-for-table copy. An isolated
runtime probe on October 13, 2026 found 39 Bookshelf tables at migration 158
and 79 Chaptarr tables at migration 119. Both fresh databases passed
`integrity_check` and had no foreign-key violations; those probes contained
only application defaults. Thirty-eight table names are shared;
`AuthorMetadata` exists only in BookshelfNG, while Chaptarr has 41 additional
tables, including derived search indexes. Bookshelf stores creator data in
`Authors` plus a separate `AuthorMetadata` table and links `Books` through
`AuthorMetadataId` and `ForeignBookId`. Chaptarr folds provider metadata into
`Authors` and uses media-scoped `Books`/`Editions` relationships.

The published ChaptarrNG converter uses a SQLite staging coordinator and row
importer wired into the full startup migration path. It accepts only the exact
BookshelfNG migration-158 table set; older or altered schemas fail closed. It
snapshots the source, migrates a native target, imports source rows with
explicit row accounting, validates SQLite integrity and foreign keys, retains
a Bookshelf backup, and promotes only after validation. The importer maps
author metadata and profiles, splits mixed books, and carries editions, files,
series, blocklist, settings, and supported history relationships. It preserves
edition image and link arrays, maps narrator strings into the target narrator
list, and reserves orphan file IDs against future reuse. Unresolved format
records are preserved in both catalogs without monitoring and reported in a
private review file. Unsupported provider identities and multiple selected
editions of one format still fail closed without changing source bytes. The
coordinator fixtures passed 5/5 and the populated startup/import fixture
passed 5/5 on the earlier candidate. The published migration-158 rehearsal
proves one SQLite database only; broader data, configuration, real-data
rollback, and channel coverage remain open.

Several compatibility questions remain after the first populated fixture:

- Mixed source books now split into media-specific target rows. Editions,
  files, series links, and file-specific history follow the mapped target row;
  generic book-level history retains the source ID, which is the primary
  target row. Review this behavior against representative user histories.
  Existing clients that refer to source numeric book IDs still need tested
  compatibility beyond the database conversion itself.
- Source `DownloadHistory` has no `BookId`; the importer retains event and
  author state and uses Chaptarr's `BookId = 0` sentinel. Replay and
  deduplication behavior remains untested against a populated download client.
- Blocklist rows convert local author/book links to provider-qualified IDs.
  A row with no supported provider identity fails closed; no collision-safe
  legacy identity adapter exists yet.
- Orphan `ExtraFiles.BookFileId` values remain unchanged and are reserved above
  the target file-ID sequence. The current fixture proves the immediate and
  future-ID boundary, but real sidecar and cleanup workflows still need tests.
- User identifiers and stored legacy password hashes are copied, but a real
  first login and one-time salted-hash upgrade have not been exercised through
  the converted database.
- Settings are not yet proven key-by-key. Common profile/root/config rows,
  import-list settings, and notifications have fixture coverage, but provider
  contracts, credentials, path aliases, and source-only settings still need a
  full field audit; non-empty unmatched columns in direct-copy tables now fail
  closed.

The populated fixture covers dual-format books, file-specific history,
bookless download history, a supported blocklist identity, settings, users,
notifications, and an orphaned extra-file reference. Unsupported provider and
ambiguous monitoring cases preserve the source bytes. Real databases, old
schemas, every provider/setting contract, and client behavior remain open.

Chaptarr's app-folder resolver keeps a non-empty `chaptarr.db`, selects exactly
one `readarr.db` or `audioarr.db` only when the primary is absent or empty, and
rejects multiple legacy candidates. It resolves filenames before database
recovery; the lineage check runs after restore and before migration. Full SQLite
main-database startup now invokes the importer for a detected Bookshelf schema.
The converter is limited to one legacy database in the selected data directory;
it does not discover a separate Bookshelf mount. The restore service's own
candidate validation remains separate from lineage conversion.

The converter must identify the exact Bookshelf database family and supported
schema version before writing. It must stop both applications, checkpoint
SQLite WAL, take a verified backup, and convert into a separate destination; for
PostgreSQL, use a separate target database or schema. A failed conversion leaves
the source untouched and the target unpublished. Promotion happens only after
SQLite integrity/foreign-key checks (or PostgreSQL equivalents), mapping and
row-count invariants, a clean Chaptarr startup, and API/file checks pass. The
original database and a rollback path remain available after promotion.

## Feature disposition and acceptance work

The BookshelfNG enhancements are a retirement gate as a whole and as
individual capabilities. Every row below is still an open blocker: a related
class, API label, or feature name is not evidence of equivalent behavior. A
row closes only after its behavior, configuration, identity, persisted data,
failure cases, and relevant clients have passed the stated acceptance work.
The exhaustive source commit/path inventory is an additional gate; these
feature rows do not replace it.

This gate answers whether BookshelfNG can be retired into ChaptarrNG. It is
separate from the later ChaptarrNG-to-Chaptarr gate. ChaptarrNG's existing
fork-maintained features, its features actively being added (including work
not yet in a published release), and every BookshelfNG feature retained by
this consolidation form one cumulative blocker set. The union blocks
ChaptarrNG retirement as a whole; each capability, sub-capability, migration
or data path, source-change group, and channel is also an individual gate.
Composite rows close only when every item they cover has passed its acceptance
checks. The combined matrix is maintained in the ChaptarrNG
[fork feature guide](https://github.com/snapetech-org/chaptarrng/blob/main/docs/FORK_FEATURES.md#chaptarrng-retirement-blockers).

The maintained backlog snapshot `24b340f` was historically 317 commits ahead
of and 4 behind `origin/main` at `660cc034`, across 703 changed paths. PR #76
later integrated that work into main at `b2827c7a`; PRs #69–#75 are merged.
The remaining active capabilities, proposed channel changes, and acceptance
evidence are listed in the ChaptarrNG
[itemized cumulative blocker matrix](https://github.com/snapetech-org/chaptarrng/blob/main/docs/FORK_FEATURES.md#itemized-active-and-unreleased-chaptarrng-blockers).
PR #73's metadata-preference port is merged, but its capability parity and
release acceptance remain individual blockers. Active capabilities count
before release.

| BookshelfNG capability or change | ChaptarrNG candidate finding | Retirement status | Required disposition and evidence |
| --- | --- | --- | --- |
| Rich book lookup; SeerrNG capabilities; paged books; format availability | Capability resource and Readarr facade exist | **Open blocker — integration parity unproven** | Test unchanged SeerrNG settings, IDs, keys, requests, pending work, and availability links against the exact candidate. |
| Native Hardcover, pacing, retry headers, author reuse, and refresh-age policy | Native Hardcover and V5 metadata implementations exist in a different provider pipeline | **Open blocker — semantic parity unproven** | Compare cache lifetime, key isolation, batching, 429 handling, refresh rules, and identity routing; retain configured behavior. |
| Supplemental catalogs: Open Library, Google Books, LOC, Gutendex, Internet Archive, NDL, Europeana, and Apify; per-field preferences | ChaptarrNG main after PR #127 (`b3089a39`) includes these adapters, selectable sources, qualified IDs, and per-field choices; hosted platform and security checks passed. Not in public `.977`. | **Source port merged; operator/settings acceptance open** | Preserve source selection/fallback, qualified IDs, field choices, provider-specific request constraints, and saved settings on converted operator data. |
| Cross-catalog unmapped recovery; normalized title and identifier matching | ChaptarrNG main after PR #127 uses exact ISBN/ASIN/provider IDs or normalized title and author, checks media type and stable identities, and queues the existing pending-author import without attaching files. PR #130 adds a lossy mapping from 50–66 to Aggressive, 67–82 to Balanced, and 83–99 to Strict when no explicit mode exists; invalid legacy values fail closed. Hosted checks passed. The source is not in public `.977`. | **Source port merged; behavioral/data acceptance open** | Verify no-false-match, ambiguity, converted provider IDs, the threshold approximation, and no-delete constraints on representative libraries. |
| Multiple ebook/audio formats; per-format folders and profile overrides | Native media-specific models, roots, and profiles exist | **Open blocker — conversion and isolation unproven** | Convert all rows and references; verify fallback rules, sibling-format isolation, monitoring, imports, upgrades, scans, and renames. |
| Weighted edition terms, preferred series, narrator evidence, and publisher/dramatized cases | The consolidation branch adds profile-based weighted edition scoring and preferred-series selection for filenames, ebook tags, Calibre, and AudioBookShelf metadata; Chaptarr's stronger match evidence stays ahead of the preference signal | **Partial candidate port; retirement blocker remains open** | Preserve weights, series choices, missing-evidence neutrality, tie behavior, and manual-review boundaries; verify the full Bookshelf edge-case set after profile/database conversion. |
| Optional M4B merge, chapters, part order, and completion state | ChaptarrNG PR #129 merged to `main` as `949ae3dd`; its clean head passed hosted Linux, macOS, Windows, PostgreSQL migration, CodeQL, dependency/security, and release-note checks. It ports the opt-in setting, tagged track order and chapter titles, original-track fallback, and move/copy source handling. A synthetic two-track smoke preserved supplied chapter titles and offsets using the `.977` toolchain, but did not exercise the importer end to end or representative media. | **Source port merged; open blocker** | Validate chapter offsets, embedded source chapters, tags, conversion failures, source retention, and restart/resume behavior with representative media and move/copy deployments. |
| Vendored TagLibSharp patch (253 changed source paths; byte-preserving MPEG-4 `chpl` handling) | The local candidate vendors the BookshelfNG TagLibSharp fork as a project and passes a synthetic version-1 `chpl` fixture that verifies exact atom preservation while writing a title. The vendor contains its LGPL-2.1 `COPYING` file; its strong-name key matches the key already committed with the BookshelfNG vendor source. | **Local port and focused regression pass; broader compatibility remains an open blocker** | Prove behavior on representative existing M4B files and across tag edits, conversion outputs, and failure cases; review continued use of the vendor signing identity and upstream the supported implementation. |
| Existing-torrent adoption and seeding preservation | Native continuation/adoption work exists | **Open blocker — edge cases unproven** | Test same-category and wrong-category cases, seeding-data preservation, and completed-download import. |
| Direct Download and browser-assisted grab | Native direct-download implementation and fixtures exist | **Open blocker — settings and recovery parity unproven** | Map settings and durable transfer state; test ordered URLs, interrupted recovery, architecture limits, and redirect/private-network safety. |
| BookLore BookDrop connection | Optional external app integration ported in PR #73; seven proxy tests pass, and the upload API/file placement were live-tested against official BookLore v2.4.0 | **Open blocker — settings migration, recovery, and successor disposition** | Convert stored Bookshelf notification settings and credentials; preserve streaming, redirect, supported-format, and size behavior. The live test proves API upload/file placement, not BookLore processing of a valid book. Test rejection, recovery, and partial batches. BookLore [identifies BookOrbit as its official successor and says it is entering maintenance mode](https://github.com/booklore-app/booklore/blob/develop/README.md); this client has no verified BookOrbit compatibility, so record and test a successor or legacy-user transition path. |
| Calibre, MyAnonamouse, Audiobookshelf sidecars, and other built-in integrations | Some have related target behavior; full semantic coverage is not established | **Open blocker — each integration must be dispositioned** | Test each connector's saved settings, identifiers, API behavior, generated metadata, and error handling. |
| Previewable single/bulk media moves and extra-file handling | Folder and colocation models differ | **Open blocker — workflow parity unproven** | Preserve preview, collision handling, cross-device behavior, and safeguards for unregistered/external files. |
| Optional diagnostics assembly | No corresponding opt-in module found | **Open blocker — preserve or replace** | Keep separate installation, explicit opt-in, and aggregate-only export behavior; migration must never enable it automatically. |
| Restricted service key, query-key policy, trusted proxies, body/rate limits | Chaptarr has its own service-key and facade policies | **Open blocker — aliases and permissions unproven** | Translate legacy settings without weakening configured restrictions; preserve key handling, authentication, and proxy behavior. |
| Encrypted backups and format-scoped profiles | Target encrypted backup support and native profile models exist | **Open blocker — old-data recovery unproven** | Test Bookshelf archive restore where supported, secret aliases, profile conversion, and rollback; never log credentials. |
| .NET 10, platform builds, ImageSharp removal, and security/dependency fixes | .NET 10 is present; target has different dependencies and still uses licensed ImageSharp | **Open blocker — patch-by-patch review pending** | Review each security and dependency change; retain compatible fixes and prove supported OS/architecture builds. |
| Release notes, announcements, package sync, and validation workflow | ChaptarrNG has separate release and validation workflows | **Open blocker — legacy identities not bridged** | Preserve old package/container IDs through tested compatibility artifacts; complete required per-repository validation without duplicate publication. |
| Every remaining fork change in the pinned source inventory | 426 reachable post-fork commits and 1,045 net-changed paths are recorded at BookshelfNG main `5d696fb0` and ChaptarrNG PR #100 `561bf395` | **Open blocker — exhaustive disposition pending** | Mark every path retained, ported, proven equivalent, or explicitly retired after impact review. |

The commit/path inventory remains the exhaustive review ledger. Every
behavioral change must be retained, ported, or proven equivalent; packaging
changes need a compatible channel disposition. Calling a feature obsolete
does not close its blocker. Any proposed removal remains open until an explicit
maintainer decision about its user impact. Similarity is not evidence, and the
combined feature set cannot be retired while any individual row or inventory
path remains open.

## Migration design

1. Detect lineage by schema and configuration, not filename or highest migration
   number. Reject unknown/mixed schemas without changing them. Detect active
   writers and refuse migration while the original app is running.
2. Take a consistent database backup (including WAL via the database backup
   API), configuration and application-state checkpoint. Check free space,
   ownership and integrity. Do not touch media or fetch metadata during conversion.
3. Create a new target database using Chaptarr's actual migrations. Convert into
   staging. Carry users/auth/API key, settings, root folders, download clients,
   indexers, tags, profiles, lists, notifications, authors, books, editions,
   files, series, history, blocklist, pending releases and transfer state.
   Classify every source table/column; never silently discard unknown state.
4. Map provider identity using explicit source lineage (`hardcover`/`softcover`)
   and stored provider identifiers. Preserve ebook/audio coexistence and all
   local foreign-key relationships. Record split records in an alias map used
   by legacy API routes and SeerrNG reconciliation. In native Hardcover mode,
   run preview and apply with that provider mode enabled so bare numeric IDs
   cannot be mistaken for Goodreads IDs.
5. Validate row accounting, foreign references, file path/size preservation,
   profile selections, historical references, encrypted backup round trip and
   unchanged credentials. Rebuild target indexes/FTS from converted rows.
6. Start a disposable target against staging with schedules and external writes
   disabled; run old and native API probes. Commit the migration marker and
   database/config switch only after all checks succeed. Use crash-recoverable
   phases and test termination at each phase. Restart must be idempotent.
7. Rollback before accepting new target writes restores the old checkpoint and
   image/package. After target writes, restoring an old checkpoint loses new
   work: require a deliberate recovery choice, never silently revert on boot.
8. PostgreSQL requires its own staged database/schema conversion and connection
   switch; SQLite-only proof cannot authorize PostgreSQL redirection.

## Distribution bridge matrix

Retain the old installation identity while delivering the ChaptarrNG application.
This avoids two services, data-directory moves and package-manager replacement
conflicts. The legacy package can remain a thin maintained compatibility package
after application development stops. Source retirement is not publisher retirement.

**Current state: no bridge has been released.** The ordinary ChaptarrNG
Linux/amd64 image passed preview, apply, and normal startup on separate copies
of one real populated migration-158 database; it is the same standard payload
for fresh and migrated installations. A legacy mutable image tag can be
retained only by pointing it at that exact multi-architecture manifest digest,
not by building a second compatibility image. No package or installer bridge
has been released. There is no single server-side redirect that reaches every
installed copy: the old updater checks the Readarr-owned service, and fixed
tags/digests, offline hosts, manual archives, and disabled updaters need an
explicit update action. Each channel needs its own tested bridge while
retaining its existing identity.

BookshelfNG PR [#130](https://github.com/snapetech-org/bookshelfng/pull/130)
adds a disabled-by-default publisher candidate for Docker Hub aliases, the
existing COPR identity, both Chocolatey package IDs, and the BookshelfNG Helm
chart identity. Its organization workflow no longer attempts to write the
personal BookshelfNG GHCR package. It requires checksummed assets from the
ordinary ChaptarrNG release and makes no external changes while disabled.
ChaptarrNG PR #100 contains the standard release and AUR package work. The
ordinary ChaptarrNG release workflow successfully pushed its standard image
to `ghcr.io/snapetech/chaptarrng` in run `38267985018`; this does not test a
BookshelfNG alias. The public, same-owner bridge repository
[`snapetech/bookshelfng-ghcr-release-bridge`](https://github.com/snapetech/bookshelfng-ghcr-release-bridge)
is wired to receive the exact image digest through a scoped dispatch in
ChaptarrNG PR #100; its workflow retags only `latest`, `hardcover`, and
`softcover` and rejects an older release event. That dispatch will run after
the ChaptarrNG changes merge and a gated release is published. BookshelfNG PR
#130 removes the duplicate organization-owned GHCR publisher. The bridge
publisher code is at `4c348c5` and its passing CI workflow is at `7e2d1b0`;
ChaptarrNG's dispatch is at `9e80f2c`, and the BookshelfNG workflow change is
at `d88accef`. The bridge still lacks its personal-account GitHub
App installation and write access to the existing `bookshelfng` package, so
no alias has been published and the migration gate stays closed. See GitHub's
documentation on
[package access control](https://docs.github.com/en/packages/learn-github-packages/configuring-a-packages-access-control-and-visibility)
and [linking a repository to a package](https://docs.github.com/en/packages/learn-github-packages/connecting-a-repository-to-a-package).

The public [new `slskdn/chaptarrng` COPR project](https://copr.fedorainfracloud.org/coprs/slskdn/chaptarrng/)
was created for Fedora 43/44/45 and Rawhide x86_64; its custom-source package
and package-scoped webhook are configured, and `COPR_WEBHOOK_URL` is stored in
ChaptarrNG Actions. No COPR build has run because public `v0.9.969` lacks the
standard SRPM and checksum assets. `BOOKSHELFNG_COPR_WEBHOOK_URL` is configured
in ChaptarrNG Actions, and the matching BookshelfNG `COPR_WEBHOOK_URL` was
rotated to the same package-scoped endpoint. Neither hook has been exercised
against a COPR build, and the old project's external bootstrap still needs its
one-time tag-pattern update. Chocolatey `chaptarrng` returns 404 and ChaptarrNG
has no Chocolatey publisher secret. The existing Chocolatey browser tab is
logged out; the Proton Pass extension is not exposed in the available browser
automation surface, so package publication remains unverified. The
[candidate's distribution matrix](https://github.com/snapetech-org/bookshelfng/blob/codex/bookshelfng-channel-bridge-20261014/docs/maintainers/chaptarrng-distribution-bridge.md)
lists the channel limits and enablement gates.

| Existing channel | Bridge needed | Automatic reach / acceptance |
| --- | --- | --- |
| GHCR and Docker Hub `latest`, `hardcover`, and `softcover` aliases | Keep all three mutable BookshelfNG tags as aliases of the exact multi-architecture digest for the ordinary ChaptarrNG image. Preserve the migrated provider choice in app data; do not retain a provider-specific image build. PR #130 has a guarded publisher candidate. Standard ChaptarrNG GHCR publication works; writing the user-owned BookshelfNG package from the organization repository is still unproven because of the namespace mismatch. | Next pull/recreate or configured updater after a real publish and digest check. Registry tags do not redirect running containers, and immutable digest pins or version-specific tags require explicit operator action. |
| Version/digest-pinned containers | Publish the standard ChaptarrNG image and provide a migration step and replacement digest | Explicit update needed; old pins remain recoverable |
| Unraid | Keep the BookshelfNG template identity and legacy mounts while changing its repository/tag to the ordinary ChaptarrNG image. Preserve port, `/config`, `/data`, `/download`, PUID/PGID, and TZ through the template and standard-image configuration. Update and sync companion `bookshelfng-unraid`. | Existing containers can pull the old image alias on their next update; changing the CA template alone does not rewrite an already-created container. Validate the installed template update plus stop, backup, conversion, restart, and rollback. |
| Debian/Ubuntu direct package and PPA | Higher-version `bookshelfng` compatibility package, same user/unit/data/env paths; Chaptarr payload and migrator | Configured apt repositories update normally; downloaded `.deb` files have no automatic subscription |
| Fedora/RPM/COPR | Higher-EVR compatibility RPM under existing project/package and signing trust; same service/user/data. PR #130 extends the verified source path for the legacy package identity. | Configured repository update; update the external COPR bootstrap to accept `vMAJOR.MINOR.PATCH`, then verify a real build, service stop, migration failure, and transaction retry. |
| AUR `bookshelfng-bin` | Update PKGBUILD/checksums to bridge release, retain package identity and hooks | User's AUR helper upgrade; AUR has no push installation mechanism |
| Chocolatey `bookshelfng` | PR #130 builds both the new `chaptarrng` and legacy `bookshelfng` package identities from the same checksummed standard Windows archive; retain the existing Windows service/data identity. | Chocolatey moderation plus a hosted upgrade from the published legacy package, successful startup, and rollback evidence. |
| Windows setup / portable | Bridge installer recognizes old installation, stops service, retains data/auth/port and recovery backup; launcher compatibility | One-time installer for unmanaged installs; old updater cannot be redirected by GitHub changes |
| macOS/Linux/FreeBSD archives | Legacy named wrapper/payload and migration-aware launcher in new bridge assets | Manual replacement unless an existing owned updater is subscribed; verify each platform rather than assuming Linux proof |
| AppImage | Legacy desktop/launcher/data identity and new bridge asset; inspect existing embedded update metadata | No blanket automatic update promise; demonstrate actual existing updater if any |
| Flatpak bundle | Retain `com.snapetech.BookshelfNG` and its sandbox data; bridge build | A standalone bundle is not a subscribed Flathub remote; one-time bundle install may be needed |
| Helm OCI chart | PR #130 renders a versioned chart under the existing OCI identity, pinned to the exact standard ChaptarrNG digest while preserving release, Service, StatefulSet, labels, port, and PVC names. | Helm/GitOps upgrades only when configured; a chart update does not force clients to upgrade. Local lint/render/package checks pass; test a real PVC upgrade, service selectors, rollback, and one writer for SQLite. |
| YunoHost historical installs | BookshelfNG app id `bookshelfng` and port 8787 differ from ChaptarrNG app id `chaptarrng` and port 8789. BookshelfNG publishing is retired; inspect installed catalog identity and companion repo branch, then provide a tested upgrade under the old app id with its existing service, URL path, data directory, and rollback. | The ChaptarrNG app listing cannot update an installed BookshelfNG app. Existing installs are reachable only if the old package's configured repository still delivers the compatibility upgrade. |
| Cloudron / Coop Cloud / StartOS catalog files | Verify which were actually accepted/published, then retain installed catalog IDs and data contract | A repository recipe/submission is not proof of an installed distribution channel |

Verify registry/package ownership, configured publisher state and signatures with
read-only API checks before designing an upload as available. Missing credentials
must be reported as unverified/unpublished, not a successful migration channel.

## Ordered implementation and release gates

1. Complete pinned feature/commit review, bridge inventory and recovery design.
2. Port independent missing features with native target tests and release notes.
3. Build lineage guard, converter, compatibility aliases and legacy image/package
   launchers. Exercise migration against generated fixtures from actual released
   BookshelfNG binaries, not hand-written approximations alone.
4. Verify SeerrNG before/after requests, local IDs, provider dialects, availability,
   polling, restricted credentials and pending requests without recreating servers.
5. Run repository-native validation engines on exact integrated source, including
   existing unrelated/dirty work requested by the maintainer. Record failures,
   skipped tests, source identities and runtime/live proof separately.
6. Install into disposable LAN VM environments. Test old release -> bridge ->
   restart -> subsequent target upgrade; forced migration failure; interrupted
   migration; disk full; missing secret; mixed formats; empty and populated
   libraries; SQLite WAL; PostgreSQL; custom URL base and port; non-root ownership.
7. Test package-manager upgrade/remove/reinstall semantics, configured update
   subscriptions, checksums/signatures, immutable release assets and downgrade
   recovery. Windows/macOS/FreeBSD and arm64 need corresponding execution evidence.
8. Review cumulative diffs and preserved work, commit/push, run required CI, merge
   ChaptarrNG and SeerrNG compatibility first, then BookshelfNG bridge automation.
   User has authorized these actions; failed required proof remains unfinished work.
9. Publish an immutable bridge release, test installation of its published artifacts,
   then advance moving aliases/publishers. Record digests and package versions.
   Keep old images/assets and the compatibility release machinery available.

## Evidence ledger

| Area | Current evidence | Remaining blocker |
| --- | --- | --- |
| BookshelfNG source inventory | Regenerated at source `5d696fb0b3cba552fa12b912a825954e2473e0e6` and target `561bf3954d0bb2bcc3beb546accdec76f26718e4`: 426 reachable commits, 417 absent from the pinned Bookshelf lineage ref, and 1,045 changed paths (422 unmapped, 473 different, 144 identical, four text-equivalent, two deleted). | Disposition every path as retained, ported, equivalent, or explicitly retired. Path classification does not establish feature equivalence; current report edits after those pins are not in the generated inventory. |
| ChaptarrNG Bookshelf feature port | PR #73 merged as `5d8fffae`; the current unpublished PR #100 application sources pass the local full Core suite (4,065 passed, 0 failed, 3 skipped) and 23 focused migration fixtures. A normal Linux/amd64 image previewed, applied, and started against separate copies of a real populated migration-158 database. The preview left the source hash unchanged and accounted for 127,177 rows; the retained backup matched all 39 source tables and rows; the v119 target passed integrity and foreign-key checks. Seven BookLore proxy tests and a live BookLore v2.4.0 upload/file-placement contract test pass. | Eighty-one source books still require operator-selected media classifications. Older schemas, PostgreSQL, full provider/config/client parity, representative M4B files, rollback on a real populated deployment, hosted Windows, and BookLore processing of a valid production book remain unproven. |
| ChaptarrNG maintained and active features | ChaptarrNG `main` at `6731a436` is 606 commits ahead and zero behind upstream `develop` at `e67374f4`, across 1,485 net-changed paths. PR #100 at `561bf395` is 25 commits ahead of main across 359 paths. Open product/security/validation work includes PRs #78, #100, #103, and #105–#109, with open dependency updates also in scope. | Every released and unreleased capability remains an individual ChaptarrNG-to-upstream blocker; see the itemized table linked above. |
| Bookshelf database compatibility | The standard Linux/amd64 candidate passed preview, explicit apply, and ordinary startup on separate copies of one real populated migration-158 SQLite database. Preview accounted for all 127,177 rows without changing the source; the retained backup matched all 39 table definitions and every source row; the v119 target passed integrity and foreign-key checks. Twenty-three focused migration fixtures pass, including rollback after a post-migration write. Eighty-one books require operator-selected media mappings; the test choices were not reviewed as classifications. | Only this exact migration-158 SQLite input is proven. Older schemas, PostgreSQL, complete provider/settings contracts, first-login hash upgrade, source numeric-ID client compatibility, rollback on a real populated deployment, feature parity, and release/channel bridges remain open. |
| Candidate runtime and SeerrNG | The ordinary Linux/amd64 image started the converted populated database, served /ping and the production UI, preserved port, URL base, API key, SSL, configured indexers, and Docker image-pull update behavior, and passed SQLite/FK checks. The live BookshelfNG service was untouched. SeerrNG PR #203 merged at 97aa148 with its hosted checks passing; those checks did not include a populated migration-library probe. | Real SeerrNG request, provider-identity, history, availability, and pending-import behavior against the converted real library remains unproven. The migration run does not cover that client contract. |
| Frontend build and static checks | `yarn typecheck` and the production webpack bundle pass; targeted ESLint reports no errors in changed JavaScript files. The bundle emitted 18 CSS-order warnings. Whole-tree ESLint reports 862 errors and 17 warnings across the inherited frontend tree. | Keep the inherited lint debt visible; resolve any candidate-caused lint error before merge. |
| Cross-project secrets | All three repositories ignore `.env`; BookshelfNG and SeerrNG have local ignored, untracked `.env` files, while this ChaptarrNG worktree has no `.env` file. No `.env` or `.lic` file is tracked. BookshelfNG's Docker ignore excludes `.env`/`.env.*`, the SixLabors license, and signing files while retaining `.env.example`; a disposable Docker build-context check confirmed `.env.example` stayed in the context and `.env` did not. The license file remains outside repository trees. | Keep Git and Docker-context checks in release validation; no secret may enter a commit, build log, or published artifact. |
| Hosted PR checks | BookshelfNG PR #112 merged as `7f7e07f0`; ChaptarrNG PRs #73, #76, and #77 merged as `5d8fffae`, `b2827c7a`, and `ee2efc55`; SeerrNG PR #203 merged as `97aa148`. ChaptarrNG PR #100 is at `9e80f2c1`; its current hosted checks are queued after the previous Windows run failed four migration/rollback tests. The new receipt captures a safe SQLite primary code and Chaptarr application method. BookshelfNG PR #128 is at `f508642d`, PR #130 at `d88accef`, and SeerrNG PR #280 at `e844689d`; the current required runs are queued. | Pass exact-head ChaptarrNG Windows and other required checks; complete the hosted BookshelfNG and SeerrNG checks. Local passes do not substitute for hosted platform validation. |
| Distribution and migration | Candidate packaging builds AUR and RPM identities from one standard Chaptarr archive; a Pacman upgrade retained the Bookshelf service identity, config, and data marker. ChaptarrNG's ordinary release run `38267985018` successfully published the standard GHCR image. ChaptarrNG PR #100 contains the gated exact-digest dispatch to the new user-owned bridge; BookshelfNG PR #130 removes its duplicate organization GHCR writer. Local actionlint, COPR source, Chocolatey template-render, Helm lint/render/package, digest-alias, stale-release rejection, and migration tests pass. The public `slskdn/chaptarrng` COPR project and webhook secrets exist. | No legacy redirect or COPR build is published, and the bridge remains disabled. The public Chaptarr release `v0.9.969` lacks standard archive, SRPM, and checksum assets. The personal bridge still needs its GitHub App installation and write access to the existing `bookshelfng` package. Existing BookshelfNG COPR bootstrap still needs its tag-pattern update. ChaptarrNG still lacks a public AUR `chaptarrng-bin` package and Chocolatey `chaptarrng`; its Chocolatey browser tab is logged out and Proton Pass is unavailable in the browser-control surface. Live registry/COPR/Helm publish tests, hosted Windows upgrade/moderation, and every other channel bridge remain open. Pinned, offline, updater-disabled, third-party, manual archive, and Readarr-owned updater paths remain separate. |
| Release decisions | The BookshelfNG enhanced feature set blocks BookshelfNG retirement as a whole and row by row. The later ChaptarrNG gate includes that retained set plus every ChaptarrNG maintained and actively developed capability, including unpublished work; each channel is a separate blocker too. | Current evidence does not support a main merge that claims parity, BookshelfNG retirement, or release redirection. |
