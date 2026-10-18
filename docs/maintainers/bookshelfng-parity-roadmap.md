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
not a release. PR #127 remains an unpublished candidate for supplemental
catalogs, per-field preferences, and exact-identity recovery of unmapped files;
current-head hosted validation is pending. Neither synthetic fixtures nor
hosted CI establish older-schema behavior on real data. The verified
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
handoff remain open. This is a feature-level matrix, not a claim that
similarly named features are equivalent.

BookshelfNG's `BookImportMinimumMatchPercent` remains a separate settings
parity blocker. It defaults to 70, allows 50–99, and affects both fuzzy title
parsing and import acceptance. The converter preserves its `Config` row, but
ChaptarrNG's `BookMatchingStrictness` has different semantics; no tested
value-by-value mapping exists.

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
| Native Hardcover metadata and request controls | Direct GraphQL provider, per-process pacing/cache, batched lookups, rate-limit recovery, and identity routing | Chaptarr has a separate resolver and consensus pipeline | **Open blocker.** Keep the configured behavior and identity boundaries or provide a tested replacement; a provider name alone is not parity. |
| Selectable supplemental catalogs and per-field source preferences | Hardcover, Readarr-compatible API, Open Library, Google Books, LOC, Gutendex, Internet Archive, NDL, Europeana, and optional Apify adapters | ChaptarrNG [PR #127](https://github.com/snapetech-org/chaptarrng/pull/127) ports Open Library, Google Books, LOC, Gutendex, Internet Archive, NDL, Europeana, and Apify, with selectable sources, qualified identities, and per-field choices. It is not in published `.977`; frontend build, typecheck, focused lint, and translation checks passed on an earlier candidate. Current-head hosted validation is pending. Hardcover and the primary metadata API retain their separate resolvers. | **Candidate port; open blocker.** Complete exact-head hosted tests and review provider/settings migration, cached credential handling, per-field matching, and fallback behavior before accepting the row. |
| Cross-catalog recovery and import matching | Retry unmapped files across configured catalogs; ISBN/ASIN/provider-ID and normalized-name matching; configurable title threshold | ChaptarrNG PR #127 at `6d437113` adds a candidate fallback after local and V5 matching fail. It searches exact ISBN/ASIN, canonical provider IDs, Goodreads work/edition IDs, or exact normalized title and author. Candidates must match supplied identity evidence, media type, and stable work/author IDs; ambiguous or conflicting IDs stay unmatched, and accepted results queue only the existing pending-author import. It never attaches files directly. Focused tests cover exact Goodreads and canonical provider-ID lookup, mismatched IDs, conflicting tags, identifier checks, ambiguity, and title matching; current-head hosted validation is still pending. | **Open blocker.** Accept identifier/name, media-type, ambiguity, and pending-import behavior after exact-head CI and migration review. The local focused test cannot compile without the ImageSharp license. `BookImportMinimumMatchPercent` still has no verified mapping to `BookMatchingStrictness`. |
| Weighted edition terms, preferred series, and narrator-aware matching | Profile terms and series preferences; narrator tags and edition evidence affect audiobook ranking | The consolidation branch adds profile-based weighted edition scoring and preferred-series selection for filenames, ebook tags, Calibre, and AudioBookShelf metadata; stronger match evidence remains authoritative | **Partial candidate port; retirement blocker remains open.** Preserve weights and series choices, neutral handling of missing data, tie behavior, and manual-review boundaries; test the full Bookshelf edge-case set after profile/database conversion. |
| Audiobook M4B merge and chapter metadata | Opt-in multi-track merge with track ordering and chapter creation | Native conversion and multipart workflows exist | **Open blocker.** Verify opt-in policy, chapter offsets and source chapters, part order, tags, failure recovery, and source retention. |
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
| All other fork changes | 426 reachable post-fork commits and 1,045 net-changed paths in the inventory pinned to BookshelfNG `5d696fb0` and ChaptarrNG candidate `561bf395` | Code paths differ across the two projects | **Open blocker.** Account for every inventory path as retained, ported, proven equivalent, or explicitly retired. Any proposed removal remains blocked until an explicit maintainer decision. The feature rows above do not replace this audit. |

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
