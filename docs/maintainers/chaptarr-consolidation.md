# BookshelfNG retirement and ChaptarrNG consolidation

Status: investigation and implementation in progress; **not safe to redirect releases**.
Date: 2026-10-12. AI-assisted investigation and implementation by Codex.
Confidence: high for cited source findings; moderate for the implementation plan;
unknown for end-to-end migration until the matrix below passes.

The pins below identify the exact source and candidate revisions used for the
current comparison and Linux proof. They describe a tested candidate, not a
released converter or a retirement-ready transition.

## Pinned evidence and preservation

- BookshelfNG source: `f3183f8f0d2a2b09811243ab6d0a85932cff5f1a`, branch
  `codex/bookshelf-chaptarr-consolidation-20261012`. It includes the current
  BookshelfNG `origin/main` merge at `5cdb0a95b02040ede4ea74e5ce8b5645ade19d90`.
  The report and audit tools are committed at this source pin; this report's
  evidence refresh is a follow-up documentation commit.
- ChaptarrNG product candidate: `4582c13317d0d0c4574e2f968a3e78f9baa96821`,
  branch `codex/bookshelf-consolidation-final-20261012`. It includes the merge
  of ChaptarrNG `origin/main` at `a6be38dd5551b513b22e2efd4504a5ee3e73895b`
  and the task commit with six product files, eight Core test fixtures, and two
  docs/readmes. A later docs-only count refresh is committed at `af3be47`.
  The executable and tests below were built from this product candidate.
