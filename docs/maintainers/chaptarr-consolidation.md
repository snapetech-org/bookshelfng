# BookshelfNG retirement and ChaptarrNG consolidation

Status: investigation and implementation in progress; **not safe to redirect releases**.
Date: 2026-10-13. AI-assisted investigation and implementation by Codex.
Confidence: high for cited source findings; moderate for the implementation plan;
unknown for end-to-end migration until the matrix below passes.

The generated source comparison is pinned to BookshelfNG code at
`9b0847973610f166523e155d3977049566d40745` and the committed base of the local
ChaptarrNG integration worktree. Subsequent documentation-only commits refresh
evidence without changing the code inventory. The ChaptarrNG worktree also has
uncommitted changes, which are not represented in the generated inventory.
PR #73 merged as `5d8fffae` on October 13, 2026, bringing its metadata-
preference port into ChaptarrNG main. The importer described here remains in a
separate, uncommitted integration worktree. It is not a released converter or
a retirement-ready transition. That worktree now contains an importer for the
exact BookshelfNG migration-158 SQLite schema, wired into full startup
migrations; current fixture evidence and its limits are below.

## Pinned evidence and preservation

- BookshelfNG code inventory: `9b0847973610f166523e155d3977049566d40745`,
  which was 30 commits ahead and zero behind `origin/main` at
  `ace06bc2766d26c8c5951563dd22679a486870bb`. Later documentation-only
  commits refresh the report without changing this source-code comparison.
- ChaptarrNG integration base: `683924daadf3201a467913c2ac4207eda6e61ea8`,
  branch `codex/bookshelf-consolidation-integrated-20261014`; the historical
  comparison against `origin/main` at `660cc0341934513a411bd40d42c781f1313c08be`
  showed 318 commits ahead and 3 behind. Later PR merges advanced main, so
  these counts are not a current comparison.
  Its working tree contains 85 tracked changed paths and 267 untracked paths
  beyond the committed base; none are in the generated source/target inventory
  and all remain part of the blocker review.
  ChaptarrNG PR #73 merged as `5d8fffae` after all 14 reported checks passed.
  Its earlier Windows failures were resolved before merge. BookshelfNG PR #112
  merged as `7f7e07f0` with 10 successful checks and 4 skipped checks.
  ChaptarrNG PR #76 merged as `b2827c7a`; 13 checks passed, while receipt
  reconciliation exposed source-fingerprint drift. The platform receipts were
  captured after frontend CSS-module generation changed two tracked declaration
  files and created one untracked declaration; the PostgreSQL receipt used the
  clean committed tree. ChaptarrNG PR #77 moves the frontend build after
  receipt export and adds a workflow-order regression check. Its exact-head
  hosted run is pending. Earlier local full Core, Chromium, rename/path, and
  M4B fixture results remain tied to their recorded snapshots.

  The focused converter coordinator fixture passes 5/5 and the current
  populated importer/startup fixture passes 5/5. The fixture exercises mixed
  media and profile mapping, edition cover/link and narrator data,
  edition/file/history and series links, settings, users and notifications,
  orphan-ID reservation, restart idempotence, and safe refusal paths. The
  complete Core suite passed 4,047 tests with 0 failures and 3 skipped (4,050
  total) in 9m44s on a build before the final cover/link-preservation fix; the
  focused fixture passed again after that fix. A self-contained Linux x64
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
  and 29 rename/path cases. The current integration tree still needs a hosted
  Windows rerun.
- ChaptarrNG feature snapshot: `24b340fffc43eb0883995a21665d3d051eb66abe`.
  Its historical comparison against `origin/main` at `660cc034` showed 317
  commits ahead and 4 behind across 703 paths. PR #76 later integrated the
  maintained backlog into main at `b2827c7a`; PRs #69–#75 are also merged.
  The remaining feature and migration blockers are tracked in the itemized
  guide below. PR #77 is open for the receipt-fingerprint correction.
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
- Unraid companion: `bookshelfng-unraid` is clean on `main` at `d96e097`; its
  template uses `ghcr.io/snapetech/bookshelfng:latest`, internal/host port
  `8787`, `/config`, `/data`, `/download`, and PUID/PGID/TZ variables. The
  ChaptarrNG template uses a separate image identity, port `8789`, and
  `/audiobooks`, `/ebooks`, and `/downloads`; an old-template bridge must keep
  the Bookshelf container contract while adapting the Chaptarr process.
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
  `bde894431`, and every net-changed path. It includes maintenance and merged
  work. At source `9b084797` and target `683924d`, it contains 412 commits
  (403 absent from the pinned Bookshelf lineage ref `3ac41f7`) and 1,039
  net-changed paths: 338 different mapped files, 684 paths without a mapped
  target, 11 identical files, four text-equivalent files after
  branding/newline normalization, and two deleted source paths. This is a
  committed-tree comparison; the Chaptarr integration working tree and current
  Bookshelf documentation edits are not included. These are path-level review
  states, not feature-parity counts.

