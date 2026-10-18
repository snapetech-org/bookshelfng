# BookshelfNG feature inventory and ChaptarrNG retirement matrix

**Reviewed:** 2026-10-18. **Status:** BookshelfNG `0.4.21.71` is the published
final source release, and issue #114 is closed. ChaptarrNG `v0.9.977` is the
latest public release with preview, apply, automatic startup conversion,
rollback, an embedded BookshelfNG SQLite migration chain, and a safe fallback
for books whose formats cannot be inferred. The `.977` table guard rejects
source versions before migration 14 because they still use `Blacklist`.
ChaptarrNG PR #126 merged the version-aware guard and synthetic migration-1
rollback fixture into `main`; hosted Linux, macOS, Windows, and PostgreSQL
migration checks passed. That source fix is not in `.977`, and releases are
frozen until the retirement gates close. PR #128 merged a fail-closed release
and distribution gate requiring `CHAPTARRNG_RELEASE_READY=true`; the
repository variable is unset. ChaptarrNG `.978` is a source version bump,
not a release. ChaptarrNG PR #127 merged to `main` as `b3089a39` with
supplemental catalogs, per-field preferences, and exact-identity recovery of
unmapped files. Linux, macOS, Windows, PostgreSQL migration, CodeQL,
dependency/security, and release-note checks passed on its exact head. Four
provider-dispatch findings on an earlier head were reviewed as false positives:
provider IDs select allowlisted public metadata APIs and do not grant access.
The merged source is not in public `.977`; converted-data and settings
acceptance remain open. ChaptarrNG PR #129 merged to `main` as `949ae3dd`;
its clean head `a671f4b3` passed hosted Linux, macOS, Windows, PostgreSQL
migration, CodeQL, dependency/security, and release-note checks. It ports
BookshelfNG's opt-in M4B settings, tagged track ordering and chapter titles,
original-track fallback, and move/copy source handling. A synthetic two-track
smoke using the `.977` toolchain preserved supplied chapter titles and offsets,
but did not exercise the importer end to end or representative media. The
source change remains unpublished; representative-media acceptance is open.
ChaptarrNG PR #130 merged to `main` as `9f1ae60b` with a policy mapping from
BookshelfNG's numeric `BookImportMinimumMatchPercent` to `BookMatchingStrictness`
when no explicit Chaptarr mode exists: 50–66 maps to Aggressive, 67–82 to
Balanced, and 83–99 to Strict. Explicit modes take precedence, invalid legacy
values fail closed, and the source row is preserved. The mapping is lossy
because the matching algorithms differ; converted-data acceptance remains
open, and this source change is not in public `.977`.
Neither synthetic fixtures nor hosted CI establish older-schema behavior on
real data. The verified
populated-database input is the exact BookshelfNG migration-158 SQLite schema.
The optional aggregate-only diagnostics replacement is included in `.977`;
artifact verification passed on Linux, macOS, and Windows. Migrated
opt-in/environment handling remains to be exercised on an installed system.
One populated Linux/amd64 run retained all 39 source tables and rows; 81 books
needed media classification, and the test-map choices were not reviewed as
correct. The current converter keeps unresolved records in both catalogs,
unmonitored, and writes a review file, but it does not classify them. The
final-release decision and helper do not close the feature, data, or
installation-channel acceptance gates. PostgreSQL, complete
settings/identity behavior, rollback on every real deployment, and package
handoff remain open. PostgreSQL conversion is supported by no published
ChaptarrNG release. A work-branch candidate targets one migration-158
PostgreSQL schema and has not passed hosted build or operator-data acceptance;
it remains unsupported for installations. This is a feature-level matrix, not
a claim that similarly named features are equivalent.

BookshelfNG's `BookImportMinimumMatchPercent` defaults to 70, allows 50–99,
and affects both fuzzy title parsing and import acceptance. ChaptarrNG `main`
maps 50–66 to Aggressive, 67–82 to Balanced, and 83–99 to Strict only when no
explicit `BookMatchingStrictness` is configured. Invalid legacy values fail
closed; the original `Config` row is retained; and the report identifies the
approximation. Because the algorithms differ, converted-data behavior remains
an acceptance gate; this mapping is not in public `.977`.