- SeerrNG: `22a73b78cc30facab29259ee6462a0cf7a6215b6`, branch
  `codex/library-stale-availability-20261012`, open PR [#203](https://github.com/snapetech/seerrng/pull/203);
  `origin/main` is `0701b65d972822952bf2c360ed96d1d20cdd7042`. Its hosted
  validation is pending. Focused post-merge Node tests passed 38/38. A later
  VM Compose smoke against the unpublished ChaptarrNG worktree passed
  capability discovery, an empty paged-library read, restricted-key access,
  denial of admin/unrelated command routes, and global-key admin access.
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
  maintenance. At the pinned revisions it contains 386 commits (377 absent
  from Bookshelf's upstream history) and 1,034 net-changed paths: 335 different
  mapped files, 679 paths without a mapped target, 14 identical files, four
  text-equivalent files after branding/newline normalization, and two deleted
  source paths. These are path-level review states, not feature-parity counts.
- The consolidation initiative memory page was updated with the cumulative
  retirement rule. Relevant architecture and feature pages still returned
  `Generating content...`; no repository or migration claims here are derived
  from those placeholders.

Regenerate the tracked-source inventory with:

```sh
python3 scripts/audit-chaptarr-consolidation.py \
  --chaptarr /path/to/chaptarrng-candidate \
  --source f3183f8f0d2a2b09811243ab6d0a85932cff5f1a \
  --target 4582c13317d0d0c4574e2f968a3e78f9baa96821 \
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

## Database conversion contract — required, not implemented

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

Chaptarr's app-folder resolver prefers `chaptarr.db`, then opens an existing
`readarr.db` or `audioarr.db` when the new filename is absent. Its main
migration controller runs the lineage guard before numbered migrations, so a
Bookshelf install is rejected before schema mutation. A completed converter
can stage and verify a new `chaptarr.db` beside the preserved source; Chaptarr
will prefer the native file on its next start. This startup-path behavior is
proven by code inspection; successful populated conversion is still pending.

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
| BookLore BookDrop connection | Ported in the candidate; proxy, settings, streaming, and schema-lineage fixtures are present | **Open blocker — stored configuration and service probe pending** | Current full Chaptarr Core suite passes; convert stored Bookshelf notification settings and verify an upload and recovery path against a disposable service. |
| Calibre, MyAnonamouse, Audiobookshelf sidecars, and other built-in integrations | Some have related target behavior; full semantic coverage is not established | **Open blocker — each integration must be dispositioned** | Test each connector's saved settings, identifiers, API behavior, generated metadata, and error handling. |
| Previewable single/bulk media moves and extra-file handling | Folder and colocation models differ | **Open blocker — workflow parity unproven** | Preserve preview, collision handling, cross-device behavior, and safeguards for unregistered/external files. |
| Optional diagnostics assembly | No corresponding opt-in module found | **Open blocker — preserve or replace** | Keep separate installation, explicit opt-in, and aggregate-only export behavior; migration must never enable it automatically. |
| Restricted service key, query-key policy, trusted proxies, body/rate limits | Chaptarr has its own service-key and facade policies | **Open blocker — aliases and permissions unproven** | Translate legacy settings without weakening configured restrictions; preserve key handling, authentication, and proxy behavior. |
| Encrypted backups and format-scoped profiles | Target encrypted backup support and native profile models exist | **Open blocker — old-data recovery unproven** | Test Bookshelf archive restore where supported, secret aliases, profile conversion, and rollback; never log credentials. |
| .NET 10, platform builds, ImageSharp removal, and security/dependency fixes | .NET 10 is present; target has different dependencies and still uses licensed ImageSharp | **Open blocker — patch-by-patch review pending** | Review each security and dependency change; retain compatible fixes and prove supported OS/architecture builds. |
| Release notes, announcements, package sync, and validation workflow | ChaptarrNG has separate release and validation workflows | **Open blocker — legacy identities not bridged** | Preserve old package/container IDs through tested compatibility artifacts; complete required per-repository validation without duplicate publication. |
| Every remaining fork change in the pinned source inventory | 386 reachable post-fork commits and 1,034 net-changed paths are recorded | **Open blocker — exhaustive disposition pending** | Mark every path retained, ported, proven equivalent, or explicitly retired after impact review. |

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

| Check | Result |
| --- | --- |
| Repository identity, dirty status, upstream parent and release list | Inspected; pinned above |
| Complete reachable fork commit and net path enumeration | Generated; semantic review still pending |
| Existing database/app/API source compatibility | Investigated; incompatible schema and upstream-owned updater confirmed |
| Published BookshelfNG source fixtures | Released `main-v0.4.21.69` Linux x64 archive SHA-256 `6ff5613524c34719820b2c1805079c5c08c1fe785a678b2a2dda0a1401a280c6`; the real binary started in Hardcover and Softcover modes and created integrity-checked empty databases. Their SHA-256 values are Hardcover `1b170993945f096457c0610014e638ebe5b2f9e4757748f1aeeb09a445663610` and Softcover `22b7d8e581b439302b47a9d9d9ce447877239a5efe97f8c7e353f20716c37418`. Both have 46 migration rows, ending at 158 with 34 absent. The generator's `--populate-bookshelf` run added linked synthetic rows; SQLite integrity and foreign-key checks passed, and the released API returned the seeded author plus book. |
| ChaptarrNG product build | The product candidate at `4582c13` published on `kspls0` with the workflow-pinned .NET SDK 10.0.401. The Linux x64 apphost SHA-256 is `dfdaae95b9cbd6a4cfe44cfe042f7e6ef87ca60402be00fa8376dc1d9fea1194`; the rebuilt `Chaptarr.dll` is `bc47fa2a4586569825839367fe3af4aaab7b1ea4377905ed55ab81fc93d550d9`, and `Chaptarr.Core.dll` is `68b891404a16247140de7cb1e1a3d098d5b3efb3b5cf0e3fdc8c684f2db1ac8e`. The disposable copy omitted `.git`, producing expected SourceLink warnings. |
| ChaptarrNG startup and lineage guard | The pinned product build started with a fresh task-scoped data path and migrated through version 114. The later unpublished worktree was published on `kspls0`, answered `/ping` with HTTP 200, created `chaptarr.db`, migrated through version 115, and passed `PRAGMA integrity_check`. Against a populated database generated by the released `main-v0.4.21.69` BookshelfNG binary, the candidate emitted the lineage error before any SQLite migration, created no `chaptarr.db`, and left source SHA-256 `09b495e49b586550bae1b5570671854c7d6f98732adbea2fd06640dd7d915187` unchanged. The guard probe stopped the process after 35 seconds (timeout exit 124); this proves fail-closed behavior, not conversion. |
| ChaptarrNG Core tests | At the pinned product revision `4582c13`, the full Linux run passed **3,956, failed 0, skipped 0** in 9m57s; its TRX result was retained in task scratch. The later unpublished working tree, including migration 115 and weighted edition/preferred-series work, passed **3,966, failed 0, skipped 3** (3,969 total) in 11m24s on `kspls0`; the 36 focused preference, API, migration, and matching tests also passed. The VM build used .NET SDK 10.0.112 and `AllowMissingPrunePackageData=true` after restore reported NETSDK1226 for missing pruning metadata. Core tests do not prove parity, populated conversion, or release-channel continuity. |
| ChaptarrNG candidate image and SeerrNG smoke | The unpublished candidate built on `kspls0` as image `sha256:18e2f2d6e6526b7ad3a827866405a4608d72f4b5dabacc138b13226008150e9d` (2,240,669,074 bytes). A disposable Compose smoke passed capability discovery, an empty paged-library read, restricted-key access, denial of admin/unrelated command routes, and global-key admin access. It proves the container and current SeerrNG contract start together, not populated Bookshelf identity/request/history continuity. |
| `.env` and license handling | BookshelfNG's root `.gitignore` excludes `.env`; no `.env` file is tracked, and the safe Coop Cloud `.env.sample` remains tracked. SeerrNG's example environment file remains tracked while local environment files are ignored. The SixLabors Community license is a required build input and stays outside Git-tracked source; builds receive it through protected local or CI configuration. Any temporary copy is limited to task-scoped scratch and removed during cleanup. No license file or `.env` is committed. |
| Accidental default-path launch and cleanup | An initial smoke command used unsupported `--version`, which started the app at its default `~/.config/Chaptarr` path. The process was stopped; directory birth and file timestamps showed that the entire 1.8 MB directory was created during that run, and no process referenced it. The task-created directory was removed. All later runs used an explicit disposable data path. |
| SeerrNG validation | Focused post-merge Node tests passed 38/38, and the release-note preview completed. A disposable VM Compose stack built the unpublished ChaptarrNG candidate and passed SeerrNG capability discovery, a zero-book paged-library response, restricted-key authorization, denial of `/config/host` and unrelated `/command`, and global-key `/config/host` access; Compose removed its test containers, network, and volume. This uses an empty Chaptarr database and does not prove populated Bookshelf identity/request continuity. Hosted Mode 2 validation for PR #203 is pending; no full hosted pass is claimed. |
| Hosted repository gates | BookshelfNG PR #112, ChaptarrNG PR #73, and SeerrNG PR #203 are open; their required hosted checks are pending. No main merge is claimed. |
| Distribution upgrade tests | Not run; compatibility converter and legacy launchers are not implemented |
| Populated BookshelfNG library conversion | Not implemented or tested |
| SeerrNG service contract probes | Not run |
| Final validation / main merges / release redirection | Not complete; PR checks and all migration/channel gates remain open |
