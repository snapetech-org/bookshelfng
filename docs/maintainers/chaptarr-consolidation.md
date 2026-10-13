# BookshelfNG retirement and ChaptarrNG consolidation

Status: investigation and implementation in progress; **not safe to redirect releases**.
Date: 2026-10-13. AI-assisted investigation and implementation by Codex.
Confidence: high for cited source findings; moderate for the implementation plan;
unknown for end-to-end migration until the matrix below passes.

The pins below identify the exact source and candidate revisions used for the
current comparison and Linux proof. They describe a tested candidate, not a
released converter or a retirement-ready transition.

## Pinned evidence and preservation

- BookshelfNG source: `102de16fe60e60eb94e6b599a826fe0779b02286`, branch
  `codex/bookshelf-chaptarr-consolidation-20261012`. At this snapshot the
  branch is 20 commits ahead and zero behind BookshelfNG `origin/main` at
  `ace06bc2766d26c8c5951563dd22679a486870bb`.
- ChaptarrNG product candidate: `6fa426ca8461e28ac343a111939108c7a04b794c`,
  branch `codex/bookshelf-consolidation-final-20261012`, draft PR [#73](https://github.com/snapetech/chaptarrng/pull/73). It is based on ChaptarrNG
  `main` at `a6be38dd5551b513b22e2efd4504a5ee3e73895b` and contains the
  metadata-profile, weighted-edition, preferred-series, and migration-115
  port. The hosted candidate `4bb1dd514435af06aa7a57c0e363329041fd853a`
  passed Linux Core with 3,972 passed and 0 failed, but its Windows Core run
  failed three path-sensitive rename tests. The local integration now uses
  OS-rooted test paths and normalized disk/event expectations; 29 rename and
  path-portability tests pass locally. The full integrated Linux Core suite
  passed 4,026 tests with 0 failures and 3 skips. A fresh hosted Windows run is
  still required; PR #73 remains a draft.
- ChaptarrNG feature snapshot: `24b340fffc43eb0883995a21665d3d051eb66abe`,
  317 commits ahead and 1 behind `origin/main` at
  `02d38e1`, with 703 changed paths. Main now includes merged CI PR #69. The
  maintained backlog includes all unreleased ChaptarrNG features and is
  separate from PR #73. Open PR #71 adds maintainer guidance; PR #72 adds
  Indonesian and Traditional Chinese language choices, AudioBookShelf mapping
  and audiobook-mode translations, and locale direction metadata; PR #74
  proposes removing YunoHost publishing.
  ChaptarrNG's itemized cumulative blocker table is in its
  [fork feature guide](https://github.com/snapetech/chaptarrng/blob/main/docs/FORK_FEATURES.md#itemized-active-and-unreleased-chaptarrng-blockers).
- SeerrNG: `1b6b31b6d0977934abf0691912059ca5ccfc21df`, branch
  `codex/library-stale-availability-20261012`, open PR [#203](https://github.com/snapetech/seerrng/pull/203);
  `origin/main` is `0701b65d972822952bf2c360ed96d1d20cdd7042` and the branch
  is 15 commits ahead with no local-behind commits. The affected component
  tests and `pnpm build:all` passed. Full hosted validation passed on code head
  `6ac0be1`; later changes only update retirement documentation and pass local
  formatting. The current title, label, and GitGuardian checks are queued or
  in progress. Its VM smoke used an empty Chaptarr library, so it does not prove
  populated Bookshelf identity, request, or history continuity.
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
  `bde894431`, and every net-changed path. It includes upstream merges and
  maintenance. At the pinned revisions it contains 402 commits (393 absent
  from Bookshelf's upstream history) and 1,036 net-changed paths compared with
  the PR #73 candidate: 336 different mapped files, 681 paths without a mapped
  target, 13 identical files, four text-equivalent files after branding/newline
  normalization, and two deleted source paths. These are path-level review
  states, not feature-parity counts.

Regenerate the tracked-source inventory with:

```sh
python3 scripts/audit-chaptarr-consolidation.py \
  --chaptarr /path/to/chaptarrng-candidate \
  --source 102de16fe60e60eb94e6b599a826fe0779b02286 \
  --target 6fa426ca8461e28ac343a111939108c7a04b794c \
  --output docs/maintainers/chaptarr-consolidation-inventory.json
```

## Hard compatibility boundaries

1. **Database migrations are unrelated.** BookshelfNG has 46 migration
   classes whose version attributes range from 1 through 158. Chaptarr has its
   own rebased schema and migration history (113 classes, versions 1 through
   114, with version 103 absent). Never copy `VersionInfo` into a Chaptarr
   database or run its numbered migrations against BookshelfNG's schema.
2. **Filename detection is not schema conversion.** Chaptarr's
   `PathExtensions.GetDatabase()` accepts `readarr.db` and `audioarr.db` when
   `chaptarr.db` is absent. Its restoration validator rejects databases without
   the Chaptarr dual-root columns. Startup needs a lineage check before any
   migration or maintenance modifies an old database.
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

The coordinator is currently SQLite-only. PostgreSQL import, configuration
conversion, and automatic discovery of a Bookshelf data directory are not
implemented. Its small unit fixture uses synthetic tables and a synthetic
import callback; it does not validate any of the table dispositions above.

The first-pass disposition below names every table in the released `.69`
schema. These are conversion requirements, not proof that the converter exists;
each mapping remains open until populated fixtures exercise it.

| BookshelfNG source tables | Proposed ChaptarrNG disposition | Required checks |
| --- | --- | --- |
| `AuthorMetadata` | Transform into native `Authors` metadata and provider identity columns | Preserve all populated metadata and qualify provider IDs; retain ambiguous identities for review. |
| `Authors` | Transform into native `Authors`, joining `AuthorMetadata` and translating common and format-specific paths, profiles, monitoring, tags, and add options | Preserve local identity aliases and both format settings independently. |
| `Books`, `Editions` | Transform into media-specific native `Books` and `Editions`; split one source book when ebook and audiobook state differs | Preserve every ISBN/ASIN, provider ID, edition property and monitored state; map source book and edition IDs to all target rows. |
| `Series`, `SeriesBookLink` | Transform into native `Series` and duplicate links only where a source book splits across media | Preserve series identifiers, primary status, positions and ordering without duplicate logical links. |
| `BookFiles`, `ExtraFiles`, `MetadataFiles` | Preserve file paths and metadata while remapping author, book, edition and file foreign keys | Confirm every path/size/timestamp/part and Calibre reference; never move or delete media. |
| `Users` | Preserve username, identifier and legacy password hash in native `Users` | Prove legacy login and one-time salted-hash upgrade; never copy fixture or production credentials into logs. |
| `Config` | Transform with explicit key aliases and native precedence | Account for every key, secret-bearing setting, URL base, port, TLS, proxy and environment alias; fail on unknown security-sensitive keys. |
| `QualityProfiles`, `MetadataProfiles`, `QualityDefinitions`, `NamingConfig`, `RootFolders`, `Tags` | Transform into native profiles, roots, naming and tags; derive per-format settings from the source's shared values and overrides | Preserve cutoffs, formats, language, naming, Calibre settings and fallback behavior; add support or halt if preferred terms/series cannot be represented. |
| `CustomFilters`, `CustomFormats`, `DelayProfiles`, `ReleaseProfiles`, `RemotePathMappings`, `Indexers`, `DownloadClients`, `Metadata`, `Notifications`, `ImportLists` | Transform settings/contracts and foreign keys into native integration tables | Preserve enablement, tags, priorities, credentials, protocol/category and trigger behavior; unknown contracts must be reported, not dropped. |
| `Blocklist`, `History`, `DownloadHistory`, `PendingReleases`, `ImportListExclusions` | Preserve user-visible history and pending work with target identity mapping | Preserve event meaning and provider/book references; validate pending rows before allowing acquisition to resume. |
| `Commands`, `ScheduledTasks`, `DownloadClientStatus`, `IndexerStatus`, `ImportListStatus`, `NotificationStatus`, `VersionInfo` | Deliberately reset transient queues/health/task state and rebuild target migration history | Never copy source commands or migration versions; let Chaptarr initialize its own scheduled tasks and schema. |

The released `.69` SQLite schema is not a table-for-table copy. It has 39
tables; Chaptarr has 78. Bookshelf stores creator data in `Authors` plus a
separate `AuthorMetadata` table and links `Books` through `AuthorMetadataId`
and `ForeignBookId`. Chaptarr folds provider metadata into `Authors` and uses
media-scoped `Books`/`Editions` relationships. A row copy or table rename
cannot preserve those relationships; conversion needs explicit entity and
foreign-key maps.

ChaptarrNG now has a staging coordinator that snapshots a file-backed source,
migrates a separate target, invokes an importer, validates SQLite integrity,
and only then promotes the target while retaining a source backup. Synthetic
unit tests cover successful promotion and importer-failure rollback. This is
coordinator plumbing only: no Bookshelf row importer is implemented, the
coordinator is not wired into startup, and no populated conversion has passed.
The tests do not establish configuration, identity, or feature parity.

Several target-model gaps are already concrete and must be resolved before
the converter can claim complete data preservation:

- One Bookshelf `Books` row can have audiobook and ebook editions. Chaptarr
  stores a media type on each book row, so conversion can produce multiple
  target book IDs for one source ID. Every dependent edition, file, series
  link, blocklist entry, history item, and legacy API ID needs an explicit
  one-to-many alias; choosing one target row silently loses a format.
- Bookshelf `DownloadHistory` is author/download-scoped and has no `BookId`,
  while Chaptarr's column is non-null. Chaptarr already uses `BookId = 0` when
  an event has no known book, so the converter can preserve these rows without
  inventing a book association: remap `AuthorId`, retain the source event,
  download ID, release, date, and data, and use the existing no-book sentinel.
  Test replay/deduplication semantics and ID normalization with imported rows.
  This internal `DownloadHistory` state is separate from the user-visible
  `History` table/API, whose book, edition, author, and event references need
  their own conversion and one-to-many alias rules.
- Bookshelf blocklist rows use local `AuthorId` and `BookIds`; Chaptarr's
  blocklist stores provider-qualified IDs and deliberately excludes local IDs
  to avoid collisions. Rows without a resolvable provider identity need a
  stable, collision-safe legacy identity representation and matching rules;
  they cannot be dropped or matched by title alone.
- The BookshelfNG `ExtraFile` model declares `BookFileId` nullable, but its
  database migration creates `ExtraFiles.BookFileId` as `NOT NULL`; the
  generated `.69` database has the same constraint. Do not infer persisted
  nullability from the model. `MetadataFiles.BookFileId` is separately
  nullable in both schemas. Because the source `ExtraFiles` table has no
  foreign-key constraint, conversion must still detect references to missing
  `BookFiles` rows and preserve them through a semantically correct target
  representation or an explicit schema change; assigning an unrelated book
  file is invalid.

These are implementation gates, not cleanup details. Add populated fixtures
for dual-format books, author-level download history, unresolved blocklist
identities, and unassociated extra files before enabling automatic promotion.

Chaptarr's app-folder resolver prefers `chaptarr.db`, then opens an existing
`readarr.db` or `audioarr.db` when the new filename is absent. Its main
migration controller runs the lineage guard before numbered migrations, so a
Bookshelf install is rejected before schema mutation. The coordinator stages a
native database beside its input, retains the source as a backup, and promotes
the native database at the input path. Startup does not call the coordinator,
and it does not yet select `readarr.db` when an empty `chaptarr.db` already
exists. Successful populated conversion is still pending.

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
ChaptarrNG retirement as a whole, with each capability and channel tracked as
an individual gate. The combined matrix is maintained in the ChaptarrNG
[fork feature guide](https://github.com/snapetech/chaptarrng/blob/main/docs/FORK_FEATURES.md#chaptarrng-retirement-blockers).

The current ChaptarrNG scope includes work outside `main`: the maintained
backlog snapshot `24b340f` is 317 commits ahead of and 1 behind
`origin/main` at `02d38e1`, across 703 changed paths. Main now includes merged
CI PR #69. Open PRs include #71 (maintainer guidance), #72 (localization),
draft #73 (BookshelfNG metadata preferences), and #74 (proposed YunoHost
removal). The active capabilities, open feature work, proposed channel changes,
and acceptance evidence are listed in the ChaptarrNG
[itemized cumulative blocker matrix](https://github.com/snapetech/chaptarrng/blob/main/docs/FORK_FEATURES.md#itemized-active-and-unreleased-chaptarrng-blockers).
Draft PR #73's metadata-preference port is on a separate branch and remains an
individual blocker. Those active capabilities count before merge or release.

| BookshelfNG capability or change | ChaptarrNG candidate finding | Retirement status | Required disposition and evidence |
| --- | --- | --- | --- |
| Rich book lookup; SeerrNG capabilities; paged books; format availability | Capability resource and Readarr facade exist | **Open blocker — integration parity unproven** | Test unchanged SeerrNG settings, IDs, keys, requests, pending work, and availability links against the exact candidate. |
| Native Hardcover, pacing, retry headers, author reuse, and refresh-age policy | Native Hardcover and V5 metadata implementations exist in a different provider pipeline | **Open blocker — semantic parity unproven** | Compare cache lifetime, key isolation, batching, 429 handling, refresh rules, and identity routing; retain configured behavior. |
| Supplemental catalogs: Open Library, Google Books, LOC, Gutendex, Internet Archive, NDL, Europeana, and Apify; per-field preferences | Provider-ID columns exist, but the BookshelfNG adapter and settings set is not present | **Open blocker — port or replace** | Preserve adapters, source selection/fallback, qualified IDs, field choices, and provider-specific request constraints. |
| Cross-catalog unmapped recovery; normalized title and identifier matching | FTS and matching architectures differ | **Open blocker — behavioral cases unproven** | Port the cases rather than the old engine wholesale; retain no-false-match, ambiguity, and no-delete constraints. |
| Multiple ebook/audio formats; per-format folders and profile overrides | Native media-specific models, roots, and profiles exist | **Open blocker — conversion and isolation unproven** | Convert all rows and references; verify fallback rules, sibling-format isolation, monitoring, imports, upgrades, scans, and renames. |
| Weighted edition terms, preferred series, narrator evidence, and publisher/dramatized cases | The consolidation branch adds profile-based weighted edition scoring and preferred-series selection for filenames, ebook tags, Calibre, and AudioBookShelf metadata; Chaptarr's stronger match evidence stays ahead of the preference signal | **Partial candidate port; retirement blocker remains open** | Preserve weights, series choices, missing-evidence neutrality, tie behavior, and manual-review boundaries; verify the full Bookshelf edge-case set after profile/database conversion. |
| Optional M4B merge, chapters, part order, and completion state | Native conversion and multipart handling exist | **Open blocker — media parity unproven** | Map opt-in policy; test chapter offsets and preservation, ordering, metadata, source retention, and failure recovery. |
| Vendored TagLibSharp patch (253 changed source paths; byte-preserving MPEG-4 `chpl` handling) | Chaptarr uses the `TagLibSharp-Lidarr` package | **Open blocker — patch behavior unreviewed** | Compare the exact fork patch and package version; prove chapter preservation on representative M4B files before selecting a native patch or dependency update. |
| Existing-torrent adoption and seeding preservation | Native continuation/adoption work exists | **Open blocker — edge cases unproven** | Test same-category and wrong-category cases, seeding-data preservation, and completed-download import. |
| Direct Download and browser-assisted grab | Native direct-download implementation and fixtures exist | **Open blocker — settings and recovery parity unproven** | Map settings and durable transfer state; test ordered URLs, interrupted recovery, architecture limits, and redirect/private-network safety. |
| BookLore BookDrop connection | Ported in PR #73; proxy, settings, streaming, and schema-lineage fixtures are present | **Open blocker — stored configuration and service probe pending** | The full Linux Core suite passes on the candidate; convert stored Bookshelf notification settings and verify an upload and recovery path against a disposable service. |
| Calibre, MyAnonamouse, Audiobookshelf sidecars, and other built-in integrations | Some have related target behavior; full semantic coverage is not established | **Open blocker — each integration must be dispositioned** | Test each connector's saved settings, identifiers, API behavior, generated metadata, and error handling. |
| Previewable single/bulk media moves and extra-file handling | Folder and colocation models differ | **Open blocker — workflow parity unproven** | Preserve preview, collision handling, cross-device behavior, and safeguards for unregistered/external files. |
| Optional diagnostics assembly | No corresponding opt-in module found | **Open blocker — preserve or replace** | Keep separate installation, explicit opt-in, and aggregate-only export behavior; migration must never enable it automatically. |
| Restricted service key, query-key policy, trusted proxies, body/rate limits | Chaptarr has its own service-key and facade policies | **Open blocker — aliases and permissions unproven** | Translate legacy settings without weakening configured restrictions; preserve key handling, authentication, and proxy behavior. |
| Encrypted backups and format-scoped profiles | Target encrypted backup support and native profile models exist | **Open blocker — old-data recovery unproven** | Test Bookshelf archive restore where supported, secret aliases, profile conversion, and rollback; never log credentials. |
| .NET 10, platform builds, ImageSharp removal, and security/dependency fixes | .NET 10 is present; target has different dependencies and still uses licensed ImageSharp | **Open blocker — patch-by-patch review pending** | Review each security and dependency change; retain compatible fixes and prove supported OS/architecture builds. |
| Release notes, announcements, package sync, and validation workflow | ChaptarrNG has separate release and validation workflows | **Open blocker — legacy identities not bridged** | Preserve old package/container IDs through tested compatibility artifacts; complete required per-repository validation without duplicate publication. |
| Every remaining fork change in the pinned source inventory | 402 reachable post-fork commits and 1,036 net-changed paths are recorded | **Open blocker — exhaustive disposition pending** | Mark every path retained, ported, proven equivalent, or explicitly retired after impact review. |

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

**Current state: plan only.** No BookshelfNG compatibility image, package,
installer, or data converter has been published or tested. There is no single
server-side redirect that reaches every installed copy: the old updater checks
the Readarr-owned service, and fixed tags/digests, offline hosts, manual
archives, and disabled updaters need an explicit update action. Each channel
needs its own tested bridge while retaining its existing identity.

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
| BookshelfNG source inventory | Source `102de16` compared with the PR #73 candidate `6fa426c`: 402 reachable commits, 393 absent from upstream history, and 1,036 changed paths. The generated inventory categorizes every path. | Path classification is not feature equivalence; review and disposition every path. |
| ChaptarrNG Bookshelf feature port | PR #73 at `6fa426c` passes hosted Linux Core with 3,972 passed and 0 failed. Its hosted Windows Core run failed three path-sensitive rename tests. The local integrated tree now normalizes OS-rooted fixture paths and filesystem/event expectations; 29 rename and path-portability tests pass locally. The full integrated Linux Core suite passed 4,026, with 0 failures and 3 skips. | Run hosted Windows again on the corrected integration tree; keep the PR a draft until that and review pass. No full semantic parity or populated-data conversion is proven. |
| ChaptarrNG maintained and active features | The separate `codex/upstream-backlog-20261012` snapshot at `24b340f` is 317 commits ahead and 1 behind `origin/main` at `02d38e1`, across 703 paths. PR #69 has since merged into main. The local integrated Linux Core suite passed 4,026, with 0 failures and 3 skips; migration-lineage reconciliation passed 2/2. | Every released and unreleased capability remains an individual ChaptarrNG-to-upstream blocker; see the itemized table linked above. |
| Bookshelf database compatibility | A populated synthetic Bookshelf database was rejected by the Chaptarr lineage guard before numbered migrations and its source bytes remained unchanged. The new SQLite staging coordinator passes synthetic promotion and import-failure rollback unit tests. | The row importer, startup wiring, configuration/identity/reference mapping, PostgreSQL path, and populated conversion proof are not implemented. |
| Candidate runtime and SeerrNG | An earlier ancestor candidate started with a fresh database and passed an empty-library SeerrNG capability/key smoke. SeerrNG PR #203 passed local and full hosted validation on its preceding code head; subsequent documentation-only commits passed local formatting. | No latest-candidate populated-library request, identity, history, or availability probe has run. |
| Cross-project secrets | Root `.env` is ignored and untracked in BookshelfNG, ChaptarrNG, and SeerrNG. The SixLabors license remains in `~/Downloads` outside all repository trees. ChaptarrNG reads its value from `SIXLABORS_LICENSE_KEY` and passes it to ImageSharp as an MSBuild property. | Keep both checks in release validation; no secret may enter a commit, build log, or published artifact. |
| Hosted PR checks | BookshelfNG PR #112 at `1c0edb7` is mergeable and its build, security, package-sync, and release-note checks passed. ChaptarrNG PR #73 at `6fa426c` has passing Linux/macOS/PostgreSQL and security checks but its hosted Windows Core run failed three path tests; local fixtures are corrected and need a fresh run. PR #72 and #74 checks pass. SeerrNG PR #203 at `1b6b31b` has title/label checks passed while the validation plan remains queued; its prior code head passed full validation. | Rerun hosted Windows and SeerrNG validation after final source changes. PR #74's YunoHost removal does not supply a tested BookshelfNG compatibility bridge. |
| Distribution and migration | The channel-by-channel bridge plan covers registries, Unraid, apt/PPA, RPM/COPR, AUR, Chocolatey, Windows, archives, AppImage, Flatpak, Helm, YunoHost, and catalog packages. | No legacy image/package bridge or converter is published or tested. Pinned, offline, manual, and updater-disabled installs cannot be silently redirected; the Readarr-owned updater endpoint is outside Snapetech control. |
| Release decisions | The BookshelfNG enhanced feature set blocks BookshelfNG retirement as a whole and row by row. The later ChaptarrNG gate includes that retained set plus every ChaptarrNG maintained and actively developed capability, including unpublished work; each channel is a separate blocker too. | Current evidence does not support a main merge that claims parity, BookshelfNG retirement, or release redirection. |