**Confidence:** high for the listed BookshelfNG behavior at the pinned
released source; moderate for whether ChaptarrNG contains a related
implementation; unknown for semantic equivalence until the listed acceptance
checks pass.

The path inventory pinned later in this document compares a specific
BookshelfNG source revision with a specific ChaptarrNG revision. Its counts
describe source history and changed paths, not feature parity, and do not
change as new releases are published. The current migration and channel
evidence is in the [consolidation report](chaptarr-consolidation.md); the
acceptance requirements in this matrix remain open until each item is tested.

## Retirement rule

Every capability BookshelfNG added or materially extended is a blocker to
retiring BookshelfNG until ChaptarrNG contains the behavior or a tested,
documented replacement. The set is conjunctive: closing one row does not close
the others. The whole enhanced BookshelfNG feature set blocks retirement, and
each row remains an independent blocker until its own evidence passes. A row
does not become optional because upstream documentation is silent or ChaptarrNG
has a feature with a similar name.

The default is to retain every capability. Calling a feature obsolete does not
close its blocker; any proposed removal requires an explicit maintainer
decision about the user impact.

This gate is separate from the later ChaptarrNG-to-Chaptarr gate. Once a
BookshelfNG capability is retained in the consolidated ChaptarrNG product, it
also joins ChaptarrNG's cumulative upstream-retirement blocker set. Every
ChaptarrNG feature it maintains or is actively adding—including work not yet
in a published release—joins that same set. The union blocks retirement as a
whole, with each capability, sub-capability, data path, and channel as an
individual gate. A composite row closes only when every item it covers passes
its acceptance checks. Active
ChaptarrNG branches and open feature PRs count before release; the combined
[ChaptarrNG retirement matrix](https://github.com/snapetech-org/chaptarrng/blob/main/docs/FORK_FEATURES.md#chaptarrng-retirement-blockers)
pins the current snapshot and tracks those blockers.

The prior maintained-backlog snapshot `24b340f` is historical: PRs #69–#77
have since merged. The pinned source inventories remain historical snapshots. Every open
ChaptarrNG product, maintenance, security, and dependency change counts in
the cumulative blocker set before and after merge or release and is tracked
in the ChaptarrNG matrix.

## Feature matrix

“Present” means the target code has a related implementation. It does not
close the row until behavior, data, configuration, and client compatibility
are tested. The current code-level findings and acceptance cases are recorded
in the [consolidation report](chaptarr-consolidation.md); the linked inventory
is the commit/path audit that must be fully dispositioned.

| BookshelfNG capability | BookshelfNG has | ChaptarrNG implementation has | Retirement disposition and status |
| --- | --- | --- | --- |
| One instance for ebooks and audiobooks; multiple compatible formats per book | Single book records can retain multiple ebook and audiobook files | Media-specific records exist; conversion preserves a selected edition per format and keeps unresolved records in both catalogs, unmonitored, with a review artifact; `main` upgrades recognized older SQLite schemas on a disposable copy | **Open blocker.** Publish the upgrader and validate older schemas with real data; convert and validate all rows and relationships; prove format isolation, monitoring, real-data rollback, and existing client behavior. The fallback does not infer the true format. |
| Format-specific author paths, quality profiles, and metadata profiles | Optional per-format paths and profile overrides, with author defaults as fallback | Native media roots and profiles exist; new authors receive usable per-format roots automatically | **Partial parity.** ChaptarrNG `v0.9.974+` initializes missing new-author roots from configured defaults or the only compatible root, preserves explicit roots, leaves ambiguous defaults blank, and does not move existing files. BookshelfNG `0.4.21.71` implements the optional setting requested in the now-closed issue #114. The broader blocker remains open for profile override/fallback semantics and conversion of existing path/profile data; test imports, upgrades, renames, scans, and moves for both formats. |
| Native Hardcover metadata and request controls | Direct GraphQL provider, per-process pacing/cache, batched lookups, rate-limit recovery, and identity routing | The ChaptarrNG retirement branch ports a native Hardcover GraphQL proxy, routes explicit Hardcover IDs through it, maps saved `HardcoverAuth` to `HardcoverApiToken`, and interprets bare numeric source IDs according to the active `HARDCOVER`/`HARDCOVER_NATIVE` mode. Its migration-helper candidate exposes `--provider-mode` so preview and apply use that same source mode. | **Open blocker.** Pass hosted tests and converted-data review; compare cache lifetime, key isolation, batching, 429 handling, refresh rules, settings preservation, provider selection, and identity routing. The provider and helper changes are source-only and not in published ChaptarrNG `.977` or BookshelfNG `.71`. |
| Selectable supplemental catalogs and per-field source preferences | Hardcover, Readarr-compatible API, Open Library, Google Books, LOC, Gutendex, Internet Archive, NDL, Europeana, and optional Apify adapters | ChaptarrNG main after PR #127 (`b3089a39`) includes Open Library, Google Books, LOC, Gutendex, Internet Archive, NDL, Europeana, and Apify with selectable sources, qualified identities, and per-field choices. Exact-head Linux, macOS, Windows, PostgreSQL migration, CodeQL, dependency/security, and release-note checks passed. It is not in published `.977`; Hardcover and the primary metadata API retain their separate resolvers. | **Source port merged; open blocker.** Review provider/settings migration, cached credential handling, per-field matching, fallback behavior, and converted operator data before accepting the row. |
| Cross-catalog recovery and import matching | Retry unmapped files across configured catalogs; ISBN/ASIN/provider-ID and normalized-name matching; configurable title threshold | ChaptarrNG main after PR #127 searches exact ISBN/ASIN, canonical provider IDs, Goodreads work/edition IDs, or exact normalized title and author. Candidates must match supplied identity evidence, media type, and stable work/author IDs; ambiguous or conflicting IDs stay unmatched, and accepted results queue only the existing pending-author import. It never attaches files directly. Focused tests cover exact Goodreads and canonical provider-ID lookup, mismatched IDs, conflicting tags, identifier checks, ambiguity, and title matching; exact-head hosted validation passed. PR #130 adds the lossy 50–66 Aggressive, 67–82 Balanced, and 83–99 Strict mapping when no explicit mode exists; invalid values fail closed. | **Source port merged; open blocker.** Accept identifier/name, threshold approximation, media-type, ambiguity, and pending-import behavior on converted operator data. The mapping is not algorithm-equivalent and is not in public `.977`. |
| Weighted edition terms, preferred series, and narrator-aware matching | Profile terms and series preferences; narrator tags and edition evidence affect audiobook ranking | The consolidation branch adds profile-based weighted edition scoring and preferred-series selection for filenames, ebook tags, Calibre, and AudioBookShelf metadata; stronger match evidence remains authoritative | **Partial candidate port; retirement blocker remains open.** Preserve weights and series choices, neutral handling of missing data, tie behavior, and manual-review boundaries; test the full Bookshelf edge-case set after profile/database conversion. |
| Audiobook M4B merge and chapter metadata | Opt-in multi-track merge with track ordering and chapter creation | ChaptarrNG PR #129 merged to `main` as `949ae3dd`. Its clean head passed hosted Linux, macOS, Windows, PostgreSQL migration, CodeQL, dependency/security, and release-note checks. It preserves tagged track order and chapter titles, falls back to original tracks on conversion failure, and removes sources only after successful move-mode import; copy mode retains them. A synthetic two-track smoke preserved supplied chapter titles and offsets using the `.977` toolchain, but did not exercise the importer end to end or representative media. The implementation is not in public `.977`. | **Source port merged; open blocker.** Validate chapter offsets, embedded source chapters, tags, conversion failures, source retention, and restart/resume behavior with representative media and move/copy deployments. |
| Vendored TagLibSharp MPEG-4 `chpl` handling | Patch includes byte-preserving chapter-list writes | The local Chaptarr candidate vendors this fork and passes a synthetic version-1 `chpl` fixture that checks exact atom preservation during a title write. The vendor includes its LGPL-2.1 `COPYING` file; its strong-name key matches the key already committed with the BookshelfNG vendor source. | **Local port and focused regression pass; broader compatibility remains an open blocker.** Validate representative M4B files, tag edits, conversion outputs, and failure cases; review continued use of the vendor signing identity and upstream the supported implementation. |
| Existing torrent adoption and safe seeding | Can adopt tracked torrent data without removing the seed | Native adoption/continuation work exists | **Open blocker.** Prove same-category, wrong-category, completed-download, and seeding-data preservation cases. |
| Direct Download with ordered sources and browser-assisted links | Ebook search, API-key downloads, optional browser fallback, durable transfer state, and redirect validation | A built-in direct-download implementation exists | **Open blocker.** Preserve URL order, configuration aliases, staged-state recovery, architecture limits, and redirect/private-network protections. |
| BookLore BookDrop uploads | Uploads imported books through BookLore's BookDrop API | Optional external app integration ported in the current ChaptarrNG candidate; seven proxy tests and one live BookLore v2.4.0 upload-contract test pass, including exact-byte file placement in BookDrop | **Open blocker.** Convert stored notification settings and credentials; preserve streaming, redirects, supported-format and size handling; test rejected files, recovery, and partial batches. The live contract proves API upload and file placement, not BookLore processing of a valid production book. BookLore [identifies BookOrbit as its official successor and says it is entering maintenance mode](https://github.com/booklore-app/booklore/blob/develop/README.md); test the successor path or record a legacy-user transition. |
| Calibre, MyAnonamouse, Audiobookshelf sidecars, and SeerrNG integration | These standalone service and metadata workflows are present | Some native integrations and the SeerrNG contract exist; the full set is not proven equivalent | **Open blocker.** Disposition each integration and preserve its settings, API behavior, and stored associations. |
| Previewable media moves, bulk moves, and extra-file handling | Preview, collision checks, registered sidecars, and format-aware paths | Chaptarr has different folder and organization behavior | **Open blocker.** Prove equivalent previews, collision and cross-device behavior, and that unknown/external files remain untouched. |
| Optional privacy-preserving diagnostics | Separate module, explicit opt-in, aggregate-only event schema | ChaptarrNG `v0.9.977` publishes the optional aggregate-only module; it honors the legacy enable flag only when the archived BookshelfNG plugin marker is present and requires endpoint/token environment variables to be carried forward. Artifact verification passed on Linux, macOS, and Windows. | **Replacement published; migration gate open.** Verify an installed transition with and without the archived marker, preserved environment variables, and default-off behavior; then close this feature row. |
| Scoped SeerrNG access, API aliases, proxy and request controls | Restricted key, compatibility routes, format-specific availability, and hardened proxy/auth boundaries | ChaptarrNG has its own facade and scoped key | **Open blocker.** Preserve existing permissions and configuration semantics; test unchanged SeerrNG settings, IDs, keys, and proxy deployments. |
| Encrypted backups and restore | Passphrase-protected portable archives and per-format profiles | ChaptarrNG has encrypted backup support | **Open blocker.** Prove legacy archive recovery, secret handling, rollback, and profile conversion; never expose secrets in logs. |
| .NET 10, dependency/security fixes, and platform builds | .NET 10 releases, broad native/package matrix, and maintained security/dependency patches | ChaptarrNG uses .NET 10 and has a different dependency/build matrix | **Open blocker.** Review every patch and supported platform; retain compatible fixes and run the target's required build and security checks. |
| Release, package, and update channels | Containers, Unraid, Debian/RPM, AUR, PPA, Windows, macOS/Linux/FreeBSD, AppImage, Flatpak, Chocolatey, and Helm; YunoHost publishing retired | ChaptarrNG has its own release and package identities | **Open blocker.** Preserve old channel identities with tested bridge packages/images and migration instructions; no universal automatic redirect exists. |
| All other fork changes | 540 reachable post-fork commits, 531 absent from the pinned Bookshelf lineage ref, and 1,091 net-changed paths in the refreshed inventory pinned to BookshelfNG `abc4e4fa` and ChaptarrNG `main` `9f1ae60b`, including PRs #127, #129, and #130 | Code paths differ across the two projects | **Open blocker.** Account for every inventory path as retained, ported, proven equivalent, or explicitly retired. Any proposed removal remains blocked until an explicit maintainer decision. The feature rows above do not replace this audit. |

## Evidence and limits

The [consolidation report](chaptarr-consolidation.md) records exact source and
target revisions, current implementation findings, the data-conversion
contract, release-channel matrix, test results, and open gates. The local
Release-mode Core suite passed 4,065 tests with 0 failures and 3 skipped on the
same application sources as the current integration head. Twenty-three
focused migration fixtures also passed,
including synthetic rollback after a post-migration write. The standard image passed preview,
apply, and startup against separate copies of one real populated migration-158
database; this is bounded evidence because 81 books had no derivable media
format. The published fallback allows conversion to continue without guessing,
but operators still need to review the format and monitoring intent. The separate opt-in
Chromium run passed 3/3 on an earlier candidate snapshot. The focused converter
coordinator fixture passes 5/5, and the populated importer/startup fixture
passes 5/5, including profile mapping, notification/config/user rows,
file-specific history, edition image/link metadata, narrator names, orphan-ID
reservation, restart idempotence, and safe refusal cases. A self-contained
Linux x64 artifact with the production UI and updater converted the populated
synthetic fixture on the isolated agentic VM through normal startup, reached
v119, served the root/JavaScript/CSS successfully, and restarted without
duplicating records. The retained backup matched all 39 source table
definitions and rows; the promoted database passed integrity and foreign-key
checks. Seven
BookLore proxy tests pass, and the explicit live BookLore v2.4.0
upload-contract fixture passes 1/1.
The Release console build has zero warnings or errors.
Additional focused reruns on the current candidate passed 16 migration-safety
cases, 29 metadata/ranking/series cases, 29 rename/path cases, and 6
BookLore/TagLib cases, alongside the 5 converter-coordinator cases.
The synthetic TagLib chapter-preservation fixture passed; focused
migration-lineage tests passed 2/2, and 29 rename/path-portability tests
passed. An earlier pre-release hosted Windows run at the previous PR #100 head failed
four migration/rollback tests. The validation engine now records a safe
exception type and method frame without logging error text or paths. The later
`v0.9.977` release workflow passed its Linux, macOS, and Windows build/test
jobs and verified the optional diagnostics module in each standalone artifact;
this does not
establish populated real-data conversion or rollback on Windows. Preview, explicit apply, and ordinary startup were also exercised
on separate copies of one real populated BookshelfNG migration-158 SQLite
database using the standard Linux/amd64 image. Preview left the source hash
unchanged and accounted for all 127,177 rows; apply retained a backup matching
all 39 source table definitions and every row; normal startup served the UI
and retained the existing port, URL base, API key, SSL setting, and Docker
image-pull update mechanism. The live BookshelfNG service was not changed.
The 81 media choices used for apply were test-only and were not reviewed as
correct library classifications. Real-data validation for older BookshelfNG
schemas, PostgreSQL, complete provider/settings behavior, rollback on a real
populated deployment, full feature-by-feature semantic acceptance, populated-library SeerrNG
request/identity/history probes, and tested old-channel bridges remain open.
The released BookshelfNG `.69` database samples inspected earlier were empty;
that earlier inspection is distinct from this one populated-database run.

The BookshelfNG and ChaptarrNG databases have different schemas and identity
models. The public ChaptarrNG `v0.9.977` converter handles the exact
migration-158 SQLite schema and bundles an older-schema SQLite chain. Its
table guard rejects versions before migration 14 because they use the
historical `Blacklist` name. PR #126 merged the correction and synthetic
migration-1 rollback fixture into `main`; hosted Linux, macOS, Windows, and
PostgreSQL migration checks passed, but the fix remains unpublished during the
release freeze. A populated synthetic migration-22 fixture exercises upgrade,
conversion, rollback, and non-mutating preview. Unknown schemas and provider
identities still fail closed with the source intact. The one populated
real-database rehearsal proves only the exact v158 input, not older real
databases, PostgreSQL, or other production data. A
separate 2026-10-18 Docker image-switch smoke used the published BookshelfNG `.71`
image to create an empty v158 database, converted it on ChaptarrNG `.977` startup,
and restored it with the rollback command; the old image then started on port
8787. The original database had 39 tables and passed SQLite integrity checks. This
does not validate populated operator data or the Community Apps update flow. The
converter stages a native ChaptarrNG database, validates it, retains a
Bookshelf backup, and promotes only after its row-accounting checks. The
evidence above does not prove PostgreSQL source conversion or every real-world
data shape.

Retirement also has a separate distribution gate. BookshelfNG's installed
updater checks the Readarr-owned update service, so changing Snapetech release
assets cannot redirect every existing installation. Pinned images, disabled
updaters, offline hosts, and manual archives also need an explicit upgrade
action. A channel-by-channel compatibility bridge can reduce effort, but a
frictionless automatic update for every historical install cannot be promised.