Regenerate the tracked-source inventory with:

```sh
python3 scripts/audit-chaptarr-consolidation.py \
  --chaptarr /path/to/chaptarrng-candidate \
  --source 9b0847973610f166523e155d3977049566d40745 \
  --target 683924daadf3201a467913c2ac4207eda6e61ea8 \
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
   Bare Hardcover and Goodreads IDs must not collide. Conversion needs durable
   old-to-new author/book/edition/file maps and compatibility for existing
   clients referring to numeric local IDs.
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

The current candidate is SQLite-only and only supports the exact migration-158
Bookshelf schema. The populated fixture validates a subset of table
dispositions; complete provider/configuration coverage, PostgreSQL import, and
automatic discovery of a separate Bookshelf data directory remain open.

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

The local ChaptarrNG integration worktree now has a SQLite staging coordinator
and row importer wired into the full startup migration path. It accepts only
the exact BookshelfNG migration-158 table set; older or altered schemas fail
closed. It snapshots the source, migrates a native target, imports source rows
with explicit row accounting, validates SQLite integrity and foreign keys,
retains a Bookshelf backup, and promotes only after validation. The importer
maps author metadata and profiles, splits mixed books, and carries editions,
files, series, blocklist, settings, and supported history relationships. It
preserves edition image and link arrays and maps narrator strings into the
target narrator-name list. It preserves orphan file IDs and reserves their sequence values against future
reuse. Unsupported provider IDs, multiple monitored editions, and ambiguous
mixed-format monitoring state refuse conversion without changing source bytes.
The coordinator fixtures pass 5/5; the populated startup/import fixture passes
5/5. This is still uncommitted candidate code, not a released converter or
proof of production-database compatibility.

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
| Supplemental catalogs: Open Library, Google Books, LOC, Gutendex, Internet Archive, NDL, Europeana, and Apify; per-field preferences | Provider-ID columns exist, but the BookshelfNG adapter and settings set is not present | **Open blocker — port or replace** | Preserve adapters, source selection/fallback, qualified IDs, field choices, and provider-specific request constraints. |
| Cross-catalog unmapped recovery; normalized title and identifier matching | FTS and matching architectures differ | **Open blocker — behavioral cases unproven** | Port the cases rather than the old engine wholesale; retain no-false-match, ambiguity, and no-delete constraints. |
| Multiple ebook/audio formats; per-format folders and profile overrides | Native media-specific models, roots, and profiles exist | **Open blocker — conversion and isolation unproven** | Convert all rows and references; verify fallback rules, sibling-format isolation, monitoring, imports, upgrades, scans, and renames. |
| Weighted edition terms, preferred series, narrator evidence, and publisher/dramatized cases | The consolidation branch adds profile-based weighted edition scoring and preferred-series selection for filenames, ebook tags, Calibre, and AudioBookShelf metadata; Chaptarr's stronger match evidence stays ahead of the preference signal | **Partial candidate port; retirement blocker remains open** | Preserve weights, series choices, missing-evidence neutrality, tie behavior, and manual-review boundaries; verify the full Bookshelf edge-case set after profile/database conversion. |
| Optional M4B merge, chapters, part order, and completion state | Native conversion and multipart handling exist | **Open blocker — media parity unproven** | Map opt-in policy; test chapter offsets and preservation, ordering, metadata, source retention, and failure recovery. |
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
| Every remaining fork change in the pinned source inventory | 412 reachable post-fork commits and 1,039 net-changed paths are recorded at the current committed source and target pins | **Open blocker — exhaustive disposition pending** | Mark every path retained, ported, proven equivalent, or explicitly retired after impact review. |

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
   by legacy API routes and SeerrNG reconciliation.
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

**Current state: bridge implementation not started.** The local converter has
passed a synthetic populated-library startup test in a self-contained Linux
artifact on the isolated VM, but no BookshelfNG compatibility image, package,
or installer has been built or tested for an existing channel. There is no
single server-side redirect that reaches every installed copy: the old
updater checks the Readarr-owned service, and fixed tags/digests, offline
hosts, manual archives, and disabled updaters need an explicit update action.
Each channel needs its own tested bridge while retaining its existing identity.

| Existing channel | Bridge needed | Automatic reach / acceptance |
| --- | --- | --- |
| GHCR and Docker Hub `latest`, `hardcover`, `softcover`, existing edge aliases | Existing images expose port 8787 with `/config`, `/data`, `/download`, PUID/PGID, TZ, and flavor variables. Publish tested Chaptarr compatibility images under those old mutable identities; configure Chaptarr to retain the old port and translate old settings. | Next pull/recreate or configured updater if Snapetech can publish to both old packages; test each flavor and architecture. Registry names do not redirect by themselves, and immutable pins remain unchanged. |
| Version/digest-pinned containers | New versioned bridge image and migration instructions | Explicit update needed; old pins remain recoverable |
| Unraid | Keep the BookshelfNG template identity, `:latest` image alias, port 8787, `/config`, `/data`, `/download`, PUID/PGID, and TZ. The ChaptarrNG template currently uses port 8789 and different media/download mount names, so the bridge image must honor the old in-container paths. Update and sync companion `bookshelfng-unraid`. | Existing containers can pull the old image alias on their next update; changing the CA template alone does not rewrite an already-created container. Validate the installed template update plus stop, backup, conversion, restart, and rollback. |
| Debian/Ubuntu direct package and PPA | Higher-version `bookshelfng` compatibility package, same user/unit/data/env paths; Chaptarr payload and migrator | Configured apt repositories update normally; downloaded `.deb` files have no automatic subscription |
| Fedora/RPM/COPR | Higher-EVR compatibility RPM under existing project/package and signing trust; same service/user/data | Configured repository update; verify service stop, migration failure and transaction retry |
| AUR `bookshelfng-bin` | Update PKGBUILD/checksums to bridge release, retain package identity and hooks | User's AUR helper upgrade; AUR has no push installation mechanism |
| Chocolatey `bookshelfng` | Higher package version with verified bridge asset, retain Windows service identity/data and idempotent upgrade | Chocolatey upgrade/scheduled updater; rollback and existing service account tested |
| Windows setup / portable | Bridge installer recognizes old installation, stops service, retains data/auth/port and recovery backup; launcher compatibility | One-time installer for unmanaged installs; old updater cannot be redirected by GitHub changes |
| macOS/Linux/FreeBSD archives | Legacy named wrapper/payload and migration-aware launcher in new bridge assets | Manual replacement unless an existing owned updater is subscribed; verify each platform rather than assuming Linux proof |
| AppImage | Legacy desktop/launcher/data identity and new bridge asset; inspect existing embedded update metadata | No blanket automatic update promise; demonstrate actual existing updater if any |
| Flatpak bundle | Retain `com.snapetech.BookshelfNG` and its sandbox data; bridge build | A standalone bundle is not a subscribed Flathub remote; one-time bundle install may be needed |
| Helm OCI chart | The current chart is named `bookshelfng`, exposes port 8787, and persists `/config`; ChaptarrNG has no matching chart. Publish a bridge chart under the existing OCI identity while preserving release, Service, StatefulSet, labels, and PVC names; add media paths only when existing values provide them. | Helm/GitOps upgrades only when configured; a chart update does not force clients to upgrade. Test PVC retention, service selectors, rollback, and one writer for SQLite. |
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
| BookshelfNG source inventory | Committed source `9b08479` compared with committed integration target `683924d`: 412 reachable commits, 403 absent from the pinned Bookshelf lineage ref, and 1,039 changed paths. Dirty worktree changes are outside this generated inventory. | Path classification is not feature equivalence; review and disposition every path, then regenerate after committing the current candidate. |
| ChaptarrNG Bookshelf feature port | PR #73 merged as `5d8fffae` after 14 checks passed. The separate local integration base is `683924d`; a full Core run passed 4,047 tests with 0 failures and 3 skipped (4,050 total) before the final edition cover/link fix, followed by a 5/5 current importer fixture. A self-contained Linux x64 artifact converted the populated synthetic fixture on the isolated VM; the opt-in Chromium run passed 3/3 on an earlier snapshot. Seven BookLore proxy tests and one explicit live BookLore v2.4.0 upload-contract test passed; focused runs also cover conversion accounting, migration safety, metadata/ranking/series, rename/path, and TagLib. | Run hosted Windows validation on the final local integration tree. Real-user database compatibility, full semantic parity, representative M4B coverage, and BookLore processing of a valid production book remain unproven. |
| ChaptarrNG maintained and active features | The `24b340f` backlog snapshot was historically 317 commits ahead and 4 behind main at `660cc03`, across 703 paths. PR #76 later merged the backlog as `b2827c7a`; PR #77 is open for the receipt-fingerprint correction. | Every released and unreleased capability remains an individual ChaptarrNG-to-upstream blocker; see the itemized table linked above. |
| Bookshelf database compatibility | The uncommitted Chaptarr integration tree has a v158 SQLite importer in the full startup migration path. Five coordinator tests and the populated importer fixture pass; the self-contained Linux artifact converted the synthetic source through normal startup, retained all 39 source table definitions and rows, and promoted a v119 database with clean integrity/FK checks. A second startup preserved row counts. | Only the exact migration-158 SQLite schema is supported. Real user databases, every provider/configuration contract, first-login hash upgrade, source numeric-ID client compatibility, PostgreSQL, and release/channel bridges remain unproven. |
| Candidate runtime and SeerrNG | The self-contained Linux x64 Release artifact included the production UI and updater. On the isolated `agent-gui` VM it converted the populated fixture, returned `OK` from `/ping`, served `/`, JavaScript and CSS with HTTP 200, and listened only on `127.0.0.1`. The retained backup matched all 39 source table definitions and rows; the target had 79 tables, `integrity_check=ok`, no foreign-key violations, and restarted without duplicating records. SeerrNG PR #203 at `dc6fe6e` is merged into its `main` at `97aa148`; its full hosted checks passed, with image/deployment jobs skipped for the PR. | The fixture is synthetic; no real-user populated-library request, identity, history, or availability probe has run. The VM smoke did not build the complete production container image. |
| Frontend build and static checks | `yarn typecheck` and the production webpack bundle pass; targeted ESLint reports no errors in changed JavaScript files. The bundle emitted 18 CSS-order warnings. Whole-tree ESLint reports 862 errors and 17 warnings across the inherited frontend tree. | Keep the inherited lint debt visible; resolve any candidate-caused lint error before merge. |
| Cross-project secrets | All three repositories ignore `.env`; BookshelfNG and SeerrNG have local ignored, untracked `.env` files, while this ChaptarrNG worktree has no `.env` file. No `.env` or `.lic` file is tracked. BookshelfNG's Docker ignore excludes `.env`/`.env.*`, the SixLabors license, and signing files while retaining `.env.example`; a disposable Docker build-context check confirmed `.env.example` stayed in the context and `.env` did not. The license file remains outside repository trees. | Keep Git and Docker-context checks in release validation; no secret may enter a commit, build log, or published artifact. |
| Hosted PR checks | BookshelfNG PR #112 merged as `7f7e07f0` with 10 successful checks and 4 skipped. ChaptarrNG PR #73 merged as `5d8fffae` with 14 successful checks. PR #76 merged as `b2827c7a` with 13 successful checks and one receipt-reconciliation failure caused by frontend-generated CSS declarations changing the source fingerprint. ChaptarrNG PR #77 moves that build after receipt export; exact-head hosted checks are pending. SeerrNG PR #203 at `dc6fe6e` merged as `97aa148` after its final hosted checks passed; image/deployment jobs were skipped. | Complete PR #77's exact-head hosted validation. Run hosted Windows on the final local Chaptarr integration tree. PR #74's YunoHost removal does not supply a tested BookshelfNG compatibility bridge. |
| Distribution and migration | The channel-by-channel bridge plan covers registries, Unraid, apt/PPA, RPM/COPR, AUR, Chocolatey, Windows, archives, AppImage, Flatpak, Helm, YunoHost, and catalog packages. A local converter candidate exists but is not released. | No legacy image/package bridge is published or tested. Pinned, offline, manual, and updater-disabled installs cannot be silently redirected; the Readarr-owned updater endpoint is outside Snapetech control. |
| Release decisions | The BookshelfNG enhanced feature set blocks BookshelfNG retirement as a whole and row by row. The later ChaptarrNG gate includes that retained set plus every ChaptarrNG maintained and actively developed capability, including unpublished work; each channel is a separate blocker too. | Current evidence does not support a main merge that claims parity, BookshelfNG retirement, or release redirection. |
