# BookshelfNG feature inventory and ChaptarrNG retirement matrix

**Current status (2026-10-21)**

BookshelfNG `0.4.21.71` remains its final public release; ChaptarrNG `v0.9.977` remains the latest public release. ChaptarrNG `main` and application code are at [`bebc5e8a`](https://github.com/snapetech-org/chaptarrng/commit/bebc5e8a923d7ebc4af7cc86b0bbec5e93f51859). The source includes the disabled-by-default author-path setting from BookshelfNG issue [#114](https://github.com/snapetech-org/bookshelfng/issues/114), its migration support, the format-specific metadata-profile refresh fix, and the corrected Calibre English language tag. These changes remain unpublished in `.977`. Exact-head Build [39539307423](https://github.com/snapetech-org/chaptarrng/actions/runs/39539307423) is running on Linux, macOS, Windows, and PostgreSQL; preceding Build [39538783209](https://github.com/snapetech-org/chaptarrng/actions/runs/39538783209) was cancelled when the Calibre tag correction landed before its platform matrix completed. Security analysis [39539307274](https://github.com/snapetech-org/chaptarrng/actions/runs/39539307274), Semgrep [39539307245](https://github.com/snapetech-org/chaptarrng/actions/runs/39539307245), Trivy [39539307454](https://github.com/snapetech-org/chaptarrng/actions/runs/39539307454), and dependency submission [39539323460](https://github.com/snapetech-org/chaptarrng/actions/runs/39539323460) passed; CodeQL [39539307127](https://github.com/snapetech-org/chaptarrng/actions/runs/39539307127) is running. The format-profile fixture passes 5/5 locally and the Calibre language fixture 4/4; earlier focused author/migration fixtures pass 11/11 and configuration persistence 1/1. No release, tag, package, image, installer, or migration bridge has been published. Representative operator-data migration and rollback, complete feature/data acceptance, provider and SeerrNG workflows, installed update-channel handoff, and operator acceptance remain open; keep BookshelfNG in service.

The schema-v4 audit pins BookshelfNG source `2811718076d84777a1b1132e4e5d2abd21231229` to ChaptarrNG target `bebc5e8a923d7ebc4af7cc86b0bbec5e93f51859`. It covers 732 post-fork commits (723 absent from pinned upstream history) and 1,119 changed paths: 85 reviewed mappings and 681 reviewed dispositions (177 retained, 133 equivalent, 200 ported, and 171 non-runtime retirements). Another 438 paths remain open (136 without mapped targets and 302 requiring semantic review). Recent passes dispositioned backup/restore, optional diagnostics, the BookshelfNG migration controller, six historical SQLite migration paths, author refresh, book-added handling, format-scoped media moves, author profile refresh, and Calibre language compatibility using source and fixture evidence. Path-level coverage is not feature-parity proof, and no runtime retirement is approved.

Representative operator data and rollback, provider fulfillment, SeerrNG workflow coverage, representative media and restart recovery, installed update-channel handoff, and operator acceptance remain open. Keep BookshelfNG in service. Older checkpoints below are historical.

ChaptarrNG commit `29852b13` introduced BookshelfNG's explicit trusted proxy and
CORS allowlists, per-client rate limit, bounded general body size, and request-ID
response header. The restore endpoint keeps its separate 1 GiB upload limit.
The first Build at `36623faf` found compile errors in its new fixture. Follow-up
`aac32822` fixed the imports but exposed an explicit interface member; `29852b13`
corrects the assertion. Exact-head Build
[39394240337](https://github.com/snapetech-org/chaptarrng/actions/runs/39394240337)
passed Linux, macOS, Windows, PostgreSQL migrations, and native-runner receipt
reconciliation. Windows passed the installer fingerprint, service upgrade,
rollback, cleanup, and selected-data-directory checks. These controls are not in
public `.977` and do not close installed migration acceptance.

Earlier BookshelfNG main snapshot `c63eb848` passed its docs-only push, security, package-sync,
release-note, and dependency-submission checks. Unraid main `296caed2` passed CI
[39387608787](https://github.com/snapetech-org/bookshelfng-unraid/actions/runs/39387608787)
and its package-sync, security, and release-note checks. Unraid transition PR
[#5](https://github.com/snapetech-org/bookshelfng-unraid/pull/5) at `1261a9f8`
passed exact-head build, template, package-sync, dependency, release-note,
Semgrep, and Trivy checks. It remains draft pending representative-data
migration/rollback and the real Community Applications update flow; publication
jobs were skipped.

Publishing remains frozen, issue #144 remains open, and BookshelfNG must stay in
service until the remaining acceptance gates close.

Prior PR #131 validation (2026-10-19): application-code snapshot `0612cb4c90b75818e5349eb868cc0638825de02a` passed exact-head Build [39239940373](https://github.com/snapetech-org/chaptarrng/actions/runs/39239940373): Linux, macOS, and Windows tests, PostgreSQL migration smoke, native-runner receipt reconciliation, and release-note contract passed. CodeQL [39239934583](https://github.com/snapetech-org/chaptarrng/actions/runs/39239934583), security [39239940344](https://github.com/snapetech-org/chaptarrng/actions/runs/39239940344), NuGet submission [39239932165](https://github.com/snapetech-org/chaptarrng/actions/runs/39239932165), and dependency review [39239940313](https://github.com/snapetech-org/chaptarrng/actions/runs/39239940313) passed. Disposable-fork validation [39239940512](https://github.com/snapetech-org/chaptarrng/actions/runs/39239940512) was skipped by its external-fork gate. SeerrNG's adapter and request-route suite at source commit `b810153c` passed 4 files / 283 tests. The Linux artifact also passed the earlier empty-library API and authorization smoke. A populated source-build smoke for later code is recorded below.

Follow-up request lifecycle probe (2026-10-19): then-draft ChaptarrNG PR #131 commit `d97136040e5f76f6aa0b140d5c0ed74f8de7501e` added [`integration/seerrng-request-lifecycle.mjs`](https://github.com/snapetech-org/chaptarrng/blob/d97136040e5f76f6aa0b140d5c0ed74f8de7501e/integration/seerrng-request-lifecycle.mjs), wired into `integration/seerrng-smoke.compose.yml`. It passed against the prebuilt Linux candidate `0.9.978.0` from Build [39239940373](https://github.com/snapetech-org/chaptarrng/actions/runs/39239940373) (application snapshot `0612cb4c90b75818e5349eb868cc0638825de02a`) and SeerrNG source `b810153c`: the real `ReadarrAPI` adapter created, polled, and cancelled a synthetic unavailable-author import, and ChaptarrNG returned terminal `Failed` / `Cancelled by user`. `node --check`, Prettier, and Compose configuration validation passed. Both smoke scripts then passed in the isolated Compose stack with a temporary runtime image assembled from the same artifact; the checked-in Dockerfile build path was bypassed. The populated migration smoke below now also covers synthetic converted records. Successful fulfillment, retries, availability/history, unchanged production settings, and operator acceptance remain open.

Populated migration-to-SeerrNG source smoke (2026-10-19): ChaptarrNG
candidate commit `12f290bde5c04d29202775c0e9eeafb5fc20608f` built through the
checked-in `Dockerfile.build` with SeerrNG at commit `fdc439aa9`. It seeded a
synthetic migration-158 database in named disposable volumes, converted it
during normal startup, retained the source backup, and persisted
`HardcoverEnabled=true` for source mode `HARDCOVER=true`. SeerrNG's real
`ReadarrAPI` read the migrated audiobook and ebook with their Hardcover
identities. The restricted-key boundary and pending add/poll/cancel lifecycle
passed; importer tests passed 43/43. Tiny `.m4b`/`.epub` placeholders are not
valid media. A separate six-case real-tool importer check passed synthetic M4B
processing; representative M4B media and restart/resume, feature parity,
installed rollback, and channel handoff remain unaccepted.

Exact-head artifact repeat (2026-10-19): the Linux artifact from ChaptarrNG
PR #131 Build [39316535744](https://github.com/snapetech-org/chaptarrng/actions/runs/39316535744)
at docs-only head `93213b677a0bbb256aaf782c389a4f1a3d9c2ee7` passed the checked-in
SeerrNG Compose smoke against SeerrNG rebuilt at
`22f3bbc5874752b50a3b1206ca0bd3ebe0309f95`. It loaded synthetic populated
migration-158 records, verified restricted-key access to both format
libraries and denial of administrative/unrelated commands, then created,
polled, and cancelled a pending import through SeerrNG's real `ReadarrAPI`
adapter. The app artifact was copied into a temporary runtime image based on
the public `.977` image; candidate image packaging was not tested. Successful
acquisition, representative media, operator-data acceptance, installed
rollback, and channel handoff remain open. Full details are in the
[migration guide](../migrate-from-bookshelfng-to-chaptarrng.md#exact-head-artifact-repeat-2026-10-19).

**Reviewed:** 2026-10-19. **Status:** BookshelfNG `0.4.21.71` is the published
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
not a release. BookshelfNG tag-triggered image/release publishing, manual
distribution retries, and the legacy bridge now also require the separate
`BOOKSHELFNG_RELEASE_READY=true` gate, which remains unset. ChaptarrNG PR #127
merged to `main` as `b3089a39` with supplemental catalogs, per-field
preferences, and exact-identity recovery of unmapped files. Linux, macOS,
Windows, PostgreSQL migration, CodeQL,
dependency/security, and release-note checks passed on its exact head. Four
provider-dispatch findings on an earlier head were reviewed as false positives:
provider IDs select allowlisted public metadata APIs and do not grant access.
The merged source is not in public `.977`; converted-data and settings
acceptance remain open. ChaptarrNG PR #129 merged to `main` as `949ae3dd`;
its clean head `a671f4b3` passed hosted Linux, macOS, Windows, PostgreSQL
migration, CodeQL, dependency/security, and release-note checks. It ports
BookshelfNG's opt-in M4B settings, tagged track ordering and chapter titles,
original-track fallback, and move/copy source handling. A synthetic two-track
smoke using the `.977` toolchain preserved supplied chapter titles and offsets.
At the 2026-10-19 checkpoint, then-draft ChaptarrNG PR #131 candidate
`12f290bd` passed the six-case
tool-enabled synthetic importer smoke 6/6 in the checked-in Debian Bookworm
image with `m4b-tool` 0.5.2 and `mp4v2` 2.1.1. Successful cases verify tagged
order, chapter titles and offsets, metadata, registration, Move-mode cleanup,
and Copy-mode source retention. Failure cases verify fallback to separate
original-track imports in both modes when FFprobe cannot read a source and
when `m4b-tool` fails after a controlled FFmpeg conversion error. Linux CI now
runs the test through `integration/Dockerfile.m4b-test`; mocked fallback tests
also remain. Embedded-chapter Move/Copy tests and TagLib write/reprobe checks passed on the then-draft candidate c4fa in exact-head Linux Build 39288736177. The run also verified source cleanup after profile-based multipart merges while Copy mode retains originals. Representative media and restart/resume remain open. The merged source change remains unpublished.
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
One populated Linux/amd64 run retained the source tables and rows; some books
needed media classification, and test-map choices were not reviewed as
correct. A separate private populated migration-158 SQLite snapshot passed
preview, apply, and rollback on the public .977 Linux image on 2026-10-18. The
preview source stayed unchanged; apply and rollback retained backups matching
their logical database contents, and SQLite integrity and foreign-key checks
passed. This validates one database round trip, not classification of the
ambiguous records or installer and client continuity. The current
converter keeps unresolved records in both catalogs,
unmonitored, and writes a review file, but it does not classify them. The
final-release decision and helper do not close the feature, data, or
installation-channel acceptance gates. PostgreSQL, complete
settings/identity behavior, rollback on every real deployment, and package
handoff remain open. PostgreSQL conversion is supported by no published ChaptarrNG release. Earlier exact-head run [39175250100](https://github.com/snapetech-org/chaptarrng/actions/runs/39175250100) on PR head `e4db2d46` passed Linux, macOS, Windows, the 4/4 PostgreSQL fixture, release-note and receipt checks, CodeQL, dependency review, secret scan, and NuGet submission. The final Linux artifact passed synthetic provider-mode refusal, Goodreads and Hardcover identity mapping, normal-startup conversion, API, and rollback checks. At that earlier checkpoint, PR #131 code head `2c0401fc` passed exact-head hosted validation in
[run 39196795646](https://github.com/snapetech-org/chaptarrng/actions/runs/39196795646):
Linux, macOS, and Windows builds/tests, the four PostgreSQL migration fixtures,
release-note, CodeQL, dependency/secret scans, NuGet submission, and runner
receipt reconciliation. Disposable-fork validation was skipped by its gate.
These merged-source checks do not establish operator-data, parity, installed
rollback, or channel acceptance. ChaptarrNG `main` remains unsupported for operator cutover.

## Earlier candidate evidence checkpoints — 2026-10-19

The details below record migration and feature checks on prior PR #131 checkpoints. The merged source and latest pre-merge exact-head CI are summarized at the top; prior-head evidence remains historical.

BookshelfNG source snapshot is `6e1a62e12`. It includes an Editions and Narrations tab
backed by `GET /api/v1/book/{id}/editions/catalog` and advertises
`editionCatalog` for SeerrNG edition cards. ChaptarrNG `main` now includes the
same book-details tab and series narrator comparison. Candidate code snapshot
`8b4c6e23` integrates that current source with the migration, rollback,
facade-specific provider IDs, proxied covers, and file-backed ownership.
Local frontend and release-note preview checks pass. Its release-note
contract, dependency review, security scan, and NuGet checks pass. CodeQL
[39205449712](https://github.com/snapetech-org/chaptarrng/actions/runs/39205449712)
passes; cross-platform Build
[39205452341](https://github.com/snapetech-org/chaptarrng/actions/runs/39205452341) passed Linux, macOS, Windows, PostgreSQL migration, release-note, and native-runner receipt checks. Public `.977` predates the catalog UI.

At the earlier media-move checkpoint, ChaptarrNG head `2c0401fc` resolved
registered book sidecars from the linked book's format root, rejects relative
paths that escape an author's configured folders, and stores moved sidecars
relative to the destination format root. Focused regression cases cover
format-root and shared-root sidecars and path traversal. Run `39195460843`
passed Linux, macOS, PostgreSQL, release-note, CodeQL, dependency, and security
checks but exposed four Windows fixture failures caused by hardcoded POSIX
paths; `2c0401fc` makes the fixture paths native and fully qualified. Exact-head
run [39196795646](https://github.com/snapetech-org/chaptarrng/actions/runs/39196795646)
passed on head 2c0401fc, including Windows tests. PR #131 later merged to
ChaptarrNG `main` on 2026-10-20; the source remains unpublished pending the
retirement gates.

Candidate build `0.9.978.0` passed migration preview, apply, rollback preview,
and rollback against a task-scoped copy of a private populated migration-158
SQLite snapshot with `HARDCOVER=true`. The live BookshelfNG service remained
running; candidate commands targeted only the copy, and network access was
not blocked for those commands. The source snapshot remained unchanged. Apply
passed integrity and foreign-key checks; rollback restored a byte-identical
source backup and preserved the converted database separately. Native
Hardcover identities were retained for migrated authors, books, and editions.
The public `.977` round trip had established structural integrity only: it
maps bare numeric IDs to Goodreads even for native Hardcover sources, so do
not apply `.977` to native Hardcover data.

The populated candidate exercise also exposed files referencing missing
editions and history rows whose file and source-book identities disagreed.
The current importer preserves those files as unmapped and keeps conflicting
history on its source book without unsafe links. Focused importer,
edition-catalog, series-catalog, and capability fixtures pass 52/52 locally.
This is one populated SQLite
candidate rehearsal, not complete operator acceptance. Ambiguous-media review,
older real schemas, PostgreSQL operator data, full feature parity, installed
rollback, and channel acceptance remain open. PR #131 code head `2c0401fc` passed exact-head hosted
validation in [run 39196795646](https://github.com/snapetech-org/chaptarrng/actions/runs/39196795646), including Linux, macOS, and Windows builds/tests, PostgreSQL fixtures, release-note, CodeQL, dependency/security, NuGet, and runner-receipt checks. Docs-only checkpoint `898b72fd` passed hosted run [39198708193](https://github.com/snapetech-org/chaptarrng/actions/runs/39198708193). Docs-only checkpoint `ddec3e81` also passed [run 39199730309](https://github.com/snapetech-org/chaptarrng/actions/runs/39199730309). Earlier docs-only head `353aeba1` passed exact-head validation in [run 39201211634](https://github.com/snapetech-org/chaptarrng/actions/runs/39201211634); CodeQL, dependency/security, dependency-review, and NuGet checks passed too. Disposable-fork validation was skipped by its gate. Earlier retirement candidate code snapshot `8b4c6e23` integrated then-current ChaptarrNG `main`, including the Editions and Narrations tab and series narrator comparison, and carries the migration, rollback, provider-identity, and media-move work. Local translation, TypeScript, targeted ESLint/Stylelint, and release-note preview pass. Its release-note contract, dependency review, security scan, and NuGet checks pass. CodeQL run [39205449712](https://github.com/snapetech-org/chaptarrng/actions/runs/39205449712) passes; exact-head cross-platform Build [39205452341](https://github.com/snapetech-org/chaptarrng/actions/runs/39205452341) passed Linux, macOS, Windows, PostgreSQL migration, release-note, and native-runner receipt checks. Operator-data and channel acceptance remain open. All releases remain frozen.

The migration accepts one database per appdata directory. ChaptarrNG refuses
two non-empty legacy database candidates rather than choosing or combining
them; the BookshelfNG helper on source `main` ignores an empty candidate and
refuses two populated candidates before it creates an archive. This helper fix
and regression coverage merged in BookshelfNG PR #154 as `de782d5`, but are not
in the published `.71` helper. The `.71` helper may print a zero-byte
`readarr.db` beside a populated `audioarr.db`; ChaptarrNG `.977` independently
ignores empty legacy files when selecting its source. For two independent
installations, migrate each appdata directory separately. To make one combined
library, use the manual two-instance media-consolidation runbook in the root
README, then migrate the verified BookshelfNG instance; that workflow does not
merge database history, profiles, monitoring, or settings.

This is a feature-level matrix, not a
claim that similarly named features are equivalent.

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
| Books index Both filter | Browse all audiobook and ebook catalog records together while keeping each format's state distinct | ChaptarrNG `main` lists each record separately with a format label; status, monitoring, and quality profiles follow its media type. Focused tests cover paged query behavior, custom filters, and row-level profile selection. Commit `a733e5f4` keeps paged mass-search confirmation open until matching IDs load and the command queues; ID lookup, queue-start, Select All, bulk Update, refresh, and RSS Sync failures have retry paths. Filter or format changes cancel an unstarted search, and queue retries reuse the same IDs. These changes are not in `.977`. | **Source implementation added; browser acceptance open.** Verify paging, filters, sorting, narrator controls, selected-row and bulk edits, profile selection, and reload behavior on a representative mixed library. |
| Grouped Bookshelf Formats view | View audiobook and ebook records together when they represent the same work | ChaptarrNG `main` groups only matching Hardcover, Goodreads, or Open Library work IDs, keeps format details and progress separate, and applies bulk monitoring to both. Focused identity and API fixtures exist; browser acceptance is open. | **Source implementation added; mixed-library acceptance open.** Test matched aliases, mismatched and missing IDs, duplicates, reload/retry, per-book and bulk monitoring, and layout against converted data. |
| Format-specific author paths, quality profiles, and metadata profiles | Per-format paths and profile overrides, with author defaults as fallback | Commit `83f66c36` adds `AutoInitializeFormatSpecificAuthorPaths`, disabled by default, to the API, config, and Media Management settings. When enabled, it initializes missing format roots for new authors only; explicit paths and existing files are untouched. Migration carries the setting and maps enabled BookshelfNG ebook/audiobook roots to ChaptarrNG defaults when those defaults are empty; configured ChaptarrNG defaults win. Focused fixtures cover enabled/disabled creation, explicit roots, mapping, and precedence. Public `.977` predates this change. | **Source parity added; operator acceptance open.** Verify settings and profile fallback behavior on converted operator data, and exercise creation, import, upgrade, rename, scan, and move flows for both formats. |
| Native Hardcover metadata and request controls | Direct GraphQL provider, per-process pacing/cache, batched lookups, rate-limit recovery, and identity routing | Merged ChaptarrNG PR #131 puts a native Hardcover GraphQL proxy on `main`, routes explicit Hardcover IDs through it, maps saved `HardcoverAuth` to `HardcoverApiToken`, and interprets bare numeric source IDs according to the active `HARDCOVER`/`HARDCOVER_NATIVE` mode. The migration helper exposes `--provider-mode` so preview and apply use that same source mode. | **Open blocker (operator acceptance).** A line-by-line comparison on 2026-10-20 found the executable request pacing, retry, rate-limit cooldown, daily quota, cache, paging, batching, and GraphQL mapping logic matches BookshelfNG. Differences are product identity, narrator resource shape, error text, and saved credential property (BookshelfNG uses `HardcoverAuth`; ChaptarrNG uses `HardcoverApiToken`). ChaptarrNG commit `1f56de51` adds mocked regression tests for the 429/`Retry-After` pause, daily quota reserve for interactive searches, and work cache reuse. Exact-head Build [39413811593](https://github.com/snapetech-org/chaptarrng/actions/runs/39413811593) completed successfully on Linux, macOS, and Windows, including PostgreSQL migration, native-runner receipts, migration-installer fingerprint, and service upgrade/rollback checks. Live provider/API behavior and representative converted-data acceptance remain open. The provider and helper changes are source-only and not in published ChaptarrNG .977 or BookshelfNG .71. |
| Selectable supplemental catalogs and per-field source preferences | Hardcover, Readarr-compatible API, Open Library, Google Books, LOC, Gutendex, Internet Archive, NDL, Europeana, and optional Apify adapters | ChaptarrNG main after PR #127 (`b3089a39`) includes Open Library, Google Books, LOC, Gutendex, Internet Archive, NDL, Europeana, and Apify with selectable sources, qualified identities, and per-field choices. Exact-head Linux, macOS, Windows, PostgreSQL migration, CodeQL, dependency/security, and release-note checks passed. It is not in published `.977`; Hardcover and the primary metadata API retain their separate resolvers. | **Source port merged; open blocker.** Review provider/settings migration, cached credential handling, per-field matching, fallback behavior, and converted operator data before accepting the row. |
| Cross-catalog recovery and import matching | Retry unmapped files across configured catalogs; ISBN/ASIN/provider-ID and normalized-name matching; configurable title threshold | ChaptarrNG main after PR #127 searches exact ISBN/ASIN, canonical provider IDs, Goodreads work/edition IDs, or exact normalized title and author. Candidates must match supplied identity evidence, media type, and stable work/author IDs; ambiguous or conflicting IDs stay unmatched, and accepted results queue only the existing pending-author import. It never attaches files directly. Focused tests cover exact Goodreads and canonical provider-ID lookup, mismatched IDs, conflicting tags, identifier checks, ambiguity, and title matching; exact-head hosted validation passed. PR #130 adds the lossy 50–66 Aggressive, 67–82 Balanced, and 83–99 Strict mapping when no explicit mode exists; invalid values fail closed. | **Source port merged; open blocker.** Accept identifier/name, threshold approximation, media-type, ambiguity, and pending-import behavior on converted operator data. The mapping is not algorithm-equivalent and is not in public `.977`. |
| Weighted edition terms, preferred series, and narrator-aware matching | Profile terms and series preferences; narrator tags and edition evidence affect audiobook ranking | The consolidation branch adds profile-based weighted edition scoring and preferred-series selection for filenames, ebook tags, Calibre, and AudioBookShelf metadata; stronger match evidence remains authoritative | **Source port merged; retirement acceptance remains open.** Preserve weights and series choices, neutral handling of missing data, tie behavior, and manual-review boundaries; test the full Bookshelf edge-case set after profile/database conversion. |
| Add New search preference | Optional “search as you type” behavior alongside submit-to-search | ChaptarrNG `main` carries the optional browser preference and defers Hardcover searches until provider configuration is known. The preference is browser-origin scoped and is not in published `.977`. | **Source behavior implemented; browser acceptance remains open.** Check preference persistence, same-query resubmission, clearing during a slow request, and a host/origin change. |
| Interactive series-pack search | Search indexers for a multi-book series release and review its files individually | ChaptarrNG `main` adds a series-row search action and API query. It builds the query from the local series links, author catalog, and series media type, then retains the books for Manual Import. A focused C# fixture covers ordered author-scoped books and full import context. | **Source port implemented; live workflow acceptance remains open.** Confirm indexer results, grab, queue, and per-file Manual Import assignments in a running instance. |
| Audiobook M4B merge and chapter metadata | Opt-in multi-track merge with track ordering and chapter creation | ChaptarrNG PR #129 merged the opt-in merge setting, tagged track order/titles, conservative conversion fallback, and Move/Copy source handling. PR #131 added synthetic embedded-chapter Move/Copy tests and a TagLib write/reprobe check. These tests exposed that a successful profile-based multipart merge left sources behind in Move mode; fixture isolation alone did not fix it. Commit `c4fa8125` now cleans sources after successful profile merges while Copy mode retains them. Exact-head Build [39288736177](https://github.com/snapetech-org/chaptarrng/actions/runs/39288736177) passed Linux's full suite and pinned-tool M4B checks, PostgreSQL migration smoke, and release-note contract. Windows build and full test steps passed; macOS was cancelled before starting, so the cross-platform matrix is incomplete. CodeQL, security, dependency review, and NuGet checks passed. | **Source port merged; acceptance remains open.** Validate representative media and restart/resume behavior with representative Move/Copy deployments. |
| Media import replacement and free-space guards | Preserve unrelated ebook containers and prevent imports that exceed configured free-space limits | ChaptarrNG `main` at `ac85470a` filters upgrade candidates to compatible audio formats or the same ebook extension before quality checks and deletion. It also checks the managed import destination against `MinimumFreeSpaceWhenImporting`, honors the skip setting, and rejects low-space imports before staging files. Regression fixtures cover mixed-format replacement and low-space copies. | **Source fixes are on main; exact-head CI and operator acceptance remain open.** Verify ebook/audiobook coexistence, EPUB/KEPUB/MOBI/AZW3 handling, configured free-space boundaries, and rollback against representative libraries. |
| Vendored TagLibSharp MPEG-4 `chpl` handling | Patch includes byte-preserving chapter-list writes | The local Chaptarr candidate vendors this fork and passes a synthetic version-1 `chpl` fixture that checks exact atom preservation during a title write. The vendor includes its LGPL-2.1 `COPYING` file; its strong-name key matches the key already committed with the BookshelfNG vendor source. | **Local port and focused regression pass; broader compatibility remains an open blocker.** Validate representative M4B files, tag edits, conversion outputs, and failure cases; review continued use of the vendor signing identity and upstream the supported implementation. |
| Existing torrent adoption and safe seeding | Can adopt tracked torrent data without removing the seed | ChaptarrNG `main` now checks torrent hashes before grabs, offers an explicit interactive adoption, and tracks the existing client ID without a second download. Automated searches skip matching torrents. Unit tests cover matching/adoption, stale and unavailable client cases, no second download, and no MAM slot reservation. Existing tests cover same-category continuation and seeding. | **Source implementation added; acceptance remains open.** Rehearse matching and wrong categories, completed and seeding states, completion import, and restart behavior with supported clients and representative downloads. |
| Direct Download with ordered sources and browser-assisted links | Ebook search, API-key downloads, optional browser fallback, durable transfer state, and redirect validation | ChaptarrNG source `a1146edd` restores KEPUB, MOBI, and AZW3 catalog search, resolves KEPUB detail-page links, and marks direct ebook releases with Books/Ebook category 7020. Regression fixtures cover the catalog query/results, KEPUB resolution, and category. Build [39524671037](https://github.com/snapetech-org/chaptarrng/actions/runs/39524671037) failed the KEPUB extension-label assertion; source `a1146edd` fixes it by preferring the filename extension and matching metadata tokens. The current exact-head Build [39539307423](https://github.com/snapetech-org/chaptarrng/actions/runs/39539307423) is running on `bebc5e8a`; prior Build [39530803846](https://github.com/snapetech-org/chaptarrng/actions/runs/39530803846) passed Linux, macOS, and PostgreSQL but failed the unrelated Windows path-normalization fixture, now fixed in the test fake; earlier Build [39239940373](https://github.com/snapetech-org/chaptarrng/actions/runs/39239940373) passed Linux, macOS, Windows, PostgreSQL migration, and runner-receipt checks. Existing fixtures cover ordered source fallback, legacy URL-array settings, API-key preservation/redaction, durable state across restart, interrupted-transfer handling, browser fallback recovery, redirect-hop validation, private-address rejection, and redirect-body clearing. | **Source-level settings and recovery compatibility covered; retirement acceptance remains open** | Validate representative saved settings, configured sources and clients, installed-state handoff, supported browser architectures, and source/transfer recovery on a deployed instance. Verify interrupted transfer/restart on an installed instance before closing the row. |
| BookLore BookDrop uploads and BookOrbit transition | Upload imported books through BookLore's BookDrop API; BookOrbit is its successor | ChaptarrNG preserves the BookLore notification provider, credentials, settings, and `OnReleaseImport` trigger in conversion and source backup. Merged PR #131 adds BookOrbit as a separate user-configured destination. Mock tests cover streaming, redirects, credential/permission rejection, size rejection, and partial batches. An isolated BookOrbit v3.2.0 instance passed setup, login, Book Dock access, EPUB upload/listing, and unsupported-file rejection. This source implementation is not in public ChaptarrNG `.977`. | **Open blocker.** Do not rewrite a BookLore URL or password as BookOrbit credentials. Test BookOrbit processing of a production book and document a real-user transition using converted BookLore settings. Preserve streaming, redirects, supported formats and size behavior; test rejection/recovery and inspect Book Dock before retrying partial batches. |
| Import-list and notification providers | Goodreads public shelves and owned books, Goodreads bookshelf and owned-book notifications, and Hardcover public lists/statuses | Merged ChaptarrNG PR #131 adds BookshelfNG's `HardcoverImport` provider and ports the OAuth-backed Goodreads bookshelf/owned-book lists and shelf/owned-book write notifications. It preserves complete matching settings, blocks missing or partial OAuth credentials without reporting values, and keeps public Goodreads shelves available with a valid user ID and no OAuth. Commit `a733e5f4` adds visible Hardcover connection loading/status and retry, plus per-list preview/history retry that preserves available API errors and discards stale preview results after close; these UI changes are not in public `.977`. | **Open blocker.** Goodreads API acceptance with saved existing credentials has not been verified; Goodreads has announced API retirement and no longer issues new developer keys. Test the imported providers against representative existing accounts, confirm shelf/private-owned data and write behavior, verify settings and secrets remain private, exercise provider rollback on converted operator data, and verify preview/history retry and connection-status refresh against saved accounts. The compatibility source and new UI recovery are not in a published ChaptarrNG release. See the [Goodreads API deprecation notice](https://www.goodreads.com/topic/show/21788520-api-deprecation). |
| Provider settings, MyAnonamouse, Calibre, and Audiobookshelf sidecars | Merged PR #131 source checks provider implementation and `ConfigContract` compatibility across indexers, download clients, import lists, notifications, and metadata. It retains settings only when their contract and serialized fields match a Chaptarr provider. Unsupported pairs or unknown fields are disabled in the staged copy, reported without secret values, and block apply before promotion. `LegacyAudiobookshelfMetadata` aliases and sidecar consumers are also checked. Fixtures cover QBittorrent categories, MyAnonamouse and Direct Download indexers, supported Goodreads and BookLore contracts, unsupported plugins, unknown settings, and metadata consumers. Exact-head Build [39332160991](https://github.com/snapetech-org/chaptarrng/actions/runs/39332160991) passed on application-code head `7b4c66e3`. | **Implementation safety covered; provider acceptance remains open.** Verify live API behavior, saved credentials, and full settings on representative converted data. Goodreads existing-key/API availability is separately uncertain; unknown plugins remain blocked pending an adapter or explicit retirement decision. |
BookshelfNG `0.4.21.71` remains its final public release; ChaptarrNG `v0.9.977` remains the latest public release. ChaptarrNG `main` and application code are at [`bebc5e8a`](https://github.com/snapetech-org/chaptarrng/commit/bebc5e8a923d7ebc4af7cc86b0bbec5e93f51859). The source includes the disabled-by-default author-path setting from BookshelfNG issue [#114](https://github.com/snapetech-org/bookshelfng/issues/114), its migration support, the format-specific metadata-profile refresh fix, and the corrected Calibre English language tag. These changes remain unpublished in `.977`. Exact-head Build [39539307423](https://github.com/snapetech-org/chaptarrng/actions/runs/39539307423) is running on Linux, macOS, Windows, and PostgreSQL; preceding Build [39538783209](https://github.com/snapetech-org/chaptarrng/actions/runs/39538783209) was cancelled when the Calibre tag correction landed before its platform matrix completed. Security analysis [39539307274](https://github.com/snapetech-org/chaptarrng/actions/runs/39539307274), Semgrep [39539307245](https://github.com/snapetech-org/chaptarrng/actions/runs/39539307245), Trivy [39539307454](https://github.com/snapetech-org/chaptarrng/actions/runs/39539307454), and dependency submission [39539323460](https://github.com/snapetech-org/chaptarrng/actions/runs/39539323460) passed; CodeQL [39539307127](https://github.com/snapetech-org/chaptarrng/actions/runs/39539307127) is running. The format-profile fixture passes 5/5 locally and the Calibre language fixture 4/4; earlier focused author/migration fixtures pass 11/11 and configuration persistence 1/1. No release, tag, package, image, installer, or migration bridge has been published. Representative operator-data migration and rollback, complete feature/data acceptance, provider and SeerrNG workflows, installed update-channel handoff, and operator acceptance remain open; keep BookshelfNG in service.
| Optional privacy-preserving diagnostics | Separate module, explicit opt-in, aggregate-only event schema | ChaptarrNG `v0.9.977` publishes the optional aggregate-only module; it honors the legacy enable flag only when the archived BookshelfNG plugin marker is present and requires endpoint/token environment variables to be carried forward. Artifact verification passed on Linux, macOS, and Windows. | **Replacement published; migration gate open.** Verify an installed transition with and without the archived marker, preserved environment variables, and default-off behavior; then close this feature row. |
| Scoped SeerrNG access, API aliases, proxy and request controls | Restricted key, compatibility routes, format-specific availability, hardened proxy/auth boundaries, edition catalog, and Editions and Narrations UI | A populated synthetic smoke passed on 2026-10-18 against ChaptarrNG candidate `0.9.978.0` at code head `1a0a1cf7` and SeerrNG `0b267d526`: it verified status/capability discovery, one audiobook through SeerrNG's paged-library adapter, migrated audiobook and ebook provider identities, and denial of administrative and unrelated command routes with the restricted key. A second isolated Compose smoke against an earlier PR #131 source head `ddec3e81` (application-code snapshot `2c0401fc`) and SeerrNG `10f06eab9` passed capability discovery, empty paged-library access, and restricted-key denials. The 2026-10-19 follow-up lifecycle probe, committed in PR #131 at `d9713604`, used SeerrNG's real `ReadarrAPI` adapter against the prebuilt candidate from Build 39239940373 and passed synthetic unavailable-author request creation, polling, cancellation, and terminal-state verification. Both scripts later passed through the checked-in `Dockerfile.build` on PR head `7cfb5d87`, after the harness added a one-shot initializer for its disposable `/books` volume. Successful acquisition and the remaining converted-data and operator acceptance checks remain open. ChaptarrNG `main` now includes the edition catalog, Editions and Narrations tab, series narrator matrix, and wanted-edition variants. Application snapshot `29852b13` also ports explicit trusted-proxy and CORS allowlists, per-client rate limits, a bounded general body size, and the BookshelfNG request-ID header; the backup restore upload retains a separate 1 GiB limit. The first exact-head Build [39392889130](https://github.com/snapetech-org/chaptarrng/actions/runs/39392889130) failed on test-fixture compilation; follow-up Build [39394240337](https://github.com/snapetech-org/chaptarrng/actions/runs/39394240337) passed Linux, macOS, Windows, PostgreSQL migration, and native-runner receipt checks. Windows also passed the migration installer fingerprint and service upgrade/rollback smoke. The exact-head Linux artifact converted the checked-in schema-158 fixture to schema 121, retained an integrity-checked source backup, and passed SeerrNG migrated-record, authorization, and pending-import cancellation checks. The synthetic media files are placeholders. These controls and migration changes are not in `.977`. Earlier PR #131 code snapshot `8b4c6e23` integrated then-current `main` with facade-specific edition identity, proxied covers, and file-backed ownership. Its release-note contract, dependency review, security scan, and NuGet checks pass. CodeQL [39205449712](https://github.com/snapetech-org/chaptarrng/actions/runs/39205449712) passes; Build [39205452341](https://github.com/snapetech-org/chaptarrng/actions/runs/39205452341) passed Linux, macOS, Windows, PostgreSQL migration, release-note, and native-runner receipt checks. Local frontend checks pass. | **Open blocker.** Successful fulfillment and retries, availability statistics, history, converted-record behavior, saved production settings, unchanged SeerrNG clients, proxy deployments, and operator acceptance remain unvalidated. Run these against converted data and unchanged client configuration; the synthetic cancellation probe and HTTP-control port do not close this row. |
| Encrypted backups and restore | Passphrase-protected portable archives and per-format profiles | ChaptarrNG PR #131 includes BKSENC01 `.enc` export and restore (introduced at historical candidate `38be9422`, present in code commits `b7e900d4` and `0e881d92`) alongside recognized BookshelfNG ZIP restore. The encryption service was cross-checked against BookshelfNG source; focused tests cover round-trip, wrong passphrases, tampering, truncation, malformed input, and cleanup. Current source `main` also accepts raw SQLite backup uploads named `.db` or with the legacy `.xml` suffix; `.xml` remains a filename only. These restore paths are not in public `.977`. ChaptarrNG scheduled `.zip.enc` remains a separate format. | **Source implementation merged; acceptance remains open.** Prove legacy archive recovery, passphrase handling, rollback, and profile conversion on representative data; never expose credentials in logs. |
| .NET 10, dependency/security fixes, and platform builds | .NET 10 releases, broad native/package matrix, and maintained security/dependency patches | ChaptarrNG uses .NET 10 and has a different dependency/build matrix | **Latest exact-head Build running; acceptance remains open.** Build [39539307423](https://github.com/snapetech-org/chaptarrng/actions/runs/39539307423) targets code head `bebc5e8a`; prior Build [39538783209](https://github.com/snapetech-org/chaptarrng/actions/runs/39538783209) was superseded by the Calibre language-tag fix before the platform matrix completed. CodeQL [39539307127](https://github.com/snapetech-org/chaptarrng/actions/runs/39539307127) is running; dependency submission [39539323460](https://github.com/snapetech-org/chaptarrng/actions/runs/39539323460), Semgrep [39539307245](https://github.com/snapetech-org/chaptarrng/actions/runs/39539307245), security analysis [39539307274](https://github.com/snapetech-org/chaptarrng/actions/runs/39539307274), and Trivy [39539307454](https://github.com/snapetech-org/chaptarrng/actions/runs/39539307454) passed. Representative data and installed-channel acceptance remain open. |
| Release, package, and update channels | Containers, Unraid, Debian/RPM, AUR, PPA, Windows, macOS/Linux/FreeBSD, AppImage, Flatpak, Chocolatey, and Helm; YunoHost publishing retired | ChaptarrNG has its own release and package identities. A local BookshelfNG-identity AUR `.977` candidate passed pacman upgrade/downgrade and active systemd service migration/restore against synthetic populated migration-158 data. A Fedora 44 RPM transaction upgraded the published BookshelfNG `.71` RPM to a local `.977` bridge candidate and downgraded back with config/data canaries; it used `rpm --nodeps` and mocked `systemctl`. The `slskdn/bookshelfng` COPR repo currently has no package entries for Fedora 43/44/45/Rawhide x86_64. | **Open blocker.** AUR acceptance with operator data and host-specific settings remains open. The RPM package transaction did not exercise live COPR/DNF, a real systemd service, or database migration. COPR publication/retirement, Chocolatey publication, Unraid, and historical/manual channel handoffs remain open; no universal automatic redirect exists. |
| All other fork changes | Current inventory pins BookshelfNG source `2811718076d84777a1b1132e4e5d2abd21231229` to ChaptarrNG target `bebc5e8a923d7ebc4af7cc86b0bbec5e93f51859`: 732 post-fork commits, 1,119 paths, 85 reviewed mappings, 681 dispositions, and 438 open paths (136 unmapped, 302 semantic review). | Path inventory is not feature-parity proof. | Resolve every path and validate behavior against representative data before retirement. |

## Evidence and limits

The [consolidation report](chaptarr-consolidation.md) records exact source and
target revisions, current implementation findings, the data-conversion
contract, release-channel matrix, test results, and open gates. The local
Release-mode Core suite passed 4,065 tests with 0 failures and 3 skipped on the
same application sources as the current integration head. Twenty-three
focused migration fixtures also passed,
including synthetic rollback after a post-migration write. The standard image passed preview,
apply, and startup against separate copies of one real populated migration-158
database; this is bounded evidence because some books had no derivable media
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
duplicating records. The retained backup matched every source table
definition and row; the promoted database passed integrity and foreign-key
checks. Seven
BookLore proxy tests pass, and the explicit live BookLore v2.4.0
upload-contract fixture passes 1/1.
The Release console build has zero warnings or errors.
Additional focused reruns on the candidate checkpoint at that time passed 16 migration-safety
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
unchanged and accounted for every source row; apply retained a backup matching
the source table definitions and every row; normal startup served the UI
and retained the existing port, URL base, API key, SSL setting, and Docker
image-pull update mechanism. The live BookshelfNG service was not changed.
The media choices used for apply were test-only and were not reviewed as
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
